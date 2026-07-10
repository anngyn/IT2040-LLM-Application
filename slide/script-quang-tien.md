# Script văn nói (bullet) — Quang & Tiến

> Cue-card để cầm trình bày. Mỗi slide một cụm bullet, nói theo ý, không cần đọc nguyên văn.
> Thứ tự: **Tiến** (bìa → Phần 2) → **Quang** (Phần 3 → Phần 4) → Ấn (Phần 5–6).
> `[~Xs]` là thời lượng gợi ý cho slide đó.

---

## TÔ HUỲNH MINH TIẾN — bìa · Nội dung · Phần 1 · Phần 2

### Slide bìa `[~25s]`
- Chào thầy và các bạn, em là Tô Huỳnh Minh Tiến, đại diện nhóm 8.
- Hôm nay nhóm em báo cáo đề tài FACT-AUDIT kết hợp RAG, dựa trên bài báo ở hội nghị ACL 2025.
- Nhóm gồm ba thành viên, chia phần: em nói bối cảnh và khung FACT-AUDIT; bạn Quang nói năm agent, bộ chỉ số và kết quả; bạn Ấn nói phần chạy lại framework và đề xuất RAG.
- Bây giờ em xin bắt đầu.

### Slide "Nội dung trình bày" `[~20s]`
- Bài của nhóm gồm sáu phần.
- Một, bối cảnh: vì sao phải đánh giá năng lực fact-checking của LLM.
- Hai, khung FACT-AUDIT với ba giai đoạn và Importance Sampling.
- Ba, năm agent và cách tạo test case; bốn, bộ chỉ số và kết quả trên 13 mô hình.
- Năm, nhóm chạy lại framework; sáu, đề xuất mở rộng RAG.
- Nhấn mạnh ngay một ý: đây là framework để ĐÁNH GIÁ năng lực mô hình, không phải đi kiểm chứng một phát biểu cụ thể.

### Divider Phần 1 — "Bối cảnh & động lực" `[~5s]`
- Mình vào phần một: bối cảnh và động lực.
- Câu hỏi lớn: tại sao cần đánh giá năng lực fact-checking của LLM.

### Slide "Bài toán & câu hỏi trung tâm" `[~50s]`
- Fact-checking hiểu đơn giản: đưa mô hình một phát biểu, nó phải làm hai việc.
- Một là phán: phát biểu Đúng, Sai, hay Chưa đủ thông tin.
- Hai là giải thích lý do cho phán quyết đó, phần này gọi là justification.
- LLM nhớ nhiều kiến thức nên làm khá tốt, nhưng vẫn có hai vấn đề: nhớ sai và suy luận sai.
- Từ đó bài báo đặt câu hỏi trung tâm: làm sao tự động chấm điểm năng lực fact-checking một cách công bằng, để biết mô hình nào thật sự đáng tin.

### Slide "Hạn chế của các phương pháp đánh giá hiện có" `[~50s]`
- Cách đánh giá cũ có ba hạn chế.
- Một, gán nhãn thủ công: tốn kém, khó mở rộng quy mô.
- Hai, dùng dataset tĩnh: dễ rò rỉ dữ liệu test, và bảng xếp hạng nhanh bão hòa.
- Ba, đa số chỉ đo accuracy của verdict, tức đo nhãn đúng sai, mà bỏ qua phần lập luận.
- Hình bên phải: (a) là pipeline cũ, (b) là FACT-AUDIT.
- Ý cốt lõi cần nhớ: verdict đúng không có nghĩa lập luận đúng. Mô hình có thể đoán trúng nhãn nhưng lý do thì sai hoặc rỗng.

### Divider Phần 2 — "FACT-AUDIT framework" `[~5s]`
- Sang phần hai: khung FACT-AUDIT.
- Hai điểm chính: ba giai đoạn lặp, và Importance Sampling để nhắm điểm yếu.

### Slide "FACT-AUDIT: ý tưởng cốt lõi" `[~60s]`
- FACT-AUDIT có hai đặc trưng mới so với cách cũ.
- Một, test data được cập nhật động, không phải bộ cố định.
- Hai, chấm sâu cả justification, không chỉ verdict.
- Cách tiếp cận: agent-driven và model-centric, tức tự thích nghi theo từng mô hình bị test.
- Phần công thức bên phải em nói ý thôi: thay vì lấy mẫu Monte Carlo rải đều và hội tụ chậm, framework dùng Importance Sampling.
- Nói nôm na, dùng một phân phối q để dồn mẫu vào đúng vùng mô hình hay sai, nhờ vậy đánh giá hiệu quả hơn nhiều.

### Slide "Pipeline 3 giai đoạn" `[~50s]`
- Đây là pipeline ba giai đoạn, chạy thành vòng lặp.
- Giai đoạn một, Prototype Emulation: sinh dữ liệu kiểm thử.
- Giai đoạn hai, Fact Verification: chấm điểm cả nhãn lẫn lập luận.
- Giai đoạn ba, Adaptive Updating: phân tích chỗ mô hình làm kém rồi cập nhật lại cây kịch bản.
- Quan trọng nhất là tính lặp: mỗi vòng lại nhắm sâu hơn vào điểm yếu của mô hình.
- Ba nhóm kịch bản khởi tạo: Complex Claim, Fake News, Social Rumor.
- **Bàn giao:** Đó là phần bối cảnh và ý tưởng khung của em. Tiếp theo em mời bạn Quang trình bày chi tiết năm agent và kết quả.

---

## TRẦN TÚ QUANG — Phần 3 · Phần 4

### Slide "Khung 5 Agent" (mở đầu của Tiến) `[~50s]`
- **Mở đầu:** Cảm ơn Tiến. Em là Trần Tú Quang, xin trình bày năm agent, cấu trúc test case, rồi bộ chỉ số và kết quả.
- Framework vận hành bằng năm agent, mỗi agent một vai.
- Appraiser: xây và cập nhật cây kịch bản, ở giai đoạn một và ba.
- Inquirer: sinh đề, tức prototype test data.
- Quality Inspector: kiểm chất lượng và độ đa dạng, đối chiếu bằng chứng qua Wikipedia API.
- Evaluator: đóng vai LLM-as-a-Judge, chấm Grade từ 1 đến 10.
- Prober: dò lặp để sinh case khó hơn.
- Hình dưới minh họa toàn cảnh năm agent qua ba giai đoạn, bằng ví dụ thật về thuốc mới chữa tiểu đường.

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

### Slide "Metrics đánh giá" `[~40s]`
- Có ba chỉ số.
- IMR, Insight Mastery Rate: tỉ lệ câu bị chấm từ 3 điểm trở xuống, tức có lỗi. Đây là chỉ số chủ đạo, càng thấp càng tốt.
- JFR, Justification Flaw Rate: tỉ lệ case verdict đúng nhưng lập luận kém. Cũng càng thấp càng tốt.
- Grade: điểm của Evaluator, từ 1 đến 10, càng cao càng tốt.
- Đáng chú ý là JFR: nó tách đúng trường hợp mô hình đoán trúng nhãn nhưng lập luận rỗng, đúng tinh thần verdict khác justification.

### Slide "Kết quả: 13 LLM (Table 1)" `[~40s]`
- Đây là bảng đầy đủ 13 mô hình, có IMR, JFR, Grade ở cả ba nhóm và cột Overall.
- Chỗ khoanh đỏ: GPT-4o đạt IMR thấp nhất, khoảng 12 phần trăm, tức tốt nhất.
- Đáng chú ý Qwen2.5-72B, mô hình mã nguồn mở, bám rất sát nhóm proprietary; dòng LLaMA thì yếu hơn.
- Một điểm nữa: prototype do người tạo và do mô hình tạo cho kết quả gần như nhau, khẳng định framework đánh giá công bằng.

### Slide "Phân tích sâu" `[~30s]`
- Hai phân tích bổ sung.
- Bên trái: hai kịch bản khó nhất của mỗi nhóm, ví dụ suy luận nhiều bước, hoặc tiêu đề lệch nội dung.
- Bên phải: IMR giảm dần rồi hội tụ qua các vòng probing.
- Điều này chứng minh framework đào đúng điểm yếu, và quá trình lặp là ổn định.

### Slide "Test Mode quyết định độ khó" `[~35s]`
- Bảng này cho thấy độ khó phụ thuộc mạnh vào Test Mode.
- Chế độ claim, không bằng chứng, khó nhất: GPT-4o có IMR 23 phần trăm.
- Chế độ wisdom of crowds ở giữa.
- Chế độ evidence, có bằng chứng, dễ nhất: IMR chỉ còn khoảng 10 phần trăm.
- Kết luận quan trọng: có bằng chứng giúp mô hình fact-check chính xác hơn hẳn, IMR giảm khoảng hai lần.
- Đây chính là cơ sở để nhóm đề xuất tích hợp RAG ở phần sau.
- **Bàn giao:** Phần bộ chỉ số và kết quả của paper đến đây là hết. Em mời bạn Ấn trình bày phần thực nghiệm tái hiện của nhóm.

---

_Tổng thời lượng gợi ý: Tiến ~4 phút 45 giây · Quang ~4 phút 25 giây._
