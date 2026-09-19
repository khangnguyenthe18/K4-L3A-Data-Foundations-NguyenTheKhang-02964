"""Render submission reports from actual v2 artifacts and member provenance."""
from __future__ import annotations

import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def table(headers: list[str], rows: list[list[Any]]) -> str:
    return "\n".join(["| " + " | ".join(headers) + " |",
                      "| " + " | ".join("---" for _ in headers) + " |",
                      *["| " + " | ".join(cell(v) for v in row) + " |" for row in rows]])


def read_json(path: str) -> Any:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def write_report(name: str, content: str) -> None:
    clean = "\n".join(line.rstrip() for line in content.splitlines()).strip() + "\n"
    (ROOT / "report" / name).write_text(clean, encoding="utf-8")


def main() -> None:
    data = read_json("report/artifacts/benchmark_results.json")
    queries = read_json("benchmark/queries.json")
    hiep = read_json("report/artifacts/hiep_results.json")
    dung = read_json("report/artifacts/dung_results.json")
    review = read_json("benchmark/answer_review.json")
    if data.get("benchmark_version") != "group-dkh-v3":
        raise ValueError("Refuse to publish reports from obsolete benchmark results")
    for name, expected in data["input_hashes"].items():
        if hashlib.sha256((ROOT / "benchmark" / name).read_bytes()).hexdigest() != expected:
            raise ValueError(f"Stale benchmark artifact for {name}")
    for local, supplied in zip(queries, hiep["experiments"][0]["queries"]):
        if (local["question"], local["metadata_filter"]) != (supplied["question"], supplied["metadata_filter"]):
            raise ValueError("Group query mismatch")
    selected = next(e for e in data["experiments"] if e["backend"] == "tfidf" and e["strategy"] == "fixed_size")
    suite = ET.parse(ROOT / "report/artifacts/test_results.xml").getroot()
    cases = list(suite.iter("testcase"))
    passed = sum(not any(child.tag in {"failure", "error", "skipped"} for child in case) for case in cases)
    core = sum("test_solution" in case.attrib.get("classname", "") for case in cases)
    metrics = table(["Backend", "Strategy", "Chunks", "Avg chars", "Hit@3", "MRR@3", "Anchor /10"],
                    [[e["backend"], e["strategy"], e["chunk_count"], f"{e['avg_length']:.1f}",
                      f"{e['hit_at_3']:.0%}", f"{e['mrr_at_3']:.3f}", e["anchor_score"]] for e in data["experiments"]])
    results = table(["Query", "Top-1 chunk", "Score", "Evidence rank", "Coverage", "Answer chứa markers?"],
                    [[r["query_id"], r["top3"][0]["metadata"]["chunk_id"], f"{r['top3'][0]['score']:.4f}",
                      r["evidence_rank"], f"{r['evidence_coverage']:.0%}", r["answer_contains_all_gold_spans"]]
                     for r in selected["queries"]])
    detail = []
    for row in selected["queries"]:
        detail += [f"### {row['query_id']}: {row['question']}", f"**Gold:** {row['gold_answer']}",
                   table(["Rank", "Chunk ID", "Score", "Chứa primary marker?"],
                         [[i, hit["metadata"]["chunk_id"], f"{hit['score']:.4f}", hit["relevant"]]
                          for i, hit in enumerate(row["top3"], 1)]),
                   "**Agent output thực tế (trích nguyên chunks, không phải LLM):**",
                   # Quote Markdown source headings so they do not break report structure.
                   "> " + row["agent_answer"].replace("\n", "\n> ")]
    answer_details = "\n\n".join(detail)
    similarity = table(["#", "Câu A", "Câu B", "Dự đoán trước chạy", "TF-IDF", "Mock"],
                       [[i, p["a"], p["b"], p["prediction"], f"{p['tfidf']:.4f}", f"{p['mock']:.4f}"]
                        for i, p in enumerate(data["similarity"], 1)])
    manual = table(["Query", "Điểm tham khảo /2", "Căn cứ"],
                   [[r["query_id"], r["provisional_score"], r["reason"]] for r in review["rows"]])
    shared = """## Giới hạn và khai báo hỗ trợ

Codex (OpenAI, 2026) hỗ trợ triển khai, chạy tests/benchmark và soạn báo cáo. Corpus và log Hiệp do người dùng cung cấp. Dự đoán similarity là giả thuyết thiết kế có hỗ trợ AI, đã lưu trước lượt tính; không mô tả như dự đoán tự làm của sinh viên. Người nộp cần hiểu, kiểm tra và khai báo hỗ trợ theo yêu cầu môn học.

Local dùng TF-IDF lexical + extractive evidence output, không dùng LLM hay API key. Log Hiệp khai báo Gemini embedding cached + Gemini Flash; được import, chưa chạy tái lập. Đã nhận log Dũng: OpenAI embeddings + GPT-4.1-mini, recursive; Q1/Q3/Q5 khác cách diễn đạt so với Hiệp. Xem [KET_QUA_DUNG.md](KET_QUA_DUNG.md). Buổi demo/thuyết trình chưa diễn ra trong phiên này.

Các gold answers là kiểm thử snapshot tài liệu đã có, không xác nhận chính sách/hiệu lực pháp lý hiện hành. Có 10 file nhưng chỉ 5 URL; một số đoạn UNA lặp giữa general/faculty. Khi chia train/test cần group theo nguồn. Năm queries là bộ đánh giá nội bộ, không phải held-out test; Q3/Q4 thiếu issuer trong câu hỏi nguyên văn nên có độ mơ hồ ngoài ngữ cảnh gold.

Không suy ra chất lượng câu trả lời chỉ từ marker hay doc_id. Các số liệu local-v1 (bộ cũ đạt 5/5) chỉ còn trong archive; bài nộp dùng group-dkh-v3.
"""
    failure = """## Phân tích lỗi và bài học

**Q3/Q4 — khác ngôn ngữ và nguồn:** query tiếng Việt, evidence đích tiếng Anh tại RMIT/UNA; lexical retrieval ưu tiên UEH và thiếu gold markers trong top-3. Root cause: TF-IDF không ánh xạ ngữ nghĩa Việt–Anh, còn query gốc không nêu issuer. Hướng cải thiện là multilingual embedding + làm rõ trường/nguồn; chưa đo mức cải thiện bằng cách đổi backend local.

**F2 — filter sai:** ép audience=faculty cho Q2 loại mọi tài liệu đích student, Hit@3=0. Filter phải lấy từ ngữ cảnh người hỏi. Exact student filter cũng loại audience=all; production phải xác định rõ có cho phép all hay không.

**Trích xuất mất ý:** phiên bản trước chỉ chọn một paragraph, có thể bỏ mất mục danh sách chứa con số dù retrieval có bằng chứng. Đã sửa extractive backend trả nguyên chunk trong context có giới hạn; test kiểm tra giữ cả con số lẫn phủ định. Vẫn có context thừa và không phải câu trả lời tổng hợp của LLM.

**Đúng tài liệu chưa đủ:** log Hiệp có doc_id score 10/10 cho mọi strategy nhưng evidence chỉ 5/10, 2/10, 6/10. Ví dụ Q1 fixed/recursive không có đoạn ngưỡng dù đúng file. Literal matcher cũng có thể chấm thiếu mẫu tương đương ở Q3 hoặc câu trả lời theo nhóm dữ liệu ở Q4; cần đọc đầy đủ output.

**Trade-off:** heading giữ Điều/Mục và ancestry để dễ kiểm tra phạm vi; số record tăng do prefix lặp. In-memory dense search O(N×D), heap top-k O(N log k), phù hợp lab nhỏ; corpus lớn cần sparse/ANN, batching và persistence. Các cải tiến đó chưa được đo ở đây.
"""
    personal = f"""# Báo cáo cá nhân — Lab 7

**Họ tên:** Nguyễn Thế Khang

**MSSV:** 2A202602964 — **Nhóm:** DKH — **Vai trò:** R1 · Data

**Chủ đề:** Quy định sử dụng AI và liêm chính học thuật trong giáo dục đại học

**Thành viên:** Nguyễn Thế Khang, Đặng Quốc Hiệp, Nguyễn Việt Dũng

**Phiên bản bài nộp:** group-dkh-v3; ngày 19/09/2026

## 1. Khởi động

Cosine similarity: đo độ tương đồng về hướng của hai vector. Với embeddings có chất lượng, hai câu gần nghĩa thường có cosine cao. Cặp gần nghĩa: “Sinh viên phải ghi nguồn khi sử dụng AI trong học thuật” / “Người học cần trích dẫn công cụ trí tuệ nhân tạo đã dùng”. Cặp khác nghĩa: “Academic integrity requires honest citation” / “The recipe uses rice and boiling water”.

Cosine bỏ qua độ lớn vector. Với vector chuẩn hóa L2, cosine và Euclidean distance cho cùng thứ tự xếp hạng; score cao không xác nhận hai câu có cùng tính đúng/sai.

10.000 ký tự, size=500, overlap=50: `ceil((10000-50)/(500-50)) = 23 chunks`. Khi overlap=100: `ceil(9900/400) = 25 chunks`. Overlap giữ ngữ cảnh qua ranh giới nhưng tăng dữ liệu trùng và chi phí embedding.

## 2. Hướng tiếp cận

- `SentenceChunker`: regex `(?<=[.!?])\\s+`, giữ dấu câu, strip và nhóm tối đa 3 câu; viết tắt/số thứ tự có thể gây tách sai.
- `RecursiveChunker`: thử đoạn, dòng, câu, từ, ký tự; giữ separators; đệ quy chỉ với phần quá dài; khi hết separators thì cắt theo size. Tests kiểm tra không mất văn bản và không vượt giới hạn.
- `compute_similarity`: kiểm tra chiều và số hữu hạn, xử lý zero vector, chia từng phần tử theo norm trước dot để tránh overflow thông thường. Comparator trả count/avg_length/chunks cho cả text rỗng.
- `HeadingChunker(800)`: giữ ancestry của tiêu đề trong từng đoạn con, dành tối đa khoảng 1/3 ngân sách cho heading và recursive split phần thân. Đây là đối chứng; strategy cá nhân theo phân công DKH là FixedSizeChunker(500, 100).
- `EmbeddingStore`: in-memory theo lựa chọn của đề, ID record riêng để cho phép thêm trùng doc_id; metadata copy sâu. Embed một lần mỗi document lúc add và một lần mỗi query lúc search; dot product trên L2 vectors bằng cosine. Filter AND trước top-k; delete mọi chunk theo doc_id.
- Error handling/concurrency: vector cùng chiều và hữu hạn, k không dương/query rỗng trả []; batch embed xong mới commit dưới RLock, search snapshot; lỗi backend không âm thầm fallback.
- `KnowledgeBaseAgent`: dependency injection store/llm_fn, pre-filter, giới hạn context, JSON evidence có citation. Không có kết quả thì thông báo thiếu evidence. Backend thực chạy là extractive, trả đủ chunk để không rơi mất ngoại lệ/định lượng.
- Ingestion: tách metadata khỏi text embedding, kiểm tra URL/ngày/audience/ID, giữ nguồn/phiên bản và thêm chunk_index/chunk_id/strategy. Front matter parser hỗ trợ schema phẳng với chuỗi quoted của dataset, không phải toàn bộ YAML.

## 3. Kiểm thử

Python **{data['python']}**. **{passed}/{len(cases)} tests pass**, trong đó có **{core} tests gốc**; còn lại là edge cases, concurrency, ingestion, benchmark alignment, import log và evidence coverage. [JUnit](artifacts/test_results.xml) và [console log](artifacts/test_results.txt).

`.venv` cũ trỏ interpreter đã mất; máy hiện tại dùng Python 3.11.9 portable trong `.runtime/python311`. Chạy `powershell -File scripts/run_lab.ps1 test`. Không sửa interpreter của hệ thống.

## 4. Dự đoán similarity

Giả thuyết lưu trước lượt tính trong [predictions.json](../benchmark/predictions.json). Cao/thấp là dự đoán theo nghĩa, không phải ngưỡng chấm số học.

{similarity}

Cặp 1 cao nhất (1.0), cặp 5 thấp nhất (0.0) theo TF-IDF, phù hợp dự đoán; cặp 3 nhiều từ chung có điểm tương đối cao. Cặp 2 paraphrase và cặp 4 khác ngôn ngữ gần nghĩa nhưng điểm thấp, thể hiện giới hạn lexical representation. Mock không dùng để suy luận ý nghĩa.

## 5. Kết quả cùng bộ câu hỏi nhóm

Đã chạy đúng nguyên văn **5 câu Hiệp gửi**, cùng filters và markers: [queries.json](../benchmark/queries.json). Chọn TF-IDF + fixed-size 500/overlap100, top_k=3. **{sum(r['hit_at_3'] for r in selected['queries'])}/5 Hit@3**, MRR@3 **{selected['mrr_at_3']:.3f}**. Đây là kết quả group-dkh-v3; không dùng kết quả 5/5 của bộ câu hỏi local-v1.

{results}

### Đánh giá câu trả lời theo rubric (tham khảo)

{manual}

Tổng tham khảo **{sum(r['provisional_score'] for r in review['rows'])}/10** cho cấu hình cá nhân, do AI hỗ trợ đối chiếu output với gold/rubric; không phải điểm giảng viên. Q3/Q4 cần cải thiện retrieval. Extractive output dài hơn câu trả lời tự nhiên nhưng cho phép kiểm tra nguồn.

{answer_details}

{failure}

## 6. Học từ kết quả thành viên và tự đánh giá

Từ log Hiệp: evidence scoring phân biệt đúng file với đúng nội dung; Gemini có thể truy xuất RMIT tiếng Anh từ query tiếng Việt nhưng vẫn thiếu chi tiết ở một số chunks. So sánh này gợi ý cần cải thiện cả embedding lẫn cấu trúc đoạn, không chỉ thay size. Đây là nhận xét từ artifact Hiệp gửi, không ghi là trải nghiệm thuyết trình đã diễn ra.

Đã có đủ code/tests, warm-up, giải thích triển khai, 5 similarity pairs, 5 kết quả theo bộ câu hỏi chung và failure analysis cho hồ sơ cá nhân. Đánh giá retrieval còn lỗi đã công khai; hoàn thành bài không đồng nghĩa đạt điểm tối đa.

{shared}
"""
    inventory = table(["Tài liệu", "Nguồn", "Ngày lấy / phiên bản", "Ký tự", "Audience"],
                      [[d["metadata"]["title"], f"[Nguồn]({d['metadata']['source_url']})",
                        d["metadata"]["retrieved_at"] + " / " + d["metadata"]["document_version"],
                        d["characters"], d["metadata"]["audience"]] for d in data["inventory"]])
    baseline = table(["Document", "Strategy", "Chunks", "Avg chars"],
                     [[doc_id, name, stats["count"], f"{stats['avg_length']:.1f}"]
                      for doc_id, values in data["baseline"].items() for name, stats in values.items()])
    member_rows = [["Khang — local", e["strategy"], "TF-IDF / extractive", e["chunk_count"],
                    f"{e['hit_at_3']:.0%}", f"{e['mrr_at_3']:.3f}", e["anchor_score"]]
                   for e in data["experiments"] if e["backend"] == "tfidf"]
    member_rows += [["Hiệp — log cung cấp", e["strategy"], "Gemini embedding / Flash", e["chunk_count"],
                     f"{e['hit_at_3']:.0%}", f"{e['mrr_at_3']:.3f}", e["content_score"]]
                    for e in hiep["experiments"]]
    member_rows.append(["Dũng — log cung cấp", "recursive", "OpenAI embedding / GPT-4.1-mini", dung["chunk_count"],
                        f"{dung['hit_at_3']:.0%}", f"{dung['mrr_at_3']:.3f}", dung["content_score"]])
    member_table = table(["Thành viên/nguồn", "Strategy", "Backend", "Chunks", "Hit@3", "MRR@3", "Anchor/log content /10"], member_rows)
    gold = table(["ID", "Query", "Ngữ cảnh/filter", "Gold answer", "Vị trí bằng chứng"],
                 [[q["id"], q["question"], q["user_context"] + " / " + json.dumps(q["metadata_filter"], ensure_ascii=False),
                   q["gold_answer"], q["source_section"]] for q in queries])
    ablation = table(["Strategy local", "Q2 RR có filter", "RR không filter", "Top-3 audiences không filter"],
                     [[e["strategy"], f"{e['queries'][1]['reciprocal_rank']:.3f}",
                       f"{e['without_filter'][0]['reciprocal_rank']:.3f}",
                       ", ".join(r["metadata"]["audience"] for r in e["without_filter"][0]["top3"])]
                      for e in data["experiments"] if e["backend"] == "tfidf"])
    rank_comparison = table(["Query", "Khang fixed rank", "Hiệp fixed rank", "Hiệp recursive rank", "Hiệp heading rank", "Dũng recursive rank"],
                           [[r["query_id"], r["evidence_rank"], *[e["queries"][i]["evidence_rank"] for e in hiep["experiments"]], dung["queries"][i]["evidence_rank"]]
                            for i, r in enumerate(selected["queries"])])
    group = f"""# Báo cáo nhóm DKH — Quy định sử dụng AI và liêm chính học thuật

**Thành viên:** Nguyễn Thế Khang, Đặng Quốc Hiệp, Nguyễn Việt Dũng

**Lớp:** K4-L3A — **Phiên bản:** group-dkh-v3 — **Ngày:** 19/09/2026

## 1. Bộ tài liệu và metadata

Chủ đề được nhóm chọn là liêm chính khoa học; corpus thực tế tập trung quy định sử dụng AI và liêm chính học thuật tại UEH, RMIT, UNA, phù hợp chủ đề quy định đại học K4-L3A. TT49 là nguồn bối cảnh. Không tuyên bố corpus bao quát mọi vấn đề đạo đức nghiên cứu.

Có **{len(data['inventory'])} tài liệu logic từ {len(set(d['metadata']['source_url'] for d in data['inventory']))} URL**, lưu trong `data/ai-liem-chinh-hoc-thuat/`. UEH/UNA được tách theo audience; không gọi đây là 10 văn bản độc lập.

{inventory}

Schema: source_url, retrieved_at, document_version, audience; thêm department, category, language, issuer, jurisdiction. Chunks bổ sung doc_id, chunk_id, chunk_index, strategy. `not-stated` là nguồn không ghi phiên bản; không tự tạo ngày hiệu lực. Nguồn được nhóm đánh dấu công khai trong sources.csv; public-source không tự đồng nghĩa giấy phép tái phân phối mở. File gốc giữ nguyên; hashes lưu trong artifacts.

## 2. Chiến lược và baseline

Phân công DKH: Khang (2A202602964, R1 · Data) dùng fixed-size 500/100; Hiệp (2A202602755, R3 · Strategy) dùng heading 800; Dũng (2A202602812, R2 · Benchmark) dùng recursive 500 theo kế hoạch. Khang đã chạy đúng tham số fixed-size, thêm ba chunkers đối chứng. Log Dũng ghi recursive/177 chunks nhưng không ghi size thực chạy. Backend thực tế: Khang TF-IDF/extractive, Hiệp Gemini/Flash, Dũng OpenAI/GPT-4.1-mini. Chưa có bench.py gốc để xác minh shared-script compliance; không tạo lượt chạy giả.

Heading giữ đường dẫn Điều/Mục trong mỗi đoạn con để dễ giải thích bằng chứng; prefix lặp tăng số chunks. Fixed-size đơn giản nhưng có thể cắt ngang câu; sentence giữ câu nhưng không khống chế cùng số ký tự; recursive ưu tiên separator, đôi khi tách phần dẫn khỏi danh sách bằng chứng.

### Baseline trên 3 tài liệu

{baseline}

Comparator ở bảng baseline dùng fixed-size 800/overlap50; cấu hình cá nhân dùng 500/100. Đây là hai thí nghiệm khác nhau, không gộp số liệu.

### So sánh có kiểm soát trong lượt local

{metrics}

TF-IDF fit một lần trên tài liệu gốc; không dùng gold/query để fit. So sánh bảng thực chạy phía trên, không suy ra heading luôn thắng. Fixed=500, recursive/heading=800, sentence=3 nên chưa cô lập thuật toán khỏi ngân sách ký tự.

## 3. Năm benchmark queries chung

Đã đồng bộ nguyên văn **5 câu, filters, doc_id chấp nhận và markers** từ log Hiệp; test tự động kiểm tra chúng khớp. [Protocol](../benchmark/PROTOCOL.md), [queries.json](../benchmark/queries.json). Q2 bắt buộc student theo ngữ cảnh; Q3/Q4 có issuer dự kiến trong gold nhưng câu hỏi gốc còn mơ hồ.

{gold}

Primary marker + accepted doc_id xác định Hit@3 và MRR local; coverage đo mọi marker trong hợp top-3. Q4 cho phép UNA faculty/general. Anchor score không phải điểm rubric. Q5 phải đọc đủ ngày và cả hai văn bản, không chỉ thấy một marker. Mã chấm gốc của Hiệp chưa có, nên điểm của Hiệp giữ đúng như log, không tự chấm lại từ preview.

## 4. So sánh thành viên và khác biệt cấu hình/query

{member_table}

Hiệp được import từ log gốc tại root; Dũng từ report/ket_qua_benchmark.txt. Giữ nguyên hai log và hashes. Các lượt API chưa tái lập tại đây. Dũng có cùng 5 ý định nhưng Q1/Q3/Q5 khác nguyên văn. Backend, matcher và implementation khác: bảng là so sánh mô tả hệ thống, không phải thí nghiệm chỉ thay chunker. Corpus hash Dũng chưa xác minh vì thiếu thuật toán tổng hợp.

{rank_comparison}

Hiệp heading có evidence Q3 RMIT ở rank 1; Khang/Dũng thiếu evidence đích Q3/Q4. Dũng có Q2 đúng rank 1 nhưng Q1/Q5 thiếu evidence, còn LLM suy diễn sai: Q1 phủ định ngưỡng; Q5 nhầm ngày ban hành thành ngày hiệu lực. Xem [đối chiếu Dũng](KET_QUA_DUNG.md) để phân biệt proxy retrieval và chất lượng câu trả lời.

### Metadata A/B

{ablation}

A/B local ghi theo bảng thực chạy, không khẳng định MRR tăng nếu số liệu không tăng. Log Hiệp: fixed 0→1, recursive/heading 1→2 điểm khi lọc student. Log Dũng: evidence student từ rank 2 lên rank 1, proxy 1→2; top-1 không filter là faculty. F2 dùng sai faculty cho Q2 làm mất bằng chứng đích.

## 5. Chất lượng câu trả lời, failure analysis và demo

Khang fixed-size 500/100 có đánh giá AI hỗ trợ theo rubric: tổng tham khảo **{sum(r['provisional_score'] for r in review['rows'])}/10**, xem [báo cáo cá nhân](REPORT_CANHAN.md). Đây là đánh giá output có evidence và lỗi thực tế, không phải điểm chính thức. Log Hiệp heading cao nhất trong ba cấu hình của Hiệp theo content score (6/10), nhưng matcher literal không thay thế đánh giá đủ ý/citation.

{failure}

Kịch bản demo đã chuẩn bị tại [DEMO.md](DEMO.md): chạy tests, benchmark chung, Q2 có/không filter, Q3 failure và so sánh ba thành viên. Chưa ghi nhận buổi thuyết trình đã thực hiện. Bài học chính: đúng file không đủ; cần đúng evidence, đúng đối tượng và đúng phạm vi nguồn.

## 6. Trạng thái nộp bài

Đã có code, báo cáo Khang, corpus, queries/gold, baseline, output và tổng hợp đủ Khang–Hiệp–Dũng. Hồ sơ đã đóng gói để nộp kèm khai báo khác backend/query/matcher. Chưa ghi nhận thuyết trình hoặc gửi bài. Nếu yêu cầu nguyên văn cùng bench.py/Gemini theo kế hoạch nhóm, cần code/config gốc và chạy lại; không xem log hiện tại là bằng chứng thỏa điều kiện đó.

{shared}
"""
    status = f"""# Trạng thái bài nộp

## Đã hoàn thành trong workspace

- [x] TODO core: chunking, similarity, store search/filter/delete và RAG agent.
- [x] Python {data['python']}: {passed}/{len(cases)} tests pass, có {core} tests gốc.
- [x] Corpus 10 tài liệu có metadata/nguồn; không sửa file gốc của nhóm.
- [x] Warm-up, phương pháp, 5 similarity predictions/results và báo cáo cá nhân Khang.
- [x] Cùng 5 queries/filters/markers với log Hiệp; đã chạy lại local trên group-dkh-v3.
- [x] So sánh 4 chiến lược local, 3 chiến lược theo log Hiệp và recursive theo log Dũng, ghi rõ backend/confounders.
- [x] Top-3 đầy đủ, scores, citations, A/B metadata, failure analysis và gold answers.
- [x] Báo cáo nhóm, kịch bản demo, instructions tái lập và khai báo hỗ trợ AI.
- [x] Đã nhận và tích hợp log Dũng, chấm đối chiếu và phân tích query variants/grounding; không sửa kết quả gốc.

## Còn cần hoạt động của nhóm

- [ ] Các thành viên đọc hiểu, xác nhận phần việc/báo cáo của mình và thực hiện demo/thuyết trình theo lịch lớp.
- [ ] Nộp bài lên kênh giảng viên yêu cầu; phiên này chưa upload hoặc gửi bài đi.

Hồ sơ code/báo cáo Khang và tổng hợp ba thành viên đã có cùng bằng chứng thực chạy. Khang fixed-size/TF-IDF có {sum(r['hit_at_3'] for r in selected['queries'])}/5 câu có primary marker trong top-3. Không đồng nghĩa điểm tối đa. Khác biệt query/backend/matcher đã công khai; chưa có shared bench.py để kiểm chứng yêu cầu đồng nhất. Thành viên tự nộp báo cáo cá nhân của mình và thực hiện demo.

Gói nộp được tạo bằng `python -m scripts.package_submission` trong `submission/`; ZIP không chứa .env, runtime, venv hoặc .git. Manifest SHA-256 bên trong dùng để kiểm tra tính toàn vẹn, không phải chữ ký số.
"""
    write_report("REPORT_CANHAN.md", personal)
    write_report("REPORT_NHOM.md", group)
    write_report("SUBMISSION_STATUS.md", status)


if __name__ == "__main__":
    main()
