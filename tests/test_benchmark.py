import json
from pathlib import Path

import pytest

from scripts.import_hiep import parse_log
from scripts.run_benchmark import evaluate, relevant
from src import Document, EmbeddingStore
from src.lexical import extractive_answer

ROOT = Path(__file__).resolve().parents[1]


def test_official_queries_match_member_log() -> None:
    imported = parse_log((ROOT / "ket_qua_benchmark.txt").read_text(encoding="utf-8-sig"))
    queries = json.loads((ROOT / "benchmark/queries.json").read_text(encoding="utf-8"))
    assert len(queries) == 5
    for local, member in zip(queries, imported[0]["queries"]):
        assert (local["id"], local["question"], local["metadata_filter"]) == (
            member["id"], member["question"], member["metadata_filter"])
        assert [e["quote"] for e in local["evidence"]] == member["evidence_markers"]
        assert [local["evidence"][0]["doc_id"], *local["evidence"][0]["alternative_doc_ids"]] == member["gold_doc_ids"]
    assert [e["content_score"] for e in imported] == [5, 2, 6]


def test_log_import_rejects_inconsistent_totals() -> None:
    text = (ROOT / "ket_qua_benchmark.txt").read_text(encoding="utf-8-sig")
    text = text.replace("TOTAL fixed: naive(doc_id)=10/10   content(evidence)=5/10",
                        "TOTAL fixed: naive(doc_id)=10/10   content(evidence)=9/10")
    with pytest.raises(ValueError, match="total"):
        parse_log(text)


def test_evidence_alternative_source_and_secondary_marker() -> None:
    query = {"evidence": [{"doc_id": "general", "alternative_doc_ids": ["faculty"], "quote": "primary"},
                          {"doc_id": "general", "quote": "secondary"}]}
    result = {"id": "r", "content": "primary", "metadata": {"doc_id": "faculty"}, "score": 1.0}
    assert relevant(result, query)
    assert not relevant({**result, "metadata": {"doc_id": "wrong"}}, query)
    assert not relevant({**result, "content": "secondary", "metadata": {"doc_id": "general"}}, query)


def test_multi_chunk_coverage_is_not_same_as_primary_rank() -> None:
    store = EmbeddingStore(embedding_fn=lambda text: [1.0])
    store.add_documents([Document("d", "secondary"), Document("d", "primary")])
    query = {"id": "Q", "question": "facts?", "metadata_filter": None, "gold_answer": "two facts",
             "evidence": [{"doc_id": "d", "quote": "primary"}, {"doc_id": "d", "quote": "secondary"}]}
    result = evaluate(store, query)
    assert result["evidence_rank"] == 2
    assert result["evidence_coverage"] == 1
    assert result["anchor_score"] == 1


def test_extractive_preserves_list_details_and_negation() -> None:
    content = "# Policy\n\nA similarity threshold is a warning.\n\n- 20% or more.\n\nIt is not proof by itself."
    prompt = "instructions\n" + json.dumps({"question": "What similarity threshold?", "evidence": [
        {"chunk_id": "d:0", "source_url": "https://example.org/policy", "content": content}]})
    answer = extractive_answer(prompt)
    assert "20% or more" in answer
    assert "not proof by itself" in answer
    assert "[d:0](https://example.org/policy)" in answer
