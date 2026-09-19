from __future__ import annotations

import math
import re
from typing import TypedDict


class ChunkStats(TypedDict):
    count: int
    avg_length: float
    chunks: list[str]


class FixedSizeChunker:
    """
    Split text into fixed-size chunks with optional overlap.

    Rules:
        - Each chunk is at most chunk_size characters long.
        - Consecutive chunks share overlap characters.
        - The last chunk contains whatever remains.
        - If text is shorter than chunk_size, return [text].
    """

    def __init__(self, chunk_size: int = 500, overlap: int = 50) -> None:
        if chunk_size <= 0 or not 0 <= overlap < chunk_size:
            raise ValueError("Require chunk_size > 0 and 0 <= overlap < chunk_size")
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> list[str]:
        if not text:
            return []
        if len(text) <= self.chunk_size:
            return [text]

        step = self.chunk_size - self.overlap
        chunks: list[str] = []
        for start in range(0, len(text), step):
            chunk = text[start : start + self.chunk_size]
            chunks.append(chunk)
            if start + self.chunk_size >= len(text):
                break
        return chunks


class SentenceChunker:
    """
    Split text into chunks of at most max_sentences_per_chunk sentences.

    Sentence detection: split on ". ", "! ", "? " or ".\n".
    Strip extra whitespace from each chunk.
    """

    def __init__(self, max_sentences_per_chunk: int = 3) -> None:
        self.max_sentences_per_chunk = max(1, max_sentences_per_chunk)

    def chunk(self, text: str) -> list[str]:
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
        size = self.max_sentences_per_chunk
        return [" ".join(sentences[i:i + size]) for i in range(0, len(sentences), size)]


class RecursiveChunker:
    """
    Recursively split text using separators in priority order.

    Default separator priority:
        ["\n\n", "\n", ". ", " ", ""]
    """

    DEFAULT_SEPARATORS = ["\n\n", "\n", ". ", " ", ""]

    def __init__(self, separators: list[str] | None = None, chunk_size: int = 500) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        self.separators = list(self.DEFAULT_SEPARATORS if separators is None else separators)
        self.chunk_size = chunk_size

    def chunk(self, text: str) -> list[str]:
        return self._split(text, self.separators) if text.strip() else []

    def _split(self, current_text: str, remaining_separators: list[str]) -> list[str]:
        if len(current_text) <= self.chunk_size:
            return [current_text] if current_text else []
        if not remaining_separators or remaining_separators[0] == "":
            return FixedSizeChunker(self.chunk_size, 0).chunk(current_text)
        separator, *remaining = remaining_separators
        # Keep separators so splitting never silently discards source content.
        pieces = re.split(f"({re.escape(separator)})", current_text)
        units = ["".join(pieces[i:i + 2]) for i in range(0, len(pieces), 2)]
        chunks: list[str] = []
        buffer = ""
        for unit in units:
            if len(buffer) + len(unit) <= self.chunk_size:
                buffer += unit
                continue
            if buffer:
                chunks.append(buffer)
                buffer = ""
            if len(unit) > self.chunk_size:
                chunks.extend(self._split(unit, remaining))
            else:
                buffer = unit
        if buffer:
            chunks.append(buffer)
        return chunks


def _dot(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError("Vector dimensions must match")
    return math.fsum(x * y for x, y in zip(a, b))


def compute_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """
    Compute cosine similarity between two vectors.

    cosine_similarity = dot(a, b) / (||a|| * ||b||)

    Returns 0.0 if either vector has zero magnitude.
    """
    if len(vec_a) != len(vec_b):
        raise ValueError("Vector dimensions must match")
    if any(not math.isfinite(v) for v in [*vec_a, *vec_b]):
        raise ValueError("Vectors must contain finite values")
    norm_a, norm_b = math.hypot(*vec_a), math.hypot(*vec_b)
    if not norm_a or not norm_b:
        return 0.0
    score = math.fsum((a / norm_a) * (b / norm_b) for a, b in zip(vec_a, vec_b))
    return max(-1.0, min(1.0, score))


class ChunkingStrategyComparator:
    """Run all built-in chunking strategies and compare their results."""

    def compare(self, text: str, chunk_size: int = 200) -> dict[str, ChunkStats]:
        strategies = {
            "fixed_size": FixedSizeChunker(chunk_size, min(50, chunk_size // 5)).chunk(text),
            "by_sentences": SentenceChunker().chunk(text),
            "recursive": RecursiveChunker(chunk_size=chunk_size).chunk(text),
        }
        return {name: {"count": len(chunks), "avg_length": sum(map(len, chunks)) / len(chunks)
                       if chunks else 0.0, "chunks": chunks}
                for name, chunks in strategies.items()}


class HeadingChunker:
    """Keep Markdown heading ancestry in every bounded section chunk."""

    def __init__(self, chunk_size: int = 1000) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        self.chunk_size = chunk_size

    def chunk(self, text: str) -> list[str]:
        chunks: list[str] = []
        headings: list[tuple[int, str]] = []
        body: list[str] = []

        def flush() -> None:
            content = "".join(body).strip()
            if not content:
                return
            prefix = "\n".join(h for _, h in headings)
            # Reserve room for content even for unusually long heading chains.
            prefix = prefix[:max(0, self.chunk_size // 3)]
            prefix = prefix + "\n\n" if prefix and self.chunk_size > 3 else ""
            budget = self.chunk_size - len(prefix)
            chunks.extend(prefix + part for part in RecursiveChunker(chunk_size=budget).chunk(content))

        for line in text.splitlines(keepends=True):
            match = re.match(r"^(#{1,6})\s+(.+)", line)
            if match:
                flush()
                body.clear()
                level = len(match[1])
                while headings and headings[-1][0] >= level:
                    headings.pop()
                headings.append((level, line.strip()))
            else:
                body.append(line)
        flush()
        if not chunks and text.strip():
            return RecursiveChunker(chunk_size=self.chunk_size).chunk(text)
        return chunks
