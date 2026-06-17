# Checklist - Mr. Tô Code/Reproduction

Nguồn phân công: `fact_audit_reproduction/source_materials/fact_audit_task_assignment_tracker.xlsx`

Owner trong Excel: `Mr. Tô - Code/Reproduction`

## Kết Luận Nhanh

Các task C2.1 đến C2.8 đã hoàn thành ở mức **baseline/demo reproduction**.

Điểm cần hiểu đúng:

- Runner mặc định dùng provider `mock` để chạy offline, ổn định khi demo.
- Nếu muốn chất lượng fact-checking tốt hơn, đổi sang provider `openai` hoặc `transformers`.
- Đây không phải bản tái hiện đầy đủ toàn bộ adaptive multi-agent FACT-AUDIT trong paper.

## Checklist Theo Task

| ID | Việc cần làm | Trạng thái | File/output chứng minh |
|---|---|---|---|
| C2.1 | Clone repo FACT-AUDIT và tạo môi trường chạy | Xong | `external/FACT-AUDIT/`, `fact_audit_reproduction/README.md`, `requirements.txt` |
| C2.2 | Tách API key/model path ra `.env`/config | Xong | `config.yaml`, `.env.example`; không lưu API key thật |
| C2.3 | Chạy smoke test 1-3 claims | Xong | `outputs/smoke_test.jsonl`, `outputs/smoke_test_scores.csv` |
| C2.3b | Chốt output schema baseline cho Cu Ấn | Xong | `schemas/schema_baseline.json`, `schemas/schema_rag.json` |
| C2.4 | Chạy baseline mini 10-30 claims | Xong | `outputs/baseline_results.jsonl` có 30 dòng |
| C2.5 | Thêm LLM client linh hoạt | Xong | `fact_audit_baseline/llm_client.py` hỗ trợ `mock`, `openai`, `transformers` |
| C2.6 | Chuẩn hóa output baseline JSONL/CSV | Xong | `outputs/baseline_results.jsonl`, `outputs/scores.csv` |
| C2.7 | Tạo script demo baseline ổn định | Xong | `scripts/run_baseline_demo.py`, `outputs/cached_demo/` |
| C2.8 | Viết README kỹ thuật phần baseline | Xong | `fact_audit_reproduction/README.md` |

## Đối Chiếu Cột Notes Trong Excel

| ID | Notes trong Excel | Đã đáp ứng bằng gì |
|---|---|---|
| C2.1 | Ghi rõ Python version và lỗi nếu có | `docs/environment_notes.md`; đã verify với Python 3.11.9; smoke test hiện không lỗi |
| C2.2 | Không commit API key | `.env.example`, `.gitignore`, `config.yaml`; không có key thật trong repo |
| C2.3 | Pipeline chạy end-to-end hoặc log lỗi rõ ràng | `scripts/run_smoke_test.py`; lỗi sẽ làm command fail, thành công thì ghi output smoke test |
| C2.3b | Bắt buộc để Cu Ấn không bị block | `schemas/schema_baseline.json`, `schemas/schema_rag.json`; dùng chung khóa `claim_id` |
| C2.4 | Cùng claim set và target model với RAG | `data/claim_sets/claim_set_30.jsonl`; RAG nên dùng cùng file và cùng model config |
| C2.5 | Hỗ trợ API hoặc local model | `llm_client.py` có `openai`/OpenAI-compatible API và `transformers` local model |
| C2.6 | Cột: claim_id, claim, verdict, justification, score, latency, cost | `outputs/scores.csv` đã có đủ các cột này; JSONL cũng có alias tương ứng |
| C2.7 | Có chế độ dùng cached output | `scripts/run_baseline_demo.py --use-cache` |
| C2.8 | Cách setup, chạy baseline, chạy cached demo | `README.md` đã ghi lệnh setup/chạy/demo cache |

## Lệnh Verify

Chạy từ root repo:

```bash
cd fact_audit_reproduction
python3 scripts/make_claim_set.py --size 30
python3 scripts/run_smoke_test.py
python3 scripts/run_baseline.py
python3 scripts/run_baseline_demo.py --use-cache --limit 5
python3 -m py_compile fact_audit_baseline/*.py scripts/*.py
```

Output đã verify:

| Output | Kỳ vọng | Hiện tại |
|---|---:|---:|
| `outputs/smoke_test.jsonl` | 3 dòng | 3 dòng |
| `outputs/baseline_results.jsonl` | 30 dòng | 30 dòng |
| `outputs/cached_demo/baseline_demo_results.jsonl` | 5 dòng | 5 dòng |

## Phạm Vi Hiện Tại

Đã có cho demo môn học:

- Baseline reproduction runner theo input style của FACT-AUDIT.
- Provider offline deterministic để chạy smoke test và demo ổn định.
- Schema contract cho Cu Ấn tích hợp FACT-AUDIT+RAG.
- Claim set chung để baseline và RAG so sánh công bằng.
- Cached demo phòng trường hợp API/GPU lỗi.

Chưa làm, và không cần làm trong phạm vi hiện tại:

- Full dynamic multi-agent adaptive search của paper.
- Tái lập toàn bộ experiment trên nhiều LLM như bài báo.
- Kỳ vọng provider `mock` cho kết quả fact-checking mạnh như LLM thật.

## Dọn Repo

Đã xóa:

- `real_estate_advisory/`
- notebook/report/chart/script/PPT generator không dùng
- raw dataset và subset không cần cho runner

Đã giữ trong repo hiện tại:

- `data/source/fact_checking_normalized.jsonl`
- `source_materials/`

Repo hiện tự đủ dữ liệu để tạo claim set và đối chiếu tài liệu cần thiết.
