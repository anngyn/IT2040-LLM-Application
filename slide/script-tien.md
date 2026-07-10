# Script văn nói (bullet) — Tô Huỳnh Minh Tiến

> Cue-card để cầm trình bày. Mỗi slide một cụm bullet, nói theo ý, không cần đọc nguyên văn.
> Phần của **Tiến**: slide bìa → Nội dung → Phần 1 (Bối cảnh) → Phần 2 (FACT-AUDIT framework). Xong bàn giao cho **Quang**.
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

_Tổng thời lượng gợi ý: ~4 phút 25 giây._
