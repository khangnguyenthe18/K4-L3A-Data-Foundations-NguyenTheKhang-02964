# Benchmark chung — group-dkh-v3

Nguồn 5 queries: `ket_qua_benchmark.txt` do Đặng Quốc Hiệp gửi. `queries.json` giữ nguyên văn câu hỏi, filter, các doc_id chấp nhận và evidence markers của log. Bổ sung gold answers, vị trí nguồn và user_context để giải thích phạm vi câu hỏi; không đưa gold vào embedding hoặc agent.

## Quy tắc

1. Dùng 10 Markdown trong `data/ai-liem-chinh-hoc-thuat/`. Lưu hash từng file cùng kết quả để xác định snapshot.
2. Chạy đúng Q1–Q5; Q2 có `audience=student` (người học, bài tập học phần). Q3 theo RMIT Library; Q4 theo UNA. Hai issuer này được ghi trong user_context/gold để chấm nhưng text query gốc không nêu rõ: đây là hạn chế bộ câu hỏi, không tự coi mọi câu trả lời từ trường khác là sai về nội dung nói chung.
3. Top-k=3. Lưu đầy đủ chunk_id, content, metadata, similarity score và agent output. Log Hiệp chỉ có preview nên không tái chấm từ toàn văn chunks.
4. Local: Hit@3/MRR@3 tính theo **marker đầu tiên** trong đúng tài liệu được chấp nhận. Q4 chấp nhận faculty hoặc general của UNA. `anchor_score` = 2 tại rank 1; 1 tại rank 2/3; 0 khi không có. Coverage đo từng marker trong hợp top-3. Q5 cần ngày hiệu lực và số văn bản thứ hai; gold answer đầy đủ còn phải nêu văn bản thứ nhất.
5. Điểm anchor không phải điểm rubric. Chấm thủ công độ đúng/đủ của câu trả lời, citation và việc phân biệt trường/đối tượng. Marker đơn lẻ không đủ chứng minh trả lời đầy đủ Q3/Q4/Q5.
6. Bảng Khang–Hiệp so sánh hệ thống trên cùng câu hỏi, **không cô lập tác động chunking**: backend embedding, answer backend, parameters và implementation khác nhau. Bảng 4 chiến lược local kiểm soát corpus/TF-IDF, nhưng sentence chunking không có cùng ngân sách ký tự.

## Trạng thái thành viên

- Nguyễn Thế Khang: đã chạy code local trên group-dkh-v3; có full artifacts.
- Đặng Quốc Hiệp: đã có log 3 chiến lược với Gemini; được import và kiểm tra tổng điểm/nhất quán câu hỏi, chưa tái lập remote run.
- Nguyễn Việt Dũng: đã nhận log recursive/OpenAI tại report/ket_qua_benchmark.txt. Q1/Q3/Q5 là biến thể cách diễn đạt của bộ Hiệp, Q2/Q4 trùng nguyên văn; đã lưu query_alignment trong dung_results.json. Matcher yêu cầu tất cả anchors trong một chunk, khác local. Không tuyên bố ba lượt chạy hoàn toàn đồng nhất.

## Tái lập

```powershell
powershell -File scripts/run_lab.ps1 benchmark
```

Lượt này dùng TF-IDF + extractive answer offline. Không cần Gemini API key. Để chạy so sánh kiểm soát với Hiệp cần cùng embedding/model settings, corpus hashes, code chunker/scorer và cấu hình LLM của Hiệp; các phần đó chưa được cung cấp.

Kết quả local-v1 và bộ câu cũ chỉ là lịch sử thử nghiệm, ở `report/archive/local-v1/` và `benchmark/archive/queries-local-v1.json`. Không lấy kết quả 5/5 của v1 làm kết quả của group-dkh-v3.

## Phân công DKH và kết quả thực tế

Khang — 2A202602964, R1 Data, fixed-size 500/100 (đã chạy local); Hiệp — 2A202602755, R3 Strategy, heading800 theo log; Dũng — 2A202602812, R2 Benchmark, recursive500 theo kế hoạch (log không ghi size, chưa xác minh). Nhóm dự kiến Gemini và shared bench.py, nhưng lượt thực có ba backend khác nhau. Báo cáo công khai deviation, không gán tên Gemini cho kết quả offline/OpenAI. Bộ v2 cũ được giữ trong report/archive/local-v2.
