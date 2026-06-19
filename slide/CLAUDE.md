# CLAUDE.md — Deck FACT-AUDIT + RAG (rules)

Slide báo cáo môn **IT2040 — Các mô hình ngôn ngữ lớn & ứng dụng**. File chính: `slides.md`.

## Thông tin cố định (không tự đổi)
- **Nhóm 8.** Thành viên: **Trần Tú Quang · Tô Huỳnh Minh Tiến · Nguyễn Ấn**.
- **GVHD: TS. Lưu Thanh Sơn.**
- Trường: **University of Information Technology, VNU-HCM (UIT)**.
- Địa điểm/ngày: **Ho Chi Minh, 7/2026** (đổi nếu lịch báo cáo thay đổi).
- Đề tài dựa trên paper: Lin et al., *FACT-AUDIT*, ACL 2025, arXiv 2502.17924.

## Style (kế thừa template navy — xem `@./CLAUDE.md`)
- Theme **navy `#1F3A68`** + font **Be Vietnam Pro**, tỉ lệ 16:9.
- Header bar navy (`##`), footer 4 ô `Nhóm 8 · IT2040 · FACT-AUDIT · Ngày · Trang`, logo UIT góc phải, số trang `x / total`.
- Slide bìa: hộp tiêu đề → tên thành viên → GVHD → môn `·` Báo cáo cuối kỳ → Ho Chi Minh, ngày. **Không** có dòng "Dựa trên: …" ở slide bìa.

## Văn phong (rule người dùng — TUÂN THỦ)
- **Hạn chế em-dash (—):** nhãn dùng `:`; trong câu dùng `,` hoặc `·`.
- **Hạn chế icon/emoji.**
- Trình bày súc tích, tiếng Việt; thuật ngữ kỹ thuật giữ tiếng Anh (verdict, justification, claim, evidence...).

## Sơ đồ
- Pre-render Mermaid ra SVG, KHÔNG inline (xem rule template). Nguồn + SVG trong `diagrams/`:
  - `pipeline.svg` — pipeline 3 giai đoạn FACT-AUDIT (vòng lặp)
  - `rag.svg` — pipeline RAG (retriever cắm trước target LLM)
- Render lại sau khi sửa `.mmd`:
  `npx -y @mermaid-js/mermaid-cli -i diagrams/<x>.mmd -o diagrams/<x>.svg -c diagrams/mermaid-config.json -b transparent`

## Nội dung đã chốt (đối chiếu paper)
- Metric: **IMR = Insight Mastery Rate** (chủ đạo, % câu Grade ≤ 3); **JFR = Justification Flaw Rate** (verdict đúng nhưng lập luận kém); **Grade 1–10**. (Không ghi nhầm "Incorrect/Misinformation" hay "Failure".)
- 5 agent: Appraiser, Inquirer, Quality Inspector, Evaluator, Prober.
- Pipeline 3 stage: Prototype Emulation → Fact Verification + Justification → Adaptive Updating (Importance Sampling).
- Luận điểm RAG: paper TỰ đề xuất RAG ở mục Limitations; Table 3 cho thấy mode `[evidence]` dễ hơn `[claim]` → RAG cấp evidence kỳ vọng giảm IMR/JFR.

## Lưu ý phạm vi
- Deck này là **phần lý thuyết (Quang)**. Số liệu baseline vs RAG thật do Mr. Tô (Tiến) & Cu Ấn (Ấn) cung cấp; hiện đang dùng số liệu paper gốc làm minh hoạ.
