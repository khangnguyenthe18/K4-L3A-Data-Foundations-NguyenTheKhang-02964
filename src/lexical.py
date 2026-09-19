"""Dependency-free lexical baselines; not neural/semantic embeddings or an LLM."""
from __future__ import annotations

import json
import math
import re
import unicodedata
from collections import Counter
from typing import Iterable


def tokenize(text: str) -> list[str]:
    return re.findall(r"[^\W_]+", unicodedata.normalize("NFC", text).casefold())


class TfidfEmbedder:
    """Fit only on source documents, then freeze vocabulary/IDF for every strategy."""

    _backend_name = "tfidf-word-unigram-l2 (lexical, offline)"

    def __init__(self, texts: Iterable[str]) -> None:
        frequency: Counter[str] = Counter()
        count = 0
        for text in texts:
            frequency.update(set(tokenize(text)))
            count += 1
        if not frequency:
            raise ValueError("Cannot fit TF-IDF on an empty vocabulary")
        self.vocabulary = {word: index for index, word in enumerate(sorted(frequency))}
        self.idf = [math.log((1 + count) / (1 + frequency[word])) + 1
                    for word in self.vocabulary]

    def __call__(self, text: str) -> list[float]:
        vector = [0.0] * len(self.vocabulary)
        for word, count in Counter(tokenize(text)).items():
            if word in self.vocabulary:
                index = self.vocabulary[word]
                vector[index] = (1 + math.log(count)) * self.idf[index]
        norm = math.hypot(*vector)
        return [value / norm for value in vector] if norm else vector


def extractive_answer(prompt: str) -> str:
    """An explicitly labelled evidence preview implementing the llm_fn interface.

    No gold answers or benchmark identifiers are accessible to this function.
    Returns complete retrieved chunks with citations. Keeping whole chunks
    preserves list items, exceptions and negations that paragraph selection
    can drop even when retrieval found the correct evidence.
    """
    payload = json.loads(prompt.split("\n", 1)[1])
    outputs: list[str] = []
    seen: set[str] = set()
    for item in payload["evidence"]:
        content = item["content"].strip()
        if not content:
            continue
        if content not in seen:
            seen.add(content)
            outputs.append(f"{content}\n[{item['chunk_id']}]({item['source_url']})")
    return "[EXTRACTIVE BASELINE — không phải LLM]\n\n" + "\n\n".join(outputs) if outputs else (
        "Không tìm thấy bằng chứng phù hợp trong cơ sở tri thức.")
