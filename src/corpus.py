"""Validated ingestion of the lab's flat, quoted Markdown front matter."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Protocol
from urllib.parse import urlparse
from datetime import date

from .models import Document


class Chunker(Protocol):
    def chunk(self, text: str) -> list[str]: ...


def load_corpus(directory: Path) -> list[Document]:
    documents: list[Document] = []
    seen: set[str] = set()
    for path in sorted(directory.glob("*.md")):
        text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
        parts = text.split("---\n", 2)
        if len(parts) != 3 or parts[0]:
            raise ValueError(f"{path.name}: expected Markdown front matter")
        metadata: dict[str, str] = {}
        for line in parts[1].splitlines():
            if not line.strip():
                continue
            key, separator, raw = line.partition(":")
            key = key.strip()
            if not separator or key in metadata:
                raise ValueError(f"{path.name}: invalid or duplicate metadata key")
            value = json.loads(raw.strip())
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{path.name}: metadata values must be nonempty quoted strings")
            metadata[key] = value
        required = {"doc_id", "title", "source_url", "retrieved_at", "document_version",
                    "audience", "category", "language"}
        if missing := required - metadata.keys():
            raise ValueError(f"{path.name}: missing {sorted(missing)}")
        url = urlparse(metadata["source_url"])
        if url.scheme not in {"http", "https"} or not url.netloc:
            raise ValueError(f"{path.name}: invalid source URL")
        date.fromisoformat(metadata["retrieved_at"])
        if metadata["audience"] not in {"student", "faculty", "staff", "all"}:
            raise ValueError(f"{path.name}: invalid audience")
        doc_id = metadata["doc_id"]
        if doc_id in seen:
            raise ValueError(f"Duplicate document id: {doc_id}")
        seen.add(doc_id)
        content = parts[2].strip()
        if not content:
            raise ValueError(f"{path.name}: empty content")
        metadata["source_file"] = path.as_posix()
        documents.append(Document(doc_id, content, metadata))
    if not documents:
        raise ValueError(f"No Markdown documents found in {directory}")
    return documents


def chunk_documents(documents: list[Document], chunker: Chunker, strategy: str) -> list[Document]:
    chunks: list[Document] = []
    for doc in documents:
        for index, content in enumerate(chunker.chunk(doc.content)):
            if not content.strip():
                continue
            chunk_id = f"{doc.id}:{strategy}:{index:03d}"
            metadata = {**doc.metadata, "doc_id": doc.id, "chunk_index": index,
                        "chunk_id": chunk_id, "strategy": strategy}
            chunks.append(Document(chunk_id, content, metadata))
    return chunks
