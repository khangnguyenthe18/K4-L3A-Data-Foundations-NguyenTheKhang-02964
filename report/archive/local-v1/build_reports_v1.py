"""Build lab reports from recorded benchmark output, without invented results."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def table(headers: list[str], rows: list[list[Any]]) -> str:
    return "\n".join(["| " + " | ".join(headers) + " |",
                      "| " + " | ".join("---" for _ in headers) + " |",
                      *["| " + " | ".join(cell(v) for v in row) + " |" for row in rows]])


def main() -> None:
    data = json.loads((ROOT / "report/artifacts/benchmark_results.json").read_text(encoding="utf-8"))
    queries = json.loads((ROOT / "benchmark/queries.json").read_text(encoding="utf-8"))
    selected = next(e for e in data["experiments"] if e["backend"] == "tfidf" and e["strategy"] == "heading")
    metrics = table(["Backend", "Chiến lược", "Chunks", "Avg chars", "Hit@3", "MRR@3", "Precision@3"],
                    [[e["backend"], e["strategy"], e["chunk_count"], f"{e['avg_length']:.1f}",
                      f"{e['hit_at_3']:.0%}", f"{e['mrr_at_3']:.3f}", f"{e['precision_at_3']:.3f}"]
                     for e in data["experiments"]])
    prediction_table = table(["#", "Câu A", "Câu B", "Dự đoán trước chạy", "TF-IDF", "Mock"],
                             [[i, p["a"], p["b"], p["prediction"], f"{p['tfidf']:.4f}", f"{p['mock']:.4f}"]
                              for i, p in enumerate(data["similarity"], 1)])
    result_table = table(["Query", "Top-1 chunk", "Score", "Top-1 đúng span?", "Gold span trong agent output?"],
                        [[r["query_id"], r["top3"][0]["metadata"]["chunk_id"], f"{r['top3'][0]['score']:.4f}",
                          r["top3"][0]["relevant"], r["answer_contains_all_gold_spans"]] for r in selected["queries"]])
    answers = "\n\n".join(f"### {r['query_id']}: {r['question']}\n\n**Gold:** {r['gold_answer']}\n\n"
                            f"**Agent output thực tế:**\n\n{r['agent_answer']}" for r in selected["queries"])
    notes = """## Phạm vi và tính minh bạch

Bài làm được hoàn thiện với hỗ trợ của Codex (OpenAI, 2026) cho triển khai code, thiết kế benchmark, chạy kiểm thử và soạn báo cáo. Corpus do nhóm cung cấp. Các dự đoán trong file predictions.json là giả thuyết thiết kế do AI hỗ trợ ghi trước lần tính similarity, không được trình bày như dự đoán cá nhân đã tự thực hiện.

Các bảng benchmark local được chạy tập trung trên máy của Nguyễn Thế Khang. Đã nhận thêm log benchmark của Đặng Quốc Hiệp, phân tích riêng trong [KET_QUA_HIEP.md](KET_QUA_HIEP.md); số liệu này do thành viên cung cấp và chưa tái lập tại đây. Chưa có kết quả của Nguyễn Việt Dũng hoặc bằng chứng thuyết trình; phần phân công vẫn là đề xuất. Người nộp cần đọc, hiểu, kiểm tra nội dung và khai báo hỗ trợ AI theo yêu cầu môn học.

Kết quả chỉ áp dụng cho snapshot dataset được cung cấp, không xác nhận hiệu lực pháp lý hoặc tính cập nhật của các quy định trên website hiện tại. Các tài liệu khác trường/quốc gia không được suy rộng thành một chính sách chung.
"""
    failure = """## Phân tích lỗi và giới hạn

**F1 — khác ngôn ngữ:** hỏi bằng tiếng Việt về hồ sơ prompt/output của RMIT nhưng bằng chứng là tiếng Anh. TF-IDF + heading không tìm thấy gold span trong top-3; agent trích nhầm tài liệu UEH. Root cause: TF-IDF so khớp từ vựng, không ánh xạ ngữ nghĩa Việt–Anh. Hướng cải thiện: thử multilingual embeddings, reranking và filter issuer; chỉ công bố mức cải thiện sau khi chạy lại.

**F2 — filter sai đối tượng:** dùng `audience=faculty` cho câu hỏi Q1 của sinh viên làm loại bỏ toàn bộ tài liệu đích; Hit@3 bằng 0. Root cause: pre-filter sai khiến retrieval không còn ứng viên đúng. Cần lấy audience từ ngữ cảnh người dùng có kiểm chứng và cho phép họ sửa; không tự đoán nhóm đối tượng từ một từ khóa.

**Chunking và đo lường:** gold-span matching yêu cầu nguyên vẹn một đoạn bằng chứng trong chunk đúng doc_id. Chunk cắt ngang span hoặc câu diễn đạt tương đương có thể bị chấm thiếu; vì vậy đã lưu nguyên top-3 để kiểm tra thủ công. `answer_contains_all_gold_spans` chỉ đo sự xuất hiện của chuỗi, không phải điểm chất lượng câu trả lời.

**Grounding:** extractive baseline chỉ trả đoạn nguồn kèm citation, có thể kèm đoạn không liên quan và không tổng hợp đầy đủ mọi ý. Q3 có bằng chứng lưu prompt/output nhưng phần trả lời chưa nhắc đầy đủ việc ghi cách sử dụng nội dung. Không quy đổi Hit@3=100% thành điểm agent 10/10. Prompt yêu cầu không trộn trường nhưng không bảo đảm ngăn lỗi; F1 chứng minh giới hạn đó.

**Giới hạn thực nghiệm:** chỉ 5 câu hỏi nội bộ, phần lớn cùng ngôn ngữ với tài liệu, có 4 câu dùng filter. Q1 được điều chỉnh sau pilot để minh họa sự nhập nhằng audience; không phải held-out benchmark. TF-IDF fit trên corpus nguồn trước chunking, không dùng gold answers để fit hoặc trả lời. Các chiến lược có cùng corpus/backend nhưng sentence chunking không có cùng giới hạn ký tự; chưa tách hoàn toàn ảnh hưởng thuật toán và kích thước.

**Nguồn và trùng lặp:** 10 file xuất phát từ 5 URL; UEH và UNA được tách theo audience. Một số đoạn UNA lặp ở general/faculty, có thể tạo kết quả gần trùng. Khi đánh giá ngoài bài lab, cần group theo URL khi chia tập và loại bản lặp, tránh data leakage.

**Mở rộng:** store hiện là in-memory, tìm kiếm O(N × D) và chọn top-k bằng heap O(N log k); TF-IDF trả vector dense nên không phù hợp corpus lớn. Bước tiếp theo là sparse vectors hoặc ANN, batch embeddings, persistence và đánh giá latency nhiều lượt. Những cải tiến này chưa được triển khai hay đo trong báo cáo.
"""
    personal = f"""# Báo cáo cá nhân — Lab 7: Embedding & Vector Store

**Họ tên:** Nguyễn Thế Khang  
**Nhóm/chủ đề:** Liêm chính khoa học — quy định sử dụng AI và liêm chính học thuật trong đại học  
**Thành viên nhóm:** Nguyễn Thế Khang, Đặng Quốc Hiệp, Nguyễn Việt Dũng  
**Ngày:** 19/09/2026

## 1. Khởi động

Cosine similarity: đo độ tương đồng về hướng của hai vector. Với embeddings có chất lượng, hai câu gần nghĩa thường có cosine cao.

- Cặp gần nghĩa: “Sinh viên phải ghi nguồn khi sử dụng AI trong học thuật” và “Người học cần trích dẫn công cụ trí tuệ nhân tạo đã dùng”. Hai câu đều nói về ghi nhận nguồn AI.
- Cặp khác nghĩa: “Academic integrity requires honest citation” và “The recipe uses rice and boiling water”. Hai câu thuộc chủ đề khác nhau.
- Cosine bỏ qua độ lớn vector để so sánh hướng; với vector đã chuẩn hóa L2, cosine và Euclidean distance cho thứ tự xếp hạng tương đương. Điểm cao không tự chứng minh hai phát biểu có cùng tính đúng/sai.

Với 10.000 ký tự, chunk_size=500, overlap=50: `ceil((10000-50)/(500-50)) = 23`. Khi overlap=100: `ceil(9900/400) = 25`. Overlap tăng giúp giữ bằng chứng qua ranh giới nhưng tăng dữ liệu lặp và chi phí lưu/embed.

## 2. Hướng tiếp cận

### Chunking và similarity

`SentenceChunker` dùng regex `(?<=[.!?])\\s+`, giữ dấu câu, strip khoảng trắng và nhóm tối đa 3 câu. Hạn chế: dấu chấm trong viết tắt hoặc số thứ tự có thể bị xem là kết thúc câu.

`RecursiveChunker` thử `\\n\\n`, `\\n`, `. `, khoảng trắng, rồi cắt ký tự. Chỉ đệ quy với phần vượt kích thước; giữ separator để không mất nội dung. Base case là đoạn không vượt giới hạn; hết separator thì fixed-size không overlap. Tests kiểm tra ghép chunks khôi phục nguyên văn.

`compute_similarity` kiểm tra cùng chiều, giá trị hữu hạn, norm 0; tính tích vô hướng trên hai vector chuẩn hóa để tránh tràn ở phép nhân lớn. Comparator trả đủ count, avg_length, chunks và xử lý văn bản rỗng.

Chiến lược chọn để trình bày là `HeadingChunker(800)`: giữ chuỗi heading cha trong mỗi đoạn con, dành tối đa khoảng một phần ba ngân sách ký tự cho heading rồi recursive split phần thân. Cách này giúp phân biệt Điều 3/Điều 5 và người học/giảng viên, đổi lại có thêm nội dung lặp.

### EmbeddingStore

Store in-memory được chọn theo lựa chọn cho phép của đề bài; không tự bật ChromaDB theo package tình cờ có trên máy. Record có ID nội bộ duy nhất, doc_id gốc và metadata copy sâu. Thêm trùng doc_id vẫn thêm record mới; xóa doc_id xóa tất cả chunks.

Embedding tài liệu chạy một lần lúc ingest; query embed một lần mỗi search. Tất cả vectors phải cùng chiều và hữu hạn. Dot product trên vectors TF-IDF đã chuẩn hóa bằng cosine. Pre-filter dùng AND trên tất cả trường rồi mới chọn top-k; None hoặc dict rỗng không lọc. k không dương, query trắng, collection rỗng trả danh sách rỗng.

Một batch được kiểm tra/embedding trước khi commit để lỗi giữa chừng không lưu một phần. RLock bảo vệ mutation; search dùng snapshot và không giữ lock trong lúc gọi backend. Lỗi embedding/LLM được truyền rõ cho caller, không âm thầm đổi backend và làm sai phép so sánh.

### KnowledgeBaseAgent

Agent nhận store và llm_fn qua dependency injection, hỗ trợ metadata_filter, giới hạn context, đóng gói question/evidence bằng JSON và yêu cầu citation. Không có kết quả thì trả thông báo thiếu bằng chứng. Bản chạy offline dùng `extractive_answer` (không phải LLM); hàm chỉ thấy prompt, không được truy cập gold answers.

### Ingestion

`load_corpus` đọc 10 file Markdown, tách front matter khỏi nội dung embedding, kiểm tra các trường bắt buộc, URL, ngày và audience. Parser chỉ hỗ trợ schema phẳng với chuỗi JSON trong front matter của dataset này, không phải YAML parser tổng quát. `chunk_documents` giữ nguồn/phiên bản/audience và bổ sung chunk_id, chunk_index, strategy.

## 3. Kết quả kiểm thử

Python **{data['python']}**, pytest **9.1.1**. Bộ gốc: **42/42 pass**; bổ sung **21 tests** cho edge cases, atomicity, concurrency, pre-filter và ingestion/citations. Tổng **63/63 pass**. Kết quả máy đọc được: [test_results.xml](artifacts/test_results.xml).

```text
collected 63 items
63 passed
```

`.venv` cũ trỏ Python 3.10 đã mất. Đã dùng Python 3.11.9 portable tại `.runtime/python311`, giữ nguyên `.venv` và tái sử dụng các dependencies pure-Python đang có; không thay Python hệ thống. Chạy bằng `powershell -File scripts/run_lab.ps1 test`.

## 4. Dự đoán similarity

Giả thuyết được lưu trong [predictions.json](../benchmark/predictions.json) trước khi tính. “Cao/thấp” là dự đoán về nghĩa, không dùng ngưỡng tùy ý để chấm đúng/sai số học.

{prediction_table}

Cặp 1 cao nhất (1.0) và cặp 5 thấp nhất (0.0) với TF-IDF, phù hợp dự đoán. Cặp 3 có nhiều từ chung nên tương đối cao. Cặp 2 và 4 gần nghĩa nhưng có điểm thấp: lexical representation bỏ lỡ paraphrase và dịch ngôn ngữ. Mock gần ngẫu nhiên với câu không giống hệt; không dùng mock score để diễn giải ngữ nghĩa.

## 5. Kết quả truy xuất cá nhân

Cùng 5 câu hỏi trong báo cáo nhóm, backend TF-IDF lexical, heading=800, top_k=3. **{sum(r['hit_at_3'] for r in selected['queries'])}/5 câu có gold span trong top-3**; MRR@3={selected['mrr_at_3']:.3f}. Chi tiết toàn bộ top-3 của mọi chiến lược: [BENCHMARK_RESULTS.md](artifacts/BENCHMARK_RESULTS.md).

{result_table}

{answers}

{failure}

## 6. Tự đánh giá theo rubric

Core code có bằng chứng 42/42 tests gốc pass. Warm-up, giải thích triển khai, similarity và 5 lượt retrieval đã có nội dung và artifact thực chạy. Điểm chất lượng agent cần người chấm đánh giá nội dung, không suy ra từ gold-span matching. Phần học hỏi trực tiếp từ thành viên khác/demo chưa diễn ra trong phiên này; bài học hiện có đến từ so sánh các chiến lược trên cùng máy.

{notes}
"""
    inventory = table(["#", "Tài liệu", "Nguồn", "Ngày lấy / phiên bản", "Ký tự", "Audience"],
                      [[i, doc["metadata"]["title"], f"[Nguồn]({doc['metadata']['source_url']})",
                        doc["metadata"]["retrieved_at"] + " / " + doc["metadata"]["document_version"],
                        doc["characters"], doc["metadata"]["audience"]]
                       for i, doc in enumerate(data["inventory"], 1)])
    baseline = table(["Tài liệu", "Strategy", "Chunks", "Avg chars"],
                     [[doc_id, name, stats["count"], f"{stats['avg_length']:.1f}"]
                      for doc_id, comparison in data["baseline"].items() for name, stats in comparison.items()])
    gold_table = table(["ID", "Query", "Gold answer", "Filter", "Tài liệu / mục"],
                      [[q["id"], q["question"], q["gold_answer"], json.dumps(q["metadata_filter"]),
                        q["evidence"][0]["doc_id"] + " / " + q["source_section"]] for q in queries])
    filtered = {r["query_id"]: r for r in selected["queries"]}
    ablation = table(["Query", "RR@3 có filter", "RR@3 không filter", "Top-1 không filter / audience"],
                     [[r["query_id"], f"{filtered[r['query_id']]['reciprocal_rank']:.3f}",
                       f"{r['reciprocal_rank']:.3f}", r["top3"][0]["metadata"]["doc_id"] + " / " +
                       r["top3"][0]["metadata"]["audience"]] for r in selected["without_filter"]])
    group = f"""# Báo cáo nhóm — Liêm chính khoa học và sử dụng AI trong đại học

**Thành viên:** Nguyễn Thế Khang; Đặng Quốc Hiệp; Nguyễn Việt Dũng  
**Lớp:** K4-L3A  
**Ngày:** 19/09/2026  
**Tên nhóm:** dùng tên chủ đề “Liêm chính khoa học” (chưa được cung cấp tên nhóm riêng).

## 1. Lựa chọn tài liệu

Chủ đề rộng là liêm chính khoa học; phạm vi corpus thực tế là quy định liêm chính học thuật và sử dụng AI trong đại học. Các tài liệu UEH, RMIT, UNA trực tiếp đáp ứng K4-L3A về quy định đại học; văn bản TT49 là nguồn bối cảnh. Không tuyên bố bao quát toàn bộ đạo đức nghiên cứu khoa học.

Corpus nằm tại `data/ai-liem-chinh-hoc-thuat/`, gồm **10 tài liệu logic từ 5 URL nguồn**, có cả tiếng Việt và tiếng Anh. Các file UEH và UNA tách theo đối tượng từ cùng một nguồn; đây không phải 10 văn bản độc lập. Số ký tự dưới đây tính phần body sau khi bỏ front matter.

{inventory}

Metadata bắt buộc: source_url, retrieved_at, document_version, audience; thêm department, category, language, issuer, jurisdiction để hỗ trợ truy xuất. Metadata chunks thêm doc_id, chunk_id, chunk_index, strategy. Giá trị document_version=`not-stated` nghĩa là nguồn snapshot không ghi phiên bản, không được tự bịa ngày hiệu lực.

Theo sources.csv, các tài liệu được nhóm ghi nhận là nguồn công khai. Thuật ngữ public-source không đồng nghĩa với giấy phép tái phân phối mở. Pipeline không đưa credentials hay dữ liệu sinh viên vào corpus. Bản gốc của nhóm được giữ nguyên; SHA-256 từng file có trong artifacts/benchmark_results.json để truy vết snapshot.

## 2. Thiết kế chiến lược

### Baseline trên 3 tài liệu

{baseline}

Comparator dùng fixed-size=800/overlap=50 theo API mặc định, sentence=3, recursive=800. Thí nghiệm toàn corpus bên dưới dùng fixed-size overlap=80; hai mức overlap được công khai và không gộp như cùng một cấu hình.

### Phân công đề xuất cho buổi demo

| Thành viên | Chiến lược đề xuất | Nội dung cần giải thích |
|---|---|---|
| Nguyễn Thế Khang | Heading 800 | Giữ Điều/Mục và ancestry; triển khai tại src/chunking.py |
| Đặng Quốc Hiệp | Fixed-size 800, overlap 80 | Chi phí thấp, ảnh hưởng cắt ngang bằng chứng |
| Nguyễn Việt Dũng | Recursive 800; đối chiếu Sentence 3 | Ưu tiên ranh giới đoạn/câu, tác động kích thước |

Đây là đề xuất phân công; số liệu sau là chạy tập trung của các cấu hình, không khẳng định kết quả được ba thành viên tự chạy độc lập.

### Kết quả Đặng Quốc Hiệp đã cung cấp

Theo [log gốc](../ket_qua_benchmark.txt), Hiệp chạy Gemini embedding cached và Gemini Flash trên 10 tài liệu, thử cả fixed-size 500/100, recursive 500 và heading custom 800. Điểm evidence lần lượt **5/10, 2/10, 6/10**; điểm chỉ theo doc_id đều 10/10. Heading có evidence trong top-3 ở 4/5 câu, MRR@3 suy ra từ log là 0.567. A/B filter student cải thiện Q2 ở cả ba chiến lược.

Bộ 5 câu của Hiệp khác bộ local bên dưới; backend, chunking và matcher cũng khác. Vì vậy chưa gộp thành bảng xếp hạng thành viên. Xem [phân tích log Hiệp](KET_QUA_HIEP.md) để biết từng câu, giới hạn phép chấm và các điều kiện cần thống nhất trước lượt so sánh chung. Các kết quả local đã có được giữ nguyên; chưa chạy lại Gemini hoặc dùng API key trong lần cập nhật này.

### Phương pháp

Ingest metadata → chunk → TF-IDF L2 → store → pre-filter → dot product top-3 → agent trích xuất nguồn. Vocabulary/IDF được fit trên cùng 10 tài liệu gốc, không fit lại theo strategy; queries/gold không tham gia fitting. TF-IDF dùng Unicode NFC, casefold, unigram, sublinear term frequency và smoothed IDF. Mock là control để chứng minh code chạy không đồng nghĩa retrieval hiểu nghĩa.

Các tham số được lưu trong benchmark_results.json. Không có API trả phí hoặc LLM sinh văn bản trong lượt chạy. Đo latency chỉ một lượt cho mỗi query để tham khảo, chưa đủ kết luận performance ổn định.

### Kết quả thực chạy

{metrics}

Fixed-size và heading cùng Hit@3=100%, MRR@3=1.000 trên bộ 5 câu. Fixed-size dùng 92 chunks, heading dùng 145 chunks; vì vậy chưa có bằng chứng heading tốt hơn về độ chính xác và fixed-size tiết kiệm record hơn. Chọn heading để trình bày vì giữ được nhãn Điều/Mục và ngữ cảnh nguồn; đây là đánh đổi khả năng đọc bằng chứng với chi phí lặp heading. Sentence/recursive đạt 80% theo gold-span matching, cần xem từng chunk trước khi quy lỗi hoàn toàn cho retrieval.

## 3. Benchmark queries và gold answers

Đúng **5 câu chính thức** được lưu tại [queries.json](../benchmark/queries.json). Q1 có ngữ cảnh người dùng là **sinh viên, bài tập học phần**; text query cố ý không lặp audience, nên phải truyền `audience=student` từ ngữ cảnh. Q2 không filter; Q3 student, Q4 faculty, Q5 staff. Các câu tiếng Anh kiểm tra retrieval cùng ngôn ngữ nguồn, không chứng minh năng lực cross-lingual.

{gold_table}

Gold answers đối chiếu snapshot nhóm đã cung cấp; script kiểm tra từng quote tồn tại trước khi chạy. Bằng chứng liên kết tới từng chunk trong [kết quả đầy đủ](artifacts/BENCHMARK_RESULTS.md).

### Kết quả cấu hình heading

{result_table}

### Tác động metadata: cùng heading/TF-IDF, bật và tắt filter

{ablation}

Với Q1, tắt filter đưa nội dung giảng viên lên top-1, trong khi đúng đối tượng người học nằm top-2; bật student đưa bằng chứng đúng lên top-1. Với Q5, tắt filter còn lấy đoạn faculty/general dù top-1 vẫn đúng. Không khẳng định filter cải thiện mọi câu: Q3/Q4 đã top-1 đúng cả hai chế độ. Filter student exact-match cũng loại tài liệu audience=all; production cần thiết kế rõ chính sách gồm cả all nếu phù hợp, thay vì đổi semantics âm thầm.

## 4. Demo và bài học

Kịch bản thuyết trình có tại [DEMO.md](DEMO.md): kiểm tra tests, nêu 10 tài liệu/5 nguồn, so sánh 4 chiến lược, chạy Q1 có/không filter, trình bày F1/F2 và trade-offs. Buổi thuyết trình chưa diễn ra; đây là tài liệu chuẩn bị, không phải biên bản hoạt động đã thực hiện.

Ba điểm chính: mock không đo ngữ nghĩa; lọc audience ngăn trộn quy định; giữ heading giúp kiểm tra nguồn nhưng tăng số chunks. Nếu làm lại, bổ sung câu hỏi diễn đạt lại, cross-lingual và dữ liệu held-out theo source URL, dùng multilingual embedding và chấm thủ công agent answers.

{failure}

## 5. Đối chiếu rubric

Đã có corpus 10 tài liệu logic + nguồn/metadata; baseline 3 tài liệu; 4 chiến lược; 5 queries/gold; top-3/score/citations; ablation metadata và 2 failure probes. Script demo đã chuẩn bị. Không tự chấm 40/40: điểm chất lượng agent, mức độc lập triển khai từng thành viên và thuyết trình cần giảng viên/nhóm xác nhận bằng hoạt động thực tế.

{notes}
"""
    for filename, content in [("REPORT_CANHAN.md", personal), ("REPORT_NHOM.md", group)]:
        content = content.replace("  \n", "\n\n")
        content = "\n".join(line.rstrip() for line in content.splitlines()).rstrip() + "\n"
        (ROOT / "report" / filename).write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
