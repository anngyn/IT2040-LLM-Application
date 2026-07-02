# Tiến độ công việc (My Progress Checklist)

Dưới đây là danh sách tổng hợp chi tiết các task thuộc khối kỹ thuật (**Reproduction & RAG**) dựa trên file mã nguồn hiện tại trong `external/FACT-AUDIT` và thư mục `fact_audit_reproduction`.

## ✅ Những task ĐÃ HOÀN THÀNH (Done)

### Code / Reproduction (Mr. Tô)
- [x] **C2.1**: Clone repo FACT-AUDIT và tạo môi trường chạy (Đã có source trong `external/FACT-AUDIT`).
- [x] **C2.2**: Tách API key/model path ra `.env`/config (Đã setup `.env` và `.env.example`).
- [x] **C2.3**: Chạy smoke test 1–3 claims (Đã có `test_api.py` để test call API).
- [x] **C2.5**: Thêm LLM client linh hoạt (Đã làm fallback cho LLaMA sang Groq/OpenRouter).

### Innovation / FACT-AUDIT+RAG (Cu Ấn)
- [x] **I3.3**: Implement retriever cắm trước target LLM (Đã có Wikipedia retriever).
- [x] **I3.4**: Implement augmented prompt với evidence (Đã hoàn thiện file `fact-audit-rag.py`).
- [x] **I3.5**: Chạy FACT-AUDIT+RAG trên cùng test set (Đã xuất ra `rag_results.jsonl`).
- [x] **I3.6**: So sánh baseline vs FACT-AUDIT+RAG (Đã có `comparison_report.csv`).


## ⏳ Những task ĐANG DỞ DANG (In Progress)
- [ ] **C2.4**: Chạy baseline mini 10–30 claims.
  *Tiến độ thực tế:* Đã chạy 10 version trong thư mục `result/factaudit/gpt-4o/complex_claim/`. Tuy nhiên mới chỉ có 6 folder (`1, 4, 5, 6, 8, 9`) sinh ra file `log.json`, 4 folder còn lại bị rỗng. Cần fix lỗi hoặc chạy lại để có đủ output.


## ❌ Những task CHƯA LÀM (To Do)

### Code / Reproduction
- [ ] **C2.6**: Chuẩn hóa output baseline JSONL/CSV (Cần script gộp 10 file `log.json` ở task C2.4 thành 1 file `scores.csv` có chứa các cột: claim_id, claim, verdict, justification, score, latency, cost).
- [ ] **C2.7**: Tạo script demo baseline ổn định (Làm script `run_baseline_demo.py` đọc từ file cache có sẵn).
- [ ] **C2.8**: Viết README kỹ thuật phần baseline (Chỉnh sửa `README.md` trong thư mục `external` để hướng dẫn nhóm cách setup).

### Innovation / FACT-AUDIT+RAG
- [ ] **I3.2**: Thiết kế sample claims EN/VI dùng chung (Cần gom ra 1 file `sample_claims_en/vi.jsonl` chuẩn).
- [ ] **I3.7**: Phân tích 3–5 case before/after (Tạo `case_studies.md` so sánh log baseline vs log RAG).
- [ ] **I3.8**: Tạo visualization cho kết quả so sánh (Vẽ biểu đồ bar chart từ `comparison_report.csv`).
