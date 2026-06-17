# Ghi Chú Môi Trường

Task liên quan: `C2.1 - Clone repo FACT-AUDIT và tạo môi trường chạy`

## Python

Python local đã kiểm tra:

```text
Python 3.11.9
```

Runner trong `fact_audit_reproduction/` ở mode mặc định `mock` chỉ dùng Python standard library, nên smoke test không cần:

- GPU;
- API key;
- dependency nặng như `torch` hoặc `transformers`.

## Official FACT-AUDIT Source

Repo official đã clone tại:

```text
external/FACT-AUDIT/
```

Ghi nhận khi đọc source official:

- `scripts/fact-audit.py` của repo gốc có hardcoded API/model settings.
- Full run kỳ vọng local model/dependency nặng.
- Vì mục tiêu môn học là demo baseline + RAG comparison, repo này giữ official source làm reference và dùng `fact_audit_reproduction/` làm lớp runner sạch, dễ chạy.

## API Key Cho RAG

Nếu bạn muốn nhánh RAG dùng Gemini:

- tạo key trong Google AI Studio;
- đặt key vào `.env` dưới biến `GEMINI_API_KEY`;
- dùng model như `gemini-2.5-flash`;
- ở tầng RAG, retriever lấy evidence trước, rồi mới gọi model với prompt đã ghép evidence.

Repo hiện đã hỗ trợ provider `gemini` trong baseline client để bạn tái dùng cùng cách cấu hình.

## Trạng Thái Smoke Test

Lệnh:

```bash
cd fact_audit_reproduction
python3 scripts/run_smoke_test.py
```

Trạng thái hiện tại:

```text
Chạy end-to-end và ghi outputs/smoke_test.jsonl
```

Nếu lỗi xảy ra, command sẽ trả non-zero exit code và in log ra terminal.
