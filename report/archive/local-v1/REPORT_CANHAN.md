# Báo cáo cá nhân — Lab 7: Embedding & Vector Store

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

`SentenceChunker` dùng regex `(?<=[.!?])\s+`, giữ dấu câu, strip khoảng trắng và nhóm tối đa 3 câu. Hạn chế: dấu chấm trong viết tắt hoặc số thứ tự có thể bị xem là kết thúc câu.

`RecursiveChunker` thử `\n\n`, `\n`, `. `, khoảng trắng, rồi cắt ký tự. Chỉ đệ quy với phần vượt kích thước; giữ separator để không mất nội dung. Base case là đoạn không vượt giới hạn; hết separator thì fixed-size không overlap. Tests kiểm tra ghép chunks khôi phục nguyên văn.

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

Python **3.11.9**, pytest **9.1.1**. Bộ gốc: **42/42 pass**; bổ sung **21 tests** cho edge cases, atomicity, concurrency, pre-filter và ingestion/citations. Tổng **63/63 pass**. Kết quả máy đọc được: [test_results.xml](artifacts/test_results.xml).

```text
collected 63 items
63 passed
```

`.venv` cũ trỏ Python 3.10 đã mất. Đã dùng Python 3.11.9 portable tại `.runtime/python311`, giữ nguyên `.venv` và tái sử dụng các dependencies pure-Python đang có; không thay Python hệ thống. Chạy bằng `powershell -File scripts/run_lab.ps1 test`.

## 4. Dự đoán similarity

Giả thuyết được lưu trong [predictions.json](../benchmark/predictions.json) trước khi tính. “Cao/thấp” là dự đoán về nghĩa, không dùng ngưỡng tùy ý để chấm đúng/sai số học.

| # | Câu A | Câu B | Dự đoán trước chạy | TF-IDF | Mock |
| --- | --- | --- | --- | --- | --- |
| 1 | Sinh viên phải ghi nguồn khi sử dụng AI trong học thuật. | Sinh viên phải ghi nguồn khi sử dụng AI trong học thuật. | cao | 1.0000 | 1.0000 |
| 2 | Sinh viên phải ghi nguồn khi sử dụng AI trong học thuật. | Người học cần trích dẫn công cụ trí tuệ nhân tạo đã dùng. | cao | 0.0609 | 0.0345 |
| 3 | Use AI responsibly and cite generated content. | Use AI responsibly and verify generated content. | cao | 0.7050 | 0.0747 |
| 4 | Students must cite AI-generated content. | Sinh viên phải trích dẫn nội dung do AI tạo ra. | cao | 0.0374 | -0.0891 |
| 5 | Academic integrity requires honest citation. | The recipe uses rice and boiling water. | thấp | 0.0000 | 0.0406 |

Cặp 1 cao nhất (1.0) và cặp 5 thấp nhất (0.0) với TF-IDF, phù hợp dự đoán. Cặp 3 có nhiều từ chung nên tương đối cao. Cặp 2 và 4 gần nghĩa nhưng có điểm thấp: lexical representation bỏ lỡ paraphrase và dịch ngôn ngữ. Mock gần ngẫu nhiên với câu không giống hệt; không dùng mock score để diễn giải ngữ nghĩa.

## 5. Kết quả truy xuất cá nhân

Cùng 5 câu hỏi trong báo cáo nhóm, backend TF-IDF lexical, heading=800, top_k=3. **5/5 câu có gold span trong top-3**; MRR@3=1.000. Chi tiết toàn bộ top-3 của mọi chiến lược: [BENCHMARK_RESULTS.md](artifacts/BENCHMARK_RESULTS.md).

| Query | Top-1 chunk | Score | Top-1 đúng span? | Gold span trong agent output? |
| --- | --- | --- | --- | --- |
| Q1 | ueh-xu-ly-vi-pham-nguoi-hoc:heading:005 | 0.4540 | True | True |
| Q2 | ueh-dao-van-ai-quy-dinh-chung:heading:004 | 0.5786 | True | True |
| Q3 | rmit-ai-acknowledgement-guide:heading:002 | 0.3765 | True | True |
| Q4 | una-genai-policy-faculty:heading:014 | 0.5401 | True | True |
| Q5 | una-genai-policy-staff:heading:001 | 0.3714 | True | True |

### Q1: Tại UEH, sau khi chỉnh sửa nhưng vẫn vi phạm sử dụng AI trong học thuật thì xử lý thế nào?

**Gold:** Với người học, giảng viên phụ trách học phần lập biên bản, thông báo chuyển cho đơn vị quản lý để xử lý tùy theo mức độ vi phạm.

**Agent output thực tế:**

[EXTRACTIVE BASELINE — không phải LLM]

b) Nếu vẫn vi phạm sau khi đã chỉnh sửa, giảng viên phụ trách học phần lập biên bản, thông báo chuyển cho đơn vị quản lý để xử lý tùy theo mức độ vi phạm.
[ueh-xu-ly-vi-pham-nguoi-hoc:heading:005](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

b) Sau khi đã chỉnh sửa, người học nộp lại bài nhưng vẫn vi phạm lỗi đạo văn thì giảng viên phụ trách học phần lập biên bản/thông báo chuyển về đơn vị quản lý để xử lý tùy theo mức độ vi phạm quy định tại Phụ lục 3.
[ueh-xu-ly-vi-pham-nguoi-hoc:heading:002](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

Nếu phát hiện vi phạm sử dụng AI, tác giả chịu trách nhiệm theo các quy định của UEH và pháp luật hiện hành.
[ueh-xu-ly-vi-pham-nguoi-hoc:heading:004](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

### Q2: Theo UEH, tỷ lệ tương đồng học thuật có phải là căn cứ duy nhất để kết luận đạo văn không?

**Gold:** Không. Tỷ lệ tương đồng không phải căn cứ duy nhất; cần xem xét chuyên môn của đơn vị quản lý, giảng viên hoặc hội đồng có thẩm quyền.

**Agent output thực tế:**

[EXTRACTIVE BASELINE — không phải LLM]

Tỷ lệ tương đồng học thuật là tỷ lệ phần trăm nội dung trùng lặp trong sản phẩm học thuật được xác định bằng phần mềm hỗ trợ (Turnitin hoặc các công cụ kiểm tra đạo văn có chức năng so sánh với cơ sở dữ liệu học thuật rộng và cho phép phân tích chi tiết mức độ trùng lặp, được UEH phê duyệt sử dụng). Tỷ lệ tương đồng không phải là căn cứ duy nhất để kết luận đạo văn; việc đánh giá phải dựa trên xem xét chuyên môn của đơn vị quản lý, giảng viên hoặc hội đồng có thẩm quyền.
[ueh-dao-van-ai-quy-dinh-chung:heading:004](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

1. UEH sử dụng phần mềm Turnitin và/hoặc công cụ tương đương để phát hiện tỷ lệ tương đồng học thuật trong các sản phẩm học thuật. Kết quả tỷ lệ tương đồng chỉ mang tính tham khảo, hỗ trợ, không tự động kết luận là đạo văn. Việc kết luận dựa trên xem xét bối cảnh, phạm vi, tính chất nội dung trùng lặp, ý chí của người thực hiện và các chứng cứ liên quan. Việc đánh giá do giảng viên phụ trách/người hướng dẫn hoặc hội đồng/đơn vị có thẩm quyền thực hiện theo quy trình được UEH quy định.
[ueh-dao-van-ai-quy-dinh-chung:heading:008](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

e) Tạp chí JABES kiểm tra tỷ lệ tương đồng theo quy định trước khi gửi phản biện và trước khi xuất bản.
[ueh-dao-van-ai-quy-dinh-chung:heading:023](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

### Q3: According to RMIT Library, what records of AI prompts and outputs should students save?

**Gold:** Keep a record of prompts, generated outputs and how the content was used; save copies because an educator may request them.

**Agent output thực tế:**

[EXTRACTIVE BASELINE — không phải LLM]

Make sure you save a copy of the prompts used and outputs generated, as you may need to provide this to your educator on request.
[rmit-ai-acknowledgement-guide:heading:002](https://rmit.libguides.com/referencing_AI_tools/acknowledging)

For this type of AI use, however, you need to include an acknowledgement of what AI tools were used and how they were used within the body or methods section of your work.
[rmit-ai-acknowledgement-guide:heading:001](https://rmit.libguides.com/referencing_AI_tools/acknowledging)

Learn about academic integrity, what happens if you breach it and where to get help if you're unsure.
[rmit-vn-academic-integrity-ai:heading:000](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)

### Q4: At UNA, should faculty use AI-detection software as the single means of verifying originality?

**Gold:** No. Faculty should avoid using AI-detection software as the single means of verifying originality.

**Agent output thực tế:**

[EXTRACTIVE BASELINE — không phải LLM]

Avoid using AI-detection software as the single means of verifying originality.
[una-genai-policy-faculty:heading:014](https://www.una.edu/academics/generative-ai-policy.html)

Users should follow best practices for selecting and using AI tools and services, considering generative AI's potential risks and benefits. This includes being aware of the limitations of AI-generated content and verifying its accuracy before using it in academic or research contexts.
[una-genai-policy-faculty:heading:013](https://www.una.edu/academics/generative-ai-policy.html)

Faculty should explicitly define and explain the acceptable use of AI in the course syllabus, assignments, and rubrics/grading guides. Sample language will be provided in Simple Syllabus and can be customized. Faculty members who use AI to create lesson plans, assignments, rubrics, reading lists, and other class documents should acknowledge the use of AI to model academic integrity practices.
[una-genai-policy-faculty:heading:001](https://www.una.edu/academics/generative-ai-policy.html)

### Q5: At UNA, what information may staff not share with generative AI, and may they create AI-generated promotional images?

**Gold:** Staff must avoid sharing confidential information, including student data protected under FERPA. Creating AI-generated images for promotional materials is not allowed in the supplied policy.

**Agent output thực tế:**

[EXTRACTIVE BASELINE — không phải LLM]

UNA staff and faculty are permitted to use generative AI responsibly to assist in their work. However, users must exercise caution to avoid sharing confidential information, including student data protected under FERPA guidelines, when using AI tools. Additionally, the creation of AI-generated images for promotional materials is not allowed, as such content may conflict with UNA’s branding standards, copyright regulations, and institutional values. To ensure that all promotional materials remain on brand and in compliance with institutional and legal standards,
[una-genai-policy-staff:heading:001](https://www.una.edu/academics/generative-ai-policy.html)

Use generative AI to improve administrative processes and decision-making.
[una-genai-policy-staff:heading:000](https://www.una.edu/academics/generative-ai-policy.html)

Work with IT Services prior to the use of AI for administrative purposes to help ensure data security, data integrity, integration needs, and data confidentiality
[una-genai-policy-staff:heading:002](https://www.una.edu/academics/generative-ai-policy.html)

## Phân tích lỗi và giới hạn

**F1 — khác ngôn ngữ:** hỏi bằng tiếng Việt về hồ sơ prompt/output của RMIT nhưng bằng chứng là tiếng Anh. TF-IDF + heading không tìm thấy gold span trong top-3; agent trích nhầm tài liệu UEH. Root cause: TF-IDF so khớp từ vựng, không ánh xạ ngữ nghĩa Việt–Anh. Hướng cải thiện: thử multilingual embeddings, reranking và filter issuer; chỉ công bố mức cải thiện sau khi chạy lại.

**F2 — filter sai đối tượng:** dùng `audience=faculty` cho câu hỏi Q1 của sinh viên làm loại bỏ toàn bộ tài liệu đích; Hit@3 bằng 0. Root cause: pre-filter sai khiến retrieval không còn ứng viên đúng. Cần lấy audience từ ngữ cảnh người dùng có kiểm chứng và cho phép họ sửa; không tự đoán nhóm đối tượng từ một từ khóa.

**Chunking và đo lường:** gold-span matching yêu cầu nguyên vẹn một đoạn bằng chứng trong chunk đúng doc_id. Chunk cắt ngang span hoặc câu diễn đạt tương đương có thể bị chấm thiếu; vì vậy đã lưu nguyên top-3 để kiểm tra thủ công. `answer_contains_all_gold_spans` chỉ đo sự xuất hiện của chuỗi, không phải điểm chất lượng câu trả lời.

**Grounding:** extractive baseline chỉ trả đoạn nguồn kèm citation, có thể kèm đoạn không liên quan và không tổng hợp đầy đủ mọi ý. Q3 có bằng chứng lưu prompt/output nhưng phần trả lời chưa nhắc đầy đủ việc ghi cách sử dụng nội dung. Không quy đổi Hit@3=100% thành điểm agent 10/10. Prompt yêu cầu không trộn trường nhưng không bảo đảm ngăn lỗi; F1 chứng minh giới hạn đó.

**Giới hạn thực nghiệm:** chỉ 5 câu hỏi nội bộ, phần lớn cùng ngôn ngữ với tài liệu, có 4 câu dùng filter. Q1 được điều chỉnh sau pilot để minh họa sự nhập nhằng audience; không phải held-out benchmark. TF-IDF fit trên corpus nguồn trước chunking, không dùng gold answers để fit hoặc trả lời. Các chiến lược có cùng corpus/backend nhưng sentence chunking không có cùng giới hạn ký tự; chưa tách hoàn toàn ảnh hưởng thuật toán và kích thước.

**Nguồn và trùng lặp:** 10 file xuất phát từ 5 URL; UEH và UNA được tách theo audience. Một số đoạn UNA lặp ở general/faculty, có thể tạo kết quả gần trùng. Khi đánh giá ngoài bài lab, cần group theo URL khi chia tập và loại bản lặp, tránh data leakage.

**Mở rộng:** store hiện là in-memory, tìm kiếm O(N × D) và chọn top-k bằng heap O(N log k); TF-IDF trả vector dense nên không phù hợp corpus lớn. Bước tiếp theo là sparse vectors hoặc ANN, batch embeddings, persistence và đánh giá latency nhiều lượt. Những cải tiến này chưa được triển khai hay đo trong báo cáo.


## 6. Tự đánh giá theo rubric

Core code có bằng chứng 42/42 tests gốc pass. Warm-up, giải thích triển khai, similarity và 5 lượt retrieval đã có nội dung và artifact thực chạy. Điểm chất lượng agent cần người chấm đánh giá nội dung, không suy ra từ gold-span matching. Phần học hỏi trực tiếp từ thành viên khác/demo chưa diễn ra trong phiên này; bài học hiện có đến từ so sánh các chiến lược trên cùng máy.

## Phạm vi và tính minh bạch

Bài làm được hoàn thiện với hỗ trợ của Codex (OpenAI, 2026) cho triển khai code, thiết kế benchmark, chạy kiểm thử và soạn báo cáo. Corpus do nhóm cung cấp. Các dự đoán trong file predictions.json là giả thuyết thiết kế do AI hỗ trợ ghi trước lần tính similarity, không được trình bày như dự đoán cá nhân đã tự thực hiện.

Các bảng benchmark local được chạy tập trung trên máy của Nguyễn Thế Khang. Đã nhận thêm log benchmark của Đặng Quốc Hiệp, phân tích riêng trong [KET_QUA_HIEP.md](KET_QUA_HIEP.md); số liệu này do thành viên cung cấp và chưa tái lập tại đây. Chưa có kết quả của Nguyễn Việt Dũng hoặc bằng chứng thuyết trình; phần phân công vẫn là đề xuất. Người nộp cần đọc, hiểu, kiểm tra nội dung và khai báo hỗ trợ AI theo yêu cầu môn học.

Kết quả chỉ áp dụng cho snapshot dataset được cung cấp, không xác nhận hiệu lực pháp lý hoặc tính cập nhật của các quy định trên website hiện tại. Các tài liệu khác trường/quốc gia không được suy rộng thành một chính sách chung.
