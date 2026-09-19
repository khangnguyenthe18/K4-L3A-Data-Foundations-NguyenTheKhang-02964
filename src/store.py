from __future__ import annotations

import heapq
import math
from copy import deepcopy
from threading import RLock
from typing import Any, Callable, TypedDict

from .chunking import _dot
from .embeddings import _mock_embed
from .models import Document


class SearchResult(TypedDict):
    id: str
    content: str
    metadata: dict[str, Any]
    score: float


class StoredRecord(TypedDict):
    id: str
    content: str
    metadata: dict[str, Any]
    embedding: list[float]


class EmbeddingStore:
    """Isolated in-memory store with atomic writes and snapshot reads.

    Embeddings execute outside the lock. No implicit network/database access.
    Ranking follows the lab contract: descending dot product.
    """

    def __init__(self, collection_name: str = "documents",
                 embedding_fn: Callable[[str], list[float]] | None = None) -> None:
        self._embedding_fn = embedding_fn or _mock_embed
        self._collection_name = collection_name
        self._store: list[StoredRecord] = []
        self._next_index = 0
        self._dimension: int | None = None
        self._lock = RLock()

    def _embed(self, text: str) -> list[float]:
        vector = [float(value) for value in self._embedding_fn(text)]
        if not vector or not all(math.isfinite(value) for value in vector):
            raise ValueError("Embedding must be nonempty and finite")
        return vector

    def _make_record(self, doc: Document) -> StoredRecord:
        if not doc.id or not doc.content.strip():
            raise ValueError("Document id and content must be nonempty")
        metadata = deepcopy(doc.metadata)
        metadata.setdefault("doc_id", doc.id)
        if not isinstance(metadata["doc_id"], str) or not metadata["doc_id"]:
            raise ValueError("metadata.doc_id must be a nonempty string")
        return {"id": doc.id, "content": doc.content, "metadata": metadata,
                "embedding": self._embed(doc.content)}

    def _search_records(self, query: str, records: list[StoredRecord],
                        top_k: int) -> list[SearchResult]:
        if top_k <= 0 or not query.strip() or not records:
            return []
        embedding = self._embed(query)
        ranked = heapq.nlargest(top_k, enumerate(records),
                              key=lambda pair: (_dot(embedding, pair[1]["embedding"]), -pair[0]))
        return [{"id": record["id"], "content": record["content"],
                 "metadata": deepcopy(record["metadata"]),
                 "score": _dot(embedding, record["embedding"])} for _, record in ranked]

    def add_documents(self, docs: list[Document]) -> None:
        records = [self._make_record(doc) for doc in docs]
        if not records:
            return
        with self._lock:
            dimension = self._dimension or len(records[0]["embedding"])
            if any(len(record["embedding"]) != dimension for record in records):
                raise ValueError("All stored embeddings must have the same dimension")
            for record in records:
                record["id"] = f"{self._collection_name}:{self._next_index}"
                self._next_index += 1
            self._store.extend(records)
            self._dimension = dimension

    def search(self, query: str, top_k: int = 5) -> list[SearchResult]:
        return self.search_with_filter(query, top_k)

    def get_collection_size(self) -> int:
        with self._lock:
            return len(self._store)

    def search_with_filter(self, query: str, top_k: int = 3,
                           metadata_filter: dict[str, Any] | None = None) -> list[SearchResult]:
        conditions = dict(metadata_filter or {})
        with self._lock:
            candidates = [record for record in self._store
                          if all(key in record["metadata"] and record["metadata"][key] == value
                                 for key, value in conditions.items())]
        return self._search_records(query, candidates, top_k)

    def delete_document(self, doc_id: str) -> bool:
        with self._lock:
            remaining = [r for r in self._store if r["metadata"]["doc_id"] != doc_id]
            removed = len(remaining) != len(self._store)
            self._store = remaining
            if not remaining:
                self._dimension = None
            return removed
