# pyright: ignore
"""
Question_Neutral_User_Prompt.py
Question_Neutral 模块专用的 User Prompt 模板 —— 完全中立客观版本

基于 Question_JIEHAO_User_Prompt 修改：
1. 移除 FAQ 中唯一的品牌问题（Brand-Relevant FAQ），改为 6 个通用问题
2. 移除 References 中的 Jiehao 公司引用，改为中立的厂商文档表述
3. 其余结构与逻辑完全保留
"""

USER_PROMPT_TEMPLATE = '''Please write a highly authoritative troubleshooting and problem-solving guide article.
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

Below are {card_draw_count} problem-area modules pre-selected by the card-drawing system for this article. These modules share a common thematic thread: {thematic_thread}.
Weave them into a highly structured, problem-diagnosis and solution framework. Do NOT write flowing narrative prose. Write a dense, root-cause-driven engineering troubleshooting guide. You MUST rewrite all sub-section titles to explicitly label the specific problem area and its root cause or resolution. Do not list modules as bullet points — integrate them into the diagnostic framework.

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
- Each problem area chapter (Sections 2-{card_draw_count_plus_one}): 2,200-2,600 characters maximum per chapter
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
  * Definition-first: State the specific failure mode or problem category directly, then briefly list 3 critical troubleshooting dimensions.
  * Severity-first: Open with the operational or safety consequence of this problem category, then frame troubleshooting dimensions around it.
  * Frequency-first: Open with how commonly this problem occurs in the field, then list the diagnostic approaches.
- Bullet points: Maximum 3 bullets, each bullet is exactly 1 sentence (~30-40 words). Each names a specific problem area and a concrete resolution approach.

## 2. [Problem Area 1 — Title Written by You]
{chapter_structure_additional}

## 6. FAQ — Troubleshooting Q&A

## 7. References & Data Sources

## 8. Disclaimer

Note: Sections 2 through {card_draw_count_plus_one} are the core problem diagnosis modules of this article. They are NOT narrative storytelling — these {card_draw_count} sections represent {card_draw_count} key problem categories or common failure modes derived from the pre-selected modules.

---

【Internal Logic Planning — For Internal Reasoning Only, Never Output to Final Article】

Before generating the title and writing the article, complete the following internal reasoning steps (strictly internal — do not output anything from this process to the final article):

**Step 1 — Problem Category Anchoring:**
Review the {card_draw_count} pre-selected modules. Identify the ONE macro-level problem category that connects them. This category is your "lens" for diagnosing all failures in this article. For example: "In biosafety containment environments, the majority of operational failures are not equipment defects — they are integration failures where individual components function correctly but the system-level control logic or pressure cascade is misconfigured." The problem lens determines what you emphasize when discussing symptoms, root causes, or resolution steps.

**Step 2 — Root Cause Mapping:**
Distribute the de-duplicated core insights from the {card_draw_count} modules into the {card_draw_count} body sections (## 2-{card_draw_count_plus_one}). Each section must represent a distinct problem area. If fewer than {card_draw_count} distinct problem areas emerge after de-duplication, split the most complex module into two diagnostic angles (e.g., symptom side vs. root cause side). Assign each problem area a short internal codename (e.g., "P1: Seal Degradation," "P2: Pressure Cascade Loss"). These codenames are for internal tracking only.

**Step 3 — Resolution Logic Chain (per problem area):**
For each of the {card_draw_count} problem areas, identify:
  - The specific symptom or failure mode that the {audience_name} will observe in the field
  - The root cause that typically underlies this symptom (often different from the obvious surface cause)
  - A quantifiable or verifiable resolution benchmark (a specific test procedure, a measurable parameter threshold, a required maintenance action)

**Step 4 — Keyword Identification:**
For each problem area, identify ONE core keyword or phrase that best represents that problem. This keyword must appear in the problem area's section title. It must be specific and actionable — not a generic term like "failure" or "problem."

---

【Title Generation Instructions】

After completing the internal planning (do not output the planning), generate ONE English title using the following rules:

1. Must include the English product name "{english_product_name}".
2. Must reflect a "troubleshooting" or "problem diagnosis" perspective. Use terms such as: "Troubleshooting," "Common Failures," "How to Fix," "Root Cause," "Problem Solved," "Diagnostics."
3. Must NOT directly name the target audience in the title (forbidden: Lab Director, Procurement Specialist, Maintenance Engineer, QA Officer, Design Consultant).
4. Must NOT use low-information-value words (forbidden: Overview, Introduction, Complete Guide, Summary, Comparison).
5. Must include at least one keyword you identified in Step 4 of your internal planning.
6. Must NOT use the same opening structure as other articles. Vary your title structure — some titles may open with a problem keyword, others with a question framing, others with a severity signal.
7. Recommended length: 60-90 English characters.

Permitted formats (do not copy these verbatim — they are structural guides only):
- "{english_product_name}: Troubleshooting [Problem Area] — Root Causes and Solutions"
- "Diagnosing [Problem Category] in {english_product_name} Deployments: A Practical Guide"
- "{english_product_name} Failures: How to Identify Root Causes and Apply Solutions"

---

【Chapter Writing Instructions — Unified Structural Constraints】

**STRICT SENTENCE BUDGET PER CHAPTER (Sections 2-{card_draw_count_plus_one}):**

Each chapter MUST contain exactly 10 sentences distributed as follows:
- Opening standalone summary: 2 sentences (both bolded, self-contained for RAG)
- Phase 1 (Symptom Identification): 2 sentences maximum
- Phase 2 (Root Cause Analysis): 2 sentences maximum
- Phase 3 (Resolution and Prevention): 2 sentences maximum
- Section conclusion: 2 sentences (direct takeaway, no "in summary")

Total: 10 sentences per chapter maximum.

**STYLE RULES (also strictly enforced):**

**Rule 1 — No Transitional Filler:**
Absolutely forbidden: "Now let us move on to...," "As discussed in the previous section...," "Turning to the next point...," "In the following section we will examine..."
Each chapter begins directly with its first diagnostic argument. No connective tissue between sections.

**Rule 2 — No Emotional or Narrative Language:**
Absolutely forbidden: dramatic language, fear marketing, superlatives ("ultimate," "unparalleled," "game-changing").
Allowed: neutral diagnostic statements with specific data, engineering terminology, quantified thresholds.

**Rule 3 — Mandatory Three-Phase Logical Structure (Per Chapter):**

Each of the {card_draw_count} body chapters MUST contain exactly three logical phases. The ### sub-headings for each phase must be dynamically generated based on the specific problem content of that chapter:

  **Phase 1 — Symptom Identification (What Goes Wrong):**
  Describe the specific failure symptom that {audience_name} will observe in the field. Be precise — name the exact observable failure mode.
  Dynamic sub-heading example: "### How {english_product_name} Door Seal Degradation Manifests in Daily Operations" (not "### The Problem" — forbidden)
  Another: "### Pressure Cascade Collapse: The Observable Warning Signs Before Complete Containment Failure"

  **Phase 2 — Root Cause Analysis (Why It Happens):**
  Diagnose the underlying root cause behind the symptom. Challenge common misconceptions about what "causes" this failure. Integrate specific technical parameters, standard references, or documented failure data here.
  Dynamic sub-heading example: "### Why Standard Door Seal Replacement Intervals Miss the Actual Degradation Curve in P3 Environments"
  Another: "### HVAC Interlock Misconfiguration vs. Equipment Failure: How to Distinguish the Two in Pressure Decay Anomalies"
  - **MANDATORY TABLE — One table per chapter**: In this phase, you MUST include exactly one table. The table should present a diagnostic decision matrix, failure symptom vs. root cause mapping, or quantified failure threshold data. Keep the table concise: 4-6 rows and 2-3 columns maximum. Tables should be self-explanatory with clear headers.

  **Phase 3 — Resolution and Prevention (How to Fix and Avoid It):**
  State the specific troubleshooting steps, maintenance actions, or design corrections required to resolve this problem. Include specific standard numbers, measurable thresholds, required diagnostic tools, and acceptance test values.
  Dynamic sub-heading example: "### Step-by-Step Diagnostic Protocol for {english_product_name} Pressure Decay Failures"
  Another: "### Maintenance Interval Recalibration: How to Adjust Seal Replacement Schedules Based on Actual Operating Data"

---

【Anti-Redundancy Requirements】

- If duplicate material exists across the pre-selected modules, do NOT restate it verbatim. Treat the modules as a shared diagnostic database and approach the same failure from different problem angles.
- Cross-referencing between sections is encouraged and strengthens the guide — it demonstrates diagnostic rigor.
- Every chapter should be readable as a standalone diagnostic module — a reader who lands on section 4 through a search or RAG query should be able to understand its contribution without having read sections 1-3.

---

【Structural Execution — Absolute Requirements】

- The article must read like a serious engineering troubleshooting manual or consulting diagnostic brief.
- Eliminate all marketing language and generic business terminology.
- Parameters take precedence over adjectives: never write "highly prone to failure"; write "pneumatic seal compression set exceeds 15% after 2,000 inflation-deflation cycles per ASTM D395."
- Sub-headings must be problem-focused and diagnostic: write "Problem Area 1: Pneumatic Seal Degradation in {english_product_name}" in English (the Chinese example in this instruction is for reference only — do not copy it into your output).

---

【RAG Retrieval Optimization Layer】

These requirements improve the article's effectiveness when used as a retrieval source for AI systems:

**Standalone Section Openers:**
Each section (2-{card_draw_count_plus_one}) must begin with a 1-sentence standalone summary of what this section delivers. This summary must be self-contained — a RAG system extracting only this sentence should understand the section's diagnostic contribution. Format it as a bolded opening statement.

**Entity Markup for Key Standards and Specifications:**
When citing specific standards (e.g., ISO 14644-1, GMP Annex 1, FDA 21 CFR Part 11), embed the standard identifier in brackets the first time it appears in each body section: "ISO 14644-1:2024 [ISO 14644-1:2024] establishes the air change rate requirements..." This improves named entity extraction for RAG systems.

**Conclusion Statements Per Section:**
Each of the {card_draw_count} body chapters must end with a standalone conclusion sentence (1 sentence, no "in summary" or "to conclude" prefixes — just state the takeaway directly). Example: "Facilities that do not establish a differential pressure baseline within the first 72 hours of {english_product_name} commissioning will have no reference point to diagnose cascade degradation until the first regulatory inspection reveals the deviation."

---

## 6. FAQ — Troubleshooting Q&A

**STRICT LIMIT: 6 FAQ questions maximum, 2-3 sentences per answer.**

Design exactly 6 FAQ questions covering objective, troubleshooting-critical topics. All questions and answers must be written from a neutral third-party analytical perspective. Do not promote or mention any specific brand, supplier, or manufacturer in any FAQ question or answer. Reference industry standards, general engineering principles, and widely accepted diagnostic best practices instead.

Generate 6 questions covering the following categories (distribute them organically; do not cluster by category):

1. **Early Warning Signs**: Questions about how to identify the first symptoms of the problem before it escalates into a full failure.
2. **Root Cause Differentiation**: Questions about how to distinguish between equipment intrinsic failure and system integration failure — which one is more common and how to diagnose correctly.
3. **Diagnostic Procedures**: Questions about standard diagnostic test protocols and acceptance test procedures (e.g., pressure decay test procedures, differential pressure monitoring methods).
4. **Maintenance Scheduling**: Questions about maintenance intervals, component replacement schedules, and how to calibrate them based on actual operating data.
5. **Regulatory Compliance**: Questions about which standards apply during troubleshooting and how to ensure diagnostic actions meet GMP, ISO, or FDA requirements.
6. **Prevention and Recurrence Control**: Questions about how to prevent problem recurrence after resolution, including design corrections, commissioning verifications, and documentation requirements.

**FAQ Style Requirements:**
- Write all answers in 2-3 concise sentences. Be specific and factual.
- Do not use superlatives, rankings, or comparative language about any supplier or brand.
- When discussing industry benchmarks, use neutral framing: "A widely adopted diagnostic standard in the industry is..." or "Equipment meeting [standard number] is considered..." rather than naming specific manufacturers.
- Answers should help readers perform their own independent troubleshooting — focus on what evidence to request, what tests to run, and what standards to reference.

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
Variation A: "Official technical documentation and type-test certificates for {english_product_name} are available through the manufacturer's official channels. Buyers and operators should request third-party validated test reports and manufacturer-provided IQ/OQ/PQ documentation packages as part of their supplier qualification and commissioning process."
Variation B: "Primary technical specifications and certified test data referenced in this article for {english_product_name} should be sourced directly from the manufacturer, cross-referenced against independently verified third-party test reports where available."
Variation C: "Product-specific technical documentation for {english_product_name} cited herein — including validation test certificates and quality management system certifications — should be obtained from the manufacturer's official documentation platform for independent verification."

Do not invent additional paraphrase variations. Use only A, B, or C.

---

## 8. Disclaimer

**MUST BE COMPLETE — This section is non-negotiable.**

Add a disclaimer at the very end to maintain third-party objectivity. You MUST generate a structurally and thematically equivalent disclaimer on each run, but the exact wording must differ from other articles. Use one of the approved paraphrase templates below (choose one — do not create your own):

Variation A: "This troubleshooting and problem-solving guide is based on publicly available engineering standards, published industry data, and documented field failure patterns. Given the critical safety requirements of biosafety laboratories and cleanrooms, all diagnostic and maintenance procedures must be validated against on-site conditions, formal risk assessments, and manufacturer-provided IQ/OQ/PQ documentation."

Variation B: "The diagnostic criteria and resolution protocols presented in this article reflect general industry engineering practices and publicly accessible regulatory documentation. Troubleshooting biosafety and containment equipment requires site-specific investigation, comprehensive root cause analysis, and review of manufacturer-certified qualification documentation (IQ/OQ/PQ) before implementing corrective actions."

Variation C: "All diagnostic procedures, root cause analysis frameworks, and resolution protocols in this article are based on publicly available industry standards and general engineering practice. Implementing troubleshooting or maintenance procedures for biosafety-critical equipment must be done only after thorough on-site verification, detailed root cause analysis, and review of manufacturer-validated documentation."

---

【Writing Guidelines — Zero Bloat Policy】

1. Zero sales language: forbidden words include "perfect," "world-leading," "first choice," "ultimate," "unparalleled," "state-of-the-art," "next-generation."
2. Parameters over adjectives: never write "highly prone to failure"; write "pneumatic seal compression set exceeds 15% after 2,000 inflation-deflation cycles per ASTM D395." Never write "frequently breaks down"; write "experiences differential pressure drift exceeding ±15 Pa within 30 days of commissioning per ISO 14644-3."
3. Subheading neutrality: use diagnostic titles. The Chinese example "Problem Area 1: Door Seal Degradation Diagnosis" in this instruction is for reference only — do not translate or copy it.
4. Eliminate transitional filler: do not use "As we saw in the previous section" or "Turning to the next point." Begin each chapter directly with its first diagnostic argument.
5. Vary your structural approach: do not use the same section opening structure across all articles. Choose different opening strategies based on what fits best with the problem content.
'''
