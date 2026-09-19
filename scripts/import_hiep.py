"""Parse a member-supplied log without claiming to reproduce its remote run."""
from __future__ import annotations

import ast
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def parse_log(text: str) -> list[dict[str, Any]]:
    experiments: list[dict[str, Any]] = []
    pattern = r"STRATEGY: (?P<label>[^\n]+)\nchunks=(?P<count>\d+)  avg_len=(?P<avg>\d+)  min=(?P<min>\d+)  max=(?P<max>\d+)(?P<body>.*?)TOTAL (?P<name>\w+): naive\(doc_id\)=(?P<naive>\d+)/10   content\(evidence\)=(?P<score>\d+)/10"
    for match in re.finditer(pattern, text, re.DOTALL):
        rows: list[dict[str, Any]] = []
        for query in re.finditer(r"\[(Q\d+)\] ([^\n]+)\n(.*?)(?=\n\[Q\d+\]|\Z)", match["body"], re.DOTALL):
            body = query[3]
            config = re.search(r"filter=(.*?)  gold=(.*?)  evidence=([^\n]+)", body)
            scores = re.search(r"naive\(doc_id\)=(\d)/2\s+content\(evidence\)=(\d)/2\s+evidence_rank=(None|[123])", body)
            agent = re.search(r"  agent: (.*)", body, re.DOTALL)
            if config is None or scores is None or agent is None:
                raise ValueError(f"Incomplete log for {query[1]}")
            hits = [{"rank": int(m[1]), "score": float(m[2]), "chunk_id": m[3], "preview": m[4]}
                    for m in re.finditer(r"^  ([123])\. score=([\d.]+)\s+(\S+)\s+(.*)$", body, re.MULTILINE)]
            if len(hits) != 3:
                raise ValueError("Expected exactly three logged previews")
            rows.append({"id": query[1], "question": query[2],
                         "metadata_filter": ast.literal_eval(config[1]),
                         "gold_doc_ids": ast.literal_eval(config[2]),
                         "evidence_markers": ast.literal_eval(config[3]),
                         "naive_score": int(scores[1]), "content_score": int(scores[2]),
                         "evidence_rank": None if scores[3] == "None" else int(scores[3]),
                         "top3_previews": hits, "agent_answer_logged": agent[1].strip()})
        if [row["id"] for row in rows] != [f"Q{i}" for i in range(1, 6)]:
            raise ValueError("Expected Q1 through Q5 exactly once")
        total = int(match["score"])
        if total != sum(row["content_score"] for row in rows):
            raise ValueError("Logged content total does not match per-query scores")
        if int(match["naive"]) != sum(row["naive_score"] for row in rows):
            raise ValueError("Logged doc-id total does not match per-query scores")
        experiments.append({"strategy": match["name"], "label": match["label"],
                            "chunk_count": int(match["count"]), "avg_length": int(match["avg"]),
                            "min_length": int(match["min"]), "max_length": int(match["max"]),
                            "content_score": total, "naive_score": int(match["naive"]),
                            "hit_at_3": sum(r["evidence_rank"] is not None for r in rows) / 5,
                            "mrr_at_3": sum(1 / r["evidence_rank"] if r["evidence_rank"] else 0 for r in rows) / 5,
                            "queries": rows})
    if {e["strategy"] for e in experiments} != {"fixed", "recursive", "heading"} or len(experiments) != 3:
        raise ValueError("Expected three strategies in the supplied log")
    for experiment in experiments[1:]:
        for expected, actual in zip(experiments[0]["queries"], experiment["queries"]):
            for key in ("id", "question", "metadata_filter", "gold_doc_ids", "evidence_markers"):
                if expected[key] != actual[key]:
                    raise ValueError(f"Inconsistent {key} between logged strategies")
    return experiments


def main() -> None:
    source = ROOT / "ket_qua_benchmark.txt"
    experiments = parse_log(source.read_text(encoding="utf-8-sig").replace("\r\n", "\n"))
    result = {"member": "Đặng Quốc Hiệp", "source_file": source.name,
              "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
              "provenance": "User-supplied member log; imported, not reproduced locally",
              "embedding": "gemini-embedding-001 (cached)", "llm": "gemini-2.5-flash",
              "experiments": experiments}
    destination = ROOT / "report/artifacts/hiep_results.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Imported 3 strategies / 15 results; verified logged totals and query consistency.")


if __name__ == "__main__":
    main()
