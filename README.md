# T2040 LLM Application Workspace

Repo này tập trung vào phần FACT-AUDIT-inspired reproduction cho đồ án:

- `static baseline`
- `dynamic prototype`
- `FACT-AUDIT + RAG comparison`

## Cấu Trúc Chính

| Đường dẫn | Tác dụng |
|---|---|
| `fact_audit_reproduction/` | Code chính: baseline, dynamic claim generation, notebook, schema, docs |
| `external/FACT-AUDIT/` | Repo FACT-AUDIT official giữ làm tài liệu đối chiếu |

## File Quan Trọng

| File | Tác dụng |
|---|---|
| `fact_audit_reproduction/README.md` | Hướng dẫn setup và chạy pipeline |
| `fact_audit_reproduction/.env.example` | Mẫu biến môi trường cho Gemini/OpenAI |
| `fact_audit_reproduction/config.yaml` | Cấu hình provider, model, input, output mặc định |
| `fact_audit_reproduction/notebooks/run_baseline_pipeline.ipynb` | Notebook chạy lại toàn bộ pipeline |
| `fact_audit_reproduction/scripts/` | Các script tạo claim set, smoke test, baseline, dynamic generation |
| `fact_audit_reproduction/schemas/` | Schema dùng chung cho baseline và nhánh RAG |
| `fact_audit_reproduction/docs/` | Checklist, ghi chú môi trường, report mock test |

## Reports

- [Checklist Mr. To](fact_audit_reproduction/docs/checklist_mr_to_code_reproduction.md)
- [Mock Test Report](fact_audit_reproduction/docs/mock_test_report.md)

## Chạy Nhanh

```bash
cd fact_audit_reproduction
python3 scripts/make_claim_set.py --size 30
python3 scripts/run_smoke_test.py
python3 scripts/run_baseline.py
python3 scripts/run_baseline_demo.py --use-cache
```

Mặc định dùng provider `mock`, chạy offline, không cần API key.
