---
marp: true
title: "FACT-AUDIT + RAG"
author: "Nhóm 8 · IT2040"
paginate: true
html: true
math: katex
backgroundColor: "#ffffff"
color: "#1d2b36"
style: |
  @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,400;0,600;0,700;1,400&display=swap');
  section {
    font-family: "Be Vietnam Pro", "Segoe UI", system-ui, sans-serif;
    font-size: 24px;
    padding: 100px 64px 64px 64px;
    background: #ffffff;
    color: #1d2b36;
    display: flex;
    flex-direction: column;
    justify-content: flex-start !important;
    align-content: flex-start;
  }
  h2 {
    position: absolute;
    top: 0; left: 0; right: 0;
    margin: 0;
    background: #1F3A68;
    color: #ffffff !important;
    font-size: 30px;
    font-weight: 600;
    padding: 16px 64px;
  }
  h3 { color:#1F3A68; font-size:24px; margin-bottom:4px; }
  strong { color:#1F3A68; }
  em { color:#1d4ed8; font-style:normal; }
  a { color:#1F3A68; }
  code { background:#e7edf6; color:#1F3A68; padding:1px 6px; border-radius:4px; }
  ul { list-style:none; padding-left:6px; }
  ul li { position:relative; padding-left:24px; margin:10px 0; }
  ul li::before { content:"●"; color:#1F3A68; font-size:14px; position:absolute; left:0; top:4px; }
  ol li { margin:10px 0; }
  table { font-size:21px; border-collapse:collapse; margin:6px 0; }
  th { background:#1F3A68; color:#ffffff; }
  td { background:#ffffff; }
  td,th { border:1px solid #c3d2ea; padding:5px 12px; }
  blockquote { border-left:4px solid #1F3A68; background:#e7edf6; color:#20324f; padding:8px 18px; }
  footer { left:0; bottom:0; width:100%; box-sizing:border-box;
           display:flex; padding:0; height:26px; font-size:13px; color:#ffffff;
           background:linear-gradient(90deg,#0e1d38 0%,#16294d 30%,#1f3a68 62%,#2a4d86 100%); }
  footer span { flex:1; display:flex; align-items:center; justify-content:center;
                border-right:1px solid rgba(255,255,255,.3); }
  footer span:nth-child(4) { flex:0 0 64px; }
  footer span:last-child { border-right:none; }
  section::after { position:absolute; right:18px; bottom:5px; z-index:10;
                   color:#ffffff; font-weight:600; font-size:13px;
                   content: attr(data-marpit-pagination) " / " attr(data-marpit-pagination-total); }
  header { position:absolute; top:9px; right:16px; left:auto; margin:0; padding:0;
           background:none; box-shadow:none; z-index:40; }
  header img { height:46px; display:block; background:#ffffff; border-radius:8px;
               padding:4px 7px; box-shadow:0 1px 5px rgba(0,0,0,.22); }
  section.lead { text-align:center; justify-content:flex-start; }
  .titlebox { width:100%; box-sizing:border-box; background:#1F3A68;
    border-radius:10px; padding:24px 40px; margin:48px 0 30px 0;
    box-shadow:0 5px 12px rgba(0,0,0,.18); text-align:center; }
  .titlebox h1 { background:none; border:none; box-shadow:none; display:block;
    color:#ffffff !important; font-size:36px; margin:0; padding:0; }
  .titlebox h3 { color:#ffffff !important; font-weight:400; margin:8px 0 0 0; }
  section.lead h3 { color:#1d2b36; font-weight:400; margin-top:0; }
  .thanks h1 { background:none; border:none; box-shadow:none;
    color:#1F3A68 !important; font-size:44px; font-weight:700; margin:60px 0 28px 0; padding:0; }
  .small { font-size:18px; color:#777; }
  .caption { font-size:16px; color:#888; font-style:italic; }
  .cols { display:flex; gap:30px; }
  .col { flex:1; }
  .box { background:#e7edf6; border:1px solid #c3d2ea; border-radius:10px; padding:12px 20px; }
  .diagram { text-align:center; margin-top:14px; }
  .diagram img { max-height:330px; width:auto; }
footer: '<span>Nhóm 8 · IT2040</span><span>FACT-AUDIT</span><span>Ho Chi Minh, 7/2026</span><span></span>'
header: '<img src="assets/UIT_logo.svg" alt="UIT">'
---

<!-- _class: lead -->

<div class="titlebox">

# FACT-AUDIT + RAG
### Evidence-Augmented Adaptive Fact-Checking Audit

</div>

**Trần Tú Quang · Tô Huỳnh Minh Tiến · Nguyễn Ấn**

GVHD: TS. Lưu Thanh Sơn

<span class="small">IT2040 · Các mô hình ngôn ngữ lớn & ứng dụng · Báo cáo cuối kỳ</span>

<br>

<span class="small">Ho Chi Minh, 7/2026</span>

---

## Nội dung trình bày

1. **Bối cảnh & động lực**: vì sao cần đánh giá fact-checking của LLM?
2. **FACT-AUDIT framework**: 3 giai đoạn + Importance Sampling
3. **Khung 5 agent** + cấu trúc test case
4. **Metrics & Kết quả**: IMR / JFR / Grade trên 13 LLM
5. **Từ Limitation → RAG**: đề xuất mở rộng của nhóm

> Đây là **framework đánh giá năng lực** fact-checking của LLM, không phải kiểm chứng một claim cụ thể.

---

## Bài toán & câu hỏi trung tâm

Cho một **Source Claim**, fact-checking dự đoán tính đúng sai **kèm lập luận**, gán nhãn **Factual / Non-Factual / Not Enough Info** dựa trên tri thức phụ trợ.

LLM lưu tri thức như "knowledge base" → hỗ trợ fact-checking, nhưng vẫn **sai kiến thức** và **lỗi suy luận**.

<div class="box">

**Câu hỏi nghiên cứu:** Làm sao *đánh giá tự động & có hệ thống* giới hạn năng lực fact-checking của LLM, để biết model nào đáng tin?

</div>

---

## Vì sao cách đánh giá cũ chưa đủ?

| # | Hạn chế của eval cũ | Hệ quả |
|---|---|---|
| 1 | Annotation **thủ công** | Tốn kém, **khó scale** |
| 2 | Dataset **tĩnh** | **Test data leakage** + leaderboard swamping |
| 3 | Chỉ đo **accuracy** của verdict | Bỏ qua **justification** (lập luận) |

> **Verdict đúng ≠ Lập luận đúng**: model có thể đoán trúng nhãn nhưng lý do sai/rỗng.

---

## FACT-AUDIT: ý tưởng cốt lõi

<div class="cols">
<div class="col">

**2 đặc trưng mới**
- Test data **cập nhật động**
- Đánh giá sâu **justification**, không chỉ verdict

→ *agent-driven*, *model-centric*, tự thích nghi theo từng target LLM.

</div>
<div class="col">

**Monte Carlo → Importance Sampling**

$$\mathbb{E}_{p(x)}[F_\alpha(x)] = \int p(x)F_\alpha(x)\,dx$$

MC chậm $O(1/\sqrt{N})$ → dùng $q(x)$ nhắm vùng LLM **dễ sai**:
$$\mathbb{E}_{q(x)}\!\Big[F_\alpha(x)\tfrac{p(x)}{q(x)}\Big]$$

</div>
</div>

<span class="small">$F_\alpha(x)$ = giới hạn hiểu biết của LLM trên case $x$; chọn $q(x)\propto p(x)F_\alpha(x)$ để lấy mẫu hiệu quả.</span>

---

## Pipeline 3 giai đoạn (vòng lặp)

<div class="diagram">

![h:230px](diagrams/pipeline.svg)

</div>

<div class="box">

$\Theta_{i+1}\sim\pi(\Theta_{i+1}\mid\Theta_i, M)$: mỗi vòng tập trung vào **điểm yếu** của target LLM. 3 đối tượng khởi tạo: Complex Claim · Fake News · Social Rumor.

</div>

---

## Khung 5 Agent

| Agent | Stage | Vai trò |
|---|---|---|
| **Appraiser** | 1 & 3 | Xây & **cập nhật taxonomy** kịch bản |
| **Inquirer** | 1 | Sinh **prototype test data** |
| **Quality Inspector** | 1 | Kiểm **chất lượng & đa dạng**, validate evidence (Wiki API) |
| **Evaluator** | 2 | **LLM-as-a-Judge**: chấm **Grade 1–10** + comment, lưu $M$ |
| **Prober** | 2 | **Probing lặp** từ $M$ → sinh case khó hơn |

<span class="small">Memory Pool $M=\{x, r, s, c\}$ · giới hạn năng lực $F_\alpha(x)\propto 1/s$.</span>

---

## Cấu trúc một test case

<div class="cols">
<div class="col">

**4 thành phần**
- **Key Point**: chỉ dẫn nhiệm vụ
- **Source Claim**: câu cần kiểm chứng
- **Auxiliary Info**: bằng chứng phụ trợ
- **Test Mode**: bối cảnh bài toán

</div>
<div class="col">

**3 Test Mode**
- `[claim]`: *không* evidence (closed-book)
- `[evidence]`: bằng chứng vàng từ Wiki
- `[wisdom of crowds]`: luồng bình luận MXH

</div>
</div>

<div class="box">Test Mode chính là chỗ **RAG** sẽ tác động.</div>

---

## Metrics đánh giá

| Metric | Nghĩa | Tốt |
|---|---|---|
| **IMR**: *Insight Mastery Rate* | % câu **Grade ≤ 3** (có lỗi), *metric chủ đạo* | ↓ |
| **JFR**: *Justification Flaw Rate* | % case **verdict đúng nhưng lập luận kém** | ↓ |
| **Grade** | Điểm Evaluator **1–10** (≤3 nếu sai verdict *hoặc* justification) | ↑ |

> **JFR** tách được "đoán đúng nhãn nhưng lập luận rỗng", đúng tinh thần *verdict ≠ justification*.

---

## Kết quả: 13 LLM (zero-shot, temp = 0)

<div class="cols">
<div class="col">

**Overall IMR ↓ (thấp = tốt)**

| Model | IMR |
|---|---|
| 🥇 GPT-4o | **12.0%** |
| 🥈 Qwen2.5-72B | 16.0% |
| 🥉 Claude3.5-Sonnet | 24.3% |
| Gemini-Pro | 27.3% |
| Mistral-7B | 54.8% |

</div>
<div class="col">

**Nhận xét**
- Top tier: GPT-4o, Qwen2.5-72B, Claude3.5, Gemini-Pro
- **Qwen2.5-72B** (open) ngang nhóm proprietary
- Dòng **LLaMA** yếu hơn rõ rệt
- Probing lặp → IMR **giảm dần & hội tụ**

</div>
</div>

---

## Test Mode quyết định độ khó

| Test Mode | Độ khó | GPT-4o IMR |
|---|---|---|
| `[claim]` (không bằng chứng) | **Khó nhất** | 23.1% |
| `[wisdom of crowds]` | Trung bình | 15.4% |
| `[evidence]` (có bằng chứng) | **Dễ nhất** | **10.6%** |

<div class="box"><strong>Có bằng chứng → LLM fact-check tốt hơn hẳn</strong> (IMR giảm ~2×). Đây là cánh cửa để RAG chen vào.</div>

---

## Từ Limitation → RAG (đề xuất của nhóm)

> Paper **tự nêu** ở *Limitations*: *"…incorporate advanced techniques such as **Retrieval-Augmented Generation (RAG)**…"*

<div class="diagram">

![h:170px](diagrams/rag.svg)

</div>

<span class="caption">Giả thuyết: RAG kéo case <code>[claim]</code> → gần <code>[evidence]</code> ⇒ giảm IMR/JFR (cùng claim set, cùng target model).</span>

---

<!-- _class: lead -->

<div class="thanks">

# Cảm ơn! · Q&A

</div>

**Nhóm 8 · IT2040**
Trần Tú Quang · Tô Huỳnh Minh Tiến · Nguyễn Ấn
Lin et al., *FACT-AUDIT*, ACL 2025 · arXiv 2502.17924

<span class="small">University of Information Technology, VNU-HCM (UIT)</span>
