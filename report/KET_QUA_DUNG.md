# Kết quả Nguyễn Việt Dũng — nhóm DKH

**MSSV:** 2A202602812 — **Vai trò:** R2 · Benchmark — **Chiến lược phân công:** Recursive 500.

Nguồn: [log Dũng gửi](ket_qua_benchmark.txt), được Khang xác nhận là kết quả Dũng. [JSON import](artifacts/dung_results.json) giữ hash file, nguyên văn câu hỏi, context/answers và A/B. Không sửa log gốc hoặc tuyên bố đã tái lập lượt API trên máy Khang.

## Cấu hình và số liệu

Log ghi recursive, 10 tài liệu, **177 chunks**, avg_len **359.49**; embedding **text-embedding-3-small**, LLM **gpt-4.1-mini**, không mock fallback. File phân công nêu size=500 nhưng log không ghi tham số, nên chưa xác minh size thực chạy. Corpus SHA-256 trong log chưa xác minh vì thiếu thuật toán tổng hợp.

| Query | Evidence rank | Doc_id /2 | Evidence proxy /2 | Rubric tham khảo /2 |
|---|---|---:|---:|---:|
| Q1 | Không có | 2 | 0 | 0 |
| Q2 | 1 | 2 | 2 | 2 |
| Q3 | Không có | 0 | 0 | 0 |
| Q4 | Không có | 0 | 0 | 0 |
| Q5 | Không có | 2 | 0 | 0 |
| Tổng | Hit@3=1/5, MRR@3=0.200 | 6/10 | 2/10 | 2/10 |

Hit@3/MRR suy ra từ evidence_rank. Rubric là đối chiếu có hỗ trợ AI, không phải điểm giảng viên; log gốc vẫn giữ UNSCORED. Matcher Dũng yêu cầu mọi anchors nằm trong **một chunk**, khác local primary-marker + coverage trên hợp top-3.

## Đánh giá từng câu

- **Q1 — 0:** context thiếu ngưỡng. Agent lại khẳng định UEH không có tỷ lệ cụ thể, vượt quá bằng chứng. Snapshot nguồn có “20% trở lên” là dấu hiệu định lượng. Phải nói thiếu evidence trong context, không phủ định sự tồn tại của quy định.
- **Q2 — 2:** rank 1 chứa xử lý bài học phần của người học; agent nêu lập biên bản/thông báo đơn vị quản lý theo Phụ lục 3, dẫn Context 1.
- **Q3 — 0 theo gold RMIT:** top-3/answer đều theo UEH, thiếu creator/năm theo gold RMIT. Query không nêu trường nên kết luận đánh giá phải giới hạn theo gold.
- **Q4 — 0 theo gold UNA:** agent trả lời nhóm dữ liệu trong UEH, nhưng không có bằng chứng UNA. Nội dung có liên quan về chủ đề, lỗi là lệch phạm vi nguồn.
- **Q5 — 0:** context có văn bản hết hiệu lực nhưng thiếu ngày hiệu lực đích. Agent nhầm ngày ban hành 30/06/2026 thành ngày hiệu lực và bỏ một văn bản. Snapshot Điều 22 ghi 15/08/2026 và hai số thông tư. Báo cáo không xác nhận tình trạng pháp lý hiện hành.

## Metadata A/B Q2

Không filter: top-1 faculty, evidence student ở rank 2, proxy=1/2. Có student filter: evidence lên rank 1, proxy=2/2. Đây là bằng chứng cụ thể về việc phân biệt đối tượng quy định.

## Tương thích với nhóm

Q2/Q4 trùng nguyên văn bộ Hiệp–Khang. Q1 dùng “%” thay “phần trăm”; Q3 rút gọn; Q5 đổi cấu trúc. Cùng 5 ý định nhưng chưa cùng 5 chuỗi query. Không sửa log để che khác biệt. Backend cũng khác kế hoạch Gemini và bản offline của Khang.

Đã đủ artifact để tổng hợp đóng góp ba thành viên, chưa đủ gọi là thí nghiệm kiểm soát chỉ thay chunker. Nếu yêu cầu nghiêm ngặt shared bench.py/Gemini, cần code/config gốc và chạy lại; không tái dựng lượt OpenAI/Gemini thật từ log.
