# Trạng thái bài nộp

## Đã hoàn thành trong workspace

- [x] TODO core: chunking, similarity, store search/filter/delete và RAG agent.
- [x] Python 3.11.9: 71/71 tests pass, có 42 tests gốc.
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

Hồ sơ code/báo cáo Khang và tổng hợp ba thành viên đã có cùng bằng chứng thực chạy. Khang fixed-size/TF-IDF có 2/5 câu có primary marker trong top-3. Không đồng nghĩa điểm tối đa. Khác biệt query/backend/matcher đã công khai; chưa có shared bench.py để kiểm chứng yêu cầu đồng nhất. Thành viên tự nộp báo cáo cá nhân của mình và thực hiện demo.

Gói nộp được tạo bằng `python -m scripts.package_submission` trong `submission/`; ZIP không chứa .env, runtime, venv hoặc .git. Manifest SHA-256 bên trong dùng để kiểm tra tính toàn vẹn, không phải chữ ký số.
