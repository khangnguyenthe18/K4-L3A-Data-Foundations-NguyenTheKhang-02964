# Kết quả benchmark thực chạy

Python 3.11.9; tfidf-word-unigram-l2 (lexical, offline).

Agent là extractive baseline, không phải LLM. Không tự quy đổi thành điểm rubric.
Bộ group-dkh-v3: giữ 5 câu/filters/markers của Hiệp; Khang dùng fixed-size 500/100 theo phân công DKH.
Hit@3 = tỷ lệ câu hỏi có ít nhất một chunk chứa marker đầu tiên trong tài liệu được chấp nhận;
MRR@3 = trung bình nghịch đảo thứ hạng đầu tiên; Precision@3 dùng mẫu số 3 kể cả khi thiếu kết quả.
Coverage đo tất cả markers trên hợp top-3; anchor_score = 2 nếu rank 1, 1 nếu rank 2/3, 0 nếu thiếu.
Literal matching có thể bỏ sót bằng chứng tương đương; anchor_score không thay thế điểm rubric/đánh giá thủ công.

| Backend | Strategy | Chunks | Avg chars | Hit@3 | MRR@3 | Precision@3 |
|---|---|---:|---:|---:|---:|---:|
| tfidf | fixed_size | 162 | 486.6 | 40% | 0.400 | 0.200 |
| tfidf | by_sentences | 133 | 476.0 | 60% | 0.600 | 0.200 |
| tfidf | recursive | 102 | 623.8 | 40% | 0.400 | 0.200 |
| tfidf | heading | 145 | 542.8 | 60% | 0.500 | 0.267 |
| mock | fixed_size | 162 | 486.6 | 20% | 0.100 | 0.067 |
| mock | by_sentences | 133 | 476.0 | 0% | 0.000 | 0.000 |
| mock | recursive | 102 | 623.8 | 0% | 0.000 | 0.000 |
| mock | heading | 145 | 542.8 | 0% | 0.000 | 0.000 |

## tfidf / fixed_size

### Q1: Theo quy định của UEH, tỷ lệ tương đồng từ bao nhiêu phần trăm thì sản phẩm học thuật bị xem là có dấu hiệu đạo văn?

Filter: `null`; Hit@3: False; coverage: 0%.

Gold: Theo snapshot UEH, tỷ lệ tương đồng từ 20% trở lên là một dấu hiệu định lượng, sau khi loại các phần được miễn trừ nêu trong quy định; không tự động kết luận đạo văn chỉ từ tỷ lệ này.

1. `ueh-dao-van-ai-quy-dinh-chung:fixed_size:003` — score 0.4561; relevant=False

>  ảnh, mô hình, sản phẩm học thuật của người khác mà không ghi nhận, trích dẫn hoặc chú thích phù hợp; hoặc tái sử dụng sản phẩm học thuật của chính mình (tự đạo văn) mà không nêu rõ nguồn gốc và tình trạng công bố.
> 
> ### Tỷ lệ tương đồng học thuật
> 
> Tỷ lệ tương đồng học thuật là tỷ lệ phần trăm nội dung trùng lặp trong sản phẩm học thuật được xác định bằng phần mềm hỗ trợ (Turnitin hoặc các công cụ kiểm tra đạo văn có chức năng so sánh với cơ sở dữ liệu học thuật rộng và cho phép phân tích chi tiế

2. `ueh-dao-van-ai-quy-dinh-chung:fixed_size:004` — score 0.4402; relevant=False

> kiểm tra đạo văn có chức năng so sánh với cơ sở dữ liệu học thuật rộng và cho phép phân tích chi tiết mức độ trùng lặp, được UEH phê duyệt sử dụng). Tỷ lệ tương đồng không phải là căn cứ duy nhất để kết luận đạo văn; việc đánh giá phải dựa trên xem xét chuyên môn của đơn vị quản lý, giảng viên hoặc hội đồng có thẩm quyền.
> 
> ### Các dấu hiệu của hành vi đạo văn hoặc vi phạm liêm chính học thuật
> 
> Sản phẩm học thuật có thể xem là có dấu hiệu vi phạm nếu có ít nhất một trong các biểu hiện sau:
> 
> a) Dấ

3. `ueh-dao-van-ai-quy-dinh-chung:fixed_size:009` — score 0.4165; relevant=False

> ng cụ tương đương để phát hiện tỷ lệ tương đồng học thuật trong các sản phẩm học thuật. Kết quả tỷ lệ tương đồng chỉ mang tính tham khảo, hỗ trợ, không tự động kết luận là đạo văn. Việc kết luận dựa trên xem xét bối cảnh, phạm vi, tính chất nội dung trùng lặp, ý chí của người thực hiện và các chứng cứ liên quan. Việc đánh giá do giảng viên phụ trách/người hướng dẫn hoặc hội đồng/đơn vị có thẩm quyền thực hiện theo quy trình được UEH quy định.
> 
> 2. Xử lý hành vi đạo văn
> 
> ### 2.1 Nguyên tắc xử lý h

**Agent output:**

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

Filter: `{"audience": "student"}`; Hit@3: True; coverage: 100%.

Gold: Trong bối cảnh bài tập học phần của người học: giảng viên phụ trách lập biên bản/thông báo chuyển về đơn vị quản lý để xử lý tùy mức độ vi phạm quy định tại Phụ lục 3.

1. `ueh-xu-ly-vi-pham-nguoi-hoc:fixed_size:002` — score 0.4009; relevant=True

>  nhiệm theo các quy định của UEH và pháp luật hiện hành.
> 
> ### 2.3 Đối với các bài kiểm tra, bài tập, tiểu luận và các bài khác thuộc các học phần
> 
> a) Khi bị phát hiện vi phạm lần đầu, người học phải chỉnh sửa và nộp lại bài theo yêu cầu của giảng viên;
> 
> b) Sau khi đã chỉnh sửa, người học nộp lại bài nhưng vẫn vi phạm lỗi đạo văn thì giảng viên phụ trách học phần lập biên bản/thông báo chuyển về đơn vị quản lý để xử lý tùy theo mức độ vi phạm quy định tại Phụ lục 3.
> 
> ## Điều 5. Xử lý vi phạm sử d

2. `ueh-xu-ly-vi-pham-nguoi-hoc:fixed_size:005` — score 0.3325; relevant=True

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

3. `ueh-xu-ly-vi-pham-nguoi-hoc:fixed_size:000` — score 0.2734; relevant=False

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

**Agent output:**

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

Filter: `null`; Hit@3: False; coverage: 0%.

Gold: Theo hướng dẫn RMIT Library: nêu cách sử dụng AI, tên công cụ và nhà phát triển, năm nội dung AI được người dùng tạo ra. Không bắt buộc phiên bản/ngày dùng trừ khi giảng viên yêu cầu.

1. `ueh-dao-van-ai-quy-dinh-chung:fixed_size:014` — score 0.2160; relevant=False

> ạt động học thuật tại UEH được sử dụng AI để hỗ trợ hoạt động nghiên cứu và học tập tại UEH trên cơ sở tuân thủ các nguyên tắc sau:
> 
> - Minh bạch: ghi rõ công cụ AI tạo sinh đã sử dụng, mục đích sử dụng (tóm tắt, dịch thuật, tạo hình, viết mã v.v.) và những nội dung có sự hỗ trợ của AI tạo sinh trong sản phẩm học thuật. Việc khai báo cần thực hiện theo chuẩn, ví dụ: Trong phần Acknowledgement hoặc Phương pháp nghiên cứu ghi: “Một phần nội dung của sản phẩm này được hỗ trợ bởi ChatGPT (phiên bản …

2. `ueh-dao-van-ai-quy-dinh-chung:fixed_size:017` — score 0.1707; relevant=False

> , không bắt buộc thông báo nếu chỉ sử dụng để kiểm tra ngôn ngữ, chỉnh lỗi chính tả, ngữ pháp hoặc dịch thuật trực tiếp không mang tính sáng tạo nội dung.
> 3. Những hành vi bị xem là vi phạm quy tắc sử dụng AI trong học thuật:
> 
> a) Sử dụng nội dung do AI tạo ra nhưng không thông báo hoặc thông báo không đầy đủ việc sử dụng công cụ, phạm vi và vai trò của AI.
> 
> b) Sử dụng AI để tạo ra nội dung nhưng không kiểm tra, xác nhận nguồn hoặc độ chính xác.
> 
> c) Sử dụng AI để tạo ra toàn bộ hoặc phần lớn nội 

3. `ueh-dao-van-ai-quy-dinh-chung:fixed_size:020` — score 0.1629; relevant=False

> huật
> 
> 1. Việc phát hiện và đánh giá vi phạm sử dụng AI trong học thuật do giảng viên phụ trách/người hướng dẫn hoặc hội đồng/đơn vị có thẩm quyền thực hiện, trên cơ sở xem xét các yếu tố: mức độ sử dụng AI, vai trò của AI trong sản phẩm, hành vi thông báo sử dụng hoặc không thông báo, dấu hiệu gian lận hoặc thay thế nhiệm vụ học thuật. UEH không sử dụng kết quả của các công cụ phát hiện nội dụng do AI tạo ra làm căn cứ duy nhất để kết luận vi phạm học thuật. Đánh giá vi phạm sử dụng AI được thực

**Agent output:**

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

Filter: `null`; Hit@3: False; coverage: 0%.

Gold: Theo snapshot UNA, không nhập thông tin cá nhân, bí mật, độc quyền hoặc nhạy cảm: ví dụ hồ sơ sinh viên/tuyển sinh, số an sinh xã hội, dữ liệu thẻ/ngân hàng, giấy tờ định danh, dữ liệu y tế/bảo hiểm, dữ liệu người tham gia nghiên cứu chưa được đồng ý công khai, hồ sơ nội bộ và nội dung thuộc NDA/sở hữu trí tuệ chưa được phép. Danh sách ví dụ không giới hạn ở một loại dữ liệu.

1. `ueh-dao-van-ai-quy-dinh-chung:fixed_size:011` — score 0.2731; relevant=False

> lỗi kỹ thuật hoặc sơ suất trong ghi nguồn, trích dẫn không đầy đủ, có thể được xem xét yêu cầu chỉnh sửa mà không xử phạt nếu không có dấu hiệu gian lận.
> 
> ## Điều 4. Sử dụng AI trong học thuật
> 
> 1. Trong Quy định này, trí tuệ nhân tạo (AI) được hiểu là các công cụ, hệ thống hoặc thuật toán có khả năng tạo, phân tích hoặc xử lý nội dung hỗ trợ hoạt động học thuật. AI được xem là công cụ hỗ trợ, không thay thế trách nhiệm tư duy, phân tích và sáng tạo của tác giả. AI trong học thuật được phân loại 

2. `ueh-dao-van-ai-quy-dinh-chung:fixed_size:016` — score 0.2475; relevant=False

>  cấp cho AI dữ liệu cá nhân, dữ liệu mật, thông tin chưa công bố hoặc dữ liệu nghiên cứu nội bộ của UEH hoặc đối tác nếu chưa được phép.
> - Không lạm dụng: không sử dụng AI để thay thế nhiệm vụ học thuật mà người học hoặc giảng viên phải tự thực hiện. AI chỉ đóng vai trò hỗ trợ. Khuyến khích người học và giảng viên sử dụng có trách nhiệm và không phụ thuộc hoàn toàn vào công cụ.
> - Đối với AI hỗ trợ, không bắt buộc thông báo nếu chỉ sử dụng để kiểm tra ngôn ngữ, chỉnh lỗi chính tả, ngữ pháp hoặc d

3. `ueh-dao-van-ai-quy-dinh-chung:fixed_size:017` — score 0.2366; relevant=False

> , không bắt buộc thông báo nếu chỉ sử dụng để kiểm tra ngôn ngữ, chỉnh lỗi chính tả, ngữ pháp hoặc dịch thuật trực tiếp không mang tính sáng tạo nội dung.
> 3. Những hành vi bị xem là vi phạm quy tắc sử dụng AI trong học thuật:
> 
> a) Sử dụng nội dung do AI tạo ra nhưng không thông báo hoặc thông báo không đầy đủ việc sử dụng công cụ, phạm vi và vai trò của AI.
> 
> b) Sử dụng AI để tạo ra nội dung nhưng không kiểm tra, xác nhận nguồn hoặc độ chính xác.
> 
> c) Sử dụng AI để tạo ra toàn bộ hoặc phần lớn nội 

**Agent output:**

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

Filter: `null`; Hit@3: True; coverage: 100%.

Gold: Theo Điều 22 trong snapshot nhóm cung cấp: hiệu lực từ 15/08/2026; Thông tư 15/2018/TT-BGDĐT và 30/2023/TT-BGDĐT hết hiệu lực từ ngày đó. Đây là gold answer kiểm thử snapshot, chưa xác minh tình trạng pháp lý hiện hành.

1. `tt49-2026-ung-dung-cong-nghe-ai:fixed_size:029` — score 0.3587; relevant=True

> học thuật; trung thực trong học tập, giảng dạy, nghiên cứu khoa học và công bố việc sử dụng công nghệ, trí tuệ nhân tạo khi có yêu cầu.
> 
> ## Điều 22. Điều khoản thi hành
> 
> 1. Thông tư này có hiệu lực thi hành kể từ ngày 15 tháng 08 năm 2026.
> 
> 2. Thông tư số 15/2018/TT-BGDĐT ngày 27 tháng 7 năm 2018 của Bộ trưởng Bộ Giáo dục và Đào tạo quy định tổ chức hoạt động, sử dụng thư điện tử và trang thông tin điện tử của các cơ sở giáo dục đại học, các trường cao đẳng sư phạm; Thông tư số 30/2023/TT-BGDĐT 

2. `tt49-2026-ung-dung-cong-nghe-ai:fixed_size:030` — score 0.3111; relevant=False

> n điện tử của các cơ sở giáo dục đại học, các trường cao đẳng sư phạm; Thông tư số 30/2023/TT-BGDĐT ngày 29 tháng 12 năm 2023 của Bộ trưởng Bộ Giáo dục và Đào tạo quy định về ứng dụng công nghệ thông tin trong đào tạo trực tuyến đối với giáo dục đại học hết hiệu lực thi hành từ ngày Thông tư này có hiệu lực.
> 
> 3. Chánh Văn phòng, Cục trưởng Cục Khoa học, Công nghệ và Thông tin, Thủ trưởng các đơn vị thuộc Bộ Giáo dục và Đào tạo, Giám đốc các đại học, học viện, Hiệu trưởng các trường đại học, Hiệu

3. `tt49-2026-ung-dung-cong-nghe-ai:fixed_size:000` — score 0.3103; relevant=False

> # Thông tư 49/2026/TT-BGDĐT — Ứng dụng công nghệ và AI trong giáo dục đại học
> 
> Số: 49/2026/TT-BGDĐT — Hà Nội, ngày 30 tháng 06 năm 2026.
> 
> Quy định ứng dụng công nghệ trong giáo dục đại học, giáo dục nghề nghiệp (trích các Điều liên quan đến trí tuệ nhân tạo và liêm chính học thuật).
> 
> ## Điều 1. Phạm vi điều chỉnh
> 
> Thông tư này quy định về ứng dụng công nghệ trong giáo dục đại học, giáo dục nghề nghiệp bao gồm: nguyên tắc, nội dung và điều kiện bảo đảm việc ứng dụng công nghệ số, trí tuệ nhân tạo

**Agent output:**

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


## tfidf / by_sentences

### Q1: Theo quy định của UEH, tỷ lệ tương đồng từ bao nhiêu phần trăm thì sản phẩm học thuật bị xem là có dấu hiệu đạo văn?

Filter: `null`; Hit@3: True; coverage: 100%.

Gold: Theo snapshot UEH, tỷ lệ tương đồng từ 20% trở lên là một dấu hiệu định lượng, sau khi loại các phần được miễn trừ nêu trong quy định; không tự động kết luận đạo văn chỉ từ tỷ lệ này.

1. `ueh-dao-van-ai-quy-dinh-chung:by_sentences:002` — score 0.5225; relevant=True

> ### Tỷ lệ tương đồng học thuật
> 
> Tỷ lệ tương đồng học thuật là tỷ lệ phần trăm nội dung trùng lặp trong sản phẩm học thuật được xác định bằng phần mềm hỗ trợ (Turnitin hoặc các công cụ kiểm tra đạo văn có chức năng so sánh với cơ sở dữ liệu học thuật rộng và cho phép phân tích chi tiết mức độ trùng lặp, được UEH phê duyệt sử dụng). Tỷ lệ tương đồng không phải là căn cứ duy nhất để kết luận đạo văn; việc đánh giá phải dựa trên xem xét chuyên môn của đơn vị quản lý, giảng viên hoặc hội đồng có thẩm quyền. ### Các dấu hiệu của hành vi đạo văn hoặc vi phạm liêm chính học thuật
> 
> Sản phẩm học thuật có thể xem là có dấu hiệu vi phạm nếu có ít nhất một trong các biểu hiện sau:
> 
> a) Dấu hiệu định lượng từ phần mềm kiểm tra
> 
> - Có tỷ lệ tương đồng từ 20% trở lên (không tính phần: trích dẫn, danh mục tài liệu tham khảo, phần mô tả phương pháp mang tính lặp lại và phổ biến trong chuyên ngành, các thuật ngữ chuyên ngành, tiêu chuẩn kỹ thuật, trích dẫn văn bản quy phạm pháp luật, tên riêng không thể thay thế).

2. `ueh-dao-van-ai-quy-dinh-chung:by_sentences:007` — score 0.4195; relevant=False

> ## Điều 3. Phát hiện và xử lý hành vi đạo văn
> 
> 1. UEH sử dụng phần mềm Turnitin và/hoặc công cụ tương đương để phát hiện tỷ lệ tương đồng học thuật trong các sản phẩm học thuật.

3. `ueh-dao-van-ai-quy-dinh-chung:by_sentences:008` — score 0.3168; relevant=False

> Kết quả tỷ lệ tương đồng chỉ mang tính tham khảo, hỗ trợ, không tự động kết luận là đạo văn. Việc kết luận dựa trên xem xét bối cảnh, phạm vi, tính chất nội dung trùng lặp, ý chí của người thực hiện và các chứng cứ liên quan. Việc đánh giá do giảng viên phụ trách/người hướng dẫn hoặc hội đồng/đơn vị có thẩm quyền thực hiện theo quy trình được UEH quy định.

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> ### Tỷ lệ tương đồng học thuật
> 
> Tỷ lệ tương đồng học thuật là tỷ lệ phần trăm nội dung trùng lặp trong sản phẩm học thuật được xác định bằng phần mềm hỗ trợ (Turnitin hoặc các công cụ kiểm tra đạo văn có chức năng so sánh với cơ sở dữ liệu học thuật rộng và cho phép phân tích chi tiết mức độ trùng lặp, được UEH phê duyệt sử dụng). Tỷ lệ tương đồng không phải là căn cứ duy nhất để kết luận đạo văn; việc đánh giá phải dựa trên xem xét chuyên môn của đơn vị quản lý, giảng viên hoặc hội đồng có thẩm quyền. ### Các dấu hiệu của hành vi đạo văn hoặc vi phạm liêm chính học thuật
> 
> Sản phẩm học thuật có thể xem là có dấu hiệu vi phạm nếu có ít nhất một trong các biểu hiện sau:
> 
> a) Dấu hiệu định lượng từ phần mềm kiểm tra
> 
> - Có tỷ lệ tương đồng từ 20% trở lên (không tính phần: trích dẫn, danh mục tài liệu tham khảo, phần mô tả phương pháp mang tính lặp lại và phổ biến trong chuyên ngành, các thuật ngữ chuyên ngành, tiêu chuẩn kỹ thuật, trích dẫn văn bản quy phạm pháp luật, tên riêng không thể thay thế).
> [ueh-dao-van-ai-quy-dinh-chung:by_sentences:002](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
> 
> ## Điều 3. Phát hiện và xử lý hành vi đạo văn
> 
> 1. UEH sử dụng phần mềm Turnitin và/hoặc công cụ tương đương để phát hiện tỷ lệ tương đồng học thuật trong các sản phẩm học thuật.
> [ueh-dao-van-ai-quy-dinh-chung:by_sentences:007](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
> 
> Kết quả tỷ lệ tương đồng chỉ mang tính tham khảo, hỗ trợ, không tự động kết luận là đạo văn. Việc kết luận dựa trên xem xét bối cảnh, phạm vi, tính chất nội dung trùng lặp, ý chí của người thực hiện và các chứng cứ liên quan. Việc đánh giá do giảng viên phụ trách/người hướng dẫn hoặc hội đồng/đơn vị có thẩm quyền thực hiện theo quy trình được UEH quy định.
> [ueh-dao-van-ai-quy-dinh-chung:by_sentences:008](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)


### Q2: Sản phẩm học thuật đã chỉnh sửa nhưng vẫn vi phạm lỗi đạo văn thì xử lý ra sao?

Filter: `{"audience": "student"}`; Hit@3: True; coverage: 100%.

Gold: Trong bối cảnh bài tập học phần của người học: giảng viên phụ trách lập biên bản/thông báo chuyển về đơn vị quản lý để xử lý tùy mức độ vi phạm quy định tại Phụ lục 3.

1. `ueh-xu-ly-vi-pham-nguoi-hoc:by_sentences:001` — score 0.3951; relevant=True

> c) Sau bảo vệ:
> 
> Sau khi đã bảo vệ, nếu có phát hiện lỗi đạo văn, tác giả chịu trách nhiệm theo các quy định của UEH và pháp luật hiện hành. ### 2.3 Đối với các bài kiểm tra, bài tập, tiểu luận và các bài khác thuộc các học phần
> 
> a) Khi bị phát hiện vi phạm lần đầu, người học phải chỉnh sửa và nộp lại bài theo yêu cầu của giảng viên;
> 
> b) Sau khi đã chỉnh sửa, người học nộp lại bài nhưng vẫn vi phạm lỗi đạo văn thì giảng viên phụ trách học phần lập biên bản/thông báo chuyển về đơn vị quản lý để xử lý tùy theo mức độ vi phạm quy định tại Phụ lục 3. ## Điều 5.

2. `ueh-xu-ly-vi-pham-nguoi-hoc:by_sentences:000` — score 0.3157; relevant=False

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
> Khi phát hiện có dấu hiệu đạo văn, người học phải chỉnh sửa, bổ sung và khắc phục theo yêu cầu của giảng viên hướng dẫn hoặc đơn vị quản lý. b) Trong khi bảo vệ:
> 
> Nếu Hội đồng đánh giá luận văn/luận án phát hiện hành vi đạo văn, chủ tịch hội đồng quyết định luận văn/luận án không đạt, người học phải chỉnh sửa lại sản phẩm và khắc phục lỗi đạo văn theo quy định của chương trình.

3. `ueh-xu-ly-vi-pham-nguoi-hoc:by_sentences:002` — score 0.2980; relevant=False

> Xử lý vi phạm sử dụng AI trong học thuật — áp dụng cho người học
> 
> ### 2.1. Đối với khóa luận, đề án tốt nghiệp, luận văn, luận án
> 
> a) Trước khi bảo vệ:
> 
> Người học phải chỉnh sửa và khắc phục vi phạm theo yêu cầu của giảng viên hướng dẫn hoặc đơn vị quản lý. b) Trong quá trình bảo vệ hoặc đánh giá:
> 
> Nếu Hội đồng đánh giá đề án tốt nghiệp, luận văn, luận án hoặc giảng viên phụ trách phát hiện vi phạm sử dụng AI trong học thuật, chủ tịch hội đồng/giảng viên phụ trách quyết định khóa luận, đề án tốt nghiệp, luận văn, luận án không đạt, người học phải chỉnh sửa lại sản phẩm và khắc phục vi phạm.

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> c) Sau bảo vệ:
> 
> Sau khi đã bảo vệ, nếu có phát hiện lỗi đạo văn, tác giả chịu trách nhiệm theo các quy định của UEH và pháp luật hiện hành. ### 2.3 Đối với các bài kiểm tra, bài tập, tiểu luận và các bài khác thuộc các học phần
> 
> a) Khi bị phát hiện vi phạm lần đầu, người học phải chỉnh sửa và nộp lại bài theo yêu cầu của giảng viên;
> 
> b) Sau khi đã chỉnh sửa, người học nộp lại bài nhưng vẫn vi phạm lỗi đạo văn thì giảng viên phụ trách học phần lập biên bản/thông báo chuyển về đơn vị quản lý để xử lý tùy theo mức độ vi phạm quy định tại Phụ lục 3. ## Điều 5.
> [ueh-xu-ly-vi-pham-nguoi-hoc:by_sentences:001](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
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
> Khi phát hiện có dấu hiệu đạo văn, người học phải chỉnh sửa, bổ sung và khắc phục theo yêu cầu của giảng viên hướng dẫn hoặc đơn vị quản lý. b) Trong khi bảo vệ:
> 
> Nếu Hội đồng đánh giá luận văn/luận án phát hiện hành vi đạo văn, chủ tịch hội đồng quyết định luận văn/luận án không đạt, người học phải chỉnh sửa lại sản phẩm và khắc phục lỗi đạo văn theo quy định của chương trình.
> [ueh-xu-ly-vi-pham-nguoi-hoc:by_sentences:000](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
> 
> Xử lý vi phạm sử dụng AI trong học thuật — áp dụng cho người học
> 
> ### 2.1. Đối với khóa luận, đề án tốt nghiệp, luận văn, luận án
> 
> a) Trước khi bảo vệ:
> 
> Người học phải chỉnh sửa và khắc phục vi phạm theo yêu cầu của giảng viên hướng dẫn hoặc đơn vị quản lý. b) Trong quá trình bảo vệ hoặc đánh giá:
> 
> Nếu Hội đồng đánh giá đề án tốt nghiệp, luận văn, luận án hoặc giảng viên phụ trách phát hiện vi phạm sử dụng AI trong học thuật, chủ tịch hội đồng/giảng viên phụ trách quyết định khóa luận, đề án tốt nghiệp, luận văn, luận án không đạt, người học phải chỉnh sửa lại sản phẩm và khắc phục vi phạm.
> [ueh-xu-ly-vi-pham-nguoi-hoc:by_sentences:002](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)


### Q3: Khi ghi nhận việc dùng công cụ AI trong bài làm, câu acknowledgement cần nêu những thông tin gì?

Filter: `null`; Hit@3: False; coverage: 0%.

Gold: Theo hướng dẫn RMIT Library: nêu cách sử dụng AI, tên công cụ và nhà phát triển, năm nội dung AI được người dùng tạo ra. Không bắt buộc phiên bản/ngày dùng trừ khi giảng viên yêu cầu.

1. `ueh-dao-van-ai-quy-dinh-chung:by_sentences:012` — score 0.2079; relevant=False

> Viên chức, người lao động, người học, giảng viên thỉnh giảng và các cá nhân, tổ chức khác có tham gia hoạt động học thuật tại UEH được sử dụng AI để hỗ trợ hoạt động nghiên cứu và học tập tại UEH trên cơ sở tuân thủ các nguyên tắc sau:
> 
> - Minh bạch: ghi rõ công cụ AI tạo sinh đã sử dụng, mục đích sử dụng (tóm tắt, dịch thuật, tạo hình, viết mã v.v.) và những nội dung có sự hỗ trợ của AI tạo sinh trong sản phẩm học thuật. Việc khai báo cần thực hiện theo chuẩn, ví dụ: Trong phần Acknowledgement hoặc Phương pháp nghiên cứu ghi: “Một phần nội dung của sản phẩm này được hỗ trợ bởi ChatGPT (phiên bản …), sử dụng cho mục đích tóm tắt tài liệu/tham khảo ý tưởng/ngôn ngữ.”
> - Trung thực và trách nhiệm: tác giả chịu trách nhiệm về tính chính xác, độ tin cậy, chất lượng và liêm chính học thuật của những nội dung được AI cung cấp. - Tôn trọng quyền riêng tư, sở hữu trí tuệ và bảo mật dữ liệu: không cung cấp cho AI dữ liệu cá nhân, dữ liệu mật, thông tin chưa công bố hoặc dữ liệu nghiên cứu nội bộ của UEH hoặc đối tác nếu chưa được phép.

2. `ueh-dao-van-ai-quy-dinh-chung:by_sentences:014` — score 0.1776; relevant=False

> - Đối với AI hỗ trợ, không bắt buộc thông báo nếu chỉ sử dụng để kiểm tra ngôn ngữ, chỉnh lỗi chính tả, ngữ pháp hoặc dịch thuật trực tiếp không mang tính sáng tạo nội dung. 3. Những hành vi bị xem là vi phạm quy tắc sử dụng AI trong học thuật:
> 
> a) Sử dụng nội dung do AI tạo ra nhưng không thông báo hoặc thông báo không đầy đủ việc sử dụng công cụ, phạm vi và vai trò của AI.

3. `ueh-dao-van-ai-quy-dinh-chung:by_sentences:001` — score 0.1521; relevant=False

> Sản phẩm học thuật trong phạm vi điều chỉnh của Quy định bao gồm, nhưng không giới hạn: bài báo khoa học, báo cáo nghiên cứu khoa học, bài tham luận tại hội thảo, khóa luận tốt nghiệp, đề án tốt nghiệp, luận văn thạc sĩ, luận án tiến sĩ, bài tập, tiểu luận, chuyên đề và các dạng sản phẩm học thuật khác do UEH quy định hoặc công nhận. ## Điều 2. Nhận diện và xác định hành vi đạo văn
> 
> ### Khái niệm đạo văn
> 
> Đạo văn là hành vi sử dụng trực tiếp hoặc gián tiếp, toàn bộ hoặc một phần ý tưởng, dữ liệu, ngôn từ, hình ảnh, mô hình, sản phẩm học thuật của người khác mà không ghi nhận, trích dẫn hoặc chú thích phù hợp; hoặc tái sử dụng sản phẩm học thuật của chính mình (tự đạo văn) mà không nêu rõ nguồn gốc và tình trạng công bố.

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> Viên chức, người lao động, người học, giảng viên thỉnh giảng và các cá nhân, tổ chức khác có tham gia hoạt động học thuật tại UEH được sử dụng AI để hỗ trợ hoạt động nghiên cứu và học tập tại UEH trên cơ sở tuân thủ các nguyên tắc sau:
> 
> - Minh bạch: ghi rõ công cụ AI tạo sinh đã sử dụng, mục đích sử dụng (tóm tắt, dịch thuật, tạo hình, viết mã v.v.) và những nội dung có sự hỗ trợ của AI tạo sinh trong sản phẩm học thuật. Việc khai báo cần thực hiện theo chuẩn, ví dụ: Trong phần Acknowledgement hoặc Phương pháp nghiên cứu ghi: “Một phần nội dung của sản phẩm này được hỗ trợ bởi ChatGPT (phiên bản …), sử dụng cho mục đích tóm tắt tài liệu/tham khảo ý tưởng/ngôn ngữ.”
> - Trung thực và trách nhiệm: tác giả chịu trách nhiệm về tính chính xác, độ tin cậy, chất lượng và liêm chính học thuật của những nội dung được AI cung cấp. - Tôn trọng quyền riêng tư, sở hữu trí tuệ và bảo mật dữ liệu: không cung cấp cho AI dữ liệu cá nhân, dữ liệu mật, thông tin chưa công bố hoặc dữ liệu nghiên cứu nội bộ của UEH hoặc đối tác nếu chưa được phép.
> [ueh-dao-van-ai-quy-dinh-chung:by_sentences:012](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
> 
> - Đối với AI hỗ trợ, không bắt buộc thông báo nếu chỉ sử dụng để kiểm tra ngôn ngữ, chỉnh lỗi chính tả, ngữ pháp hoặc dịch thuật trực tiếp không mang tính sáng tạo nội dung. 3. Những hành vi bị xem là vi phạm quy tắc sử dụng AI trong học thuật:
> 
> a) Sử dụng nội dung do AI tạo ra nhưng không thông báo hoặc thông báo không đầy đủ việc sử dụng công cụ, phạm vi và vai trò của AI.
> [ueh-dao-van-ai-quy-dinh-chung:by_sentences:014](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
> 
> Sản phẩm học thuật trong phạm vi điều chỉnh của Quy định bao gồm, nhưng không giới hạn: bài báo khoa học, báo cáo nghiên cứu khoa học, bài tham luận tại hội thảo, khóa luận tốt nghiệp, đề án tốt nghiệp, luận văn thạc sĩ, luận án tiến sĩ, bài tập, tiểu luận, chuyên đề và các dạng sản phẩm học thuật khác do UEH quy định hoặc công nhận. ## Điều 2. Nhận diện và xác định hành vi đạo văn
> 
> ### Khái niệm đạo văn
> 
> Đạo văn là hành vi sử dụng trực tiếp hoặc gián tiếp, toàn bộ hoặc một phần ý tưởng, dữ liệu, ngôn từ, hình ảnh, mô hình, sản phẩm học thuật của người khác mà không ghi nhận, trích dẫn hoặc chú thích phù hợp; hoặc tái sử dụng sản phẩm học thuật của chính mình (tự đạo văn) mà không nêu rõ nguồn gốc và tình trạng công bố.
> [ueh-dao-van-ai-quy-dinh-chung:by_sentences:001](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)


### Q4: Những loại thông tin nào không được phép nhập vào công cụ AI tạo sinh?

Filter: `null`; Hit@3: False; coverage: 0%.

Gold: Theo snapshot UNA, không nhập thông tin cá nhân, bí mật, độc quyền hoặc nhạy cảm: ví dụ hồ sơ sinh viên/tuyển sinh, số an sinh xã hội, dữ liệu thẻ/ngân hàng, giấy tờ định danh, dữ liệu y tế/bảo hiểm, dữ liệu người tham gia nghiên cứu chưa được đồng ý công khai, hồ sơ nội bộ và nội dung thuộc NDA/sở hữu trí tuệ chưa được phép. Danh sách ví dụ không giới hạn ở một loại dữ liệu.

1. `ueh-dao-van-ai-quy-dinh-chung:by_sentences:012` — score 0.2643; relevant=False

> Viên chức, người lao động, người học, giảng viên thỉnh giảng và các cá nhân, tổ chức khác có tham gia hoạt động học thuật tại UEH được sử dụng AI để hỗ trợ hoạt động nghiên cứu và học tập tại UEH trên cơ sở tuân thủ các nguyên tắc sau:
> 
> - Minh bạch: ghi rõ công cụ AI tạo sinh đã sử dụng, mục đích sử dụng (tóm tắt, dịch thuật, tạo hình, viết mã v.v.) và những nội dung có sự hỗ trợ của AI tạo sinh trong sản phẩm học thuật. Việc khai báo cần thực hiện theo chuẩn, ví dụ: Trong phần Acknowledgement hoặc Phương pháp nghiên cứu ghi: “Một phần nội dung của sản phẩm này được hỗ trợ bởi ChatGPT (phiên bản …), sử dụng cho mục đích tóm tắt tài liệu/tham khảo ý tưởng/ngôn ngữ.”
> - Trung thực và trách nhiệm: tác giả chịu trách nhiệm về tính chính xác, độ tin cậy, chất lượng và liêm chính học thuật của những nội dung được AI cung cấp. - Tôn trọng quyền riêng tư, sở hữu trí tuệ và bảo mật dữ liệu: không cung cấp cho AI dữ liệu cá nhân, dữ liệu mật, thông tin chưa công bố hoặc dữ liệu nghiên cứu nội bộ của UEH hoặc đối tác nếu chưa được phép.

2. `ueh-dao-van-ai-quy-dinh-chung:by_sentences:014` — score 0.2508; relevant=False

> - Đối với AI hỗ trợ, không bắt buộc thông báo nếu chỉ sử dụng để kiểm tra ngôn ngữ, chỉnh lỗi chính tả, ngữ pháp hoặc dịch thuật trực tiếp không mang tính sáng tạo nội dung. 3. Những hành vi bị xem là vi phạm quy tắc sử dụng AI trong học thuật:
> 
> a) Sử dụng nội dung do AI tạo ra nhưng không thông báo hoặc thông báo không đầy đủ việc sử dụng công cụ, phạm vi và vai trò của AI.

3. `ueh-dao-van-ai-quy-dinh-chung:by_sentences:011` — score 0.2300; relevant=False

> AI được xem là công cụ hỗ trợ, không thay thế trách nhiệm tư duy, phân tích và sáng tạo của tác giả. AI trong học thuật được phân loại thành hai nhóm chính: (1) AI hỗ trợ (Assistive AI), là các công cụ hoặc tính năng sử dụng AI để hỗ trợ kỹ thuật như chỉnh lỗi ngôn ngữ, kiểm tra chính tả, ngữ pháp, dịch thuật hoặc đề xuất cấu trúc câu, bao gồm nhưng không giới hạn ở Google Translate, Grammarly, chức năng kiểm lỗi ngữ pháp của phần mềm soạn thảo văn bản (như MS Word) và (2) AI tạo sinh (Generative AI), là các hệ thống có khả năng tự tạo nội dung mới như văn bản, mã lệnh, hình ảnh, luận điểm hoặc cấu trúc học thuật theo yêu cầu người dùng, ví dụ: ChatGPT, Claude, Gemini, Copilot và các mô hình ngôn ngữ lớn (LLMs) khác. 2.

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> Viên chức, người lao động, người học, giảng viên thỉnh giảng và các cá nhân, tổ chức khác có tham gia hoạt động học thuật tại UEH được sử dụng AI để hỗ trợ hoạt động nghiên cứu và học tập tại UEH trên cơ sở tuân thủ các nguyên tắc sau:
> 
> - Minh bạch: ghi rõ công cụ AI tạo sinh đã sử dụng, mục đích sử dụng (tóm tắt, dịch thuật, tạo hình, viết mã v.v.) và những nội dung có sự hỗ trợ của AI tạo sinh trong sản phẩm học thuật. Việc khai báo cần thực hiện theo chuẩn, ví dụ: Trong phần Acknowledgement hoặc Phương pháp nghiên cứu ghi: “Một phần nội dung của sản phẩm này được hỗ trợ bởi ChatGPT (phiên bản …), sử dụng cho mục đích tóm tắt tài liệu/tham khảo ý tưởng/ngôn ngữ.”
> - Trung thực và trách nhiệm: tác giả chịu trách nhiệm về tính chính xác, độ tin cậy, chất lượng và liêm chính học thuật của những nội dung được AI cung cấp. - Tôn trọng quyền riêng tư, sở hữu trí tuệ và bảo mật dữ liệu: không cung cấp cho AI dữ liệu cá nhân, dữ liệu mật, thông tin chưa công bố hoặc dữ liệu nghiên cứu nội bộ của UEH hoặc đối tác nếu chưa được phép.
> [ueh-dao-van-ai-quy-dinh-chung:by_sentences:012](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
> 
> - Đối với AI hỗ trợ, không bắt buộc thông báo nếu chỉ sử dụng để kiểm tra ngôn ngữ, chỉnh lỗi chính tả, ngữ pháp hoặc dịch thuật trực tiếp không mang tính sáng tạo nội dung. 3. Những hành vi bị xem là vi phạm quy tắc sử dụng AI trong học thuật:
> 
> a) Sử dụng nội dung do AI tạo ra nhưng không thông báo hoặc thông báo không đầy đủ việc sử dụng công cụ, phạm vi và vai trò của AI.
> [ueh-dao-van-ai-quy-dinh-chung:by_sentences:014](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
> 
> AI được xem là công cụ hỗ trợ, không thay thế trách nhiệm tư duy, phân tích và sáng tạo của tác giả. AI trong học thuật được phân loại thành hai nhóm chính: (1) AI hỗ trợ (Assistive AI), là các công cụ hoặc tính năng sử dụng AI để hỗ trợ kỹ thuật như chỉnh lỗi ngôn ngữ, kiểm tra chính tả, ngữ pháp, dịch thuật hoặc đề xuất cấu trúc câu, bao gồm nhưng không giới hạn ở Google Translate, Grammarly, chức năng kiểm lỗi ngữ pháp của phần mềm soạn thảo văn bản (như MS Word) và (2) AI tạo sinh (Generative AI), là các hệ thống có khả năng tự tạo nội dung mới như văn bản, mã lệnh, hình ảnh, luận điểm hoặc cấu trúc học thuật theo yêu cầu người dùng, ví dụ: ChatGPT, Claude, Gemini, Copilot và các mô hình ngôn ngữ lớn (LLMs) khác. 2.
> [ueh-dao-van-ai-quy-dinh-chung:by_sentences:011](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)


### Q5: Thông tư 49/2026/TT-BGDĐT có hiệu lực từ ngày nào và thay thế những thông tư nào?

Filter: `null`; Hit@3: True; coverage: 100%.

Gold: Theo Điều 22 trong snapshot nhóm cung cấp: hiệu lực từ 15/08/2026; Thông tư 15/2018/TT-BGDĐT và 30/2023/TT-BGDĐT hết hiệu lực từ ngày đó. Đây là gold answer kiểm thử snapshot, chưa xác minh tình trạng pháp lý hiện hành.

1. `tt49-2026-ung-dung-cong-nghe-ai:by_sentences:022` — score 0.3669; relevant=True

> ## Điều 22. Điều khoản thi hành
> 
> 1. Thông tư này có hiệu lực thi hành kể từ ngày 15 tháng 08 năm 2026.

2. `tt49-2026-ung-dung-cong-nghe-ai:by_sentences:023` — score 0.3552; relevant=False

> 2. Thông tư số 15/2018/TT-BGDĐT ngày 27 tháng 7 năm 2018 của Bộ trưởng Bộ Giáo dục và Đào tạo quy định tổ chức hoạt động, sử dụng thư điện tử và trang thông tin điện tử của các cơ sở giáo dục đại học, các trường cao đẳng sư phạm; Thông tư số 30/2023/TT-BGDĐT ngày 29 tháng 12 năm 2023 của Bộ trưởng Bộ Giáo dục và Đào tạo quy định về ứng dụng công nghệ thông tin trong đào tạo trực tuyến đối với giáo dục đại học hết hiệu lực thi hành từ ngày Thông tư này có hiệu lực. 3.

3. `tt49-2026-ung-dung-cong-nghe-ai:by_sentences:000` — score 0.3529; relevant=False

> # Thông tư 49/2026/TT-BGDĐT — Ứng dụng công nghệ và AI trong giáo dục đại học
> 
> Số: 49/2026/TT-BGDĐT — Hà Nội, ngày 30 tháng 06 năm 2026. Quy định ứng dụng công nghệ trong giáo dục đại học, giáo dục nghề nghiệp (trích các Điều liên quan đến trí tuệ nhân tạo và liêm chính học thuật). ## Điều 1.

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> ## Điều 22. Điều khoản thi hành
> 
> 1. Thông tư này có hiệu lực thi hành kể từ ngày 15 tháng 08 năm 2026.
> [tt49-2026-ung-dung-cong-nghe-ai:by_sentences:022](https://luatvietnam.vn/giao-duc/thong-tu-49-2026-tt-bgddt-ung-dung-cong-nghe-trong-giao-duc-dai-hoc-va-nghe-nghiep-439350-d1.html)
> 
> 2. Thông tư số 15/2018/TT-BGDĐT ngày 27 tháng 7 năm 2018 của Bộ trưởng Bộ Giáo dục và Đào tạo quy định tổ chức hoạt động, sử dụng thư điện tử và trang thông tin điện tử của các cơ sở giáo dục đại học, các trường cao đẳng sư phạm; Thông tư số 30/2023/TT-BGDĐT ngày 29 tháng 12 năm 2023 của Bộ trưởng Bộ Giáo dục và Đào tạo quy định về ứng dụng công nghệ thông tin trong đào tạo trực tuyến đối với giáo dục đại học hết hiệu lực thi hành từ ngày Thông tư này có hiệu lực. 3.
> [tt49-2026-ung-dung-cong-nghe-ai:by_sentences:023](https://luatvietnam.vn/giao-duc/thong-tu-49-2026-tt-bgddt-ung-dung-cong-nghe-trong-giao-duc-dai-hoc-va-nghe-nghiep-439350-d1.html)
> 
> # Thông tư 49/2026/TT-BGDĐT — Ứng dụng công nghệ và AI trong giáo dục đại học
> 
> Số: 49/2026/TT-BGDĐT — Hà Nội, ngày 30 tháng 06 năm 2026. Quy định ứng dụng công nghệ trong giáo dục đại học, giáo dục nghề nghiệp (trích các Điều liên quan đến trí tuệ nhân tạo và liêm chính học thuật). ## Điều 1.
> [tt49-2026-ung-dung-cong-nghe-ai:by_sentences:000](https://luatvietnam.vn/giao-duc/thong-tu-49-2026-tt-bgddt-ung-dung-cong-nghe-trong-giao-duc-dai-hoc-va-nghe-nghiep-439350-d1.html)


## tfidf / recursive

### Q1: Theo quy định của UEH, tỷ lệ tương đồng từ bao nhiêu phần trăm thì sản phẩm học thuật bị xem là có dấu hiệu đạo văn?

Filter: `null`; Hit@3: False; coverage: 0%.

Gold: Theo snapshot UEH, tỷ lệ tương đồng từ 20% trở lên là một dấu hiệu định lượng, sau khi loại các phần được miễn trừ nêu trong quy định; không tự động kết luận đạo văn chỉ từ tỷ lệ này.

1. `ueh-dao-van-ai-quy-dinh-chung:recursive:002` — score 0.5520; relevant=False

> Tỷ lệ tương đồng học thuật là tỷ lệ phần trăm nội dung trùng lặp trong sản phẩm học thuật được xác định bằng phần mềm hỗ trợ (Turnitin hoặc các công cụ kiểm tra đạo văn có chức năng so sánh với cơ sở dữ liệu học thuật rộng và cho phép phân tích chi tiết mức độ trùng lặp, được UEH phê duyệt sử dụng). Tỷ lệ tương đồng không phải là căn cứ duy nhất để kết luận đạo văn; việc đánh giá phải dựa trên xem xét chuyên môn của đơn vị quản lý, giảng viên hoặc hội đồng có thẩm quyền.
> 
> ### Các dấu hiệu của hành vi đạo văn hoặc vi phạm liêm chính học thuật
> 
> Sản phẩm học thuật có thể xem là có dấu hiệu vi phạm nếu có ít nhất một trong các biểu hiện sau:
> 
> a) Dấu hiệu định lượng từ phần mềm kiểm tra
> 
> 

2. `ueh-dao-van-ai-quy-dinh-chung:recursive:006` — score 0.3963; relevant=False

> 1. UEH sử dụng phần mềm Turnitin và/hoặc công cụ tương đương để phát hiện tỷ lệ tương đồng học thuật trong các sản phẩm học thuật. Kết quả tỷ lệ tương đồng chỉ mang tính tham khảo, hỗ trợ, không tự động kết luận là đạo văn. Việc kết luận dựa trên xem xét bối cảnh, phạm vi, tính chất nội dung trùng lặp, ý chí của người thực hiện và các chứng cứ liên quan. Việc đánh giá do giảng viên phụ trách/người hướng dẫn hoặc hội đồng/đơn vị có thẩm quyền thực hiện theo quy trình được UEH quy định.
> 
> 2. Xử lý hành vi đạo văn
> 
> ### 2.1 Nguyên tắc xử lý hành vi đạo văn
> 
> Việc xử lý được căn cứ trên mức độ nghiêm trọng, tính lặp lại và động cơ của hành vi:
> 
> 

3. `ueh-dao-van-ai-quy-dinh-chung:recursive:001` — score 0.3682; relevant=False

> Sản phẩm học thuật trong phạm vi điều chỉnh của Quy định bao gồm, nhưng không giới hạn: bài báo khoa học, báo cáo nghiên cứu khoa học, bài tham luận tại hội thảo, khóa luận tốt nghiệp, đề án tốt nghiệp, luận văn thạc sĩ, luận án tiến sĩ, bài tập, tiểu luận, chuyên đề và các dạng sản phẩm học thuật khác do UEH quy định hoặc công nhận.
> 
> ## Điều 2. Nhận diện và xác định hành vi đạo văn
> 
> ### Khái niệm đạo văn
> 
> Đạo văn là hành vi sử dụng trực tiếp hoặc gián tiếp, toàn bộ hoặc một phần ý tưởng, dữ liệu, ngôn từ, hình ảnh, mô hình, sản phẩm học thuật của người khác mà không ghi nhận, trích dẫn hoặc chú thích phù hợp; hoặc tái sử dụng sản phẩm học thuật của chính mình (tự đạo văn) mà không nêu rõ nguồn gốc và tình trạng công bố.
> 
> ### Tỷ lệ tương đồng học thuật
> 
> 

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> Tỷ lệ tương đồng học thuật là tỷ lệ phần trăm nội dung trùng lặp trong sản phẩm học thuật được xác định bằng phần mềm hỗ trợ (Turnitin hoặc các công cụ kiểm tra đạo văn có chức năng so sánh với cơ sở dữ liệu học thuật rộng và cho phép phân tích chi tiết mức độ trùng lặp, được UEH phê duyệt sử dụng). Tỷ lệ tương đồng không phải là căn cứ duy nhất để kết luận đạo văn; việc đánh giá phải dựa trên xem xét chuyên môn của đơn vị quản lý, giảng viên hoặc hội đồng có thẩm quyền.
> 
> ### Các dấu hiệu của hành vi đạo văn hoặc vi phạm liêm chính học thuật
> 
> Sản phẩm học thuật có thể xem là có dấu hiệu vi phạm nếu có ít nhất một trong các biểu hiện sau:
> 
> a) Dấu hiệu định lượng từ phần mềm kiểm tra
> [ueh-dao-van-ai-quy-dinh-chung:recursive:002](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
> 
> 1. UEH sử dụng phần mềm Turnitin và/hoặc công cụ tương đương để phát hiện tỷ lệ tương đồng học thuật trong các sản phẩm học thuật. Kết quả tỷ lệ tương đồng chỉ mang tính tham khảo, hỗ trợ, không tự động kết luận là đạo văn. Việc kết luận dựa trên xem xét bối cảnh, phạm vi, tính chất nội dung trùng lặp, ý chí của người thực hiện và các chứng cứ liên quan. Việc đánh giá do giảng viên phụ trách/người hướng dẫn hoặc hội đồng/đơn vị có thẩm quyền thực hiện theo quy trình được UEH quy định.
> 
> 2. Xử lý hành vi đạo văn
> 
> ### 2.1 Nguyên tắc xử lý hành vi đạo văn
> 
> Việc xử lý được căn cứ trên mức độ nghiêm trọng, tính lặp lại và động cơ của hành vi:
> [ueh-dao-van-ai-quy-dinh-chung:recursive:006](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
> 
> Sản phẩm học thuật trong phạm vi điều chỉnh của Quy định bao gồm, nhưng không giới hạn: bài báo khoa học, báo cáo nghiên cứu khoa học, bài tham luận tại hội thảo, khóa luận tốt nghiệp, đề án tốt nghiệp, luận văn thạc sĩ, luận án tiến sĩ, bài tập, tiểu luận, chuyên đề và các dạng sản phẩm học thuật khác do UEH quy định hoặc công nhận.
> 
> ## Điều 2. Nhận diện và xác định hành vi đạo văn
> 
> ### Khái niệm đạo văn
> 
> Đạo văn là hành vi sử dụng trực tiếp hoặc gián tiếp, toàn bộ hoặc một phần ý tưởng, dữ liệu, ngôn từ, hình ảnh, mô hình, sản phẩm học thuật của người khác mà không ghi nhận, trích dẫn hoặc chú thích phù hợp; hoặc tái sử dụng sản phẩm học thuật của chính mình (tự đạo văn) mà không nêu rõ nguồn gốc và tình trạng công bố.
> 
> ### Tỷ lệ tương đồng học thuật
> [ueh-dao-van-ai-quy-dinh-chung:recursive:001](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)


### Q2: Sản phẩm học thuật đã chỉnh sửa nhưng vẫn vi phạm lỗi đạo văn thì xử lý ra sao?

Filter: `{"audience": "student"}`; Hit@3: True; coverage: 100%.

Gold: Trong bối cảnh bài tập học phần của người học: giảng viên phụ trách lập biên bản/thông báo chuyển về đơn vị quản lý để xử lý tùy mức độ vi phạm quy định tại Phụ lục 3.

1. `ueh-xu-ly-vi-pham-nguoi-hoc:recursive:001` — score 0.4061; relevant=True

> Sau khi đã bảo vệ, nếu có phát hiện lỗi đạo văn, tác giả chịu trách nhiệm theo các quy định của UEH và pháp luật hiện hành.
> 
> ### 2.3 Đối với các bài kiểm tra, bài tập, tiểu luận và các bài khác thuộc các học phần
> 
> a) Khi bị phát hiện vi phạm lần đầu, người học phải chỉnh sửa và nộp lại bài theo yêu cầu của giảng viên;
> 
> b) Sau khi đã chỉnh sửa, người học nộp lại bài nhưng vẫn vi phạm lỗi đạo văn thì giảng viên phụ trách học phần lập biên bản/thông báo chuyển về đơn vị quản lý để xử lý tùy theo mức độ vi phạm quy định tại Phụ lục 3.
> 
> ## Điều 5. Xử lý vi phạm sử dụng AI trong học thuật — áp dụng cho người học
> 
> ### 2.1. Đối với khóa luận, đề án tốt nghiệp, luận văn, luận án
> 
> a) Trước khi bảo vệ:
> 
> 

2. `ueh-xu-ly-vi-pham-nguoi-hoc:recursive:003` — score 0.3727; relevant=True

> b) Nếu vẫn vi phạm sau khi đã chỉnh sửa, giảng viên phụ trách học phần lập biên bản, thông báo chuyển cho đơn vị quản lý để xử lý tùy theo mức độ vi phạm.
> 
> ## Điều 6. Tổ chức thực hiện — trách nhiệm của người học
> 
> ### Trách nhiệm của tác giả sản phẩm học thuật và người học tại UEH:
> 
> a) Thực hiện nghiêm túc các quy định về đạo văn và sử dụng AI trong học thuật.
> 
> b) Khuyến khích toàn thể người học, viên chức, người lao động của UEH thông báo và cung cấp những bằng chứng về những trường hợp nghi ngờ có hành vi đạo văn hoặc vi phạm sử dụng AI trong học thuật.

3. `ueh-xu-ly-vi-pham-nguoi-hoc:recursive:000` — score 0.3110; relevant=False

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
> Nếu Hội đồng đánh giá luận văn/luận án phát hiện hành vi đạo văn, chủ tịch hội đồng quyết định luận văn/luận án không đạt, người học phải chỉnh sửa lại sản phẩm và khắc phục lỗi đạo văn theo quy định của chương trình.
> 
> c) Sau bảo vệ:
> 
> 

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> Sau khi đã bảo vệ, nếu có phát hiện lỗi đạo văn, tác giả chịu trách nhiệm theo các quy định của UEH và pháp luật hiện hành.
> 
> ### 2.3 Đối với các bài kiểm tra, bài tập, tiểu luận và các bài khác thuộc các học phần
> 
> a) Khi bị phát hiện vi phạm lần đầu, người học phải chỉnh sửa và nộp lại bài theo yêu cầu của giảng viên;
> 
> b) Sau khi đã chỉnh sửa, người học nộp lại bài nhưng vẫn vi phạm lỗi đạo văn thì giảng viên phụ trách học phần lập biên bản/thông báo chuyển về đơn vị quản lý để xử lý tùy theo mức độ vi phạm quy định tại Phụ lục 3.
> 
> ## Điều 5. Xử lý vi phạm sử dụng AI trong học thuật — áp dụng cho người học
> 
> ### 2.1. Đối với khóa luận, đề án tốt nghiệp, luận văn, luận án
> 
> a) Trước khi bảo vệ:
> [ueh-xu-ly-vi-pham-nguoi-hoc:recursive:001](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
> 
> b) Nếu vẫn vi phạm sau khi đã chỉnh sửa, giảng viên phụ trách học phần lập biên bản, thông báo chuyển cho đơn vị quản lý để xử lý tùy theo mức độ vi phạm.
> 
> ## Điều 6. Tổ chức thực hiện — trách nhiệm của người học
> 
> ### Trách nhiệm của tác giả sản phẩm học thuật và người học tại UEH:
> 
> a) Thực hiện nghiêm túc các quy định về đạo văn và sử dụng AI trong học thuật.
> 
> b) Khuyến khích toàn thể người học, viên chức, người lao động của UEH thông báo và cung cấp những bằng chứng về những trường hợp nghi ngờ có hành vi đạo văn hoặc vi phạm sử dụng AI trong học thuật.
> [ueh-xu-ly-vi-pham-nguoi-hoc:recursive:003](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
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
> Nếu Hội đồng đánh giá luận văn/luận án phát hiện hành vi đạo văn, chủ tịch hội đồng quyết định luận văn/luận án không đạt, người học phải chỉnh sửa lại sản phẩm và khắc phục lỗi đạo văn theo quy định của chương trình.
> 
> c) Sau bảo vệ:
> [ueh-xu-ly-vi-pham-nguoi-hoc:recursive:000](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)


### Q3: Khi ghi nhận việc dùng công cụ AI trong bài làm, câu acknowledgement cần nêu những thông tin gì?

Filter: `null`; Hit@3: False; coverage: 0%.

Gold: Theo hướng dẫn RMIT Library: nêu cách sử dụng AI, tên công cụ và nhà phát triển, năm nội dung AI được người dùng tạo ra. Không bắt buộc phiên bản/ngày dùng trừ khi giảng viên yêu cầu.

1. `ueh-dao-van-ai-quy-dinh-chung:recursive:012` — score 0.2328; relevant=False

> - Minh bạch: ghi rõ công cụ AI tạo sinh đã sử dụng, mục đích sử dụng (tóm tắt, dịch thuật, tạo hình, viết mã v.v.) và những nội dung có sự hỗ trợ của AI tạo sinh trong sản phẩm học thuật. Việc khai báo cần thực hiện theo chuẩn, ví dụ: Trong phần Acknowledgement hoặc Phương pháp nghiên cứu ghi: “Một phần nội dung của sản phẩm này được hỗ trợ bởi ChatGPT (phiên bản …), sử dụng cho mục đích tóm tắt tài liệu/tham khảo ý tưởng/ngôn ngữ.”
> - Trung thực và trách nhiệm: tác giả chịu trách nhiệm về tính chính xác, độ tin cậy, chất lượng và liêm chính học thuật của những nội dung được AI cung cấp.
> 

2. `ueh-dao-van-ai-quy-dinh-chung:recursive:014` — score 0.2038; relevant=False

> a) Sử dụng nội dung do AI tạo ra nhưng không thông báo hoặc thông báo không đầy đủ việc sử dụng công cụ, phạm vi và vai trò của AI.
> 
> b) Sử dụng AI để tạo ra nội dung nhưng không kiểm tra, xác nhận nguồn hoặc độ chính xác.
> 
> c) Sử dụng AI để tạo ra toàn bộ hoặc phần lớn nội dung sản phẩm học thuật mà không có sự đóng góp đáng kể, thực chất và sáng tạo của tác giả.
> 
> d) Sử dụng AI để gian lận trong bài kiểm tra, bài thi.
> 
> e) Sử dụng AI để tạo dữ liệu giả hoặc làm sai lệch dữ liệu gốc.
> 
> f) Sử dụng AI để tạo trích dẫn giả hoặc tài liệu tham khảo không tồn tại.
> 
> g) Sử dụng AI trong những trường hợp UEH, giảng viên hoặc hội đồng chuyên môn quy định là không được phép.
> 
> 

3. `ueh-dao-van-ai-quy-dinh-chung:recursive:001` — score 0.1493; relevant=False

> Sản phẩm học thuật trong phạm vi điều chỉnh của Quy định bao gồm, nhưng không giới hạn: bài báo khoa học, báo cáo nghiên cứu khoa học, bài tham luận tại hội thảo, khóa luận tốt nghiệp, đề án tốt nghiệp, luận văn thạc sĩ, luận án tiến sĩ, bài tập, tiểu luận, chuyên đề và các dạng sản phẩm học thuật khác do UEH quy định hoặc công nhận.
> 
> ## Điều 2. Nhận diện và xác định hành vi đạo văn
> 
> ### Khái niệm đạo văn
> 
> Đạo văn là hành vi sử dụng trực tiếp hoặc gián tiếp, toàn bộ hoặc một phần ý tưởng, dữ liệu, ngôn từ, hình ảnh, mô hình, sản phẩm học thuật của người khác mà không ghi nhận, trích dẫn hoặc chú thích phù hợp; hoặc tái sử dụng sản phẩm học thuật của chính mình (tự đạo văn) mà không nêu rõ nguồn gốc và tình trạng công bố.
> 
> ### Tỷ lệ tương đồng học thuật
> 
> 

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> - Minh bạch: ghi rõ công cụ AI tạo sinh đã sử dụng, mục đích sử dụng (tóm tắt, dịch thuật, tạo hình, viết mã v.v.) và những nội dung có sự hỗ trợ của AI tạo sinh trong sản phẩm học thuật. Việc khai báo cần thực hiện theo chuẩn, ví dụ: Trong phần Acknowledgement hoặc Phương pháp nghiên cứu ghi: “Một phần nội dung của sản phẩm này được hỗ trợ bởi ChatGPT (phiên bản …), sử dụng cho mục đích tóm tắt tài liệu/tham khảo ý tưởng/ngôn ngữ.”
> - Trung thực và trách nhiệm: tác giả chịu trách nhiệm về tính chính xác, độ tin cậy, chất lượng và liêm chính học thuật của những nội dung được AI cung cấp.
> [ueh-dao-van-ai-quy-dinh-chung:recursive:012](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
> 
> a) Sử dụng nội dung do AI tạo ra nhưng không thông báo hoặc thông báo không đầy đủ việc sử dụng công cụ, phạm vi và vai trò của AI.
> 
> b) Sử dụng AI để tạo ra nội dung nhưng không kiểm tra, xác nhận nguồn hoặc độ chính xác.
> 
> c) Sử dụng AI để tạo ra toàn bộ hoặc phần lớn nội dung sản phẩm học thuật mà không có sự đóng góp đáng kể, thực chất và sáng tạo của tác giả.
> 
> d) Sử dụng AI để gian lận trong bài kiểm tra, bài thi.
> 
> e) Sử dụng AI để tạo dữ liệu giả hoặc làm sai lệch dữ liệu gốc.
> 
> f) Sử dụng AI để tạo trích dẫn giả hoặc tài liệu tham khảo không tồn tại.
> 
> g) Sử dụng AI trong những trường hợp UEH, giảng viên hoặc hội đồng chuyên môn quy định là không được phép.
> [ueh-dao-van-ai-quy-dinh-chung:recursive:014](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
> 
> Sản phẩm học thuật trong phạm vi điều chỉnh của Quy định bao gồm, nhưng không giới hạn: bài báo khoa học, báo cáo nghiên cứu khoa học, bài tham luận tại hội thảo, khóa luận tốt nghiệp, đề án tốt nghiệp, luận văn thạc sĩ, luận án tiến sĩ, bài tập, tiểu luận, chuyên đề và các dạng sản phẩm học thuật khác do UEH quy định hoặc công nhận.
> 
> ## Điều 2. Nhận diện và xác định hành vi đạo văn
> 
> ### Khái niệm đạo văn
> 
> Đạo văn là hành vi sử dụng trực tiếp hoặc gián tiếp, toàn bộ hoặc một phần ý tưởng, dữ liệu, ngôn từ, hình ảnh, mô hình, sản phẩm học thuật của người khác mà không ghi nhận, trích dẫn hoặc chú thích phù hợp; hoặc tái sử dụng sản phẩm học thuật của chính mình (tự đạo văn) mà không nêu rõ nguồn gốc và tình trạng công bố.
> 
> ### Tỷ lệ tương đồng học thuật
> [ueh-dao-van-ai-quy-dinh-chung:recursive:001](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)


### Q4: Những loại thông tin nào không được phép nhập vào công cụ AI tạo sinh?

Filter: `null`; Hit@3: False; coverage: 0%.

Gold: Theo snapshot UNA, không nhập thông tin cá nhân, bí mật, độc quyền hoặc nhạy cảm: ví dụ hồ sơ sinh viên/tuyển sinh, số an sinh xã hội, dữ liệu thẻ/ngân hàng, giấy tờ định danh, dữ liệu y tế/bảo hiểm, dữ liệu người tham gia nghiên cứu chưa được đồng ý công khai, hồ sơ nội bộ và nội dung thuộc NDA/sở hữu trí tuệ chưa được phép. Danh sách ví dụ không giới hạn ở một loại dữ liệu.

1. `ueh-dao-van-ai-quy-dinh-chung:recursive:013` — score 0.2618; relevant=False

> - Tôn trọng quyền riêng tư, sở hữu trí tuệ và bảo mật dữ liệu: không cung cấp cho AI dữ liệu cá nhân, dữ liệu mật, thông tin chưa công bố hoặc dữ liệu nghiên cứu nội bộ của UEH hoặc đối tác nếu chưa được phép.
> - Không lạm dụng: không sử dụng AI để thay thế nhiệm vụ học thuật mà người học hoặc giảng viên phải tự thực hiện. AI chỉ đóng vai trò hỗ trợ. Khuyến khích người học và giảng viên sử dụng có trách nhiệm và không phụ thuộc hoàn toàn vào công cụ.
> - Đối với AI hỗ trợ, không bắt buộc thông báo nếu chỉ sử dụng để kiểm tra ngôn ngữ, chỉnh lỗi chính tả, ngữ pháp hoặc dịch thuật trực tiếp không mang tính sáng tạo nội dung.
> 3. Những hành vi bị xem là vi phạm quy tắc sử dụng AI trong học thuật:
> 
> 

2. `ueh-dao-van-ai-quy-dinh-chung:recursive:008` — score 0.2594; relevant=False

> 1. Trong Quy định này, trí tuệ nhân tạo (AI) được hiểu là các công cụ, hệ thống hoặc thuật toán có khả năng tạo, phân tích hoặc xử lý nội dung hỗ trợ hoạt động học thuật. AI được xem là công cụ hỗ trợ, không thay thế trách nhiệm tư duy, phân tích và sáng tạo của tác giả. 

3. `ueh-dao-van-ai-quy-dinh-chung:recursive:014` — score 0.2569; relevant=False

> a) Sử dụng nội dung do AI tạo ra nhưng không thông báo hoặc thông báo không đầy đủ việc sử dụng công cụ, phạm vi và vai trò của AI.
> 
> b) Sử dụng AI để tạo ra nội dung nhưng không kiểm tra, xác nhận nguồn hoặc độ chính xác.
> 
> c) Sử dụng AI để tạo ra toàn bộ hoặc phần lớn nội dung sản phẩm học thuật mà không có sự đóng góp đáng kể, thực chất và sáng tạo của tác giả.
> 
> d) Sử dụng AI để gian lận trong bài kiểm tra, bài thi.
> 
> e) Sử dụng AI để tạo dữ liệu giả hoặc làm sai lệch dữ liệu gốc.
> 
> f) Sử dụng AI để tạo trích dẫn giả hoặc tài liệu tham khảo không tồn tại.
> 
> g) Sử dụng AI trong những trường hợp UEH, giảng viên hoặc hội đồng chuyên môn quy định là không được phép.
> 
> 

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> - Tôn trọng quyền riêng tư, sở hữu trí tuệ và bảo mật dữ liệu: không cung cấp cho AI dữ liệu cá nhân, dữ liệu mật, thông tin chưa công bố hoặc dữ liệu nghiên cứu nội bộ của UEH hoặc đối tác nếu chưa được phép.
> - Không lạm dụng: không sử dụng AI để thay thế nhiệm vụ học thuật mà người học hoặc giảng viên phải tự thực hiện. AI chỉ đóng vai trò hỗ trợ. Khuyến khích người học và giảng viên sử dụng có trách nhiệm và không phụ thuộc hoàn toàn vào công cụ.
> - Đối với AI hỗ trợ, không bắt buộc thông báo nếu chỉ sử dụng để kiểm tra ngôn ngữ, chỉnh lỗi chính tả, ngữ pháp hoặc dịch thuật trực tiếp không mang tính sáng tạo nội dung.
> 3. Những hành vi bị xem là vi phạm quy tắc sử dụng AI trong học thuật:
> [ueh-dao-van-ai-quy-dinh-chung:recursive:013](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
> 
> 1. Trong Quy định này, trí tuệ nhân tạo (AI) được hiểu là các công cụ, hệ thống hoặc thuật toán có khả năng tạo, phân tích hoặc xử lý nội dung hỗ trợ hoạt động học thuật. AI được xem là công cụ hỗ trợ, không thay thế trách nhiệm tư duy, phân tích và sáng tạo của tác giả.
> [ueh-dao-van-ai-quy-dinh-chung:recursive:008](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
> 
> a) Sử dụng nội dung do AI tạo ra nhưng không thông báo hoặc thông báo không đầy đủ việc sử dụng công cụ, phạm vi và vai trò của AI.
> 
> b) Sử dụng AI để tạo ra nội dung nhưng không kiểm tra, xác nhận nguồn hoặc độ chính xác.
> 
> c) Sử dụng AI để tạo ra toàn bộ hoặc phần lớn nội dung sản phẩm học thuật mà không có sự đóng góp đáng kể, thực chất và sáng tạo của tác giả.
> 
> d) Sử dụng AI để gian lận trong bài kiểm tra, bài thi.
> 
> e) Sử dụng AI để tạo dữ liệu giả hoặc làm sai lệch dữ liệu gốc.
> 
> f) Sử dụng AI để tạo trích dẫn giả hoặc tài liệu tham khảo không tồn tại.
> 
> g) Sử dụng AI trong những trường hợp UEH, giảng viên hoặc hội đồng chuyên môn quy định là không được phép.
> [ueh-dao-van-ai-quy-dinh-chung:recursive:014](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)


### Q5: Thông tư 49/2026/TT-BGDĐT có hiệu lực từ ngày nào và thay thế những thông tư nào?

Filter: `null`; Hit@3: True; coverage: 100%.

Gold: Theo Điều 22 trong snapshot nhóm cung cấp: hiệu lực từ 15/08/2026; Thông tư 15/2018/TT-BGDĐT và 30/2023/TT-BGDĐT hết hiệu lực từ ngày đó. Đây là gold answer kiểm thử snapshot, chưa xác minh tình trạng pháp lý hiện hành.

1. `tt49-2026-ung-dung-cong-nghe-ai:recursive:017` — score 0.3953; relevant=True

> 1. Thông tư này có hiệu lực thi hành kể từ ngày 15 tháng 08 năm 2026.
> 
> 2. Thông tư số 15/2018/TT-BGDĐT ngày 27 tháng 7 năm 2018 của Bộ trưởng Bộ Giáo dục và Đào tạo quy định tổ chức hoạt động, sử dụng thư điện tử và trang thông tin điện tử của các cơ sở giáo dục đại học, các trường cao đẳng sư phạm; Thông tư số 30/2023/TT-BGDĐT ngày 29 tháng 12 năm 2023 của Bộ trưởng Bộ Giáo dục và Đào tạo quy định về ứng dụng công nghệ thông tin trong đào tạo trực tuyến đối với giáo dục đại học hết hiệu lực thi hành từ ngày Thông tư này có hiệu lực.
> 
> 

2. `tt49-2026-ung-dung-cong-nghe-ai:recursive:000` — score 0.2974; relevant=False

> # Thông tư 49/2026/TT-BGDĐT — Ứng dụng công nghệ và AI trong giáo dục đại học
> 
> Số: 49/2026/TT-BGDĐT — Hà Nội, ngày 30 tháng 06 năm 2026.
> 
> Quy định ứng dụng công nghệ trong giáo dục đại học, giáo dục nghề nghiệp (trích các Điều liên quan đến trí tuệ nhân tạo và liêm chính học thuật).
> 
> ## Điều 1. Phạm vi điều chỉnh
> 
> Thông tư này quy định về ứng dụng công nghệ trong giáo dục đại học, giáo dục nghề nghiệp bao gồm: nguyên tắc, nội dung và điều kiện bảo đảm việc ứng dụng công nghệ số, trí tuệ nhân tạo và các công nghệ có liên quan trong hoạt động đào tạo, nghiên cứu khoa học, quản trị và cung cấp dịch vụ phục vụ người học tại cơ sở giáo dục đại học, cơ sở giáo dục nghề nghiệp.
> 
> ## Điều 2. Đối tượng áp dụng
> 
> Thông tư này áp dụng với:
> 
> 

3. `tt49-2026-ung-dung-cong-nghe-ai:recursive:018` — score 0.1809; relevant=False

> 3. Chánh Văn phòng, Cục trưởng Cục Khoa học, Công nghệ và Thông tin, Thủ trưởng các đơn vị thuộc Bộ Giáo dục và Đào tạo, Giám đốc các đại học, học viện, Hiệu trưởng các trường đại học, Hiệu trưởng các trường cao đẳng, Giám đốc các sở Giáo dục và Đào tạo và các tổ chức, cá nhân có liên quan chịu trách nhiệm thi hành Thông tư này./.

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> 1. Thông tư này có hiệu lực thi hành kể từ ngày 15 tháng 08 năm 2026.
> 
> 2. Thông tư số 15/2018/TT-BGDĐT ngày 27 tháng 7 năm 2018 của Bộ trưởng Bộ Giáo dục và Đào tạo quy định tổ chức hoạt động, sử dụng thư điện tử và trang thông tin điện tử của các cơ sở giáo dục đại học, các trường cao đẳng sư phạm; Thông tư số 30/2023/TT-BGDĐT ngày 29 tháng 12 năm 2023 của Bộ trưởng Bộ Giáo dục và Đào tạo quy định về ứng dụng công nghệ thông tin trong đào tạo trực tuyến đối với giáo dục đại học hết hiệu lực thi hành từ ngày Thông tư này có hiệu lực.
> [tt49-2026-ung-dung-cong-nghe-ai:recursive:017](https://luatvietnam.vn/giao-duc/thong-tu-49-2026-tt-bgddt-ung-dung-cong-nghe-trong-giao-duc-dai-hoc-va-nghe-nghiep-439350-d1.html)
> 
> # Thông tư 49/2026/TT-BGDĐT — Ứng dụng công nghệ và AI trong giáo dục đại học
> 
> Số: 49/2026/TT-BGDĐT — Hà Nội, ngày 30 tháng 06 năm 2026.
> 
> Quy định ứng dụng công nghệ trong giáo dục đại học, giáo dục nghề nghiệp (trích các Điều liên quan đến trí tuệ nhân tạo và liêm chính học thuật).
> 
> ## Điều 1. Phạm vi điều chỉnh
> 
> Thông tư này quy định về ứng dụng công nghệ trong giáo dục đại học, giáo dục nghề nghiệp bao gồm: nguyên tắc, nội dung và điều kiện bảo đảm việc ứng dụng công nghệ số, trí tuệ nhân tạo và các công nghệ có liên quan trong hoạt động đào tạo, nghiên cứu khoa học, quản trị và cung cấp dịch vụ phục vụ người học tại cơ sở giáo dục đại học, cơ sở giáo dục nghề nghiệp.
> 
> ## Điều 2. Đối tượng áp dụng
> 
> Thông tư này áp dụng với:
> [tt49-2026-ung-dung-cong-nghe-ai:recursive:000](https://luatvietnam.vn/giao-duc/thong-tu-49-2026-tt-bgddt-ung-dung-cong-nghe-trong-giao-duc-dai-hoc-va-nghe-nghiep-439350-d1.html)
> 
> 3. Chánh Văn phòng, Cục trưởng Cục Khoa học, Công nghệ và Thông tin, Thủ trưởng các đơn vị thuộc Bộ Giáo dục và Đào tạo, Giám đốc các đại học, học viện, Hiệu trưởng các trường đại học, Hiệu trưởng các trường cao đẳng, Giám đốc các sở Giáo dục và Đào tạo và các tổ chức, cá nhân có liên quan chịu trách nhiệm thi hành Thông tư này./.
> [tt49-2026-ung-dung-cong-nghe-ai:recursive:018](https://luatvietnam.vn/giao-duc/thong-tu-49-2026-tt-bgddt-ung-dung-cong-nghe-trong-giao-duc-dai-hoc-va-nghe-nghiep-439350-d1.html)


## tfidf / heading

### Q1: Theo quy định của UEH, tỷ lệ tương đồng từ bao nhiêu phần trăm thì sản phẩm học thuật bị xem là có dấu hiệu đạo văn?

Filter: `null`; Hit@3: True; coverage: 100%.

Gold: Theo snapshot UEH, tỷ lệ tương đồng từ 20% trở lên là một dấu hiệu định lượng, sau khi loại các phần được miễn trừ nêu trong quy định; không tự động kết luận đạo văn chỉ từ tỷ lệ này.

1. `ueh-dao-van-ai-quy-dinh-chung:heading:004` — score 0.5090; relevant=False

> # UEH — Quy định kiểm soát đạo văn và sử dụng AI: quy định chung
> ## Điều 2. Nhận diện và xác định hành vi đạo văn
> ### Tỷ lệ tương đồng học thuật
> 
> Tỷ lệ tương đồng học thuật là tỷ lệ phần trăm nội dung trùng lặp trong sản phẩm học thuật được xác định bằng phần mềm hỗ trợ (Turnitin hoặc các công cụ kiểm tra đạo văn có chức năng so sánh với cơ sở dữ liệu học thuật rộng và cho phép phân tích chi tiết mức độ trùng lặp, được UEH phê duyệt sử dụng). Tỷ lệ tương đồng không phải là căn cứ duy nhất để kết luận đạo văn; việc đánh giá phải dựa trên xem xét chuyên môn của đơn vị quản lý, giảng viên hoặc hội đồng có thẩm quyền.

2. `ueh-dao-van-ai-quy-dinh-chung:heading:005` — score 0.4734; relevant=True

> # UEH — Quy định kiểm soát đạo văn và sử dụng AI: quy định chung
> ## Điều 2. Nhận diện và xác định hành vi đạo văn
> ### Các dấu hiệu của hành vi đạo văn hoặc vi phạm liêm chính học thuật
> 
> Sản phẩm học thuật có thể xem là có dấu hiệu vi phạm nếu có ít nhất một trong các biểu hiện sau:
> 
> a) Dấu hiệu định lượng từ phần mềm kiểm tra
> 
> - Có tỷ lệ tương đồng từ 20% trở lên (không tính phần: trích dẫn, danh mục tài liệu tham khảo, phần mô tả phương pháp mang tính lặp lại và phổ biến trong chuyên ngành, các thuật ngữ chuyên ngành, tiêu chuẩn kỹ thuật, trích dẫn văn bản quy phạm pháp luật, tên riêng không thể thay thế).
> b) Sử dụng sản phẩm của người khác mà không ghi nguồn
> 
> 

3. `ueh-dao-van-ai-quy-dinh-chung:heading:008` — score 0.4382; relevant=False

> # UEH — Quy định kiểm soát đạo văn và sử dụng AI: quy định chung
> ## Điều 3. Phát hiện và xử lý hành vi đạo văn
> 
> 1. UEH sử dụng phần mềm Turnitin và/hoặc công cụ tương đương để phát hiện tỷ lệ tương đồng học thuật trong các sản phẩm học thuật. Kết quả tỷ lệ tương đồng chỉ mang tính tham khảo, hỗ trợ, không tự động kết luận là đạo văn. Việc kết luận dựa trên xem xét bối cảnh, phạm vi, tính chất nội dung trùng lặp, ý chí của người thực hiện và các chứng cứ liên quan. Việc đánh giá do giảng viên phụ trách/người hướng dẫn hoặc hội đồng/đơn vị có thẩm quyền thực hiện theo quy trình được UEH quy định.
> 
> 2. Xử lý hành vi đạo văn

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> # UEH — Quy định kiểm soát đạo văn và sử dụng AI: quy định chung
> ## Điều 2. Nhận diện và xác định hành vi đạo văn
> ### Tỷ lệ tương đồng học thuật
> 
> Tỷ lệ tương đồng học thuật là tỷ lệ phần trăm nội dung trùng lặp trong sản phẩm học thuật được xác định bằng phần mềm hỗ trợ (Turnitin hoặc các công cụ kiểm tra đạo văn có chức năng so sánh với cơ sở dữ liệu học thuật rộng và cho phép phân tích chi tiết mức độ trùng lặp, được UEH phê duyệt sử dụng). Tỷ lệ tương đồng không phải là căn cứ duy nhất để kết luận đạo văn; việc đánh giá phải dựa trên xem xét chuyên môn của đơn vị quản lý, giảng viên hoặc hội đồng có thẩm quyền.
> [ueh-dao-van-ai-quy-dinh-chung:heading:004](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
> 
> # UEH — Quy định kiểm soát đạo văn và sử dụng AI: quy định chung
> ## Điều 2. Nhận diện và xác định hành vi đạo văn
> ### Các dấu hiệu của hành vi đạo văn hoặc vi phạm liêm chính học thuật
> 
> Sản phẩm học thuật có thể xem là có dấu hiệu vi phạm nếu có ít nhất một trong các biểu hiện sau:
> 
> a) Dấu hiệu định lượng từ phần mềm kiểm tra
> 
> - Có tỷ lệ tương đồng từ 20% trở lên (không tính phần: trích dẫn, danh mục tài liệu tham khảo, phần mô tả phương pháp mang tính lặp lại và phổ biến trong chuyên ngành, các thuật ngữ chuyên ngành, tiêu chuẩn kỹ thuật, trích dẫn văn bản quy phạm pháp luật, tên riêng không thể thay thế).
> b) Sử dụng sản phẩm của người khác mà không ghi nguồn
> [ueh-dao-van-ai-quy-dinh-chung:heading:005](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
> 
> # UEH — Quy định kiểm soát đạo văn và sử dụng AI: quy định chung
> ## Điều 3. Phát hiện và xử lý hành vi đạo văn
> 
> 1. UEH sử dụng phần mềm Turnitin và/hoặc công cụ tương đương để phát hiện tỷ lệ tương đồng học thuật trong các sản phẩm học thuật. Kết quả tỷ lệ tương đồng chỉ mang tính tham khảo, hỗ trợ, không tự động kết luận là đạo văn. Việc kết luận dựa trên xem xét bối cảnh, phạm vi, tính chất nội dung trùng lặp, ý chí của người thực hiện và các chứng cứ liên quan. Việc đánh giá do giảng viên phụ trách/người hướng dẫn hoặc hội đồng/đơn vị có thẩm quyền thực hiện theo quy trình được UEH quy định.
> 
> 2. Xử lý hành vi đạo văn
> [ueh-dao-van-ai-quy-dinh-chung:heading:008](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)


### Q2: Sản phẩm học thuật đã chỉnh sửa nhưng vẫn vi phạm lỗi đạo văn thì xử lý ra sao?

Filter: `{"audience": "student"}`; Hit@3: True; coverage: 100%.

Gold: Trong bối cảnh bài tập học phần của người học: giảng viên phụ trách lập biên bản/thông báo chuyển về đơn vị quản lý để xử lý tùy mức độ vi phạm quy định tại Phụ lục 3.

1. `ueh-xu-ly-vi-pham-nguoi-hoc:heading:002` — score 0.4437; relevant=True

> # UEH — Xử lý vi phạm đạo văn và sử dụng AI đối với người học
> ## Điều 3. Xử lý hành vi đạo văn — áp dụng cho người học
> ### 2.3 Đối với các bài kiểm tra, bài tập, tiểu luận và các bài khác thuộc các học phần
> 
> a) Khi bị phát hiện vi phạm lần đầu, người học phải chỉnh sửa và nộp lại bài theo yêu cầu của giảng viên;
> 
> b) Sau khi đã chỉnh sửa, người học nộp lại bài nhưng vẫn vi phạm lỗi đạo văn thì giảng viên phụ trách học phần lập biên bản/thông báo chuyển về đơn vị quản lý để xử lý tùy theo mức độ vi phạm quy định tại Phụ lục 3.

2. `ueh-xu-ly-vi-pham-nguoi-hoc:heading:005` — score 0.3701; relevant=True

> # UEH — Xử lý vi phạm đạo văn và sử dụng AI đối với người học
> ## Điều 5. Xử lý vi phạm sử dụng AI trong học thuật — áp dụng cho người học
> ### 2.2. Đối với các bài kiểm tra, bài tập, tiểu luận, đồ án, dự án và các bài khác thuộc học phần
> 
> a) Khi bị phát hiện vi phạm lần đầu, người học phải chỉnh sửa và nộp lại bài theo yêu cầu của giảng viên;
> 
> b) Nếu vẫn vi phạm sau khi đã chỉnh sửa, giảng viên phụ trách học phần lập biên bản, thông báo chuyển cho đơn vị quản lý để xử lý tùy theo mức độ vi phạm.

3. `ueh-xu-ly-vi-pham-nguoi-hoc:heading:001` — score 0.3357; relevant=False

> # UEH — Xử lý vi phạm đạo văn và sử dụng AI đối với người học
> ## Điều 3. Xử lý hành vi đạo văn — áp dụng cho người học
> ### 2.2 Đối với khóa luận, đề án tốt nghiệp, luận văn, luận án
> 
> a) Trước khi bảo vệ:
> 
> Khi phát hiện có dấu hiệu đạo văn, người học phải chỉnh sửa, bổ sung và khắc phục theo yêu cầu của giảng viên hướng dẫn hoặc đơn vị quản lý.
> 
> b) Trong khi bảo vệ:
> 
> Nếu Hội đồng đánh giá luận văn/luận án phát hiện hành vi đạo văn, chủ tịch hội đồng quyết định luận văn/luận án không đạt, người học phải chỉnh sửa lại sản phẩm và khắc phục lỗi đạo văn theo quy định của chương trình.
> 
> c) Sau bảo vệ:
> 
> Sau khi đã bảo vệ, nếu có phát hiện lỗi đạo văn, tác giả chịu trách nhiệm theo các quy định của UEH và pháp luật hiện hành.

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> # UEH — Xử lý vi phạm đạo văn và sử dụng AI đối với người học
> ## Điều 3. Xử lý hành vi đạo văn — áp dụng cho người học
> ### 2.3 Đối với các bài kiểm tra, bài tập, tiểu luận và các bài khác thuộc các học phần
> 
> a) Khi bị phát hiện vi phạm lần đầu, người học phải chỉnh sửa và nộp lại bài theo yêu cầu của giảng viên;
> 
> b) Sau khi đã chỉnh sửa, người học nộp lại bài nhưng vẫn vi phạm lỗi đạo văn thì giảng viên phụ trách học phần lập biên bản/thông báo chuyển về đơn vị quản lý để xử lý tùy theo mức độ vi phạm quy định tại Phụ lục 3.
> [ueh-xu-ly-vi-pham-nguoi-hoc:heading:002](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
> 
> # UEH — Xử lý vi phạm đạo văn và sử dụng AI đối với người học
> ## Điều 5. Xử lý vi phạm sử dụng AI trong học thuật — áp dụng cho người học
> ### 2.2. Đối với các bài kiểm tra, bài tập, tiểu luận, đồ án, dự án và các bài khác thuộc học phần
> 
> a) Khi bị phát hiện vi phạm lần đầu, người học phải chỉnh sửa và nộp lại bài theo yêu cầu của giảng viên;
> 
> b) Nếu vẫn vi phạm sau khi đã chỉnh sửa, giảng viên phụ trách học phần lập biên bản, thông báo chuyển cho đơn vị quản lý để xử lý tùy theo mức độ vi phạm.
> [ueh-xu-ly-vi-pham-nguoi-hoc:heading:005](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
> 
> # UEH — Xử lý vi phạm đạo văn và sử dụng AI đối với người học
> ## Điều 3. Xử lý hành vi đạo văn — áp dụng cho người học
> ### 2.2 Đối với khóa luận, đề án tốt nghiệp, luận văn, luận án
> 
> a) Trước khi bảo vệ:
> 
> Khi phát hiện có dấu hiệu đạo văn, người học phải chỉnh sửa, bổ sung và khắc phục theo yêu cầu của giảng viên hướng dẫn hoặc đơn vị quản lý.
> 
> b) Trong khi bảo vệ:
> 
> Nếu Hội đồng đánh giá luận văn/luận án phát hiện hành vi đạo văn, chủ tịch hội đồng quyết định luận văn/luận án không đạt, người học phải chỉnh sửa lại sản phẩm và khắc phục lỗi đạo văn theo quy định của chương trình.
> 
> c) Sau bảo vệ:
> 
> Sau khi đã bảo vệ, nếu có phát hiện lỗi đạo văn, tác giả chịu trách nhiệm theo các quy định của UEH và pháp luật hiện hành.
> [ueh-xu-ly-vi-pham-nguoi-hoc:heading:001](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)


### Q3: Khi ghi nhận việc dùng công cụ AI trong bài làm, câu acknowledgement cần nêu những thông tin gì?

Filter: `null`; Hit@3: False; coverage: 0%.

Gold: Theo hướng dẫn RMIT Library: nêu cách sử dụng AI, tên công cụ và nhà phát triển, năm nội dung AI được người dùng tạo ra. Không bắt buộc phiên bản/ngày dùng trừ khi giảng viên yêu cầu.

1. `ueh-dao-van-ai-quy-dinh-chung:heading:014` — score 0.2268; relevant=False

> # UEH — Quy định kiểm soát đạo văn và sử dụng AI: quy định chung
> ## Điều 4. Sử dụng AI trong học thuật
> 
> - Minh bạch: ghi rõ công cụ AI tạo sinh đã sử dụng, mục đích sử dụng (tóm tắt, dịch thuật, tạo hình, viết mã v.v.) và những nội dung có sự hỗ trợ của AI tạo sinh trong sản phẩm học thuật. Việc khai báo cần thực hiện theo chuẩn, ví dụ: Trong phần Acknowledgement hoặc Phương pháp nghiên cứu ghi: “Một phần nội dung của sản phẩm này được hỗ trợ bởi ChatGPT (phiên bản …), sử dụng cho mục đích tóm tắt tài liệu/tham khảo ý tưởng/ngôn ngữ.”
> - Trung thực và trách nhiệm: tác giả chịu trách nhiệm về tính chính xác, độ tin cậy, chất lượng và liêm chính học thuật của những nội dung được AI cung cấp.
> 

2. `ueh-dao-van-ai-quy-dinh-chung:heading:017` — score 0.1978; relevant=False

> # UEH — Quy định kiểm soát đạo văn và sử dụng AI: quy định chung
> ## Điều 4. Sử dụng AI trong học thuật
> 
> a) Sử dụng nội dung do AI tạo ra nhưng không thông báo hoặc thông báo không đầy đủ việc sử dụng công cụ, phạm vi và vai trò của AI.
> 
> b) Sử dụng AI để tạo ra nội dung nhưng không kiểm tra, xác nhận nguồn hoặc độ chính xác.
> 
> c) Sử dụng AI để tạo ra toàn bộ hoặc phần lớn nội dung sản phẩm học thuật mà không có sự đóng góp đáng kể, thực chất và sáng tạo của tác giả.
> 
> d) Sử dụng AI để gian lận trong bài kiểm tra, bài thi.
> 
> e) Sử dụng AI để tạo dữ liệu giả hoặc làm sai lệch dữ liệu gốc.
> 
> f) Sử dụng AI để tạo trích dẫn giả hoặc tài liệu tham khảo không tồn tại.
> 
> g) Sử dụng AI trong những trường hợp UEH, giảng viên hoặc hội đồng chuyên môn quy định là không được phép.
> 
> 

3. `tt49-2026-ung-dung-cong-nghe-ai:heading:016` — score 0.1549; relevant=False

> # Thông tư 49/2026/TT-BGDĐT — Ứng dụng công nghệ và AI trong giáo dục đại học
> ## Điều 10. Bảo đảm liêm chính học thuật khi ứng dụng công nghệ
> 
> b) Sao chép, đạo văn, sử dụng trái phép tài liệu, dữ liệu, học liệu số hoặc kết quả nghiên cứu;
> 
> c) Giả mạo, làm sai lệch dữ liệu, kết quả nghiên cứu hoặc thông tin học tập;
> 
> d) Nhờ người khác thực hiện hoặc thực hiện thay các nhiệm vụ học tập, kiểm tra, đánh giá hoặc nghiên cứu;
> 
> đ) Không công bố hoặc công bố không đầy đủ việc sử dụng công nghệ, trí tuệ nhân tạo khi có yêu cầu theo quy định nội bộ của cơ sở giáo dục và pháp luật của Nhà nước;
> 
> e) Các hành vi khác vi phạm quy định về liêm chính học thuật theo quy định của pháp luật và quy chế của cơ sở giáo dục.
> 
> 3. Trách nhiệm của các bên liên quan
> 
> 

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> # UEH — Quy định kiểm soát đạo văn và sử dụng AI: quy định chung
> ## Điều 4. Sử dụng AI trong học thuật
> 
> - Minh bạch: ghi rõ công cụ AI tạo sinh đã sử dụng, mục đích sử dụng (tóm tắt, dịch thuật, tạo hình, viết mã v.v.) và những nội dung có sự hỗ trợ của AI tạo sinh trong sản phẩm học thuật. Việc khai báo cần thực hiện theo chuẩn, ví dụ: Trong phần Acknowledgement hoặc Phương pháp nghiên cứu ghi: “Một phần nội dung của sản phẩm này được hỗ trợ bởi ChatGPT (phiên bản …), sử dụng cho mục đích tóm tắt tài liệu/tham khảo ý tưởng/ngôn ngữ.”
> - Trung thực và trách nhiệm: tác giả chịu trách nhiệm về tính chính xác, độ tin cậy, chất lượng và liêm chính học thuật của những nội dung được AI cung cấp.
> [ueh-dao-van-ai-quy-dinh-chung:heading:014](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
> 
> # UEH — Quy định kiểm soát đạo văn và sử dụng AI: quy định chung
> ## Điều 4. Sử dụng AI trong học thuật
> 
> a) Sử dụng nội dung do AI tạo ra nhưng không thông báo hoặc thông báo không đầy đủ việc sử dụng công cụ, phạm vi và vai trò của AI.
> 
> b) Sử dụng AI để tạo ra nội dung nhưng không kiểm tra, xác nhận nguồn hoặc độ chính xác.
> 
> c) Sử dụng AI để tạo ra toàn bộ hoặc phần lớn nội dung sản phẩm học thuật mà không có sự đóng góp đáng kể, thực chất và sáng tạo của tác giả.
> 
> d) Sử dụng AI để gian lận trong bài kiểm tra, bài thi.
> 
> e) Sử dụng AI để tạo dữ liệu giả hoặc làm sai lệch dữ liệu gốc.
> 
> f) Sử dụng AI để tạo trích dẫn giả hoặc tài liệu tham khảo không tồn tại.
> 
> g) Sử dụng AI trong những trường hợp UEH, giảng viên hoặc hội đồng chuyên môn quy định là không được phép.
> [ueh-dao-van-ai-quy-dinh-chung:heading:017](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
> 
> # Thông tư 49/2026/TT-BGDĐT — Ứng dụng công nghệ và AI trong giáo dục đại học
> ## Điều 10. Bảo đảm liêm chính học thuật khi ứng dụng công nghệ
> 
> b) Sao chép, đạo văn, sử dụng trái phép tài liệu, dữ liệu, học liệu số hoặc kết quả nghiên cứu;
> 
> c) Giả mạo, làm sai lệch dữ liệu, kết quả nghiên cứu hoặc thông tin học tập;
> 
> d) Nhờ người khác thực hiện hoặc thực hiện thay các nhiệm vụ học tập, kiểm tra, đánh giá hoặc nghiên cứu;
> 
> đ) Không công bố hoặc công bố không đầy đủ việc sử dụng công nghệ, trí tuệ nhân tạo khi có yêu cầu theo quy định nội bộ của cơ sở giáo dục và pháp luật của Nhà nước;
> 
> e) Các hành vi khác vi phạm quy định về liêm chính học thuật theo quy định của pháp luật và quy chế của cơ sở giáo dục.
> 
> 3. Trách nhiệm của các bên liên quan
> [tt49-2026-ung-dung-cong-nghe-ai:heading:016](https://luatvietnam.vn/giao-duc/thong-tu-49-2026-tt-bgddt-ung-dung-cong-nghe-trong-giao-duc-dai-hoc-va-nghe-nghiep-439350-d1.html)


### Q4: Những loại thông tin nào không được phép nhập vào công cụ AI tạo sinh?

Filter: `null`; Hit@3: False; coverage: 0%.

Gold: Theo snapshot UNA, không nhập thông tin cá nhân, bí mật, độc quyền hoặc nhạy cảm: ví dụ hồ sơ sinh viên/tuyển sinh, số an sinh xã hội, dữ liệu thẻ/ngân hàng, giấy tờ định danh, dữ liệu y tế/bảo hiểm, dữ liệu người tham gia nghiên cứu chưa được đồng ý công khai, hồ sơ nội bộ và nội dung thuộc NDA/sở hữu trí tuệ chưa được phép. Danh sách ví dụ không giới hạn ở một loại dữ liệu.

1. `ueh-dao-van-ai-quy-dinh-chung:heading:017` — score 0.2430; relevant=False

> # UEH — Quy định kiểm soát đạo văn và sử dụng AI: quy định chung
> ## Điều 4. Sử dụng AI trong học thuật
> 
> a) Sử dụng nội dung do AI tạo ra nhưng không thông báo hoặc thông báo không đầy đủ việc sử dụng công cụ, phạm vi và vai trò của AI.
> 
> b) Sử dụng AI để tạo ra nội dung nhưng không kiểm tra, xác nhận nguồn hoặc độ chính xác.
> 
> c) Sử dụng AI để tạo ra toàn bộ hoặc phần lớn nội dung sản phẩm học thuật mà không có sự đóng góp đáng kể, thực chất và sáng tạo của tác giả.
> 
> d) Sử dụng AI để gian lận trong bài kiểm tra, bài thi.
> 
> e) Sử dụng AI để tạo dữ liệu giả hoặc làm sai lệch dữ liệu gốc.
> 
> f) Sử dụng AI để tạo trích dẫn giả hoặc tài liệu tham khảo không tồn tại.
> 
> g) Sử dụng AI trong những trường hợp UEH, giảng viên hoặc hội đồng chuyên môn quy định là không được phép.
> 
> 

2. `ueh-dao-van-ai-quy-dinh-chung:heading:014` — score 0.2408; relevant=False

> # UEH — Quy định kiểm soát đạo văn và sử dụng AI: quy định chung
> ## Điều 4. Sử dụng AI trong học thuật
> 
> - Minh bạch: ghi rõ công cụ AI tạo sinh đã sử dụng, mục đích sử dụng (tóm tắt, dịch thuật, tạo hình, viết mã v.v.) và những nội dung có sự hỗ trợ của AI tạo sinh trong sản phẩm học thuật. Việc khai báo cần thực hiện theo chuẩn, ví dụ: Trong phần Acknowledgement hoặc Phương pháp nghiên cứu ghi: “Một phần nội dung của sản phẩm này được hỗ trợ bởi ChatGPT (phiên bản …), sử dụng cho mục đích tóm tắt tài liệu/tham khảo ý tưởng/ngôn ngữ.”
> - Trung thực và trách nhiệm: tác giả chịu trách nhiệm về tính chính xác, độ tin cậy, chất lượng và liêm chính học thuật của những nội dung được AI cung cấp.
> 

3. `ueh-dao-van-ai-quy-dinh-chung:heading:015` — score 0.2369; relevant=False

> # UEH — Quy định kiểm soát đạo văn và sử dụng AI: quy định chung
> ## Điều 4. Sử dụng AI trong học thuật
> 
> - Tôn trọng quyền riêng tư, sở hữu trí tuệ và bảo mật dữ liệu: không cung cấp cho AI dữ liệu cá nhân, dữ liệu mật, thông tin chưa công bố hoặc dữ liệu nghiên cứu nội bộ của UEH hoặc đối tác nếu chưa được phép.
> - Không lạm dụng: không sử dụng AI để thay thế nhiệm vụ học thuật mà người học hoặc giảng viên phải tự thực hiện. AI chỉ đóng vai trò hỗ trợ. Khuyến khích người học và giảng viên sử dụng có trách nhiệm và không phụ thuộc hoàn toàn vào công cụ.
> - Đối với AI hỗ trợ, không bắt buộc thông báo nếu chỉ sử dụng để kiểm tra ngôn ngữ, chỉnh lỗi chính tả, ngữ pháp hoặc dịch thuật trực tiếp không mang tính sáng tạo nội dung.
> 

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> # UEH — Quy định kiểm soát đạo văn và sử dụng AI: quy định chung
> ## Điều 4. Sử dụng AI trong học thuật
> 
> a) Sử dụng nội dung do AI tạo ra nhưng không thông báo hoặc thông báo không đầy đủ việc sử dụng công cụ, phạm vi và vai trò của AI.
> 
> b) Sử dụng AI để tạo ra nội dung nhưng không kiểm tra, xác nhận nguồn hoặc độ chính xác.
> 
> c) Sử dụng AI để tạo ra toàn bộ hoặc phần lớn nội dung sản phẩm học thuật mà không có sự đóng góp đáng kể, thực chất và sáng tạo của tác giả.
> 
> d) Sử dụng AI để gian lận trong bài kiểm tra, bài thi.
> 
> e) Sử dụng AI để tạo dữ liệu giả hoặc làm sai lệch dữ liệu gốc.
> 
> f) Sử dụng AI để tạo trích dẫn giả hoặc tài liệu tham khảo không tồn tại.
> 
> g) Sử dụng AI trong những trường hợp UEH, giảng viên hoặc hội đồng chuyên môn quy định là không được phép.
> [ueh-dao-van-ai-quy-dinh-chung:heading:017](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
> 
> # UEH — Quy định kiểm soát đạo văn và sử dụng AI: quy định chung
> ## Điều 4. Sử dụng AI trong học thuật
> 
> - Minh bạch: ghi rõ công cụ AI tạo sinh đã sử dụng, mục đích sử dụng (tóm tắt, dịch thuật, tạo hình, viết mã v.v.) và những nội dung có sự hỗ trợ của AI tạo sinh trong sản phẩm học thuật. Việc khai báo cần thực hiện theo chuẩn, ví dụ: Trong phần Acknowledgement hoặc Phương pháp nghiên cứu ghi: “Một phần nội dung của sản phẩm này được hỗ trợ bởi ChatGPT (phiên bản …), sử dụng cho mục đích tóm tắt tài liệu/tham khảo ý tưởng/ngôn ngữ.”
> - Trung thực và trách nhiệm: tác giả chịu trách nhiệm về tính chính xác, độ tin cậy, chất lượng và liêm chính học thuật của những nội dung được AI cung cấp.
> [ueh-dao-van-ai-quy-dinh-chung:heading:014](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
> 
> # UEH — Quy định kiểm soát đạo văn và sử dụng AI: quy định chung
> ## Điều 4. Sử dụng AI trong học thuật
> 
> - Tôn trọng quyền riêng tư, sở hữu trí tuệ và bảo mật dữ liệu: không cung cấp cho AI dữ liệu cá nhân, dữ liệu mật, thông tin chưa công bố hoặc dữ liệu nghiên cứu nội bộ của UEH hoặc đối tác nếu chưa được phép.
> - Không lạm dụng: không sử dụng AI để thay thế nhiệm vụ học thuật mà người học hoặc giảng viên phải tự thực hiện. AI chỉ đóng vai trò hỗ trợ. Khuyến khích người học và giảng viên sử dụng có trách nhiệm và không phụ thuộc hoàn toàn vào công cụ.
> - Đối với AI hỗ trợ, không bắt buộc thông báo nếu chỉ sử dụng để kiểm tra ngôn ngữ, chỉnh lỗi chính tả, ngữ pháp hoặc dịch thuật trực tiếp không mang tính sáng tạo nội dung.
> [ueh-dao-van-ai-quy-dinh-chung:heading:015](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)


### Q5: Thông tư 49/2026/TT-BGDĐT có hiệu lực từ ngày nào và thay thế những thông tư nào?

Filter: `null`; Hit@3: True; coverage: 100%.

Gold: Theo Điều 22 trong snapshot nhóm cung cấp: hiệu lực từ 15/08/2026; Thông tư 15/2018/TT-BGDĐT và 30/2023/TT-BGDĐT hết hiệu lực từ ngày đó. Đây là gold answer kiểm thử snapshot, chưa xác minh tình trạng pháp lý hiện hành.

1. `tt49-2026-ung-dung-cong-nghe-ai:heading:024` — score 0.4245; relevant=True

> # Thông tư 49/2026/TT-BGDĐT — Ứng dụng công nghệ và AI trong giáo dục đại học
> ## Điều 22. Điều khoản thi hành
> 
> 1. Thông tư này có hiệu lực thi hành kể từ ngày 15 tháng 08 năm 2026.
> 
> 2. Thông tư số 15/2018/TT-BGDĐT ngày 27 tháng 7 năm 2018 của Bộ trưởng Bộ Giáo dục và Đào tạo quy định tổ chức hoạt động, sử dụng thư điện tử và trang thông tin điện tử của các cơ sở giáo dục đại học, các trường cao đẳng sư phạm; Thông tư số 30/2023/TT-BGDĐT ngày 29 tháng 12 năm 2023 của Bộ trưởng Bộ Giáo dục và Đào tạo quy định về ứng dụng công nghệ thông tin trong đào tạo trực tuyến đối với giáo dục đại học hết hiệu lực thi hành từ ngày Thông tư này có hiệu lực.
> 
> 

2. `tt49-2026-ung-dung-cong-nghe-ai:heading:000` — score 0.3574; relevant=False

> # Thông tư 49/2026/TT-BGDĐT — Ứng dụng công nghệ và AI trong giáo dục đại học
> 
> Số: 49/2026/TT-BGDĐT — Hà Nội, ngày 30 tháng 06 năm 2026.
> 
> Quy định ứng dụng công nghệ trong giáo dục đại học, giáo dục nghề nghiệp (trích các Điều liên quan đến trí tuệ nhân tạo và liêm chính học thuật).

3. `tt49-2026-ung-dung-cong-nghe-ai:heading:009` — score 0.3476; relevant=False

> # Thông tư 49/2026/TT-BGDĐT — Ứng dụng công nghệ và AI trong giáo dục đại học
> ## Điều 6. Ứng dụng công nghệ trong hoạt động đào tạo
> 
> 
> 

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> # Thông tư 49/2026/TT-BGDĐT — Ứng dụng công nghệ và AI trong giáo dục đại học
> ## Điều 22. Điều khoản thi hành
> 
> 1. Thông tư này có hiệu lực thi hành kể từ ngày 15 tháng 08 năm 2026.
> 
> 2. Thông tư số 15/2018/TT-BGDĐT ngày 27 tháng 7 năm 2018 của Bộ trưởng Bộ Giáo dục và Đào tạo quy định tổ chức hoạt động, sử dụng thư điện tử và trang thông tin điện tử của các cơ sở giáo dục đại học, các trường cao đẳng sư phạm; Thông tư số 30/2023/TT-BGDĐT ngày 29 tháng 12 năm 2023 của Bộ trưởng Bộ Giáo dục và Đào tạo quy định về ứng dụng công nghệ thông tin trong đào tạo trực tuyến đối với giáo dục đại học hết hiệu lực thi hành từ ngày Thông tư này có hiệu lực.
> [tt49-2026-ung-dung-cong-nghe-ai:heading:024](https://luatvietnam.vn/giao-duc/thong-tu-49-2026-tt-bgddt-ung-dung-cong-nghe-trong-giao-duc-dai-hoc-va-nghe-nghiep-439350-d1.html)
> 
> # Thông tư 49/2026/TT-BGDĐT — Ứng dụng công nghệ và AI trong giáo dục đại học
> 
> Số: 49/2026/TT-BGDĐT — Hà Nội, ngày 30 tháng 06 năm 2026.
> 
> Quy định ứng dụng công nghệ trong giáo dục đại học, giáo dục nghề nghiệp (trích các Điều liên quan đến trí tuệ nhân tạo và liêm chính học thuật).
> [tt49-2026-ung-dung-cong-nghe-ai:heading:000](https://luatvietnam.vn/giao-duc/thong-tu-49-2026-tt-bgddt-ung-dung-cong-nghe-trong-giao-duc-dai-hoc-va-nghe-nghiep-439350-d1.html)
> 
> # Thông tư 49/2026/TT-BGDĐT — Ứng dụng công nghệ và AI trong giáo dục đại học
> ## Điều 6. Ứng dụng công nghệ trong hoạt động đào tạo
> [tt49-2026-ung-dung-cong-nghe-ai:heading:009](https://luatvietnam.vn/giao-duc/thong-tu-49-2026-tt-bgddt-ung-dung-cong-nghe-trong-giao-duc-dai-hoc-va-nghe-nghiep-439350-d1.html)


## mock / fixed_size

### Q1: Theo quy định của UEH, tỷ lệ tương đồng từ bao nhiêu phần trăm thì sản phẩm học thuật bị xem là có dấu hiệu đạo văn?

Filter: `null`; Hit@3: False; coverage: 0%.

Gold: Theo snapshot UEH, tỷ lệ tương đồng từ 20% trở lên là một dấu hiệu định lượng, sau khi loại các phần được miễn trừ nêu trong quy định; không tự động kết luận đạo văn chỉ từ tỷ lệ này.

1. `rmit-ai-acknowledgement-guide:fixed_size:000` — score 0.3758; relevant=False

> # RMIT Library — Acknowledging the use of AI tools (students)
> 
> ## Acknowledging the AI tools you have used
> 
> In some assessment tasks, you may be permitted to use AI tools for certain purposes, such as to:
> 
> conduct background research on a topic
> 
> generate or brainstorm an outline or ideas for your assessment
> 
> clarify your reading interpretation or confirm your understanding of a topic
> 
> receive feedback for your writing (e.g. checking for consistency, clarity, grammar, spelling and expression)
> 
> In

2. `una-genai-policy-general:fixed_size:010` — score 0.3592; relevant=False

> or copyright in the future
> 
> ### Rationale for the Above Guidelines
> 
> Please note that Microsoft and OpenAI explicitly forbid using ChatGPT and their other products for specific activity categories, including fraud and illegal activities.  This list of items can be found in their usage policy document.
> 
> ### Personal liability for publication on ChatGPT
> 
> ChatGPT uses a click-through agreement.  Click-through agreements, including OpenAI and ChatGPT terms of use, are contracts. Individuals who accep

3. `rmit-vn-academic-integrity-ai:fixed_size:015` — score 0.2356; relevant=False

>  can collaborate with your peers without breaching academic integrity by:
> 
> working together on a group assignment with your group members (just remember to credit all group members)
> 
> helping each other understand the assignment question
> 
> studying together
> 
> If you’re unsure, ask your educator about what kind of collaboration is permitted in your course.
> 
> ### Fabrication and falsification
> 
> What is fabrication?
> 
> Fabrication is when someone claims to have carried out tests, experiments, research or 

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> # RMIT Library — Acknowledging the use of AI tools (students)
> 
> ## Acknowledging the AI tools you have used
> 
> In some assessment tasks, you may be permitted to use AI tools for certain purposes, such as to:
> 
> conduct background research on a topic
> 
> generate or brainstorm an outline or ideas for your assessment
> 
> clarify your reading interpretation or confirm your understanding of a topic
> 
> receive feedback for your writing (e.g. checking for consistency, clarity, grammar, spelling and expression)
> 
> In
> [rmit-ai-acknowledgement-guide:fixed_size:000](https://rmit.libguides.com/referencing_AI_tools/acknowledging)
> 
> or copyright in the future
> 
> ### Rationale for the Above Guidelines
> 
> Please note that Microsoft and OpenAI explicitly forbid using ChatGPT and their other products for specific activity categories, including fraud and illegal activities.  This list of items can be found in their usage policy document.
> 
> ### Personal liability for publication on ChatGPT
> 
> ChatGPT uses a click-through agreement.  Click-through agreements, including OpenAI and ChatGPT terms of use, are contracts. Individuals who accep
> [una-genai-policy-general:fixed_size:010](https://www.una.edu/academics/generative-ai-policy.html)
> 
> can collaborate with your peers without breaching academic integrity by:
> 
> working together on a group assignment with your group members (just remember to credit all group members)
> 
> helping each other understand the assignment question
> 
> studying together
> 
> If you’re unsure, ask your educator about what kind of collaboration is permitted in your course.
> 
> ### Fabrication and falsification
> 
> What is fabrication?
> 
> Fabrication is when someone claims to have carried out tests, experiments, research or
> [rmit-vn-academic-integrity-ai:fixed_size:015](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)


### Q2: Sản phẩm học thuật đã chỉnh sửa nhưng vẫn vi phạm lỗi đạo văn thì xử lý ra sao?

Filter: `{"audience": "student"}`; Hit@3: True; coverage: 100%.

Gold: Trong bối cảnh bài tập học phần của người học: giảng viên phụ trách lập biên bản/thông báo chuyển về đơn vị quản lý để xử lý tùy mức độ vi phạm quy định tại Phụ lục 3.

1. `una-genai-policy-students:fixed_size:004` — score 0.3908; relevant=False

> r own creation.
> 
> Learning and Exploration: AI tools can be explored to supplement learning and deepen your understanding of course material. This includes using AI to clarify concepts, simulate scenarios, or analyze data sets.
> 
> ### Unacceptable AI Use
> 
> Plagiarism or Full Automation of Assignments: Submitting AI-generated work as your own without meaningful engagement or modification is considered plagiarism. All assignments should reflect your own original thought processes, critical analysis, a

2. `ueh-xu-ly-vi-pham-nguoi-hoc:fixed_size:005` — score 0.2855; relevant=True

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

3. `rmit-ai-acknowledgement-guide:fixed_size:003` — score 0.2388; relevant=False

> rd of how you have used AI tools in the process of creating your work, including the prompt used, the outputs generated, and how the generated content was used in your work.
> 
> Make sure you save a copy of the prompts used and outputs generated, as you may need to provide this to your educator on request.
> 
> ## Template for acknowledging the use of AI tools
> 
> The advice below is based on the current (September 2025) advice from the APA 7th style manual editors.
> 
> Please note that there is no longer a 

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> r own creation.
> 
> Learning and Exploration: AI tools can be explored to supplement learning and deepen your understanding of course material. This includes using AI to clarify concepts, simulate scenarios, or analyze data sets.
> 
> ### Unacceptable AI Use
> 
> Plagiarism or Full Automation of Assignments: Submitting AI-generated work as your own without meaningful engagement or modification is considered plagiarism. All assignments should reflect your own original thought processes, critical analysis, a
> [una-genai-policy-students:fixed_size:004](https://www.una.edu/academics/generative-ai-policy.html)
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
> rd of how you have used AI tools in the process of creating your work, including the prompt used, the outputs generated, and how the generated content was used in your work.
> 
> Make sure you save a copy of the prompts used and outputs generated, as you may need to provide this to your educator on request.
> 
> ## Template for acknowledging the use of AI tools
> 
> The advice below is based on the current (September 2025) advice from the APA 7th style manual editors.
> 
> Please note that there is no longer a
> [rmit-ai-acknowledgement-guide:fixed_size:003](https://rmit.libguides.com/referencing_AI_tools/acknowledging)


### Q3: Khi ghi nhận việc dùng công cụ AI trong bài làm, câu acknowledgement cần nêu những thông tin gì?

Filter: `null`; Hit@3: False; coverage: 0%.

Gold: Theo hướng dẫn RMIT Library: nêu cách sử dụng AI, tên công cụ và nhà phát triển, năm nội dung AI được người dùng tạo ra. Không bắt buộc phiên bản/ngày dùng trừ khi giảng viên yêu cầu.

1. `una-genai-policy-students:fixed_size:009` — score 0.3558; relevant=False

> g objectives and demonstrate your personal understanding of the course material, the use of artificial intelligence (AI) tools for any aspect of coursework is strictly prohibited.
> 
> ### Prohibited AI Activities Include, but Are Not Limited to:
> 
> Generating Content: Using AI tools (e.g., ChatGPT, Jasper, Grammarly AI) to generate essays, assignments, reports, code, or any other form of academic work is not allowed.
> 
> Assisting with Writing or Revisions: AI tools cannot be used to help with writing, 

2. `una-genai-policy-students:fixed_size:008` — score 0.2835; relevant=False

> ourse, depending on the severity of the infraction.
> 
> ### Instructor's Role
> 
> If you are uncertain about whether your use of AI falls within acceptable guidelines, consult the instructor before submitting your work.
> 
> ### OPTION 2 Policy on AI Use in Coursework
> 
> This course is designed to foster your independent critical thinking, creativity, and skill development. To ensure that you meet the learning objectives and demonstrate your personal understanding of the course material, the use of artifici

3. `una-genai-policy-faculty:fixed_size:014` — score 0.2803; relevant=False

> ies, including fraud and illegal activities.  This list of items can be found in their usage policy document.
> 
> ### Personal liability for publication on ChatGPT
> 
> ChatGPT uses a click-through agreement.  Click-through agreements, including OpenAI and ChatGPT terms of use, are contracts. Individuals who accept click-through agreements without delegated signature authority may face personal consequences, including responsibility for compliance with terms and conditions.
> 
> For questions regarding dat

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> g objectives and demonstrate your personal understanding of the course material, the use of artificial intelligence (AI) tools for any aspect of coursework is strictly prohibited.
> 
> ### Prohibited AI Activities Include, but Are Not Limited to:
> 
> Generating Content: Using AI tools (e.g., ChatGPT, Jasper, Grammarly AI) to generate essays, assignments, reports, code, or any other form of academic work is not allowed.
> 
> Assisting with Writing or Revisions: AI tools cannot be used to help with writing,
> [una-genai-policy-students:fixed_size:009](https://www.una.edu/academics/generative-ai-policy.html)
> 
> ourse, depending on the severity of the infraction.
> 
> ### Instructor's Role
> 
> If you are uncertain about whether your use of AI falls within acceptable guidelines, consult the instructor before submitting your work.
> 
> ### OPTION 2 Policy on AI Use in Coursework
> 
> This course is designed to foster your independent critical thinking, creativity, and skill development. To ensure that you meet the learning objectives and demonstrate your personal understanding of the course material, the use of artifici
> [una-genai-policy-students:fixed_size:008](https://www.una.edu/academics/generative-ai-policy.html)
> 
> ies, including fraud and illegal activities.  This list of items can be found in their usage policy document.
> 
> ### Personal liability for publication on ChatGPT
> 
> ChatGPT uses a click-through agreement.  Click-through agreements, including OpenAI and ChatGPT terms of use, are contracts. Individuals who accept click-through agreements without delegated signature authority may face personal consequences, including responsibility for compliance with terms and conditions.
> 
> For questions regarding dat
> [una-genai-policy-faculty:fixed_size:014](https://www.una.edu/academics/generative-ai-policy.html)


### Q4: Những loại thông tin nào không được phép nhập vào công cụ AI tạo sinh?

Filter: `null`; Hit@3: False; coverage: 0%.

Gold: Theo snapshot UNA, không nhập thông tin cá nhân, bí mật, độc quyền hoặc nhạy cảm: ví dụ hồ sơ sinh viên/tuyển sinh, số an sinh xã hội, dữ liệu thẻ/ngân hàng, giấy tờ định danh, dữ liệu y tế/bảo hiểm, dữ liệu người tham gia nghiên cứu chưa được đồng ý công khai, hồ sơ nội bộ và nội dung thuộc NDA/sở hữu trí tuệ chưa được phép. Danh sách ví dụ không giới hạn ở một loại dữ liệu.

1. `rmit-vn-academic-integrity-ai:fixed_size:001` — score 0.3194; relevant=False

> ontacts, resources and support
> 
> ## What is academic integrity?
> 
> When working on assessments, it’s essential to know your academic integrity responsibilities. In practical terms, academic integrity means developing and submitting for assessment your own academic work. Some breaches of academic integrity include plagiarism, collusion and contract cheating, which all have serious consequences. Sometimes, the inappropriate use of AI in your studies can result in a breach.
> 
> Academic integrity has bee

2. `rmit-ai-acknowledgement-guide:fixed_size:004` — score 0.3180; relevant=False

> eptember 2025) advice from the APA 7th style manual editors.
> 
> Please note that there is no longer a requirement to include the version number for the AI tool or the date that you used the tool, unless you are required to do so by your course coordinator or teacher.
> 
> In your acknowledgement, include the following:
> 
> how you used the AI tool
> 
> the name of the AI tool and its creator
> 
> the year the AI content was generated by the user
> 
> In your reference list or bibliography, include an entry for the A

3. `tt49-2026-ung-dung-cong-nghe-ai:fixed_size:003` — score 0.3165; relevant=False

> ục đại học, giáo dục nghề nghiệp
> 
> Việc ứng dụng công nghệ trong cơ sở giáo dục tuân thủ các nguyên tắc sau:
> 
> 1. Bảo đảm quyền tự chủ của cơ sở giáo dục, gắn với tự kiểm soát, minh bạch và trách nhiệm giải trình, tuân thủ các quy định của pháp luật có liên quan.
> 
> 2. Ứng dụng công nghệ phải lấy người học làm trung tâm; phục vụ thực hiện chương trình đào tạo, đáp ứng chuẩn đầu ra và duy trì các điều kiện bảo đảm chất lượng theo quy định; công nghệ và trí tuệ nhân tạo là công cụ hỗ trợ, không thay t

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> ontacts, resources and support
> 
> ## What is academic integrity?
> 
> When working on assessments, it’s essential to know your academic integrity responsibilities. In practical terms, academic integrity means developing and submitting for assessment your own academic work. Some breaches of academic integrity include plagiarism, collusion and contract cheating, which all have serious consequences. Sometimes, the inappropriate use of AI in your studies can result in a breach.
> 
> Academic integrity has bee
> [rmit-vn-academic-integrity-ai:fixed_size:001](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)
> 
> eptember 2025) advice from the APA 7th style manual editors.
> 
> Please note that there is no longer a requirement to include the version number for the AI tool or the date that you used the tool, unless you are required to do so by your course coordinator or teacher.
> 
> In your acknowledgement, include the following:
> 
> how you used the AI tool
> 
> the name of the AI tool and its creator
> 
> the year the AI content was generated by the user
> 
> In your reference list or bibliography, include an entry for the A
> [rmit-ai-acknowledgement-guide:fixed_size:004](https://rmit.libguides.com/referencing_AI_tools/acknowledging)
> 
> ục đại học, giáo dục nghề nghiệp
> 
> Việc ứng dụng công nghệ trong cơ sở giáo dục tuân thủ các nguyên tắc sau:
> 
> 1. Bảo đảm quyền tự chủ của cơ sở giáo dục, gắn với tự kiểm soát, minh bạch và trách nhiệm giải trình, tuân thủ các quy định của pháp luật có liên quan.
> 
> 2. Ứng dụng công nghệ phải lấy người học làm trung tâm; phục vụ thực hiện chương trình đào tạo, đáp ứng chuẩn đầu ra và duy trì các điều kiện bảo đảm chất lượng theo quy định; công nghệ và trí tuệ nhân tạo là công cụ hỗ trợ, không thay t
> [tt49-2026-ung-dung-cong-nghe-ai:fixed_size:003](https://luatvietnam.vn/giao-duc/thong-tu-49-2026-tt-bgddt-ung-dung-cong-nghe-trong-giao-duc-dai-hoc-va-nghe-nghiep-439350-d1.html)


### Q5: Thông tư 49/2026/TT-BGDĐT có hiệu lực từ ngày nào và thay thế những thông tư nào?

Filter: `null`; Hit@3: False; coverage: 0%.

Gold: Theo Điều 22 trong snapshot nhóm cung cấp: hiệu lực từ 15/08/2026; Thông tư 15/2018/TT-BGDĐT và 30/2023/TT-BGDĐT hết hiệu lực từ ngày đó. Đây là gold answer kiểm thử snapshot, chưa xác minh tình trạng pháp lý hiện hành.

1. `una-genai-policy-faculty:fixed_size:010` — score 0.3149; relevant=False

> t
> - Health insurance information, including policy number(s), subscriber number(s), application information, claims history, and appeals records
> - Research participant data unless there is consent to use it publicly
> - Bank account numbers or information
> - University budget and business records
> - Employee personal records, including recruitment and search records, employee performance evaluation, and disciplinary records
> - Legal analysis or advice
> - University telephone directories
> - Any informat

2. `una-genai-policy-students:fixed_size:004` — score 0.2498; relevant=False

> r own creation.
> 
> Learning and Exploration: AI tools can be explored to supplement learning and deepen your understanding of course material. This includes using AI to clarify concepts, simulate scenarios, or analyze data sets.
> 
> ### Unacceptable AI Use
> 
> Plagiarism or Full Automation of Assignments: Submitting AI-generated work as your own without meaningful engagement or modification is considered plagiarism. All assignments should reflect your own original thought processes, critical analysis, a

3. `una-genai-policy-faculty:fixed_size:011` — score 0.2482; relevant=False

> nd disciplinary records
> - Legal analysis or advice
> - University telephone directories
> - Any information within the scope of a Nondisclosure Agreement or nondisclosure terms of contracts
> - Intellectual property owned by or licensed from a third party without express written permission
> - Donor information
> - Passport or visa numbers
> - Copyrighted material unless you are the author and it does not require permission from your publisher
> 
> ### Information where caution should be used before input into 

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> t
> - Health insurance information, including policy number(s), subscriber number(s), application information, claims history, and appeals records
> - Research participant data unless there is consent to use it publicly
> - Bank account numbers or information
> - University budget and business records
> - Employee personal records, including recruitment and search records, employee performance evaluation, and disciplinary records
> - Legal analysis or advice
> - University telephone directories
> - Any informat
> [una-genai-policy-faculty:fixed_size:010](https://www.una.edu/academics/generative-ai-policy.html)
> 
> r own creation.
> 
> Learning and Exploration: AI tools can be explored to supplement learning and deepen your understanding of course material. This includes using AI to clarify concepts, simulate scenarios, or analyze data sets.
> 
> ### Unacceptable AI Use
> 
> Plagiarism or Full Automation of Assignments: Submitting AI-generated work as your own without meaningful engagement or modification is considered plagiarism. All assignments should reflect your own original thought processes, critical analysis, a
> [una-genai-policy-students:fixed_size:004](https://www.una.edu/academics/generative-ai-policy.html)
> 
> nd disciplinary records
> - Legal analysis or advice
> - University telephone directories
> - Any information within the scope of a Nondisclosure Agreement or nondisclosure terms of contracts
> - Intellectual property owned by or licensed from a third party without express written permission
> - Donor information
> - Passport or visa numbers
> - Copyrighted material unless you are the author and it does not require permission from your publisher
> 
> ### Information where caution should be used before input into
> [una-genai-policy-faculty:fixed_size:011](https://www.una.edu/academics/generative-ai-policy.html)


## mock / by_sentences

### Q1: Theo quy định của UEH, tỷ lệ tương đồng từ bao nhiêu phần trăm thì sản phẩm học thuật bị xem là có dấu hiệu đạo văn?

Filter: `null`; Hit@3: False; coverage: 0%.

Gold: Theo snapshot UEH, tỷ lệ tương đồng từ 20% trở lên là một dấu hiệu định lượng, sau khi loại các phần được miễn trừ nêu trong quy định; không tự động kết luận đạo văn chỉ từ tỷ lệ này.

1. `rmit-vn-academic-integrity-ai:by_sentences:026` — score 0.2337; relevant=False

> Keep drafts of your work. To help prove the authenticity and originality of your work, you should keep all draft versions of your work to show how your assessments were developed. These can be requested at any time during your program.

2. `una-genai-policy-students:by_sentences:006` — score 0.2282; relevant=False

> Failure to do so will be treated as academic dishonesty. Personal, confidential, proprietary, or sensitive information that should not be published or uploaded into a Generative AI tool. ### Guidelines for AI Attribution
> 
> When using AI-generated content (e.g., for ideation or content improvement), cite the tool and briefly describe its use, like this:
> 
> Formal citation in appropriate course format (e.g., APA 7, MLA, ect.) o “This assignment used suggestions from ChatGPT for structuring arguments.”
> 
> ### Consequences of Misuse
> 
> Misuse of AI will be treated as a violation of academic integrity and may result in penalties ranging from assignment point deductions to failure of the course, depending on the severity of the infraction.

3. `rmit-vn-academic-integrity-ai:by_sentences:019` — score 0.2261; relevant=False

> Be open about problems such as missing, messy, or unexpected results, and explain these limitations instead of trying to ‘fix’ them
> 
> Keep a record of your raw data, and if you make changes, document the rules you used and why. Only cite references that you have found and utilised, and check or validate references cited in genAI output. ### Other types of academic integrity breaches
> 
> Attempting to gain unfair advantage in an invigilated assessment, breaching the rules for the conduct of invigilated assessment in a manner that defeats or compromises the purposes of the task.

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> Keep drafts of your work. To help prove the authenticity and originality of your work, you should keep all draft versions of your work to show how your assessments were developed. These can be requested at any time during your program.
> [rmit-vn-academic-integrity-ai:by_sentences:026](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)
> 
> Failure to do so will be treated as academic dishonesty. Personal, confidential, proprietary, or sensitive information that should not be published or uploaded into a Generative AI tool. ### Guidelines for AI Attribution
> 
> When using AI-generated content (e.g., for ideation or content improvement), cite the tool and briefly describe its use, like this:
> 
> Formal citation in appropriate course format (e.g., APA 7, MLA, ect.) o “This assignment used suggestions from ChatGPT for structuring arguments.”
> 
> ### Consequences of Misuse
> 
> Misuse of AI will be treated as a violation of academic integrity and may result in penalties ranging from assignment point deductions to failure of the course, depending on the severity of the infraction.
> [una-genai-policy-students:by_sentences:006](https://www.una.edu/academics/generative-ai-policy.html)
> 
> Be open about problems such as missing, messy, or unexpected results, and explain these limitations instead of trying to ‘fix’ them
> 
> Keep a record of your raw data, and if you make changes, document the rules you used and why. Only cite references that you have found and utilised, and check or validate references cited in genAI output. ### Other types of academic integrity breaches
> 
> Attempting to gain unfair advantage in an invigilated assessment, breaching the rules for the conduct of invigilated assessment in a manner that defeats or compromises the purposes of the task.
> [rmit-vn-academic-integrity-ai:by_sentences:019](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)


### Q2: Sản phẩm học thuật đã chỉnh sửa nhưng vẫn vi phạm lỗi đạo văn thì xử lý ra sao?

Filter: `{"audience": "student"}`; Hit@3: False; coverage: 0%.

Gold: Trong bối cảnh bài tập học phần của người học: giảng viên phụ trách lập biên bản/thông báo chuyển về đơn vị quản lý để xử lý tùy mức độ vi phạm quy định tại Phụ lục 3.

1. `ueh-xu-ly-vi-pham-nguoi-hoc:by_sentences:004` — score 0.2919; relevant=False

> ## Điều 6. Tổ chức thực hiện — trách nhiệm của người học
> 
> ### Trách nhiệm của tác giả sản phẩm học thuật và người học tại UEH:
> 
> a) Thực hiện nghiêm túc các quy định về đạo văn và sử dụng AI trong học thuật. b) Khuyến khích toàn thể người học, viên chức, người lao động của UEH thông báo và cung cấp những bằng chứng về những trường hợp nghi ngờ có hành vi đạo văn hoặc vi phạm sử dụng AI trong học thuật.

2. `rmit-vn-academic-integrity-ai:by_sentences:025` — score 0.2799; relevant=False

> When in doubt, check your course guide or ask your teacher
> 
> Be transparent about how you’ve used AI. This might mean referencing the tools you used, or reflecting on how they shaped your work. See the Library's AI referencing guide for specific AI referencing information.

3. `rmit-vn-academic-integrity-ai:by_sentences:018` — score 0.2077; relevant=False

> An example might be deleting “inconvenient” data points to make your graph look better, or changing dates/times on experiments to fit your hypothesis. How to avoid fabrication and falsification
> 
> Only ever use real and credible research, data and information. Don’t make it up!

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> ## Điều 6. Tổ chức thực hiện — trách nhiệm của người học
> 
> ### Trách nhiệm của tác giả sản phẩm học thuật và người học tại UEH:
> 
> a) Thực hiện nghiêm túc các quy định về đạo văn và sử dụng AI trong học thuật. b) Khuyến khích toàn thể người học, viên chức, người lao động của UEH thông báo và cung cấp những bằng chứng về những trường hợp nghi ngờ có hành vi đạo văn hoặc vi phạm sử dụng AI trong học thuật.
> [ueh-xu-ly-vi-pham-nguoi-hoc:by_sentences:004](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
> 
> When in doubt, check your course guide or ask your teacher
> 
> Be transparent about how you’ve used AI. This might mean referencing the tools you used, or reflecting on how they shaped your work. See the Library's AI referencing guide for specific AI referencing information.
> [rmit-vn-academic-integrity-ai:by_sentences:025](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)
> 
> An example might be deleting “inconvenient” data points to make your graph look better, or changing dates/times on experiments to fit your hypothesis. How to avoid fabrication and falsification
> 
> Only ever use real and credible research, data and information. Don’t make it up!
> [rmit-vn-academic-integrity-ai:by_sentences:018](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)


### Q3: Khi ghi nhận việc dùng công cụ AI trong bài làm, câu acknowledgement cần nêu những thông tin gì?

Filter: `null`; Hit@3: False; coverage: 0%.

Gold: Theo hướng dẫn RMIT Library: nêu cách sử dụng AI, tên công cụ và nhà phát triển, năm nội dung AI được người dùng tạo ra. Không bắt buộc phiên bản/ngày dùng trừ khi giảng viên yêu cầu.

1. `rmit-vn-academic-integrity-ai:by_sentences:012` — score 0.3498; relevant=False

> The RMIT Library has plenty of supports available to help you reference. Visit Referencing or book a consultation appointment with an RMIT Librarian. ### Collusion
> 
> What is collusion?

2. `una-genai-policy-students:by_sentences:001` — score 0.3491; relevant=False

> Be aware of the limitations of AI-generated content and verify its accuracy before using it in academic or research contexts. ## Sample syllabus language (AI use in coursework)
> 
> ### OPTION 1 Policy on AI Use in Coursework
> 
> As part of this course, students are encouraged to engage with emerging technologies, including artificial intelligence (AI) tools, to enhance learning and skill development. However, it is essential to use these tools responsibly and ethically.

3. `ueh-xu-ly-vi-pham-giang-vien:by_sentences:000` — score 0.2560; relevant=False

> # UEH — Xử lý vi phạm đạo văn và sử dụng AI đối với giảng viên, viên chức
> 
> (Kèm theo Quyết định số: 4002/QĐ-ĐHKT-NCPTGKTC, ngày 18 tháng 12 năm 2025 của Giám đốc Đại học Kinh tế Thành phố Hồ Chí Minh)
> 
> ## Điều 3. Xử lý hành vi đạo văn — áp dụng cho viên chức, người lao động, giảng viên thỉnh giảng
> 
> ### 2.4 Đối với sản phẩm học thuật của viên chức, người lao động, giảng viên thỉnh giảng của UEH:
> 
> a) Trước khi nghiệm thu/công bố:
> 
> Khi phát hiện vi phạm lỗi đạo văn, tác giả phải chỉnh sửa và khắc phục lỗi;
> 
> b) Sau khi chỉnh sửa nhưng vẫn vi phạm: sản phẩm không được công nhận, không được nghiệm thu và không được sử dụng trong bất kỳ hoạt động chuyên môn nào tại UEH. c) Sau nghiệm thu, công bố, phát hành:
> 
> Nếu phát hiện vi phạm đạo văn, tác giả phải chịu trách nhiệm theo quy định của UEH và pháp luật hiện hành; đồng thời thực hiện các nghĩa vụ liên quan như báo cáo đơn vị phát hành, rút bài, cải chính hoặc thu hồi (nếu có nhu cầu).

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> The RMIT Library has plenty of supports available to help you reference. Visit Referencing or book a consultation appointment with an RMIT Librarian. ### Collusion
> 
> What is collusion?
> [rmit-vn-academic-integrity-ai:by_sentences:012](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)
> 
> Be aware of the limitations of AI-generated content and verify its accuracy before using it in academic or research contexts. ## Sample syllabus language (AI use in coursework)
> 
> ### OPTION 1 Policy on AI Use in Coursework
> 
> As part of this course, students are encouraged to engage with emerging technologies, including artificial intelligence (AI) tools, to enhance learning and skill development. However, it is essential to use these tools responsibly and ethically.
> [una-genai-policy-students:by_sentences:001](https://www.una.edu/academics/generative-ai-policy.html)
> 
> # UEH — Xử lý vi phạm đạo văn và sử dụng AI đối với giảng viên, viên chức
> 
> (Kèm theo Quyết định số: 4002/QĐ-ĐHKT-NCPTGKTC, ngày 18 tháng 12 năm 2025 của Giám đốc Đại học Kinh tế Thành phố Hồ Chí Minh)
> 
> ## Điều 3. Xử lý hành vi đạo văn — áp dụng cho viên chức, người lao động, giảng viên thỉnh giảng
> 
> ### 2.4 Đối với sản phẩm học thuật của viên chức, người lao động, giảng viên thỉnh giảng của UEH:
> 
> a) Trước khi nghiệm thu/công bố:
> 
> Khi phát hiện vi phạm lỗi đạo văn, tác giả phải chỉnh sửa và khắc phục lỗi;
> 
> b) Sau khi chỉnh sửa nhưng vẫn vi phạm: sản phẩm không được công nhận, không được nghiệm thu và không được sử dụng trong bất kỳ hoạt động chuyên môn nào tại UEH. c) Sau nghiệm thu, công bố, phát hành:
> 
> Nếu phát hiện vi phạm đạo văn, tác giả phải chịu trách nhiệm theo quy định của UEH và pháp luật hiện hành; đồng thời thực hiện các nghĩa vụ liên quan như báo cáo đơn vị phát hành, rút bài, cải chính hoặc thu hồi (nếu có nhu cầu).
> [ueh-xu-ly-vi-pham-giang-vien:by_sentences:000](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)


### Q4: Những loại thông tin nào không được phép nhập vào công cụ AI tạo sinh?

Filter: `null`; Hit@3: False; coverage: 0%.

Gold: Theo snapshot UNA, không nhập thông tin cá nhân, bí mật, độc quyền hoặc nhạy cảm: ví dụ hồ sơ sinh viên/tuyển sinh, số an sinh xã hội, dữ liệu thẻ/ngân hàng, giấy tờ định danh, dữ liệu y tế/bảo hiểm, dữ liệu người tham gia nghiên cứu chưa được đồng ý công khai, hồ sơ nội bộ và nội dung thuộc NDA/sở hữu trí tuệ chưa được phép. Danh sách ví dụ không giới hạn ở một loại dữ liệu.

1. `una-genai-policy-students:by_sentences:009` — score 0.3355; relevant=False

> Problem Solving and Coding: AI tools are not to be used to solve problems, generate solutions, or assist with coding assignments. All work submitted must reflect your own efforts and understanding. Research and Idea Generation: You must not use AI tools to generate research topics, conduct research summaries, or formulate ideas for your coursework.

2. `tt49-2026-ung-dung-cong-nghe-ai:by_sentences:015` — score 0.2741; relevant=False

> Việc ứng dụng công nghệ số và trí tuệ nhân tạo trong đào tạo, kiểm tra, đánh giá và nghiên cứu khoa học phải bảo đảm trung thực, khách quan, minh bạch; tôn trọng quyền sở hữu trí tuệ; phản ánh đúng năng lực của người học và kết quả nghiên cứu; bảo đảm khả năng kiểm chứng, giải trình và không làm sai lệch kết quả; công nghệ số và trí tuệ nhân tạo chỉ là công cụ hỗ trợ, không thay thế trách nhiệm học thuật của người học, nhà giáo và nhà nghiên cứu. 2. Các hành vi vi phạm liêm chính học thuật trong môi trường số bao gồm:
> 
> a) Sử dụng công nghệ, bao gồm trí tuệ nhân tạo, để gian lận trong học tập, kiểm tra, đánh giá hoặc nghiên cứu khoa học;
> 
> b) Sao chép, đạo văn, sử dụng trái phép tài liệu, dữ liệu, học liệu số hoặc kết quả nghiên cứu;
> 
> c) Giả mạo, làm sai lệch dữ liệu, kết quả nghiên cứu hoặc thông tin học tập;
> 
> d) Nhờ người khác thực hiện hoặc thực hiện thay các nhiệm vụ học tập, kiểm tra, đánh giá hoặc nghiên cứu;
> 
> đ) Không công bố hoặc công bố không đầy đủ việc sử dụng công nghệ, trí tuệ nhân tạo khi có yêu cầu theo quy định nội bộ của cơ sở giáo dục và pháp luật của Nhà nước;
> 
> e) Các hành vi khác vi phạm quy định về liêm chính học thuật theo quy định của pháp luật và quy chế của cơ sở giáo dục.

3. `una-genai-policy-students:by_sentences:007` — score 0.2741; relevant=False

> ### Instructor's Role
> 
> If you are uncertain about whether your use of AI falls within acceptable guidelines, consult the instructor before submitting your work. ### OPTION 2 Policy on AI Use in Coursework
> 
> This course is designed to foster your independent critical thinking, creativity, and skill development. To ensure that you meet the learning objectives and demonstrate your personal understanding of the course material, the use of artificial intelligence (AI) tools for any aspect of coursework is strictly prohibited.

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> Problem Solving and Coding: AI tools are not to be used to solve problems, generate solutions, or assist with coding assignments. All work submitted must reflect your own efforts and understanding. Research and Idea Generation: You must not use AI tools to generate research topics, conduct research summaries, or formulate ideas for your coursework.
> [una-genai-policy-students:by_sentences:009](https://www.una.edu/academics/generative-ai-policy.html)
> 
> Việc ứng dụng công nghệ số và trí tuệ nhân tạo trong đào tạo, kiểm tra, đánh giá và nghiên cứu khoa học phải bảo đảm trung thực, khách quan, minh bạch; tôn trọng quyền sở hữu trí tuệ; phản ánh đúng năng lực của người học và kết quả nghiên cứu; bảo đảm khả năng kiểm chứng, giải trình và không làm sai lệch kết quả; công nghệ số và trí tuệ nhân tạo chỉ là công cụ hỗ trợ, không thay thế trách nhiệm học thuật của người học, nhà giáo và nhà nghiên cứu. 2. Các hành vi vi phạm liêm chính học thuật trong môi trường số bao gồm:
> 
> a) Sử dụng công nghệ, bao gồm trí tuệ nhân tạo, để gian lận trong học tập, kiểm tra, đánh giá hoặc nghiên cứu khoa học;
> 
> b) Sao chép, đạo văn, sử dụng trái phép tài liệu, dữ liệu, học liệu số hoặc kết quả nghiên cứu;
> 
> c) Giả mạo, làm sai lệch dữ liệu, kết quả nghiên cứu hoặc thông tin học tập;
> 
> d) Nhờ người khác thực hiện hoặc thực hiện thay các nhiệm vụ học tập, kiểm tra, đánh giá hoặc nghiên cứu;
> 
> đ) Không công bố hoặc công bố không đầy đủ việc sử dụng công nghệ, trí tuệ nhân tạo khi có yêu cầu theo quy định nội bộ của cơ sở giáo dục và pháp luật của Nhà nước;
> 
> e) Các hành vi khác vi phạm quy định về liêm chính học thuật theo quy định của pháp luật và quy chế của cơ sở giáo dục.
> [tt49-2026-ung-dung-cong-nghe-ai:by_sentences:015](https://luatvietnam.vn/giao-duc/thong-tu-49-2026-tt-bgddt-ung-dung-cong-nghe-trong-giao-duc-dai-hoc-va-nghe-nghiep-439350-d1.html)
> 
> ### Instructor's Role
> 
> If you are uncertain about whether your use of AI falls within acceptable guidelines, consult the instructor before submitting your work. ### OPTION 2 Policy on AI Use in Coursework
> 
> This course is designed to foster your independent critical thinking, creativity, and skill development. To ensure that you meet the learning objectives and demonstrate your personal understanding of the course material, the use of artificial intelligence (AI) tools for any aspect of coursework is strictly prohibited.
> [una-genai-policy-students:by_sentences:007](https://www.una.edu/academics/generative-ai-policy.html)


### Q5: Thông tư 49/2026/TT-BGDĐT có hiệu lực từ ngày nào và thay thế những thông tư nào?

Filter: `null`; Hit@3: False; coverage: 0%.

Gold: Theo Điều 22 trong snapshot nhóm cung cấp: hiệu lực từ 15/08/2026; Thông tư 15/2018/TT-BGDĐT và 30/2023/TT-BGDĐT hết hiệu lực từ ngày đó. Đây là gold answer kiểm thử snapshot, chưa xác minh tình trạng pháp lý hiện hành.

1. `ueh-xu-ly-vi-pham-nguoi-hoc:by_sentences:002` — score 0.2127; relevant=False

> Xử lý vi phạm sử dụng AI trong học thuật — áp dụng cho người học
> 
> ### 2.1. Đối với khóa luận, đề án tốt nghiệp, luận văn, luận án
> 
> a) Trước khi bảo vệ:
> 
> Người học phải chỉnh sửa và khắc phục vi phạm theo yêu cầu của giảng viên hướng dẫn hoặc đơn vị quản lý. b) Trong quá trình bảo vệ hoặc đánh giá:
> 
> Nếu Hội đồng đánh giá đề án tốt nghiệp, luận văn, luận án hoặc giảng viên phụ trách phát hiện vi phạm sử dụng AI trong học thuật, chủ tịch hội đồng/giảng viên phụ trách quyết định khóa luận, đề án tốt nghiệp, luận văn, luận án không đạt, người học phải chỉnh sửa lại sản phẩm và khắc phục vi phạm.

2. `una-genai-policy-faculty:by_sentences:005` — score 0.2114; relevant=False

> Entering information into most non-enterprise generative AI tools or services is like posting that data on a public website. ### University information that may be input into Generative AI tools:
> 
> Publicly available information lawfully published or internal information approved to be provided to the public by the University. Examples include:University community email announcements/digest content
> 
> - University publications
> - Information on the University’s public-facing website accessible without authentication of UNA login information
> - Content on official university social media accounts
> - Job postings
> - Publicly available maps
> 
> ### Information that may NOT be input into Generative AI tools:
> 
> Personal, confidential, proprietary, or sensitive information that should not be published or uploaded into a Generative AI tool.

3. `una-genai-policy-general:by_sentences:003` — score 0.2114; relevant=False

> Entering information into most non-enterprise generative AI tools or services is like posting that data on a public website. ### University information that may be input into Generative AI tools:
> 
> Publicly available information lawfully published or internal information approved to be provided to the public by the University. Examples include:University community email announcements/digest content
> 
> - University publications
> - Information on the University’s public-facing website accessible without authentication of UNA login information
> - Content on official university social media accounts
> - Job postings
> - Publicly available maps
> 
> ### Information that may NOT be input into Generative AI tools:
> 
> Personal, confidential, proprietary, or sensitive information that should not be published or uploaded into a Generative AI tool.

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> Xử lý vi phạm sử dụng AI trong học thuật — áp dụng cho người học
> 
> ### 2.1. Đối với khóa luận, đề án tốt nghiệp, luận văn, luận án
> 
> a) Trước khi bảo vệ:
> 
> Người học phải chỉnh sửa và khắc phục vi phạm theo yêu cầu của giảng viên hướng dẫn hoặc đơn vị quản lý. b) Trong quá trình bảo vệ hoặc đánh giá:
> 
> Nếu Hội đồng đánh giá đề án tốt nghiệp, luận văn, luận án hoặc giảng viên phụ trách phát hiện vi phạm sử dụng AI trong học thuật, chủ tịch hội đồng/giảng viên phụ trách quyết định khóa luận, đề án tốt nghiệp, luận văn, luận án không đạt, người học phải chỉnh sửa lại sản phẩm và khắc phục vi phạm.
> [ueh-xu-ly-vi-pham-nguoi-hoc:by_sentences:002](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
> 
> Entering information into most non-enterprise generative AI tools or services is like posting that data on a public website. ### University information that may be input into Generative AI tools:
> 
> Publicly available information lawfully published or internal information approved to be provided to the public by the University. Examples include:University community email announcements/digest content
> 
> - University publications
> - Information on the University’s public-facing website accessible without authentication of UNA login information
> - Content on official university social media accounts
> - Job postings
> - Publicly available maps
> 
> ### Information that may NOT be input into Generative AI tools:
> 
> Personal, confidential, proprietary, or sensitive information that should not be published or uploaded into a Generative AI tool.
> [una-genai-policy-faculty:by_sentences:005](https://www.una.edu/academics/generative-ai-policy.html)


## mock / recursive

### Q1: Theo quy định của UEH, tỷ lệ tương đồng từ bao nhiêu phần trăm thì sản phẩm học thuật bị xem là có dấu hiệu đạo văn?

Filter: `null`; Hit@3: False; coverage: 0%.

Gold: Theo snapshot UEH, tỷ lệ tương đồng từ 20% trở lên là một dấu hiệu định lượng, sau khi loại các phần được miễn trừ nêu trong quy định; không tự động kết luận đạo văn chỉ từ tỷ lệ này.

1. `tt49-2026-ung-dung-cong-nghe-ai:recursive:007` — score 0.3049; relevant=False

> đ) Việc sử dụng trí tuệ nhân tạo phải bảo đảm hỗ trợ, không thay thế vai trò của giảng viên; không làm sai lệch kết quả học tập; tuân thủ liêm chính học thuật và có cơ chế kiểm soát, giám sát, minh bạch.
> 
> 5. Bộ Giáo dục và Đào tạo khuyến khích, hướng dẫn và thúc đẩy phát triển các nền tảng hỗ trợ đào tạo dùng chung trong các cơ sở giáo dục.
> 
> ## Điều 7. Ứng dụng công nghệ trong kiểm tra, đánh giá người học
> 
> 1. Cơ sở giáo dục chủ động ứng dụng công nghệ số và trí tuệ nhân tạo trong kiểm tra, đánh giá người học bảo đảm tính chính xác, khách quan, minh bạch và công bằng; phù hợp với chuẩn đầu ra của chương trình đào tạo, bảo đảm quyền tự chủ gắn với trách nhiệm giải trình và tuân thủ quy định của pháp luật.
> 
> 2. Việc ứng dụng công nghệ được thực hiện phù hợp thông qua các phương thức sau:
> 
> 

2. `ueh-dao-van-ai-quy-dinh-chung:recursive:016` — score 0.2821; relevant=False

> 1. Việc phát hiện và đánh giá vi phạm sử dụng AI trong học thuật do giảng viên phụ trách/người hướng dẫn hoặc hội đồng/đơn vị có thẩm quyền thực hiện, trên cơ sở xem xét các yếu tố: mức độ sử dụng AI, vai trò của AI trong sản phẩm, hành vi thông báo sử dụng hoặc không thông báo, dấu hiệu gian lận hoặc thay thế nhiệm vụ học thuật. UEH không sử dụng kết quả của các công cụ phát hiện nội dụng do AI tạo ra làm căn cứ duy nhất để kết luận vi phạm học thuật. Đánh giá vi phạm sử dụng AI được thực hiện qua trao đổi trực tiếp giữa cá nhân/đơn vị có thẩm quyền và tác giả sử dụng AI. Trường hợp không thể tổ chức trao đổi trực tiếp vì lý do khách quan, đơn vị có thẩm quyền sẽ thực hiện đánh giá qua hình thức thay thế phù hợp.
> 
> ## Điều 6. Tổ chức thực hiện (trách nhiệm các đơn vị)
> 
> 

3. `ueh-dao-van-ai-quy-dinh-chung:recursive:007` — score 0.2559; relevant=False

> - Đối với các hành vi có tính chất chiếm đoạt nội dung, cố ý gian lận học thuật, xử lý theo hướng kỷ luật học thuật nghiêm khắc theo quy định hiện hành của UEH và pháp luật có liên quan.
> - Đối với lỗi kỹ thuật hoặc sơ suất trong ghi nguồn, trích dẫn không đầy đủ, có thể được xem xét yêu cầu chỉnh sửa mà không xử phạt nếu không có dấu hiệu gian lận.
> 
> ## Điều 4. Sử dụng AI trong học thuật
> 
> 

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> đ) Việc sử dụng trí tuệ nhân tạo phải bảo đảm hỗ trợ, không thay thế vai trò của giảng viên; không làm sai lệch kết quả học tập; tuân thủ liêm chính học thuật và có cơ chế kiểm soát, giám sát, minh bạch.
> 
> 5. Bộ Giáo dục và Đào tạo khuyến khích, hướng dẫn và thúc đẩy phát triển các nền tảng hỗ trợ đào tạo dùng chung trong các cơ sở giáo dục.
> 
> ## Điều 7. Ứng dụng công nghệ trong kiểm tra, đánh giá người học
> 
> 1. Cơ sở giáo dục chủ động ứng dụng công nghệ số và trí tuệ nhân tạo trong kiểm tra, đánh giá người học bảo đảm tính chính xác, khách quan, minh bạch và công bằng; phù hợp với chuẩn đầu ra của chương trình đào tạo, bảo đảm quyền tự chủ gắn với trách nhiệm giải trình và tuân thủ quy định của pháp luật.
> 
> 2. Việc ứng dụng công nghệ được thực hiện phù hợp thông qua các phương thức sau:
> [tt49-2026-ung-dung-cong-nghe-ai:recursive:007](https://luatvietnam.vn/giao-duc/thong-tu-49-2026-tt-bgddt-ung-dung-cong-nghe-trong-giao-duc-dai-hoc-va-nghe-nghiep-439350-d1.html)
> 
> 1. Việc phát hiện và đánh giá vi phạm sử dụng AI trong học thuật do giảng viên phụ trách/người hướng dẫn hoặc hội đồng/đơn vị có thẩm quyền thực hiện, trên cơ sở xem xét các yếu tố: mức độ sử dụng AI, vai trò của AI trong sản phẩm, hành vi thông báo sử dụng hoặc không thông báo, dấu hiệu gian lận hoặc thay thế nhiệm vụ học thuật. UEH không sử dụng kết quả của các công cụ phát hiện nội dụng do AI tạo ra làm căn cứ duy nhất để kết luận vi phạm học thuật. Đánh giá vi phạm sử dụng AI được thực hiện qua trao đổi trực tiếp giữa cá nhân/đơn vị có thẩm quyền và tác giả sử dụng AI. Trường hợp không thể tổ chức trao đổi trực tiếp vì lý do khách quan, đơn vị có thẩm quyền sẽ thực hiện đánh giá qua hình thức thay thế phù hợp.
> 
> ## Điều 6. Tổ chức thực hiện (trách nhiệm các đơn vị)
> [ueh-dao-van-ai-quy-dinh-chung:recursive:016](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
> 
> - Đối với các hành vi có tính chất chiếm đoạt nội dung, cố ý gian lận học thuật, xử lý theo hướng kỷ luật học thuật nghiêm khắc theo quy định hiện hành của UEH và pháp luật có liên quan.
> - Đối với lỗi kỹ thuật hoặc sơ suất trong ghi nguồn, trích dẫn không đầy đủ, có thể được xem xét yêu cầu chỉnh sửa mà không xử phạt nếu không có dấu hiệu gian lận.
> 
> ## Điều 4. Sử dụng AI trong học thuật
> [ueh-dao-van-ai-quy-dinh-chung:recursive:007](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)


### Q2: Sản phẩm học thuật đã chỉnh sửa nhưng vẫn vi phạm lỗi đạo văn thì xử lý ra sao?

Filter: `{"audience": "student"}`; Hit@3: False; coverage: 0%.

Gold: Trong bối cảnh bài tập học phần của người học: giảng viên phụ trách lập biên bản/thông báo chuyển về đơn vị quản lý để xử lý tùy mức độ vi phạm quy định tại Phụ lục 3.

1. `una-genai-policy-students:recursive:007` — score 0.3293; relevant=False

> Personal, confidential, proprietary, or sensitive information that should not be published or uploaded into a Generative AI tool.
> 
> ### Consequences of Misuse
> 
> Misuse of AI will be treated as a violation of academic integrity and may result in penalties ranging from assignment point deductions to failure of the course, depending on the severity of the infraction.

2. `rmit-vn-academic-integrity-ai:recursive:000` — score 0.2720; relevant=False

> # RMIT Vietnam — Academic integrity and appropriate use of AI (students)
> 
> Learn about academic integrity, what happens if you breach it and where to get help if you're unsure.
> 
> ## What is academic integrity?
> 
> ## Types of academic integrity breaches
> 
> Using artificial intelligence (AI) appropriately
> 
> ## What happens if I breach academic integrity?
> 
> Complete the Academic Integrity Awareness module
> 
> Contacts, resources and support
> 
> ## What is academic integrity?
> 
> 

3. `rmit-vn-academic-integrity-ai:recursive:012` — score 0.2041; relevant=False

> Sometimes, inappropriate use of AI in your studies can result in a breach of academic integrity, such as plagiarism or ghost writing.
> 
> The use of AI tools in your studies will be guided by your program and course requirements – what’s permitted in one course or assessment may not be allowed in another. So, it's always a good idea to double check your course guide or ask your educator for more information.
> 
> ### When is it okay to use AI tools in my studies?
> 
> Depending on your course, AI can support your studies in lots of ways. For example:
> 
> Explaining concepts: ask AI to explain theories, methods, or terminology in simpler words (like a study aid)
> 
> Brainstorming and planning: generating topic ideas, outlines, and question prompts to clarify direction
> 
> 

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> Personal, confidential, proprietary, or sensitive information that should not be published or uploaded into a Generative AI tool.
> 
> ### Consequences of Misuse
> 
> Misuse of AI will be treated as a violation of academic integrity and may result in penalties ranging from assignment point deductions to failure of the course, depending on the severity of the infraction.
> [una-genai-policy-students:recursive:007](https://www.una.edu/academics/generative-ai-policy.html)
> 
> # RMIT Vietnam — Academic integrity and appropriate use of AI (students)
> 
> Learn about academic integrity, what happens if you breach it and where to get help if you're unsure.
> 
> ## What is academic integrity?
> 
> ## Types of academic integrity breaches
> 
> Using artificial intelligence (AI) appropriately
> 
> ## What happens if I breach academic integrity?
> 
> Complete the Academic Integrity Awareness module
> 
> Contacts, resources and support
> 
> ## What is academic integrity?
> [rmit-vn-academic-integrity-ai:recursive:000](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)
> 
> Sometimes, inappropriate use of AI in your studies can result in a breach of academic integrity, such as plagiarism or ghost writing.
> 
> The use of AI tools in your studies will be guided by your program and course requirements – what’s permitted in one course or assessment may not be allowed in another. So, it's always a good idea to double check your course guide or ask your educator for more information.
> 
> ### When is it okay to use AI tools in my studies?
> 
> Depending on your course, AI can support your studies in lots of ways. For example:
> 
> Explaining concepts: ask AI to explain theories, methods, or terminology in simpler words (like a study aid)
> 
> Brainstorming and planning: generating topic ideas, outlines, and question prompts to clarify direction
> [rmit-vn-academic-integrity-ai:recursive:012](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)


### Q3: Khi ghi nhận việc dùng công cụ AI trong bài làm, câu acknowledgement cần nêu những thông tin gì?

Filter: `null`; Hit@3: False; coverage: 0%.

Gold: Theo hướng dẫn RMIT Library: nêu cách sử dụng AI, tên công cụ và nhà phát triển, năm nội dung AI được người dùng tạo ra. Không bắt buộc phiên bản/ngày dùng trừ khi giảng viên yêu cầu.

1. `una-genai-policy-staff:recursive:001` — score 0.2841; relevant=False

> UNA staff and faculty are permitted to use generative AI responsibly to assist in their work. However, users must exercise caution to avoid sharing confidential information, including student data protected under FERPA guidelines, when using AI tools. Additionally, the creation of AI-generated images for promotional materials is not allowed, as such content may conflict with UNA’s branding standards, copyright regulations, and institutional values. To ensure that all promotional materials remain on brand and in compliance with institutional and legal standards,
> 
> the Office of Enrollment Marketing & Digital Communications is available to assist in developing any needed promotional images.
> 
> 

2. `una-genai-policy-students:recursive:002` — score 0.2645; relevant=False

> Programming and Coding Assistance: AI tools may be used to generate code snippets or suggest solutions. Students should ensure that they understand the generated code and are able to explain its functionality during assessments or in class discussions.
> 
> Proofreading and Editing: Students may use AI for basic proofreading, formatting, and language refinement, as long as the content remains their own creation.
> 
> Learning and Exploration: AI tools can be explored to supplement learning and deepen your understanding of course material. This includes using AI to clarify concepts, simulate scenarios, or analyze data sets.
> 
> ### Unacceptable AI Use
> 
> 

3. `tt49-2026-ung-dung-cong-nghe-ai:recursive:018` — score 0.2541; relevant=False

> 3. Chánh Văn phòng, Cục trưởng Cục Khoa học, Công nghệ và Thông tin, Thủ trưởng các đơn vị thuộc Bộ Giáo dục và Đào tạo, Giám đốc các đại học, học viện, Hiệu trưởng các trường đại học, Hiệu trưởng các trường cao đẳng, Giám đốc các sở Giáo dục và Đào tạo và các tổ chức, cá nhân có liên quan chịu trách nhiệm thi hành Thông tư này./.

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> UNA staff and faculty are permitted to use generative AI responsibly to assist in their work. However, users must exercise caution to avoid sharing confidential information, including student data protected under FERPA guidelines, when using AI tools. Additionally, the creation of AI-generated images for promotional materials is not allowed, as such content may conflict with UNA’s branding standards, copyright regulations, and institutional values. To ensure that all promotional materials remain on brand and in compliance with institutional and legal standards,
> 
> the Office of Enrollment Marketing & Digital Communications is available to assist in developing any needed promotional images.
> [una-genai-policy-staff:recursive:001](https://www.una.edu/academics/generative-ai-policy.html)
> 
> Programming and Coding Assistance: AI tools may be used to generate code snippets or suggest solutions. Students should ensure that they understand the generated code and are able to explain its functionality during assessments or in class discussions.
> 
> Proofreading and Editing: Students may use AI for basic proofreading, formatting, and language refinement, as long as the content remains their own creation.
> 
> Learning and Exploration: AI tools can be explored to supplement learning and deepen your understanding of course material. This includes using AI to clarify concepts, simulate scenarios, or analyze data sets.
> 
> ### Unacceptable AI Use
> [una-genai-policy-students:recursive:002](https://www.una.edu/academics/generative-ai-policy.html)
> 
> 3. Chánh Văn phòng, Cục trưởng Cục Khoa học, Công nghệ và Thông tin, Thủ trưởng các đơn vị thuộc Bộ Giáo dục và Đào tạo, Giám đốc các đại học, học viện, Hiệu trưởng các trường đại học, Hiệu trưởng các trường cao đẳng, Giám đốc các sở Giáo dục và Đào tạo và các tổ chức, cá nhân có liên quan chịu trách nhiệm thi hành Thông tư này./.
> [tt49-2026-ung-dung-cong-nghe-ai:recursive:018](https://luatvietnam.vn/giao-duc/thong-tu-49-2026-tt-bgddt-ung-dung-cong-nghe-trong-giao-duc-dai-hoc-va-nghe-nghiep-439350-d1.html)


### Q4: Những loại thông tin nào không được phép nhập vào công cụ AI tạo sinh?

Filter: `null`; Hit@3: False; coverage: 0%.

Gold: Theo snapshot UNA, không nhập thông tin cá nhân, bí mật, độc quyền hoặc nhạy cảm: ví dụ hồ sơ sinh viên/tuyển sinh, số an sinh xã hội, dữ liệu thẻ/ngân hàng, giấy tờ định danh, dữ liệu y tế/bảo hiểm, dữ liệu người tham gia nghiên cứu chưa được đồng ý công khai, hồ sơ nội bộ và nội dung thuộc NDA/sở hữu trí tuệ chưa được phép. Danh sách ví dụ không giới hạn ở một loại dữ liệu.

1. `ueh-dao-van-ai-quy-dinh-chung:recursive:003` — score 0.3993; relevant=False

> - Có tỷ lệ tương đồng từ 20% trở lên (không tính phần: trích dẫn, danh mục tài liệu tham khảo, phần mô tả phương pháp mang tính lặp lại và phổ biến trong chuyên ngành, các thuật ngữ chuyên ngành, tiêu chuẩn kỹ thuật, trích dẫn văn bản quy phạm pháp luật, tên riêng không thể thay thế).
> b) Sử dụng sản phẩm của người khác mà không ghi nguồn
> 
> 

2. `tt49-2026-ung-dung-cong-nghe-ai:recursive:011` — score 0.3293; relevant=False

> c) Giả mạo, làm sai lệch dữ liệu, kết quả nghiên cứu hoặc thông tin học tập;
> 
> d) Nhờ người khác thực hiện hoặc thực hiện thay các nhiệm vụ học tập, kiểm tra, đánh giá hoặc nghiên cứu;
> 
> đ) Không công bố hoặc công bố không đầy đủ việc sử dụng công nghệ, trí tuệ nhân tạo khi có yêu cầu theo quy định nội bộ của cơ sở giáo dục và pháp luật của Nhà nước;
> 
> e) Các hành vi khác vi phạm quy định về liêm chính học thuật theo quy định của pháp luật và quy chế của cơ sở giáo dục.
> 
> 3. Trách nhiệm của các bên liên quan
> 
> 

3. `una-genai-policy-faculty:recursive:009` — score 0.2798; relevant=False

> ### Information where caution should be used before input into Generative AI tools:
> 
> Content that may contain personal, confidential, proprietary, or sensitive information should only be uploaded after verification that it does not include information that may not be uploaded. Examples include:
> 
> - Course content materials
> - Unpublished academic research or discoveries
> - Meeting notes
> - Presentation notes
> - Research data
> - Email
> - Proprietary or unpublished research data or writing or uploading information on discoveries may compromise your ability to seek a patent or copyright in the future
> 
> ### Rationale for the Above Guidelines
> 
> 

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> - Có tỷ lệ tương đồng từ 20% trở lên (không tính phần: trích dẫn, danh mục tài liệu tham khảo, phần mô tả phương pháp mang tính lặp lại và phổ biến trong chuyên ngành, các thuật ngữ chuyên ngành, tiêu chuẩn kỹ thuật, trích dẫn văn bản quy phạm pháp luật, tên riêng không thể thay thế).
> b) Sử dụng sản phẩm của người khác mà không ghi nguồn
> [ueh-dao-van-ai-quy-dinh-chung:recursive:003](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
> 
> c) Giả mạo, làm sai lệch dữ liệu, kết quả nghiên cứu hoặc thông tin học tập;
> 
> d) Nhờ người khác thực hiện hoặc thực hiện thay các nhiệm vụ học tập, kiểm tra, đánh giá hoặc nghiên cứu;
> 
> đ) Không công bố hoặc công bố không đầy đủ việc sử dụng công nghệ, trí tuệ nhân tạo khi có yêu cầu theo quy định nội bộ của cơ sở giáo dục và pháp luật của Nhà nước;
> 
> e) Các hành vi khác vi phạm quy định về liêm chính học thuật theo quy định của pháp luật và quy chế của cơ sở giáo dục.
> 
> 3. Trách nhiệm của các bên liên quan
> [tt49-2026-ung-dung-cong-nghe-ai:recursive:011](https://luatvietnam.vn/giao-duc/thong-tu-49-2026-tt-bgddt-ung-dung-cong-nghe-trong-giao-duc-dai-hoc-va-nghe-nghiep-439350-d1.html)
> 
> ### Information where caution should be used before input into Generative AI tools:
> 
> Content that may contain personal, confidential, proprietary, or sensitive information should only be uploaded after verification that it does not include information that may not be uploaded. Examples include:
> 
> - Course content materials
> - Unpublished academic research or discoveries
> - Meeting notes
> - Presentation notes
> - Research data
> - Email
> - Proprietary or unpublished research data or writing or uploading information on discoveries may compromise your ability to seek a patent or copyright in the future
> 
> ### Rationale for the Above Guidelines
> [una-genai-policy-faculty:recursive:009](https://www.una.edu/academics/generative-ai-policy.html)


### Q5: Thông tư 49/2026/TT-BGDĐT có hiệu lực từ ngày nào và thay thế những thông tư nào?

Filter: `null`; Hit@3: False; coverage: 0%.

Gold: Theo Điều 22 trong snapshot nhóm cung cấp: hiệu lực từ 15/08/2026; Thông tư 15/2018/TT-BGDĐT và 30/2023/TT-BGDĐT hết hiệu lực từ ngày đó. Đây là gold answer kiểm thử snapshot, chưa xác minh tình trạng pháp lý hiện hành.

1. `ueh-dao-van-ai-quy-dinh-chung:recursive:008` — score 0.2390; relevant=False

> 1. Trong Quy định này, trí tuệ nhân tạo (AI) được hiểu là các công cụ, hệ thống hoặc thuật toán có khả năng tạo, phân tích hoặc xử lý nội dung hỗ trợ hoạt động học thuật. AI được xem là công cụ hỗ trợ, không thay thế trách nhiệm tư duy, phân tích và sáng tạo của tác giả. 

2. `rmit-vn-academic-integrity-ai:recursive:010` — score 0.2354; relevant=False

> How to avoid fabrication and falsification
> 
> Only ever use real and credible research, data and information. Don’t make it up!
> 
> Be open about problems such as missing, messy, or unexpected results, and explain these limitations instead of trying to ‘fix’ them
> 
> Keep a record of your raw data, and if you make changes, document the rules you used and why.
> 
> Only cite references that you have found and utilised, and check or validate references cited in genAI output.
> 
> ### Other types of academic integrity breaches
> 
> Attempting to gain unfair advantage in an invigilated assessment, breaching the rules for the conduct of invigilated assessment in a manner that defeats or compromises the purposes of the task.
> 
> 

3. `tt49-2026-ung-dung-cong-nghe-ai:recursive:008` — score 0.2098; relevant=False

> a) Kiểm tra, đánh giá trực tiếp có hỗ trợ công nghệ;
> 
> b) Kiểm tra, đánh giá trực tuyến;
> 
> c) Kiểm tra, đánh giá kết hợp trực tiếp và trực tuyến;
> 
> d) Đánh giá quá trình học tập trên hệ thống số dựa trên dữ liệu và phân tích dữ liệu học tập;
> 
> đ) Các phương thức khác có ứng dụng công nghệ phù hợp.
> 
> 3. Ứng dụng công nghệ trong kiểm tra, đánh giá được thực hiện trong các hoạt động chủ yếu sau:
> 
> a) Xây dựng, quản lý ngân hàng câu hỏi, đề thi;
> 
> b) Tổ chức kiểm tra, đánh giá và chấm điểm;
> 
> c) Giám sát quá trình kiểm tra, đánh giá;
> 
> d) Lưu trữ, quản lý và khai thác dữ liệu đánh giá; phân tích kết quả học tập và đánh giá năng lực người học;
> 
> 4. Việc ứng dụng công nghệ trong kiểm tra, đánh giá phải bảo đảm:
> 
> a) Có hệ thống quản lý kiểm tra, đánh giá hoặc được tích hợp trong hệ thống quản lý học tập;
> 
> 

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> 1. Trong Quy định này, trí tuệ nhân tạo (AI) được hiểu là các công cụ, hệ thống hoặc thuật toán có khả năng tạo, phân tích hoặc xử lý nội dung hỗ trợ hoạt động học thuật. AI được xem là công cụ hỗ trợ, không thay thế trách nhiệm tư duy, phân tích và sáng tạo của tác giả.
> [ueh-dao-van-ai-quy-dinh-chung:recursive:008](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
> 
> How to avoid fabrication and falsification
> 
> Only ever use real and credible research, data and information. Don’t make it up!
> 
> Be open about problems such as missing, messy, or unexpected results, and explain these limitations instead of trying to ‘fix’ them
> 
> Keep a record of your raw data, and if you make changes, document the rules you used and why.
> 
> Only cite references that you have found and utilised, and check or validate references cited in genAI output.
> 
> ### Other types of academic integrity breaches
> 
> Attempting to gain unfair advantage in an invigilated assessment, breaching the rules for the conduct of invigilated assessment in a manner that defeats or compromises the purposes of the task.
> [rmit-vn-academic-integrity-ai:recursive:010](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)
> 
> a) Kiểm tra, đánh giá trực tiếp có hỗ trợ công nghệ;
> 
> b) Kiểm tra, đánh giá trực tuyến;
> 
> c) Kiểm tra, đánh giá kết hợp trực tiếp và trực tuyến;
> 
> d) Đánh giá quá trình học tập trên hệ thống số dựa trên dữ liệu và phân tích dữ liệu học tập;
> 
> đ) Các phương thức khác có ứng dụng công nghệ phù hợp.
> 
> 3. Ứng dụng công nghệ trong kiểm tra, đánh giá được thực hiện trong các hoạt động chủ yếu sau:
> 
> a) Xây dựng, quản lý ngân hàng câu hỏi, đề thi;
> 
> b) Tổ chức kiểm tra, đánh giá và chấm điểm;
> 
> c) Giám sát quá trình kiểm tra, đánh giá;
> 
> d) Lưu trữ, quản lý và khai thác dữ liệu đánh giá; phân tích kết quả học tập và đánh giá năng lực người học;
> 
> 4. Việc ứng dụng công nghệ trong kiểm tra, đánh giá phải bảo đảm:
> 
> a) Có hệ thống quản lý kiểm tra, đánh giá hoặc được tích hợp trong hệ thống quản lý học tập;
> [tt49-2026-ung-dung-cong-nghe-ai:recursive:008](https://luatvietnam.vn/giao-duc/thong-tu-49-2026-tt-bgddt-ung-dung-cong-nghe-trong-giao-duc-dai-hoc-va-nghe-nghiep-439350-d1.html)


## mock / heading

### Q1: Theo quy định của UEH, tỷ lệ tương đồng từ bao nhiêu phần trăm thì sản phẩm học thuật bị xem là có dấu hiệu đạo văn?

Filter: `null`; Hit@3: False; coverage: 0%.

Gold: Theo snapshot UEH, tỷ lệ tương đồng từ 20% trở lên là một dấu hiệu định lượng, sau khi loại các phần được miễn trừ nêu trong quy định; không tự động kết luận đạo văn chỉ từ tỷ lệ này.

1. `tt49-2026-ung-dung-cong-nghe-ai:heading:010` — score 0.3167; relevant=False

> # Thông tư 49/2026/TT-BGDĐT — Ứng dụng công nghệ và AI trong giáo dục đại học
> ## Điều 6. Ứng dụng công nghệ trong hoạt động đào tạo
> 
> b) Đào tạo dựa trên công nghệ phải bảo đảm chất lượng, chương trình đào tạo, chuẩn đầu ra, phương thức kiểm tra đánh giá và các điều kiện bảo đảm chất lượng theo quy định của pháp luật về giáo dục đại học và giáo dục nghề nghiệp;
> 
> c) Bảo đảm khả năng tổ chức, quản lý và theo dõi, đánh giá toàn bộ các hoạt động đào tạo, trọng tâm là quá trình học tập của người học; quản lý hồ sơ, quá trình và kết quả học tập của người học, hoạt động dạy của người dạy; ghi nhận trung thực, chính xác dữ liệu phục vụ quản lý, kiểm tra, giám sát và giải trình;
> 
> 

2. `ueh-dao-van-ai-quy-dinh-chung:heading:019` — score 0.2983; relevant=False

> # UEH — Quy định kiểm soát đạo văn và sử dụng AI: quy định chung
> ## Điều 5. Phát hiện và xử lý vi phạm sử dụng AI trong học thuật
> 
> 1. Việc phát hiện và đánh giá vi phạm sử dụng AI trong học thuật do giảng viên phụ trách/người hướng dẫn hoặc hội đồng/đơn vị có thẩm quyền thực hiện, trên cơ sở xem xét các yếu tố: mức độ sử dụng AI, vai trò của AI trong sản phẩm, hành vi thông báo sử dụng hoặc không thông báo, dấu hiệu gian lận hoặc thay thế nhiệm vụ học thuật. UEH không sử dụng kết quả của các công cụ phát hiện nội dụng do AI tạo ra làm căn cứ duy nhất để kết luận vi phạm học thuật. Đánh giá vi phạm sử dụng AI được thực hiện qua trao đổi trực tiếp giữa cá nhân/đơn vị có thẩm quyền và tác giả sử dụng AI. 

3. `una-genai-policy-faculty:heading:015` — score 0.2846; relevant=False

> # University of North Alabama — Generative AI Policy: faculty
> ## Faculty
> 
> UNA faculty members are strongly cautioned against using AI grading tools to evaluate student work. While these tools may offer efficiency, they lack the nuanced understanding required to assess critical thinking, creativity, and individual learning needs. Faculty are encouraged to maintain direct involvement in the grading process to ensure fair and meaningful assessment. Any use of AI grading tools should be carefully considered and supplemented with human oversight to preserve academic integrity and instructional quality. If AI grading tools are utilized in a course, this information must be disclosed to students in the course syllabus.

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> # Thông tư 49/2026/TT-BGDĐT — Ứng dụng công nghệ và AI trong giáo dục đại học
> ## Điều 6. Ứng dụng công nghệ trong hoạt động đào tạo
> 
> b) Đào tạo dựa trên công nghệ phải bảo đảm chất lượng, chương trình đào tạo, chuẩn đầu ra, phương thức kiểm tra đánh giá và các điều kiện bảo đảm chất lượng theo quy định của pháp luật về giáo dục đại học và giáo dục nghề nghiệp;
> 
> c) Bảo đảm khả năng tổ chức, quản lý và theo dõi, đánh giá toàn bộ các hoạt động đào tạo, trọng tâm là quá trình học tập của người học; quản lý hồ sơ, quá trình và kết quả học tập của người học, hoạt động dạy của người dạy; ghi nhận trung thực, chính xác dữ liệu phục vụ quản lý, kiểm tra, giám sát và giải trình;
> [tt49-2026-ung-dung-cong-nghe-ai:heading:010](https://luatvietnam.vn/giao-duc/thong-tu-49-2026-tt-bgddt-ung-dung-cong-nghe-trong-giao-duc-dai-hoc-va-nghe-nghiep-439350-d1.html)
> 
> # UEH — Quy định kiểm soát đạo văn và sử dụng AI: quy định chung
> ## Điều 5. Phát hiện và xử lý vi phạm sử dụng AI trong học thuật
> 
> 1. Việc phát hiện và đánh giá vi phạm sử dụng AI trong học thuật do giảng viên phụ trách/người hướng dẫn hoặc hội đồng/đơn vị có thẩm quyền thực hiện, trên cơ sở xem xét các yếu tố: mức độ sử dụng AI, vai trò của AI trong sản phẩm, hành vi thông báo sử dụng hoặc không thông báo, dấu hiệu gian lận hoặc thay thế nhiệm vụ học thuật. UEH không sử dụng kết quả của các công cụ phát hiện nội dụng do AI tạo ra làm căn cứ duy nhất để kết luận vi phạm học thuật. Đánh giá vi phạm sử dụng AI được thực hiện qua trao đổi trực tiếp giữa cá nhân/đơn vị có thẩm quyền và tác giả sử dụng AI.
> [ueh-dao-van-ai-quy-dinh-chung:heading:019](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
> 
> # University of North Alabama — Generative AI Policy: faculty
> ## Faculty
> 
> UNA faculty members are strongly cautioned against using AI grading tools to evaluate student work. While these tools may offer efficiency, they lack the nuanced understanding required to assess critical thinking, creativity, and individual learning needs. Faculty are encouraged to maintain direct involvement in the grading process to ensure fair and meaningful assessment. Any use of AI grading tools should be carefully considered and supplemented with human oversight to preserve academic integrity and instructional quality. If AI grading tools are utilized in a course, this information must be disclosed to students in the course syllabus.
> [una-genai-policy-faculty:heading:015](https://www.una.edu/academics/generative-ai-policy.html)


### Q2: Sản phẩm học thuật đã chỉnh sửa nhưng vẫn vi phạm lỗi đạo văn thì xử lý ra sao?

Filter: `{"audience": "student"}`; Hit@3: False; coverage: 0%.

Gold: Trong bối cảnh bài tập học phần của người học: giảng viên phụ trách lập biên bản/thông báo chuyển về đơn vị quản lý để xử lý tùy mức độ vi phạm quy định tại Phụ lục 3.

1. `rmit-vn-academic-integrity-ai:heading:013` — score 0.2415; relevant=False

> # RMIT Vietnam — Academic integrity and appropriate use of AI (students)
> ## Types of academic integrity breaches
> ### Collusion
> 
> What is collusion?
> 
> Collaborating is an essential part of studying. However, there are times when helping or getting help from others isn’t allowed. If you’re doing an individual assignment and get help completing it, or help another student complete their individual assignment, that is collusion, which is a breach of academic integrity.
> 
> Types of collusion
> 
> Collusion can include:
> 
> working with someone else on an assignment that you are supposed to write individually
> 
> copying another student’s work, or letting another student copy your work
> 
> letting someone write part of an assignment for you
> 
> When is collaboration permitted?
> 
> 

2. `rmit-vn-academic-integrity-ai:heading:023` — score 0.1876; relevant=False

> # RMIT Vietnam — Academic integrity and appropriate use of AI (students)
> ## Using Artificial Intelligence (AI) appropriately
> ### Don’t forget:
> 
> AI can get things wrong. Responses can be outdated, biased, or simply made up (this is called hallucinating). Before including anything AI-generated in your work, check it against a credible source that you can verify.

3. `rmit-vn-academic-integrity-ai:heading:024` — score 0.1839; relevant=False

> # RMIT Vietnam — Academic integrity and appropriate use of AI (students)
> ## Using Artificial Intelligence (AI) appropriately
> ### How not to use AI
> 
> You cannot use AI to:
> 
> Complete or contribute to an assessment task when it has not been specifically allowed. Check your course guide or ask your educator if you’re not sure
> 
> Produce ideas that you don't reference and try to pass off as your own
> 
> Produce content that you are unable to understand or explain in your own words.
> 
> Using AI in these ways is a breach of Academic Integrity Policy and may have serious consequences.
> 
> Want to know more about how to use generative AI tools in your learning? Complete the Generative AI for students at RMIT module.

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> # RMIT Vietnam — Academic integrity and appropriate use of AI (students)
> ## Types of academic integrity breaches
> ### Collusion
> 
> What is collusion?
> 
> Collaborating is an essential part of studying. However, there are times when helping or getting help from others isn’t allowed. If you’re doing an individual assignment and get help completing it, or help another student complete their individual assignment, that is collusion, which is a breach of academic integrity.
> 
> Types of collusion
> 
> Collusion can include:
> 
> working with someone else on an assignment that you are supposed to write individually
> 
> copying another student’s work, or letting another student copy your work
> 
> letting someone write part of an assignment for you
> 
> When is collaboration permitted?
> [rmit-vn-academic-integrity-ai:heading:013](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)
> 
> # RMIT Vietnam — Academic integrity and appropriate use of AI (students)
> ## Using Artificial Intelligence (AI) appropriately
> ### Don’t forget:
> 
> AI can get things wrong. Responses can be outdated, biased, or simply made up (this is called hallucinating). Before including anything AI-generated in your work, check it against a credible source that you can verify.
> [rmit-vn-academic-integrity-ai:heading:023](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)
> 
> # RMIT Vietnam — Academic integrity and appropriate use of AI (students)
> ## Using Artificial Intelligence (AI) appropriately
> ### How not to use AI
> 
> You cannot use AI to:
> 
> Complete or contribute to an assessment task when it has not been specifically allowed. Check your course guide or ask your educator if you’re not sure
> 
> Produce ideas that you don't reference and try to pass off as your own
> 
> Produce content that you are unable to understand or explain in your own words.
> 
> Using AI in these ways is a breach of Academic Integrity Policy and may have serious consequences.
> 
> Want to know more about how to use generative AI tools in your learning? Complete the Generative AI for students at RMIT module.
> [rmit-vn-academic-integrity-ai:heading:024](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)


### Q3: Khi ghi nhận việc dùng công cụ AI trong bài làm, câu acknowledgement cần nêu những thông tin gì?

Filter: `null`; Hit@3: False; coverage: 0%.

Gold: Theo hướng dẫn RMIT Library: nêu cách sử dụng AI, tên công cụ và nhà phát triển, năm nội dung AI được người dùng tạo ra. Không bắt buộc phiên bản/ngày dùng trừ khi giảng viên yêu cầu.

1. `ueh-dao-van-ai-quy-dinh-chung:heading:026` — score 0.3510; relevant=False

> # UEH — Quy định kiểm soát đạo văn và sử dụng AI: quy định chung
> ## Điều 7. Điều khoản thi hành
> 
> 1. Quy định này có hiệu lực thi hành kể từ ngày ký ban hành và thay thế quy định trong Quyết định số 4621/QĐ-ĐHKT-VSĐH ngày 15/12/2016. Các đơn vị, tổ chức và cá nhân có liên quan tại UEH có trách nhiệm phổ biến và thực hiện nghiêm túc các nội dung của Quy định này.
> 
> 2. Trong quá trình triển khai, nếu có vấn đề phát sinh, Ban Nghiên cứu – Phát triển và Gắn kết toàn cầu có trách nhiệm tổng hợp, báo cáo và trình Ban Giám đốc Đại học UEH xem xét, quyết định việc điều chỉnh, bổ sung cho phù hợp với tình hình thực tế.
> 
> 

2. `una-genai-policy-faculty:heading:010` — score 0.3311; relevant=False

> # University of North Alabama — Generative AI Policy: faculty
> ## Data Privacy and Security
> ### Information where caution should be used before input into Generative AI tools:
> 
> Content that may contain personal, confidential, proprietary, or sensitive information should only be uploaded after verification that it does not include information that may not be uploaded. Examples include:
> 
> - Course content materials
> - Unpublished academic research or discoveries
> - Meeting notes
> - Presentation notes
> - Research data
> - Email
> - Proprietary or unpublished research data or writing or uploading information on discoveries may compromise your ability to seek a patent or copyright in the future

3. `ueh-xu-ly-vi-pham-nguoi-hoc:heading:005` — score 0.3201; relevant=False

> # UEH — Xử lý vi phạm đạo văn và sử dụng AI đối với người học
> ## Điều 5. Xử lý vi phạm sử dụng AI trong học thuật — áp dụng cho người học
> ### 2.2. Đối với các bài kiểm tra, bài tập, tiểu luận, đồ án, dự án và các bài khác thuộc học phần
> 
> a) Khi bị phát hiện vi phạm lần đầu, người học phải chỉnh sửa và nộp lại bài theo yêu cầu của giảng viên;
> 
> b) Nếu vẫn vi phạm sau khi đã chỉnh sửa, giảng viên phụ trách học phần lập biên bản, thông báo chuyển cho đơn vị quản lý để xử lý tùy theo mức độ vi phạm.

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> # UEH — Quy định kiểm soát đạo văn và sử dụng AI: quy định chung
> ## Điều 7. Điều khoản thi hành
> 
> 1. Quy định này có hiệu lực thi hành kể từ ngày ký ban hành và thay thế quy định trong Quyết định số 4621/QĐ-ĐHKT-VSĐH ngày 15/12/2016. Các đơn vị, tổ chức và cá nhân có liên quan tại UEH có trách nhiệm phổ biến và thực hiện nghiêm túc các nội dung của Quy định này.
> 
> 2. Trong quá trình triển khai, nếu có vấn đề phát sinh, Ban Nghiên cứu – Phát triển và Gắn kết toàn cầu có trách nhiệm tổng hợp, báo cáo và trình Ban Giám đốc Đại học UEH xem xét, quyết định việc điều chỉnh, bổ sung cho phù hợp với tình hình thực tế.
> [ueh-dao-van-ai-quy-dinh-chung:heading:026](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
> 
> # University of North Alabama — Generative AI Policy: faculty
> ## Data Privacy and Security
> ### Information where caution should be used before input into Generative AI tools:
> 
> Content that may contain personal, confidential, proprietary, or sensitive information should only be uploaded after verification that it does not include information that may not be uploaded. Examples include:
> 
> - Course content materials
> - Unpublished academic research or discoveries
> - Meeting notes
> - Presentation notes
> - Research data
> - Email
> - Proprietary or unpublished research data or writing or uploading information on discoveries may compromise your ability to seek a patent or copyright in the future
> [una-genai-policy-faculty:heading:010](https://www.una.edu/academics/generative-ai-policy.html)
> 
> # UEH — Xử lý vi phạm đạo văn và sử dụng AI đối với người học
> ## Điều 5. Xử lý vi phạm sử dụng AI trong học thuật — áp dụng cho người học
> ### 2.2. Đối với các bài kiểm tra, bài tập, tiểu luận, đồ án, dự án và các bài khác thuộc học phần
> 
> a) Khi bị phát hiện vi phạm lần đầu, người học phải chỉnh sửa và nộp lại bài theo yêu cầu của giảng viên;
> 
> b) Nếu vẫn vi phạm sau khi đã chỉnh sửa, giảng viên phụ trách học phần lập biên bản, thông báo chuyển cho đơn vị quản lý để xử lý tùy theo mức độ vi phạm.
> [ueh-xu-ly-vi-pham-nguoi-hoc:heading:005](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)


### Q4: Những loại thông tin nào không được phép nhập vào công cụ AI tạo sinh?

Filter: `null`; Hit@3: False; coverage: 0%.

Gold: Theo snapshot UNA, không nhập thông tin cá nhân, bí mật, độc quyền hoặc nhạy cảm: ví dụ hồ sơ sinh viên/tuyển sinh, số an sinh xã hội, dữ liệu thẻ/ngân hàng, giấy tờ định danh, dữ liệu y tế/bảo hiểm, dữ liệu người tham gia nghiên cứu chưa được đồng ý công khai, hồ sơ nội bộ và nội dung thuộc NDA/sở hữu trí tuệ chưa được phép. Danh sách ví dụ không giới hạn ở một loại dữ liệu.

1. `ueh-xu-ly-vi-pham-giang-vien:heading:002` — score 0.3324; relevant=False

> # UEH — Xử lý vi phạm đạo văn và sử dụng AI đối với giảng viên, viên chức
> ## Điều 3. Xử lý hành vi đạo văn — áp dụng cho viên chức, người lao động, giảng viên thỉnh giảng
> ### 2.4 Đối với sản phẩm học thuật của viên chức, người lao động, giảng viên thỉnh giảng của UE
> 
> Nếu phát hiện vi phạm đạo văn, tác giả phải chịu trách nhiệm theo quy định của UEH và pháp luật hiện hành; đồng thời thực hiện các nghĩa vụ liên quan như báo cáo đơn vị phát hành, rút bài, cải chính hoặc thu hồi (nếu có nhu cầu).

2. `una-genai-policy-faculty:heading:012` — score 0.2530; relevant=False

> # University of North Alabama — Generative AI Policy: faculty
> ## Data Privacy and Security
> ### Personal liability for publication on ChatGPT
> 
> ChatGPT uses a click-through agreement.  Click-through agreements, including OpenAI and ChatGPT terms of use, are contracts. Individuals who accept click-through agreements without delegated signature authority may face personal consequences, including responsibility for compliance with terms and conditions.
> 
> For questions regarding data privacy, contact Information Technology Services.

3. `rmit-vn-academic-integrity-ai:heading:023` — score 0.2489; relevant=False

> # RMIT Vietnam — Academic integrity and appropriate use of AI (students)
> ## Using Artificial Intelligence (AI) appropriately
> ### Don’t forget:
> 
> AI can get things wrong. Responses can be outdated, biased, or simply made up (this is called hallucinating). Before including anything AI-generated in your work, check it against a credible source that you can verify.

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> # UEH — Xử lý vi phạm đạo văn và sử dụng AI đối với giảng viên, viên chức
> ## Điều 3. Xử lý hành vi đạo văn — áp dụng cho viên chức, người lao động, giảng viên thỉnh giảng
> ### 2.4 Đối với sản phẩm học thuật của viên chức, người lao động, giảng viên thỉnh giảng của UE
> 
> Nếu phát hiện vi phạm đạo văn, tác giả phải chịu trách nhiệm theo quy định của UEH và pháp luật hiện hành; đồng thời thực hiện các nghĩa vụ liên quan như báo cáo đơn vị phát hành, rút bài, cải chính hoặc thu hồi (nếu có nhu cầu).
> [ueh-xu-ly-vi-pham-giang-vien:heading:002](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)
> 
> # University of North Alabama — Generative AI Policy: faculty
> ## Data Privacy and Security
> ### Personal liability for publication on ChatGPT
> 
> ChatGPT uses a click-through agreement.  Click-through agreements, including OpenAI and ChatGPT terms of use, are contracts. Individuals who accept click-through agreements without delegated signature authority may face personal consequences, including responsibility for compliance with terms and conditions.
> 
> For questions regarding data privacy, contact Information Technology Services.
> [una-genai-policy-faculty:heading:012](https://www.una.edu/academics/generative-ai-policy.html)
> 
> # RMIT Vietnam — Academic integrity and appropriate use of AI (students)
> ## Using Artificial Intelligence (AI) appropriately
> ### Don’t forget:
> 
> AI can get things wrong. Responses can be outdated, biased, or simply made up (this is called hallucinating). Before including anything AI-generated in your work, check it against a credible source that you can verify.
> [rmit-vn-academic-integrity-ai:heading:023](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)


### Q5: Thông tư 49/2026/TT-BGDĐT có hiệu lực từ ngày nào và thay thế những thông tư nào?

Filter: `null`; Hit@3: False; coverage: 0%.

Gold: Theo Điều 22 trong snapshot nhóm cung cấp: hiệu lực từ 15/08/2026; Thông tư 15/2018/TT-BGDĐT và 30/2023/TT-BGDĐT hết hiệu lực từ ngày đó. Đây là gold answer kiểm thử snapshot, chưa xác minh tình trạng pháp lý hiện hành.

1. `rmit-vn-academic-integrity-ai:heading:003` — score 0.2616; relevant=False

> # RMIT Vietnam — Academic integrity and appropriate use of AI (students)
> ## What is academic integrity?
> 
> When working on assessments, it’s essential to know your academic integrity responsibilities. In practical terms, academic integrity means developing and submitting for assessment your own academic work. Some breaches of academic integrity include plagiarism, collusion and contract cheating, which all have serious consequences. Sometimes, the inappropriate use of AI in your studies can result in a breach.
> 
> Academic integrity has been more formally defined as ‘the expectation that teachers, students, researchers and all members of the academic community act with: honesty, trust, fairness, respect and responsibility.’
> 
> 

2. `rmit-vn-academic-integrity-ai:heading:016` — score 0.2552; relevant=False

> # RMIT Vietnam — Academic integrity and appropriate use of AI (students)
> ## Types of academic integrity breaches
> ### Fabrication and falsification
> 
> Falsification involves the manipulation or misrepresentation of research data, source material or results, or the presentation of results that are not supported by the evidence. In other words, changing real data.
> 
> An example might be deleting “inconvenient” data points to make your graph look better, or changing dates/times on experiments to fit your hypothesis.
> 
> How to avoid fabrication and falsification
> 
> Only ever use real and credible research, data and information. Don’t make it up!
> 
> Be open about problems such as missing, messy, or unexpected results, and explain these limitations instead of trying to ‘fix’ them
> 
> 

3. `tt49-2026-ung-dung-cong-nghe-ai:heading:017` — score 0.2260; relevant=False

> # Thông tư 49/2026/TT-BGDĐT — Ứng dụng công nghệ và AI trong giáo dục đại học
> ## Điều 10. Bảo đảm liêm chính học thuật khi ứng dụng công nghệ
> 
> a) Cơ sở giáo dục ban hành quy định nội bộ về liêm chính học thuật, trong đó xác định rõ các hành vi vi phạm, biện pháp phòng ngừa, quy trình xử lý và trách nhiệm của các bên liên quan; tổ chức phổ biến, tuyên truyền, nâng cao nhận thức về liêm chính học thuật; áp dụng các biện pháp phù hợp để phòng ngừa, phát hiện và xử lý vi phạm;
> 
> b) Người học, giảng viên và các bên liên quan tuân thủ quy định về liêm chính học thuật; trung thực trong hoạt động học thuật; công bố việc sử dụng công nghệ, trí tuệ nhân tạo theo quy định và chịu trách nhiệm về sản phẩm học tập, giảng dạy và nghiên cứu của mình.

**Agent output:**

> [EXTRACTIVE BASELINE — không phải LLM]
> 
> # RMIT Vietnam — Academic integrity and appropriate use of AI (students)
> ## What is academic integrity?
> 
> When working on assessments, it’s essential to know your academic integrity responsibilities. In practical terms, academic integrity means developing and submitting for assessment your own academic work. Some breaches of academic integrity include plagiarism, collusion and contract cheating, which all have serious consequences. Sometimes, the inappropriate use of AI in your studies can result in a breach.
> 
> Academic integrity has been more formally defined as ‘the expectation that teachers, students, researchers and all members of the academic community act with: honesty, trust, fairness, respect and responsibility.’
> [rmit-vn-academic-integrity-ai:heading:003](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)
> 
> # RMIT Vietnam — Academic integrity and appropriate use of AI (students)
> ## Types of academic integrity breaches
> ### Fabrication and falsification
> 
> Falsification involves the manipulation or misrepresentation of research data, source material or results, or the presentation of results that are not supported by the evidence. In other words, changing real data.
> 
> An example might be deleting “inconvenient” data points to make your graph look better, or changing dates/times on experiments to fit your hypothesis.
> 
> How to avoid fabrication and falsification
> 
> Only ever use real and credible research, data and information. Don’t make it up!
> 
> Be open about problems such as missing, messy, or unexpected results, and explain these limitations instead of trying to ‘fix’ them
> [rmit-vn-academic-integrity-ai:heading:016](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)
> 
> # Thông tư 49/2026/TT-BGDĐT — Ứng dụng công nghệ và AI trong giáo dục đại học
> ## Điều 10. Bảo đảm liêm chính học thuật khi ứng dụng công nghệ
> 
> a) Cơ sở giáo dục ban hành quy định nội bộ về liêm chính học thuật, trong đó xác định rõ các hành vi vi phạm, biện pháp phòng ngừa, quy trình xử lý và trách nhiệm của các bên liên quan; tổ chức phổ biến, tuyên truyền, nâng cao nhận thức về liêm chính học thuật; áp dụng các biện pháp phù hợp để phòng ngừa, phát hiện và xử lý vi phạm;
> 
> b) Người học, giảng viên và các bên liên quan tuân thủ quy định về liêm chính học thuật; trung thực trong hoạt động học thuật; công bố việc sử dụng công nghệ, trí tuệ nhân tạo theo quy định và chịu trách nhiệm về sản phẩm học tập, giảng dạy và nghiên cứu của mình.
> [tt49-2026-ung-dung-cong-nghe-ai:heading:017](https://luatvietnam.vn/giao-duc/thong-tu-49-2026-tt-bgddt-ung-dung-cong-nghe-trong-giao-duc-dai-hoc-va-nghe-nghiep-439350-d1.html)

