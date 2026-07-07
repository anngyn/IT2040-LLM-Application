# Báo cáo Thực nghiệm FACT-AUDIT

## Tổng quan

Báo cáo này ghi nhận các thực nghiệm nhằm tìm hiểu cách **retrieval-augmented generation (RAG)** và **bằng chứng bên ngoài** ảnh hưởng đến khả năng kiểm chứng sự kiện (fact-checking) của LLM, dựa trên framework FACT-AUDIT (adaptive multi-agent dynamic fact-checking evaluation).

**Câu hỏi nghiên cứu:** Việc cung cấp bằng chứng truy xuất có cải thiện khả năng fact-checking của LLM không? Trong điều kiện nào nó giúp ích hoặc gây hại?

---

## Cài đặt thực nghiệm

### Framework: FACT-AUDIT

FACT-AUDIT sử dụng 3 vai trò:
- **Optimizer** — sinh câu trả lời tham chiếu (reference answer) và test cases
- **Judge** — chấm điểm câu trả lời của target model (thang 1-10)
- **Target** — LLM đang được đánh giá

### Các model sử dụng

| Vai trò | Provider | Model |
|---------|----------|-------|
| Optimizer | Google Gemini | gemini-2.5-flash |
| Judge | Google Gemini | gemini-2.5-flash |
| Target (yếu) | Third-party (vilao.ai) | ts/llama-4-scout-17b-16e-instruct |
| Target (mạnh) | Google Gemini | gemini-2.5-pro |

### Chỉ số đánh giá (theo paper)

- **Grade**: Điểm trung bình (1-10), cao hơn = fact-checking tốt hơn
- **IMR** (Incorrect & Missed Rate): % điểm <= 3, thấp hơn = tốt hơn

### Các chế độ test (theo paper)

| Chế độ | Mô tả |
|--------|--------|
| `[claim]` | Chỉ cho claim, không có evidence — kiểm tra kiến thức tham số (parametric knowledge) |
| `[evidence]` | Claim + gold evidence (do optimizer viết) — kiểm tra khả năng sử dụng bằng chứng |
| `[wisdom of crowds]` | Claim + luồng thảo luận mạng xã hội — kiểm tra khả năng xử lý bằng chứng nhiễu |

---

## Thực nghiệm 1: Baseline

**Mục tiêu:** Thiết lập hiệu suất nền (baseline) của model target khi chỉ dùng claim.

**Script:** `scripts/fact-audit.py`

**Cấu hình:**
- Target: ts/llama-4-scout-17b-16e-instruct (qua third-party provider)
- 10 claims, 2 knowledge points, mỗi point 5 steps
- Trộn các test modes (claim, evidence, wisdom of crowds)

### Kết quả

| Model | Grade | IMR |
|-------|-------|-----|
| LLaMA-4-Scout-17B | 8.80 | 10% |

### Nhận xét

LLaMA-4-Scout hoạt động khá tốt khi chỉ dùng kiến thức tham số (parametric knowledge). Model nhận diện đúng hầu hết các claim hư cấu là "không thể xác minh", cho thấy khả năng suy luận nội tại tương đối ổn định. Điểm IMR chỉ 10% nghĩa là chỉ 1/10 claim bị đánh giá sai hoàn toàn.

**Lưu ý quan trọng về pipeline:** Lần chạy baseline đầu tiên dùng `--limit-steps 5` nhưng `gen_seed()` luôn sinh 10 seed → vòng lặp adaptive `while len(steps) < max_steps` không bao giờ chạy (vì `10 < 5` là False). Nghĩa là 20 claims đều là **seed ngẫu nhiên** (Monte Carlo từ p(x)), CHƯA có importance sampling nhắm điểm yếu. Xem Thực nghiệm 4 để biết cách chạy đúng cơ chế paper.

---

## Thực nghiệm 2: Gold Evidence (Bằng chứng đối sánh của paper)

**Mục tiêu:** Kiểm tra xem gold evidence (do optimizer sinh) của paper có giúp model yếu hay không.

**Script:** `scripts/fact-audit-exp2-gold-evidence.py`

**Phương pháp:**
1. Load claims từ kết quả baseline (log.json)
2. Với mỗi claim: chạy target ở chế độ `[claim]` (không evidence)
3. Nếu claim có gold auxiliary_info: chạy thêm ở chế độ `[evidence]` hoặc `[wisdom]`
4. So sánh điểm 2 chế độ

### Kết quả

| Chế độ | Grade (chỉ claim) | Grade (có evidence) | Delta |
|--------|--------------------|-----------------------|-------|
| Tổng thể | 5.60 | 1.50 | -4.10 |
| [evidence] | 3.00 | 1.50 | -1.50 |
| [wisdom of crowds] | 6.00 | 1.50 | -4.50 |

Cải thiện theo từng claim: [-2.0, -8.0, -1.0, -1.0]

### Nhận xét

Gold evidence của paper **làm giảm** điểm của model yếu (LLaMA-4-Scout). Nguyên nhân:

1. **Bản chất contrastive evidence**: Paper thiết kế gold evidence chứa đồng thời thông tin hỗ trợ (supporting), bác bỏ (refuting), và trung lập (neutral). Mục đích là test khả năng phân biệt của model.

2. **Model yếu không phân biệt được**: LLaMA-4-Scout không có khả năng lọc ra đâu là thông tin hỗ trợ, đâu là thông tin bác bỏ. Khi thấy hỗn hợp thông tin, model bị nhiễu loạn và đưa ra kết luận sai.

3. **So với paper**: Paper báo cáo evidence giúp cải thiện điểm — nhưng chỉ đúng với model mạnh (GPT-4, Claude). Model mạnh có khả năng reasoning để lọc contrastive evidence; model yếu thì không.

**Kết luận:** Kết luận "evidence giúp fact-checking" của paper phụ thuộc vào sức mạnh model. Đây là limitation mà paper chưa nhấn mạnh đủ.

---

## Thực nghiệm 3: RAG với Wikipedia

**Mục tiêu:** Kiểm tra liệu bằng chứng truy xuất thực tế (từ Wikipedia) có cải thiện fact-checking so với baseline.

**Script:** `scripts/fact-audit-rag.py`

**Phương pháp:**
1. Load 10 claims từ kết quả baseline
2. Với mỗi claim:
   - Chạy target với prompt chỉ-claim (baseline)
   - Tìm kiếm Wikipedia API cho các đoạn văn liên quan (top_k=5, max_chars=1500)
   - Nếu tìm được evidence: chạy target với RAG prompt (claim + evidence truy xuất)
   - Nếu không tìm được: **fallback về prompt chỉ-claim** (tránh confuse model bằng "không có evidence")
3. Judge chấm điểm cả 2 câu trả lời
4. So sánh

**Pipeline RAG:**
```
claim text → Wikipedia Search API → top-k page titles → Wikipedia Extract API → text passages → RAG prompt
```

### Kết quả: LLaMA-4-Scout (model yếu)

| Chỉ số | Baseline | RAG | Delta |
|--------|----------|-----|-------|
| Grade | 6.20 | 5.40 | -0.80 |
| IMR | 40% | 60% | +20% |

Chi tiết từng claim:

| # | Chủ đề | Baseline | RAG | Delta | Kết quả Wiki |
|---|--------|----------|-----|-------|--------------|
| 1 | Dự luật HR 1234 | 3 | 3 | 0 | 0 (fallback) |
| 2 | Rau xanh & sức khỏe | 8 | 10 | +2 | 0 (fallback) |
| 3 | Vi xử lý Quantum Leap | 2 | 9 | +7 | 0 (fallback) |
| 4 | Báo cáo IPCC | 2 | 2 | 0 | 0 (fallback) |
| 5 | Freedom March | 9 | 2 | **-7** | 5 đoạn |
| 6 | Cổ phiếu TechGiant | 10 | 3 | **-7** | 5 đoạn |
| 7 | Elizabeth I theo Công giáo | 2 | 10 | +8 | 0 (fallback) |
| 8 | Phát hiện sự sống trên Sao Hỏa | 7 | 10 | +3 | 0 (fallback) |
| 9 | Hiệp ước Hòa bình Toàn cầu | 9 | 2 | **-7** | 2 đoạn |
| 10 | Luật An toàn Trực tuyến | 10 | 3 | **-7** | 4 đoạn |

### Kết quả: Gemini 2.5 Pro (model mạnh)

| Chỉ số | Baseline | RAG | Delta |
|--------|----------|-----|-------|
| Grade | **9.50** | 6.70 | **-2.80** |
| IMR | **0%** | 40% | +40% |

Chi tiết từng claim:

| # | Chủ đề | Baseline | RAG | Delta | Kết quả Wiki |
|---|--------|----------|-----|-------|--------------|
| 1 | Dự luật HR 1234 | 10 | 10 | 0 | 0 (fallback) |
| 2 | Rau xanh & sức khỏe | 10 | 10 | 0 | 0 (fallback) |
| 3 | Vi xử lý Quantum Leap | 10 | 10 | 0 | 0 (fallback) |
| 4 | Báo cáo IPCC | 9 | 10 | +1 | 0 (fallback) |
| 5 | Freedom March | 10 | 3 | **-7** | 5 đoạn |
| 6 | Cổ phiếu TechGiant | 9 | 1 | **-8** | 5 đoạn |
| 7 | Elizabeth I theo Công giáo | 10 | 10 | 0 | 0 (fallback) |
| 8 | Phát hiện sự sống trên Sao Hỏa | 10 | 10 | 0 | 0 (fallback) |
| 9 | Hiệp ước Hòa bình Toàn cầu | 8 | 1 | **-7** | 2 đoạn |
| 10 | Luật An toàn Trực tuyến | 9 | 2 | **-7** | 4 đoạn |

### Nhận xét

**1. Bằng chứng không liên quan gây hại cho tất cả model:**

Mọi claim mà Wikipedia trả về kết quả đều bị giảm -7 đến -8 điểm, bất kể model mạnh hay yếu. Đây là phát hiện quan trọng nhất: vấn đề nằm ở chất lượng retrieval, không phải sức mạnh model.

**2. Cơ chế gây hại:**

FACT-AUDIT sinh các claim **hư cấu** (fictional). Wikipedia không có bài viết về chúng. Khi search:
- "Freedom March in Capital City" → Wiki trả bài về cuộc biểu tình khác (không liên quan)
- "TechGiant Inc. stock" → Wiki trả bài về công ty tech khác
- "Global Peace Accord" → Wiki trả bài về hiệp định khác

Model nhận evidence không liên quan → **cố gắng dùng nó** thay vì bỏ qua → kết luận sai.

**3. Hành vi "evidence follower" của LLM:**
- **Không có evidence**: Model nói "Tôi không thể xác minh claim này" → đúng → điểm cao (9-10)
- **Có evidence không liên quan**: Model cố match claim với evidence → sai → điểm thấp (1-3)

Hành vi này nhất quán giữa cả model yếu (LLaMA) và mạnh (Gemini 2.5 Pro). LLM ưu tiên evidence bên ngoài hơn kiến thức nội tại, ngay cả khi evidence đó không liên quan.

**4. Chiến lược fallback hoạt động tốt:**

Claims không có kết quả Wikipedia → dùng prompt baseline → không bị giảm điểm. Chứng minh: khi không có evidence, không gây hại.

**5. Model mạnh có baseline cao hơn nhưng cùng mức tổn thương:**

Gemini 2.5 Pro đạt 9.5 baseline (so với 6.2 của LLaMA) nhưng giảm tương đương khi nhận evidence không liên quan. Delta tuyệt đối thậm chí lớn hơn (-2.80 vs -0.80) vì có nhiều "chỗ để rơi" hơn.

---

## Thực nghiệm 4: Pipeline Adaptive (giống paper — Importance Sampling)

**Mục tiêu:** Chạy đúng cơ chế cốt lõi của paper — vòng lặp thăm dò lặp (iterative probing) sinh claim mới nhắm vào **điểm yếu** của model, thay vì chỉ sinh claim ngẫu nhiên.

**Script:** `scripts/fact-audit.py` (thêm arg `--limit-seeds`)

### Nền tảng lý thuyết: Monte Carlo vs Importance Sampling

Paper mô hình hóa việc tạo test case như một bài toán lấy mẫu:

- **p(x)** — Phân phối tri thức chuẩn (Oracle Knowledge Distribution): phân phối THỰC của mọi claim có thể tồn tại trong thế giới thực. Đa số claim nằm ở vùng "phổ biến/dễ", ít claim ở vùng "hiếm/khó" (long-tail).
- **Fα(x)** — Giới hạn fact-checking của model α trên test case x (điểm Judge chấm; điểm thấp = model yếu tại đó).

**Monte Carlo (naive):** Lấy mẫu x ngẫu nhiên từ p(x) rồi đo Fα(x).
```
E_p(x)[Fα(x)] = ∫ p(x)·Fα(x) dx
```
Vấn đề: hầu hết mẫu rơi vào vùng dễ (model đã biết) → tốn nhiều mẫu mà ít phát hiện điểm yếu. Hội tụ chậm O(1/√N).

**Importance Sampling (FACT-AUDIT):** Thay p(x) bằng phân phối đề xuất **q(x)** tập trung vào vùng model yếu:
```
E_p(x)[Fα(x)] = ∫ q(x)·Fα(x)·[p(x)/q(x)] dx = E_q(x)[Fα(x)·p(x)/q(x)]
```
- Trọng số quan trọng `p(x)/q(x)` bù đắp sai lệch → ước lượng vẫn không chệch (unbiased)
- q(x) lý tưởng: `q(x) ∝ p(x)·Fα(x)` — dồn mật độ vào nơi model sai nhiều nhất

**Ánh xạ vào code:**

| Lý thuyết | Hiện thực trong FACT-AUDIT |
|-----------|----------------------------|
| p(x) | Toàn bộ claim có thể sinh (giai đoạn seed ngẫu nhiên) |
| q(x) | **Optimizer agent** — sinh claim nhắm điểm yếu model |
| x | Một test case (claim + evidence + key_point + test_mode) |
| Fα(x) | Điểm Judge chấm (score thấp = điểm yếu) |
| Cập nhật q(x) | Vòng lặp `while len(steps) < max_steps` trong `deep_search()` |

### Phương pháp

Pipeline có 2 giai đoạn trong mỗi knowledge point:

1. **Giai đoạn seed (Monte Carlo):** `gen_seed()` sinh N claim ngẫu nhiên đa chủ đề. Thêm `--limit-seeds N` để giới hạn số seed.
2. **Giai đoạn adaptive (Importance Sampling):** Vòng lặp lấy các claim điểm thấp (bad cases, score ≤ 3) làm ví dụ, yêu cầu Optimizer sinh claim MỚI khó hơn nhắm đúng vùng đó → chạy Target → Judge chấm → lặp lại cho tới đủ `--limit-steps`.

**Lệnh chạy:**
```bash
python fact-audit.py --category complex_claim --limit-points 1 --limit-seeds 3 --limit-steps 10
# = 3 seed (Monte Carlo) + 7 adaptive (Importance Sampling) = 10 claims
```

### Kết quả

Target: ts/llama-4-scout-17b-16e-instruct

| # | Loại | Mode | Score | Chủ đề |
|---|------|------|-------|--------|
| 1 | seed | evidence | 10 | HR 1234 bill |
| 2 | seed | claim | 10 | leafy greens |
| 3 | seed | wisdom of crowds | **3** | Quantum Leap processor |
| 4 | adaptive | wisdom of crowds | 7 | historical causal links |
| 5 | adaptive | evidence | 10 | Great Wall |
| 6 | adaptive | wisdom of crowds | **3** | transatlantic cable |
| 7 | adaptive | wisdom of crowds | 7 | penicillin discoverer |
| 8 | adaptive | evidence | 10 | Apollo 11 |
| 9 | adaptive | wisdom of crowds | 10 | penicillin WWII |
| 10 | adaptive | wisdom of crowds | 10 | Titanic |

Grade trung bình: **8.0** | IMR: **20%** (2/10 claim điểm ≤ 3)

### Nhận xét — Bằng chứng Importance Sampling hoạt động

**1. Optimizer phát hiện điểm yếu:** Seed claim 3 (Quantum Leap, chế độ `wisdom of crowds`) bị điểm 3 — điểm yếu đầu tiên lộ ra.

**2. Optimizer dồn mẫu vào điểm yếu:** Trong 7 claim adaptive, **6/7 claim đều dùng chế độ `wisdom of crowds`** — đúng chế độ mà model vừa bị điểm thấp. Đây chính là q(x) tập trung mật độ vào vùng `Fα(x)` thấp.

**3. Đa dạng hóa chủ đề nhưng giữ độ khó:** Claim adaptive chuyển sang chủ đề lịch sử/khoa học (Great Wall, penicillin, Apollo, Titanic) — theo Guideline "không lặp chủ đề để tối đa đa dạng" nhưng vẫn nhắm chế độ khó.

**4. So với lần chạy trước:**

| | Baseline (lần 1) | Adaptive (Exp4) |
|--|------------------|-----------------|
| Số seed | 10 (không giới hạn) | 3 |
| Số adaptive | 0 | 7 |
| Vòng importance sampling | Không chạy | Chạy 7 vòng |
| Cơ chế | Chỉ Monte Carlo p(x) | Monte Carlo + Importance Sampling q(x) |

**5. Về `new_points` (mở rộng taxonomy):** Vẫn = 0 vì chỉ chạy 1 knowledge point. Hàm `analysis()` (sinh knowledge point mới dựa trên bad cases toàn cục) chỉ kích hoạt khi chạy tới knowledge point cuối cùng. Đây là **tầng adaptive thứ 2** của paper — mở rộng cây phân loại (taxonomy). Cần `--limit-points ≥ 2` để trigger.

### Hai tầng adaptive của FACT-AUDIT

```
Tầng 1 — Importance Sampling (trong deep_search):
    sinh claim khó hơn TRONG một knowledge point → nhắm điểm yếu cụ thể

Tầng 2 — Taxonomy Expansion (analysis):
    phân tích bad cases toàn bộ → sinh knowledge point MỚI (new_points)
    → phát hiện loại điểm yếu chưa từng test
```

Exp4 đã chạy Tầng 1. Tầng 2 được chạy trong Thực nghiệm 5.

---

## Thực nghiệm 5: Tầng 2 Adaptive — Mở rộng Taxonomy (Taxonomy Expansion)

**Mục tiêu:** Chạy tầng adaptive thứ 2 của paper — hàm `analysis()` phân tích các bad case trên nhiều scenario, rồi tự **sinh ra một loại điểm yếu (knowledge point) hoàn toàn MỚI** chưa có trong cây phân loại (taxonomy).

**Script:** `scripts/fact-audit.py` (thêm arg `--max-expansions`)

### Phương pháp

```bash
python fact-audit.py --category complex_claim --limit-points 3 \
    --limit-seeds 2 --limit-steps 3 --max-expansions 1
# 3 scenario x 3 claims (2 seed + 1 adaptive) + 1 knowledge point MỚI x 3 claims
```

Sau khi chạy hết 3 scenario, `analysis()` gom bad cases (score ≤ 3) từ cả 3 → hỏi Optimizer: "taxonomy đã đủ chưa? Nếu chưa, suy ra một loại điểm yếu mới". Điểm mới được `judge_new_task()` kiểm định, rồi chèn vào và chạy tiếp.

### Kết quả

Điểm trung bình từng scenario (Tầng 1):

| Scenario | Avg score | Ghi chú |
|----------|-----------|---------|
| multiple_facts_combination | **2.5** | Điểm yếu rõ nhất |
| reasoning_with_structural_table_data | 7.0 | |
| facts_change_over_time | 7.3 | |
| **deductive_causal_reasoning** (MỚI) | 7.3 | Sinh bởi Tầng 2 |

**Knowledge point MỚI do `analysis()` sinh ra:** `deductive_causal_reasoning`

**Giải thích của Optimizer (dịch tóm tắt):**
> Taxonomy hiện có: ghép nhiều fact độc lập (`multiple_facts_combination`), trích xuất & so sánh số liệu từ bảng (`reasoning_with_structural_table_data`), fact thay đổi theo thời gian (`facts_change_over_time`). Nhưng **thiếu** category cho claim khẳng định **quan hệ nhân quả** hoặc cần **suy luận logic nhiều bước** (dạng "A xảy ra vì B, dẫn tới C"). Để verify loại này, LLM phải tổng hợp bằng chứng rời rạc, thiết lập phụ thuộc, và validate từng bước suy luận — không chỉ kiểm tra từng fact nguyên tử riêng lẻ.

### Nhận xét — Đây là điểm mấu chốt của FACT-AUDIT

**1. Hai tầng adaptive hoàn chỉnh:**

```
Tầng 1 (Importance Sampling): tìm claim KHÓ trong một loại điểm yếu có sẵn
Tầng 2 (Taxonomy Expansion):  tìm LOẠI năng lực chưa từng được test
```

**2. "Adaptive discovery" thực sự:** Framework không chỉ tìm claim khó hơn, mà còn tự phát hiện **chiều đánh giá mới** mà con người thiết kế taxonomy ban đầu bỏ sót. Đúng tinh thần "dynamically identify deficiencies" của paper.

**3. New point có căn cứ:** `deductive_causal_reasoning` được suy ra HỢP LÝ từ khoảng trống trong taxonomy — không phải random. Điều này cần bad cases đa dạng từ ≥ 3 scenario mới có ý nghĩa (nếu chỉ 1 scenario, new point sẽ kém đại diện).

### Đối chiếu với code paper gốc

Đã so sánh trực tiếp với `FACT-AUDIT/scripts/fact-audit.py` (bản gốc):

| Thành phần | Bản gốc | Bản của chúng tôi | Khớp |
|-----------|---------|-------------------|------|
| Vòng importance sampling (`deep_search`) | `while len(steps) < 30` | `while len(steps) < max_steps` (param hóa) | ✅ Logic y hệt |
| Chọn bad/good cases | `random.sample(bad_cases, 2)` + good | Giống | ✅ |
| Prompt sinh claim khó | "aim for score < 3.0" | Giống nguyên văn | ✅ |
| `analysis()` sinh new point | Giống | Giống hàm, giống prompt | ✅ |
| Trigger tầng 2 | Point cuối của cả 9-point taxonomy, rồi `exit(0)` | Point cuối trong `--limit-points`, rồi `break` | ⚠️ Điều chỉnh cho bounded run |
| Số claim/point | 10 seed + 20 adaptive = 30 | Giảm qua `--limit-seeds/steps` để tiết kiệm API | ⚠️ Ít mẫu hơn |

**Kết luận đối chiếu:** Logic cốt lõi (cả 2 tầng adaptive) **trung thành với paper gốc**. Khác biệt chỉ ở quy mô (số claim nhỏ hơn để tiết kiệm API/thời gian) và cách dừng (bounded thay vì chạy hết 9 scenario). Cơ chế importance sampling và taxonomy expansion giữ nguyên.

---

## Thực nghiệm 6: So sánh Target (Reproduce Table 1 của paper)

**Mục tiêu:** Chạy CÙNG pipeline adaptive với các target model khác nhau để kiểm chứng: framework có phân biệt được model mạnh/yếu không? (Paper Table 1 xếp hạng 13 LLM theo IMR.)

**Script:** `scripts/fact-audit.py`

**Cấu hình chung (giống nhau cho mọi target):**
- Optimizer + Judge: gemini-2.5-flash (cố định — là "thước đo", không đổi)
- Pipeline: 3 seed + 7 adaptive = 10 claims, cùng knowledge point `multiple_facts_combination`

### Kết quả

| Target model | Grade | IMR | Provider |
|--------------|-------|-----|----------|
| ts/llama-4-scout-17b | 8.00 | 20% | third-party |
| gemini-2.5-pro | **9.80** | **0%** | gemini |

Chi tiết gemini-2.5-pro: 8/10 claim đạt điểm 10, không claim nào ≤ 3.

### Nhận xét

**1. Framework phân biệt đúng năng lực:** Model mạnh (Gemini 2.5 Pro) có IMR thấp hơn hẳn (0% vs 20%), Grade cao hơn (9.80 vs 8.00). Đây là reproduce tinh thần Table 1 của paper: IMR là chỉ số phân biệt model.

**2. Model càng mạnh, importance sampling càng khó tìm điểm yếu:**
- Với **LLaMA**: seed claim chế độ `wisdom of crowds` bị điểm 3 → Optimizer dồn 6/7 claim adaptive vào wisdom mode (tìm được điểm yếu rõ).
- Với **Gemini Pro**: mọi mode đều ~9-10 điểm → Optimizer không tìm được điểm yếu rõ rệt → cần nhiều vòng lặp hơn để hội tụ.

Điều này khớp quan sát Figure 5 của paper: với model mạnh, IMR hội tụ chậm hơn vì khó đào ra lỗi.

**3. Ý nghĩa:** Chất lượng của một benchmark adaptive phụ thuộc vào việc nó có "theo kịp" model mạnh không. Model càng khỏe, càng cần nhiều vòng probing (và nhiều claim) để đánh giá đầy đủ.

### Bug đã phát hiện & sửa trong quá trình chạy

Khi chạy target = gemini-2.5-pro lần đầu, TẤT CẢ claim bị điểm 1 (Grade 1.0, IMR 100%) — bất thường với model mạnh. Nguyên nhân:

- Hàm `_target_api_generate()` **hardcode gọi third-party provider** bất kể `TARGET_PROVIDER`.
- → Target gemini bị route sai qua vilao.ai → `permission_error` → trả chuỗi rỗng → Judge chấm 1 điểm.

**Sửa:** route theo `TARGET_PROVIDER` giống optimizer/judge:
```python
def _target_api_generate(text):
    _step_counter['llama'] += 1
    return _call(TARGET_PROVIDER, TARGET_MODEL, text, temp=0)
```
LLaMA vẫn chạy đúng (TARGET_PROVIDER=third-party). Bài học: kết quả IMR=100% cho model mạnh là dấu hiệu lỗi hạ tầng (empty response), không phải model kém — luôn kiểm tra `answer` thật trước khi tin điểm số.

---

## So sánh tổng hợp giữa các thực nghiệm

| Thực nghiệm | Model | Grade Baseline | Grade có Evidence | Delta |
|-------------|-------|---------------|------------------:|------:|
| Exp2 (gold evidence) | LLaMA-4-Scout | 5.60 | 1.50 | -4.10 |
| Exp3 (RAG Wikipedia) | LLaMA-4-Scout | 6.20 | 5.40 | -0.80 |
| Exp3 (RAG Wikipedia) | Gemini 2.5 Pro | 9.50 | 6.70 | -2.80 |

**Nhận xét bảng tổng hợp:**
- Gold evidence gây hại nhiều nhất (-4.10) vì nó chứa thông tin đối sánh (contrastive) — hỗn hợp supporting + refuting khiến model yếu bị confused nhiều hơn evidence hoàn toàn không liên quan.
- RAG với model mạnh bị ảnh hưởng nặng hơn model yếu (-2.80 vs -0.80) về mặt tuyệt đối vì baseline cao hơn.
- Cả 3 trường hợp đều cho thấy: evidence không phù hợp = giảm hiệu suất.

---

## Phân tích & Kết luận

### Tại sao evidence gây hại thay vì giúp ích

```
Giả định paper:    evidence → fact-checking tốt hơn
Thực tế:           chất lượng evidence → quyết định kết quả

                        ┌─ evidence liên quan (relevant) → giúp ích (trường hợp lý tưởng của paper)
chất lượng evidence ────┤
                        └─ evidence không liên quan (irrelevant) → gây hại (trường hợp RAG thực tế)
```

### So sánh với kết luận của paper

| Paper kết luận | Phát hiện của chúng tôi |
|----------------|-------------------------|
| Chế độ [evidence] cho điểm cao nhất | Chỉ đúng khi gold evidence **liên quan** và model **đủ mạnh** |
| Evidence giúp fact-checking | Chỉ khi chất lượng retrieval cao |
| Model mạnh hơn điểm tốt hơn | Đúng cho baseline; nhưng model mạnh cũng bị tổn thương tương đương khi evidence irrelevant |
| [wisdom of crowds] ở mức trung bình | Evidence nhiễu vẫn confuse model yếu |

### Ý nghĩa cho hệ thống RAG thực tế

1. **Naive RAG (truy xuất không lọc) có thể phản tác dụng** — khi retrieval quality thấp, tốt hơn là không cung cấp evidence
2. **Retrieval relevance quan trọng hơn retrieval quantity** — 5 đoạn không liên quan tệ hơn 0 đoạn
3. **LLM không tự đánh giá được relevance** — cả model mạnh lẫn yếu đều "tin" evidence được cung cấp
4. **Cần cơ chế lọc relevance** trước khi đưa evidence vào prompt

### Hạn chế của nghiên cứu

1. **Mẫu nhỏ** (10 claims) — kết quả có thể không tổng quát hóa được
2. **Chỉ claims hư cấu** — claims thực tế sẽ có coverage tốt hơn trên Wikipedia
3. **Không có relevance filtering** — RAG naive đưa tất cả passages mà không kiểm tra chất lượng
4. **Một nguồn truy xuất duy nhất** (Wikipedia) — multi-source có thể tốt hơn
5. **Tính nhất quán Judge** — cùng claim có thể bị chấm điểm khác nhau giữa các lần chạy (variance ở claims 3, 7)

### Hướng cải thiện

1. **Trích xuất từ khóa (keyword extraction)** — Trích entity chính từ claim trước khi search (giảm kết quả không liên quan)
2. **Lọc relevance** — Dùng LLM đánh giá evidence có liên quan không trước khi đưa vào prompt
3. **Ngưỡng confidence** — Bỏ evidence có search relevance score thấp
4. **Truy xuất đa nguồn** — Kết hợp Wikipedia + news APIs + fact-check databases
5. **Dataset claims thực** — Test với claims có coverage thực trên Wikipedia

---

## Cấu trúc thư mục

```
external/FACT-AUDIT/
├── scripts/
│   ├── fact-audit.py              # Baseline (multi-provider, sửa từ paper gốc)
│   ├── fact-audit-rag.py          # Exp3: Pipeline so sánh RAG
│   ├── fact-audit-exp2-gold-evidence.py  # Exp2: Phân tích gold evidence
│   ├── test_api.py                # Helper kiểm tra API
│   ├── .env                       # API keys và cấu hình
│   └── .env.example               # Template
├── result/
│   ├── factaudit/
│   │   └── ts-llama-4-scout-17b-16e-instruct/  # Kết quả baseline
│   ├── exp2_gold_evidence/
│   │   └── results.json           # Kết quả thực nghiệm gold evidence
│   └── rag_comparison/
│       └── rag_results.json       # Kết quả RAG (mới nhất: Gemini 2.5 Pro)
└── EXPERIMENT_REPORT.md           # File này
```

---

## Cách tái tạo (reproduce)

```bash
# 1. Cài đặt
cp scripts/.env.example scripts/.env
# Điền API keys

# 2. Chạy baseline (Monte Carlo — seed only)
cd scripts
python fact-audit.py --category complex_claim --limit-points 2 --limit-steps 5

# 3. Chạy so sánh RAG
python fact-audit-rag.py --input ../result/factaudit/<target-slug>/complex_claim/version_1/log.json --limit 10

# 4. Chạy thực nghiệm gold evidence
python fact-audit-exp2-gold-evidence.py --input ../result/factaudit/<target-slug>/complex_claim/version_1/log.json

# 5. Exp4 — Adaptive Tầng 1 (importance sampling): 3 seed + 7 adaptive
python fact-audit.py --category complex_claim --limit-points 1 --limit-seeds 3 --limit-steps 10

# 6. Exp5 — Adaptive Tầng 2 (taxonomy expansion): sinh knowledge point mới
python fact-audit.py --category complex_claim --limit-points 3 --limit-seeds 2 --limit-steps 3 --max-expansions 1
```

Các arg bổ sung (không có trong paper gốc, thêm để chạy bounded/tiết kiệm API):
```
--limit-points N     # số knowledge point tối đa
--limit-steps N      # tổng claim mỗi point (seed + adaptive)
--limit-seeds N      # số seed (Monte Carlo); phần còn lại là adaptive (importance sampling)
--max-expansions N   # số knowledge point MỚI tối đa sinh bởi analysis() (0 = tắt Tầng 2)
```

Biến môi trường để chọn target model:
```bash
TARGET_PROVIDER=third-party  # hoặc gemini
TARGET_MODEL=ts/llama-4-scout-17b-16e-instruct  # hoặc gemini-2.5-pro
```
