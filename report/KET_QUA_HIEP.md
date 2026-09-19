# Kết quả benchmark do Đặng Quốc Hiệp cung cấp

Nguồn: [ket_qua_benchmark.txt](../ket_qua_benchmark.txt), được Nguyễn Thế Khang xác nhận là file Hiệp gửi. Các số liệu dưới đây được đọc từ log, chưa chạy tái lập trên máy hiện tại. Giữ nguyên file gốc để đối chiếu.

## Cấu hình được ghi trong log

- Corpus: `data/ai-liem-chinh-hoc-thuat`, 10 tài liệu. Log không có SHA-256 nên chưa xác nhận snapshot giống hệt corpus local.
- Embedding: `gemini-embedding-001 (cached)`.
- LLM: `gemini-2.5-flash`.
- Retrieval: top-3; Q2 dùng `audience=student`, các câu khác không filter.
- Chưa có mã benchmark, toàn văn chunks/cache, dimension/task type của embeddings, prompt LLM hoặc cấu hình generation để tái lập hoàn toàn.

## Tổng hợp theo log

| Strategy | Tham số | Chunks | Avg/min/max ký tự | Chấm doc_id | Chấm evidence | Hit@3 từ evidence_rank | MRR@3 từ evidence_rank |
|---|---|---:|---|---:|---:|---:|---:|
| Fixed-size | size=500, overlap=100 | 162 | 487 / 127 / 500 | 10/10 | 5/10 | 4/5 | 0.467 |
| Recursive | size=500 | 161 | 393 / 84 / 500 | 10/10 | 2/10 | 1/5 | 0.200 |
| Heading custom | max_chars=800, theo Điều/mục | 140 | 552 / 158 / 798 | 10/10 | 6/10 | 4/5 | 0.567 |

Hit@3 và MRR@3 trong bảng được suy ra từ evidence_rank của log: rank=None tính 0, rank=r tính reciprocal rank=1/r. Không đồng nhất điểm evidence /10 với Hit@3 hoặc điểm chất lượng câu trả lời do người chấm xác nhận. Từ các dòng đã ghi, quy tắc điểm evidence tương ứng 2 điểm khi rank=1, 1 điểm khi rank=2/3 và 0 khi không có evidence; chưa có code để kiểm tra cách khớp nhiều evidence trong Q5.

## Năm câu hỏi của Hiệp

| Câu | Nội dung | Evidence được cấu hình trong log | Fixed / Recursive / Heading (điểm trên 2) |
|---|---|---|---|
| Q1 | Ngưỡng tỷ lệ tương đồng có dấu hiệu đạo văn tại UEH | `20% trở lên` | 0 / 0 / 1 |
| Q2 | Xử lý người học vẫn vi phạm đạo văn sau chỉnh sửa | `lập biên bản` | 1 / 2 / 2 |
| Q3 | Thông tin phải nêu trong acknowledgement công cụ AI | `the name of the AI tool and its creator` | 1 / 0 / 2 |
| Q4 | Các loại thông tin không được nhập vào generative AI | `Social Security numbers` | 2 / 0 / 0 |
| Q5 | Ngày hiệu lực và văn bản được thay thế của TT49 | Hai cụm ngày hiệu lực và số văn bản trong log | 1 / 0 / 1 |

Các mô tả trên chỉ tóm tắt bài kiểm tra retrieval dựa trên snapshot; không xác nhận tính hiện hành của văn bản pháp luật.

## Những kết luận có bằng chứng

**Chỉ kiểm tra doc_id làm đánh giá quá lạc quan.** Cả ba chiến lược đều 10/10 theo doc_id, nhưng evidence chỉ 5/10, 2/10 và 6/10. Q1 fixed/recursive lấy đúng tài liệu UEH nhưng thiếu đoạn chứa ngưỡng cần trả lời; agent thông báo context không có con số. Root cause: retrieval đúng tài liệu nhưng sai đoạn chứa bằng chứng.

**Heading tốt nhất theo tổng điểm evidence trong lượt chạy này.** Heading tìm được evidence Q1 ở rank 3, Q3 ở rank 1 và Q5 ở rank 2. Fixed-size cùng Hit@3=4/5 nhưng MRR thấp hơn. Chưa thể tách tác động heading khỏi kích thước: heading có ngân sách 800, hai cấu hình còn lại dùng 500.

**Metadata cải thiện Q2.** Đây là câu hỏi của người học, trong khi văn bản giảng viên có cách diễn đạt tương tự:

| Strategy | Điểm evidence không filter | Có student filter | Quan sát |
|---|---:|---:|---|
| Fixed-size | 0/2 | 1/2 | Không filter: hai kết quả đầu là faculty; có filter: evidence xuất hiện ở rank 2 |
| Recursive | 1/2 | 2/2 | Evidence đúng chuyển từ rank 2 lên rank 1 |
| Heading | 1/2 | 2/2 | Evidence đúng chuyển từ rank 2 lên rank 1 |

**Cross-lingual có tín hiệu tích cực nhưng chưa chứng minh hơn baseline local.** Q3 bằng tiếng Việt truy xuất tài liệu RMIT tiếng Anh; heading có evidence rank 1. Tuy nhiên câu hỏi local trước đây khác nội dung nên không dùng kết quả này để định lượng mức Gemini cải thiện so với TF-IDF.

## Lưu ý về phép chấm và câu trả lời

- Q3 recursive nhận 0 theo literal evidence, nhưng top-3 có mẫu `I used [tool used] (Creator, year)...`; thông tin tương đương có thể hiện diện. Agent còn tổng hợp từ UEH và RMIT. Cần gold answer theo từng issuer và kiểm tra thủ công trước khi kết luận hoàn toàn không có bằng chứng.
- Q4 hỏi rộng về loại thông tin, nhưng matcher chỉ yêu cầu `Social Security numbers`. Agent recursive/heading vẫn trả các nhóm thông tin cấm; điểm 0 chỉ chứng minh thiếu cụm mục tiêu theo log, không đủ chứng minh toàn bộ câu trả lời sai. Nên chấm nhiều ý bắt buộc hoặc thu hẹp câu hỏi tương ứng.
- Q4 fixed có agent output kết thúc giữa câu (`Số`); log có vẻ cắt phần hiển thị. Không thể chấm độ đầy đủ chỉ từ preview này.
- Q5 có hai evidence nhưng thiếu code matcher; cần xác định kiểm tra all/any và cho phép bằng chứng nằm ở nhiều chunks. Không coi một evidence_rank là xác nhận đủ mọi ý.
- Các score similarity chỉ nên so sánh trong cùng backend/cấu hình; không so sánh trực tiếp score Gemini khoảng 0.8 với score TF-IDF local.

## Đối chiếu với lượt local của Khang

| Yếu tố | Local Khang | Log Hiệp |
|---|---|---|
| Embedding | TF-IDF lexical; mock control | Gemini embedding cached |
| Answer backend | Extractive evidence preview | Gemini Flash |
| Năm queries | `benchmark/queries.json`, group-dkh-v3, đã đồng bộ | Năm câu gốc ở bảng trên |
| Fixed-size | 500 / overlap 100 (v3) | 500 / overlap 100 |
| Recursive | 800 | 500 |
| Heading | 800, 145 chunks | Custom 800, 140 chunks |
| Evidence matching | Full normalized span + doc_id | Các cụm evidence trong log, thiếu mã matcher |

Đã chuyển lượt local sang đúng 5 câu, filters và markers của Hiệp, rồi chạy lại: xem `benchmark/PROTOCOL.md` và báo cáo nhóm. Bộ local-v1 cũ được lưu ở archive, không dùng để đối chiếu với log này nữa. Hai backend/implementations vẫn khác nên đây là so sánh hệ thống trên cùng câu hỏi, chưa phải thí nghiệm cô lập chunking. Khi có mã, cấu hình và cache của Hiệp có thể tái lập chính xác hơn. Đã nhận kết quả Dũng và tổng hợp trong KET_QUA_DUNG.md: recursive/OpenAI, evidence 2/10 theo log; Q1/Q3/Q5 khác nguyên văn và matcher khác. Không coi đây là phép so sánh chỉ đổi chunker.
