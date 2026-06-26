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
    font-size: 21px;
    padding: 100px 64px 64px 64px;
    background: #ffffff;
    color: #1d2b36;
    display: flex;
    flex-direction: column;
    justify-content: flex-start !important;
    align-content: flex-start;
  }
  section.mid { justify-content: center !important; }   /* chỉ slide NGẮN mới thêm class mid để canh giữa */
  /* slide ít chữ: thêm class "airy" để giãn cách, lấp đầy bớt khoảng trắng */
  section.airy li { margin:18px 0; }
  section.airy td, section.airy th { padding-top:12px; padding-bottom:12px; }
  section.airy .box { padding:18px 22px; margin-top:22px; }
  section.airy p { margin:18px 0; }
  section.airy h3 { margin-bottom:14px; }
  h2 {
    position: absolute;
    top: 0; left: 0; right: 0;
    margin: 0;
    background: #1F3A68;
    color: #ffffff !important;
    font-size: 26px;
    font-weight: 600;
    padding: 14px 64px;
  }
  h3 { color:#1F3A68; font-size:21px; margin-bottom:4px; }
  strong { color:#1F3A68; }
  em { color:#1d4ed8; font-style:normal; }
  a { color:#1F3A68; }
  code { background:#e7edf6; color:#1F3A68; padding:1px 6px; border-radius:4px; }
  ul { list-style:none; padding-left:6px; }
  ul li { position:relative; padding-left:24px; margin:10px 0; }
  ul li::before { content:"●"; color:#1F3A68; font-size:14px; position:absolute; left:0; top:4px; }
  ol li { margin:10px 0; }
  table { font-size:18px; border-collapse:collapse; margin:6px auto; }
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
  .small { font-size:16px; color:#777; }
  .caption { font-size:14px; color:#888; font-style:italic; }
  .cols { display:flex; gap:30px; }
  .col { flex:1; }
  .box { background:#e7edf6; border:1px solid #c3d2ea; border-radius:10px; padding:12px 20px; }
  .diagram { text-align:center; margin-top:14px; }
  .diagram img { max-height:330px; width:auto; }
  /* --- khoanh đỏ nổi bật (CSS overlay): đặt trong <div position:relative> --- */
  .hl { position:absolute; border:3px solid #e11d48; border-radius:8px; z-index:30; pointer-events:none;
        box-shadow:0 0 0 2px rgba(225,29,72,.12); }
  .hl-oval { border-radius:50%; }
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

<!--
Chào thầy và các bạn. Nhóm 8 xin trình bày đề tài FACT-AUDIT cộng RAG, dựa trên bài báo công bố tại ACL 2025. Phần đầu (cơ sở lý thuyết) do em phụ trách; phần cài đặt và kết quả các bạn trình bày sau. [~25s]
-->

---

## Nội dung trình bày

1. **Bối cảnh & động lực**: vì sao cần đánh giá fact-checking của LLM?
2. **FACT-AUDIT framework**: 3 giai đoạn + Importance Sampling
3. **Khung 5 agent** + cấu trúc test case
4. **Metrics & Kết quả**: IMR / JFR / Grade trên 13 LLM
5. **Từ Limitation → RAG**: đề xuất mở rộng của nhóm

> Đây là **framework đánh giá năng lực** fact-checking của LLM, không phải kiểm chứng một claim cụ thể.

<!--
Bài gồm 5 phần: bối cảnh, khung FACT-AUDIT, các agent và dữ liệu kiểm thử, bộ chỉ số và kết quả, cuối cùng là đề xuất RAG. Nhấn mạnh: đây là framework ĐÁNH GIÁ năng lực, không phải kiểm chứng một phát biểu cụ thể. [~20s]
-->

---

<!-- _class: airy -->

## Bài toán & câu hỏi trung tâm

**Fact-checking** = đưa mô hình một phát biểu, nó phải làm 2 việc:
- **Phán**: phát biểu là Đúng / Sai / Chưa đủ thông tin
- **Giải thích**: nêu lý do cho phán quyết đó *(justification)*

LLM nhớ rất nhiều kiến thức nên làm khá tốt, nhưng vẫn **nhớ sai** và **suy luận sai**.

<div class="box">

**Câu hỏi của bài báo:** Làm sao **tự động chấm điểm** năng lực fact-checking của một LLM một cách công bằng, để biết mô hình nào thật sự đáng tin?

</div>

<!--
Fact-checking nghĩa là đưa mô hình một phát biểu, nó phải vừa phán đúng sai vừa giải thích lý do, với ba nhãn Đúng, Sai, hoặc Chưa đủ thông tin. LLM nhớ nhiều kiến thức nên làm khá tốt nhưng vẫn nhớ sai và suy luận sai. Câu hỏi của bài báo: làm sao tự động chấm điểm năng lực này một cách công bằng, để biết mô hình nào thật sự đáng tin. [~50s]
-->

---

## Hạn chế của các phương pháp đánh giá hiện có

<div class="cols">
<div class="col">

- **Gán nhãn thủ công**: tốn kém, khó mở rộng quy mô
- **Dataset tĩnh**: test data leakage, leaderboard swamping
- **Chỉ đo accuracy của verdict**: bỏ qua justification

Về bản chất, đây là một paradigm phân loại tĩnh: không đánh giá được lập luận và không theo kịp các LLM mới.

</div>
<div class="col">

![w:340px](assets/paper_fig1.png)

<span class="caption">Pipeline đánh giá cũ (a) vs FACT-AUDIT (b) — Lin et al., Fig 1</span>

</div>
</div>

> **Verdict đúng ≠ Lập luận đúng**: mô hình có thể dự đoán đúng nhãn nhưng lập luận sai hoặc thiếu cơ sở.

<!--
Ba hạn chế của cách đánh giá cũ: gán nhãn thủ công tốn kém; dữ liệu tĩnh gây rò rỉ và bão hòa bảng xếp hạng; chỉ đo độ chính xác của nhãn, bỏ qua lập luận. Hình bên phải so sánh pipeline cũ (a) và FACT-AUDIT (b). Ý cốt lõi: dự đoán đúng nhãn không đồng nghĩa lập luận đúng. [~50s]
-->

---

## FACT-AUDIT: ý tưởng cốt lõi

<div class="cols">
<div class="col">

**2 đặc trưng mới**
- Test data **cập nhật động**
- Đánh giá sâu **justification**, không chỉ verdict

Hướng tiếp cận: *agent-driven*, *model-centric*, tự thích nghi theo từng target LLM.

</div>
<div class="col">

**Monte Carlo → Importance Sampling**

$$\mathbb{E}_{p(x)}[F_\alpha(x)] = \int p(x)F_\alpha(x)\,dx$$

MC chậm $O(1/\sqrt{N})$ → dùng $q(x)$ nhắm vùng LLM **dễ sai**:
$$\mathbb{E}_{q(x)}\!\Big[F_\alpha(x)\tfrac{p(x)}{q(x)}\Big]$$

</div>
</div>

<span class="small">$F_\alpha(x)$ = giới hạn hiểu biết của LLM trên case $x$; chọn $q(x)\propto p(x)F_\alpha(x)$ để lấy mẫu hiệu quả.</span>

<!--
Hai đặc trưng: dữ liệu cập nhật động và chấm cả lập luận. Về toán: thay lấy mẫu Monte Carlo rải đều và chậm bằng Importance Sampling, dùng phân phối q nhắm vào vùng mô hình dễ sai. Nói cách khác, khung chủ động truy lùng điểm yếu thay vì kiểm tra ngẫu nhiên. [~60s]
-->

---

## Pipeline 3 giai đoạn (vòng lặp)

<div class="diagram">

![h:230px](diagrams/pipeline.svg)

</div>

<div class="box">

$\Theta_{i+1}\sim\pi(\Theta_{i+1}\mid\Theta_i, M)$: mỗi vòng tập trung vào **điểm yếu** của target LLM. 3 đối tượng khởi tạo: Complex Claim · Fake News · Social Rumor.

</div>

<!--
Ba giai đoạn lặp: Prototype Emulation sinh dữ liệu kiểm thử; Fact Verification chấm điểm cả nhãn lẫn lập luận; Adaptive Updating phân tích chỗ làm kém để cập nhật cây kịch bản. Điểm quan trọng là vòng lặp: mỗi vòng lại nhắm sâu hơn vào điểm yếu của mô hình. [~50s]
-->

---

## Khung 5 Agent

- **Appraiser** *(stage 1 & 3)*: xây & **cập nhật taxonomy** kịch bản
- **Inquirer** *(1)*: sinh **prototype test data**
- **Quality Inspector** *(1)*: kiểm **chất lượng & đa dạng**, validate evidence (Wiki API)
- **Evaluator** *(2)*: **LLM-as-a-Judge**, chấm **Grade 1–10**, lưu $M$
- **Prober** *(2)*: **probing lặp** từ $M$ → sinh case khó hơn

<div class="diagram" style="margin-top:8px;">

![w:830px](assets/paper_fig2.png)

</div>

<span class="caption">Toàn cảnh 5 agent qua 3 giai đoạn, ví dụ thật "thuốc mới chữa tiểu đường" — Lin et al., Fig 2</span>

<!--
Năm agent: Appraiser xây cây kịch bản; Inquirer sinh đề; Quality Inspector lọc chất lượng và đối chiếu bằng chứng qua Wikipedia; Evaluator chấm điểm theo kiểu trọng tài; Prober dò ra các đề khó hơn. Hình dưới minh hoạ toàn cảnh bằng ví dụ thật về thuốc chữa tiểu đường, kèm bằng chứng và ba chế độ kiểm thử. [~50s]
-->

---

## Taxonomy kịch bản fact-checking

<div class="diagram">

![w:820px](assets/paper_fig3.png)

</div>

<span class="caption">Appraiser khởi tạo cây kịch bản từ 3 nhóm, mở rộng dần qua các vòng lặp (Lin et al., Fig 3).</span>

<!--
Appraiser khởi tạo cây kịch bản từ ba nhóm: Complex Claim, Fake News và Social Rumor. Mỗi nhóm có nhiều kịch bản con, ví dụ tin giả gồm châm biếm, nội dung sai lệch, ngụy tạo. Cây này được mở rộng dần qua các vòng lặp khi phát hiện điểm yếu mới. [~30s]
-->

---

<!-- _class: airy -->

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

<div class="box">

Test Mode chính là chỗ **RAG** sẽ tác động.

</div>

<!--
Mỗi đề gồm bốn phần: Key Point chỉ dẫn nhiệm vụ, Source Claim là câu cần kiểm chứng, Auxiliary Info là bằng chứng, và Test Mode là bối cảnh. Có ba chế độ: claim không bằng chứng, evidence có bằng chứng chuẩn, và wisdom of crowds dùng bình luận. Lưu ý Test Mode, vì đây là nơi RAG sẽ tác động. [~35s]
-->

---

<!-- _class: airy -->

## Metrics đánh giá

| Metric | Nghĩa | Tốt |
|---|---|---|
| **IMR**: *Insight Mastery Rate* | % câu **Grade ≤ 3** (có lỗi), *metric chủ đạo* | ↓ |
| **JFR**: *Justification Flaw Rate* | % case **verdict đúng nhưng lập luận kém** | ↓ |
| **Grade** | Điểm Evaluator **1–10** (≤3 nếu sai verdict *hoặc* justification) | ↑ |

> **JFR** tách được "đoán đúng nhãn nhưng lập luận rỗng", đúng tinh thần *verdict ≠ justification*.

<!--
Ba chỉ số: IMR là tỉ lệ câu bị chấm từ ba điểm trở xuống, tức có lỗi, đây là chỉ số chủ đạo. JFR là tỉ lệ nhãn đúng nhưng lập luận kém. Grade là điểm một đến mười. Điểm đáng chú ý là JFR: nó bắt đúng trường hợp đoán trúng nhãn nhưng lập luận rỗng. [~40s]
-->

---

## Kết quả: 13 LLM (Table 1)

<div style="position:relative; width:1000px; margin:14px auto 0;">

![w:1000px](assets/paper_table1.png)

<div class="hl" style="left:793px; top:363px; width:72px; height:30px;"></div>

</div>

<span class="caption">GPT-4o đạt IMR thấp nhất (12.02%); Qwen2.5-72B (mã nguồn mở) bám sát. IMR là metric chủ đạo — Lin et al., Table 1.</span>

<!--
Bảng đầy đủ 13 mô hình với IMR, JFR, Grade ở cả ba nhóm và Overall. Khoanh đỏ: GPT-4o đạt IMR thấp nhất khoảng mười hai phần trăm. Đáng chú ý Qwen2.5-72B mã nguồn mở bám sát nhóm proprietary, dòng LLaMA yếu hơn. Prototype do người và do mô hình tạo cho kết quả gần như nhau, khẳng định tính công bằng. [~40s]
-->

---

## Phân tích sâu

<div class="cols">
<div class="col">

**Kịch bản khó nhất**

![w:430px](assets/paper_fig4.png)

<span class="caption">IMR của 2 kịch bản khó nhất mỗi nhóm (Fig 4)</span>

</div>
<div class="col">

**Vòng lặp hội tụ**

![w:430px](assets/paper_fig5.png)

<span class="caption">IMR giảm dần & hội tụ qua các vòng probing (Fig 5)</span>

</div>
</div>

<!--
Hai phân tích bổ sung. Bên trái: hai kịch bản khó nhất của mỗi nhóm, ví dụ suy luận nhiều bước hay tiêu đề lệch nội dung. Bên phải: IMR giảm dần rồi hội tụ qua các vòng probing, chứng minh framework đào đúng vào điểm yếu và quá trình lặp ổn định. [~30s]
-->

---

<!-- _class: airy -->

## Test Mode quyết định độ khó

| Test Mode | Độ khó | GPT-4o IMR |
|---|---|---|
| `[claim]` (không bằng chứng) | **Khó nhất** | 23.1% |
| `[wisdom of crowds]` | Trung bình | 15.4% |
| `[evidence]` (có bằng chứng) | **Dễ nhất** | **10.6%** |

<div class="box"><strong>Có bằng chứng giúp LLM fact-check chính xác hơn đáng kể</strong> (IMR giảm khoảng 2 lần). Đây là cơ sở để tích hợp RAG.</div>

<!--
Độ khó phụ thuộc mạnh vào chế độ kiểm thử: claim không bằng chứng khó nhất, evidence có bằng chứng dễ nhất; với GPT-4o, IMR giảm gần một nửa khi có bằng chứng. Đây chính là quan sát then chốt làm cơ sở để nhóm đề xuất RAG. [~35s]
-->

---

## Từ Limitation → RAG (đề xuất của nhóm)

> Paper **tự nêu** ở *Limitations*: *"…incorporate advanced techniques such as **Retrieval-Augmented Generation (RAG)**…"*

<div class="diagram">

![h:170px](diagrams/rag.svg)

</div>

<span class="caption">Giả thuyết: việc bổ sung evidence đưa trường hợp <code>[claim]</code> tiệm cận <code>[evidence]</code>, kỳ vọng giảm IMR/JFR (trên cùng claim set và cùng target model).</span>

<!--
Đề xuất xuất phát trực tiếp từ bài báo: chính tác giả nêu RAG trong mục Limitations. Nhóm cắm một retriever trước mô hình mục tiêu, lấy bằng chứng liên quan rồi ghép vào prompt. Giả thuyết: việc này đưa trường hợp claim tiệm cận evidence, kỳ vọng giảm IMR và JFR. Phần cài đặt và kết quả so sánh do các bạn trình bày tiếp. [~50s]
-->

---

<!-- _class: lead -->

<div class="thanks">

# Cảm ơn! · Q&A

</div>

**Nhóm 8 · IT2040**
Trần Tú Quang · Tô Huỳnh Minh Tiến · Nguyễn Ấn
Lin et al., *FACT-AUDIT*, ACL 2025 · arXiv 2502.17924

<span class="small">University of Information Technology, VNU-HCM (UIT)</span>

<!--
Đó là phần cơ sở lý thuyết. Em xin chuyển sang phần cài đặt do bạn Tiến trình bày. Em xin cảm ơn thầy và các bạn. [~15s]
-->
