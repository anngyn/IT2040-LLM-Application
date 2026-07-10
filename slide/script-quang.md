# Script văn nói (bullet) — Trần Tú Quang

> Cue-card để cầm trình bày. Mỗi slide một cụm bullet, nói theo ý, không cần đọc nguyên văn.
> Phần của **Quang**: Phần 3 (Khung 5 agent & test case) → Phần 4 (Metrics & Kết quả). Nhận bàn giao từ **Tiến**; xong bàn giao cho **Ấn**.
> `[~Xs]` là thời lượng gợi ý cho slide đó.

---

## TRẦN TÚ QUANG — Phần 3 · Phần 4

### Slide "Khung 5 Agent" (mở đầu của Quang) `[~70s]`
- **Mở đầu:** Cảm ơn Tiến. Em là Trần Tú Quang, xin trình bày năm agent, cấu trúc test case, rồi bộ chỉ số và kết quả.
- Toàn bộ framework vận hành nhờ năm agent phối hợp qua ba giai đoạn: sinh đề, chấm điểm, rồi cập nhật.
- Appraiser là "kiến trúc sư": giai đoạn một dựng cây kịch bản, giai đoạn ba cập nhật lại cây theo chỗ mô hình làm kém.
- Inquirer dựa vào cây đó sinh đề, tức prototype test data cho từng kịch bản.
- Quality Inspector đóng vai kiểm duyệt: lọc chất lượng và độ đa dạng của đề, đồng thời đối chiếu bằng chứng thật qua Wikipedia API để đề không sai dữ kiện.
- Evaluator là trọng tài, đóng vai LLM-as-a-Judge, chấm Grade từ một đến mười, rồi lưu vào Memory Pool M. M gồm bốn thứ: test case, câu trả lời, điểm, và nhận xét.
- Prober đọc Memory Pool M đó, dò lặp để sinh các đề khó hơn, nhắm đúng chỗ mô hình vừa sai.
- Hình dưới minh họa toàn cảnh năm agent qua ba giai đoạn, bằng ví dụ thật về một loại thuốc mới chữa tiểu đường, kèm bằng chứng và ba chế độ kiểm thử.

### Slide "Taxonomy kịch bản fact-checking" `[~30s]`
- Đây là cây kịch bản do Appraiser khởi tạo.
- Ban đầu chia ba nhóm lớn: Complex Claim, Fake News, Social Rumor.
- Mỗi nhóm có nhiều kịch bản con, ví dụ Fake News gồm châm biếm, nội dung sai lệch, ngụy tạo.
- Điểm hay: cây này không cố định, nó mở rộng dần qua các vòng lặp mỗi khi phát hiện điểm yếu mới.

### Slide "Cấu trúc một test case" `[~35s]`
- Mỗi test case gồm bốn thành phần.
- Key Point: chỉ dẫn nhiệm vụ. Source Claim: câu cần kiểm chứng.
- Auxiliary Info: bằng chứng phụ trợ. Test Mode: bối cảnh bài toán.
- Test Mode có ba chế độ: claim là không cho bằng chứng, tức closed-book; evidence là cho bằng chứng vàng từ Wikipedia; wisdom of crowds là cho một luồng bình luận mạng xã hội.
- Mọi người để ý Test Mode, vì đây chính là chỗ RAG sẽ tác động ở phần sau.

### Divider Phần 4 — "Metrics & Kết quả" `[~5s]`
- Mình sang phần bốn: bộ chỉ số và kết quả.
- Ba chỉ số chính là IMR, JFR, Grade, đánh giá trên 13 mô hình.

### Slide "Metrics đánh giá" `[~55s]`
- Bộ ba chỉ số, đều suy ra từ điểm Grade của Evaluator.
- IMR, Insight Mastery Rate: tỉ lệ câu bị chấm từ 3 điểm trở xuống trên tổng số câu, tức tỉ lệ câu có lỗi. Đây là chỉ số chủ đạo, càng thấp càng tốt.
- JFR, Justification Flaw Rate: tỉ lệ case verdict đúng nhưng lập luận kém. Càng thấp càng tốt.
- Grade: điểm Evaluator chấm, thang 1 đến 10, càng cao càng tốt. Quy tắc: sai ở verdict HOẶC justification thì không được quá 3 điểm, nên mốc 3 điểm chính là ranh giới của IMR.
- Đáng chú ý là JFR: nó tách đúng trường hợp mô hình đoán trúng nhãn nhưng lập luận rỗng, đúng tinh thần verdict khác justification.

### Slide "Kết quả: 13 LLM (Table 1)" `[~45s]`
- Đây là bảng đầy đủ 13 mô hình, có IMR, JFR, Grade ở cả ba nhóm và cột Overall.
- Setup: mười mô hình mã nguồn mở và ba mô hình proprietary, suy luận zero-shot, temperature bằng không nên tái lập được.
- Chỗ khoanh đỏ: GPT-4o đạt IMR thấp nhất, khoảng 12 phần trăm, tức tốt nhất.
- Đáng chú ý Qwen2.5-72B, mô hình mã nguồn mở, bám rất sát nhóm proprietary; dòng LLaMA thì yếu hơn.
- Một điểm nữa: prototype do người tạo và do mô hình tạo cho IMR gần như nhau, tức Table 2, khẳng định framework đánh giá công bằng.

### Slide "Phân tích sâu" `[~45s]`
- Hai phân tích bổ sung.
- Bên trái là kịch bản khó nhất mỗi nhóm: Complex Claim khó ở suy luận nhiều bước; Fake News ở tiêu đề lệch nội dung; Social Rumor ở tin đồn kiểu mong đợi hoặc lo sợ.
- Bên phải: IMR giảm dần rồi hội tụ qua các vòng probing.
- Điều này chứng minh framework đào đúng điểm yếu, và quá trình lặp là ổn định.
- Ý nghĩa: framework không chỉ chấm điểm mà còn chỉ đúng điểm yếu cụ thể (Fig 4); vòng lặp hội tụ (Fig 5) chứng tỏ Importance Sampling đào đúng chỗ, không ngẫu nhiên.
- Cầu nối: "suy luận nhiều bước" (Multi-Step Reasoning) chính là kịch bản Prober của nhóm tự sinh lại thành deductive_causal_reasoning ở Phần 5, nên nhóm tái hiện đúng cái paper phát hiện.

### Slide "Test Mode quyết định độ khó" `[~40s]`
- Bảng này cho thấy độ khó phụ thuộc mạnh vào Test Mode.
- Chế độ claim, không bằng chứng, khó nhất: GPT-4o có IMR 23 phần trăm.
- Chế độ wisdom of crowds ở giữa.
- Chế độ evidence, có bằng chứng, dễ nhất: IMR chỉ còn khoảng 10 phần trăm.
- Kết luận quan trọng: có bằng chứng giúp mô hình fact-check chính xác hơn hẳn, IMR giảm khoảng hai lần.
- Ánh xạ sang RAG: claim là baseline chưa có bằng chứng, evidence là trần trên khi retrieval hoàn hảo; wisdom of crowds cho thấy evidence nhiễu vẫn giúp, nên RAG thực tế nằm giữa hai mốc, tùy chất lượng retriever.
- Đây chính là cơ sở để nhóm đề xuất tích hợp RAG ở phần sau.
- **Bàn giao:** Phần bộ chỉ số và kết quả của paper đến đây là hết. Em mời bạn Ấn trình bày phần thực nghiệm tái hiện của nhóm.

---

_Tổng thời lượng gợi ý: ~5 phút 25 giây._
