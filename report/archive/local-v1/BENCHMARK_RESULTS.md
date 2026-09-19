# Kết quả benchmark thực chạy

Python 3.11.9; tfidf-word-unigram-l2 (lexical, offline).

Agent là extractive baseline, không phải LLM. Không tự quy đổi thành điểm rubric.
Hit@3 = tỷ lệ câu hỏi có ít nhất một chunk chứa gold span đúng tài liệu;
MRR@3 = trung bình nghịch đảo thứ hạng đầu tiên; Precision@3 dùng mẫu số 3 kể cả khi thiếu kết quả.
Gold-span matching có thể bỏ sót bằng chứng tương đương; không thay thế đánh giá thủ công.

| Backend | Strategy | Chunks | Avg chars | Hit@3 | MRR@3 | Precision@3 |
|---|---|---:|---:|---:|---:|---:|
| tfidf | fixed_size | 92 | 762.9 | 100% | 1.000 | 0.333 |
| tfidf | by_sentences | 133 | 476.0 | 80% | 0.700 | 0.267 |
| tfidf | recursive | 102 | 623.8 | 80% | 0.800 | 0.267 |
| tfidf | heading | 145 | 542.8 | 100% | 1.000 | 0.333 |
| mock | fixed_size | 92 | 762.9 | 40% | 0.167 | 0.133 |
| mock | by_sentences | 133 | 476.0 | 20% | 0.067 | 0.067 |
| mock | recursive | 102 | 623.8 | 20% | 0.100 | 0.067 |
| mock | heading | 145 | 542.8 | 20% | 0.200 | 0.067 |

## tfidf / fixed_size

### Q1: Tại UEH, sau khi chỉnh sửa nhưng vẫn vi phạm sử dụng AI trong học thuật thì xử lý thế nào?

Filter: `{"audience": "student"}`; Hit@3: True; coverage: 100%.

Gold: Với người học, giảng viên phụ trách học phần lập biên bản, thông báo chuyển cho đơn vị quản lý để xử lý tùy theo mức độ vi phạm.

1. `ueh-xu-ly-vi-pham-nguoi-hoc:fixed_size:003` — score 0.4235; relevant=True

> c phải chỉnh sửa và nộp lại bài theo yêu cầu của giảng viên;
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

2. `ueh-xu-ly-vi-pham-nguoi-hoc:fixed_size:001` — score 0.4181; relevant=False

> Sau bảo vệ:
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
> 
> Người học phải chỉnh sửa và khắc phục vi phạm theo yêu cầu của giảng viên hướng dẫn h

3. `ueh-xu-ly-vi-pham-nguoi-hoc:fixed_size:002` — score 0.3269; relevant=False

>  học phải chỉnh sửa và khắc phục vi phạm theo yêu cầu của giảng viên hướng dẫn hoặc đơn vị quản lý.
> 
> b) Trong quá trình bảo vệ hoặc đánh giá:
> 
> Nếu Hội đồng đánh giá đề án tốt nghiệp, luận văn, luận án hoặc giảng viên phụ trách phát hiện vi phạm sử dụng AI trong học thuật, chủ tịch hội đồng/giảng viên phụ trách quyết định khóa luận, đề án tốt nghiệp, luận văn, luận án không đạt, người học phải chỉnh sửa lại sản phẩm và khắc phục vi phạm.
> 
> c) Sau khi đã bảo vệ:
> 
> Nếu phát hiện vi phạm sử dụng AI, tác giả chịu trách nhiệm theo các quy định của UEH và pháp luật hiện hành.
> 
> ### 2.2. Đối với các bài kiểm tra, bài tập, tiểu luận, đồ án, dự án và các bài khác thuộc học phần
> 
> a) Khi bị phát hiện vi phạm lần đầu, người học phải chỉnh sửa và nộp lại bài theo yêu cầu của giảng viên;
> 
> b) Nếu vẫn vi phạm

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

b) Nếu vẫn vi phạm sau khi đã chỉnh sửa, giảng viên phụ trách học phần lập biên bản, thông báo chuyển cho đơn vị quản lý để xử lý tùy theo mức độ vi phạm.
[ueh-xu-ly-vi-pham-nguoi-hoc:fixed_size:003](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

b) Sau khi đã chỉnh sửa, người học nộp lại bài nhưng vẫn vi phạm lỗi đạo văn thì giảng viên phụ trách học phần lập biên bản/thông báo chuyển về đơn vị quản lý để xử lý tùy theo mức độ vi phạm quy định tại Phụ lục 3.
[ueh-xu-ly-vi-pham-nguoi-hoc:fixed_size:001](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

b) Nếu vẫn vi phạm
[ueh-xu-ly-vi-pham-nguoi-hoc:fixed_size:002](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)


### Q2: Theo UEH, tỷ lệ tương đồng học thuật có phải là căn cứ duy nhất để kết luận đạo văn không?

Filter: `null`; Hit@3: True; coverage: 100%.

Gold: Không. Tỷ lệ tương đồng không phải căn cứ duy nhất; cần xem xét chuyên môn của đơn vị quản lý, giảng viên hoặc hội đồng có thẩm quyền.

1. `ueh-dao-van-ai-quy-dinh-chung:fixed_size:002` — score 0.5374; relevant=True

>  thuật
> 
> Tỷ lệ tương đồng học thuật là tỷ lệ phần trăm nội dung trùng lặp trong sản phẩm học thuật được xác định bằng phần mềm hỗ trợ (Turnitin hoặc các công cụ kiểm tra đạo văn có chức năng so sánh với cơ sở dữ liệu học thuật rộng và cho phép phân tích chi tiết mức độ trùng lặp, được UEH phê duyệt sử dụng). Tỷ lệ tương đồng không phải là căn cứ duy nhất để kết luận đạo văn; việc đánh giá phải dựa trên xem xét chuyên môn của đơn vị quản lý, giảng viên hoặc hội đồng có thẩm quyền.
> 
> ### Các dấu hiệu của hành vi đạo văn hoặc vi phạm liêm chính học thuật
> 
> Sản phẩm học thuật có thể xem là có dấu hiệu vi phạm nếu có ít nhất một trong các biểu hiện sau:
> 
> a) Dấu hiệu định lượng từ phần mềm kiểm tra
> 
> - Có tỷ lệ tương đồng từ 20% trở lên (không tính phần: trích dẫn, danh mục tài liệu tham khảo, phần 

2. `ueh-dao-van-ai-quy-dinh-chung:fixed_size:005` — score 0.4554; relevant=False

> ng cụ tương đương để phát hiện tỷ lệ tương đồng học thuật trong các sản phẩm học thuật. Kết quả tỷ lệ tương đồng chỉ mang tính tham khảo, hỗ trợ, không tự động kết luận là đạo văn. Việc kết luận dựa trên xem xét bối cảnh, phạm vi, tính chất nội dung trùng lặp, ý chí của người thực hiện và các chứng cứ liên quan. Việc đánh giá do giảng viên phụ trách/người hướng dẫn hoặc hội đồng/đơn vị có thẩm quyền thực hiện theo quy trình được UEH quy định.
> 
> 2. Xử lý hành vi đạo văn
> 
> ### 2.1 Nguyên tắc xử lý hành vi đạo văn
> 
> Việc xử lý được căn cứ trên mức độ nghiêm trọng, tính lặp lại và động cơ của hành vi:
> 
> - Đối với các hành vi có tính chất chiếm đoạt nội dung, cố ý gian lận học thuật, xử lý theo hướng kỷ luật học thuật nghiêm khắc theo quy định hiện hành của UEH và pháp luật có liên quan.
> - Đối với 

3. `ueh-dao-van-ai-quy-dinh-chung:fixed_size:001` — score 0.3758; relevant=False

> u chỉnh của Quy định bao gồm, nhưng không giới hạn: bài báo khoa học, báo cáo nghiên cứu khoa học, bài tham luận tại hội thảo, khóa luận tốt nghiệp, đề án tốt nghiệp, luận văn thạc sĩ, luận án tiến sĩ, bài tập, tiểu luận, chuyên đề và các dạng sản phẩm học thuật khác do UEH quy định hoặc công nhận.
> 
> ## Điều 2. Nhận diện và xác định hành vi đạo văn
> 
> ### Khái niệm đạo văn
> 
> Đạo văn là hành vi sử dụng trực tiếp hoặc gián tiếp, toàn bộ hoặc một phần ý tưởng, dữ liệu, ngôn từ, hình ảnh, mô hình, sản phẩm học thuật của người khác mà không ghi nhận, trích dẫn hoặc chú thích phù hợp; hoặc tái sử dụng sản phẩm học thuật của chính mình (tự đạo văn) mà không nêu rõ nguồn gốc và tình trạng công bố.
> 
> ### Tỷ lệ tương đồng học thuật
> 
> Tỷ lệ tương đồng học thuật là tỷ lệ phần trăm nội dung trùng lặp trong s

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

Tỷ lệ tương đồng học thuật là tỷ lệ phần trăm nội dung trùng lặp trong sản phẩm học thuật được xác định bằng phần mềm hỗ trợ (Turnitin hoặc các công cụ kiểm tra đạo văn có chức năng so sánh với cơ sở dữ liệu học thuật rộng và cho phép phân tích chi tiết mức độ trùng lặp, được UEH phê duyệt sử dụng). Tỷ lệ tương đồng không phải là căn cứ duy nhất để kết luận đạo văn; việc đánh giá phải dựa trên xem xét chuyên môn của đơn vị quản lý, giảng viên hoặc hội đồng có thẩm quyền.
[ueh-dao-van-ai-quy-dinh-chung:fixed_size:002](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

ng cụ tương đương để phát hiện tỷ lệ tương đồng học thuật trong các sản phẩm học thuật. Kết quả tỷ lệ tương đồng chỉ mang tính tham khảo, hỗ trợ, không tự động kết luận là đạo văn. Việc kết luận dựa trên xem xét bối cảnh, phạm vi, tính chất nội dung trùng lặp, ý chí của người thực hiện và các chứng cứ liên quan. Việc đánh giá do giảng viên phụ trách/người hướng dẫn hoặc hội đồng/đơn vị có thẩm quyền thực hiện theo quy trình được UEH quy định.
[ueh-dao-van-ai-quy-dinh-chung:fixed_size:005](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

Tỷ lệ tương đồng học thuật là tỷ lệ phần trăm nội dung trùng lặp trong s
[ueh-dao-van-ai-quy-dinh-chung:fixed_size:001](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)


### Q3: According to RMIT Library, what records of AI prompts and outputs should students save?

Filter: `{"audience": "student"}`; Hit@3: True; coverage: 100%.

Gold: Keep a record of prompts, generated outputs and how the content was used; save copies because an educator may request them.

1. `rmit-ai-acknowledgement-guide:fixed_size:001` — score 0.2918; relevant=True

> nt of what AI tools were used and how they were used within the body or methods section of your work.
> 
> If you include any AI-generated outputs (such as text, images or code) in your work, you need to include a citation and a reference - see the citing and referencing guidelines page of this guide for more details.
> 
> ## Overall guidelines for acknowledging the use of AI tools
> 
> Check your assessment task instructions and/or assignment declaration for specific advice
> 
> Keep a record of how you have used AI tools in the process of creating your work, including the prompt used, the outputs generated, and how the generated content was used in your work.
> 
> Make sure you save a copy of the prompts used and outputs generated, as you may need to provide this to your educator on request.
> 
> ## Template fo

2. `rmit-vn-academic-integrity-ai:fixed_size:000` — score 0.2189; relevant=False

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
> When working on assessments, it’s essential to know your academic integrity responsibilities. In practical terms, academic integrity means developing and submitting for assessment your own academic work. Some breaches of academic integrity include plagiarism, collusion and contract cheating, which all have serious consequences. Someti

3. `rmit-ai-acknowledgement-guide:fixed_size:000` — score 0.2073; relevant=False

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
> In such cases, you will not include AI-generated content directly in your final work, e.g. you are using AI tools in the process of creating the work.
> 
> For this type of AI use, however, you need to include an acknowledgement of what AI tools were used and how they were used within the body or methods 

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

Make sure you save a copy of the prompts used and outputs generated, as you may need to provide this to your educator on request.
[rmit-ai-acknowledgement-guide:fixed_size:001](https://rmit.libguides.com/referencing_AI_tools/acknowledging)

Learn about academic integrity, what happens if you breach it and where to get help if you're unsure.
[rmit-vn-academic-integrity-ai:fixed_size:000](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)

For this type of AI use, however, you need to include an acknowledgement of what AI tools were used and how they were used within the body or methods
[rmit-ai-acknowledgement-guide:fixed_size:000](https://rmit.libguides.com/referencing_AI_tools/acknowledging)


### Q4: At UNA, should faculty use AI-detection software as the single means of verifying originality?

Filter: `{"audience": "faculty"}`; Hit@3: True; coverage: 100%.

Gold: No. Faculty should avoid using AI-detection software as the single means of verifying originality.

1. `una-genai-policy-faculty:fixed_size:009` — score 0.4218; relevant=True

> rative AI to enhance teaching and learning experiences while maintaining academic integrity.
> 
> Faculty should include an AI Policy Statement in each course syllabus. (Template language included at the end of this policy).
> 
> Be transparent about the use of AI-generated content in course materials.
> 
> Encourage students to use AI responsibly and ethically.
> 
> Avoid using AI-detection software as the single means of verifying originality.
> 
> UNA faculty members are strongly cautioned against using AI grading tools to evaluate student work. While these tools may offer efficiency, they lack the nuanced understanding required to assess critical thinking, creativity, and individual learning needs. Faculty are encouraged to maintain direct involvement in the grading process to ensure fair and meaningful a

2. `una-genai-policy-faculty:fixed_size:002` — score 0.2135; relevant=False

>  Syllabus Policy Statements from The University of Texas at Austin, Center for Teaching and Learning
> 
> Faculty should explicitly define and explain the acceptable use of AI in the course syllabus, assignments, and rubrics/grading guides. Sample language will be provided in Simple Syllabus and can be customized. Faculty members who use AI to create lesson plans, assignments, rubrics, reading lists, and other class documents should acknowledge the use of AI to model academic integrity practices.
> 
> When using generative AI, users must acknowledge the use of AI-generated content by properly citing AI-generated content in academic work and ensuring that AI-generated content does not violate academic integrity policies. Faculty should review the appropriate procedures for documenting AIgenerated c

3. `una-genai-policy-faculty:fixed_size:000` — score 0.2078; relevant=False

> # University of North Alabama — Generative AI Policy: faculty
> 
> ## Academic Integrity
> 
> The University of North Alabama acknowledges that faculty have complete discretion in establishing acceptable use of Generative AI (and other assistive tools) in their courses, so long as that use complies with existing university policies such as Faculty Handbook policies, Academic Honesty policies, IT Acceptable Use policies, and Privacy policies. The University offers the following guidance for crafting syllabus policies:
> 
> Faculty should explicitly define and explain the acceptable use of AI in the course syllabus, assignments, and rubrics/grading guides. Sample language will be provided in Simple Syllabus and can be customized. Faculty members who use AI to create lesson plans, assignments, rubrics, r

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

Avoid using AI-detection software as the single means of verifying originality.
[una-genai-policy-faculty:fixed_size:009](https://www.una.edu/academics/generative-ai-policy.html)

When using generative AI, users must acknowledge the use of AI-generated content by properly citing AI-generated content in academic work and ensuring that AI-generated content does not violate academic integrity policies. Faculty should review the appropriate procedures for documenting AIgenerated c
[una-genai-policy-faculty:fixed_size:002](https://www.una.edu/academics/generative-ai-policy.html)

Faculty should explicitly define and explain the acceptable use of AI in the course syllabus, assignments, and rubrics/grading guides. Sample language will be provided in Simple Syllabus and can be customized. Faculty members who use AI to create lesson plans, assignments, rubrics, r
[una-genai-policy-faculty:fixed_size:000](https://www.una.edu/academics/generative-ai-policy.html)


### Q5: At UNA, what information may staff not share with generative AI, and may they create AI-generated promotional images?

Filter: `{"audience": "staff"}`; Hit@3: True; coverage: 100%.

Gold: Staff must avoid sharing confidential information, including student data protected under FERPA. Creating AI-generated images for promotional materials is not allowed in the supplied policy.

1. `una-genai-policy-staff:fixed_size:000` — score 0.3440; relevant=True

> # University of North Alabama — Generative AI Policy: staff
> 
> ## Staff
> 
> Use generative AI to improve administrative processes and decision-making.
> 
> Ensure data privacy and security when using AI tools in daily tasks.
> 
> Stay informed about the latest AI developments and best practices.
> 
> UNA staff and faculty are permitted to use generative AI responsibly to assist in their work. However, users must exercise caution to avoid sharing confidential information, including student data protected under FERPA guidelines, when using AI tools. Additionally, the creation of AI-generated images for promotional materials is not allowed, as such content may conflict with UNA’s branding standards, copyright regulations, and institutional values. To ensure that all promotional materials remain on brand and i

2. `una-genai-policy-staff:fixed_size:001` — score 0.1990; relevant=False

> itutional values. To ensure that all promotional materials remain on brand and in compliance with institutional and legal standards,
> 
> the Office of Enrollment Marketing & Digital Communications is available to assist in developing any needed promotional images.
> 
> Work with IT Services prior to the use of AI for administrative purposes to help ensure data security, data integrity, integration needs, and data confidentiality

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

UNA staff and faculty are permitted to use generative AI responsibly to assist in their work. However, users must exercise caution to avoid sharing confidential information, including student data protected under FERPA guidelines, when using AI tools. Additionally, the creation of AI-generated images for promotional materials is not allowed, as such content may conflict with UNA’s branding standards, copyright regulations, and institutional values. To ensure that all promotional materials remain on brand and i
[una-genai-policy-staff:fixed_size:000](https://www.una.edu/academics/generative-ai-policy.html)

itutional values. To ensure that all promotional materials remain on brand and in compliance with institutional and legal standards,
[una-genai-policy-staff:fixed_size:001](https://www.una.edu/academics/generative-ai-policy.html)


## tfidf / by_sentences

### Q1: Tại UEH, sau khi chỉnh sửa nhưng vẫn vi phạm sử dụng AI trong học thuật thì xử lý thế nào?

Filter: `{"audience": "student"}`; Hit@3: True; coverage: 100%.

Gold: Với người học, giảng viên phụ trách học phần lập biên bản, thông báo chuyển cho đơn vị quản lý để xử lý tùy theo mức độ vi phạm.

1. `ueh-xu-ly-vi-pham-nguoi-hoc:by_sentences:001` — score 0.3639; relevant=False

> c) Sau bảo vệ:
> 
> Sau khi đã bảo vệ, nếu có phát hiện lỗi đạo văn, tác giả chịu trách nhiệm theo các quy định của UEH và pháp luật hiện hành. ### 2.3 Đối với các bài kiểm tra, bài tập, tiểu luận và các bài khác thuộc các học phần
> 
> a) Khi bị phát hiện vi phạm lần đầu, người học phải chỉnh sửa và nộp lại bài theo yêu cầu của giảng viên;
> 
> b) Sau khi đã chỉnh sửa, người học nộp lại bài nhưng vẫn vi phạm lỗi đạo văn thì giảng viên phụ trách học phần lập biên bản/thông báo chuyển về đơn vị quản lý để xử lý tùy theo mức độ vi phạm quy định tại Phụ lục 3. ## Điều 5.

2. `ueh-xu-ly-vi-pham-nguoi-hoc:by_sentences:003` — score 0.3615; relevant=True

> c) Sau khi đã bảo vệ:
> 
> Nếu phát hiện vi phạm sử dụng AI, tác giả chịu trách nhiệm theo các quy định của UEH và pháp luật hiện hành. ### 2.2. Đối với các bài kiểm tra, bài tập, tiểu luận, đồ án, dự án và các bài khác thuộc học phần
> 
> a) Khi bị phát hiện vi phạm lần đầu, người học phải chỉnh sửa và nộp lại bài theo yêu cầu của giảng viên;
> 
> b) Nếu vẫn vi phạm sau khi đã chỉnh sửa, giảng viên phụ trách học phần lập biên bản, thông báo chuyển cho đơn vị quản lý để xử lý tùy theo mức độ vi phạm.

3. `ueh-xu-ly-vi-pham-nguoi-hoc:by_sentences:002` — score 0.3363; relevant=False

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

[EXTRACTIVE BASELINE — không phải LLM]

b) Sau khi đã chỉnh sửa, người học nộp lại bài nhưng vẫn vi phạm lỗi đạo văn thì giảng viên phụ trách học phần lập biên bản/thông báo chuyển về đơn vị quản lý để xử lý tùy theo mức độ vi phạm quy định tại Phụ lục 3. ## Điều 5.
[ueh-xu-ly-vi-pham-nguoi-hoc:by_sentences:001](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

b) Nếu vẫn vi phạm sau khi đã chỉnh sửa, giảng viên phụ trách học phần lập biên bản, thông báo chuyển cho đơn vị quản lý để xử lý tùy theo mức độ vi phạm.
[ueh-xu-ly-vi-pham-nguoi-hoc:by_sentences:003](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

Xử lý vi phạm sử dụng AI trong học thuật — áp dụng cho người học
[ueh-xu-ly-vi-pham-nguoi-hoc:by_sentences:002](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)


### Q2: Theo UEH, tỷ lệ tương đồng học thuật có phải là căn cứ duy nhất để kết luận đạo văn không?

Filter: `null`; Hit@3: True; coverage: 100%.

Gold: Không. Tỷ lệ tương đồng không phải căn cứ duy nhất; cần xem xét chuyên môn của đơn vị quản lý, giảng viên hoặc hội đồng có thẩm quyền.

1. `ueh-dao-van-ai-quy-dinh-chung:by_sentences:002` — score 0.5061; relevant=True

> ### Tỷ lệ tương đồng học thuật
> 
> Tỷ lệ tương đồng học thuật là tỷ lệ phần trăm nội dung trùng lặp trong sản phẩm học thuật được xác định bằng phần mềm hỗ trợ (Turnitin hoặc các công cụ kiểm tra đạo văn có chức năng so sánh với cơ sở dữ liệu học thuật rộng và cho phép phân tích chi tiết mức độ trùng lặp, được UEH phê duyệt sử dụng). Tỷ lệ tương đồng không phải là căn cứ duy nhất để kết luận đạo văn; việc đánh giá phải dựa trên xem xét chuyên môn của đơn vị quản lý, giảng viên hoặc hội đồng có thẩm quyền. ### Các dấu hiệu của hành vi đạo văn hoặc vi phạm liêm chính học thuật
> 
> Sản phẩm học thuật có thể xem là có dấu hiệu vi phạm nếu có ít nhất một trong các biểu hiện sau:
> 
> a) Dấu hiệu định lượng từ phần mềm kiểm tra
> 
> - Có tỷ lệ tương đồng từ 20% trở lên (không tính phần: trích dẫn, danh mục tài liệu tham khảo, phần mô tả phương pháp mang tính lặp lại và phổ biến trong chuyên ngành, các thuật ngữ chuyên ngành, tiêu chuẩn kỹ thuật, trích dẫn văn bản quy phạm pháp luật, tên riêng không thể thay thế).

2. `ueh-dao-van-ai-quy-dinh-chung:by_sentences:007` — score 0.4179; relevant=False

> ## Điều 3. Phát hiện và xử lý hành vi đạo văn
> 
> 1. UEH sử dụng phần mềm Turnitin và/hoặc công cụ tương đương để phát hiện tỷ lệ tương đồng học thuật trong các sản phẩm học thuật.

3. `ueh-dao-van-ai-quy-dinh-chung:by_sentences:008` — score 0.3905; relevant=False

> Kết quả tỷ lệ tương đồng chỉ mang tính tham khảo, hỗ trợ, không tự động kết luận là đạo văn. Việc kết luận dựa trên xem xét bối cảnh, phạm vi, tính chất nội dung trùng lặp, ý chí của người thực hiện và các chứng cứ liên quan. Việc đánh giá do giảng viên phụ trách/người hướng dẫn hoặc hội đồng/đơn vị có thẩm quyền thực hiện theo quy trình được UEH quy định.

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

Tỷ lệ tương đồng học thuật là tỷ lệ phần trăm nội dung trùng lặp trong sản phẩm học thuật được xác định bằng phần mềm hỗ trợ (Turnitin hoặc các công cụ kiểm tra đạo văn có chức năng so sánh với cơ sở dữ liệu học thuật rộng và cho phép phân tích chi tiết mức độ trùng lặp, được UEH phê duyệt sử dụng). Tỷ lệ tương đồng không phải là căn cứ duy nhất để kết luận đạo văn; việc đánh giá phải dựa trên xem xét chuyên môn của đơn vị quản lý, giảng viên hoặc hội đồng có thẩm quyền. ### Các dấu hiệu của hành vi đạo văn hoặc vi phạm liêm chính học thuật
[ueh-dao-van-ai-quy-dinh-chung:by_sentences:002](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

1. UEH sử dụng phần mềm Turnitin và/hoặc công cụ tương đương để phát hiện tỷ lệ tương đồng học thuật trong các sản phẩm học thuật.
[ueh-dao-van-ai-quy-dinh-chung:by_sentences:007](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

Kết quả tỷ lệ tương đồng chỉ mang tính tham khảo, hỗ trợ, không tự động kết luận là đạo văn. Việc kết luận dựa trên xem xét bối cảnh, phạm vi, tính chất nội dung trùng lặp, ý chí của người thực hiện và các chứng cứ liên quan. Việc đánh giá do giảng viên phụ trách/người hướng dẫn hoặc hội đồng/đơn vị có thẩm quyền thực hiện theo quy trình được UEH quy định.
[ueh-dao-van-ai-quy-dinh-chung:by_sentences:008](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)


### Q3: According to RMIT Library, what records of AI prompts and outputs should students save?

Filter: `{"audience": "student"}`; Hit@3: False; coverage: 0%.

Gold: Keep a record of prompts, generated outputs and how the content was used; save copies because an educator may request them.

1. `rmit-vn-academic-integrity-ai:by_sentences:012` — score 0.2749; relevant=False

> The RMIT Library has plenty of supports available to help you reference. Visit Referencing or book a consultation appointment with an RMIT Librarian. ### Collusion
> 
> What is collusion?

2. `rmit-vn-academic-integrity-ai:by_sentences:000` — score 0.2632; relevant=False

> # RMIT Vietnam — Academic integrity and appropriate use of AI (students)
> 
> Learn about academic integrity, what happens if you breach it and where to get help if you're unsure. ## What is academic integrity? ## Types of academic integrity breaches
> 
> Using artificial intelligence (AI) appropriately
> 
> ## What happens if I breach academic integrity?

3. `rmit-vn-academic-integrity-ai:by_sentences:029` — score 0.2379; relevant=False

> Want to know more about how to use generative AI tools in your learning? Complete the Generative AI for students at RMIT module. ## What happens if I breach academic integrity?

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

The RMIT Library has plenty of supports available to help you reference. Visit Referencing or book a consultation appointment with an RMIT Librarian. ### Collusion
[rmit-vn-academic-integrity-ai:by_sentences:012](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)

Learn about academic integrity, what happens if you breach it and where to get help if you're unsure. ## What is academic integrity? ## Types of academic integrity breaches
[rmit-vn-academic-integrity-ai:by_sentences:000](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)

Want to know more about how to use generative AI tools in your learning? Complete the Generative AI for students at RMIT module. ## What happens if I breach academic integrity?
[rmit-vn-academic-integrity-ai:by_sentences:029](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)


### Q4: At UNA, should faculty use AI-detection software as the single means of verifying originality?

Filter: `{"audience": "faculty"}`; Hit@3: True; coverage: 100%.

Gold: No. Faculty should avoid using AI-detection software as the single means of verifying originality.

1. `una-genai-policy-faculty:by_sentences:010` — score 0.6269; relevant=True

> Be transparent about the use of AI-generated content in course materials. Encourage students to use AI responsibly and ethically. Avoid using AI-detection software as the single means of verifying originality.

2. `una-genai-policy-faculty:by_sentences:009` — score 0.2403; relevant=False

> ## Faculty
> 
> Use generative AI to enhance teaching and learning experiences while maintaining academic integrity. Faculty should include an AI Policy Statement in each course syllabus. (Template language included at the end of this policy).

3. `una-genai-policy-faculty:by_sentences:000` — score 0.2112; relevant=False

> # University of North Alabama — Generative AI Policy: faculty
> 
> ## Academic Integrity
> 
> The University of North Alabama acknowledges that faculty have complete discretion in establishing acceptable use of Generative AI (and other assistive tools) in their courses, so long as that use complies with existing university policies such as Faculty Handbook policies, Academic Honesty policies, IT Acceptable Use policies, and Privacy policies. The University offers the following guidance for crafting syllabus policies:
> 
> Faculty should explicitly define and explain the acceptable use of AI in the course syllabus, assignments, and rubrics/grading guides. Sample language will be provided in Simple Syllabus and can be customized.

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

Be transparent about the use of AI-generated content in course materials. Encourage students to use AI responsibly and ethically. Avoid using AI-detection software as the single means of verifying originality.
[una-genai-policy-faculty:by_sentences:010](https://www.una.edu/academics/generative-ai-policy.html)

Use generative AI to enhance teaching and learning experiences while maintaining academic integrity. Faculty should include an AI Policy Statement in each course syllabus. (Template language included at the end of this policy).
[una-genai-policy-faculty:by_sentences:009](https://www.una.edu/academics/generative-ai-policy.html)

Faculty should explicitly define and explain the acceptable use of AI in the course syllabus, assignments, and rubrics/grading guides. Sample language will be provided in Simple Syllabus and can be customized.
[una-genai-policy-faculty:by_sentences:000](https://www.una.edu/academics/generative-ai-policy.html)


### Q5: At UNA, what information may staff not share with generative AI, and may they create AI-generated promotional images?

Filter: `{"audience": "staff"}`; Hit@3: True; coverage: 100%.

Gold: Staff must avoid sharing confidential information, including student data protected under FERPA. Creating AI-generated images for promotional materials is not allowed in the supplied policy.

1. `una-genai-policy-staff:by_sentences:001` — score 0.3501; relevant=True

> UNA staff and faculty are permitted to use generative AI responsibly to assist in their work. However, users must exercise caution to avoid sharing confidential information, including student data protected under FERPA guidelines, when using AI tools. Additionally, the creation of AI-generated images for promotional materials is not allowed, as such content may conflict with UNA’s branding standards, copyright regulations, and institutional values.

2. `una-genai-policy-staff:by_sentences:000` — score 0.2029; relevant=False

> # University of North Alabama — Generative AI Policy: staff
> 
> ## Staff
> 
> Use generative AI to improve administrative processes and decision-making. Ensure data privacy and security when using AI tools in daily tasks. Stay informed about the latest AI developments and best practices.

3. `una-genai-policy-staff:by_sentences:002` — score 0.2019; relevant=False

> To ensure that all promotional materials remain on brand and in compliance with institutional and legal standards,
> 
> the Office of Enrollment Marketing & Digital Communications is available to assist in developing any needed promotional images. Work with IT Services prior to the use of AI for administrative purposes to help ensure data security, data integrity, integration needs, and data confidentiality

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

UNA staff and faculty are permitted to use generative AI responsibly to assist in their work. However, users must exercise caution to avoid sharing confidential information, including student data protected under FERPA guidelines, when using AI tools. Additionally, the creation of AI-generated images for promotional materials is not allowed, as such content may conflict with UNA’s branding standards, copyright regulations, and institutional values.
[una-genai-policy-staff:by_sentences:001](https://www.una.edu/academics/generative-ai-policy.html)

Use generative AI to improve administrative processes and decision-making. Ensure data privacy and security when using AI tools in daily tasks. Stay informed about the latest AI developments and best practices.
[una-genai-policy-staff:by_sentences:000](https://www.una.edu/academics/generative-ai-policy.html)

the Office of Enrollment Marketing & Digital Communications is available to assist in developing any needed promotional images. Work with IT Services prior to the use of AI for administrative purposes to help ensure data security, data integrity, integration needs, and data confidentiality
[una-genai-policy-staff:by_sentences:002](https://www.una.edu/academics/generative-ai-policy.html)


## tfidf / recursive

### Q1: Tại UEH, sau khi chỉnh sửa nhưng vẫn vi phạm sử dụng AI trong học thuật thì xử lý thế nào?

Filter: `{"audience": "student"}`; Hit@3: True; coverage: 100%.

Gold: Với người học, giảng viên phụ trách học phần lập biên bản, thông báo chuyển cho đơn vị quản lý để xử lý tùy theo mức độ vi phạm.

1. `ueh-xu-ly-vi-pham-nguoi-hoc:recursive:003` — score 0.4247; relevant=True

> b) Nếu vẫn vi phạm sau khi đã chỉnh sửa, giảng viên phụ trách học phần lập biên bản, thông báo chuyển cho đơn vị quản lý để xử lý tùy theo mức độ vi phạm.
> 
> ## Điều 6. Tổ chức thực hiện — trách nhiệm của người học
> 
> ### Trách nhiệm của tác giả sản phẩm học thuật và người học tại UEH:
> 
> a) Thực hiện nghiêm túc các quy định về đạo văn và sử dụng AI trong học thuật.
> 
> b) Khuyến khích toàn thể người học, viên chức, người lao động của UEH thông báo và cung cấp những bằng chứng về những trường hợp nghi ngờ có hành vi đạo văn hoặc vi phạm sử dụng AI trong học thuật.

2. `ueh-xu-ly-vi-pham-nguoi-hoc:recursive:001` — score 0.4225; relevant=False

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

3. `ueh-xu-ly-vi-pham-nguoi-hoc:recursive:002` — score 0.3052; relevant=False

> Người học phải chỉnh sửa và khắc phục vi phạm theo yêu cầu của giảng viên hướng dẫn hoặc đơn vị quản lý.
> 
> b) Trong quá trình bảo vệ hoặc đánh giá:
> 
> Nếu Hội đồng đánh giá đề án tốt nghiệp, luận văn, luận án hoặc giảng viên phụ trách phát hiện vi phạm sử dụng AI trong học thuật, chủ tịch hội đồng/giảng viên phụ trách quyết định khóa luận, đề án tốt nghiệp, luận văn, luận án không đạt, người học phải chỉnh sửa lại sản phẩm và khắc phục vi phạm.
> 
> c) Sau khi đã bảo vệ:
> 
> Nếu phát hiện vi phạm sử dụng AI, tác giả chịu trách nhiệm theo các quy định của UEH và pháp luật hiện hành.
> 
> ### 2.2. Đối với các bài kiểm tra, bài tập, tiểu luận, đồ án, dự án và các bài khác thuộc học phần
> 
> a) Khi bị phát hiện vi phạm lần đầu, người học phải chỉnh sửa và nộp lại bài theo yêu cầu của giảng viên;
> 
> 

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

b) Nếu vẫn vi phạm sau khi đã chỉnh sửa, giảng viên phụ trách học phần lập biên bản, thông báo chuyển cho đơn vị quản lý để xử lý tùy theo mức độ vi phạm.
[ueh-xu-ly-vi-pham-nguoi-hoc:recursive:003](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

b) Sau khi đã chỉnh sửa, người học nộp lại bài nhưng vẫn vi phạm lỗi đạo văn thì giảng viên phụ trách học phần lập biên bản/thông báo chuyển về đơn vị quản lý để xử lý tùy theo mức độ vi phạm quy định tại Phụ lục 3.
[ueh-xu-ly-vi-pham-nguoi-hoc:recursive:001](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

Nếu Hội đồng đánh giá đề án tốt nghiệp, luận văn, luận án hoặc giảng viên phụ trách phát hiện vi phạm sử dụng AI trong học thuật, chủ tịch hội đồng/giảng viên phụ trách quyết định khóa luận, đề án tốt nghiệp, luận văn, luận án không đạt, người học phải chỉnh sửa lại sản phẩm và khắc phục vi phạm.
[ueh-xu-ly-vi-pham-nguoi-hoc:recursive:002](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)


### Q2: Theo UEH, tỷ lệ tương đồng học thuật có phải là căn cứ duy nhất để kết luận đạo văn không?

Filter: `null`; Hit@3: True; coverage: 100%.

Gold: Không. Tỷ lệ tương đồng không phải căn cứ duy nhất; cần xem xét chuyên môn của đơn vị quản lý, giảng viên hoặc hội đồng có thẩm quyền.

1. `ueh-dao-van-ai-quy-dinh-chung:recursive:002` — score 0.5404; relevant=True

> Tỷ lệ tương đồng học thuật là tỷ lệ phần trăm nội dung trùng lặp trong sản phẩm học thuật được xác định bằng phần mềm hỗ trợ (Turnitin hoặc các công cụ kiểm tra đạo văn có chức năng so sánh với cơ sở dữ liệu học thuật rộng và cho phép phân tích chi tiết mức độ trùng lặp, được UEH phê duyệt sử dụng). Tỷ lệ tương đồng không phải là căn cứ duy nhất để kết luận đạo văn; việc đánh giá phải dựa trên xem xét chuyên môn của đơn vị quản lý, giảng viên hoặc hội đồng có thẩm quyền.
> 
> ### Các dấu hiệu của hành vi đạo văn hoặc vi phạm liêm chính học thuật
> 
> Sản phẩm học thuật có thể xem là có dấu hiệu vi phạm nếu có ít nhất một trong các biểu hiện sau:
> 
> a) Dấu hiệu định lượng từ phần mềm kiểm tra
> 
> 

2. `ueh-dao-van-ai-quy-dinh-chung:recursive:006` — score 0.4703; relevant=False

> 1. UEH sử dụng phần mềm Turnitin và/hoặc công cụ tương đương để phát hiện tỷ lệ tương đồng học thuật trong các sản phẩm học thuật. Kết quả tỷ lệ tương đồng chỉ mang tính tham khảo, hỗ trợ, không tự động kết luận là đạo văn. Việc kết luận dựa trên xem xét bối cảnh, phạm vi, tính chất nội dung trùng lặp, ý chí của người thực hiện và các chứng cứ liên quan. Việc đánh giá do giảng viên phụ trách/người hướng dẫn hoặc hội đồng/đơn vị có thẩm quyền thực hiện theo quy trình được UEH quy định.
> 
> 2. Xử lý hành vi đạo văn
> 
> ### 2.1 Nguyên tắc xử lý hành vi đạo văn
> 
> Việc xử lý được căn cứ trên mức độ nghiêm trọng, tính lặp lại và động cơ của hành vi:
> 
> 

3. `ueh-dao-van-ai-quy-dinh-chung:recursive:018` — score 0.3309; relevant=False

> b) Ban Đào tạo căn cứ kết quả kiểm tra của người hướng dẫn khoa học để tổ chức đánh giá, công nhận kết quả khóa luận tốt nghiệp, đề án tốt nghiệp, luận văn, luận án, đề tài nghiên cứu khoa học của người học.
> 
> c) Ban Nghiên cứu – Phát triển và Gắn kết toàn cầu, Văn phòng Trường thành viên/phân hiệu căn cứ kết quả tự kiểm tra của viên chức, người lao động UEH để tổ chức đánh giá, công nhận kết quả đề tài/báo cáo khoa học.
> 
> d) Đơn vị tổ chức hội thảo, tọa đàm, hội nghị căn cứ kết quả kiểm tra hoặc tự kiểm tra của viên chức, người lao động UEH để chọn bài đăng kỷ yếu hội thảo.
> 
> e) Tạp chí JABES kiểm tra tỷ lệ tương đồng theo quy định trước khi gửi phản biện và trước khi xuất bản.
> 
> ### Trách nhiệm của Ban Quản trị hạ tầng.
> 
> a) Quản lý phần mềm Turnitin, đảm bảo hoạt động liên tục, ổn định.
> 
> 

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

Tỷ lệ tương đồng học thuật là tỷ lệ phần trăm nội dung trùng lặp trong sản phẩm học thuật được xác định bằng phần mềm hỗ trợ (Turnitin hoặc các công cụ kiểm tra đạo văn có chức năng so sánh với cơ sở dữ liệu học thuật rộng và cho phép phân tích chi tiết mức độ trùng lặp, được UEH phê duyệt sử dụng). Tỷ lệ tương đồng không phải là căn cứ duy nhất để kết luận đạo văn; việc đánh giá phải dựa trên xem xét chuyên môn của đơn vị quản lý, giảng viên hoặc hội đồng có thẩm quyền.
[ueh-dao-van-ai-quy-dinh-chung:recursive:002](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

1. UEH sử dụng phần mềm Turnitin và/hoặc công cụ tương đương để phát hiện tỷ lệ tương đồng học thuật trong các sản phẩm học thuật. Kết quả tỷ lệ tương đồng chỉ mang tính tham khảo, hỗ trợ, không tự động kết luận là đạo văn. Việc kết luận dựa trên xem xét bối cảnh, phạm vi, tính chất nội dung trùng lặp, ý chí của người thực hiện và các chứng cứ liên quan. Việc đánh giá do giảng viên phụ trách/người hướng dẫn hoặc hội đồng/đơn vị có thẩm quyền thực hiện theo quy trình được UEH quy định.
[ueh-dao-van-ai-quy-dinh-chung:recursive:006](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

e) Tạp chí JABES kiểm tra tỷ lệ tương đồng theo quy định trước khi gửi phản biện và trước khi xuất bản.
[ueh-dao-van-ai-quy-dinh-chung:recursive:018](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)


### Q3: According to RMIT Library, what records of AI prompts and outputs should students save?

Filter: `{"audience": "student"}`; Hit@3: False; coverage: 0%.

Gold: Keep a record of prompts, generated outputs and how the content was used; save copies because an educator may request them.

1. `rmit-vn-academic-integrity-ai:recursive:000` — score 0.2523; relevant=False

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

2. `rmit-ai-acknowledgement-guide:recursive:001` — score 0.2160; relevant=False

> For this type of AI use, however, you need to include an acknowledgement of what AI tools were used and how they were used within the body or methods section of your work.
> 
> If you include any AI-generated outputs (such as text, images or code) in your work, you need to include a citation and a reference - see the citing and referencing guidelines page of this guide for more details.
> 
> ## Overall guidelines for acknowledging the use of AI tools
> 
> Check your assessment task instructions and/or assignment declaration for specific advice
> 
> Keep a record of how you have used AI tools in the process of creating your work, including the prompt used, the outputs generated, and how the generated content was used in your work.
> 
> 

3. `rmit-vn-academic-integrity-ai:recursive:015` — score 0.2115; relevant=False

> Produce content that you are unable to understand or explain in your own words.
> 
> Using AI in these ways is a breach of Academic Integrity Policy and may have serious consequences.
> 
> Want to know more about how to use generative AI tools in your learning? Complete the Generative AI for students at RMIT module.
> 
> ## What happens if I breach academic integrity?

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

Learn about academic integrity, what happens if you breach it and where to get help if you're unsure.
[rmit-vn-academic-integrity-ai:recursive:000](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)

For this type of AI use, however, you need to include an acknowledgement of what AI tools were used and how they were used within the body or methods section of your work.
[rmit-ai-acknowledgement-guide:recursive:001](https://rmit.libguides.com/referencing_AI_tools/acknowledging)

Want to know more about how to use generative AI tools in your learning? Complete the Generative AI for students at RMIT module.
[rmit-vn-academic-integrity-ai:recursive:015](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)


### Q4: At UNA, should faculty use AI-detection software as the single means of verifying originality?

Filter: `{"audience": "faculty"}`; Hit@3: True; coverage: 100%.

Gold: No. Faculty should avoid using AI-detection software as the single means of verifying originality.

1. `una-genai-policy-faculty:recursive:011` — score 0.4814; relevant=True

> Users should follow best practices for selecting and using AI tools and services, considering generative AI's potential risks and benefits. This includes being aware of the limitations of AI-generated content and verifying its accuracy before using it in academic or research contexts.
> 
> ## Faculty
> 
> Use generative AI to enhance teaching and learning experiences while maintaining academic integrity.
> 
> Faculty should include an AI Policy Statement in each course syllabus. (Template language included at the end of this policy).
> 
> Be transparent about the use of AI-generated content in course materials.
> 
> Encourage students to use AI responsibly and ethically.
> 
> Avoid using AI-detection software as the single means of verifying originality.
> 
> 

2. `una-genai-policy-faculty:recursive:001` — score 0.2080; relevant=False

> Faculty should explicitly define and explain the acceptable use of AI in the course syllabus, assignments, and rubrics/grading guides. Sample language will be provided in Simple Syllabus and can be customized. Faculty members who use AI to create lesson plans, assignments, rubrics, reading lists, and other class documents should acknowledge the use of AI to model academic integrity practices.
> 
> 

3. `una-genai-policy-faculty:recursive:003` — score 0.2080; relevant=False

> Faculty should explicitly define and explain the acceptable use of AI in the course syllabus, assignments, and rubrics/grading guides. Sample language will be provided in Simple Syllabus and can be customized. Faculty members who use AI to create lesson plans, assignments, rubrics, reading lists, and other class documents should acknowledge the use of AI to model academic integrity practices.
> 
> 

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

Avoid using AI-detection software as the single means of verifying originality.
[una-genai-policy-faculty:recursive:011](https://www.una.edu/academics/generative-ai-policy.html)

Faculty should explicitly define and explain the acceptable use of AI in the course syllabus, assignments, and rubrics/grading guides. Sample language will be provided in Simple Syllabus and can be customized. Faculty members who use AI to create lesson plans, assignments, rubrics, reading lists, and other class documents should acknowledge the use of AI to model academic integrity practices.
[una-genai-policy-faculty:recursive:001](https://www.una.edu/academics/generative-ai-policy.html)


### Q5: At UNA, what information may staff not share with generative AI, and may they create AI-generated promotional images?

Filter: `{"audience": "staff"}`; Hit@3: True; coverage: 100%.

Gold: Staff must avoid sharing confidential information, including student data protected under FERPA. Creating AI-generated images for promotional materials is not allowed in the supplied policy.

1. `una-genai-policy-staff:recursive:001` — score 0.3422; relevant=True

> UNA staff and faculty are permitted to use generative AI responsibly to assist in their work. However, users must exercise caution to avoid sharing confidential information, including student data protected under FERPA guidelines, when using AI tools. Additionally, the creation of AI-generated images for promotional materials is not allowed, as such content may conflict with UNA’s branding standards, copyright regulations, and institutional values. To ensure that all promotional materials remain on brand and in compliance with institutional and legal standards,
> 
> the Office of Enrollment Marketing & Digital Communications is available to assist in developing any needed promotional images.
> 
> 

2. `una-genai-policy-staff:recursive:000` — score 0.2029; relevant=False

> # University of North Alabama — Generative AI Policy: staff
> 
> ## Staff
> 
> Use generative AI to improve administrative processes and decision-making.
> 
> Ensure data privacy and security when using AI tools in daily tasks.
> 
> Stay informed about the latest AI developments and best practices.
> 
> 

3. `una-genai-policy-staff:recursive:002` — score 0.0834; relevant=False

> Work with IT Services prior to the use of AI for administrative purposes to help ensure data security, data integrity, integration needs, and data confidentiality

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

UNA staff and faculty are permitted to use generative AI responsibly to assist in their work. However, users must exercise caution to avoid sharing confidential information, including student data protected under FERPA guidelines, when using AI tools. Additionally, the creation of AI-generated images for promotional materials is not allowed, as such content may conflict with UNA’s branding standards, copyright regulations, and institutional values. To ensure that all promotional materials remain on brand and in compliance with institutional and legal standards,
[una-genai-policy-staff:recursive:001](https://www.una.edu/academics/generative-ai-policy.html)

Use generative AI to improve administrative processes and decision-making.
[una-genai-policy-staff:recursive:000](https://www.una.edu/academics/generative-ai-policy.html)

Work with IT Services prior to the use of AI for administrative purposes to help ensure data security, data integrity, integration needs, and data confidentiality
[una-genai-policy-staff:recursive:002](https://www.una.edu/academics/generative-ai-policy.html)


## tfidf / heading

### Q1: Tại UEH, sau khi chỉnh sửa nhưng vẫn vi phạm sử dụng AI trong học thuật thì xử lý thế nào?

Filter: `{"audience": "student"}`; Hit@3: True; coverage: 100%.

Gold: Với người học, giảng viên phụ trách học phần lập biên bản, thông báo chuyển cho đơn vị quản lý để xử lý tùy theo mức độ vi phạm.

1. `ueh-xu-ly-vi-pham-nguoi-hoc:heading:005` — score 0.4540; relevant=True

> # UEH — Xử lý vi phạm đạo văn và sử dụng AI đối với người học
> ## Điều 5. Xử lý vi phạm sử dụng AI trong học thuật — áp dụng cho người học
> ### 2.2. Đối với các bài kiểm tra, bài tập, tiểu luận, đồ án, dự án và các bài khác thuộc học phần
> 
> a) Khi bị phát hiện vi phạm lần đầu, người học phải chỉnh sửa và nộp lại bài theo yêu cầu của giảng viên;
> 
> b) Nếu vẫn vi phạm sau khi đã chỉnh sửa, giảng viên phụ trách học phần lập biên bản, thông báo chuyển cho đơn vị quản lý để xử lý tùy theo mức độ vi phạm.

2. `ueh-xu-ly-vi-pham-nguoi-hoc:heading:002` — score 0.4474; relevant=False

> # UEH — Xử lý vi phạm đạo văn và sử dụng AI đối với người học
> ## Điều 3. Xử lý hành vi đạo văn — áp dụng cho người học
> ### 2.3 Đối với các bài kiểm tra, bài tập, tiểu luận và các bài khác thuộc các học phần
> 
> a) Khi bị phát hiện vi phạm lần đầu, người học phải chỉnh sửa và nộp lại bài theo yêu cầu của giảng viên;
> 
> b) Sau khi đã chỉnh sửa, người học nộp lại bài nhưng vẫn vi phạm lỗi đạo văn thì giảng viên phụ trách học phần lập biên bản/thông báo chuyển về đơn vị quản lý để xử lý tùy theo mức độ vi phạm quy định tại Phụ lục 3.

3. `ueh-xu-ly-vi-pham-nguoi-hoc:heading:004` — score 0.4014; relevant=False

> # UEH — Xử lý vi phạm đạo văn và sử dụng AI đối với người học
> ## Điều 5. Xử lý vi phạm sử dụng AI trong học thuật — áp dụng cho người học
> ### 2.1. Đối với khóa luận, đề án tốt nghiệp, luận văn, luận án
> 
> Nếu phát hiện vi phạm sử dụng AI, tác giả chịu trách nhiệm theo các quy định của UEH và pháp luật hiện hành.

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

b) Nếu vẫn vi phạm sau khi đã chỉnh sửa, giảng viên phụ trách học phần lập biên bản, thông báo chuyển cho đơn vị quản lý để xử lý tùy theo mức độ vi phạm.
[ueh-xu-ly-vi-pham-nguoi-hoc:heading:005](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

b) Sau khi đã chỉnh sửa, người học nộp lại bài nhưng vẫn vi phạm lỗi đạo văn thì giảng viên phụ trách học phần lập biên bản/thông báo chuyển về đơn vị quản lý để xử lý tùy theo mức độ vi phạm quy định tại Phụ lục 3.
[ueh-xu-ly-vi-pham-nguoi-hoc:heading:002](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

Nếu phát hiện vi phạm sử dụng AI, tác giả chịu trách nhiệm theo các quy định của UEH và pháp luật hiện hành.
[ueh-xu-ly-vi-pham-nguoi-hoc:heading:004](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)


### Q2: Theo UEH, tỷ lệ tương đồng học thuật có phải là căn cứ duy nhất để kết luận đạo văn không?

Filter: `null`; Hit@3: True; coverage: 100%.

Gold: Không. Tỷ lệ tương đồng không phải căn cứ duy nhất; cần xem xét chuyên môn của đơn vị quản lý, giảng viên hoặc hội đồng có thẩm quyền.

1. `ueh-dao-van-ai-quy-dinh-chung:heading:004` — score 0.5786; relevant=True

> # UEH — Quy định kiểm soát đạo văn và sử dụng AI: quy định chung
> ## Điều 2. Nhận diện và xác định hành vi đạo văn
> ### Tỷ lệ tương đồng học thuật
> 
> Tỷ lệ tương đồng học thuật là tỷ lệ phần trăm nội dung trùng lặp trong sản phẩm học thuật được xác định bằng phần mềm hỗ trợ (Turnitin hoặc các công cụ kiểm tra đạo văn có chức năng so sánh với cơ sở dữ liệu học thuật rộng và cho phép phân tích chi tiết mức độ trùng lặp, được UEH phê duyệt sử dụng). Tỷ lệ tương đồng không phải là căn cứ duy nhất để kết luận đạo văn; việc đánh giá phải dựa trên xem xét chuyên môn của đơn vị quản lý, giảng viên hoặc hội đồng có thẩm quyền.

2. `ueh-dao-van-ai-quy-dinh-chung:heading:008` — score 0.4686; relevant=False

> # UEH — Quy định kiểm soát đạo văn và sử dụng AI: quy định chung
> ## Điều 3. Phát hiện và xử lý hành vi đạo văn
> 
> 1. UEH sử dụng phần mềm Turnitin và/hoặc công cụ tương đương để phát hiện tỷ lệ tương đồng học thuật trong các sản phẩm học thuật. Kết quả tỷ lệ tương đồng chỉ mang tính tham khảo, hỗ trợ, không tự động kết luận là đạo văn. Việc kết luận dựa trên xem xét bối cảnh, phạm vi, tính chất nội dung trùng lặp, ý chí của người thực hiện và các chứng cứ liên quan. Việc đánh giá do giảng viên phụ trách/người hướng dẫn hoặc hội đồng/đơn vị có thẩm quyền thực hiện theo quy trình được UEH quy định.
> 
> 2. Xử lý hành vi đạo văn

3. `ueh-dao-van-ai-quy-dinh-chung:heading:023` — score 0.3145; relevant=False

> # UEH — Quy định kiểm soát đạo văn và sử dụng AI: quy định chung
> ## Điều 6. Tổ chức thực hiện (trách nhiệm các đơn vị)
> ### Trách nhiệm của các đơn vị quản lý hoạt động đào tạo, hoạt động nghiên cứu khoa học.
> 
> c) Ban Nghiên cứu – Phát triển và Gắn kết toàn cầu, Văn phòng Trường thành viên/phân hiệu căn cứ kết quả tự kiểm tra của viên chức, người lao động UEH để tổ chức đánh giá, công nhận kết quả đề tài/báo cáo khoa học.
> 
> d) Đơn vị tổ chức hội thảo, tọa đàm, hội nghị căn cứ kết quả kiểm tra hoặc tự kiểm tra của viên chức, người lao động UEH để chọn bài đăng kỷ yếu hội thảo.
> 
> e) Tạp chí JABES kiểm tra tỷ lệ tương đồng theo quy định trước khi gửi phản biện và trước khi xuất bản.

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

Tỷ lệ tương đồng học thuật là tỷ lệ phần trăm nội dung trùng lặp trong sản phẩm học thuật được xác định bằng phần mềm hỗ trợ (Turnitin hoặc các công cụ kiểm tra đạo văn có chức năng so sánh với cơ sở dữ liệu học thuật rộng và cho phép phân tích chi tiết mức độ trùng lặp, được UEH phê duyệt sử dụng). Tỷ lệ tương đồng không phải là căn cứ duy nhất để kết luận đạo văn; việc đánh giá phải dựa trên xem xét chuyên môn của đơn vị quản lý, giảng viên hoặc hội đồng có thẩm quyền.
[ueh-dao-van-ai-quy-dinh-chung:heading:004](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

1. UEH sử dụng phần mềm Turnitin và/hoặc công cụ tương đương để phát hiện tỷ lệ tương đồng học thuật trong các sản phẩm học thuật. Kết quả tỷ lệ tương đồng chỉ mang tính tham khảo, hỗ trợ, không tự động kết luận là đạo văn. Việc kết luận dựa trên xem xét bối cảnh, phạm vi, tính chất nội dung trùng lặp, ý chí của người thực hiện và các chứng cứ liên quan. Việc đánh giá do giảng viên phụ trách/người hướng dẫn hoặc hội đồng/đơn vị có thẩm quyền thực hiện theo quy trình được UEH quy định.
[ueh-dao-van-ai-quy-dinh-chung:heading:008](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

e) Tạp chí JABES kiểm tra tỷ lệ tương đồng theo quy định trước khi gửi phản biện và trước khi xuất bản.
[ueh-dao-van-ai-quy-dinh-chung:heading:023](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)


### Q3: According to RMIT Library, what records of AI prompts and outputs should students save?

Filter: `{"audience": "student"}`; Hit@3: True; coverage: 100%.

Gold: Keep a record of prompts, generated outputs and how the content was used; save copies because an educator may request them.

1. `rmit-ai-acknowledgement-guide:heading:002` — score 0.3765; relevant=True

> # RMIT Library — Acknowledging the use of AI tools (students)
> ## Overall guidelines for acknowledging the use of AI tools
> 
> Check your assessment task instructions and/or assignment declaration for specific advice
> 
> Keep a record of how you have used AI tools in the process of creating your work, including the prompt used, the outputs generated, and how the generated content was used in your work.
> 
> Make sure you save a copy of the prompts used and outputs generated, as you may need to provide this to your educator on request.

2. `rmit-ai-acknowledgement-guide:heading:001` — score 0.3060; relevant=False

> # RMIT Library — Acknowledging the use of AI tools (students)
> ## Acknowledging the AI tools you have used
> 
> For this type of AI use, however, you need to include an acknowledgement of what AI tools were used and how they were used within the body or methods section of your work.
> 
> If you include any AI-generated outputs (such as text, images or code) in your work, you need to include a citation and a reference - see the citing and referencing guidelines page of this guide for more details.

3. `rmit-vn-academic-integrity-ai:heading:000` — score 0.2693; relevant=False

> # RMIT Vietnam — Academic integrity and appropriate use of AI (students)
> 
> Learn about academic integrity, what happens if you breach it and where to get help if you're unsure.

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

Make sure you save a copy of the prompts used and outputs generated, as you may need to provide this to your educator on request.
[rmit-ai-acknowledgement-guide:heading:002](https://rmit.libguides.com/referencing_AI_tools/acknowledging)

For this type of AI use, however, you need to include an acknowledgement of what AI tools were used and how they were used within the body or methods section of your work.
[rmit-ai-acknowledgement-guide:heading:001](https://rmit.libguides.com/referencing_AI_tools/acknowledging)

Learn about academic integrity, what happens if you breach it and where to get help if you're unsure.
[rmit-vn-academic-integrity-ai:heading:000](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)


### Q4: At UNA, should faculty use AI-detection software as the single means of verifying originality?

Filter: `{"audience": "faculty"}`; Hit@3: True; coverage: 100%.

Gold: No. Faculty should avoid using AI-detection software as the single means of verifying originality.

1. `una-genai-policy-faculty:heading:014` — score 0.5401; relevant=True

> # University of North Alabama — Generative AI Policy: faculty
> ## Faculty
> 
> Use generative AI to enhance teaching and learning experiences while maintaining academic integrity.
> 
> Faculty should include an AI Policy Statement in each course syllabus. (Template language included at the end of this policy).
> 
> Be transparent about the use of AI-generated content in course materials.
> 
> Encourage students to use AI responsibly and ethically.
> 
> Avoid using AI-detection software as the single means of verifying originality.
> 
> 

2. `una-genai-policy-faculty:heading:013` — score 0.2335; relevant=False

> # University of North Alabama — Generative AI Policy: faculty
> ## Responsible Use
> 
> Users should follow best practices for selecting and using AI tools and services, considering generative AI's potential risks and benefits. This includes being aware of the limitations of AI-generated content and verifying its accuracy before using it in academic or research contexts.

3. `una-genai-policy-faculty:heading:001` — score 0.2167; relevant=False

> # University of North Alabama — Generative AI Policy: faculty
> ## Academic Integrity
> 
> Faculty should explicitly define and explain the acceptable use of AI in the course syllabus, assignments, and rubrics/grading guides. Sample language will be provided in Simple Syllabus and can be customized. Faculty members who use AI to create lesson plans, assignments, rubrics, reading lists, and other class documents should acknowledge the use of AI to model academic integrity practices.
> 
> 

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

Avoid using AI-detection software as the single means of verifying originality.
[una-genai-policy-faculty:heading:014](https://www.una.edu/academics/generative-ai-policy.html)

Users should follow best practices for selecting and using AI tools and services, considering generative AI's potential risks and benefits. This includes being aware of the limitations of AI-generated content and verifying its accuracy before using it in academic or research contexts.
[una-genai-policy-faculty:heading:013](https://www.una.edu/academics/generative-ai-policy.html)

Faculty should explicitly define and explain the acceptable use of AI in the course syllabus, assignments, and rubrics/grading guides. Sample language will be provided in Simple Syllabus and can be customized. Faculty members who use AI to create lesson plans, assignments, rubrics, reading lists, and other class documents should acknowledge the use of AI to model academic integrity practices.
[una-genai-policy-faculty:heading:001](https://www.una.edu/academics/generative-ai-policy.html)


### Q5: At UNA, what information may staff not share with generative AI, and may they create AI-generated promotional images?

Filter: `{"audience": "staff"}`; Hit@3: True; coverage: 100%.

Gold: Staff must avoid sharing confidential information, including student data protected under FERPA. Creating AI-generated images for promotional materials is not allowed in the supplied policy.

1. `una-genai-policy-staff:heading:001` — score 0.3714; relevant=True

> # University of North Alabama — Generative AI Policy: staff
> ## Staff
> 
> UNA staff and faculty are permitted to use generative AI responsibly to assist in their work. However, users must exercise caution to avoid sharing confidential information, including student data protected under FERPA guidelines, when using AI tools. Additionally, the creation of AI-generated images for promotional materials is not allowed, as such content may conflict with UNA’s branding standards, copyright regulations, and institutional values. To ensure that all promotional materials remain on brand and in compliance with institutional and legal standards,
> 
> the Office of Enrollment Marketing & Digital Communications is available to assist in developing any needed promotional images.
> 
> 

2. `una-genai-policy-staff:heading:000` — score 0.2029; relevant=False

> # University of North Alabama — Generative AI Policy: staff
> ## Staff
> 
> Use generative AI to improve administrative processes and decision-making.
> 
> Ensure data privacy and security when using AI tools in daily tasks.
> 
> Stay informed about the latest AI developments and best practices.
> 
> 

3. `una-genai-policy-staff:heading:002` — score 0.2027; relevant=False

> # University of North Alabama — Generative AI Policy: staff
> ## Staff
> 
> Work with IT Services prior to the use of AI for administrative purposes to help ensure data security, data integrity, integration needs, and data confidentiality

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

UNA staff and faculty are permitted to use generative AI responsibly to assist in their work. However, users must exercise caution to avoid sharing confidential information, including student data protected under FERPA guidelines, when using AI tools. Additionally, the creation of AI-generated images for promotional materials is not allowed, as such content may conflict with UNA’s branding standards, copyright regulations, and institutional values. To ensure that all promotional materials remain on brand and in compliance with institutional and legal standards,
[una-genai-policy-staff:heading:001](https://www.una.edu/academics/generative-ai-policy.html)

Use generative AI to improve administrative processes and decision-making.
[una-genai-policy-staff:heading:000](https://www.una.edu/academics/generative-ai-policy.html)

Work with IT Services prior to the use of AI for administrative purposes to help ensure data security, data integrity, integration needs, and data confidentiality
[una-genai-policy-staff:heading:002](https://www.una.edu/academics/generative-ai-policy.html)


## mock / fixed_size

### Q1: Tại UEH, sau khi chỉnh sửa nhưng vẫn vi phạm sử dụng AI trong học thuật thì xử lý thế nào?

Filter: `{"audience": "student"}`; Hit@3: True; coverage: 100%.

Gold: Với người học, giảng viên phụ trách học phần lập biên bản, thông báo chuyển cho đơn vị quản lý để xử lý tùy theo mức độ vi phạm.

1. `rmit-ai-acknowledgement-guide:fixed_size:004` — score 0.2584; relevant=False

>  you put the following statement in your general acknowledgement:
> 
> I did not use any AI tools in the creation of this work.

2. `una-genai-policy-students:fixed_size:000` — score 0.1852; relevant=False

> # University of North Alabama — Generative AI Policy: students and sample syllabus rules
> 
> ## Students
> 
> Use generative AI to support learning and research while adhering to UNA’s academic integrity policies.
> 
> Know your instructors’ policies for using AI in your courses.
> 
> Properly cite AI-generated content in academic work.
> 
> Be aware of the limitations of AI-generated content and verify its accuracy before using it in academic or research contexts.
> 
> ## Sample syllabus language (AI use in coursework)
> 
> ### OPTION 1 Policy on AI Use in Coursework
> 
> As part of this course, students are encouraged to engage with emerging technologies, including artificial intelligence (AI) tools, to enhance learning and skill development. However, it is essential to use these tools responsibly and ethically. The f

3. `ueh-xu-ly-vi-pham-nguoi-hoc:fixed_size:003` — score 0.1681; relevant=True

> c phải chỉnh sửa và nộp lại bài theo yêu cầu của giảng viên;
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

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

I did not use any AI tools in the creation of this work.
[rmit-ai-acknowledgement-guide:fixed_size:004](https://rmit.libguides.com/referencing_AI_tools/acknowledging)

Properly cite AI-generated content in academic work.
[una-genai-policy-students:fixed_size:000](https://www.una.edu/academics/generative-ai-policy.html)

b) Nếu vẫn vi phạm sau khi đã chỉnh sửa, giảng viên phụ trách học phần lập biên bản, thông báo chuyển cho đơn vị quản lý để xử lý tùy theo mức độ vi phạm.
[ueh-xu-ly-vi-pham-nguoi-hoc:fixed_size:003](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)


### Q2: Theo UEH, tỷ lệ tương đồng học thuật có phải là căn cứ duy nhất để kết luận đạo văn không?

Filter: `null`; Hit@3: False; coverage: 0%.

Gold: Không. Tỷ lệ tương đồng không phải căn cứ duy nhất; cần xem xét chuyên môn của đơn vị quản lý, giảng viên hoặc hội đồng có thẩm quyền.

1. `ueh-dao-van-ai-quy-dinh-chung:fixed_size:016` — score 0.2669; relevant=False

> n Giám đốc Đại học UEH xem xét, quyết định việc điều chỉnh, bổ sung cho phù hợp với tình hình thực tế.
> 
> 3. Trường hợp phát hiện vi phạm sau khi đã cấp văn bằng, nghiệm thu hoặc công bố, việc xử lý được thực hiện theo quy định của UEH và quy định hiện hành của Bộ Giáo dục và Đào tạo và các quy định pháp luật có liên quan.

2. `una-genai-policy-students:fixed_size:001` — score 0.2417; relevant=False

> nt. However, it is essential to use these tools responsibly and ethically. The following guidelines outline acceptable and unacceptable uses of AI in coursework.
> 
> ### Acceptable AI Use
> 
> Assistance with Research and Writing: Students may use AI tools (e.g., ChatGPT, Grammarly) to assist with brainstorming ideas, conducting research, grammar checks, or improving the clarity of writing. However, the original ideas and final work must reflect the student’s understanding and effort.
> 
> Programming and Coding Assistance: AI tools may be used to generate code snippets or suggest solutions. Students should ensure that they understand the generated code and are able to explain its functionality during assessments or in class discussions.
> 
> Proofreading and Editing: Students may use AI for basic proofr

3. `rmit-vn-academic-integrity-ai:fixed_size:005` — score 0.2406; relevant=False

> ou can contact Campus Security or Safer Community. These services can support you with taking appropriate steps to remove any risk to your safety and/or the integrity of your studies
> 
> If you are experiencing study difficulties you should always speak with your teacher or course coordinator. They can help you access study support and ensure you understand and maintain academic integrity.
> 
> Source: Identifying, avoiding and reporting illegal cheating services.
> 
> To report a contract cheating service, or if you have any concerns or questions about contract cheating, please email studentconduct@rmit.edu.vn
> 
> ### Plagiarism and self-plagiarism
> 
> What is plagiarism?
> 
> Plagiarism means using someone else’s work or ideas without giving them proper credit. It's considered a form of theft, because the wo

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

3. Trường hợp phát hiện vi phạm sau khi đã cấp văn bằng, nghiệm thu hoặc công bố, việc xử lý được thực hiện theo quy định của UEH và quy định hiện hành của Bộ Giáo dục và Đào tạo và các quy định pháp luật có liên quan.
[ueh-dao-van-ai-quy-dinh-chung:fixed_size:016](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

nt. However, it is essential to use these tools responsibly and ethically. The following guidelines outline acceptable and unacceptable uses of AI in coursework.
[una-genai-policy-students:fixed_size:001](https://www.una.edu/academics/generative-ai-policy.html)

ou can contact Campus Security or Safer Community. These services can support you with taking appropriate steps to remove any risk to your safety and/or the integrity of your studies
[rmit-vn-academic-integrity-ai:fixed_size:005](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)


### Q3: According to RMIT Library, what records of AI prompts and outputs should students save?

Filter: `{"audience": "student"}`; Hit@3: False; coverage: 0%.

Gold: Keep a record of prompts, generated outputs and how the content was used; save copies because an educator may request them.

1. `rmit-vn-academic-integrity-ai:fixed_size:001` — score 0.2152; relevant=False

> sm, collusion and contract cheating, which all have serious consequences. Sometimes, the inappropriate use of AI in your studies can result in a breach.
> 
> Academic integrity has been more formally defined as ‘the expectation that teachers, students, researchers and all members of the academic community act with: honesty, trust, fairness, respect and responsibility.’
> 
> Be confident that you understand your responsibilities - find out more about academic integrity, what happens if you breach it and where to get help if you're unsure.
> 
> ## Types of academic integrity breaches
> 
> Examples of academic integrity breaches include:
> 
> ### Contract cheating and ghostwriting
> 
> Ghostwriting
> 
> Ghostwriting is when someone else completes an assignment for you without payment, like having someone else write your

2. `rmit-vn-academic-integrity-ai:fixed_size:005` — score 0.1870; relevant=False

> ou can contact Campus Security or Safer Community. These services can support you with taking appropriate steps to remove any risk to your safety and/or the integrity of your studies
> 
> If you are experiencing study difficulties you should always speak with your teacher or course coordinator. They can help you access study support and ensure you understand and maintain academic integrity.
> 
> Source: Identifying, avoiding and reporting illegal cheating services.
> 
> To report a contract cheating service, or if you have any concerns or questions about contract cheating, please email studentconduct@rmit.edu.vn
> 
> ### Plagiarism and self-plagiarism
> 
> What is plagiarism?
> 
> Plagiarism means using someone else’s work or ideas without giving them proper credit. It's considered a form of theft, because the wo

3. `rmit-vn-academic-integrity-ai:fixed_size:006` — score 0.1769; relevant=False

> thout giving them proper credit. It's considered a form of theft, because the work doesn't belong to you. It's also fraud, because it means you are claiming someone else’s work or ideas as your own.
> 
> Types of plagiarism
> 
> Intentional plagiarism – when you deliberately use someone else’s ideas, words or images and present them as your own, including failure to appropriately and accurately acknowledge the use of Artificial Intelligence tools.
> 
> Accidental plagiarism - when you don’t reference sources correctly in an assignment.
> 
> Self-plagiarism – when you use parts of your old assignments in new assignments without referencing it. Note, many courses do not allow self-referencing.
> 
> Avoid plagiarism – reference correctly
> 
> The best way to avoid the risk of plagiarism is to reference your work cor

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

sm, collusion and contract cheating, which all have serious consequences. Sometimes, the inappropriate use of AI in your studies can result in a breach.
[rmit-vn-academic-integrity-ai:fixed_size:001](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)

What is plagiarism?
[rmit-vn-academic-integrity-ai:fixed_size:005](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)

Types of plagiarism
[rmit-vn-academic-integrity-ai:fixed_size:006](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)


### Q4: At UNA, should faculty use AI-detection software as the single means of verifying originality?

Filter: `{"audience": "faculty"}`; Hit@3: False; coverage: 0%.

Gold: No. Faculty should avoid using AI-detection software as the single means of verifying originality.

1. `una-genai-policy-faculty:fixed_size:001` — score 0.1900; relevant=False

> ized. Faculty members who use AI to create lesson plans, assignments, rubrics, reading lists, and other class documents should acknowledge the use of AI to model academic integrity practices.
> 
> When using generative AI, users must acknowledge the use of AI-generated content by properly citing AI-generated content in academic work and ensuring that AI-generated content does not violate academic integrity policies. Faculty should review the appropriate procedures for documenting AIgenerated content with students. The reference list below includes links to the Modern Language Association, the American Psychological Association, and the Chicago Manual of Style guidelines for documenting AI-generated content.
> 
> Sample Syllabus Policy Statements from The University of Texas at Austin, Center for T

2. `una-genai-policy-faculty:fixed_size:010` — score 0.1390; relevant=False

> intain direct involvement in the grading process to ensure fair and meaningful assessment. Any use of AI grading tools should be carefully considered and supplemented with human oversight to preserve academic integrity and instructional quality. If AI grading tools are utilized in a course, this information must be disclosed to students in the course syllabus.

3. `una-genai-policy-faculty:fixed_size:007` — score 0.0787; relevant=False

> erification that it does not include information that may not be uploaded. Examples include:
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
> Please note that Microsoft and OpenAI explicitly forbid using ChatGPT and their other products for specific activity categories, including fraud and illegal activities.  This list of items can be found in their usage policy document.
> 
> ### Personal liability for publication on ChatGPT
> 
> ChatGPT uses a click-through agreement.  Click-through agreements, including O

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

ized. Faculty members who use AI to create lesson plans, assignments, rubrics, reading lists, and other class documents should acknowledge the use of AI to model academic integrity practices.
[una-genai-policy-faculty:fixed_size:001](https://www.una.edu/academics/generative-ai-policy.html)

intain direct involvement in the grading process to ensure fair and meaningful assessment. Any use of AI grading tools should be carefully considered and supplemented with human oversight to preserve academic integrity and instructional quality. If AI grading tools are utilized in a course, this information must be disclosed to students in the course syllabus.
[una-genai-policy-faculty:fixed_size:010](https://www.una.edu/academics/generative-ai-policy.html)

Please note that Microsoft and OpenAI explicitly forbid using ChatGPT and their other products for specific activity categories, including fraud and illegal activities.  This list of items can be found in their usage policy document.
[una-genai-policy-faculty:fixed_size:007](https://www.una.edu/academics/generative-ai-policy.html)


### Q5: At UNA, what information may staff not share with generative AI, and may they create AI-generated promotional images?

Filter: `{"audience": "staff"}`; Hit@3: True; coverage: 100%.

Gold: Staff must avoid sharing confidential information, including student data protected under FERPA. Creating AI-generated images for promotional materials is not allowed in the supplied policy.

1. `una-genai-policy-staff:fixed_size:001` — score 0.1262; relevant=False

> itutional values. To ensure that all promotional materials remain on brand and in compliance with institutional and legal standards,
> 
> the Office of Enrollment Marketing & Digital Communications is available to assist in developing any needed promotional images.
> 
> Work with IT Services prior to the use of AI for administrative purposes to help ensure data security, data integrity, integration needs, and data confidentiality

2. `una-genai-policy-staff:fixed_size:000` — score -0.1942; relevant=True

> # University of North Alabama — Generative AI Policy: staff
> 
> ## Staff
> 
> Use generative AI to improve administrative processes and decision-making.
> 
> Ensure data privacy and security when using AI tools in daily tasks.
> 
> Stay informed about the latest AI developments and best practices.
> 
> UNA staff and faculty are permitted to use generative AI responsibly to assist in their work. However, users must exercise caution to avoid sharing confidential information, including student data protected under FERPA guidelines, when using AI tools. Additionally, the creation of AI-generated images for promotional materials is not allowed, as such content may conflict with UNA’s branding standards, copyright regulations, and institutional values. To ensure that all promotional materials remain on brand and i

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

itutional values. To ensure that all promotional materials remain on brand and in compliance with institutional and legal standards,
[una-genai-policy-staff:fixed_size:001](https://www.una.edu/academics/generative-ai-policy.html)

UNA staff and faculty are permitted to use generative AI responsibly to assist in their work. However, users must exercise caution to avoid sharing confidential information, including student data protected under FERPA guidelines, when using AI tools. Additionally, the creation of AI-generated images for promotional materials is not allowed, as such content may conflict with UNA’s branding standards, copyright regulations, and institutional values. To ensure that all promotional materials remain on brand and i
[una-genai-policy-staff:fixed_size:000](https://www.una.edu/academics/generative-ai-policy.html)


## mock / by_sentences

### Q1: Tại UEH, sau khi chỉnh sửa nhưng vẫn vi phạm sử dụng AI trong học thuật thì xử lý thế nào?

Filter: `{"audience": "student"}`; Hit@3: False; coverage: 0%.

Gold: Với người học, giảng viên phụ trách học phần lập biên bản, thông báo chuyển cho đơn vị quản lý để xử lý tùy theo mức độ vi phạm.

1. `ueh-xu-ly-vi-pham-nguoi-hoc:by_sentences:000` — score 0.3248; relevant=False

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

2. `rmit-vn-academic-integrity-ai:by_sentences:014` — score 0.2237; relevant=False

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
> When is collaboration permitted? There are still circumstances where working with others is allowed. You can collaborate with your peers without breaching academic integrity by:
> 
> working together on a group assignment with your group members (just remember to credit all group members)
> 
> helping each other understand the assignment question
> 
> studying together
> 
> If you’re unsure, ask your educator about what kind of collaboration is permitted in your course.

3. `rmit-vn-academic-integrity-ai:by_sentences:020` — score 0.2221; relevant=False

> Behaviour that violates assessment instructions thereby defeating or compromising the purpose of the assessment. Unauthorised sharing of course materials and previously submitted assessment items including via online study platforms. ‘Washing’ - the use of software services to disguise plagiarism.

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

Khi phát hiện có dấu hiệu đạo văn, người học phải chỉnh sửa, bổ sung và khắc phục theo yêu cầu của giảng viên hướng dẫn hoặc đơn vị quản lý. b) Trong khi bảo vệ:
[ueh-xu-ly-vi-pham-nguoi-hoc:by_sentences:000](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

Types of collusion
[rmit-vn-academic-integrity-ai:by_sentences:014](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)

Behaviour that violates assessment instructions thereby defeating or compromising the purpose of the assessment. Unauthorised sharing of course materials and previously submitted assessment items including via online study platforms. ‘Washing’ - the use of software services to disguise plagiarism.
[rmit-vn-academic-integrity-ai:by_sentences:020](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)


### Q2: Theo UEH, tỷ lệ tương đồng học thuật có phải là căn cứ duy nhất để kết luận đạo văn không?

Filter: `null`; Hit@3: False; coverage: 0%.

Gold: Không. Tỷ lệ tương đồng không phải căn cứ duy nhất; cần xem xét chuyên môn của đơn vị quản lý, giảng viên hoặc hội đồng có thẩm quyền.

1. `ueh-dao-van-ai-quy-dinh-chung:by_sentences:026` — score 0.3097; relevant=False

> 2. Trong quá trình triển khai, nếu có vấn đề phát sinh, Ban Nghiên cứu – Phát triển và Gắn kết toàn cầu có trách nhiệm tổng hợp, báo cáo và trình Ban Giám đốc Đại học UEH xem xét, quyết định việc điều chỉnh, bổ sung cho phù hợp với tình hình thực tế. 3.

2. `una-genai-policy-faculty:by_sentences:010` — score 0.3089; relevant=False

> Be transparent about the use of AI-generated content in course materials. Encourage students to use AI responsibly and ethically. Avoid using AI-detection software as the single means of verifying originality.

3. `rmit-vn-academic-integrity-ai:by_sentences:017` — score 0.3068; relevant=False

> What is falsification? Falsification involves the manipulation or misrepresentation of research data, source material or results, or the presentation of results that are not supported by the evidence. In other words, changing real data.

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

2. Trong quá trình triển khai, nếu có vấn đề phát sinh, Ban Nghiên cứu – Phát triển và Gắn kết toàn cầu có trách nhiệm tổng hợp, báo cáo và trình Ban Giám đốc Đại học UEH xem xét, quyết định việc điều chỉnh, bổ sung cho phù hợp với tình hình thực tế. 3.
[ueh-dao-van-ai-quy-dinh-chung:by_sentences:026](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

Be transparent about the use of AI-generated content in course materials. Encourage students to use AI responsibly and ethically. Avoid using AI-detection software as the single means of verifying originality.
[una-genai-policy-faculty:by_sentences:010](https://www.una.edu/academics/generative-ai-policy.html)

What is falsification? Falsification involves the manipulation or misrepresentation of research data, source material or results, or the presentation of results that are not supported by the evidence. In other words, changing real data.
[rmit-vn-academic-integrity-ai:by_sentences:017](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)


### Q3: According to RMIT Library, what records of AI prompts and outputs should students save?

Filter: `{"audience": "student"}`; Hit@3: False; coverage: 0%.

Gold: Keep a record of prompts, generated outputs and how the content was used; save copies because an educator may request them.

1. `rmit-ai-acknowledgement-guide:by_sentences:000` — score 0.2283; relevant=False

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
> In such cases, you will not include AI-generated content directly in your final work, e.g. you are using AI tools in the process of creating the work.

2. `una-genai-policy-students:by_sentences:003` — score 0.2245; relevant=False

> Programming and Coding Assistance: AI tools may be used to generate code snippets or suggest solutions. Students should ensure that they understand the generated code and are able to explain its functionality during assessments or in class discussions. Proofreading and Editing: Students may use AI for basic proofreading, formatting, and language refinement, as long as the content remains their own creation.

3. `rmit-vn-academic-integrity-ai:by_sentences:019` — score 0.1903; relevant=False

> Be open about problems such as missing, messy, or unexpected results, and explain these limitations instead of trying to ‘fix’ them
> 
> Keep a record of your raw data, and if you make changes, document the rules you used and why. Only cite references that you have found and utilised, and check or validate references cited in genAI output. ### Other types of academic integrity breaches
> 
> Attempting to gain unfair advantage in an invigilated assessment, breaching the rules for the conduct of invigilated assessment in a manner that defeats or compromises the purposes of the task.

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

In some assessment tasks, you may be permitted to use AI tools for certain purposes, such as to:
[rmit-ai-acknowledgement-guide:by_sentences:000](https://rmit.libguides.com/referencing_AI_tools/acknowledging)

Programming and Coding Assistance: AI tools may be used to generate code snippets or suggest solutions. Students should ensure that they understand the generated code and are able to explain its functionality during assessments or in class discussions. Proofreading and Editing: Students may use AI for basic proofreading, formatting, and language refinement, as long as the content remains their own creation.
[una-genai-policy-students:by_sentences:003](https://www.una.edu/academics/generative-ai-policy.html)

Be open about problems such as missing, messy, or unexpected results, and explain these limitations instead of trying to ‘fix’ them
[rmit-vn-academic-integrity-ai:by_sentences:019](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)


### Q4: At UNA, should faculty use AI-detection software as the single means of verifying originality?

Filter: `{"audience": "faculty"}`; Hit@3: False; coverage: 0%.

Gold: No. Faculty should avoid using AI-detection software as the single means of verifying originality.

1. `ueh-xu-ly-vi-pham-giang-vien:by_sentences:001` — score 0.2020; relevant=False

> ## Điều 5. Xử lý vi phạm sử dụng AI — áp dụng cho viên chức, người lao động, giảng viên thỉnh giảng
> 
> ### 2.3. Đối với viên chức, người lao động, giảng viên thỉnh giảng của UEH:
> 
> a) Trước khi nghiệm thu, công bố, phát hành: tác giả chỉnh sửa và khắc phục vi phạm;
> 
> b) Sau khi chỉnh sửa nhưng vẫn vi phạm: sản phẩm không được nghiệm thu, không được công nhận, không được sử dụng cho bất kỳ hoạt động chuyên môn nào.

2. `ueh-xu-ly-vi-pham-giang-vien:by_sentences:003` — score 0.1925; relevant=False

> b) Sử dụng phần mềm Turnitin để kiểm tra các sản phẩm học thuật theo quy định:
> 
> - Kiểm tra ngẫu nhiên hoặc theo yêu cầu đối với bài tập, tiểu luận, đồ án, dự án, bài kiểm tra;
> - Kiểm tra bắt buộc đối với báo cáo nghiên cứu khoa học, khóa luận tốt nghiệp, đề án tốt nghiệp, luận văn thạc sĩ, luận án tiến sĩ và các sản phẩm học thuật quan trọng khác trước khi gửi đến các đơn vị quản lý. c) Tự kiểm tra các sản phẩm học thuật của mình trước khi nộp; bắt buộc kiểm tra đối với các sản phẩm gửi xuất bản, nghiệm thu, báo cáo đề tài nghiên cứu, bài đăng tạp chí, hoặc các sản phẩm sử dụng cho hoạt động chuyên môn theo quy định của UEH. d) Trách nhiệm giải trình: Trong trường hợp có khiếu nại liên quan đến kết luận vi phạm đạo văn hoặc sử dụng AI, giảng viên có trách nhiệm cung cấp đầy đủ căn cứ chuyên môn, kết quả kiểm tra, trao đổi đã thực hiện và các minh chứng liên quan để phục vụ việc xem xét, giải quyết khiếu nại theo quy trình nội bộ của UEH.

3. `una-genai-policy-faculty:by_sentences:004` — score 0.1778; relevant=False

> The reference list below includes links to the Modern Language Association, the American Psychological Association, and the Chicago Manual of Style guidelines for documenting AI-generated content. Sample Syllabus Policy Statements from The University of Texas at Austin, Center for Teaching and Learning
> 
> ## Data Privacy and Security
> 
> Users must follow data privacy and security guidelines when using generative AI to protect personal and institutional data. This includes adhering to UNA’s data privacy, confidential information policies, and applicable laws and regulations.

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

a) Trước khi nghiệm thu, công bố, phát hành: tác giả chỉnh sửa và khắc phục vi phạm;
[ueh-xu-ly-vi-pham-giang-vien:by_sentences:001](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

- Kiểm tra ngẫu nhiên hoặc theo yêu cầu đối với bài tập, tiểu luận, đồ án, dự án, bài kiểm tra;
- Kiểm tra bắt buộc đối với báo cáo nghiên cứu khoa học, khóa luận tốt nghiệp, đề án tốt nghiệp, luận văn thạc sĩ, luận án tiến sĩ và các sản phẩm học thuật quan trọng khác trước khi gửi đến các đơn vị quản lý. c) Tự kiểm tra các sản phẩm học thuật của mình trước khi nộp; bắt buộc kiểm tra đối với các sản phẩm gửi xuất bản, nghiệm thu, báo cáo đề tài nghiên cứu, bài đăng tạp chí, hoặc các sản phẩm sử dụng cho hoạt động chuyên môn theo quy định của UEH. d) Trách nhiệm giải trình: Trong trường hợp có khiếu nại liên quan đến kết luận vi phạm đạo văn hoặc sử dụng AI, giảng viên có trách nhiệm cung cấp đầy đủ căn cứ chuyên môn, kết quả kiểm tra, trao đổi đã thực hiện và các minh chứng liên quan để phục vụ việc xem xét, giải quyết khiếu nại theo quy trình nội bộ của UEH.
[ueh-xu-ly-vi-pham-giang-vien:by_sentences:003](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

The reference list below includes links to the Modern Language Association, the American Psychological Association, and the Chicago Manual of Style guidelines for documenting AI-generated content. Sample Syllabus Policy Statements from The University of Texas at Austin, Center for Teaching and Learning
[una-genai-policy-faculty:by_sentences:004](https://www.una.edu/academics/generative-ai-policy.html)


### Q5: At UNA, what information may staff not share with generative AI, and may they create AI-generated promotional images?

Filter: `{"audience": "staff"}`; Hit@3: True; coverage: 100%.

Gold: Staff must avoid sharing confidential information, including student data protected under FERPA. Creating AI-generated images for promotional materials is not allowed in the supplied policy.

1. `una-genai-policy-staff:by_sentences:002` — score 0.0690; relevant=False

> To ensure that all promotional materials remain on brand and in compliance with institutional and legal standards,
> 
> the Office of Enrollment Marketing & Digital Communications is available to assist in developing any needed promotional images. Work with IT Services prior to the use of AI for administrative purposes to help ensure data security, data integrity, integration needs, and data confidentiality

2. `una-genai-policy-staff:by_sentences:000` — score -0.0875; relevant=False

> # University of North Alabama — Generative AI Policy: staff
> 
> ## Staff
> 
> Use generative AI to improve administrative processes and decision-making. Ensure data privacy and security when using AI tools in daily tasks. Stay informed about the latest AI developments and best practices.

3. `una-genai-policy-staff:by_sentences:001` — score -0.1136; relevant=True

> UNA staff and faculty are permitted to use generative AI responsibly to assist in their work. However, users must exercise caution to avoid sharing confidential information, including student data protected under FERPA guidelines, when using AI tools. Additionally, the creation of AI-generated images for promotional materials is not allowed, as such content may conflict with UNA’s branding standards, copyright regulations, and institutional values.

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

the Office of Enrollment Marketing & Digital Communications is available to assist in developing any needed promotional images. Work with IT Services prior to the use of AI for administrative purposes to help ensure data security, data integrity, integration needs, and data confidentiality
[una-genai-policy-staff:by_sentences:002](https://www.una.edu/academics/generative-ai-policy.html)

Use generative AI to improve administrative processes and decision-making. Ensure data privacy and security when using AI tools in daily tasks. Stay informed about the latest AI developments and best practices.
[una-genai-policy-staff:by_sentences:000](https://www.una.edu/academics/generative-ai-policy.html)

UNA staff and faculty are permitted to use generative AI responsibly to assist in their work. However, users must exercise caution to avoid sharing confidential information, including student data protected under FERPA guidelines, when using AI tools. Additionally, the creation of AI-generated images for promotional materials is not allowed, as such content may conflict with UNA’s branding standards, copyright regulations, and institutional values.
[una-genai-policy-staff:by_sentences:001](https://www.una.edu/academics/generative-ai-policy.html)


## mock / recursive

### Q1: Tại UEH, sau khi chỉnh sửa nhưng vẫn vi phạm sử dụng AI trong học thuật thì xử lý thế nào?

Filter: `{"audience": "student"}`; Hit@3: False; coverage: 0%.

Gold: Với người học, giảng viên phụ trách học phần lập biên bản, thông báo chuyển cho đơn vị quản lý để xử lý tùy theo mức độ vi phạm.

1. `rmit-ai-acknowledgement-guide:recursive:003` — score 0.1951; relevant=False

> Format for the acknowledgement (based on APA 7th, you may need to modify this for your referencing style):
> 
> I used [tool used] (Creator, year) to [explain how tool was used].
> 
> Example acknowledgements:
> 
> I used ChatGPT (OpenAI, 2026) to provide topic suggestions for my research project.
> 
> I used the Writing Help persona in Val (RMIT, 2026) to provide feedback on my assignment draft.
> 
> Format for reference list/bibliography entry:
> 
> Check the Citing and referencing guidelines for AI tools page in this guide for the reference list/bibliography format for each of the referencing styles used at RMIT University.
> 
> ## Haven't used any AI tools?
> 
> 

2. `rmit-ai-acknowledgement-guide:recursive:000` — score 0.1276; relevant=False

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
> In such cases, you will not include AI-generated content directly in your final work, e.g. you are using AI tools in the process of creating the work.
> 
> 

3. `ueh-xu-ly-vi-pham-nguoi-hoc:recursive:000` — score 0.0972; relevant=False

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

[EXTRACTIVE BASELINE — không phải LLM]

Check the Citing and referencing guidelines for AI tools page in this guide for the reference list/bibliography format for each of the referencing styles used at RMIT University.
[rmit-ai-acknowledgement-guide:recursive:003](https://rmit.libguides.com/referencing_AI_tools/acknowledging)

In some assessment tasks, you may be permitted to use AI tools for certain purposes, such as to:
[rmit-ai-acknowledgement-guide:recursive:000](https://rmit.libguides.com/referencing_AI_tools/acknowledging)

Khi phát hiện có dấu hiệu đạo văn, người học phải chỉnh sửa, bổ sung và khắc phục theo yêu cầu của giảng viên hướng dẫn hoặc đơn vị quản lý.
[ueh-xu-ly-vi-pham-nguoi-hoc:recursive:000](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)


### Q2: Theo UEH, tỷ lệ tương đồng học thuật có phải là căn cứ duy nhất để kết luận đạo văn không?

Filter: `null`; Hit@3: False; coverage: 0%.

Gold: Không. Tỷ lệ tương đồng không phải căn cứ duy nhất; cần xem xét chuyên môn của đơn vị quản lý, giảng viên hoặc hội đồng có thẩm quyền.

1. `tt49-2026-ung-dung-cong-nghe-ai:recursive:003` — score 0.2593; relevant=False

> 5. Bảo đảm an toàn thông tin, an ninh dữ liệu, an ninh mạng, bảo vệ dữ liệu cá nhân; sử dụng công nghệ và trí tuệ nhân tạo có trách nhiệm, tuân thủ các nguyên tắc đạo đức và bảo đảm liêm chính học thuật.
> 
> ## Điều 6. Ứng dụng công nghệ trong hoạt động đào tạo
> 
> 1. Cơ sở giáo dục chủ động ứng dụng công nghệ số và trí tuệ nhân tạo trong hoạt động đào tạo nhằm nâng cao chất lượng, hiệu quả của hoạt động đào tạo; bảo đảm quyền tự chủ gắn với trách nhiệm giải trình, tuân thủ quy định của pháp luật.
> 
> 2. Việc ứng dụng công nghệ được thực hiện phù hợp thông qua các phương thức đào tạo sau:
> 
> a) Đào tạo trực tiếp có hỗ trợ công nghệ số;
> 
> b) Đào tạo trực tuyến toàn phần;
> 
> c) Đào tạo kết hợp trực tuyến và trực tiếp;
> 
> d) Đào tạo cá thể hóa dựa trên dữ liệu và trí tuệ nhân tạo;
> 
> 

2. `ueh-xu-ly-vi-pham-nguoi-hoc:recursive:000` — score 0.2513; relevant=False

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

3. `ueh-dao-van-ai-quy-dinh-chung:recursive:000` — score 0.2442; relevant=False

> # UEH — Quy định kiểm soát đạo văn và sử dụng AI: quy định chung
> 
> (Kèm theo Quyết định số: 4002/QĐ-ĐHKT-NCPTGKTC, ngày 18 tháng 12 năm 2025 của Giám đốc Đại học Kinh tế Thành phố Hồ Chí Minh)
> 
> ## Điều 1. Mục đích, phạm vi điều chỉnh và đối tượng áp dụng
> 
> Quy định này quy định về việc quản lý, kiểm soát và xử lý hành vi đạo văn; việc sử dụng trí tuệ nhân tạo (AI) trong học thuật nhằm đảm bảo liêm chính, minh bạch và trách nhiệm học thuật tại Đại học Kinh tế Thành phố Hồ Chí Minh (UEH).
> 
> Quy định này áp dụng đối với viên chức, người lao động, người học, giảng viên thỉnh giảng và các tổ chức, cá nhân có liên quan đến hoạt động đào tạo, nghiên cứu khoa học và học thuật tại UEH.
> 
> 

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

5. Bảo đảm an toàn thông tin, an ninh dữ liệu, an ninh mạng, bảo vệ dữ liệu cá nhân; sử dụng công nghệ và trí tuệ nhân tạo có trách nhiệm, tuân thủ các nguyên tắc đạo đức và bảo đảm liêm chính học thuật.
[tt49-2026-ung-dung-cong-nghe-ai:recursive:003](https://luatvietnam.vn/giao-duc/thong-tu-49-2026-tt-bgddt-ung-dung-cong-nghe-trong-giao-duc-dai-hoc-va-nghe-nghiep-439350-d1.html)

Nếu Hội đồng đánh giá luận văn/luận án phát hiện hành vi đạo văn, chủ tịch hội đồng quyết định luận văn/luận án không đạt, người học phải chỉnh sửa lại sản phẩm và khắc phục lỗi đạo văn theo quy định của chương trình.
[ueh-xu-ly-vi-pham-nguoi-hoc:recursive:000](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

Quy định này quy định về việc quản lý, kiểm soát và xử lý hành vi đạo văn; việc sử dụng trí tuệ nhân tạo (AI) trong học thuật nhằm đảm bảo liêm chính, minh bạch và trách nhiệm học thuật tại Đại học Kinh tế Thành phố Hồ Chí Minh (UEH).
[ueh-dao-van-ai-quy-dinh-chung:recursive:000](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)


### Q3: According to RMIT Library, what records of AI prompts and outputs should students save?

Filter: `{"audience": "student"}`; Hit@3: False; coverage: 0%.

Gold: Keep a record of prompts, generated outputs and how the content was used; save copies because an educator may request them.

1. `una-genai-policy-students:recursive:003` — score 0.3309; relevant=False

> Plagiarism or Full Automation of Assignments: Submitting AI-generated work as your own without meaningful engagement or modification is considered plagiarism. All assignments should reflect your own original thought processes, critical analysis, and academic effort.
> 
> Bypassing Learning Objectives: Using AI to complete an assignment without engaging with the learning objectives (e.g., generating entire essays, exam answers, or project deliverables without personal input) is prohibited.
> 
> Uncredited Use of AI-Generated Content: If you use AI-generated content in your work, it must be properly credited, even if the AI only provided part of the assignment. Failure to do so will be treated as academic dishonesty.
> 
> 

2. `rmit-vn-academic-integrity-ai:recursive:000` — score 0.2163; relevant=False

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

3. `ueh-xu-ly-vi-pham-nguoi-hoc:recursive:003` — score 0.2154; relevant=False

> b) Nếu vẫn vi phạm sau khi đã chỉnh sửa, giảng viên phụ trách học phần lập biên bản, thông báo chuyển cho đơn vị quản lý để xử lý tùy theo mức độ vi phạm.
> 
> ## Điều 6. Tổ chức thực hiện — trách nhiệm của người học
> 
> ### Trách nhiệm của tác giả sản phẩm học thuật và người học tại UEH:
> 
> a) Thực hiện nghiêm túc các quy định về đạo văn và sử dụng AI trong học thuật.
> 
> b) Khuyến khích toàn thể người học, viên chức, người lao động của UEH thông báo và cung cấp những bằng chứng về những trường hợp nghi ngờ có hành vi đạo văn hoặc vi phạm sử dụng AI trong học thuật.

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

Plagiarism or Full Automation of Assignments: Submitting AI-generated work as your own without meaningful engagement or modification is considered plagiarism. All assignments should reflect your own original thought processes, critical analysis, and academic effort.
[una-genai-policy-students:recursive:003](https://www.una.edu/academics/generative-ai-policy.html)

Learn about academic integrity, what happens if you breach it and where to get help if you're unsure.
[rmit-vn-academic-integrity-ai:recursive:000](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)

a) Thực hiện nghiêm túc các quy định về đạo văn và sử dụng AI trong học thuật.
[ueh-xu-ly-vi-pham-nguoi-hoc:recursive:003](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)


### Q4: At UNA, should faculty use AI-detection software as the single means of verifying originality?

Filter: `{"audience": "faculty"}`; Hit@3: False; coverage: 0%.

Gold: No. Faculty should avoid using AI-detection software as the single means of verifying originality.

1. `una-genai-policy-faculty:recursive:004` — score 0.1868; relevant=False

> When using generative AI, users must acknowledge the use of AI-generated content by properly citing AI-generated content in academic work and ensuring that AI-generated content does not violate academic integrity policies. Faculty should review the appropriate procedures for documenting AIgenerated content with students. The reference list below includes links to the Modern Language Association, the American Psychological Association, and the Chicago Manual of Style guidelines for documenting AI-generated content.
> 
> Sample Syllabus Policy Statements from The University of Texas at Austin, Center for Teaching and Learning
> 
> ## Data Privacy and Security
> 
> 

2. `una-genai-policy-faculty:recursive:012` — score 0.1037; relevant=False

> UNA faculty members are strongly cautioned against using AI grading tools to evaluate student work. While these tools may offer efficiency, they lack the nuanced understanding required to assess critical thinking, creativity, and individual learning needs. Faculty are encouraged to maintain direct involvement in the grading process to ensure fair and meaningful assessment. Any use of AI grading tools should be carefully considered and supplemented with human oversight to preserve academic integrity and instructional quality. If AI grading tools are utilized in a course, this information must be disclosed to students in the course syllabus.

3. `ueh-xu-ly-vi-pham-giang-vien:recursive:001` — score 0.0797; relevant=False

> Nếu phát hiện vi phạm đạo văn, tác giả phải chịu trách nhiệm theo quy định của UEH và pháp luật hiện hành; đồng thời thực hiện các nghĩa vụ liên quan như báo cáo đơn vị phát hành, rút bài, cải chính hoặc thu hồi (nếu có nhu cầu).
> 
> ## Điều 5. Xử lý vi phạm sử dụng AI — áp dụng cho viên chức, người lao động, giảng viên thỉnh giảng
> 
> ### 2.3. Đối với viên chức, người lao động, giảng viên thỉnh giảng của UEH:
> 
> a) Trước khi nghiệm thu, công bố, phát hành: tác giả chỉnh sửa và khắc phục vi phạm;
> 
> b) Sau khi chỉnh sửa nhưng vẫn vi phạm: sản phẩm không được nghiệm thu, không được công nhận, không được sử dụng cho bất kỳ hoạt động chuyên môn nào.
> 
> 

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

Sample Syllabus Policy Statements from The University of Texas at Austin, Center for Teaching and Learning
[una-genai-policy-faculty:recursive:004](https://www.una.edu/academics/generative-ai-policy.html)

UNA faculty members are strongly cautioned against using AI grading tools to evaluate student work. While these tools may offer efficiency, they lack the nuanced understanding required to assess critical thinking, creativity, and individual learning needs. Faculty are encouraged to maintain direct involvement in the grading process to ensure fair and meaningful assessment. Any use of AI grading tools should be carefully considered and supplemented with human oversight to preserve academic integrity and instructional quality. If AI grading tools are utilized in a course, this information must be disclosed to students in the course syllabus.
[una-genai-policy-faculty:recursive:012](https://www.una.edu/academics/generative-ai-policy.html)

Nếu phát hiện vi phạm đạo văn, tác giả phải chịu trách nhiệm theo quy định của UEH và pháp luật hiện hành; đồng thời thực hiện các nghĩa vụ liên quan như báo cáo đơn vị phát hành, rút bài, cải chính hoặc thu hồi (nếu có nhu cầu).
[ueh-xu-ly-vi-pham-giang-vien:recursive:001](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)


### Q5: At UNA, what information may staff not share with generative AI, and may they create AI-generated promotional images?

Filter: `{"audience": "staff"}`; Hit@3: True; coverage: 100%.

Gold: Staff must avoid sharing confidential information, including student data protected under FERPA. Creating AI-generated images for promotional materials is not allowed in the supplied policy.

1. `una-genai-policy-staff:recursive:002` — score 0.0747; relevant=False

> Work with IT Services prior to the use of AI for administrative purposes to help ensure data security, data integrity, integration needs, and data confidentiality

2. `una-genai-policy-staff:recursive:001` — score -0.0501; relevant=True

> UNA staff and faculty are permitted to use generative AI responsibly to assist in their work. However, users must exercise caution to avoid sharing confidential information, including student data protected under FERPA guidelines, when using AI tools. Additionally, the creation of AI-generated images for promotional materials is not allowed, as such content may conflict with UNA’s branding standards, copyright regulations, and institutional values. To ensure that all promotional materials remain on brand and in compliance with institutional and legal standards,
> 
> the Office of Enrollment Marketing & Digital Communications is available to assist in developing any needed promotional images.
> 
> 

3. `una-genai-policy-staff:recursive:000` — score -0.1918; relevant=False

> # University of North Alabama — Generative AI Policy: staff
> 
> ## Staff
> 
> Use generative AI to improve administrative processes and decision-making.
> 
> Ensure data privacy and security when using AI tools in daily tasks.
> 
> Stay informed about the latest AI developments and best practices.
> 
> 

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

Work with IT Services prior to the use of AI for administrative purposes to help ensure data security, data integrity, integration needs, and data confidentiality
[una-genai-policy-staff:recursive:002](https://www.una.edu/academics/generative-ai-policy.html)

UNA staff and faculty are permitted to use generative AI responsibly to assist in their work. However, users must exercise caution to avoid sharing confidential information, including student data protected under FERPA guidelines, when using AI tools. Additionally, the creation of AI-generated images for promotional materials is not allowed, as such content may conflict with UNA’s branding standards, copyright regulations, and institutional values. To ensure that all promotional materials remain on brand and in compliance with institutional and legal standards,
[una-genai-policy-staff:recursive:001](https://www.una.edu/academics/generative-ai-policy.html)

Use generative AI to improve administrative processes and decision-making.
[una-genai-policy-staff:recursive:000](https://www.una.edu/academics/generative-ai-policy.html)


## mock / heading

### Q1: Tại UEH, sau khi chỉnh sửa nhưng vẫn vi phạm sử dụng AI trong học thuật thì xử lý thế nào?

Filter: `{"audience": "student"}`; Hit@3: False; coverage: 0%.

Gold: Với người học, giảng viên phụ trách học phần lập biên bản, thông báo chuyển cho đơn vị quản lý để xử lý tùy theo mức độ vi phạm.

1. `una-genai-policy-students:heading:003` — score 0.3382; relevant=False

> # University of North Alabama — Generative AI Policy: students and sample syllabus rules
> ## Sample syllabus language (AI use in coursework)
> ### Acceptable AI Use
> 
> Proofreading and Editing: Students may use AI for basic proofreading, formatting, and language refinement, as long as the content remains their own creation.
> 
> Learning and Exploration: AI tools can be explored to supplement learning and deepen your understanding of course material. This includes using AI to clarify concepts, simulate scenarios, or analyze data sets.

2. `rmit-vn-academic-integrity-ai:heading:022` — score 0.2902; relevant=False

> # RMIT Vietnam — Academic integrity and appropriate use of AI (students)
> ## Using Artificial Intelligence (AI) appropriately
> ### Don’t forget:
> 
> Your course guide is your first stop. AI use varies across courses and assessments, some may ask you not to use it at all. When in doubt, check your course guide or ask your teacher
> 
> Be transparent about how you’ve used AI. This might mean referencing the tools you used, or reflecting on how they shaped your work. See the Library's AI referencing guide for specific AI referencing information.
> 
> Keep drafts of your work. To help prove the authenticity and originality of your work, you should keep all draft versions of your work to show how your assessments were developed. These can be requested at any time during your program.
> 
> 

3. `una-genai-policy-students:heading:000` — score 0.2721; relevant=False

> # University of North Alabama — Generative AI Policy: students and sample syllabus rules
> ## Students
> 
> Use generative AI to support learning and research while adhering to UNA’s academic integrity policies.
> 
> Know your instructors’ policies for using AI in your courses.
> 
> Properly cite AI-generated content in academic work.
> 
> Be aware of the limitations of AI-generated content and verify its accuracy before using it in academic or research contexts.

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

Proofreading and Editing: Students may use AI for basic proofreading, formatting, and language refinement, as long as the content remains their own creation.
[una-genai-policy-students:heading:003](https://www.una.edu/academics/generative-ai-policy.html)

Your course guide is your first stop. AI use varies across courses and assessments, some may ask you not to use it at all. When in doubt, check your course guide or ask your teacher
[rmit-vn-academic-integrity-ai:heading:022](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)

Properly cite AI-generated content in academic work.
[una-genai-policy-students:heading:000](https://www.una.edu/academics/generative-ai-policy.html)


### Q2: Theo UEH, tỷ lệ tương đồng học thuật có phải là căn cứ duy nhất để kết luận đạo văn không?

Filter: `null`; Hit@3: False; coverage: 0%.

Gold: Không. Tỷ lệ tương đồng không phải căn cứ duy nhất; cần xem xét chuyên môn của đơn vị quản lý, giảng viên hoặc hội đồng có thẩm quyền.

1. `rmit-vn-academic-integrity-ai:heading:002` — score 0.2617; relevant=False

> # RMIT Vietnam — Academic integrity and appropriate use of AI (students)
> ## What happens if I breach academic integrity?
> 
> Complete the Academic Integrity Awareness module
> 
> Contacts, resources and support

2. `una-genai-policy-general:heading:010` — score 0.2338; relevant=False

> # University of North Alabama — Generative AI Policy: general provisions and data privacy
> ## Data Privacy and Security
> ### Rationale for the Above Guidelines
> 
> Please note that Microsoft and OpenAI explicitly forbid using ChatGPT and their other products for specific activity categories, including fraud and illegal activities.  This list of items can be found in their usage policy document.

3. `rmit-vn-academic-integrity-ai:heading:022` — score 0.2197; relevant=False

> # RMIT Vietnam — Academic integrity and appropriate use of AI (students)
> ## Using Artificial Intelligence (AI) appropriately
> ### Don’t forget:
> 
> Your course guide is your first stop. AI use varies across courses and assessments, some may ask you not to use it at all. When in doubt, check your course guide or ask your teacher
> 
> Be transparent about how you’ve used AI. This might mean referencing the tools you used, or reflecting on how they shaped your work. See the Library's AI referencing guide for specific AI referencing information.
> 
> Keep drafts of your work. To help prove the authenticity and originality of your work, you should keep all draft versions of your work to show how your assessments were developed. These can be requested at any time during your program.
> 
> 

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

Complete the Academic Integrity Awareness module
[rmit-vn-academic-integrity-ai:heading:002](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)

Please note that Microsoft and OpenAI explicitly forbid using ChatGPT and their other products for specific activity categories, including fraud and illegal activities.  This list of items can be found in their usage policy document.
[una-genai-policy-general:heading:010](https://www.una.edu/academics/generative-ai-policy.html)

Your course guide is your first stop. AI use varies across courses and assessments, some may ask you not to use it at all. When in doubt, check your course guide or ask your teacher
[rmit-vn-academic-integrity-ai:heading:022](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)


### Q3: According to RMIT Library, what records of AI prompts and outputs should students save?

Filter: `{"audience": "student"}`; Hit@3: False; coverage: 0%.

Gold: Keep a record of prompts, generated outputs and how the content was used; save copies because an educator may request them.

1. `una-genai-policy-students:heading:004` — score 0.2501; relevant=False

> # University of North Alabama — Generative AI Policy: students and sample syllabus rules
> ## Sample syllabus language (AI use in coursework)
> ### Unacceptable AI Use
> 
> Plagiarism or Full Automation of Assignments: Submitting AI-generated work as your own without meaningful engagement or modification is considered plagiarism. All assignments should reflect your own original thought processes, critical analysis, and academic effort.
> 
> Bypassing Learning Objectives: Using AI to complete an assignment without engaging with the learning objectives (e.g., generating entire essays, exam answers, or project deliverables without personal input) is prohibited.
> 
> 

2. `rmit-vn-academic-integrity-ai:heading:011` — score 0.2103; relevant=False

> # RMIT Vietnam — Academic integrity and appropriate use of AI (students)
> ## Types of academic integrity breaches
> ### Plagiarism and self-plagiarism
> 
> What is plagiarism?
> 
> Plagiarism means using someone else’s work or ideas without giving them proper credit. It's considered a form of theft, because the work doesn't belong to you. It's also fraud, because it means you are claiming someone else’s work or ideas as your own.
> 
> Types of plagiarism
> 
> Intentional plagiarism – when you deliberately use someone else’s ideas, words or images and present them as your own, including failure to appropriately and accurately acknowledge the use of Artificial Intelligence tools.
> 
> Accidental plagiarism - when you don’t reference sources correctly in an assignment.
> 
> 

3. `rmit-vn-academic-integrity-ai:heading:005` — score 0.1936; relevant=False

> # RMIT Vietnam — Academic integrity and appropriate use of AI (students)
> ## Types of academic integrity breaches
> 
> Examples of academic integrity breaches include:

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

Plagiarism or Full Automation of Assignments: Submitting AI-generated work as your own without meaningful engagement or modification is considered plagiarism. All assignments should reflect your own original thought processes, critical analysis, and academic effort.
[una-genai-policy-students:heading:004](https://www.una.edu/academics/generative-ai-policy.html)

What is plagiarism?
[rmit-vn-academic-integrity-ai:heading:011](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)

Examples of academic integrity breaches include:
[rmit-vn-academic-integrity-ai:heading:005](https://www.rmit.edu.vn/students/my-studies/assessment-and-results/academic-integrity)


### Q4: At UNA, should faculty use AI-detection software as the single means of verifying originality?

Filter: `{"audience": "faculty"}`; Hit@3: False; coverage: 0%.

Gold: No. Faculty should avoid using AI-detection software as the single means of verifying originality.

1. `una-genai-policy-faculty:heading:000` — score 0.2007; relevant=False

> # University of North Alabama — Generative AI Policy: faculty
> ## Academic Integrity
> 
> The University of North Alabama acknowledges that faculty have complete discretion in establishing acceptable use of Generative AI (and other assistive tools) in their courses, so long as that use complies with existing university policies such as Faculty Handbook policies, Academic Honesty policies, IT Acceptable Use policies, and Privacy policies. The University offers the following guidance for crafting syllabus policies:
> 
> 

2. `ueh-xu-ly-vi-pham-giang-vien:heading:005` — score 0.1953; relevant=False

> # UEH — Xử lý vi phạm đạo văn và sử dụng AI đối với giảng viên, viên chức
> ## Điều 6. Tổ chức thực hiện — trách nhiệm của giảng viên
> ### Trách nhiệm của giảng viên:
> 
> - Kiểm tra ngẫu nhiên hoặc theo yêu cầu đối với bài tập, tiểu luận, đồ án, dự án, bài kiểm tra;
> - Kiểm tra bắt buộc đối với báo cáo nghiên cứu khoa học, khóa luận tốt nghiệp, đề án tốt nghiệp, luận văn thạc sĩ, luận án tiến sĩ và các sản phẩm học thuật quan trọng khác trước khi gửi đến các đơn vị quản lý.
> c) Tự kiểm tra các sản phẩm học thuật của mình trước khi nộp; bắt buộc kiểm tra đối với các sản phẩm gửi xuất bản, nghiệm thu, báo cáo đề tài nghiên cứu, bài đăng tạp chí, hoặc các sản phẩm sử dụng cho hoạt động chuyên môn theo quy định của UEH.
> 
> 

3. `una-genai-policy-faculty:heading:006` — score 0.1387; relevant=False

> # University of North Alabama — Generative AI Policy: faculty
> ## Data Privacy and Security
> ### University information that may be input into Generative AI tools:
> 
> Publicly available information lawfully published or internal information approved to be provided to the public by the University.
> 
> Examples include:University community email announcements/digest content
> 
> - University publications
> - Information on the University’s public-facing website accessible without authentication of UNA login information
> - Content on official university social media accounts
> - Job postings
> - Publicly available maps

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

The University of North Alabama acknowledges that faculty have complete discretion in establishing acceptable use of Generative AI (and other assistive tools) in their courses, so long as that use complies with existing university policies such as Faculty Handbook policies, Academic Honesty policies, IT Acceptable Use policies, and Privacy policies. The University offers the following guidance for crafting syllabus policies:
[una-genai-policy-faculty:heading:000](https://www.una.edu/academics/generative-ai-policy.html)

- Kiểm tra ngẫu nhiên hoặc theo yêu cầu đối với bài tập, tiểu luận, đồ án, dự án, bài kiểm tra;
- Kiểm tra bắt buộc đối với báo cáo nghiên cứu khoa học, khóa luận tốt nghiệp, đề án tốt nghiệp, luận văn thạc sĩ, luận án tiến sĩ và các sản phẩm học thuật quan trọng khác trước khi gửi đến các đơn vị quản lý.
c) Tự kiểm tra các sản phẩm học thuật của mình trước khi nộp; bắt buộc kiểm tra đối với các sản phẩm gửi xuất bản, nghiệm thu, báo cáo đề tài nghiên cứu, bài đăng tạp chí, hoặc các sản phẩm sử dụng cho hoạt động chuyên môn theo quy định của UEH.
[ueh-xu-ly-vi-pham-giang-vien:heading:005](https://daotao.ueh.edu.vn/quy-dinh-ve-viec-kiem-soat-xu-ly-hanh-vi-dao-van-su-dung-tri-tue-nhan-tao-ai-trong-cac-san-pham-hoc-thuat-tai-dai-hoc-kinh-te-thanh-pho-ho-chi-minh/)

- University publications
- Information on the University’s public-facing website accessible without authentication of UNA login information
- Content on official university social media accounts
- Job postings
- Publicly available maps
[una-genai-policy-faculty:heading:006](https://www.una.edu/academics/generative-ai-policy.html)


### Q5: At UNA, what information may staff not share with generative AI, and may they create AI-generated promotional images?

Filter: `{"audience": "staff"}`; Hit@3: True; coverage: 100%.

Gold: Staff must avoid sharing confidential information, including student data protected under FERPA. Creating AI-generated images for promotional materials is not allowed in the supplied policy.

1. `una-genai-policy-staff:heading:001` — score 0.2890; relevant=True

> # University of North Alabama — Generative AI Policy: staff
> ## Staff
> 
> UNA staff and faculty are permitted to use generative AI responsibly to assist in their work. However, users must exercise caution to avoid sharing confidential information, including student data protected under FERPA guidelines, when using AI tools. Additionally, the creation of AI-generated images for promotional materials is not allowed, as such content may conflict with UNA’s branding standards, copyright regulations, and institutional values. To ensure that all promotional materials remain on brand and in compliance with institutional and legal standards,
> 
> the Office of Enrollment Marketing & Digital Communications is available to assist in developing any needed promotional images.
> 
> 

2. `una-genai-policy-staff:heading:002` — score -0.0259; relevant=False

> # University of North Alabama — Generative AI Policy: staff
> ## Staff
> 
> Work with IT Services prior to the use of AI for administrative purposes to help ensure data security, data integrity, integration needs, and data confidentiality

3. `una-genai-policy-staff:heading:000` — score -0.2566; relevant=False

> # University of North Alabama — Generative AI Policy: staff
> ## Staff
> 
> Use generative AI to improve administrative processes and decision-making.
> 
> Ensure data privacy and security when using AI tools in daily tasks.
> 
> Stay informed about the latest AI developments and best practices.
> 
> 

**Agent output:**

[EXTRACTIVE BASELINE — không phải LLM]

UNA staff and faculty are permitted to use generative AI responsibly to assist in their work. However, users must exercise caution to avoid sharing confidential information, including student data protected under FERPA guidelines, when using AI tools. Additionally, the creation of AI-generated images for promotional materials is not allowed, as such content may conflict with UNA’s branding standards, copyright regulations, and institutional values. To ensure that all promotional materials remain on brand and in compliance with institutional and legal standards,
[una-genai-policy-staff:heading:001](https://www.una.edu/academics/generative-ai-policy.html)

Work with IT Services prior to the use of AI for administrative purposes to help ensure data security, data integrity, integration needs, and data confidentiality
[una-genai-policy-staff:heading:002](https://www.una.edu/academics/generative-ai-policy.html)

Use generative AI to improve administrative processes and decision-making.
[una-genai-policy-staff:heading:000](https://www.una.edu/academics/generative-ai-policy.html)

