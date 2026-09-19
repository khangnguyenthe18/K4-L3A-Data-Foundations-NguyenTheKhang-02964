"""Import Dũng's supplied log with explicit provenance and query differences."""
from __future__ import annotations

import ast
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def parse_results(block: str) -> dict[str, Any]:
    filt = re.search(r"^filter=(.+)$", block, re.MULTILINE)
    score = re.search(r"^naive=(\d)/2 content\(evidence\)=(\d)/2 evidence_rank=(None|[123])$", block, re.MULTILINE)
    if filt is None or score is None:
        raise ValueError("Missing filter or evidence scores")
    hits = [{"rank": int(m[1]), "chunk_id": m[2], "score": float(m[3]),
             "audience": m[4], "content_logged": m[5].strip()}
            for m in re.finditer(r"^  ([123])\. id=(\S+) score=([\d.]+) audience=(\w+)\n     ([^\n]*)", block, re.MULTILINE)]
    if [r["rank"] for r in hits] != [1, 2, 3]:
        raise ValueError("Expected three ranked log records")
    return {"metadata_filter": ast.literal_eval(filt[1]), "top3": hits,
            "naive_score": int(score[1]), "content_score": int(score[2]),
            "evidence_rank": None if score[3] == "None" else int(score[3])}


def parse_log(text: str) -> dict[str, Any]:
    text = text.replace("\r\n", "\n")
    header = re.search(r"documents=(\d+) chunks=(\d+) avg_len=([\d.]+)", text)
    total = re.search(r"TOTAL naive=(\d+)/10 evidence=(\d+)/10; rubric=(\w+)", text)
    corpus = re.search(r"corpus_sha256=([0-9a-f]{64})", text)
    provider = re.search(r"provider=(\w+) embedding=(\S+) llm=(\S+);", text)
    if any(item is None for item in (header, total, corpus, provider)):
        raise ValueError("Incomplete member log header")
    assert header is not None and total is not None and corpus is not None and provider is not None
    rows = []
    for query in re.finditer(r"^(Q\d): ([^\n]+)\n(.*?)(?=^Q\d:|^TOTAL)", text, re.MULTILINE | re.DOTALL):
        answer = re.search(r"^agent: (.*?)\ngold: ([^\n]+)\nrubric: ([^\n]+)", query[3], re.MULTILINE | re.DOTALL)
        if answer is None:
            raise ValueError("Missing agent output or gold")
        rows.append({"id": query[1], "question": query[2], **parse_results(query[3]),
                     "agent_answer_logged": answer[1], "gold_logged": answer[2], "rubric_logged": answer[3]})
    if [r["id"] for r in rows] != [f"Q{i}" for i in range(1, 6)]:
        raise ValueError("Expected exactly Q1 through Q5")
    if sum(r["naive_score"] for r in rows) != int(total[1]) or sum(r["content_score"] for r in rows) != int(total[2]):
        raise ValueError("Member totals disagree with per-query scores")
    ab_text = text.split("A/B METADATA FILTER — Q2", 1)
    if len(ab_text) != 2:
        raise ValueError("Missing metadata ablation")
    ablation = [parse_results(m[0]) for m in re.finditer(r"^filter=.*?(?=^filter=|\Z)", ab_text[1], re.MULTILINE | re.DOTALL)]
    if len(ablation) != 2:
        raise ValueError("Expected both ablation conditions")
    return {"strategy": "recursive", "chunk_size": None,
            "chunk_size_note": "Group guide specifies 500; supplied log does not record the parameter",
            "documents": int(header[1]), "chunk_count": int(header[2]), "avg_length": float(header[3]),
            "corpus_sha256_reported": corpus[1], "corpus_hash_verified": False,
            "provider": provider[1], "embedding": provider[2], "llm": provider[3],
            "naive_score": int(total[1]), "content_score": int(total[2]), "rubric_logged": total[3],
            "scoring": "All anchors in one chunk, per supplied log; original bench.py unverified",
            "queries": rows, "ablation": ablation,
            "hit_at_3": sum(r["evidence_rank"] is not None for r in rows) / 5,
            "mrr_at_3": sum(1 / r["evidence_rank"] if r["evidence_rank"] else 0 for r in rows) / 5}


def main() -> None:
    source = ROOT / "report/ket_qua_benchmark.txt"
    result = parse_log(source.read_text(encoding="utf-8-sig"))
    official = json.loads((ROOT / "benchmark/queries.json").read_text(encoding="utf-8"))
    result.update({"member": "Nguyễn Việt Dũng", "student_id": "2A202602812",
                   "source_file": "report/ket_qua_benchmark.txt",
                   "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                   "provenance": "User supplied member log; not a reproduced OpenAI run",
                   "query_alignment": [{"id": q["id"], "exact_text_match": q["question"] == o["question"],
                                        "filter_match": q["metadata_filter"] == o["metadata_filter"],
                                        "official_question": o["question"], "logged_question": q["question"]}
                                       for q, o in zip(result["queries"], official)]})
    (ROOT / "report/artifacts/dung_results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Imported Dung: 5 queries, evidence=2/10, both ablation conditions; Q1/Q3/Q5 wording differs.")


if __name__ == "__main__":
    main()
