"""Reproducible offline experiment: python -m scripts.run_benchmark."""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import time
import unicodedata
from pathlib import Path
from typing import Any

from src import (ChunkingStrategyComparator, EmbeddingStore, FixedSizeChunker,
                 HeadingChunker, KnowledgeBaseAgent, RecursiveChunker,
                 SentenceChunker, compute_similarity, _mock_embed)
from src.corpus import Chunker, chunk_documents, load_corpus
from src.lexical import TfidfEmbedder, extractive_answer
from src.store import SearchResult

ROOT = Path(__file__).resolve().parents[1]


def normalized(text: str) -> str:
    return " ".join(unicodedata.normalize("NFC", text).casefold().split())


def matches_evidence(result: SearchResult, item: dict[str, Any]) -> bool:
    accepted = [item["doc_id"], *item.get("alternative_doc_ids", [])]
    return (result["metadata"]["doc_id"] in accepted and
            normalized(item["quote"]) in normalized(result["content"]))


def relevant(result: SearchResult, query: dict[str, Any]) -> bool:
    # Anchor rank and total coverage are different metrics. A later marker alone
    # must not count as a hit on a question whose primary fact is missing.
    return matches_evidence(result, query["evidence"][0])


def evaluate(store: EmbeddingStore, query: dict[str, Any], filtered: bool = True) -> dict[str, Any]:
    metadata_filter = query["metadata_filter"] if filtered else None
    started = time.perf_counter()
    results = store.search_with_filter(query["question"], 3, metadata_filter)
    latency = (time.perf_counter() - started) * 1000
    hits = [relevant(result, query) for result in results]
    answer = KnowledgeBaseAgent(store, extractive_answer).answer(query["question"], 3, metadata_filter)
    coverage = sum(any(matches_evidence(r, item)
                       for r in results) for item in query["evidence"]) / len(query["evidence"])
    evidence_rank = hits.index(True) + 1 if any(hits) else None
    return {"query_id": query["id"], "question": query["question"],
            "metadata_filter": metadata_filter, "gold_answer": query["gold_answer"],
            "top3": [{**result, "relevant": hit} for result, hit in zip(results, hits)],
            "hit_at_3": any(hits), "evidence_rank": evidence_rank,
            "anchor_score": 2 if evidence_rank == 1 else (1 if evidence_rank else 0),
            "reciprocal_rank": 1 / evidence_rank if evidence_rank else 0,
            "precision_at_3": sum(hits) / 3, "evidence_coverage": coverage,
            "search_ms": latency, "agent_answer": answer,
            "answer_contains_all_gold_spans": all(normalized(e["quote"]) in normalized(answer)
                                                   for e in query["evidence"])}


def run(output: Path) -> dict[str, Any]:
    directory = ROOT / "data" / "ai-liem-chinh-hoc-thuat"
    documents = load_corpus(directory)
    queries = json.loads((ROOT / "benchmark/queries.json").read_text(encoding="utf-8"))
    if [query["id"] for query in queries] != [f"Q{i}" for i in range(1, 6)]:
        raise ValueError("The official benchmark must contain exactly Q1 through Q5")
    predictions = json.loads((ROOT / "benchmark/predictions.json").read_text(encoding="utf-8"))
    by_id = {doc.id: doc for doc in documents}
    # Fail fast if a gold quote is not in the frozen corpus; no fabricated answers.
    for query in queries:
        for item in query["evidence"]:
            for doc_id in [item["doc_id"], *item.get("alternative_doc_ids", [])]:
                if normalized(item["quote"]) not in normalized(by_id[doc_id].content):
                    raise ValueError(f"Invalid gold evidence for {query['id']} / {doc_id}")
    tfidf = TfidfEmbedder(doc.content for doc in documents)
    strategies: dict[str, Chunker] = {
        "fixed_size": FixedSizeChunker(500, 100),
        "by_sentences": SentenceChunker(3),
        "recursive": RecursiveChunker(chunk_size=800),
        "heading": HeadingChunker(800),
    }
    experiments: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for backend, embedder in [("tfidf", tfidf), ("mock", _mock_embed)]:
        for name, chunker in strategies.items():
            chunks = chunk_documents(documents, chunker, name)
            store = EmbeddingStore(f"{backend}-{name}", embedder)
            started = time.perf_counter()
            store.add_documents(chunks)
            ingest_ms = (time.perf_counter() - started) * 1000
            rows = [evaluate(store, query) for query in queries]
            ablation = [evaluate(store, query, filtered=False) for query in queries
                        if query["metadata_filter"]]
            experiments.append({"backend": backend, "strategy": name, "chunk_count": len(chunks),
                                "avg_length": sum(len(c.content) for c in chunks) / len(chunks),
                                "max_length": max(len(c.content) for c in chunks), "ingest_ms": ingest_ms,
                                "hit_at_3": sum(row["hit_at_3"] for row in rows) / len(rows),
                                "mrr_at_3": sum(row["reciprocal_rank"] for row in rows) / len(rows),
                                "precision_at_3": sum(row["precision_at_3"] for row in rows) / len(rows),
                                "anchor_score": sum(row["anchor_score"] for row in rows),
                                "queries": rows, "without_filter": ablation})
            if backend == "tfidf" and name == "heading":
                cross_language = {**queries[2], "id": "F1", "metadata_filter": None}
                failures.append(evaluate(store, cross_language))
                wrong_audience = {**queries[1], "id": "F2", "metadata_filter": {"audience": "faculty"}}
                failures.append(evaluate(store, wrong_audience))
    similarity = [{**pair, "tfidf": compute_similarity(tfidf(pair["a"]), tfidf(pair["b"])),
                   "mock": compute_similarity(_mock_embed(pair["a"]), _mock_embed(pair["b"]))}
                  for pair in predictions]
    result = {
        "python": platform.python_version(), "platform": platform.platform(),
        "embedding": tfidf._backend_name, "vocabulary_size": len(tfidf.vocabulary),
        "answer_backend": "extractive evidence preview; no generative LLM",
        "benchmark_version": "group-dkh-v3",
        "method": "Primary marker + accepted doc_id determines rank/Hit@3; coverage measures all markers across top-3. Literal metrics are not rubric grades.",
        "parameters": {"fixed_size": {"chunk_size": 500, "overlap": 100},
                       "by_sentences": {"max_sentences_per_chunk": 3},
                       "recursive": {"chunk_size": 800}, "heading": {"chunk_size": 800}},
        "inventory": [{"id": doc.id, "characters": len(doc.content), "metadata": doc.metadata,
                       "sha256": hashlib.sha256(Path(doc.metadata["source_file"]).read_bytes()).hexdigest()}
                      for doc in documents],
        "input_hashes": {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                         for path in [ROOT / "benchmark/queries.json", ROOT / "benchmark/predictions.json"]},
        "baseline": {doc.id: ChunkingStrategyComparator().compare(doc.content, 800)
                     for doc in documents[:3]},
        "experiments": experiments, "similarity": similarity, "failure_probes": failures,
    }
    output.mkdir(parents=True, exist_ok=True)
    (output / "benchmark_results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# Kết quả benchmark thực chạy", "", f"Python {result['python']}; {tfidf._backend_name}.",
             "", "Agent là extractive baseline, không phải LLM. Không tự quy đổi thành điểm rubric.",
             "Bộ group-dkh-v3: giữ 5 câu/filters/markers của Hiệp; Khang dùng fixed-size 500/100 theo phân công DKH.",
             "Hit@3 = tỷ lệ câu hỏi có ít nhất một chunk chứa marker đầu tiên trong tài liệu được chấp nhận;",
             "MRR@3 = trung bình nghịch đảo thứ hạng đầu tiên; Precision@3 dùng mẫu số 3 kể cả khi thiếu kết quả.",
             "Coverage đo tất cả markers trên hợp top-3; anchor_score = 2 nếu rank 1, 1 nếu rank 2/3, 0 nếu thiếu.",
             "Literal matching có thể bỏ sót bằng chứng tương đương; anchor_score không thay thế điểm rubric/đánh giá thủ công.",
             "", "| Backend | Strategy | Chunks | Avg chars | Hit@3 | MRR@3 | Precision@3 |",
             "|---|---|---:|---:|---:|---:|---:|"]
    for exp in experiments:
        lines.append(f"| {exp['backend']} | {exp['strategy']} | {exp['chunk_count']} | {exp['avg_length']:.1f} | {exp['hit_at_3']:.0%} | {exp['mrr_at_3']:.3f} | {exp['precision_at_3']:.3f} |")
    for exp in experiments:
        lines += ["", f"## {exp['backend']} / {exp['strategy']}"]
        for row in exp["queries"]:
            lines += ["", f"### {row['query_id']}: {row['question']}", "",
                      f"Filter: `{json.dumps(row['metadata_filter'], ensure_ascii=False)}`; Hit@3: {row['hit_at_3']}; coverage: {row['evidence_coverage']:.0%}.",
                      "", f"Gold: {row['gold_answer']}", ""]
            for rank, hit in enumerate(row["top3"], 1):
                lines += [f"{rank}. `{hit['metadata']['chunk_id']}` — score {hit['score']:.4f}; relevant={hit['relevant']}", "",
                          "> " + hit["content"].replace("\n", "\n> "), ""]
            lines += ["**Agent output:**", "", "> " + row["agent_answer"].replace("\n", "\n> "), ""]
    (output / "BENCHMARK_RESULTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "report/artifacts")
    args = parser.parse_args()
    result = run(args.output)
    for exp in result["experiments"]:
        print(f"{exp['backend']:5} {exp['strategy']:12} chunks={exp['chunk_count']:3} Hit@3={exp['hit_at_3']:.0%} MRR={exp['mrr_at_3']:.3f}")


if __name__ == "__main__":
    main()
