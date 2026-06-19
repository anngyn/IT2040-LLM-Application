# Report Kiem Thu Mock Baseline

Ngay kiem thu: `2026-06-19`

Nguoi tong hop: `Mr. To`

## Muc Dich

Report nay tong hop ket qua chay lai cac bai test o che do `mock` trong pipeline FACT-AUDIT-inspired reproduction.

Muc tieu cua `mock test`:

- Kiem tra pipeline co chay end-to-end hay khong.
- Kiem tra format input/output JSONL va CSV co dung schema khong.
- Kiem tra script baseline, demo, smoke test co hoat dong on dinh khong.
- Khong dung de danh gia chat luong fact-checking thuc te cua mo hinh.

## Pham Vi Kiem Thu

Da chay lai 3 script sau:

```bash
python3 fact_audit_reproduction/scripts/run_smoke_test.py
python3 fact_audit_reproduction/scripts/run_baseline_demo.py
python3 fact_audit_reproduction/scripts/run_baseline.py
```

Tat ca deu chay bang provider mac dinh `mock`.

## Ket Qua

### 1. Smoke test 3 mau

- Script: `fact_audit_reproduction/scripts/run_smoke_test.py`
- Output:
  - `fact_audit_reproduction/outputs/smoke_test.jsonl`
  - `fact_audit_reproduction/outputs/smoke_test_scores.csv`
- Ket qua:
  - So mau: `3`
  - Verdict dung: `2/3`
  - Diem trung binh: `6.67`

Y nghia:

- Xac nhan pipeline co the doc claim set, tao prompt, sinh ket qua, cham diem, va ghi file output.
- Phu hop de smoke test nhanh sau moi lan sua code.

### 2. Baseline demo 5 mau

- Script: `fact_audit_reproduction/scripts/run_baseline_demo.py`
- Output:
  - `fact_audit_reproduction/outputs/cached_demo/baseline_demo_results.jsonl`
  - `fact_audit_reproduction/outputs/cached_demo/demo_scores.csv`
- Ket qua:
  - So mau: `5`
  - Verdict dung: `3/5`
  - Diem trung binh: `6.20`

Y nghia:

- Day la ban demo nho gon hon full baseline.
- Phu hop de trinh bay nhanh trong nhom hoac demo tren may khong co API key.

### 3. Full baseline 30 mau

- Script: `fact_audit_reproduction/scripts/run_baseline.py`
- Output:
  - `fact_audit_reproduction/outputs/baseline_results.jsonl`
  - `fact_audit_reproduction/outputs/scores.csv`
- Ket qua:
  - So mau: `30`
  - Verdict dung: `9/30`
  - Diem trung binh: `4.10`

Y nghia:

- Xac nhan pipeline baseline day du van chay het 30 claims.
- Diem thap la binh thuong vi `mock` chi la heuristic offline, khong phai LLM that.

## Nhan Xet Chung

- Phan `mock` hien da chay on dinh va lap lai duoc.
- Output JSONL/CSV duoc tao thanh cong cho ca smoke test, demo, va full baseline.
- `mock` huu ich de kiem tra code, schema, va pipeline.
- `mock` khong nen dung de rut ra ket luan ve nang luc fact-checking cua he thong.

## Gioi Han Cua Mock Test

- Khong truy cap web hoac tri thuc dong.
- Khong mo phong day du hanh vi cua Gemini/OpenAI/local LLM.
- Co the dung de xac nhan code khong vo pipeline, nhung khong dung de so sanh hoc thuat.

## Khi Nao Nen Dung Mock

Nen dung `mock` khi:

- Muon kiem tra nhanh sau khi sua code.
- Muon chia se cho thanh vien khac de ho chay duoc ngay.
- Khong co API key hoac khong muon ton chi phi goi model.

Nen dung `gemini` hoac provider that khi:

- Can sinh claim dong.
- Can ket qua gan voi tinh than cua bai bao FACT-AUDIT hon.
- Can danh gia chat luong verdict/justification nghiem tuc hon.

## File Lien Quan

- `fact_audit_reproduction/scripts/run_smoke_test.py`
- `fact_audit_reproduction/scripts/run_baseline_demo.py`
- `fact_audit_reproduction/scripts/run_baseline.py`
- `fact_audit_reproduction/fact_audit_baseline/llm_client.py`

## Ket Luan

Tinh den ngay `2026-06-19`, phan `mock baseline` da:

- chay duoc,
- ghi output dung dinh dang,
- phu hop de demo va regression check,
- san sang de chia se cho cac thanh vien khac trong nhom.
