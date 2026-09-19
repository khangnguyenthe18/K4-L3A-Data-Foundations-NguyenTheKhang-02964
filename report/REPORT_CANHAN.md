# Báo cáo cá nhân — Lab 7

**Họ tên:** Nguyễn Thế Khang

**MSSV:** 2A202602964 — **Nhóm:** DKH — **Vai trò:** R1 · Data

**Chủ đề:** Quy định sử dụng AI và liêm chính học thuật trong giáo dục đại học

**Thành viên:** Nguyễn Thế Khang, Đặng Quốc Hiệp, Nguyễn Việt Dũng

**Phiên bản bài nộp:** group-dkh-v3; ngày 19/09/2026

## 1. Khởi động

Cosine similarity: đo độ tương đồng về hướng của hai vector. Với embeddings có chất lượng, hai câu gần nghĩa thường có cosine cao. Cặp gần nghĩa: “Sinh viên phải ghi nguồn khi sử dụng AI trong học thuật” / “Người học cần trích dẫn công cụ trí tuệ nhân tạo đã dùng”. Cặp khác nghĩa: “Academic integrity requires honest citation” / “The recipe uses rice and boiling water”.

Cosine bỏ qua độ lớn vector. Với vector chuẩn hóa L2, cosine và Euclidean distance cho cùng thứ tự xếp hạng; score cao không xác nhận hai câu có cùng tính đúng/sai.

10.000 ký tự, size=500, overlap=50: `ceil((10000-50)/(500-50)) = 23 chunks`. Khi overlap=100: `ceil(9900/400) = 25 chunks`. Overlap giữ ngữ cảnh qua ranh giới nhưng tăng dữ liệu trùng và chi phí embedding.

## 2. Hướng tiếp cận

- `SentenceChunker`: regex `(?<=[.!?])\s+`, giữ dấu câu, strip và nhóm tối đa 3 câu; viết tắt/số thứ tự có thể gây tách sai.
- `RecursiveChunker`: thử đoạn, dòng, câu, từ, ký tự; giữ separators; đệ quy chỉ với phần quá dài; khi hết separators thì cắt theo size. Tests kiểm tra không mất văn bản và không vượt giới hạn.
- `compute_similarity`: kiểm tra chiều và số hữu hạn, xử lý zero vector, chia từng phần tử theo norm trước dot để tránh overflow thông thường. Comparator trả count/avg_length/chunks cho cả text rỗng.
- `HeadingChunker(800)`: giữ ancestry của tiêu đề trong từng đoạn con, dành tối đa khoảng 1/3 ngân sách cho heading và recursive split phần thân. Đây là đối chứng; strategy cá nhân theo phân công DKH là FixedSizeChunker(500, 100).
- `EmbeddingStore`: in-memory theo lựa chọn của đề, ID record riêng để cho phép thêm trùng doc_id; metadata copy sâu. Embed một lần mỗi document lúc add và một lần mỗi query lúc search; dot product trên L2 vectors bằng cosine. Filter AND trước top-k; delete mọi chunk theo doc_id.
- Error handling/concurrency: vector cùng chiều và hữu hạn, k không dương/query rỗng trả []; batch embed xong mới commit dưới RLock, search snapshot; lỗi backend không âm thầm fallback.
- `KnowledgeBaseAgent`: dependency injection store/llm_fn, pre-filter, giới hạn context, JSON evidence có citation. Không có kết quả thì thông báo thiếu evidence. Backend thực chạy là extractive, trả đủ chunk để không rơi mất ngoại lệ/định lượng.
- Ingestion: tách metadata khỏi text embedding, kiểm tra URL/ngày/audience/ID, giữ nguồn/phiên bản và thêm chunk_index/chunk_id/strategy. Front matter parser hỗ trợ schema phẳng với chuỗi quoted của dataset, không phải toàn bộ YAML.

## 3. Kiểm thử

Python **3.11.9**. **71/71 tests pass**, trong đó có **42 tests gốc**; còn lại là edge cases, concurrency, ingestion, benchmark alignment, import log và evidence coverage. [JUnit](artifacts/test_results.xml) và [console log](artifacts/test_results.txt).

`.venv` cũ trỏ interpreter đã mất; máy hiện tại dùng Python 3.11.9 portable trong `.runtime/python311`. Chạy `powershell -File scripts/run_lab.ps1 test`. Không sửa interpreter của hệ thống.

## 4. Dự đoán similarity

Giả thuyết lưu trước lượt tính trong [predictions.json](../benchmark/predictions.json). Cao/thấp là dự đoán theo nghĩa, không phải ngưỡng chấm số học.

| # | Câu A | Câu B | Dự đoán trước chạy | TF-IDF | Mock |
| --- | --- | --- | --- | --- | --- |
| 1 | Sinh viên phải ghi nguồn khi sử dụng AI trong học thuật. | Sinh viên phải ghi nguồn khi sử dụng AI trong học thuật. | cao | 1.0000 | 1.0000 |
| 2 | Sinh viên phải ghi nguồn khi sử dụng AI trong học thuật. | Người học cần trích dẫn công cụ trí tuệ nhân tạo đã dùng. | cao | 0.0609 | 0.0345 |
| 3 | Use AI responsibly and cite generated content. | Use AI responsibly and verify generated content. | cao | 0.7050 | 0.0747 |
| 4 | Students must cite AI-generated content. | Sinh viên phải trích dẫn nội dung do AI tạo ra. | cao | 0.0374 | -0.0891 |
| 5 | Academic integrity requires honest citation. | The recipe uses rice and boiling water. | thấp | 0.0000 | 0.0406 |

Cặp 1 cao nhất (1.0), cặp 5 thấp nhất (0.0) theo TF-IDF, phù hợp dự đoán; cặp 3 nhiều từ chung có điểm tương đối cao. Cặp 2 paraphrase và cặp 4 khác ngôn ngữ gần nghĩa nhưng điểm thấp, thể hiện giới hạn lexical representation. Mock không dùng để suy luận ý nghĩa.

## 5. Kết quả cùng bộ câu hỏi nhóm

Đã chạy đúng nguyên văn **5 câu Hiệp gửi**, cùng filters và markers: [queries.json](../benchmark/queries.json). Chọn TF-IDF + fixed-size 500/overlap100, top_k=3. **2/5 Hit@3**, MRR@3 **0.400**. Đây là kết quả group-dkh-v3; không dùng kết quả 5/5 của bộ câu hỏi local-v1.

| Query | Top-1 chunk | Score | Evidence rank | Coverage | Answer chứa markers? |
| --- | --- | --- | --- | --- | --- |
| Q1 | ueh-dao-van-ai-quy-dinh-chung:fixed_size:003 | 0.4561 | None | 0% | False |
| Q2 | ueh-xu-ly-vi-pham-nguoi-hoc:fixed_size:002 | 0.4009 | 1 | 100% | True |
| Q3 | ueh-dao-van-ai-quy-dinh-chung:fixed_size:014 | 0.2160 | None | 0% | False |
| Q4 | ueh-dao-van-ai-quy-dinh-chung:fixed_size:011 | 0.2731 | None | 0% | False |
| Q5 | tt49-2026-ung-dung-cong-nghe-ai:fixed_size:029 | 0.3587 | 1 | 100% | True |

### Đánh giá câu trả lời theo rubric (tham khảo)

| Query | Điểm tham khảo /2 | Căn cứ |
| --- | --- | --- |
| Q1 | 0 | Top-3 đúng tài liệu UEH nhưng không có ngưỡng cần hỏi; extractive output không đáp ứng câu hỏi định lượng. |
| Q2 | 2 | Rank 1 chứa xử lý bài tập của người học: lập biên bản/thông báo đơn vị quản lý theo Phụ lục 3; extractive output giữ nguyên đoạn và citation. Có thêm context không cần thiết nhưng ý chính đầy đủ. |
| Q3 | 0 | Không lấy được bằng chứng RMIT trong top-3; output chủ yếu UEH, không chứng minh đủ cách dùng, creator và năm theo gold RMIT. |
| Q4 | 0 | Không lấy được tài liệu UNA/gold marker trong top-3. Nội dung UEH có chủ đề liên quan nhưng không đáp ứng phạm vi nguồn UNA của gold. |
| Q5 | 2 | Rank 1 có ngày hiệu lực và hai số thông tư; rank 2 bổ sung phần cuối về hết hiệu lực. Hợp context/answer đủ ý và citations theo snapshot; không xác minh pháp lý hiện hành. |

Tổng tham khảo **4/10** cho cấu hình cá nhân, do AI hỗ trợ đối chiếu output với gold/rubric; không phải điểm giảng viên. Q3/Q4 cần cải thiện retrieval. Extractive output dài hơn câu trả lời tự nhiên nhưng cho phép kiểm tra nguồn.

### Q1: Theo quy định của UEH, tỷ lệ tương đồng từ bao nhiêu phần trăm thì sản phẩm học thuật bị xem là có dấu hiệu đạo văn?

**Gold:** Theo snapshot UEH, tỷ lệ tương đồng từ 20% trở lên là một dấu hiệu định lượng, sau khi loại các phần được miễn trừ nêu trong quy định; không tự động kết luận đạo văn chỉ từ tỷ lệ này.

| Rank | Chunk ID | Score | Chứa primary marker? |
| --- | --- | --- | --- |
| 1 | ueh-dao-van-ai-quy-dinh-chung:fixed_size:003 | 0.4561 | False |
| 2 | ueh-dao-van-ai-quy-dinh-chung:fixed_size:004 | 0.4402 | False |
| 3 | ueh-dao-van-ai-quy-dinh-chung:fixed_size:009 | 0.4165 | False |

**Agent output thực tế (trích nguyên chunks, không phải LLM):**

> [EXTRACTIVE BASELINE — không phải LLM]
>
> ảnh, mô hình, sản phẩm học thuật của người khác mà không ghi nhận, trích dẫn hoặc chú thích phù hợp; hoặc tái sử dụng sản phẩm học thuật của chính mình (tự đạo văn) mà không nêu rõ nguồn gốc và tình trạng công bố.
>
> ### Tỷ lệ tương đồng học thuật
>
> Tỷ lệ tương đồng học thuật là tỷ lệ phần trăm nội dung trùng lặp trong sản phẩm học thuật được xác định bằng phần mềm hỗ trợ (Turnitin hoặc các công cụ kiểm tra đạo văn có chức năng so sánh với cơ sở dữ liệu học thuật rộng và cho phép phân tích chi tiế
> [ueh-dao-van-ai-quy-dinh-chung:fixed_size:003](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
>
> kiểm tra đạo văn có chức năng so sánh với cơ sở dữ liệu học thuật rộng và cho phép phân tích chi tiết mức độ trùng lặp, được UEH phê duyệt sử dụng). Tỷ lệ tương đồng không phải là căn cứ duy nhất để kết luận đạo văn; việc đánh giá phải dựa trên xem xét chuyên môn của đơn vị quản lý, giảng viên hoặc hội đồng có thẩm quyền.
>
> ### Các dấu hiệu của hành vi đạo văn hoặc vi phạm liêm chính học thuật
>
> Sản phẩm học thuật có thể xem là có dấu hiệu vi phạm nếu có ít nhất một trong các biểu hiện sau:
>
> a) Dấ
> [ueh-dao-van-ai-quy-dinh-chung:fixed_size:004](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
>
> ng cụ tương đương để phát hiện tỷ lệ tương đồng học thuật trong các sản phẩm học thuật. Kết quả tỷ lệ tương đồng chỉ mang tính tham khảo, hỗ trợ, không tự động kết luận là đạo văn. Việc kết luận dựa trên xem xét bối cảnh, phạm vi, tính chất nội dung trùng lặp, ý chí của người thực hiện và các chứng cứ liên quan. Việc đánh giá do giảng viên phụ trách/người hướng dẫn hoặc hội đồng/đơn vị có thẩm quyền thực hiện theo quy trình được UEH quy định.
>
> 2. Xử lý hành vi đạo văn
>
> ### 2.1 Nguyên tắc xử lý h
> [ueh-dao-van-ai-quy-dinh-chung:fixed_size:009](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

### Q2: Sản phẩm học thuật đã chỉnh sửa nhưng vẫn vi phạm lỗi đạo văn thì xử lý ra sao?

**Gold:** Trong bối cảnh bài tập học phần của người học: giảng viên phụ trách lập biên bản/thông báo chuyển về đơn vị quản lý để xử lý tùy mức độ vi phạm quy định tại Phụ lục 3.

| Rank | Chunk ID | Score | Chứa primary marker? |
| --- | --- | --- | --- |
| 1 | ueh-xu-ly-vi-pham-nguoi-hoc:fixed_size:002 | 0.4009 | True |
| 2 | ueh-xu-ly-vi-pham-nguoi-hoc:fixed_size:005 | 0.3325 | True |
| 3 | ueh-xu-ly-vi-pham-nguoi-hoc:fixed_size:000 | 0.2734 | False |

**Agent output thực tế (trích nguyên chunks, không phải LLM):**

> [EXTRACTIVE BASELINE — không phải LLM]
>
> nhiệm theo các quy định của UEH và pháp luật hiện hành.
>
> ### 2.3 Đối với các bài kiểm tra, bài tập, tiểu luận và các bài khác thuộc các học phần
>
> a) Khi bị phát hiện vi phạm lần đầu, người học phải chỉnh sửa và nộp lại bài theo yêu cầu của giảng viên;
>
> b) Sau khi đã chỉnh sửa, người học nộp lại bài nhưng vẫn vi phạm lỗi đạo văn thì giảng viên phụ trách học phần lập biên bản/thông báo chuyển về đơn vị quản lý để xử lý tùy theo mức độ vi phạm quy định tại Phụ lục 3.
>
> ## Điều 5. Xử lý vi phạm sử d
> [ueh-xu-ly-vi-pham-nguoi-hoc:fixed_size:002](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
>
> ật hiện hành.
>
> ### 2.2. Đối với các bài kiểm tra, bài tập, tiểu luận, đồ án, dự án và các bài khác thuộc học phần
>
> a) Khi bị phát hiện vi phạm lần đầu, người học phải chỉnh sửa và nộp lại bài theo yêu cầu của giảng viên;
>
> b) Nếu vẫn vi phạm sau khi đã chỉnh sửa, giảng viên phụ trách học phần lập biên bản, thông báo chuyển cho đơn vị quản lý để xử lý tùy theo mức độ vi phạm.
>
> ## Điều 6. Tổ chức thực hiện — trách nhiệm của người học
>
> ### Trách nhiệm của tác giả sản phẩm học thuật và người học tại
> [ueh-xu-ly-vi-pham-nguoi-hoc:fixed_size:005](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
>
> # UEH — Xử lý vi phạm đạo văn và sử dụng AI đối với người học
>
> (Kèm theo Quyết định số: 4002/QĐ-ĐHKT-NCPTGKTC, ngày 18 tháng 12 năm 2025 của Giám đốc Đại học Kinh tế Thành phố Hồ Chí Minh)
>
> ## Điều 3. Xử lý hành vi đạo văn — áp dụng cho người học
>
> ### 2.2 Đối với khóa luận, đề án tốt nghiệp, luận văn, luận án
>
> a) Trước khi bảo vệ:
>
> Khi phát hiện có dấu hiệu đạo văn, người học phải chỉnh sửa, bổ sung và khắc phục theo yêu cầu của giảng viên hướng dẫn hoặc đơn vị quản lý.
>
> b) Trong khi bảo vệ:
>
> Nế
> [ueh-xu-ly-vi-pham-nguoi-hoc:fixed_size:000](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

### Q3: Khi ghi nhận việc dùng công cụ AI trong bài làm, câu acknowledgement cần nêu những thông tin gì?

**Gold:** Theo hướng dẫn RMIT Library: nêu cách sử dụng AI, tên công cụ và nhà phát triển, năm nội dung AI được người dùng tạo ra. Không bắt buộc phiên bản/ngày dùng trừ khi giảng viên yêu cầu.

| Rank | Chunk ID | Score | Chứa primary marker? |
| --- | --- | --- | --- |
| 1 | ueh-dao-van-ai-quy-dinh-chung:fixed_size:014 | 0.2160 | False |
| 2 | ueh-dao-van-ai-quy-dinh-chung:fixed_size:017 | 0.1707 | False |
| 3 | ueh-dao-van-ai-quy-dinh-chung:fixed_size:020 | 0.1629 | False |

**Agent output thực tế (trích nguyên chunks, không phải LLM):**

> [EXTRACTIVE BASELINE — không phải LLM]
>
> ạt động học thuật tại UEH được sử dụng AI để hỗ trợ hoạt động nghiên cứu và học tập tại UEH trên cơ sở tuân thủ các nguyên tắc sau:
>
> - Minh bạch: ghi rõ công cụ AI tạo sinh đã sử dụng, mục đích sử dụng (tóm tắt, dịch thuật, tạo hình, viết mã v.v.) và những nội dung có sự hỗ trợ của AI tạo sinh trong sản phẩm học thuật. Việc khai báo cần thực hiện theo chuẩn, ví dụ: Trong phần Acknowledgement hoặc Phương pháp nghiên cứu ghi: “Một phần nội dung của sản phẩm này được hỗ trợ bởi ChatGPT (phiên bản …
> [ueh-dao-van-ai-quy-dinh-chung:fixed_size:014](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
>
> , không bắt buộc thông báo nếu chỉ sử dụng để kiểm tra ngôn ngữ, chỉnh lỗi chính tả, ngữ pháp hoặc dịch thuật trực tiếp không mang tính sáng tạo nội dung.
> 3. Những hành vi bị xem là vi phạm quy tắc sử dụng AI trong học thuật:
>
> a) Sử dụng nội dung do AI tạo ra nhưng không thông báo hoặc thông báo không đầy đủ việc sử dụng công cụ, phạm vi và vai trò của AI.
>
> b) Sử dụng AI để tạo ra nội dung nhưng không kiểm tra, xác nhận nguồn hoặc độ chính xác.
>
> c) Sử dụng AI để tạo ra toàn bộ hoặc phần lớn nội
> [ueh-dao-van-ai-quy-dinh-chung:fixed_size:017](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
>
> huật
>
> 1. Việc phát hiện và đánh giá vi phạm sử dụng AI trong học thuật do giảng viên phụ trách/người hướng dẫn hoặc hội đồng/đơn vị có thẩm quyền thực hiện, trên cơ sở xem xét các yếu tố: mức độ sử dụng AI, vai trò của AI trong sản phẩm, hành vi thông báo sử dụng hoặc không thông báo, dấu hiệu gian lận hoặc thay thế nhiệm vụ học thuật. UEH không sử dụng kết quả của các công cụ phát hiện nội dụng do AI tạo ra làm căn cứ duy nhất để kết luận vi phạm học thuật. Đánh giá vi phạm sử dụng AI được thực
> [ueh-dao-van-ai-quy-dinh-chung:fixed_size:020](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

### Q4: Những loại thông tin nào không được phép nhập vào công cụ AI tạo sinh?

**Gold:** Theo snapshot UNA, không nhập thông tin cá nhân, bí mật, độc quyền hoặc nhạy cảm: ví dụ hồ sơ sinh viên/tuyển sinh, số an sinh xã hội, dữ liệu thẻ/ngân hàng, giấy tờ định danh, dữ liệu y tế/bảo hiểm, dữ liệu người tham gia nghiên cứu chưa được đồng ý công khai, hồ sơ nội bộ và nội dung thuộc NDA/sở hữu trí tuệ chưa được phép. Danh sách ví dụ không giới hạn ở một loại dữ liệu.

| Rank | Chunk ID | Score | Chứa primary marker? |
| --- | --- | --- | --- |
| 1 | ueh-dao-van-ai-quy-dinh-chung:fixed_size:011 | 0.2731 | False |
| 2 | ueh-dao-van-ai-quy-dinh-chung:fixed_size:016 | 0.2475 | False |
| 3 | ueh-dao-van-ai-quy-dinh-chung:fixed_size:017 | 0.2366 | False |

**Agent output thực tế (trích nguyên chunks, không phải LLM):**

> [EXTRACTIVE BASELINE — không phải LLM]
>
> lỗi kỹ thuật hoặc sơ suất trong ghi nguồn, trích dẫn không đầy đủ, có thể được xem xét yêu cầu chỉnh sửa mà không xử phạt nếu không có dấu hiệu gian lận.
>
> ## Điều 4. Sử dụng AI trong học thuật
>
> 1. Trong Quy định này, trí tuệ nhân tạo (AI) được hiểu là các công cụ, hệ thống hoặc thuật toán có khả năng tạo, phân tích hoặc xử lý nội dung hỗ trợ hoạt động học thuật. AI được xem là công cụ hỗ trợ, không thay thế trách nhiệm tư duy, phân tích và sáng tạo của tác giả. AI trong học thuật được phân loại
> [ueh-dao-van-ai-quy-dinh-chung:fixed_size:011](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
>
> cấp cho AI dữ liệu cá nhân, dữ liệu mật, thông tin chưa công bố hoặc dữ liệu nghiên cứu nội bộ của UEH hoặc đối tác nếu chưa được phép.
> - Không lạm dụng: không sử dụng AI để thay thế nhiệm vụ học thuật mà người học hoặc giảng viên phải tự thực hiện. AI chỉ đóng vai trò hỗ trợ. Khuyến khích người học và giảng viên sử dụng có trách nhiệm và không phụ thuộc hoàn toàn vào công cụ.
> - Đối với AI hỗ trợ, không bắt buộc thông báo nếu chỉ sử dụng để kiểm tra ngôn ngữ, chỉnh lỗi chính tả, ngữ pháp hoặc d
> [ueh-dao-van-ai-quy-dinh-chung:fixed_size:016](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
>
> , không bắt buộc thông báo nếu chỉ sử dụng để kiểm tra ngôn ngữ, chỉnh lỗi chính tả, ngữ pháp hoặc dịch thuật trực tiếp không mang tính sáng tạo nội dung.
> 3. Những hành vi bị xem là vi phạm quy tắc sử dụng AI trong học thuật:
>
> a) Sử dụng nội dung do AI tạo ra nhưng không thông báo hoặc thông báo không đầy đủ việc sử dụng công cụ, phạm vi và vai trò của AI.
>
> b) Sử dụng AI để tạo ra nội dung nhưng không kiểm tra, xác nhận nguồn hoặc độ chính xác.
>
> c) Sử dụng AI để tạo ra toàn bộ hoặc phần lớn nội
> [ueh-dao-van-ai-quy-dinh-chung:fixed_size:017](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

### Q5: Thông tư 49/2026/TT-BGDĐT có hiệu lực từ ngày nào và thay thế những thông tư nào?

**Gold:** Theo Điều 22 trong snapshot nhóm cung cấp: hiệu lực từ 15/08/2026; Thông tư 15/2018/TT-BGDĐT và 30/2023/TT-BGDĐT hết hiệu lực từ ngày đó. Đây là gold answer kiểm thử snapshot, chưa xác minh tình trạng pháp lý hiện hành.

| Rank | Chunk ID | Score | Chứa primary marker? |
| --- | --- | --- | --- |
| 1 | tt49-2026-ung-dung-cong-nghe-ai:fixed_size:029 | 0.3587 | True |
| 2 | tt49-2026-ung-dung-cong-nghe-ai:fixed_size:030 | 0.3111 | False |
| 3 | tt49-2026-ung-dung-cong-nghe-ai:fixed_size:000 | 0.3103 | False |

**Agent output thực tế (trích nguyên chunks, không phải LLM):**

> [EXTRACTIVE BASELINE — không phải LLM]
>
> học thuật; trung thực trong học tập, giảng dạy, nghiên cứu khoa học và công bố việc sử dụng công nghệ, trí tuệ nhân tạo khi có yêu cầu.
>
> ## Điều 22. Điều khoản thi hành
>
> 1. Thông tư này có hiệu lực thi hành kể từ ngày 15 tháng 08 năm 2026.
>
> 2. Thông tư số 15/2018/TT-BGDĐT ngày 27 tháng 7 năm 2018 của Bộ trưởng Bộ Giáo dục và Đào tạo quy định tổ chức hoạt động, sử dụng thư điện tử và trang thông tin điện tử của các cơ sở giáo dục đại học, các trường cao đẳng sư phạm; Thông tư số 30/2023/TT-BGDĐT
> [tt49-2026-ung-dung-cong-nghe-ai:fixed_size:029](https://luatvietnam.vn/giao-duc/thong-tu-49-2026-tt-bgddt-ung-dung-cong-nghe-trong-giao-duc-dai-hoc-va-nghe-nghiep-439350-d1.html)
>
> n điện tử của các cơ sở giáo dục đại học, các trường cao đẳng sư phạm; Thông tư số 30/2023/TT-BGDĐT ngày 29 tháng 12 năm 2023 của Bộ trưởng Bộ Giáo dục và Đào tạo quy định về ứng dụng công nghệ thông tin trong đào tạo trực tuyến đối với giáo dục đại học hết hiệu lực thi hành từ ngày Thông tư này có hiệu lực.
>
> 3. Chánh Văn phòng, Cục trưởng Cục Khoa học, Công nghệ và Thông tin, Thủ trưởng các đơn vị thuộc Bộ Giáo dục và Đào tạo, Giám đốc các đại học, học viện, Hiệu trưởng các trường đại học, Hiệu
> [tt49-2026-ung-dung-cong-nghe-ai:fixed_size:030](https://luatvietnam.vn/giao-duc/thong-tu-49-2026-tt-bgddt-ung-dung-cong-nghe-trong-giao-duc-dai-hoc-va-nghe-nghiep-439350-d1.html)
>
> # Thông tư 49/2026/TT-BGDĐT — Ứng dụng công nghệ và AI trong giáo dục đại học
>
> Số: 49/2026/TT-BGDĐT — Hà Nội, ngày 30 tháng 06 năm 2026.
>
> Quy định ứng dụng công nghệ trong giáo dục đại học, giáo dục nghề nghiệp (trích các Điều liên quan đến trí tuệ nhân tạo và liêm chính học thuật).
>
> ## Điều 1. Phạm vi điều chỉnh
>
> Thông tư này quy định về ứng dụng công nghệ trong giáo dục đại học, giáo dục nghề nghiệp bao gồm: nguyên tắc, nội dung và điều kiện bảo đảm việc ứng dụng công nghệ số, trí tuệ nhân tạo
> [tt49-2026-ung-dung-cong-nghe-ai:fixed_size:000](https://luatvietnam.vn/giao-duc/thong-tu-49-2026-tt-bgddt-ung-dung-cong-nghe-trong-giao-duc-dai-hoc-va-nghe-nghiep-439350-d1.html)

## Phân tích lỗi và bài học

**Q3/Q4 — khác ngôn ngữ và nguồn:** query tiếng Việt, evidence đích tiếng Anh tại RMIT/UNA; lexical retrieval ưu tiên UEH và thiếu gold markers trong top-3. Root cause: TF-IDF không ánh xạ ngữ nghĩa Việt–Anh, còn query gốc không nêu issuer. Hướng cải thiện là multilingual embedding + làm rõ trường/nguồn; chưa đo mức cải thiện bằng cách đổi backend local.

**F2 — filter sai:** ép audience=faculty cho Q2 loại mọi tài liệu đích student, Hit@3=0. Filter phải lấy từ ngữ cảnh người hỏi. Exact student filter cũng loại audience=all; production phải xác định rõ có cho phép all hay không.

**Trích xuất mất ý:** phiên bản trước chỉ chọn một paragraph, có thể bỏ mất mục danh sách chứa con số dù retrieval có bằng chứng. Đã sửa extractive backend trả nguyên chunk trong context có giới hạn; test kiểm tra giữ cả con số lẫn phủ định. Vẫn có context thừa và không phải câu trả lời tổng hợp của LLM.

**Đúng tài liệu chưa đủ:** log Hiệp có doc_id score 10/10 cho mọi strategy nhưng evidence chỉ 5/10, 2/10, 6/10. Ví dụ Q1 fixed/recursive không có đoạn ngưỡng dù đúng file. Literal matcher cũng có thể chấm thiếu mẫu tương đương ở Q3 hoặc câu trả lời theo nhóm dữ liệu ở Q4; cần đọc đầy đủ output.

**Trade-off:** heading giữ Điều/Mục và ancestry để dễ kiểm tra phạm vi; số record tăng do prefix lặp. In-memory dense search O(N×D), heap top-k O(N log k), phù hợp lab nhỏ; corpus lớn cần sparse/ANN, batching và persistence. Các cải tiến đó chưa được đo ở đây.


## 6. Học từ kết quả thành viên và tự đánh giá

Từ log Hiệp: evidence scoring phân biệt đúng file với đúng nội dung; Gemini có thể truy xuất RMIT tiếng Anh từ query tiếng Việt nhưng vẫn thiếu chi tiết ở một số chunks. So sánh này gợi ý cần cải thiện cả embedding lẫn cấu trúc đoạn, không chỉ thay size. Đây là nhận xét từ artifact Hiệp gửi, không ghi là trải nghiệm thuyết trình đã diễn ra.

Đã có đủ code/tests, warm-up, giải thích triển khai, 5 similarity pairs, 5 kết quả theo bộ câu hỏi chung và failure analysis cho hồ sơ cá nhân. Đánh giá retrieval còn lỗi đã công khai; hoàn thành bài không đồng nghĩa đạt điểm tối đa.

## Giới hạn và khai báo hỗ trợ

Codex (OpenAI, 2026) hỗ trợ triển khai, chạy tests/benchmark và soạn báo cáo. Corpus và log Hiệp do người dùng cung cấp. Dự đoán similarity là giả thuyết thiết kế có hỗ trợ AI, đã lưu trước lượt tính; không mô tả như dự đoán tự làm của sinh viên. Người nộp cần hiểu, kiểm tra và khai báo hỗ trợ theo yêu cầu môn học.

Local dùng TF-IDF lexical + extractive evidence output, không dùng LLM hay API key. Log Hiệp khai báo Gemini embedding cached + Gemini Flash; được import, chưa chạy tái lập. Đã nhận log Dũng: OpenAI embeddings + GPT-4.1-mini, recursive; Q1/Q3/Q5 khác cách diễn đạt so với Hiệp. Xem [KET_QUA_DUNG.md](KET_QUA_DUNG.md). Buổi demo/thuyết trình chưa diễn ra trong phiên này.

Các gold answers là kiểm thử snapshot tài liệu đã có, không xác nhận chính sách/hiệu lực pháp lý hiện hành. Có 10 file nhưng chỉ 5 URL; một số đoạn UNA lặp giữa general/faculty. Khi chia train/test cần group theo nguồn. Năm queries là bộ đánh giá nội bộ, không phải held-out test; Q3/Q4 thiếu issuer trong câu hỏi nguyên văn nên có độ mơ hồ ngoài ngữ cảnh gold.

Không suy ra chất lượng câu trả lời chỉ từ marker hay doc_id. Các số liệu local-v1 (bộ cũ đạt 5/5) chỉ còn trong archive; bài nộp dùng group-dkh-v3.
