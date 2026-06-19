# T2040 LLM Application Workspace

Repo nay tap trung vao phan FACT-AUDIT-inspired reproduction cho do an:

- `static baseline`
- `dynamic prototype`
- `FACT-AUDIT + RAG comparison`

## Cau Truc Chinh

| Duong dan | Tac dung |
|---|---|
| `fact_audit_reproduction/` | Code chinh: baseline, dynamic claim generation, notebook, schema, docs |
| `external/FACT-AUDIT/` | Repo FACT-AUDIT official giu lam tai lieu doi chieu |

## File Quan Trong

| File | Tac dung |
|---|---|
| `fact_audit_reproduction/README.md` | Huong dan setup va chay pipeline |
| `fact_audit_reproduction/.env.example` | Mau bien moi truong cho Gemini/OpenAI |
| `fact_audit_reproduction/config.yaml` | Cau hinh provider, model, input, output mac dinh |
| `fact_audit_reproduction/notebooks/run_baseline_pipeline.ipynb` | Notebook chay lai toan bo pipeline |
| `fact_audit_reproduction/scripts/` | Cac script tao claim set, smoke test, baseline, dynamic generation |
| `fact_audit_reproduction/schemas/` | Schema dung chung cho baseline va nhanh RAG |
| `fact_audit_reproduction/docs/` | Checklist, ghi chu moi truong, report mock test |

## Reports

- [Checklist Mr. To](fact_audit_reproduction/docs/checklist_mr_to_code_reproduction.md)
- [Mock Test Report](fact_audit_reproduction/docs/mock_test_report.md)

## Chay Nhanh

```bash
cd fact_audit_reproduction
python3 scripts/make_claim_set.py --size 30
python3 scripts/run_smoke_test.py
python3 scripts/run_baseline.py
python3 scripts/run_baseline_demo.py --use-cache
```

Mac dinh dung provider `mock`, chay offline, khong can API key.
