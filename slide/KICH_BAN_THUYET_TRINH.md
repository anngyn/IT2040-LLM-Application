# Kịch bản thuyết trình — Phần lý thuyết FACT-AUDIT (Quang)

Cue-card: chỉ key cần nói + ví dụ cụ thể. Không đọc nguyên văn.

---

## Bìa + Nội dung trình bày (~45s)
- Giới thiệu đề tài, nhóm, GVHD. Nói rõ: phần lý thuyết (mình) → phần cài đặt/kết quả (Tiến, Ấn).
- 6 phần: bối cảnh → framework → 5 agent → metrics/kết quả → tái hiện → RAG.
- **Chốt ngay:** đây là framework **đánh giá năng lực**, không phải công cụ kiểm chứng 1 claim.

---

## Phần 1: Bối cảnh & động lực

### Slide "Bài toán & câu hỏi trung tâm"
- Fact-checking = 2 việc: **phán** (Factual/Non-Factual/NEI) + **giải thích** (justification).
- Ví dụ nhanh: LLM bảo "tin này đúng" nhưng không nói được vì sao → chưa đủ.
- Câu hỏi bài báo: đo năng lực này **tự động, công bằng** thế nào?

### Slide "Hạn chế đánh giá hiện có"
- 3 hạn chế: thủ công tốn kém · dataset tĩnh (leak, swamping) · chỉ đo accuracy verdict, bỏ qua justification.
- **Ví dụ cốt lõi (nhắc lại nhiều lần trong bài):** verdict đúng ≠ lập luận đúng.

---

## Phần 2: FACT-AUDIT framework

### Slide "Ý tưởng cốt lõi"
- 2 đặc trưng mới: data **động** + chấm **justification**.
- Toán: Monte Carlo (chọn ngẫu nhiên, chậm O(1/√N)) → Importance Sampling (q(x) nhắm vùng model dễ sai).
- **Ví dụ trực quan:** giống đi tìm lỗi phần mềm — test ngẫu nhiên (MC) vs test tập trung vào module hay lỗi (IS).

### Slide "Pipeline 3 giai đoạn"
- 3 stage lặp: Prototype Emulation → Fact Verification+Justification → Adaptive Updating.
- Nhấn: đây là **vòng lặp**, Θ cập nhật liên tục theo điểm yếu model.
- 3 đối tượng gốc: Complex Claim, Fake News, Social Rumor.

---

## Phần 3: Khung 5 agent & test case

### Slide "Khung 5 Agent"
- 5 vai trò, mỗi vai trò 1 câu: Appraiser (xây/cập nhật taxonomy) → Inquirer (sinh đề) → Quality Inspector (lọc chất lượng, check Wiki) → Evaluator (chấm điểm, LLM-as-Judge) → Prober (dò sâu hơn).
- **Ví dụ paper (Fig 2):** claim "thuốc mới chữa tiểu đường" — key point, source claim, auxiliary info (FDA approval, clinical trial...), test mode [evidence].

### Slide "Taxonomy kịch bản"
- Cây phân loại 3 nhóm, mỗi nhóm nhiều nhánh con (VD Fake News: satire, misleading, fabricated...).
- Cây này **không cố định** — Appraiser mở rộng theo lỗi model.

### Slide "Cấu trúc test case"
- 4 phần: Key Point, Source Claim, Auxiliary Info, Test Mode.
- 3 Test Mode, xếp theo độ khó: `[claim]` (không evidence, khó nhất) > `[wisdom of crowds]` (bình luận MXH) > `[evidence]` (bằng chứng vàng Wiki, dễ nhất).
- **Chốt:** Test Mode là chỗ RAG sẽ tác động (link tới phần 6).

---

## Phần 4: Metrics & Kết quả

### Slide "Metrics đánh giá"
- 3 chỉ số: **IMR** (% Grade≤3, chủ đạo) · **JFR** (verdict đúng nhưng lập luận kém) · **Grade** (1-10).
- Nhắc: IMR cao = tệ (nhiều lỗi), Grade cao = tốt.

### Slide "Case study JFR" (Fig 6)
- **Ví dụ cụ thể, kể chi tiết:** claim tre mọc "35 inch/ngày". GPT-4o trả lời verdict **Factual** (đúng) nhưng giải thích ghi "35 inch (91cm)" — sai quy đổi (35 inch ≈ 88,9cm, còn 91cm = 36 inch).
- Kết quả: Grade chỉ 2/10 dù verdict đúng → đây là JFR bị bắt được, thứ mà đo accuracy thường sẽ bỏ lọt.

### Slide "Kết quả 13 LLM (Table 1)"
- GPT-4o IMR thấp nhất (12.02%) → tốt nhất.
- Điểm hay: Qwen2.5-72B (mã nguồn mở) bám sát nhóm proprietary.
- LLaMA yếu hơn hẳn các dòng khác.

### Slide "Phân tích sâu" (Fig 4, 5)
- Trái: kịch bản khó nhất mỗi nhóm (multi-step reasoning, mismatched headline...).
- Phải: IMR giảm dần & hội tụ qua vòng lặp probing → chứng minh framework hoạt động đúng thiết kế.

### Slide "Test Mode quyết định độ khó"
- GPT-4o: claim 23.1% > wisdom 15.4% > evidence 10.6% (IMR).
- **Chốt quan trọng nhất của cả phần lý thuyết:** có evidence giúp giảm IMR ~2 lần → đây là cơ sở trực tiếp để làm RAG.

---

## Phần 5: Thực nghiệm tái hiện (bàn giao sang Ấn/Tiến nếu cần, hoặc tự trình bày ngắn)

### Slide "Cấu hình tái hiện"
- 3 agent qua API: Optimizer=Judge=gemini-2.5-flash, Target thay đổi.
- Quy mô: 3 seed + 7 adaptive, nhóm complex_claim.
- **Nhắc rõ:** mục tiêu mid-term là tái hiện đúng cơ chế, không phải SOTA.

### Slide "Bằng chứng Importance Sampling"
- **Ví dụ thật:** target LLaMA-4-Scout, seed case `wisdom of crowds` bị điểm 3/10.
- Ngay sau: 6/7 case adaptive tiếp theo đều rơi vào `wisdom of crowds` → đúng q(x) tự dồn vào vùng yếu.
- Có tái hiện cả 2 tầng: Tầng 1 (Prober, sâu trong 1 kịch bản) + Tầng 2 (Appraiser, sinh kịch bản mới — VD "deductive_causal_reasoning").

### Slide "Kết quả so sánh model"
- LLaMA-4-Scout: Grade 8.00, IMR 20%.
- Gemini 2.5 Pro: Grade 9.80, IMR 0%.
- Framework phân biệt được model mạnh/yếu, khớp tinh thần Table 1 paper.

---

## Phần 6: Từ Limitation → RAG

### Slide "3 hạn chế paper tự nêu"
- Nói **đủ 3**, không chỉ RAG: (1) bias của agent controller (GPT-4o cũng có định kiến tri thức) · (2) thiếu tri thức cập nhật động → chỗ RAG · (3) thiếu cơ chế cải thiện model (preference optimization).
- Nhóm chọn khai thác (2) vì có cơ sở rõ nhất (Table 3, evidence > claim).

### Slide "Từ Limitation → RAG (đề xuất)"
- Trích đúng câu paper tự đề xuất RAG.
- Giả thuyết: RAG đưa `[claim]` gần với `[evidence]` → giảm IMR/JFR.
- **Câu hỏi mở, nói thẳng với thầy:** evidence paper là *gold*, RAG thực tế tự động retrieve — nếu retrieval kém liên quan thì chưa chắc cải thiện. Đây là hướng thử nghiệm, kết quả thật để cuối kỳ.

### Slide "Tổng kết mid-term"
- Đã làm: hiểu + trình bày cơ chế, tái hiện qua API, xác nhận Importance Sampling hoạt động, tái hiện 2 tầng, so sánh model.
- Hướng tới: RAG thật, so sánh baseline vs RAG, phân tích chất lượng retrieval.
- Mạch xuyên suốt: hiểu paper → tái hiện được → đề xuất có cơ sở.

### Slide cảm ơn
- Chuyển giao sang Tiến (phần cài đặt/kết quả RAG thật).

---

## Lưu ý khi trình bày
- Timing tổng ước lượng theo speaker notes trong `slides.md`: ~10-12 phút cho phần lý thuyết (18 slide nội dung).
- Nếu bị hỏi xoáy, 2 chỗ dễ bị hỏi nhất:
  1. **"Tại sao IMR ≤3 mà không phải ngưỡng khác?"** → paper chọn theo phân tích thực tiễn, thang 10 điểm, 4.0 là ranh giới tự nhiên giữa thấp/trung bình.
  2. **"RAG có chắc cải thiện không?"** → không chắc, đó là câu hỏi mở nhóm đặt ra, cần thực nghiệm thật (đã có early test cho thấy RAG có thể **làm giảm** điểm nếu evidence không liên quan — nói nếu được hỏi sâu).
