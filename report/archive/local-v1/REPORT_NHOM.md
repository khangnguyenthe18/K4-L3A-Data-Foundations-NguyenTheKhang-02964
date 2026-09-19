# Báo cáo nhóm — Liêm chính khoa học và sử dụng AI trong đại học

**Thành viên:** Nguyễn Thế Khang; Đặng Quốc Hiệp; Nguyễn Việt Dũng

**Lớp:** K4-L3A

**Ngày:** 19/09/2026

**Tên nhóm:** dùng tên chủ đề “Liêm chính khoa học” (chưa được cung cấp tên nhóm riêng).

## 1. Lựa chọn tài liệu

Chủ đề rộng là liêm chính khoa học; phạm vi corpus thực tế là quy định liêm chính học thuật và sử dụng AI trong đại học. Các tài liệu UEH, RMIT, UNA trực tiếp đáp ứng K4-L3A về quy định đại học; văn bản TT49 là nguồn bối cảnh. Không tuyên bố bao quát toàn bộ đạo đức nghiên cứu khoa học.

Corpus nằm tại `data/ai-liem-chinh-hoc-thuat/`, gồm **10 tài liệu logic từ 5 URL nguồn**, có cả tiếng Việt và tiếng Anh. Các file UEH và UNA tách theo đối tượng từ cùng một nguồn; đây không phải 10 văn bản độc lập. Số ký tự dưới đây tính phần body sau khi bỏ front matter.

| # | Tài liệu | Nguồn | Ngày lấy / phiên bản | Ký tự | Audience |
| --- | --- | --- | --- | --- | --- |
| 1 | RMIT Library — Acknowledging the use of AI tools (students) | [Nguồn](https://rmit.libguides.com/referencing_AI_tools/acknowledging) | 2026-09-19 / last-updated 2026-07-29 | 3003 | student |
| 2 | RMIT Vietnam — Academic integrity and appropriate use of AI (students) | [Nguồn](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity) | 2026-09-19 / not-stated | 11327 | student |
| 3 | Thông tư 49/2026/TT-BGDĐT — Ứng dụng công nghệ và AI trong giáo dục đại học | [Nguồn](https://luatvietnam.vn/giao-duc/thong-tu-49-2026-tt-bgddt-ung-dung-cong-nghe-trong-giao-duc-dai-hoc-va-nghe-nghiep-439350-d1.html) | 2026-09-19 / 49/2026/TT-BGDĐT, ban hành 2026-06-30, hiệu lực 2026-08-15 | 12643 | all |
| 4 | UEH — Quy định kiểm soát đạo văn và sử dụng AI: quy định chung | [Nguồn](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/) | 2026-09-19 / 4002/QĐ-ĐHKT-NCPTGKTC, ban hành 2025-12-18 | 11842 | all |
| 5 | UEH — Xử lý vi phạm đạo văn và sử dụng AI đối với giảng viên, viên chức | [Nguồn](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/) | 2026-09-19 / 4002/QĐ-ĐHKT-NCPTGKTC, ban hành 2025-12-18 | 2771 | faculty |
| 6 | UEH — Xử lý vi phạm đạo văn và sử dụng AI đối với người học | [Nguồn](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/) | 2026-09-19 / 4002/QĐ-ĐHKT-NCPTGKTC, ban hành 2025-12-18 | 2783 | student |
| 7 | University of North Alabama — Generative AI Policy: faculty | [Nguồn](https://www.una.edu/academics/generative-ai-policy.html) | 2026-09-19 / not-stated | 7562 | faculty |
| 8 | University of North Alabama — Generative AI Policy: general provisions and data privacy | [Nguồn](https://www.una.edu/academics/generative-ai-policy.html) | 2026-09-19 / not-stated | 5442 | all |
| 9 | University of North Alabama — Generative AI Policy: staff | [Nguồn](https://www.una.edu/academics/generative-ai-policy.html) | 2026-09-19 / not-stated | 1145 | staff |
| 10 | University of North Alabama — Generative AI Policy: students and sample syllabus rules | [Nguồn](https://www.una.edu/academics/generative-ai-policy.html) | 2026-09-19 / not-stated | 5111 | student |

Metadata bắt buộc: source_url, retrieved_at, document_version, audience; thêm department, category, language, issuer, jurisdiction để hỗ trợ truy xuất. Metadata chunks thêm doc_id, chunk_id, chunk_index, strategy. Giá trị document_version=`not-stated` nghĩa là nguồn snapshot không ghi phiên bản, không được tự bịa ngày hiệu lực.

Theo sources.csv, các tài liệu được nhóm ghi nhận là nguồn công khai. Thuật ngữ public-source không đồng nghĩa với giấy phép tái phân phối mở. Pipeline không đưa credentials hay dữ liệu sinh viên vào corpus. Bản gốc của nhóm được giữ nguyên; SHA-256 từng file có trong artifacts/benchmark_results.json để truy vết snapshot.

## 2. Thiết kế chiến lược

### Baseline trên 3 tài liệu

| Tài liệu | Strategy | Chunks | Avg chars |
| --- | --- | --- | --- |
| rmit-ai-acknowledgement-guide | fixed_size | 4 | 788.2 |
| rmit-ai-acknowledgement-guide | by_sentences | 6 | 497.5 |
| rmit-ai-acknowledgement-guide | recursive | 5 | 600.6 |
| rmit-vn-academic-integrity-ai | fixed_size | 16 | 754.8 |
| rmit-vn-academic-integrity-ai | by_sentences | 30 | 374.9 |
| rmit-vn-academic-integrity-ai | recursive | 16 | 707.9 |
| tt49-2026-ung-dung-cong-nghe-ai | fixed_size | 17 | 790.8 |
| tt49-2026-ung-dung-cong-nghe-ai | by_sentences | 25 | 503.5 |
| tt49-2026-ung-dung-cong-nghe-ai | recursive | 19 | 665.4 |

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

| Backend | Chiến lược | Chunks | Avg chars | Hit@3 | MRR@3 | Precision@3 |
| --- | --- | --- | --- | --- | --- | --- |
| tfidf | fixed_size | 92 | 762.9 | 100% | 1.000 | 0.333 |
| tfidf | by_sentences | 133 | 476.0 | 80% | 0.700 | 0.267 |
| tfidf | recursive | 102 | 623.8 | 80% | 0.800 | 0.267 |
| tfidf | heading | 145 | 542.8 | 100% | 1.000 | 0.333 |
| mock | fixed_size | 92 | 762.9 | 40% | 0.167 | 0.133 |
| mock | by_sentences | 133 | 476.0 | 20% | 0.067 | 0.067 |
| mock | recursive | 102 | 623.8 | 20% | 0.100 | 0.067 |
| mock | heading | 145 | 542.8 | 20% | 0.200 | 0.067 |

Fixed-size và heading cùng Hit@3=100%, MRR@3=1.000 trên bộ 5 câu. Fixed-size dùng 92 chunks, heading dùng 145 chunks; vì vậy chưa có bằng chứng heading tốt hơn về độ chính xác và fixed-size tiết kiệm record hơn. Chọn heading để trình bày vì giữ được nhãn Điều/Mục và ngữ cảnh nguồn; đây là đánh đổi khả năng đọc bằng chứng với chi phí lặp heading. Sentence/recursive đạt 80% theo gold-span matching, cần xem từng chunk trước khi quy lỗi hoàn toàn cho retrieval.

## 3. Benchmark queries và gold answers

Đúng **5 câu chính thức** được lưu tại [queries.json](../benchmark/queries.json). Q1 có ngữ cảnh người dùng là **sinh viên, bài tập học phần**; text query cố ý không lặp audience, nên phải truyền `audience=student` từ ngữ cảnh. Q2 không filter; Q3 student, Q4 faculty, Q5 staff. Các câu tiếng Anh kiểm tra retrieval cùng ngôn ngữ nguồn, không chứng minh năng lực cross-lingual.

| ID | Query | Gold answer | Filter | Tài liệu / mục |
| --- | --- | --- | --- | --- |
| Q1 | Tại UEH, sau khi chỉnh sửa nhưng vẫn vi phạm sử dụng AI trong học thuật thì xử lý thế nào? | Với người học, giảng viên phụ trách học phần lập biên bản, thông báo chuyển cho đơn vị quản lý để xử lý tùy theo mức độ vi phạm. | {"audience": "student"} | ueh-xu-ly-vi-pham-nguoi-hoc / Điều 5, mục 2.2(b), áp dụng cho bài tập học phần của người học. |
| Q2 | Theo UEH, tỷ lệ tương đồng học thuật có phải là căn cứ duy nhất để kết luận đạo văn không? | Không. Tỷ lệ tương đồng không phải căn cứ duy nhất; cần xem xét chuyên môn của đơn vị quản lý, giảng viên hoặc hội đồng có thẩm quyền. | null | ueh-dao-van-ai-quy-dinh-chung / Điều 2, Tỷ lệ tương đồng học thuật. |
| Q3 | According to RMIT Library, what records of AI prompts and outputs should students save? | Keep a record of prompts, generated outputs and how the content was used; save copies because an educator may request them. | {"audience": "student"} | rmit-ai-acknowledgement-guide / Overall guidelines for acknowledging the use of AI tools. |
| Q4 | At UNA, should faculty use AI-detection software as the single means of verifying originality? | No. Faculty should avoid using AI-detection software as the single means of verifying originality. | {"audience": "faculty"} | una-genai-policy-faculty / Faculty. |
| Q5 | At UNA, what information may staff not share with generative AI, and may they create AI-generated promotional images? | Staff must avoid sharing confidential information, including student data protected under FERPA. Creating AI-generated images for promotional materials is not allowed in the supplied policy. | {"audience": "staff"} | una-genai-policy-staff / Staff. |

Gold answers đối chiếu snapshot nhóm đã cung cấp; script kiểm tra từng quote tồn tại trước khi chạy. Bằng chứng liên kết tới từng chunk trong [kết quả đầy đủ](artifacts/BENCHMARK_RESULTS.md).

### Kết quả cấu hình heading

| Query | Top-1 chunk | Score | Top-1 đúng span? | Gold span trong agent output? |
| --- | --- | --- | --- | --- |
| Q1 | ueh-xu-ly-vi-pham-nguoi-hoc:heading:005 | 0.4540 | True | True |
| Q2 | ueh-dao-van-ai-quy-dinh-chung:heading:004 | 0.5786 | True | True |
| Q3 | rmit-ai-acknowledgement-guide:heading:002 | 0.3765 | True | True |
| Q4 | una-genai-policy-faculty:heading:014 | 0.5401 | True | True |
| Q5 | una-genai-policy-staff:heading:001 | 0.3714 | True | True |

### Tác động metadata: cùng heading/TF-IDF, bật và tắt filter

| Query | RR@3 có filter | RR@3 không filter | Top-1 không filter / audience |
| --- | --- | --- | --- |
| Q1 | 1.000 | 0.500 | ueh-xu-ly-vi-pham-giang-vien / faculty |
| Q3 | 1.000 | 1.000 | rmit-ai-acknowledgement-guide / student |
| Q4 | 1.000 | 1.000 | una-genai-policy-faculty / faculty |
| Q5 | 1.000 | 1.000 | una-genai-policy-staff / staff |

Với Q1, tắt filter đưa nội dung giảng viên lên top-1, trong khi đúng đối tượng người học nằm top-2; bật student đưa bằng chứng đúng lên top-1. Với Q5, tắt filter còn lấy đoạn faculty/general dù top-1 vẫn đúng. Không khẳng định filter cải thiện mọi câu: Q3/Q4 đã top-1 đúng cả hai chế độ. Filter student exact-match cũng loại tài liệu audience=all; production cần thiết kế rõ chính sách gồm cả all nếu phù hợp, thay vì đổi semantics âm thầm.

## 4. Demo và bài học

Kịch bản thuyết trình có tại [DEMO.md](DEMO.md): kiểm tra tests, nêu 10 tài liệu/5 nguồn, so sánh 4 chiến lược, chạy Q1 có/không filter, trình bày F1/F2 và trade-offs. Buổi thuyết trình chưa diễn ra; đây là tài liệu chuẩn bị, không phải biên bản hoạt động đã thực hiện.

Ba điểm chính: mock không đo ngữ nghĩa; lọc audience ngăn trộn quy định; giữ heading giúp kiểm tra nguồn nhưng tăng số chunks. Nếu làm lại, bổ sung câu hỏi diễn đạt lại, cross-lingual và dữ liệu held-out theo source URL, dùng multilingual embedding và chấm thủ công agent answers.

## Phân tích lỗi và giới hạn

**F1 — khác ngôn ngữ:** hỏi bằng tiếng Việt về hồ sơ prompt/output của RMIT nhưng bằng chứng là tiếng Anh. TF-IDF + heading không tìm thấy gold span trong top-3; agent trích nhầm tài liệu UEH. Root cause: TF-IDF so khớp từ vựng, không ánh xạ ngữ nghĩa Việt–Anh. Hướng cải thiện: thử multilingual embeddings, reranking và filter issuer; chỉ công bố mức cải thiện sau khi chạy lại.

**F2 — filter sai đối tượng:** dùng `audience=faculty` cho câu hỏi Q1 của sinh viên làm loại bỏ toàn bộ tài liệu đích; Hit@3 bằng 0. Root cause: pre-filter sai khiến retrieval không còn ứng viên đúng. Cần lấy audience từ ngữ cảnh người dùng có kiểm chứng và cho phép họ sửa; không tự đoán nhóm đối tượng từ một từ khóa.

**Chunking và đo lường:** gold-span matching yêu cầu nguyên vẹn một đoạn bằng chứng trong chunk đúng doc_id. Chunk cắt ngang span hoặc câu diễn đạt tương đương có thể bị chấm thiếu; vì vậy đã lưu nguyên top-3 để kiểm tra thủ công. `answer_contains_all_gold_spans` chỉ đo sự xuất hiện của chuỗi, không phải điểm chất lượng câu trả lời.

**Grounding:** extractive baseline chỉ trả đoạn nguồn kèm citation, có thể kèm đoạn không liên quan và không tổng hợp đầy đủ mọi ý. Q3 có bằng chứng lưu prompt/output nhưng phần trả lời chưa nhắc đầy đủ việc ghi cách sử dụng nội dung. Không quy đổi Hit@3=100% thành điểm agent 10/10. Prompt yêu cầu không trộn trường nhưng không bảo đảm ngăn lỗi; F1 chứng minh giới hạn đó.

**Giới hạn thực nghiệm:** chỉ 5 câu hỏi nội bộ, phần lớn cùng ngôn ngữ với tài liệu, có 4 câu dùng filter. Q1 được điều chỉnh sau pilot để minh họa sự nhập nhằng audience; không phải held-out benchmark. TF-IDF fit trên corpus nguồn trước chunking, không dùng gold answers để fit hoặc trả lời. Các chiến lược có cùng corpus/backend nhưng sentence chunking không có cùng giới hạn ký tự; chưa tách hoàn toàn ảnh hưởng thuật toán và kích thước.

**Nguồn và trùng lặp:** 10 file xuất phát từ 5 URL; UEH và UNA được tách theo audience. Một số đoạn UNA lặp ở general/faculty, có thể tạo kết quả gần trùng. Khi đánh giá ngoài bài lab, cần group theo URL khi chia tập và loại bản lặp, tránh data leakage.

**Mở rộng:** store hiện là in-memory, tìm kiếm O(N × D) và chọn top-k bằng heap O(N log k); TF-IDF trả vector dense nên không phù hợp corpus lớn. Bước tiếp theo là sparse vectors hoặc ANN, batch embeddings, persistence và đánh giá latency nhiều lượt. Những cải tiến này chưa được triển khai hay đo trong báo cáo.


## 5. Đối chiếu rubric

Đã có corpus 10 tài liệu logic + nguồn/metadata; baseline 3 tài liệu; 4 chiến lược; 5 queries/gold; top-3/score/citations; ablation metadata và 2 failure probes. Script demo đã chuẩn bị. Không tự chấm 40/40: điểm chất lượng agent, mức độc lập triển khai từng thành viên và thuyết trình cần giảng viên/nhóm xác nhận bằng hoạt động thực tế.

## Phạm vi và tính minh bạch

Bài làm được hoàn thiện với hỗ trợ của Codex (OpenAI, 2026) cho triển khai code, thiết kế benchmark, chạy kiểm thử và soạn báo cáo. Corpus do nhóm cung cấp. Các dự đoán trong file predictions.json là giả thuyết thiết kế do AI hỗ trợ ghi trước lần tính similarity, không được trình bày như dự đoán cá nhân đã tự thực hiện.

Các bảng benchmark local được chạy tập trung trên máy của Nguyễn Thế Khang. Đã nhận thêm log benchmark của Đặng Quốc Hiệp, phân tích riêng trong [KET_QUA_HIEP.md](KET_QUA_HIEP.md); số liệu này do thành viên cung cấp và chưa tái lập tại đây. Chưa có kết quả của Nguyễn Việt Dũng hoặc bằng chứng thuyết trình; phần phân công vẫn là đề xuất. Người nộp cần đọc, hiểu, kiểm tra nội dung và khai báo hỗ trợ AI theo yêu cầu môn học.

Kết quả chỉ áp dụng cho snapshot dataset được cung cấp, không xác nhận hiệu lực pháp lý hoặc tính cập nhật của các quy định trên website hiện tại. Các tài liệu khác trường/quốc gia không được suy rộng thành một chính sách chung.
