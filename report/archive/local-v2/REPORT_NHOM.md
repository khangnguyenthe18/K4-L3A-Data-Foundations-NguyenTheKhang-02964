# Báo cáo nhóm — Liêm chính khoa học

**Thành viên:** Nguyễn Thế Khang, Đặng Quốc Hiệp, Nguyễn Việt Dũng

**Lớp:** K4-L3A — **Phiên bản:** group-hiep-v2 — **Ngày:** 19/09/2026

## 1. Bộ tài liệu và metadata

Chủ đề được nhóm chọn là liêm chính khoa học; corpus thực tế tập trung quy định sử dụng AI và liêm chính học thuật tại UEH, RMIT, UNA, phù hợp chủ đề quy định đại học K4-L3A. TT49 là nguồn bối cảnh. Không tuyên bố corpus bao quát mọi vấn đề đạo đức nghiên cứu.

Có **10 tài liệu logic từ 5 URL**, lưu trong `data/ai-liem-chinh-hoc-thuat/`. UEH/UNA được tách theo audience; không gọi đây là 10 văn bản độc lập.

| Tài liệu | Nguồn | Ngày lấy / phiên bản | Ký tự | Audience |
| --- | --- | --- | --- | --- |
| RMIT Library — Acknowledging the use of AI tools (students) | [Nguồn](https://rmit.libguides.com/referencing_AI_tools/acknowledging) | 2026-09-19 / last-updated 2026-07-29 | 3003 | student |
| RMIT Vietnam — Academic integrity and appropriate use of AI (students) | [Nguồn](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity) | 2026-09-19 / not-stated | 11327 | student |
| Thông tư 49/2026/TT-BGDĐT — Ứng dụng công nghệ và AI trong giáo dục đại học | [Nguồn](https://luatvietnam.vn/giao-duc/thong-tu-49-2026-tt-bgddt-ung-dung-cong-nghe-trong-giao-duc-dai-hoc-va-nghe-nghiep-439350-d1.html) | 2026-09-19 / 49/2026/TT-BGDĐT, ban hành 2026-06-30, hiệu lực 2026-08-15 | 12643 | all |
| UEH — Quy định kiểm soát đạo văn và sử dụng AI: quy định chung | [Nguồn](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/) | 2026-09-19 / 4002/QĐ-ĐHKT-NCPTGKTC, ban hành 2025-12-18 | 11842 | all |
| UEH — Xử lý vi phạm đạo văn và sử dụng AI đối với giảng viên, viên chức | [Nguồn](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/) | 2026-09-19 / 4002/QĐ-ĐHKT-NCPTGKTC, ban hành 2025-12-18 | 2771 | faculty |
| UEH — Xử lý vi phạm đạo văn và sử dụng AI đối với người học | [Nguồn](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/) | 2026-09-19 / 4002/QĐ-ĐHKT-NCPTGKTC, ban hành 2025-12-18 | 2783 | student |
| University of North Alabama — Generative AI Policy: faculty | [Nguồn](https://www.una.edu/academics/generative-ai-policy.html) | 2026-09-19 / not-stated | 7562 | faculty |
| University of North Alabama — Generative AI Policy: general provisions and data privacy | [Nguồn](https://www.una.edu/academics/generative-ai-policy.html) | 2026-09-19 / not-stated | 5442 | all |
| University of North Alabama — Generative AI Policy: staff | [Nguồn](https://www.una.edu/academics/generative-ai-policy.html) | 2026-09-19 / not-stated | 1145 | staff |
| University of North Alabama — Generative AI Policy: students and sample syllabus rules | [Nguồn](https://www.una.edu/academics/generative-ai-policy.html) | 2026-09-19 / not-stated | 5111 | student |

Schema: source_url, retrieved_at, document_version, audience; thêm department, category, language, issuer, jurisdiction. Chunks bổ sung doc_id, chunk_id, chunk_index, strategy. `not-stated` là nguồn không ghi phiên bản; không tự tạo ngày hiệu lực. Nguồn được nhóm đánh dấu công khai trong sources.csv; public-source không tự đồng nghĩa giấy phép tái phân phối mở. File gốc giữ nguyên; hashes lưu trong artifacts.

## 2. Chiến lược và baseline

Khang chạy fixed-size 800/overlap80, sentence 3, recursive 800 và heading 800. Hiệp đã gửi log fixed-size 500/overlap100, recursive 500, heading custom max_chars800. Dũng chưa có kết quả theo xác nhận của Khang; không gán strategy hoặc số liệu như đã thực hiện.

Heading giữ đường dẫn Điều/Mục trong mỗi đoạn con để dễ giải thích bằng chứng; prefix lặp tăng số chunks. Fixed-size đơn giản nhưng có thể cắt ngang câu; sentence giữ câu nhưng không khống chế cùng số ký tự; recursive ưu tiên separator, đôi khi tách phần dẫn khỏi danh sách bằng chứng.

### Baseline trên 3 tài liệu

| Document | Strategy | Chunks | Avg chars |
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

Comparator ở bảng này dùng fixed-size 800/overlap50 theo API; bảng toàn corpus dùng overlap80, đã ghi tách biệt trong cấu hình.

### So sánh có kiểm soát trong lượt local

| Backend | Strategy | Chunks | Avg chars | Hit@3 | MRR@3 | Anchor /10 |
| --- | --- | --- | --- | --- | --- | --- |
| tfidf | fixed_size | 92 | 762.9 | 60% | 0.600 | 6 |
| tfidf | by_sentences | 133 | 476.0 | 60% | 0.600 | 6 |
| tfidf | recursive | 102 | 623.8 | 40% | 0.400 | 4 |
| tfidf | heading | 145 | 542.8 | 60% | 0.500 | 5 |
| mock | fixed_size | 92 | 762.9 | 0% | 0.000 | 0 |
| mock | by_sentences | 133 | 476.0 | 0% | 0.000 | 0 |
| mock | recursive | 102 | 623.8 | 0% | 0.000 | 0 |
| mock | heading | 145 | 542.8 | 0% | 0.000 | 0 |

TF-IDF fit một lần trên tài liệu gốc, vocabulary/IDF cố định giữa chunkers; không fit trên gold/query. Trong v2 fixed-size, sentence và heading cùng Hit@3=60%, recursive=40%; fixed-size/sentence có MRR cao hơn heading. Vì vậy không khẳng định heading luôn tốt hơn về precision, chỉ chọn nó để trình bày cấu trúc evidence và trade-off.

## 3. Năm benchmark queries chung

Đã đồng bộ nguyên văn **5 câu, filters, doc_id chấp nhận và markers** từ log Hiệp; test tự động kiểm tra chúng khớp. [Protocol](../benchmark/PROTOCOL.md), [queries.json](../benchmark/queries.json). Q2 bắt buộc student theo ngữ cảnh; Q3/Q4 có issuer dự kiến trong gold nhưng câu hỏi gốc còn mơ hồ.

| ID | Query | Ngữ cảnh/filter | Gold answer | Vị trí bằng chứng |
| --- | --- | --- | --- | --- |
| Q1 | Theo quy định của UEH, tỷ lệ tương đồng từ bao nhiêu phần trăm thì sản phẩm học thuật bị xem là có dấu hiệu đạo văn? | Quy định UEH; phân biệt dấu hiệu và kết luận vi phạm. / null | Theo snapshot UEH, tỷ lệ tương đồng từ 20% trở lên là một dấu hiệu định lượng, sau khi loại các phần được miễn trừ nêu trong quy định; không tự động kết luận đạo văn chỉ từ tỷ lệ này. | Điều 2: Các dấu hiệu của hành vi đạo văn hoặc vi phạm liêm chính học thuật; đối chiếu Tỷ lệ tương đồng học thuật. |
| Q2 | Sản phẩm học thuật đã chỉnh sửa nhưng vẫn vi phạm lỗi đạo văn thì xử lý ra sao? | Người hỏi là sinh viên; câu hỏi nói về bài tập học phần. Truyền audience=student từ ngữ cảnh. / {"audience": "student"} | Trong bối cảnh bài tập học phần của người học: giảng viên phụ trách lập biên bản/thông báo chuyển về đơn vị quản lý để xử lý tùy mức độ vi phạm quy định tại Phụ lục 3. | Điều 3, mục 2.3(b): bài kiểm tra, bài tập, tiểu luận và các bài khác thuộc học phần. |
| Q3 | Khi ghi nhận việc dùng công cụ AI trong bài làm, câu acknowledgement cần nêu những thông tin gì? | Hỏi theo hướng dẫn RMIT Library; không trộn với hướng dẫn UEH. / null | Theo hướng dẫn RMIT Library: nêu cách sử dụng AI, tên công cụ và nhà phát triển, năm nội dung AI được người dùng tạo ra. Không bắt buộc phiên bản/ngày dùng trừ khi giảng viên yêu cầu. | Template for acknowledging the use of AI tools. |
| Q4 | Những loại thông tin nào không được phép nhập vào công cụ AI tạo sinh? | Hỏi theo chính sách UNA. Social Security numbers là marker retrieval, không phải toàn bộ gold answer. / null | Theo snapshot UNA, không nhập thông tin cá nhân, bí mật, độc quyền hoặc nhạy cảm: ví dụ hồ sơ sinh viên/tuyển sinh, số an sinh xã hội, dữ liệu thẻ/ngân hàng, giấy tờ định danh, dữ liệu y tế/bảo hiểm, dữ liệu người tham gia nghiên cứu chưa được đồng ý công khai, hồ sơ nội bộ và nội dung thuộc NDA/sở hữu trí tuệ chưa được phép. Danh sách ví dụ không giới hạn ở một loại dữ liệu. | Data Privacy and Security / Information that may NOT be input into Generative AI tools. |
| Q5 | Thông tư 49/2026/TT-BGDĐT có hiệu lực từ ngày nào và thay thế những thông tư nào? | Chỉ trả lời theo văn bản trong corpus; không coi kết quả là xác minh hiệu lực pháp lý. / null | Theo Điều 22 trong snapshot nhóm cung cấp: hiệu lực từ 15/08/2026; Thông tư 15/2018/TT-BGDĐT và 30/2023/TT-BGDĐT hết hiệu lực từ ngày đó. Đây là gold answer kiểm thử snapshot, chưa xác minh tình trạng pháp lý hiện hành. | Điều 22, khoản 1–2: Điều khoản thi hành. |

Primary marker + accepted doc_id xác định Hit@3 và MRR local; coverage đo mọi marker trong hợp top-3. Q4 cho phép UNA faculty/general. Anchor score không phải điểm rubric. Q5 phải đọc đủ ngày và cả hai văn bản, không chỉ thấy một marker. Mã chấm gốc của Hiệp chưa có, nên điểm của Hiệp giữ đúng như log, không tự chấm lại từ preview.

## 4. So sánh giữa các thành viên trên cùng câu hỏi

| Thành viên/nguồn | Strategy | Backend | Chunks | Hit@3 | MRR@3 | Anchor/log content /10 |
| --- | --- | --- | --- | --- | --- | --- |
| Khang — local | fixed_size | TF-IDF / extractive | 92 | 60% | 0.600 | 6 |
| Khang — local | by_sentences | TF-IDF / extractive | 133 | 60% | 0.600 | 6 |
| Khang — local | recursive | TF-IDF / extractive | 102 | 40% | 0.400 | 4 |
| Khang — local | heading | TF-IDF / extractive | 145 | 60% | 0.500 | 5 |
| Hiệp — log cung cấp | fixed | Gemini embedding / Flash | 162 | 80% | 0.467 | 5 |
| Hiệp — log cung cấp | recursive | Gemini embedding / Flash | 161 | 20% | 0.200 | 2 |
| Hiệp — log cung cấp | heading | Gemini embedding / Flash | 140 | 80% | 0.567 | 6 |
| Dũng | Chưa có kết quả | — | — | — | — | — |

Các số liệu Hiệp được import từ [log gốc](../ket_qua_benchmark.txt), kiểm tra tổng điểm và tính nhất quán của 15 records; chưa tái lập remote run. Khang có full artifacts, Hiệp có previews và câu trả lời LLM. Backend, parameters và implementation khác, corpus Hiệp chưa có hash. Bảng này là **so sánh hệ thống trên cùng queries**, không đủ để quy mọi khác biệt cho chunking hay xếp hạng năng lực thành viên.

| Query | Khang heading rank | Hiệp fixed rank | Hiệp recursive rank | Hiệp heading rank |
| --- | --- | --- | --- | --- |
| Q1 | 2 | None | None | 3 |
| Q2 | 1 | 2 | 1 | 1 |
| Q3 | None | 2 | None | 1 |
| Q4 | None | 1 | None | None |
| Q5 | 1 | 3 | None | 2 |

Hiệp heading có evidence Q3 RMIT ở rank 1 trong khi local thiếu; local heading có Q5 ở rank 1 còn log Hiệp ở rank 2. Q4 local thiếu UNA, Hiệp fixed tìm marker rank 1 nhưng heading/recursive không có marker. Đó là lý do cần xem từng câu thay vì chỉ một tổng điểm. Chưa có dữ liệu của Dũng để đưa vào so sánh.

### Metadata A/B

| Strategy local | Q2 RR có filter | RR không filter | Top-3 audiences không filter |
| --- | --- | --- | --- |
| fixed_size | 1.000 | 1.000 | student, faculty, student |
| by_sentences | 1.000 | 1.000 | student, faculty, student |
| recursive | 1.000 | 1.000 | student, faculty, student |
| heading | 1.000 | 1.000 | student, faculty, student |

Trong lượt local heading, Q2 vẫn đúng top-1 khi bỏ filter nhưng top-3 lẫn tài liệu faculty; filter loại nhiễu đối tượng. Không báo tăng MRR nếu số liệu không tăng. Trong log Hiệp, Q2 fixed tăng 0→1 điểm, recursive/heading tăng 1→2 điểm khi lọc student. Thí nghiệm F2 cố tình lọc faculty cho Q2 làm mất gold evidence, chứng minh filter sai có thể phá retrieval.

## 5. Chất lượng câu trả lời, failure analysis và demo

Khang heading có đánh giá AI hỗ trợ theo rubric: tổng tham khảo **5/10**, xem [báo cáo cá nhân](REPORT_CANHAN.md). Đây là đánh giá output có evidence và lỗi thực tế, không phải điểm chính thức. Log Hiệp heading cao nhất trong ba cấu hình của Hiệp theo content score (6/10), nhưng matcher literal không thay thế đánh giá đủ ý/citation.

## Phân tích lỗi và bài học

**Q3/Q4 — khác ngôn ngữ và nguồn:** query tiếng Việt, evidence đích tiếng Anh tại RMIT/UNA; lexical retrieval ưu tiên UEH và thiếu gold markers trong top-3. Root cause: TF-IDF không ánh xạ ngữ nghĩa Việt–Anh, còn query gốc không nêu issuer. Hướng cải thiện là multilingual embedding + làm rõ trường/nguồn; chưa đo mức cải thiện bằng cách đổi backend local.

**F2 — filter sai:** ép audience=faculty cho Q2 loại mọi tài liệu đích student, Hit@3=0. Filter phải lấy từ ngữ cảnh người hỏi. Exact student filter cũng loại audience=all; production phải xác định rõ có cho phép all hay không.

**Trích xuất mất ý:** phiên bản trước chỉ chọn một paragraph, có thể bỏ mất mục danh sách chứa con số dù retrieval có bằng chứng. Đã sửa extractive backend trả nguyên chunk trong context có giới hạn; test kiểm tra giữ cả con số lẫn phủ định. Vẫn có context thừa và không phải câu trả lời tổng hợp của LLM.

**Đúng tài liệu chưa đủ:** log Hiệp có doc_id score 10/10 cho mọi strategy nhưng evidence chỉ 5/10, 2/10, 6/10. Ví dụ Q1 fixed/recursive không có đoạn ngưỡng dù đúng file. Literal matcher cũng có thể chấm thiếu mẫu tương đương ở Q3 hoặc câu trả lời theo nhóm dữ liệu ở Q4; cần đọc đầy đủ output.

**Trade-off:** heading giữ Điều/Mục và ancestry để dễ kiểm tra phạm vi; số record tăng do prefix lặp. In-memory dense search O(N×D), heap top-k O(N log k), phù hợp lab nhỏ; corpus lớn cần sparse/ANN, batching và persistence. Các cải tiến đó chưa được đo ở đây.


Kịch bản demo đã chuẩn bị tại [DEMO.md](DEMO.md): chạy tests, benchmark chung, Q2 có/không filter, Q3 failure và so sánh local–Hiệp. Chưa ghi nhận buổi thuyết trình đã thực hiện. Bài học chính: đúng file không đủ; cần đúng evidence, đúng đối tượng và đúng phạm vi nguồn.

## 6. Trạng thái nộp bài

Code, báo cáo cá nhân Khang, corpus, 5 queries chung, baseline, top-3/answers, similarity, so sánh Khang–Hiệp và kịch bản demo đã có. **Chưa thể đánh dấu toàn bộ phần nhóm hoàn thành** vì chưa có kết quả Dũng và chưa thực hiện thuyết trình. Xem [SUBMISSION_STATUS.md](SUBMISSION_STATUS.md); không tạo kết quả để lấp chỗ trống.

## Giới hạn và khai báo hỗ trợ

Codex (OpenAI, 2026) hỗ trợ triển khai, chạy tests/benchmark và soạn báo cáo. Corpus và log Hiệp do người dùng cung cấp. Dự đoán similarity là giả thuyết thiết kế có hỗ trợ AI, đã lưu trước lượt tính; không mô tả như dự đoán tự làm của sinh viên. Người nộp cần hiểu, kiểm tra và khai báo hỗ trợ theo yêu cầu môn học.

Local dùng TF-IDF lexical + extractive evidence output, không dùng LLM hay API key. Log Hiệp khai báo Gemini embedding cached + Gemini Flash; được import, chưa chạy tái lập. Dũng chưa có kết quả theo xác nhận của Khang. Buổi demo/thuyết trình chưa diễn ra trong phiên này.

Các gold answers là kiểm thử snapshot tài liệu đã có, không xác nhận chính sách/hiệu lực pháp lý hiện hành. Có 10 file nhưng chỉ 5 URL; một số đoạn UNA lặp giữa general/faculty. Khi chia train/test cần group theo nguồn. Năm queries là bộ đánh giá nội bộ, không phải held-out test; Q3/Q4 thiếu issuer trong câu hỏi nguyên văn nên có độ mơ hồ ngoài ngữ cảnh gold.

Không suy ra chất lượng câu trả lời chỉ từ marker hay doc_id. Các số liệu local-v1 (bộ cũ đạt 5/5) chỉ còn trong archive; bài nộp dùng group-hiep-v2.
