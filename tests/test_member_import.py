from pathlib import Path
import pytest
from scripts.import_dung import parse_log

ROOT = Path(__file__).resolve().parents[1]

def test_dung_log_totals_and_multiline_answer() -> None:
    result = parse_log((ROOT / "report/ket_qua_benchmark.txt").read_text(encoding="utf-8"))
    assert result["chunk_count"] == 177
    assert result["content_score"] == 2 and result["naive_score"] == 6
    assert result["hit_at_3"] == 0.2 and result["mrr_at_3"] == 0.2
    assert "Vậy, theo quy định" in result["queries"][0]["agent_answer_logged"]
    assert [r["evidence_rank"] for r in result["ablation"]] == [2, 1]
    assert result["corpus_hash_verified"] is False

def test_dung_import_rejects_incorrect_totals() -> None:
    text = (ROOT / "report/ket_qua_benchmark.txt").read_text(encoding="utf-8")
    with pytest.raises(ValueError, match="totals"):
        parse_log(text.replace("TOTAL naive=6/10 evidence=2/10", "TOTAL naive=6/10 evidence=8/10"))

def test_dung_import_requires_ablation() -> None:
    text = (ROOT / "report/ket_qua_benchmark.txt").read_text(encoding="utf-8")
    with pytest.raises(ValueError, match="ablation"):
        parse_log(text.split("A/B METADATA FILTER", 1)[0])
