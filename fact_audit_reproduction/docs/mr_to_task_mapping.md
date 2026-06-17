# Mapping Task - Mr. Tô Code/Reproduction

Nguồn phân công: `fact_audit_reproduction/source_materials/fact_audit_task_assignment_tracker.xlsx`, sheet `PhanCong`.

## Mapping Nhanh

| ID | Task trong Excel | Trạng thái | File/output chính |
|---|---|---|---|
| C2.1 | Clone repo FACT-AUDIT và tạo môi trường chạy | Xong | `external/FACT-AUDIT/`, `fact_audit_reproduction/requirements.txt` |
| C2.2 | Tách API key/model path ra config | Xong | `fact_audit_reproduction/config.yaml`, `.env.example` |
| C2.3 | Smoke test 1-3 claims | Xong | `scripts/run_smoke_test.py`, `outputs/smoke_test.jsonl` |
| C2.3b | Schema output baseline cho Cu Ấn | Xong | `schemas/schema_baseline.json`, `schemas/schema_rag.json` |
| C2.4 | Baseline mini 10-30 claims | Xong | `scripts/run_baseline.py`, `outputs/baseline_results.jsonl` |
| C2.5 | LLM client linh hoạt | Xong | `fact_audit_baseline/llm_client.py` |
| C2.6 | Chuẩn hóa output JSONL/CSV | Xong | `outputs/baseline_results.jsonl`, `outputs/scores.csv` |
| C2.7 | Script demo baseline ổn định | Xong | `scripts/run_baseline_demo.py`, `outputs/cached_demo/` |
| C2.8 | README kỹ thuật | Xong | `README.md` |

Checklist đầy đủ:

```text
docs/checklist_mr_to_code_reproduction.md
```

## Ghi Chú

- Official FACT-AUDIT repo có script hardcode API/model, nên bản này giữ official repo làm reference và tự viết runner sạch hơn cho demo.
- Provider mặc định là `mock`, chạy offline và deterministic.
- Khi có API key hoặc local model, có thể đổi sang provider `openai` hoặc `transformers`.
