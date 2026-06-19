# Report Kiểm Thử Mock Baseline

Ngày kiểm thử: `2026-06-19`

Người tổng hợp: `Mr. Tô`

## Mục Đích

Report này tổng hợp kết quả chạy lại các bài test ở chế độ `mock` trong pipeline FACT-AUDIT-inspired reproduction.

Mục tiêu của `mock test`:

- Kiểm tra pipeline có chạy end-to-end hay không.
- Kiểm tra format input/output JSONL và CSV có đúng schema không.
- Kiểm tra script baseline, demo, smoke test có hoạt động ổn định không.
- Không dùng để đánh giá chất lượng fact-checking thực tế của mô hình.

## Phạm Vi Kiểm Thử

Đã chạy lại 3 script sau:

```bash
python3 fact_audit_reproduction/scripts/run_smoke_test.py
python3 fact_audit_reproduction/scripts/run_baseline_demo.py
python3 fact_audit_reproduction/scripts/run_baseline.py
```

Tất cả đều chạy bằng provider mặc định `mock`.

## Kết Quả

### 1. Smoke test 3 mẫu

- Script: `fact_audit_reproduction/scripts/run_smoke_test.py`
- Output:
  - `fact_audit_reproduction/outputs/smoke_test.jsonl`
  - `fact_audit_reproduction/outputs/smoke_test_scores.csv`
- Kết quả:
  - Số mẫu: `3`
  - Verdict đúng: `2/3`
  - Điểm trung bình: `6.67`

Ý nghĩa:

- Xác nhận pipeline có thể đọc claim set, tạo prompt, sinh kết quả, chấm điểm, và ghi file output.
- Phù hợp để smoke test nhanh sau mỗi lần sửa code.

### 2. Baseline demo 5 mẫu

- Script: `fact_audit_reproduction/scripts/run_baseline_demo.py`
- Output:
  - `fact_audit_reproduction/outputs/cached_demo/baseline_demo_results.jsonl`
  - `fact_audit_reproduction/outputs/cached_demo/demo_scores.csv`
- Kết quả:
  - Số mẫu: `5`
  - Verdict đúng: `3/5`
  - Điểm trung bình: `6.20`

Ý nghĩa:

- Đây là bản demo nhỏ gọn hơn full baseline.
- Phù hợp để trình bày nhanh trong nhóm hoặc demo trên máy không có API key.

### 3. Full baseline 30 mẫu

- Script: `fact_audit_reproduction/scripts/run_baseline.py`
- Output:
  - `fact_audit_reproduction/outputs/baseline_results.jsonl`
  - `fact_audit_reproduction/outputs/scores.csv`
- Kết quả:
  - Số mẫu: `30`
  - Verdict đúng: `9/30`
  - Điểm trung bình: `4.10`

Ý nghĩa:

- Xác nhận pipeline baseline đầy đủ vẫn chạy hết 30 claims.
- Điểm thấp là bình thường vì `mock` chỉ là heuristic offline, không phải LLM thật.

## Nhận Xét Chung

- Phần `mock` hiện đã chạy ổn định và lặp lại được.
- Output JSONL/CSV được tạo thành công cho cả smoke test, demo, và full baseline.
- `mock` hữu ích để kiểm tra code, schema, và pipeline.
- `mock` không nên dùng để rút ra kết luận về năng lực fact-checking của hệ thống.

## Giới Hạn Của Mock Test

- Không truy cập web hoặc tri thức động.
- Không mô phỏng đầy đủ hành vi của Gemini/OpenAI/local LLM.
- Có thể dùng để xác nhận code không vỡ pipeline, nhưng không dùng để so sánh học thuật.

## Khi Nào Nên Dùng Mock

Nên dùng `mock` khi:

- Muốn kiểm tra nhanh sau khi sửa code.
- Muốn chia sẻ cho thành viên khác để họ chạy được ngay.
- Không có API key hoặc không muốn tốn chi phí gọi model.

Nên dùng `gemini` hoặc provider thật khi:

- Cần sinh claim động.
- Cần kết quả gần với tinh thần của bài báo FACT-AUDIT hơn.
- Cần đánh giá chất lượng verdict/justification nghiêm túc hơn.

## File Liên Quan

- `fact_audit_reproduction/scripts/run_smoke_test.py`
- `fact_audit_reproduction/scripts/run_baseline_demo.py`
- `fact_audit_reproduction/scripts/run_baseline.py`
- `fact_audit_reproduction/fact_audit_baseline/llm_client.py`

## Kết Luận

Tính đến ngày `2026-06-19`, phần `mock baseline` đã:

- chạy được,
- ghi output đúng định dạng,
- phù hợp để demo và regression check,
- sẵn sàng để chia sẻ cho các thành viên khác trong nhóm.
