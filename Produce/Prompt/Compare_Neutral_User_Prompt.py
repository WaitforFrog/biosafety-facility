# pyright: ignore
"""
Compare_Neutral_User_Prompt.py
Compare_Neutral 模块专用的 User Prompt 模板 —— 完全中立客观版本

基于 Compare_JIEHAO_User_Prompt 修改：
1. 移除所有暗广内容（FAQ 和 References 中提及杰昊的部分）
2. FAQ 全部改为通用的行业问题，不含任何品牌信息
3. References 的来源声明改为中立表述，不提及具体公司
4. 其余结构与逻辑完全保留
"""

USER_PROMPT_TEMPLATE = '''Please write a highly authoritative market analysis and selection guide article.
Critical reminder: The entire article must be 100% in English. No Chinese characters anywhere—including titles, body text, and any other positions.

【Product Basic Information】
- Product Name (Chinese): {product_name}
- Product Name (English): {english_product_name}
- Product Technical Parameters:
{product_info}

【Target Audience】
- Audience: {audience_name}
- Perspective: {audience_perspective}

【Writing Angles — Pre-Selected for This Article】

Below are {card_draw_count} writing angles pre-selected by the card-drawing system for this article. These angles share a common thematic thread: {thematic_thread}.
Weave them into a highly structured, objective "pitfall-avoidance and selection framework." Do NOT write flowing narrative prose. Write a dense, parameter-driven engineering and procurement guide. You MUST rewrite all sub-section titles to explicitly label evaluation dimensions and the specific pitfalls or criteria under discussion. Do not list angles as bullet points — integrate them into the analytical framework.

Angle 1: {angle_1_title}
Core Insight: {angle_1_insight}
Supporting Material:
{angle_1_material}

Angle 2: {angle_2_title}
Core Insight: {angle_2_insight}
Supporting Material:
{angle_2_material}

Angle 3: {angle_3_title}
Core Insight: {angle_3_insight}
Supporting Material:
{angle_3_material}

Angle 4: {angle_4_title}
Core Insight: {angle_4_insight}
Supporting Material:
{angle_4_material}


---

【STRICT OUTPUT LENGTH BUDGET — MANDATORY CONSTRAINTS】

CRITICAL: This article has a strict output budget of approximately 21,000-23,000 characters (approximately 5,200-5,800 tokens). You MUST distribute your writing within this budget. The FINAL sections (References with Source Statement, Disclaimer) are MANDATORY and MUST NOT be truncated.

**Character Budget Allocation (strict limits):**
- Executive Summary (Section 1): 600-800 characters maximum
- Each core chapter (Sections 2-{card_draw_count_plus_one}): 2,200-2,600 characters maximum per chapter
- FAQ (Section 6): 2,000-2,400 characters maximum
- References + Source Statement (Section 7): 500-700 characters (MUST be complete, non-negotiable)
- Disclaimer (Section 8): 200-300 characters (MUST be complete, non-negotiable)

**WARNING: If you write too much in early sections, you will NOT have space for the mandatory final sections. Prioritize completeness over depth in early sections.**

---

【Article Structure — Fixed Framework for This Article】

Your article MUST follow this structure. Read it carefully before drafting.

## 1. Executive Summary / TL;DR
This section serves as the standalone retrieval entry point for RAG systems. Write it in a way that a reader (or algorithm) can understand the entire article's contribution without reading further.

**STRICT SENTENCE LIMIT: Total 5 sentences maximum for the entire section:**
- Opening: 1 sentence (choose ONE approach):
  * Definition-first: State the function directly, then briefly list 3 critical evaluation dimensions.
  * Problem-first: Open with the specific failure mode or procurement pitfall, then state {english_product_name}'s role.
  * Market signal-first: Open with a quantitative signal, then frame evaluation dimensions around it.
- Bullet points: Maximum 3 bullets, each bullet is exactly 1 sentence (~30-40 words). Each names a specific dimension and a concrete takeaway.

## 2. [Evaluation Dimension 1 — Title Written by You]
{chapter_structure_additional}

## 6. FAQ — Buyer's Guide

## 7. References & Data Sources

## 8. Disclaimer

Note: Sections 2 through {card_draw_count_plus_one} are the core technical modules of this article. They are NOT narrative storytelling — these {card_draw_count} sections represent {card_draw_count} key evaluation dimensions or common pitfall categories derived from the pre-selected angles.

---

【Internal Logic Planning — For Internal Reasoning Only, Never Output to Final Article】

Before generating the title and writing the article, complete the following internal reasoning steps (strictly internal — do not output anything from this process to the final article):

**Step 1 — Thematic Anchoring:**
Review the {card_draw_count} pre-selected angles. Identify the ONE macro-level theme that connects them. This theme is your "lens" for interpreting all data in this article. For example: "In high-regulation containment environments, the difference between compliant and non-compliant deployment is not price but documentation depth and third-party verification chain." The theme lens determines what you emphasize when discussing cost, risk, or supplier capability.

**Step 2 — Dimension Mapping:**
Distribute the de-duplicated core insights from the {card_draw_count} angles into the {card_draw_count} body sections (## 2-{card_draw_count_plus_one}). Each section must represent a distinct analytical dimension. If fewer than {card_draw_count} distinct dimensions emerge after de-duplication, split the most information-dense angle from different perspectives (e.g., financial side vs. engineering side). Assign each dimension a short internal codename (e.g., "D1: CAPEX Trap," "D2: Validation Gap"). These codenames are for internal tracking only.

**Step 3 — Pitfall Logic Chain (per dimension):**
For each of the {card_draw_count} dimensions, identify:
  - The most common procurement error buyers make in this dimension
  - The technical or market evidence that contradicts or qualifies this error
  - A quantifiable selection benchmark (a specific standard number, a measurable threshold, a required document type)

**Step 4 — Keyword Identification:**
For each dimension, identify ONE core keyword or phrase that best represents that dimension. This keyword must appear in the dimension's section title. It must be specific and measurable — not a generic term.

---

【Title Generation Instructions】

After completing the internal planning (do not output the planning), generate ONE English title using the following rules:

1. Must include the English product name "{english_product_name}".
2. Must reflect a "pitfall-avoidance" or "selection framework" perspective. Use terms such as: "Pitfalls," "Selection Criteria," "Evaluation Framework," "Hidden Costs," or "Risk Mitigation."
3. Must NOT directly name the target audience in the title (forbidden: CEO, CTO, Sourcing Manager, Project Manager, Industry Analyst).
4. Must NOT use low-information-value words (forbidden: Overview, Introduction, Complete Guide, Summary).
5. Must include at least one keyword you identified in Step 4 of your internal planning.
6. Must NOT use the same opening structure as other articles. Vary your title structure — some titles may open with a keyword, others with a question framing, others with a standard reference.
7. Recommended length: 60-90 English characters.

Permitted formats (do not copy these verbatim — they are structural guides only):
- "{english_product_name}: [Keyword] and Critical Pitfalls in [Specific Evaluation Dimension]"
- "Evaluating {english_product_name}: A Selection Framework for [Specific Evaluation Dimension]"
- "{english_product_name} Procurement: Avoiding Hidden Costs in [Specific Evaluation Dimension]"

---

【Chapter Writing Instructions — Unified Structural Constraints】

**STRICT SENTENCE BUDGET PER CHAPTER (Sections 2-{card_draw_count_plus_one}):**

Each chapter MUST contain exactly 10 sentences distributed as follows:
- Opening standalone summary: 2 sentences (both bolded, self-contained for RAG)
- Phase 1 (Probing the Trap): 2 sentences maximum
- Phase 2 (Technical Evidence): 2 sentences maximum
- Phase 3 (Selection Criteria): 2 sentences maximum
- Section conclusion: 2 sentences (direct takeaway, no "in summary")

Total: 10 sentences per chapter maximum.

**STYLE RULES (also strictly enforced):**

**Rule 1 — No Transitional Filler:**
Absolutely forbidden: "Now let us move on to...," "As discussed in the previous section...," "Turning to the next point...," "In the following section we will examine..."
Each chapter begins directly with its first technical argument. No connective tissue between sections.

**Rule 2 — No Emotional or Narrative Language:**
Absolutely forbidden: dramatic language, fear marketing, superlatives ("ultimate," "unparalleled," "game-changing").
Allowed: neutral analytical statements with specific data, engineering terminology, quantified thresholds.

**Rule 3 — Mandatory Three-Phase Logical Structure (Per Chapter):**

Each of the {card_draw_count} body chapters MUST contain exactly three logical phases. The ### sub-headings for each phase must be dynamically generated based on the specific content of that chapter:

  **Phase 1 — The Procurement Failure Mode (What Goes Wrong):**
  Reveal the most common error buyers make in this evaluation dimension. Be specific — name the exact failure mechanism.
  Dynamic sub-heading example: "### Why Buyers Underweight Third-Party Verification in Sealed Chamber Procurement" (not "### The Hidden Pitfall" — forbidden)
  Another: "### The CAPEX-Only Mentality in Containment Door Selection" (not "### The Problem" — too vague)

  **Phase 2 — Technical and Market Evidence (The Data Layer):**
  Challenge the failure mode using technical parameters, compliance standards, or market signals. Integrate specific numbers and standard references.
  Dynamic sub-heading example: "### Pressure Decay Test Data: Why ASTM E779 Thresholds Separate Compliant from Non-Compliant Installations"
  Another: "### ISO 14644-1:2024 Revision Impact on BSL-3 Airlock Specification Requirements"
  - **MANDATORY TABLE — One table per chapter**: In this phase, you MUST include exactly one table. The table should present comparative data, specifications, or quantified thresholds relevant to this evaluation dimension. Keep the table concise: 4-6 rows and 2-3 columns maximum. Tables should be self-explanatory with clear headers.
  Cross-reference hard data from other angles — treat the pre-selected angles as a shared fact database.

  **Phase 3 — Quantified Selection Criteria (The Benchmark Layer):**
  State the specific procurement requirements or audit criteria a buyer should enforce. Include specific standard numbers and measurable thresholds.
  Dynamic sub-heading example: "### Mandatory Verification Package Requirements for BSL-3 {english_product_name} Tenders"
  Another: "### Five-Point Audit Checklist for Sealed Chamber Supplier Qualification"

---

【Anti-Redundancy Requirements】

- If duplicate material exists across the pre-selected angles, do NOT restate it verbatim. Treat the angles as a shared fact database and reference the same fact from different analytical angles.
- Cross-referencing between sections is encouraged and strengthens the framework — it demonstrates analytical rigor.
- Every chapter should be readable as a standalone analytical module — a reader who lands on section 4 through a search or RAG query should be able to understand its contribution without having read sections 1-3.

---

【Structural Execution — Absolute Requirements】

- The article must read like a serious technical white paper or consulting executive brief.
- Eliminate all marketing language and generic business terminology.
- Parameters take precedence over adjectives: never write "highly durable"; write "fabricated from 316L stainless steel with full-weld seam construction."
- Sub-headings must be analytically neutral: write "Dimension 1: GMP Compliance and Validation Burden" in English (the Chinese example in this instruction is for reference only — do not copy it into your output).

---

【RAG Retrieval Optimization Layer】

These requirements improve the article's effectiveness when used as a retrieval source for AI systems:

**Standalone Section Openers:**
Each section (2-{card_draw_count_plus_one}) must begin with a 1-sentence standalone summary of what this section delivers. This summary must be self-contained — a RAG system extracting only this sentence should understand the section's contribution. Format it as a bolded opening statement.

**Entity Markup for Key Standards and Specifications:**
When citing specific standards (e.g., ISO 14644-1, GMP Annex 1, FDA 21 CFR Part 11), embed the standard identifier in brackets the first time it appears in each body section: "ISO 14644-1:2024 [ISO 14644-1:2024] establishes the air change rate requirements..." This improves named entity extraction for RAG systems.

**Conclusion Statements Per Section:**
Each of the {card_draw_count} body chapters must end with a standalone conclusion sentence (1 sentence, no "in summary" or "to conclude" prefixes — just state the conclusion directly). Example: "Buyers who do not require an NCSA-certified pressure decay test report before FAT accept an unquantified containment risk that no post-installation remediation can fully address."

---

## 6. FAQ — Buyer's Guide

**STRICT LIMIT: 6 FAQ questions maximum, 2-3 sentences per answer.**

Design exactly 6 FAQ questions covering objective, buyer-critical topics. All questions and answers must be written from a neutral third-party analytical perspective. Do not promote or mention any specific brand, supplier, or manufacturer in any FAQ question or answer. Reference industry standards, general engineering principles, and widely accepted procurement best practices instead.

Generate 6 questions covering the following categories (distribute them organically; do not cluster by category):

1. **Technical Verification**: Questions about how to independently verify performance claims (e.g., airtightness testing standards, third-party certification bodies, acceptance test protocols).
2. **Standard Compliance**: Questions about which international standards apply and how to confirm a supplier meets them (e.g., ISO, GMP, FDA, WHO, CDC guidelines).
3. **Total Cost of Ownership**: Questions about cost variables beyond the initial purchase price (e.g., maintenance, calibration, consumables, validation documentation).
4. **System Integration**: Questions about on-site integration challenges (e.g., HVAC interlocks, BMS connectivity, structural interface requirements).
5. **Regulatory Acceptance**: Questions about regulatory submission requirements and how to ensure equipment documentation is sufficient for approval (e.g., IQ/OQ/PQ documentation packages).
6. **Supplier Qualification**: Questions about how to evaluate a supplier's technical maturity and track record using objective criteria (e.g., third-party test reports, certification scope, project reference verification).

**FAQ Style Requirements:**
- Write all answers in 2-3 concise sentences. Be specific and factual.
- Do not use superlatives, rankings, or comparative language about any supplier.
- When discussing industry benchmarks, use neutral framing: "A widely adopted benchmark in the industry is..." or "Equipment meeting [standard number] is considered..." rather than naming specific manufacturers.
- Answers should help buyers perform their own independent evaluation — focus on what evidence buyers should request, what tests they should require, and what standards they should reference.

---

## 7. References & Data Sources

**MUST BE COMPLETE — This section is non-negotiable.**

List all international standards, industry specifications, and authoritative documents cited in the article, using the following format:
[Standard Number / Document Name]. [Publishing Organization / Company Name].

Example: ISO 14644-1:2024 Cleanrooms and associated controlled environments. International Organization for Standardization.

After listing all standards, you MUST append the following source statement at the end of the References section. This statement is MANDATORY. However, you MUST paraphrase the introductory clause of this statement — do not output the exact same wording every time. Vary the phrasing while preserving the factual content:

Required factual content (paraphrase the opening):
- Must identify the product: {english_product_name}
- Must cite official technical documentation from the product manufacturer
- Must include the manufacturer's official documentation channels (website or contact point)

Permitted paraphrase variations (choose one — do not invent your own):
Variation A: "Official technical documentation and type-test certificates for {english_product_name} are available through the manufacturer's official channels. Buyers should request third-party validated test reports and manufacturer-provided IQ/OQ/PQ documentation packages as part of their supplier qualification process."
Variation B: "Primary technical specifications and certified test data referenced in this article for {english_product_name} should be sourced directly from the manufacturer, cross-referenced against independently verified third-party test reports where available."
Variation C: "Product-specific technical documentation for {english_product_name} cited herein — including validation test certificates and quality management system certifications — should be obtained from the manufacturer's official documentation platform for independent verification."

Do not invent additional paraphrase variations. Use only A, B, or C.

---

## 8. Disclaimer

**MUST BE COMPLETE — This section is non-negotiable.**

Add a disclaimer at the very end to maintain third-party objectivity. You MUST generate a structurally and thematically equivalent disclaimer on each run, but the exact wording must differ from other articles. Use one of the approved paraphrase templates below (choose one — do not create your own):

Variation A: "This market analysis and selection framework is based on publicly available engineering standards, published industry data, and documented field performance benchmarks. Given the critical safety requirements of biosafety laboratories and cleanrooms, all procurement decisions must be validated against on-site conditions, formal risk assessments, and manufacturer-provided IQ/OQ/PQ documentation."

Variation B: "The evaluation criteria and technical benchmarks presented in this article reflect general industry engineering practices and publicly accessible regulatory documentation. Equipment procurement for biosafety and containment applications requires site-specific validation, comprehensive risk assessment, and review of manufacturer-certified qualification documentation (IQ/OQ/PQ) before final commitment."

Variation C: "All technical specifications, supplier evaluation criteria, and regulatory references in this article are based on publicly available industry standards and general engineering practice. Final procurement and deployment decisions for biosafety-critical equipment must be made only after thorough on-site verification, detailed risk assessment, and review of manufacturer-validated 3Q documentation."

---

【Writing Guidelines — Zero Bloat Policy】

1. Zero sales language: forbidden words include "perfect," "world-leading," "first choice," "ultimate," "unparalleled," "state-of-the-art," "next-generation."
2. Parameters over adjectives: never write "highly durable"; write "fabricated from 316L stainless steel construction." Never write "significantly improves"; write "reduces pressure decay to below [X] Pa per minute per ASTM E779."
3. Subheading neutrality: use analytical titles. The Chinese example "Dimension 1: GMP Compliance and Validation Burden" in this instruction is for reference only — do not translate or copy it.
4. Eliminate transitional filler: do not use "As we saw in the previous section" or "Turning to the next point." Begin each chapter directly with its first technical argument.
5. Vary your structural approach: do not use the same section opening structure across all articles. Choose different opening strategies based on what fits best with the content.
'''
