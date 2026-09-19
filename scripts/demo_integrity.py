"""Offline, cited retrieval demo over the group's actual corpus."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from src import EmbeddingStore, FixedSizeChunker, HeadingChunker, KnowledgeBaseAgent, RecursiveChunker, SentenceChunker
from src.corpus import Chunker
from src.corpus import chunk_documents, load_corpus
from src.lexical import TfidfEmbedder, extractive_answer


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question", nargs="?", default="")
    parser.add_argument("--audience", choices=["student", "faculty", "staff", "all"])
    parser.add_argument("--strategy", choices=["fixed_size", "heading", "recursive", "by_sentences"], default="fixed_size")
    parser.add_argument("--query-id", choices=[f"Q{i}" for i in range(1, 6)],
                        help="Run an official group question with its configured metadata filter")
    args = parser.parse_args()
    documents = load_corpus(Path(__file__).resolve().parents[1] / "data/ai-liem-chinh-hoc-thuat")
    embedder = TfidfEmbedder(doc.content for doc in documents)
    store = EmbeddingStore("integrity", embedder)
    chunkers: dict[str, Chunker] = {"fixed_size": FixedSizeChunker(500, 100), "heading": HeadingChunker(800),
                                   "recursive": RecursiveChunker(chunk_size=800), "by_sentences": SentenceChunker(3)}
    store.add_documents(chunk_documents(documents, chunkers[args.strategy], args.strategy))
    question = args.question
    conditions = {"audience": args.audience} if args.audience else None
    if args.query_id or not question:
        queries = json.loads((Path(__file__).resolve().parents[1] / "benchmark/queries.json").read_text(encoding="utf-8"))
        selected = next(q for q in queries if q["id"] == (args.query_id or "Q2"))
        question = selected["question"]
        if args.audience is None:
            conditions = selected["metadata_filter"]
    print(f"Backend: {embedder._backend_name}; strategy: {args.strategy}; chunks: {store.get_collection_size()}")
    for result in store.search_with_filter(question, 3, conditions):
        print(f"{result['score']:.4f} {result['metadata']['chunk_id']}")
    print(KnowledgeBaseAgent(store, extractive_answer).answer(question, metadata_filter=conditions))


if __name__ == "__main__":
    main()
