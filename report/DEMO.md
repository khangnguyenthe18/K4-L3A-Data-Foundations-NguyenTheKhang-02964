# Demo — Liêm chính khoa học / group-dkh-v3

Thành viên: Nguyễn Thế Khang, Đặng Quốc Hiệp, Nguyễn Việt Dũng. Đã có code/kết quả Khang và log Hiệp/Dũng; nhóm DKH. Đây là kịch bản chuẩn bị, không ghi nhận đã thuyết trình.

## 1. Corpus và core (1 phút)

10 tài liệu logic, 5 URL; tiếng Việt/Anh; giữ audience, source_url, retrieved_at, document_version. Giới thiệu source → chunk → embedding → filter → search → answer có citation.

```powershell
powershell -File scripts/run_lab.ps1 test
```

Mở log/XML để xem số tests thực tế. Giải thích atomic add, filter trước top-k, delete toàn bộ chunks theo doc_id và context limit.

## 2. Benchmark chung (1 phút)

```powershell
powershell -File scripts/run_lab.ps1 benchmark
```

Mở `benchmark/queries.json` và `report/REPORT_NHOM.md`. Cùng 5 câu và filters với Hiệp; local dùng TF-IDF/extractive, Hiệp dùng Gemini/Flash. Khang fixed-size500/100: 2/5 Hit@3, MRR@3=0.400. Hiệp heading theo log: 4/5 Hit@3, MRR@3≈0.567. Dũng recursive theo log: 1/5 Hit@3, MRR@3=0.200. Không kết luận chênh lệch chỉ do chunking; model, cách diễn đạt Q1/Q3/Q5, scoring và implementation khác nhau.

## 3. Metadata Q2 (1 phút)

```powershell
$labPython = '.\.runtime\python311\python.exe'
& $labPython -X utf8 main.py --query-id Q2
& $labPython -X utf8 main.py 'Sản phẩm học thuật đã chỉnh sửa nhưng vẫn vi phạm lỗi đạo văn thì xử lý ra sao?'
```

Lệnh query-id dùng filter student chính thức. Lệnh truyền text không tự filter. Local fixed-size vẫn đúng top-1 nhưng không filter lẫn faculty trong top-3; không tuyên bố MRR tăng. Log Hiệp thể hiện việc chuyển evidence lên top-1 ở recursive/heading khi dùng student filter.

## 4. Failure và grounding (1 phút)

```powershell
& $labPython -X utf8 main.py --query-id Q3
& $labPython -X utf8 main.py --query-id Q2 --audience faculty
```

Q3: lexical retrieval dễ lấy UEH tiếng Việt thay vì RMIT tiếng Anh. Filter faculty sai ở Q2 loại tài liệu người học. Nêu nhu cầu làm rõ issuer, thử multilingual embeddings và human evaluation.

## 5. Kết luận thảo luận (30 giây)

Đúng doc_id chưa chắc đúng evidence; marker đơn lẻ chưa chứng minh trả lời đầy đủ. Trả nguyên chunk giúp giữ ngoại lệ và số liệu nhưng có context thừa. Các thành viên cần hiểu code và kết quả mình trình bày; trình bày log Dũng và phân biệt lỗi retrieval với lỗi suy diễn của LLM tại Q1/Q5. Không lấy số liệu một backend gán cho backend khác.
