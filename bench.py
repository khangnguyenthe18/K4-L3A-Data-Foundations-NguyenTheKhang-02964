#!/usr/bin/env python3
"""bench.py - Benchmark 5 cau hoi nhom tren chien luoc ca nhan.

Chay: python bench.py
Output: ket_qua_benchmark_khang.txt (top-3 + agent answer cho 5 cau)

Chien luoc ca nhan Khang: FixedSizeChunker(500, 100) + TF-IDF extractive.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from src import EmbeddingStore, FixedSizeChunker, KnowledgeBaseAgent
from src.corpus import chunk_documents, load_corpus
from src.lexical import TfidfEmbedder, extractive_answer

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "ai-liem-chinh-hoc-thuat"
QUERIES_FILE = ROOT / "benchmark" / "queries.json"
OUTPUT_FILE = ROOT / "ket_qua_benchmark_khang.txt"

STRATEGY_NAME = "fixed_size"
CHUNKER = FixedSizeChunker(chunk_size=500, overlap=100)


def main() -> None:
    documents = load_corpus(DATA_DIR)
    print(f"Corpus: {len(documents)} tai lieu tu {DATA_DIR.name}/")

    chunks = chunk_documents(documents, CHUNKER, STRATEGY_NAME)
    print(f"Chunker: {STRATEGY_NAME} (size=500, overlap=100) -> {len(chunks)} chunks")

    embedder = TfidfEmbedder(doc.content for doc in documents)
    store = EmbeddingStore("bench", embedder)
    store.add_documents(chunks)
    print(f"Store: {store.get_collection_size()} records; backend={embedder._backend_name}")

    queries = json.loads(QUERIES_FILE.read_text(encoding="utf-8"))
    assert len(queries) == 5, f"Can dung 5 cau, co {len(queries)}"

    agent = KnowledgeBaseAgent(store, extractive_answer)

    lines: list[str] = []
    lines.append("=" * 72)
    lines.append("KET QUA BENCHMARK - Nguyen The Khang (2A202602964)")
    lines.append(f"Thoi gian: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"Python: {sys.version.split()[0]}")
    lines.append(f"Strategy: {STRATEGY_NAME} (chunk_size=500, overlap=100)")
    lines.append(f"Backend: {embedder._backend_name} + extractive (khong LLM)")
    lines.append(f"Chunks nap: {store.get_collection_size()}")
    lines.append("=" * 72)

    for query in queries:
        qid = query["id"]
        question = query["question"]
        gold = query["gold_answer"]
        mfilter = query["metadata_filter"]

        lines.append("")
        lines.append("-" * 72)
        lines.append(f"## {qid}: {question}")
        lines.append(f"Filter: {json.dumps(mfilter, ensure_ascii=False)}")
        lines.append(f"Gold:   {gold}")
        lines.append("")

        results = store.search_with_filter(question, 3, mfilter)
        lines.append(f"{'Rank':<5} {'Score':>7}  Chunk ID")
        lines.append(f"{'---':<5} {'---':>7}  {'---'}")
        for rank, r in enumerate(results, 1):
            chunk_id = r["metadata"].get("chunk_id", r["metadata"].get("doc_id", "?"))
            lines.append(f"{rank:<5} {r['score']:>7.4f}  {chunk_id}")
            preview = r["content"][:200].replace("\n", " ")
            lines.append(f"       > {preview}...")
        lines.append("")

        answer = agent.answer(question, top_k=3, metadata_filter=mfilter)
        lines.append("Agent output:")
        for al in answer.split("\n"):
            lines.append(f"  {al}")

    # A/B: Q2 co/khong metadata filter
    q2 = next(q for q in queries if q["id"] == "Q2")
    lines.append("")
    lines.append("=" * 72)
    lines.append("## A/B - Q2 co/khong metadata filter")
    lines.append("=" * 72)

    for label, flt in [("CO filter (audience=student)", q2["metadata_filter"]),
                       ("KHONG filter", None)]:
        results = store.search_with_filter(q2["question"], 3, flt)
        lines.append(f"\n### {label}")
        lines.append(f"{'Rank':<5} {'Score':>7}  {'Audience':<10} Chunk ID")
        for rank, r in enumerate(results, 1):
            aud = r["metadata"].get("audience", "?")
            cid = r["metadata"].get("chunk_id", "?")
            lines.append(f"{rank:<5} {r['score']:>7.4f}  {aud:<10} {cid}")

    lines.append("")
    lines.append("=" * 72)
    lines.append("Ket thuc benchmark.")

    output_text = "\n".join(lines) + "\n"
    print()
    print(output_text)
    OUTPUT_FILE.write_text(output_text, encoding="utf-8")
    print(f"\n-> Da ghi ket qua vao: {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()