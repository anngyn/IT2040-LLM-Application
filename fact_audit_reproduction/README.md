# FACT-AUDIT-Inspired Reproduction

Thu muc nay la phan viec cua **Mr. To - Code/Reproduction** trong do an:

```text
Static baseline + dynamic prototype + FACT-AUDIT+RAG comparison
```

Muc tieu la dung mot phien ban gan paper nhung vua suc de nhom co the:

- chay smoke test 1-3 claims;
- chay baseline mini 10-30 claims;
- sinh test case dong theo taxonomy cua FACT-AUDIT khi co model that;
- xuat JSONL/CSV theo schema thong nhat;
- dua output cho phan FACT-AUDIT+RAG so sanh;
- demo duoc ke ca khi API/GPU loi nho cached output.

## Hai Luong Chay

- `static baseline`: dung dataset co san, phu hop de demo nhanh va so sanh on dinh.
- `dynamic prototype`: sinh claim moi theo taxonomy cua FACT-AUDIT, gan paper hon nhung can Gemini/OpenAI/local model.

Repo nay khong tu nhan la tai hien day du FACT-AUDIT goc. Phan gan paper hon nam o nhanh `dynamic prototype`.

## Reports

- `docs/checklist_mr_to_code_reproduction.md`: checklist cong viec va doi chieu cot Notes
- `docs/mock_test_report.md`: tong hop ket qua mock test de chia se trong nhom

## Source Materials

Thu muc `source_materials/` chi giu:

- `2025.acl-long.17.pdf`: bai bao FACT-AUDIT de doi chieu phuong phap
- `fact_audit_task_assignment_tracker.xlsx`: file phan cong cong viec cua nhom

## Tac Dung Tung File/Thu Muc

| File/thu muc | Tac dung |
|---|---|
| `config.yaml` | Cau hinh mac dinh: provider, model, input claim set, output JSONL/CSV |
| `.env.example` | Mau file `.env`; dung khi chay API that; khong chua API key that |
| `requirements.txt` | Ghi chu dependency; mock mode dung standard library |
| `data/source/fact_checking_normalized.jsonl` | Dataset normalized nguon de tao claim set |
| `data/claim_sets/claim_set_30.jsonl` | Claim set chung 30 mau de baseline va RAG chay cung du lieu |
| `source_materials/2025.acl-long.17.pdf` | PDF bài báo FACT-AUDIT |
| `source_materials/fact_audit_task_assignment_tracker.xlsx` | Excel phân công công việc |
| `fact_audit_baseline/config.py` | Doc `.env`, config YAML, va chon model theo provider |
| `fact_audit_baseline/io_utils.py` | Đọc/ghi JSONL và CSV |
| `fact_audit_baseline/prompting.py` | Tạo prompt theo format FACT-AUDIT-style |
| `fact_audit_baseline/llm_client.py` | LLM client linh hoạt: `mock`, `gemini`, `openai`, `transformers` |
| `fact_audit_baseline/evaluator.py` | Parse response và chấm điểm baseline đơn giản |
| `scripts/make_claim_set.py` | Tạo claim set 30 mẫu từ dataset local |
| `scripts/generate_dynamic_claim_set.py` | Sinh claim set dong tu taxonomy cua FACT-AUDIT bang model that |
| `scripts/run_smoke_test.py` | Chạy end-to-end 3 claims để kiểm tra pipeline |
| `scripts/run_baseline.py` | Chạy baseline chính và xuất JSONL/CSV |
| `scripts/run_baseline_demo.py` | Script demo ổn định, hỗ trợ `--use-cache` |
| `notebooks/run_baseline_pipeline.ipynb` | Notebook gom cac buoc chay lai pipeline trong mot cho |
| `schemas/schema_baseline.json` | Contract output baseline cho nhóm RAG |
| `schemas/schema_rag.json` | Contract output phía FACT-AUDIT+RAG |
| `outputs/smoke_test.jsonl` | Kết quả smoke test 3 claims |
| `outputs/smoke_test_scores.csv` | Bảng điểm smoke test |
| `outputs/baseline_results.jsonl` | Kết quả baseline 30 claims |
| `outputs/scores.csv` | Bảng score baseline có các cột yêu cầu trong Excel |
| `outputs/cached_demo/` | Output demo cache để trình bày khi API/GPU lỗi |
| `docs/checklist_mr_to_code_reproduction.md` | Checklist C2.1-C2.8 va doi chieu cot Notes |
| `docs/mock_test_report.md` | Report mock test de gui cho thanh vien khac |
| `docs/environment_notes.md` | Ghi chu moi truong chay, Python version, official repo |
| `docs/mr_to_task_mapping.md` | Mapping task Excel sang file/output trong repo |

## Chạy Nhanh

Chay tu root repo:

```bash
cd fact_audit_reproduction
python3 scripts/make_claim_set.py --size 30
python3 scripts/run_smoke_test.py
python3 scripts/run_baseline.py
python3 scripts/run_baseline_demo.py --use-cache
```

Output ky vong:

```text
data/claim_sets/claim_set_30.jsonl
outputs/smoke_test.jsonl
outputs/smoke_test_scores.csv
outputs/baseline_results.jsonl
outputs/scores.csv
outputs/cached_demo/baseline_demo_results.jsonl
outputs/cached_demo/demo_scores.csv
```

## Chay Dynamic Prototype

Dynamic prototype gan tinh than FACT-AUDIT hon vi khong lay claim truc tiep tu dataset tinh, ma sinh claim moi theo taxonomy.

Vi du voi Gemini:

```bash
cd fact_audit_reproduction
python3 scripts/generate_dynamic_claim_set.py --provider gemini --model gemini-2.5-flash --size 12
python3 scripts/run_baseline.py --input-file data/claim_sets/dynamic_claim_set_12.jsonl --provider gemini --model gemini-2.5-flash
```

Dau ra mac dinh:

```text
data/claim_sets/dynamic_claim_set_12.jsonl
```

## Chay Voi API That

Tao file `.env` tu mau:

```bash
cp .env.example .env
```

### Dung Gemini

Dien vao `.env`:

```bash
GEMINI_API_KEY=your_real_key
GEMINI_MODEL=gemini-2.5-flash
```

Doi `config.yaml`:

```yaml
llm:
  provider: gemini
  model: gemini-2.5-flash
```

Chạy:

```bash
python3 scripts/run_baseline.py --provider gemini --model gemini-2.5-flash
```

Neu ban lam nhanh RAG voi Gemini thi process tiep theo la:

1. Retriever lấy top-k evidence cho từng `claim_id`.
2. Prompt RAG ghép `claim + retrieved_evidence`.
3. Gọi Gemini để sinh `rag_verdict` và `rag_justification`.
4. Xuất file đúng `schemas/schema_rag.json`.
5. Neu chay so sanh baseline vs RAG, dung cung mot claim set cho ca hai nhanh.

### Dung OpenAI-compatible

Dien API key vao `.env`, sau do doi `config.yaml`:

```yaml
llm:
  provider: openai
  model: gpt-4o-mini
```

Chạy:

```bash
python3 scripts/run_baseline.py --provider openai --model gpt-4o-mini
```

Khong commit `.env`.

## Schema Dung Chung Voi Nhom RAG

Baseline output schema:

```text
schemas/schema_baseline.json
```

RAG output schema:

```text
schemas/schema_rag.json
```

Khóa nối chung khi so sánh:

```text
claim_id
```

Baseline và RAG nên chạy cùng file:

```text
data/claim_sets/claim_set_30.jsonl
```

## Ghi Chu Don Repo

Repo hien chi giu phan dang dung cho static baseline, dynamic prototype, va tai lieu tham chieu toi thieu.
