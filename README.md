# T2040 LLM Application Workspace

Repo hiện tại phục vụ đề tài:

```text
FACT-AUDIT + FACT-AUDIT+RAG: Evidence-Augmented Adaptive Fact-Checking Audit
```

## Trạng Thái Repo

Repo hiện chỉ giữ phần đang dùng cho project hiện tại:

- code baseline trong `fact_audit_reproduction/`;
- repo official FACT-AUDIT trong `external/FACT-AUDIT/`;
- dataset normalized nguồn để tạo claim set;
- 2 file tài liệu tham chiếu: paper PDF và Excel phân công.

## Cấu Trúc Chính

| Đường dẫn | Tác dụng |
|---|---|
| `fact_audit_reproduction/` | Phần code chính của Mr. Tô: baseline reproduction, smoke test, demo cache, schema cho nhóm RAG |
| `external/FACT-AUDIT/` | Repo FACT-AUDIT official clone, giữ làm reference source gốc |

## File Quan Trọng

| File | Tác dụng |
|---|---|
| `fact_audit_reproduction/README.md` | Hướng dẫn setup, chạy baseline, chạy cached demo |
| `fact_audit_reproduction/config.yaml` | Cấu hình provider/model/input/output mặc định |
| `fact_audit_reproduction/.env.example` | Mẫu file môi trường, không chứa API key thật |
| `fact_audit_reproduction/data/source/fact_checking_normalized.jsonl` | Dataset normalized nguồn để tạo claim set |
| `fact_audit_reproduction/source_materials/` | Chỉ còn paper PDF và Excel phân công đang dùng |
| `fact_audit_reproduction/scripts/make_claim_set.py` | Tạo claim set 30 mẫu từ dataset local |
| `fact_audit_reproduction/scripts/run_smoke_test.py` | Chạy smoke test 3 claims |
| `fact_audit_reproduction/scripts/run_baseline.py` | Chạy baseline FACT-AUDIT-style trên claim set |
| `fact_audit_reproduction/scripts/run_baseline_demo.py` | Chạy demo baseline, có chế độ dùng cache |
| `fact_audit_reproduction/schemas/schema_baseline.json` | Schema output baseline cho Cu Ấn/RAG dùng chung |
| `fact_audit_reproduction/schemas/schema_rag.json` | Schema output phía FACT-AUDIT+RAG |
| `fact_audit_reproduction/docs/checklist_mr_to_code_reproduction.md` | Checklist hoàn thành C2.1-C2.8 và coverage cột Notes |

## Chạy Nhanh

```bash
cd fact_audit_reproduction
python3 scripts/make_claim_set.py --size 30
python3 scripts/run_smoke_test.py
python3 scripts/run_baseline.py
python3 scripts/run_baseline_demo.py --use-cache
```

Mặc định dùng provider `mock`, chạy offline, không cần API key.
# IT2040-LLM-Application
