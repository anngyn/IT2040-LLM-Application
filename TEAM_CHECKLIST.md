# Checklist Nhiệm Vụ Cho Các Thành Viên Còn Lại

Dưới đây là danh sách công việc chi tiết dành cho các thành viên trong nhóm (ngoài phần code RAG/Baseline đã check ở file của bạn), cùng với các đầu việc chung mà cả nhóm cần phối hợp hoàn thiện.

## 1. Thành viên: Quang Tèo (Theory / Slides)
*Hiện trạng: Toàn bộ các task đều chưa bắt đầu hoặc đang làm dở.*

- [ ] **T1.1**: Đọc paper, tóm tắt problem & motivation (Yêu cầu: Tóm tắt khoảng 1 trang, nhấn mạnh vào benchmark tĩnh, data leakage, và thiếu đánh giá justification).
- [ ] **T1.2**: Vẽ sơ đồ pipeline FACT-AUDIT gốc (Yêu cầu: Đưa lên slide luồng Prototype Emulation → Fact Verification → Adaptive Updating).
- [ ] **T1.3**: Giải thích vai trò của các Agent (Yêu cầu: Làm bảng phân vai cho Appraiser, Inquirer, Quality Inspector, Evaluator, Prober).
- [ ] **T1.4**: Tóm tắt metrics đánh giá (Yêu cầu: Cần slide giải thích IMR, JFR, Grade và ví dụ phân biệt verdict vs justification).
- [ ] **T1.5**: Tóm tắt experiments gốc trong paper (Yêu cầu: Bảng kết quả, nhấn mạnh việc nhóm không tái lập full 13 LLM mà chỉ làm scope nhỏ).
- [ ] **T1.6**: Viết luận điểm chứng minh vì sao mở rộng thêm RAG là hợp lý (Yêu cầu: Bám vào phần future work / limitation của paper gốc).
- [ ] **T1.7**: Soạn storyline và nội dung thô cho slide 1–9.
- [ ] **T1.8**: Viết speaker notes (kịch bản thuyết trình) phần lý thuyết (Yêu cầu: Script dài khoảng 7 phút).


## 2. Thành viên: Mr. Tô / Cu Ấn (Nếu user chỉ là 1 trong 2 người)
*(Lưu ý: Nếu bạn chỉ đảm nhận RAG hoặc chỉ đảm nhận Baseline, hãy chuyển các task chưa làm của mảng còn lại cho thành viên tương ứng)*
- [ ] **C2.6** (Mr. Tô): Viết script gom log json thành 1 file `scores.csv` tổng hợp cho Baseline.
- [ ] **C2.7** (Mr. Tô): Tạo script `run_baseline_demo.py` để demo offline (có cache).
- [ ] **C2.8** (Mr. Tô): Viết `README.md` hướng dẫn chạy script cho cả nhóm.
- [ ] **I3.2** (Cu Ấn): Viết file chứa 10-30 claim mẫu `sample_claims_en/vi.jsonl` để demo chung.
- [ ] **I3.7** (Cu Ấn): Lọc ra 3-5 case study so sánh trước/sau khi có RAG (`case_studies.md`).
- [ ] **I3.8** (Cu Ấn): Vẽ biểu đồ Bar Chart so sánh điểm của Baseline vs RAG.


## 3. Cả Nhóm (Management / General)
*Các đầu việc cần sự có mặt của tất cả thành viên để thống nhất và chốt sổ trước ngày báo cáo.*

- [ ] **G4.1**: Chốt scope final (Quyết định chính xác số lượng claim, model sẽ báo cáo: Baseline vs FACT-AUDIT+RAG).
- [ ] **G4.2**: Review chung về input/output schema giữa Baseline và RAG để đảm bảo không lệch form.
- [ ] **G4.3**: Ghép Slide v1 (Gom slide lý thuyết của Tèo và chart/result của team Code, giới hạn 15–18 slides).
- [ ] **G4.4**: Rehearsal lần 1 (Mục tiêu: Căn thời gian thuyết trình cả nhóm dưới 22 phút).
- [ ] **G4.5**: Quay video demo backup (Quay lại màn hình chạy script demo, dài 2-4 phút đề phòng hôm báo cáo bị lỗi mạng/API).
- [ ] **G4.6**: Đóng gói Final Submission (Tạo `final_package.zip` hoặc GitHub release chứa source code, file output mẫu, slide và README).
- [ ] **G4.7**: Tổng duyệt Final (Rehearsal lần cuối, yêu cầu trơn tru dưới 20 phút).
