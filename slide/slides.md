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
  @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap');
  :root {
    --navy:#1F3A68; --navy-deep:#16294d; --ink:#1d2b36;
    --accent:#2a6df4; --soft:#eef3fb; --line:#d4deee; --muted:#6b7a90;
  }
  section {
    font-family: "Be Vietnam Pro", "Segoe UI", system-ui, sans-serif;
    font-size: 22px;
    padding: 92px 66px 58px 66px;
    background:
      radial-gradient(1200px 380px at 88% -8%, #eef3fb 0%, rgba(238,243,251,0) 60%),
      #ffffff;
    color: var(--ink);
    display: flex; flex-direction: column;
    justify-content: flex-start !important; align-content: flex-start;
    letter-spacing:.1px;
  }
  /* --- THANH HEADER NAVY gradient tràn viền (dùng cho ## slide nội dung) --- */
  h2 {
    position: absolute; top: 0; left: 0; right: 0; margin: 0;
    background: linear-gradient(100deg, var(--navy-deep) 0%, var(--navy) 58%, #28508f 100%);
    color: #ffffff !important; font-size: 27px; font-weight: 600;
    padding: 16px 66px 14px 66px;
    box-shadow: 0 3px 14px rgba(15,29,56,.18);
  }
  h3 {
    color: var(--navy); font-size: 22px; font-weight: 700; margin: 2px 0 12px 0;
    padding-bottom: 6px; border-bottom: 2px solid var(--line); display: inline-block;
  }
  p { margin: 8px 0; }
  strong { color: var(--navy); font-weight: 700; }
  em { color: var(--accent); font-style: normal; font-weight: 600; }
  a { color: var(--navy); }
  code { background: var(--soft); color: var(--navy); padding: 1px 7px; border-radius: 5px; font-size: .94em; }
  /* --- bullet markers gradient vuông bo --- */
  ul { list-style: none; padding-left: 4px; margin: 6px 0; }
  ul li { position: relative; padding-left: 26px; margin: 10px 0; line-height: 1.45; }
  ul li::before {
    content: ""; position: absolute; left: 3px; top: .55em;
    width: 8px; height: 8px; border-radius: 3px;
    background: linear-gradient(135deg, var(--navy), var(--accent));
  }
  ol { padding-left: 22px; } ol li { margin: 10px 0; line-height: 1.45; }
  /* --- bảng bo góc + đổ bóng + zebra --- */
  table { font-size: 19px; border-collapse: collapse; margin: 10px auto; width: 100%;
    border-radius: 10px; overflow: hidden; }
  thead th { background: var(--navy); color: #fff; font-weight: 600; }
  th { background: var(--navy); color: #fff; }
  tbody tr:nth-child(even) td { background: #f6f9fe; }
  td, th { border: 1px solid var(--line); padding: 7px 13px; }
  blockquote {
    border: none; border-left: 5px solid var(--accent);
    background: var(--soft); color: #20324f; padding: 11px 20px;
    border-radius: 0 12px 12px 0; margin: 12px 0;
  }
  /* --- công thức display dạng card --- */
  .katex-display {
    background: linear-gradient(180deg, #f7faff 0%, #eef3fb 100%);
    border: 1px solid var(--line); border-left: 5px solid var(--navy);
    border-radius: 12px; padding: 14px 20px; margin: 12px 0;
    box-shadow: 0 2px 12px rgba(15,29,56,.07);
  }
  .katex { font-size: 1.12em; }
  /* --- footer 4 ô gradient (Name | Title | Date | page) --- */
  footer { left:0; bottom:0; width:100%; box-sizing:border-box; display:flex; padding:0;
    height:26px; font-size:13px; color:#ffffff;
    background: linear-gradient(90deg,#0e1d38 0%,#16294d 30%,#1f3a68 62%,#2a4d86 100%); }
  footer span { flex:1; display:flex; align-items:center; justify-content:center;
    border-right:1px solid rgba(255,255,255,.28); }
  footer span:nth-child(4) { flex:0 0 64px; }
  footer span:last-child { border-right:none; }
  section::after { position:absolute; right:20px; bottom:5px; z-index:10; color:#ffffff;
    font-weight:600; font-size:13px;
    content: attr(data-marpit-pagination) " / " attr(data-marpit-pagination-total); }
  /* --- logo UIT góc phải (circle, giữ size nhỏ theo deck) --- */
  header { position:absolute; top:11px; right:20px; left:auto; margin:0; padding:0;
    background:none; box-shadow:none; z-index:40; }
  header img { width:30px; height:30px; object-fit:contain; display:block; background:#ffffff;
    border-radius:50%; padding:4px; box-sizing:border-box; box-shadow:0 1px 5px rgba(0,0,0,.22); }
  section.cover header img { background:none; box-shadow:none; padding:0; }
  /* --- slide bìa / cảm ơn dạng lead --- */
  section.lead { text-align:center; justify-content:center; }
  section.lead::before { content:""; position:absolute; top:0; left:0; right:0; height:8px;
    background: linear-gradient(90deg, var(--navy) 0%, var(--accent) 100%); }
  .titlebox { width:100%; box-sizing:border-box;
    background: linear-gradient(120deg, #16294d 0%, #1F3A68 60%, #2a558f 100%);
    border-radius:16px; padding:28px 44px; margin:10px 0 24px 0;
    box-shadow:0 10px 30px rgba(15,29,56,.22); text-align:center; }
  .titlebox h1 { background:none; border:none; color:#fff !important;
    font-size:40px; margin:0; padding:0; letter-spacing:.3px; }
  .titlebox h3 { color:#cfe0ff !important; font-weight:400; border:none; margin:10px 0 0 0; display:block; }
  section.lead h1 { color:var(--navy); font-size:40px; }
  section.lead h3 { color:var(--ink); font-weight:400; border:none; display:block; }
  .thanks h1 { background:none; border:none; box-shadow:none; color:var(--navy) !important;
    font-size:46px; font-weight:700; margin:40px 0 24px 0; padding:0; }
  /* --- slide chuyển mục (section divider): nền navy + số mờ lớn --- */
  section.divider {
    background-color:#16294d !important;
    background-image: linear-gradient(135deg,#0e1d38 0%,#16294d 45%,#1F3A68 100%) !important;
    color:#eaf1fc; justify-content:center !important; align-content:center;
    padding:92px 80px; overflow:hidden;
  }
  section.divider footer { display:none; }
  section.divider .dnum { position:absolute; top:14px; right:50px;
    font-size:260px; font-weight:800; line-height:1;
    color:rgba(255,255,255,.06); letter-spacing:-6px; z-index:0; pointer-events:none; }
  section.divider .dbar { width:64px; height:6px; border-radius:3px; position:relative; z-index:1;
    background:linear-gradient(90deg,var(--accent),#86b4ff); margin:0 0 20px 0; }
  section.divider h1 { color:#ffffff !important; background:none; border:none; box-shadow:none;
    font-size:46px; line-height:1.12; margin:0 0 16px 0; padding:0; position:relative; z-index:1; max-width:82%; }
  section.divider .dsub { color:#cfe0ff; font-size:23px; line-height:1.5; max-width:80%; position:relative; z-index:1; }
  section.divider .dmeta { color:#9db4d8; font-size:18px; margin-top:28px; position:relative; z-index:1; }
  /* --- components --- */
  .small { font-size:17px; color:var(--muted); }
  .caption { font-size:15px; color:#888; font-style:italic; }
  .box { background:#f7faff; border:1px solid var(--line); border-left:5px solid var(--accent);
    border-radius:0 12px 12px 0; padding:12px 20px; box-shadow:0 2px 12px rgba(15,29,56,.06); }
  .warn { background:#fff8ec; border:1px solid #f3dca6; border-left:5px solid #e0a51e;
    border-radius:0 12px 12px 0; padding:12px 20px; }
  .grid2 { display:grid; grid-template-columns:1fr 1fr; gap:20px; align-items:start; }
  .cols { display:flex; gap:30px; } .col { flex:1; }
  .center { text-align:center; }
  /* --- sơ đồ (ảnh / SVG) --- */
  .diagram { text-align:center; margin-top:12px; }
  .diagram img { max-height:300px; width:auto; }
  .box, .warn, .grid2, .cols, table { margin-top:14px; margin-bottom:14px; }
  /* --- khoanh đỏ nổi bật (CSS overlay): đặt trong <div position:relative> --- */
  .hl { position:absolute; border:3px solid #e11d48; border-radius:8px; z-index:30; pointer-events:none;
        box-shadow:0 0 0 2px rgba(225,29,72,.12); }
  .hl-oval { border-radius:50%; }
footer: '<span>Nhóm 8 · IT2040</span><span>FACT-AUDIT</span><span>Ho Chi Minh, 07/2026</span><span></span>'
header: '<img src="assets/UIT_logo.svg" alt="UIT">'
---

<!-- _class: lead cover -->
<!-- _paginate: false -->

<div class="titlebox">

# FACT-AUDIT + RAG
### Evidence-Augmented Adaptive Fact-Checking Audit

</div>

**Trần Tú Quang · Tô Huỳnh Minh Tiến · Nguyễn Ấn**

GVHD: TS. Lưu Thanh Sơn

<span class="small">IT2040 · Các mô hình ngôn ngữ lớn & ứng dụng · Báo cáo cuối kỳ</span>

<br>

<span class="small">Ho Chi Minh, 07/2026</span>

<!--
Chào thầy và các bạn. Nhóm 8 xin trình bày đề tài FACT-AUDIT cộng RAG, dựa trên bài báo công bố tại ACL 2025. Phần đầu (cơ sở lý thuyết) do em phụ trách; phần cài đặt và kết quả các bạn trình bày sau. [~25s]
-->

---

<!-- _footer: '<span>Nhóm 8 · IT2040</span><span>FACT-AUDIT</span><span>Ho Chi Minh, 07/2026</span><span></span>' -->

## Nội dung trình bày

1. **Bối cảnh & động lực**: vì sao cần đánh giá fact-checking của LLM?
2. **FACT-AUDIT framework**: 3 giai đoạn và Importance Sampling
3. **Khung 5 agent** và cấu trúc test case
4. **Metrics & Kết quả**: IMR / JFR / Grade trên 13 LLM
5. **Thực nghiệm tái hiện**: nhóm chạy lại framework
6. **Hướng mở rộng: RAG**, đề xuất của nhóm

> Đây là **framework đánh giá năng lực** fact-checking của LLM, không phải kiểm chứng một claim cụ thể.

<!--
Bài gồm sáu phần: bối cảnh, khung FACT-AUDIT, các agent và dữ liệu kiểm thử, bộ chỉ số và kết quả, phần tái hiện framework do nhóm chạy lại, cuối cùng là đề xuất RAG. Nhấn mạnh: đây là framework ĐÁNH GIÁ năng lực, không phải kiểm chứng một phát biểu cụ thể. [~20s]
-->

---

<!-- _class: divider -->

<div class="dnum">1</div>

<div class="dbar"></div>

# Bối cảnh & động lực

<div class="dsub">Vì sao cần đánh giá năng lực fact-checking của LLM?</div>

<div class="dmeta">Phần 1</div>

---

<!-- _footer: '<span>Nhóm 8 · IT2040</span><span>1. Bối cảnh & động lực</span><span>Ho Chi Minh, 07/2026</span><span></span>' -->

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

<!-- _footer: '<span>Nhóm 8 · IT2040</span><span>1. Bối cảnh & động lực</span><span>Ho Chi Minh, 07/2026</span><span></span>' -->

## Hạn chế của các phương pháp đánh giá hiện có

<style scoped>
  .cols { align-items: center; }
</style>

<div class="cols">
<div class="col">

- **Gán nhãn thủ công**: tốn kém, khó mở rộng quy mô
- **Dataset tĩnh**: test data leakage, leaderboard swamping
- **Chỉ đo accuracy của verdict**: bỏ qua justification

Về bản chất, đây là một paradigm phân loại tĩnh: không đánh giá được lập luận và không theo kịp các LLM mới.

</div>
<div class="col center">

![w:380px](assets/paper_fig1.png)

<span class="caption">Pipeline đánh giá cũ (a) vs FACT-AUDIT (b) — Lin et al., Fig 1</span>

</div>
</div>

> **Verdict đúng ≠ Lập luận đúng**: mô hình có thể dự đoán đúng nhãn nhưng lập luận sai hoặc thiếu cơ sở.

<!--
Ba hạn chế của cách đánh giá cũ: gán nhãn thủ công tốn kém; dữ liệu tĩnh gây rò rỉ và bão hòa bảng xếp hạng; chỉ đo độ chính xác của nhãn, bỏ qua lập luận. Hình bên phải so sánh pipeline cũ (a) và FACT-AUDIT (b). Ý cốt lõi: dự đoán đúng nhãn không đồng nghĩa lập luận đúng. [~50s]
-->

---

<!-- _class: divider -->

<div class="dnum">2</div>

<div class="dbar"></div>

# FACT-AUDIT framework

<div class="dsub">3 giai đoạn lặp · Importance Sampling nhắm điểm yếu</div>

<div class="dmeta">Phần 2</div>

---

<!-- _footer: '<span>Nhóm 8 · IT2040</span><span>2. FACT-AUDIT framework</span><span>Ho Chi Minh, 07/2026</span><span></span>' -->

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

<!-- _footer: '<span>Nhóm 8 · IT2040</span><span>2. FACT-AUDIT framework</span><span>Ho Chi Minh, 07/2026</span><span></span>' -->

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

<!-- _class: divider -->

<div class="dnum">3</div>

<div class="dbar"></div>

# Khung 5 agent & test case

<div class="dsub">5 vai trò agent · taxonomy kịch bản · cấu trúc test case</div>

<div class="dmeta">Phần 3</div>

---

<!-- _footer: '<span>Nhóm 8 · IT2040</span><span>3. Khung 5 agent</span><span>Ho Chi Minh, 07/2026</span><span></span>' -->

## Khung 5 Agent

<style scoped>
  section { padding-top: 78px; }
  ul { margin: 4px 0; }
  ul li { margin: 6px 0; }
  .diagram { margin-top: 4px; }
  .diagram img { max-height: 360px; }
</style>

- **Appraiser** *(stage 1 & 3)*: xây & **cập nhật taxonomy** kịch bản
- **Inquirer** *(1)*: sinh **prototype test data**
- **Quality Inspector** *(1)*: kiểm **chất lượng & đa dạng**, validate evidence (Wiki API)
- **Evaluator** *(2)*: **LLM-as-a-Judge**, chấm **Grade 1–10**, lưu $M$
- **Prober** *(2)*: **probing lặp** từ $M$ → sinh case khó hơn

<div class="diagram" style="margin-top:4px;">

![w:900px](assets/paper_fig2.png)

</div>

<span class="caption">Toàn cảnh 5 agent qua 3 giai đoạn, ví dụ thật "thuốc mới chữa tiểu đường" — Lin et al., Fig 2</span>

<!--
Năm agent: Appraiser xây cây kịch bản; Inquirer sinh đề; Quality Inspector lọc chất lượng và đối chiếu bằng chứng qua Wikipedia; Evaluator chấm điểm theo kiểu trọng tài; Prober dò ra các đề khó hơn. Hình dưới minh hoạ toàn cảnh bằng ví dụ thật về thuốc chữa tiểu đường, kèm bằng chứng và ba chế độ kiểm thử. [~50s]
-->

---

<!-- _footer: '<span>Nhóm 8 · IT2040</span><span>3. Khung 5 agent</span><span>Ho Chi Minh, 07/2026</span><span></span>' -->

## Taxonomy kịch bản fact-checking

<div class="diagram">

![w:820px](assets/paper_fig3.png)

</div>

<span class="caption">Appraiser khởi tạo cây kịch bản từ 3 nhóm, mở rộng dần qua các vòng lặp (Lin et al., Fig 3).</span>

<!--
Appraiser khởi tạo cây kịch bản từ ba nhóm: Complex Claim, Fake News và Social Rumor. Mỗi nhóm có nhiều kịch bản con, ví dụ tin giả gồm châm biếm, nội dung sai lệch, ngụy tạo. Cây này được mở rộng dần qua các vòng lặp khi phát hiện điểm yếu mới. [~30s]
-->

---

<!-- _footer: '<span>Nhóm 8 · IT2040</span><span>3. Khung 5 agent</span><span>Ho Chi Minh, 07/2026</span><span></span>' -->

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
Mỗi đề gồm bốn phần: Key Point chỉ dẫn nhiệm vụ, Source Claim là câu cần kiểm chứng, Auxiliary Info là bằng chứng, và Test Mode là bối cảnh. Có ba chế độ: claim, evidence có bằng chứng chuẩn, và wisdom of crowds dùng bình luận. Lưu ý Test Mode, vì đây là nơi RAG sẽ tác động. [~35s]
-->

---

<!-- _class: divider -->

<div class="dnum">4</div>

<div class="dbar"></div>

# Metrics & Kết quả

<div class="dsub">IMR · JFR · Grade — đánh giá trên 13 LLM</div>

<div class="dmeta">Phần 4</div>

---

<!-- _footer: '<span>Nhóm 8 · IT2040</span><span>4. Metrics & Kết quả</span><span>Ho Chi Minh, 07/2026</span><span></span>' -->

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

<!-- _footer: '<span>Nhóm 8 · IT2040</span><span>4. Metrics & Kết quả</span><span>Ho Chi Minh, 07/2026</span><span></span>' -->

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

<!-- _footer: '<span>Nhóm 8 · IT2040</span><span>4. Metrics & Kết quả</span><span>Ho Chi Minh, 07/2026</span><span></span>' -->

## Phân tích sâu

<style scoped>
  .cols { margin-top: 24px; }
  .col img { max-width: 100%; }
</style>

<div class="cols">
<div class="col center">

**Kịch bản khó nhất**

![w:560px](assets/paper_fig4.png)

<span class="caption">IMR của 2 kịch bản khó nhất mỗi nhóm (Fig 4)</span>

</div>
<div class="col center">

**Vòng lặp hội tụ**

![w:560px](assets/paper_fig5.png)

<span class="caption">IMR giảm dần & hội tụ qua các vòng probing (Fig 5)</span>

</div>
</div>

<!--
Hai phân tích bổ sung. Bên trái: hai kịch bản khó nhất của mỗi nhóm, ví dụ suy luận nhiều bước hay tiêu đề lệch nội dung. Bên phải: IMR giảm dần rồi hội tụ qua các vòng probing, chứng minh framework đào đúng vào điểm yếu và quá trình lặp ổn định. [~30s]
-->

---

<!-- _footer: '<span>Nhóm 8 · IT2040</span><span>4. Metrics & Kết quả</span><span>Ho Chi Minh, 07/2026</span><span></span>' -->

## Test Mode quyết định độ khó

| Test Mode | Độ khó | GPT-4o IMR |
|---|---|---|
| `[claim]` | **Khó nhất** | 23.1% |
| `[wisdom of crowds]` | Trung bình | 15.4% |
| `[evidence]` | **Dễ nhất** | **10.6%** |

<div class="box"><strong>Có bằng chứng giúp LLM fact-check chính xác hơn đáng kể</strong> (IMR giảm khoảng 2 lần). Đây là cơ sở để tích hợp RAG.</div>

<!--
Độ khó phụ thuộc mạnh vào chế độ kiểm thử: claim khó nhất, evidence có bằng chứng dễ nhất; với GPT-4o, IMR giảm gần một nửa khi có bằng chứng. Đây chính là quan sát then chốt làm cơ sở để nhóm đề xuất RAG. [~35s]
-->

---

<!-- _class: divider -->

<div class="dnum">5</div>

<div class="dbar"></div>

# Thực nghiệm tái hiện

<div class="dsub">Nhóm chạy lại framework: baseline · vòng lặp adaptive · so sánh model</div>

<div class="dmeta">Phần 5</div>

---

<!-- _footer: '<span>Nhóm 8 · IT2040</span><span>5. Thực nghiệm tái hiện</span><span>Ho Chi Minh, 07/2026</span><span></span>' -->

## Cấu hình tái hiện

<div class="cols">
<div class="col">

**Phân vai 3 agent** *(qua API)*
- **Optimizer**: `gemini-2.5-flash`
- **Judge**: `gemini-2.5-flash`
- **Target** *(model bị test)*: thay đổi

**Giữ nguyên logic paper**
- Chỉ đổi backend LLM sang API
- Importance Sampling & taxonomy: nguyên vẹn

</div>
<div class="col">

**Quy mô mỗi lần chạy**
- 3 seed *(Monte Carlo)* + 7 adaptive *(Importance Sampling)*
- Nhóm kịch bản: `complex_claim`
- Metric: **Grade 1–10**, **IMR** (% Grade ≤ 3)

</div>
</div>

<div class="box">

Mục tiêu mid-term: chứng minh **tái hiện đúng cơ chế** của paper, không phải đạt SOTA.

</div>

<!--
Nhóm chạy lại framework qua API. Optimizer và Judge cố định là Gemini 2.5 Flash, đóng vai thước đo; Target là model bị kiểm tra, thay đổi giữa các lần chạy. Logic gốc của paper giữ nguyên, chỉ đổi backend sang API. Mỗi lần chạy gồm ba seed ngẫu nhiên cộng bảy case adaptive. Mục tiêu mid-term là tái hiện đúng cơ chế, không phải đạt điểm cao nhất. [~45s]
-->

---

<!-- _footer: '<span>Nhóm 8 · IT2040</span><span>5. Thực nghiệm tái hiện</span><span>Ho Chi Minh, 07/2026</span><span></span>' -->

## Bằng chứng: Importance Sampling nhắm điểm yếu

**Chạy target LLaMA-4-Scout:** seed case chế độ `wisdom of crowds` bị điểm thấp (3/10).

<div class="box">

Ở 7 case adaptive tiếp theo, Optimizer sinh **6/7 case đều `wisdom of crowds`** — đúng chế độ mô hình vừa làm kém. Đây chính là $q(x)$ tự dồn mật độ vào vùng $F_\alpha(x)$ thấp.

</div>

**Tái hiện 2 tầng adaptive:**
- **Tầng 1** *(Prober)*: sinh case khó hơn TRONG một kịch bản
- **Tầng 2** *(Appraiser)*: phân tích bad case → sinh **kịch bản MỚI** `deductive_causal_reasoning` (suy luận nhân quả nhiều bước) mà taxonomy gốc chưa có

<!--
Bằng chứng cụ thể cho Importance Sampling: khi chạy LLaMA-4-Scout, case chế độ wisdom of crowds bị điểm ba. Ngay sau đó, sáu trên bảy case adaptive đều rơi vào chế độ wisdom, đúng chỗ mô hình yếu. Đây là phân phối q tự dồn vào vùng điểm thấp. Nhóm cũng tái hiện cả hai tầng adaptive: tầng một sinh case khó hơn trong kịch bản, tầng hai tự sinh kịch bản mới về suy luận nhân quả mà cây phân loại gốc chưa có. [~50s]
-->

---

<!-- _footer: '<span>Nhóm 8 · IT2040</span><span>5. Thực nghiệm tái hiện</span><span>Ho Chi Minh, 07/2026</span><span></span>' -->

## Kết quả: framework phân biệt được model

| Target model | Grade | IMR (% Grade ≤ 3) |
|---|---|---|
| LLaMA-4-Scout-17B | 8.00 | 20% |
| **Gemini 2.5 Pro** | **9.80** | **0%** |

<div class="box">

Model mạnh (Gemini Pro) có **IMR thấp hơn hẳn**: khớp tinh thần Table 1 của paper (IMR là chỉ số phân biệt năng lực).

</div>

> Model càng mạnh, Importance Sampling càng **khó đào ra điểm yếu** → cần nhiều vòng probing hơn để hội tụ (khớp Fig 5).

<!--
Kết quả so sánh hai target trên cùng cấu hình: LLaMA-4-Scout đạt Grade tám, IMR hai mươi phần trăm; Gemini 2.5 Pro đạt Grade chín phẩy tám, IMR không phần trăm. Model mạnh có IMR thấp hơn hẳn, đúng tinh thần Table 1 của bài báo. Một nhận xét: model càng mạnh thì Importance Sampling càng khó đào ra điểm yếu, cần nhiều vòng probing hơn để hội tụ, khớp với Figure 5. [~40s]
-->

---

<!-- _class: divider -->

<div class="dnum">6</div>

<div class="dbar"></div>

# Từ Limitation → RAG

<div class="dsub">Đề xuất mở rộng của nhóm: cấp evidence qua retriever</div>

<div class="dmeta">Phần 6</div>

---

<!-- _footer: '<span>Nhóm 8 · IT2040</span><span>6. Từ Limitation → RAG</span><span>Ho Chi Minh, 07/2026</span><span></span>' -->

## Từ Limitation → RAG (đề xuất của nhóm)

> Paper **tự nêu** ở *Limitations*: *"…incorporate advanced techniques such as **Retrieval-Augmented Generation (RAG)**…"*

<div class="diagram">

![h:170px](diagrams/rag.svg)

</div>

<span class="caption">Giả thuyết: việc bổ sung evidence đưa trường hợp <code>[claim]</code> tiệm cận <code>[evidence]</code>, kỳ vọng giảm IMR/JFR (trên cùng claim set và cùng target model).</span>

<div class="warn">

**Câu hỏi để ngỏ cho final-term:** evidence của paper là *gold* (chuẩn, do người soạn). RAG thực tế lấy evidence *tự động* — nếu retrieval **kém liên quan** thì IMR có giảm không? Kết quả so sánh baseline vs RAG sẽ trình bày ở báo cáo cuối kỳ.

</div>

<!--
Đề xuất xuất phát trực tiếp từ bài báo: chính tác giả nêu RAG trong mục Limitations. Nhóm cắm một retriever trước mô hình mục tiêu, lấy bằng chứng liên quan rồi ghép vào prompt. Giả thuyết: việc này đưa trường hợp claim tiệm cận evidence, kỳ vọng giảm IMR và JFR. Nhưng có một câu hỏi để ngỏ: evidence trong bài báo là gold, do người soạn chuẩn; còn RAG thực tế lấy evidence tự động, nếu truy xuất kém liên quan thì chưa chắc giảm IMR. Kết quả so sánh cụ thể nhóm sẽ trình bày ở báo cáo cuối kỳ. [~55s]
-->

---

<!-- _footer: '<span>Nhóm 8 · IT2040</span><span>6. Từ Limitation → RAG</span><span>Ho Chi Minh, 07/2026</span><span></span>' -->

## Tổng kết mid-term

<div class="cols">
<div class="col">

**Đã làm được**
- Hiểu & trình bày cơ chế FACT-AUDIT
- Tái hiện framework qua API
- Xác nhận Importance Sampling nhắm điểm yếu
- Tái hiện 2 tầng adaptive
- So sánh model: framework phân biệt mạnh/yếu

</div>
<div class="col">

**Hướng final-term**
- Cắm retriever (RAG) trước target
- So sánh baseline vs RAG trên cùng claim set
- Phân tích ảnh hưởng của **chất lượng retrieval** lên IMR/JFR

</div>
</div>

<div class="box">

Cốt lõi: từ **hiểu paper** → **tái hiện được** → **đề xuất mở rộng có cơ sở**.

</div>

<!--
Tổng kết phần mid-term. Nhóm đã hiểu và trình bày cơ chế FACT-AUDIT, tái hiện framework qua API, xác nhận Importance Sampling thực sự nhắm vào điểm yếu, tái hiện cả hai tầng adaptive, và so sánh được các model. Hướng cuối kỳ: cắm retriever để làm RAG, so sánh baseline với RAG trên cùng tập claim, và phân tích ảnh hưởng của chất lượng retrieval lên IMR. Mạch xuyên suốt: hiểu paper, tái hiện được, rồi đề xuất mở rộng có cơ sở. [~40s]
-->

<!--
KẾT: chuyển tiếp sang lời cảm ơn.
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
