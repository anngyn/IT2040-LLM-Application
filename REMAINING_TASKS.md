# Danh sách các task cần làm (Remaining Tasks)

Dựa trên file tracking (`fact_audit_task_assignment_tracker.xlsx`) và những code đã được push (tích hợp RAG, API fallback, config GPT provider, xuất kết quả baseline và RAG), dưới đây là các task **chưa hoàn thành** cần được ưu tiên xử lý để kịp tiến độ.

## 1. Nhóm Theory/Slides (Tèo - Theory/Slides)
*Tất cả các task phần lý thuyết và slide đều đang ở trạng thái chưa hoàn thành hoặc đang làm dở.*
- [ ] **T1.1**: Đọc paper, tóm tắt problem & motivation (Tóm tắt 1 trang).
- [ ] **T1.2**: Vẽ pipeline FACT-AUDIT gốc (Prototype Emulation → Fact Verification → Adaptive Updating).
- [ ] **T1.3**: Giải thích vai trò các agent trong FACT-AUDIT (Appraiser, Inquirer, Quality Inspector, Evaluator, Prober).
- [ ] **T1.4**: Tóm tắt metrics IMR/JFR/Grade.
- [ ] **T1.5**: Tóm tắt experiments gốc trong paper.
- [ ] **T1.6**: Viết luận điểm vì sao thêm RAG là hợp lý (Dựa trên limitation của paper).
- [ ] **T1.7**: Soạn storyline slide 1–9.
- [ ] **T1.8**: Viết speaker notes phần lý thuyết (Script 7 phút).

## 2. Nhóm Code/Reproduction (Mr. Tô - Code/Reproduction)
*Đã hoàn thành C2.5 (LLM Client linh hoạt) và một phần pipeline baseline. Các phần còn lại:*
- [ ] **C2.6**: Chuẩn hóa output baseline JSONL/CSV (`scores.csv` với các cột claim_id, claim, verdict, justification, score, latency, cost).
- [ ] **C2.7**: Tạo script demo baseline ổn định (`run_baseline_demo.py` có chế độ dùng cached output).
- [ ] **C2.8**: Viết README kỹ thuật phần baseline (Cách setup, chạy baseline, chạy cached demo).

## 3. Nhóm Innovation: FACT-AUDIT+RAG (Cu Ấn - FACT-AUDIT+RAG)
*Đã hoàn thành I3.3 (Retriever), I3.4 (Augmented prompt), I3.5 (rag_results.jsonl), I3.6 (comparison_report.csv).*
- [ ] **I3.2**: Thiết kế sample claims EN/VI dùng chung (`sample_claims_en/vi.jsonl` 10–30 claims để demo case study).
- [ ] **I3.7**: Phân tích 3–5 case before/after (`case_studies.md` chứa claim, evidence, baseline output, RAG output).
- [ ] **I3.8**: Tạo visualization cho kết quả so sánh (Bar chart so sánh baseline vs RAG trong notebook hoặc script tạo chart).

## 4. Nhóm Management/General (Cả nhóm)
- [ ] **G4.1**: Chốt scope final (Baseline vs FACT-AUDIT+RAG).
- [ ] **G4.2**: Review schema baseline ↔ RAG.
- [ ] **G4.3**: Ghép slide v1 (`deck_v1.pptx` 15–18 slides).
- [ ] **G4.4**: Rehearsal lần 1.
- [ ] **G4.5**: Quay video demo backup (2-4 phút).
- [ ] **G4.6**: Đóng gói final submission (`final_package.zip` / GitHub release).
- [ ] **G4.7**: Tổng duyệt final.
