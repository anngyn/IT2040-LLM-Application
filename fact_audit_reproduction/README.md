# FACT-AUDIT Baseline Reproduction

Thư mục này là phần việc của **Mr. Tô - Code/Reproduction** trong đồ án:

```text
Baseline FACT-AUDIT + FACT-AUDIT+RAG comparison
```

Mục tiêu là dựng một baseline chạy được để nhóm có thể:

- chạy smoke test 1-3 claims;
- chạy baseline mini 10-30 claims;
- xuất JSONL/CSV theo schema thống nhất;
- đưa output cho phần FACT-AUDIT+RAG so sánh;
- demo được kể cả khi API/GPU lỗi nhờ cached output.

## Source Materials

Thư mục `source_materials/` hiện chỉ giữ:

- `2025.acl-long.17.pdf`: bài báo FACT-AUDIT để đối chiếu phương pháp.
- `fact_audit_task_assignment_tracker.xlsx`: file phân công công việc của nhóm.

## Tác Dụng Từng File/Thư Mục

| File/thư mục | Tác dụng |
|---|---|
| `config.yaml` | Cấu hình mặc định: provider, model, input claim set, output JSONL/CSV |
| `.env.example` | Mẫu file `.env`; dùng khi chạy API thật; không chứa API key thật |
| `requirements.txt` | Ghi chú dependency; mock mode dùng standard library |
| `data/source/fact_checking_normalized.jsonl` | Dataset normalized nguồn để tạo claim set |
| `data/claim_sets/claim_set_30.jsonl` | Claim set chung 30 mẫu để baseline và RAG chạy cùng dữ liệu |
| `source_materials/2025.acl-long.17.pdf` | PDF bài báo FACT-AUDIT |
| `source_materials/fact_audit_task_assignment_tracker.xlsx` | Excel phân công công việc |
| `fact_audit_baseline/config.py` | Đọc `.env` và config YAML tối giản |
| `fact_audit_baseline/io_utils.py` | Đọc/ghi JSONL và CSV |
| `fact_audit_baseline/prompting.py` | Tạo prompt theo format FACT-AUDIT-style |
| `fact_audit_baseline/llm_client.py` | LLM client linh hoạt: `mock`, `gemini`, `openai`, `transformers` |
| `fact_audit_baseline/evaluator.py` | Parse response và chấm điểm baseline đơn giản |
| `scripts/make_claim_set.py` | Tạo claim set 30 mẫu từ dataset local |
| `scripts/run_smoke_test.py` | Chạy end-to-end 3 claims để kiểm tra pipeline |
| `scripts/run_baseline.py` | Chạy baseline chính và xuất JSONL/CSV |
| `scripts/run_baseline_demo.py` | Script demo ổn định, hỗ trợ `--use-cache` |
| `notebooks/run_baseline_pipeline.ipynb` | Notebook gom các script để chạy lại pipeline trong một chỗ |
| `schemas/schema_baseline.json` | Contract output baseline cho nhóm RAG |
| `schemas/schema_rag.json` | Contract output phía FACT-AUDIT+RAG |
| `outputs/smoke_test.jsonl` | Kết quả smoke test 3 claims |
| `outputs/smoke_test_scores.csv` | Bảng điểm smoke test |
| `outputs/baseline_results.jsonl` | Kết quả baseline 30 claims |
| `outputs/scores.csv` | Bảng score baseline có các cột yêu cầu trong Excel |
| `outputs/cached_demo/` | Output demo cache để trình bày khi API/GPU lỗi |
| `docs/checklist_mr_to_code_reproduction.md` | Checklist C2.1-C2.8 và đối chiếu cột Notes |
| `docs/environment_notes.md` | Ghi chú môi trường chạy, Python version, official repo |
| `docs/mr_to_task_mapping.md` | Mapping task Excel sang file/output trong repo |

## Chạy Nhanh

Chạy từ root repo:

```bash
cd fact_audit_reproduction
python3 scripts/make_claim_set.py --size 30
python3 scripts/run_smoke_test.py
python3 scripts/run_baseline.py
python3 scripts/run_baseline_demo.py --use-cache
```

Output kỳ vọng:

```text
data/claim_sets/claim_set_30.jsonl
outputs/smoke_test.jsonl
outputs/smoke_test_scores.csv
outputs/baseline_results.jsonl
outputs/scores.csv
outputs/cached_demo/baseline_demo_results.jsonl
outputs/cached_demo/demo_scores.csv
```

## Chạy Với API Thật

Tạo file `.env` từ mẫu:

```bash
cp .env.example .env
```

### Dùng Gemini

Điền vào `.env`:

```bash
GEMINI_API_KEY=your_real_key
GEMINI_MODEL=gemini-2.5-flash
```

Đổi `config.yaml`:

```yaml
llm:
  provider: gemini
  model: gemini-2.5-flash
```

Chạy:

```bash
python3 scripts/run_baseline.py --provider gemini --model gemini-2.5-flash
```

Nếu bạn làm nhánh RAG với Gemini thì process tiếp theo là:

1. Retriever lấy top-k evidence cho từng `claim_id`.
2. Prompt RAG ghép `claim + retrieved_evidence`.
3. Gọi Gemini để sinh `rag_verdict` và `rag_justification`.
4. Xuất file đúng `schemas/schema_rag.json`.
5. Dùng cùng `data/claim_sets/claim_set_30.jsonl` để so sánh công bằng với baseline.

### Dùng OpenAI-compatible

Điền API key vào `.env`, sau đó đổi `config.yaml`:

```yaml
llm:
  provider: openai
  model: gpt-4o-mini
```

Chạy:

```bash
python3 scripts/run_baseline.py --provider openai --model gpt-4o-mini
```

Không commit `.env`.

## Schema Dùng Chung Với Nhóm RAG

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

## Ghi Chú Dọn Repo

Repo hiện chỉ giữ phần đang dùng cho baseline hiện tại và tài liệu tham chiếu tối thiểu.
