from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
import math

import pytest

from src import (Document, EmbeddingStore, FixedSizeChunker, HeadingChunker,
                 KnowledgeBaseAgent, RecursiveChunker, ChunkingStrategyComparator, compute_similarity)
from src.corpus import chunk_documents, load_corpus
from src.lexical import TfidfEmbedder, extractive_answer


@pytest.mark.parametrize("size,overlap", [(0, 0), (-1, 0), (10, 10), (10, -1)])
def test_fixed_invalid_window(size: int, overlap: int) -> None:
    with pytest.raises(ValueError):
        FixedSizeChunker(size, overlap)


@pytest.mark.parametrize("separators", [None, [], ["\n\n"], [""]])
def test_recursive_preserves_text_and_bounds(separators: list[str] | None) -> None:
    text = "Điều 1. Quy định.\n\n" + "longword" * 30 + "\nKết thúc!"
    chunks = RecursiveChunker(separators, 31).chunk(text)
    assert "".join(chunks) == text
    assert all(0 < len(chunk) <= 31 for chunk in chunks)


def test_heading_retains_context_for_long_sections() -> None:
    chunks = HeadingChunker(120).chunk("# UEH\n\n## Người học\n\n" + "Nội dung. " * 50)
    assert len(chunks) > 1
    assert all("## Người học" in chunk and len(chunk) <= 120 for chunk in chunks)


def test_empty_comparison() -> None:
    assert all(row["count"] == 0 and row["avg_length"] == 0
               for row in ChunkingStrategyComparator().compare("").values())


def test_cosine_rejects_invalid_vectors_and_handles_large_values() -> None:
    for a, b in [([1.0], [1.0, 2.0]), ([math.nan], [1.0])]:
        with pytest.raises(ValueError):
            compute_similarity(a, b)
    assert compute_similarity([1e200, 1e200], [1e200, 1e200]) == pytest.approx(1)


def test_prefilter_runs_before_top_k_and_matches_all_keys() -> None:
    store = EmbeddingStore(embedding_fn=lambda text: [float(text), 1.0])
    store.add_documents([Document("faculty", "100", {"audience": "faculty", "lang": "vi"}),
                         Document("student", "1", {"audience": "student", "lang": "vi"})])
    results = store.search_with_filter("1", 1, {"audience": "student", "lang": "vi"})
    assert results[0]["metadata"]["doc_id"] == "student"
    assert store.search_with_filter("1", 1, {"audience": "student", "lang": "en"}) == []
    assert store.search_with_filter("1", 1, {"absent": None}) == []


def test_duplicate_ids_delete_all_and_isolate_metadata() -> None:
    store = EmbeddingStore()
    doc = Document("chunk", "content", {"doc_id": "parent", "nested": {"x": 1}})
    store.add_documents([doc, doc])
    doc.metadata["nested"]["x"] = 2
    results = store.search("content")
    assert len({r["id"] for r in results}) == 2
    assert results[0]["metadata"]["nested"]["x"] == 1
    results[0]["metadata"]["doc_id"] = "changed"
    assert store.delete_document("parent")
    assert store.get_collection_size() == 0
    assert not store.delete_document("parent")


def test_add_is_atomic_on_embedding_failure() -> None:
    def embed(text: str) -> list[float]:
        if text == "bad":
            raise RuntimeError("backend failure")
        return [1.0]
    store = EmbeddingStore(embedding_fn=embed)
    with pytest.raises(RuntimeError):
        store.add_documents([Document("a", "ok"), Document("b", "bad")])
    assert store.get_collection_size() == 0


def test_vector_dimension_changes_rejected_atomically() -> None:
    store = EmbeddingStore(embedding_fn=lambda text: [1.0] * len(text))
    store.add_documents([Document("a", "a")])
    with pytest.raises(ValueError):
        store.add_documents([Document("b", "bb")])
    assert store.get_collection_size() == 1
    with pytest.raises(ValueError):
        store.search("bb")


def test_concurrent_writes_have_unique_records() -> None:
    store = EmbeddingStore()
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(lambda i: store.add_documents([Document(str(i), "content")]), range(30)))
    assert store.get_collection_size() == 30
    assert len({r["id"] for r in store.search("content", 30)}) == 30


def test_nonpositive_k_and_blank_query() -> None:
    store = EmbeddingStore()
    store.add_documents([Document("a", "content")])
    assert store.search("q", -1) == []
    assert store.search("q", 0) == []
    assert store.search("   ") == []


def test_agent_propagates_filter_and_limits_context() -> None:
    store = EmbeddingStore()
    store.add_documents([Document("a", "evidence" * 50, {"audience": "student"}),
                         Document("b", "faculty only", {"audience": "faculty"})])
    captured: list[str] = []
    def llm(prompt: str) -> str:
        captured.append(prompt)
        return "answer"
    agent = KnowledgeBaseAgent(store, llm, max_context_chars=20)
    assert agent.answer("question", metadata_filter={"audience": "student"}) == "answer"
    payload = json.loads(captured[0].split("\n", 1)[1])
    assert sum(len(e["content"]) for e in payload["evidence"]) <= 20
    assert "faculty only" not in captured[0]
    agent.answer("question", metadata_filter={"audience": "staff"})
    assert len(captured) == 1


def test_actual_corpus_ingestion_and_citations() -> None:
    docs = load_corpus(Path(__file__).resolve().parents[1] / "data/ai-liem-chinh-hoc-thuat")
    assert len(docs) == 10
    chunks = chunk_documents(docs, HeadingChunker(800), "heading")
    assert all("---\ndoc_id:" not in chunk.content for chunk in chunks)
    assert len({c.id for c in chunks}) == len(chunks)
    tfidf = TfidfEmbedder(doc.content for doc in docs)
    store = EmbeddingStore(embedding_fn=tfidf)
    store.add_documents(chunks)
    answer = KnowledgeBaseAgent(store, extractive_answer).answer(
        "At UNA should faculty use AI-detection software as the single means of verifying originality?",
        metadata_filter={"audience": "faculty"})
    assert "https://www.una.edu/" in answer
    assert "EXTRACTIVE BASELINE" in answer


def test_corpus_rejects_missing_metadata(tmp_path: Path) -> None:
    (tmp_path / "bad.md").write_text('---\ndoc_id: "a"\n---\nbody', encoding="utf-8")
    with pytest.raises(ValueError, match="missing"):
        load_corpus(tmp_path)


def test_tfidf_is_normalized_and_handles_unknown_terms() -> None:
    embedder = TfidfEmbedder(["alpha beta", "beta gamma"])
    assert math.hypot(*embedder("alpha beta")) == pytest.approx(1)
    assert embedder("unknown") == [0.0, 0.0, 0.0]
