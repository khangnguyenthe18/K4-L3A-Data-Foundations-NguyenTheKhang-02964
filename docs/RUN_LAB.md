# Cách chạy bài nộp — group-dkh-v3

## Máy Windows hiện tại

Python 3.11.9 portable đã có tại `.runtime/python311/` (gitignored). `.venv` cũ trỏ interpreter đã mất, không sử dụng nó trên máy này.

```powershell
powershell -File scripts/run_lab.ps1 test
powershell -File scripts/run_lab.ps1 benchmark
powershell -File scripts/run_lab.ps1 demo
```

Tái tạo toàn bộ tests, import log Hiệp, benchmark, báo cáo và ZIP:

```powershell
powershell -File scripts/run_lab.ps1 finalize
```

Lệnh finalize ghi lại báo cáo/artifacts từ dữ liệu hiện tại; giữ riêng chỉnh sửa thủ công nếu muốn bảo toàn. ZIP nằm tại `submission/K4-L3A-NguyenTheKhang-02964.zip`.

## Máy khác có Python 3.11

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -X utf8 -m scripts.finalize_lab
.\.venv\Scripts\python.exe -X utf8 main.py --query-id Q2
```

Linux/macOS thay bằng `python3.11 -m venv .venv` và `.venv/bin/python`. Package nộp không mang theo runtime hoặc dependencies, cần cài requirements.

`main.py --query-id Q1` đến `Q5` dùng câu hỏi/filter chính thức. `main.py 'câu hỏi' --audience student` dùng câu hỏi tùy chọn. `main.py --sample` giữ demo mẫu cũ; không dùng demo mẫu để báo cáo kết quả nhóm.

## Artifacts

- `benchmark/queries.json`: 5 câu đúng nguyên văn log Hiệp, gold answers, markers, accepted docs và filters.
- `benchmark/PROTOCOL.md`: cách chấm, phạm vi nguồn và những yếu tố chưa kiểm soát khi so sánh Khang–Hiệp.
- `benchmark/predictions.json`: 5 giả thuyết similarity được lưu trước lượt tính.
- `benchmark/answer_review.json`: đánh giá định tính có hỗ trợ AI cho output local fixed-size 500/100; không phải điểm giảng viên. Nếu đổi backend/chunker/answers, phải đọc lại output và cập nhật review, không tự giữ điểm cũ.
- `report/artifacts/benchmark_results.json`: full chunks/top-3, scores, answers, coverage, ablation và input hashes.
- `report/artifacts/hiep_results.json`: 15 records import từ log Hiệp, có hash nguồn, chưa tái lập remote run.
- `report/artifacts/test_results.txt` và `.xml`: output kiểm thử thực chạy.
- `report/REPORT_CANHAN.md`, `REPORT_NHOM.md`, `DEMO.md`, `SUBMISSION_STATUS.md`: bài báo cáo, demo và checklist còn lại.
- `report/archive/local-v1/`, `benchmark/archive/queries-local-v1.json`: kết quả cũ trước khi đồng bộ queries, chỉ để truy vết.

Benchmark offline dùng TF-IDF + extractive output có citation; không đọc API keys, không gọi Gemini, không âm thầm fallback. Log Hiệp được giữ nguyên; không sửa corpus gốc. Parser metadata hỗ trợ schema phẳng với quoted string của dataset, không phải YAML parser tổng quát.

Đã có kết quả cả ba thành viên DKH: Khang fixed-size500/100, Hiệp heading, Dũng recursive. Q1/Q3/Q5 của Dũng khác cách diễn đạt; backend/matcher cũng khác. Đã ghi rõ trong báo cáo, không cam kết đã chạy chung bench.py/Gemini. Chưa thực hiện thuyết trình hoặc upload bài.

Log Dũng: report/ket_qua_benchmark.txt; bản import: report/artifacts/dung_results.json; đánh giá: report/KET_QUA_DUNG.md. Demo main.py mặc định dùng fixed_size500/100 của Khang; chọn --strategy heading để xem đối chứng. finalize kiểm tra/import cả hai log, chạy benchmark, cập nhật báo cáo rồi đóng ZIP.
