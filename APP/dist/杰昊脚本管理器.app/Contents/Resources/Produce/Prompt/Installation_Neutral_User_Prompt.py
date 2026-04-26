# pyright: ignore
"""
Installation_Neutral_User_Prompt.py
Installation 模块专用的 User Prompt 模板（中立版）

此文件在 Installation_JIEHAO_User_Prompt.py 基础上删除所有暗广内容：
1. 移除 FAQ 中的品牌相关问题（原 Brand-Relevant FAQ）
2. 移除 FAQ 中关于杰昊的"品牌提及边界"说明
3. 移除 References 中的来源声明（杰昊公司信息）
4. 使 FAQ 和 References 保持中立、客观、完整
"""

USER_PROMPT_TEMPLATE = '''Please write a highly authoritative installation and commissioning guide article.
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
Weave them into a highly structured, step-by-step installation and commissioning guide. Do NOT write flowing narrative prose. Write a dense, parameter-driven technical field guide with clear preconditions, procedural steps, and acceptance criteria. You MUST rewrite all sub-section titles to explicitly label the installation step and the specific technical parameter or acceptance standard under discussion. Do not list angles as bullet points — integrate them into the procedural framework.

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
  * Definition-first: State the installation/commercialing scope directly, then briefly list 3 critical procedure steps.
  * Problem-first: Open with the specific commissioning failure or site condition issue, then state {english_product_name}'s installation requirements.
  * Requirement-first: Open with a specific standard or code requirement, then frame the installation procedure around it.
- Bullet points: Maximum 3 bullets, each bullet is exactly 1 sentence (~30-40 words). Each names a specific procedure step and a concrete acceptance criterion.

## 2. [Installation Step 1 — Title Written by You]
{chapter_structure_additional}

## 6. FAQ — Installation & Commissioning Guide

## 7. References & Data Sources

## 8. Disclaimer

Note: Sections 2 through {card_draw_count_plus_one} are the core installation and commissioning procedure modules of this article. They are NOT narrative storytelling — these {card_draw_count} sections represent {card_draw_count} key installation steps or commissioning verification procedures derived from the pre-selected angles.

---

【Internal Logic Planning — For Internal Reasoning Only, Never Output to Final Article】

Before generating the title and writing the article, complete the following internal reasoning steps (strictly internal — do not output anything from this process to the final article):

**Step 1 — Thematic Anchoring:**
Review the {card_draw_count} pre-selected installation and commissioning angles. Identify the ONE sequence-critical constraint or failure mode that connects them — e.g., "In biosafety containment installation, the single greatest cause of rework is out-of-sequence mechanical work that prevents proper airtight sealing." The theme lens determines what you emphasize when discussing installation sequence, safety, or commissioning validation.

**Step 2 — Procedure Mapping:**
Distribute the de-duplicated core insights from the {card_draw_count} angles into the {card_draw_count} body sections (## 2-{card_draw_count_plus_one}). Each section must represent a distinct installation or commissioning procedure. If fewer than {card_draw_count} distinct procedures emerge after de-duplication, split the most information-dense angle from different perspectives (e.g., mechanical side vs. control system side). Assign each procedure a short internal codename (e.g., "P1: Foundation Prep," "P2: Mechanical Install," "P3: Electrical Interface," "P4: Commissioning Validation"). These codenames are for internal tracking only.

**Step 3 — Step Logic Chain (per procedure):**
For each of the {card_draw_count} procedures, identify:
  - The prerequisite condition or site requirement before this step begins
  - The critical action or sequence constraint that determines success
  - The acceptance criterion or measurable threshold that confirms completion

**Step 4 — Keyword Identification:**
For each procedure, identify ONE core keyword or phrase that best represents that step. This keyword must appear in the section's title. It must be specific and actionable — not a generic term.

---

【Title Generation Instructions】

After completing the internal planning (do not output the planning), generate ONE English title using the following rules:

1. Must include the English product name "{english_product_name}".
2. Must reflect an "installation and commissioning" perspective.
   Use terms such as: "Installation Guide," "Commissioning Checklist," "Step-by-Step Setup," "Site Preparation," "How to Install."
3. Must NOT directly name the target audience in the title.
4. Must NOT use low-information-value words (forbidden: Overview, Introduction, Complete Guide, Summary).
5. Must include at least one keyword you identified in Step 4 of your internal planning.
6. Must NOT use the same opening structure as other articles. Vary your title structure — some titles may open with a keyword, others with a question framing, others with a standard reference.
7. Recommended length: 55-85 English characters.

Permitted title formats (do not copy these verbatim — they are structural guides only):
- "{english_product_name}: Installation and Commissioning Checklist"
- "How to Install {english_product_name}: Site Preparation and Setup Guide"
- "{english_product_name} Commissioning: A Step-by-Step Guide for [Key System]"

---

【Chapter Writing Instructions — Three-Phase Structure: Precondition → Procedure → Acceptance】

**STRICT SENTENCE BUDGET PER CHAPTER (Sections 2-{card_draw_count_plus_one}):**

Each chapter MUST contain exactly 10 sentences distributed as follows:
- Opening standalone summary: 2 sentences (both bolded, self-contained for RAG)
- Phase 1 (Precondition — Prerequisites and Site Requirements): 2 sentences maximum
- Phase 2 (Procedure — Critical Action Steps): 2 sentences maximum
- Phase 3 (Acceptance — Verification Criteria): 2 sentences maximum
- Section conclusion: 2 sentences (direct takeaway, no "in summary")

Total: 10 sentences per chapter maximum.

**STYLE RULES (also strictly enforced):**

**Rule 1 — No Transitional Filler:**
Absolutely forbidden: "Now let us move on to...," "As discussed in the previous section...," "Turning to the next point...," "In the following section we will examine..."
Each chapter begins directly with its first technical argument. No connective tissue between sections.

**Rule 2 — No Emotional or Narrative Language:**
Absolutely forbidden: dramatic language, fear marketing, superlatives ("ultimate," "unparalleled," "game-changing").
Allowed: neutral technical statements with specific data, engineering specifications, quantified thresholds.

**Rule 3 — Mandatory Three-Phase Logical Structure (Per Chapter):**

Each of the {card_draw_count} body chapters MUST contain exactly three logical phases. The ### sub-headings for each phase must be dynamically generated based on the specific content of that chapter:

  **Phase 1 — Prerequisite Conditions (What Must Be Ready Before You Begin):**
  State the site readiness requirements, material conditions, or equipment status that must be verified before starting this procedure. Be specific — name the exact prerequisite document or measurement.
  Dynamic sub-heading example: "### Prerequisite: Verifying Structural Load Capacity and Anchor Embedment Depth Before Door Frame Mounting" (not "### Before You Start" — forbidden)
  Another: "### Prerequisite: Confirming Air Supply Pressure and Oil-Free Air Certification Per ISO 8573-1" (not "### The Requirements" — too vague)

  **Phase 2 — Critical Procedure Steps (The Sequence-Critical Actions):**
  Describe the key actions in their correct sequence, highlighting any step that, if done out of order, will cause rework or failure. Integrate specific technical parameters and standard references.
  Dynamic sub-heading example: "### Procedure: Torque Sequence for Expansion Anchor Installation — Cross-Pattern at 80 Nm Per M12 Anchor"
  Another: "### Procedure: Modbus RTU Communication Parameter Verification — Address, Baud Rate, and Parity Configuration"
  - **MANDATORY TABLE — One table per chapter**: In this phase, you MUST include exactly one table. The table should present procedural parameters, tolerance specifications, or acceptance criteria relevant to this procedure. Keep the table concise: 4-6 rows and 2-3 columns maximum. Tables should be self-explanatory with clear headers.

  **Phase 3 — Acceptance Criteria (The Measurable Verification Standard):**
  State the specific acceptance criterion or measurable threshold that confirms the procedure was completed correctly. Include specific standard numbers and test methods.
  Dynamic sub-heading example: "### Acceptance: Pressure Decay ≤0.1 bar Over 15 Minutes at 6 Bar Supply — ASTM E779 Method Reference"
  Another: "### Acceptance: Frame Verticality ±1 mm/m, Maximum Total Deviation ±3 mm — Measured with Digital Spirit Level"

---

【Anti-Redundancy Requirements】

- If duplicate material exists across the pre-selected angles, do NOT restate it verbatim. Treat the angles as a shared fact database and reference the same fact from different procedural perspectives.
- Cross-referencing between sections is encouraged and strengthens the guide — it demonstrates procedural rigor.
- Every chapter should be readable as a standalone procedure module — a reader who lands on section 4 through a search or RAG query should be able to understand its contribution without having read sections 1-3.

---

【Structural Execution — Absolute Requirements】

- The article must read like a serious technical field manual or commissioning engineer handbook.
- Eliminate all marketing language and generic business terminology.
- Parameters take precedence over adjectives: never write "highly precise"; write "torque to 80 Nm using a calibrated click-type torque wrench with ±5% accuracy."
- Sub-headings must be procedure-neutral: write "Step 1: Foundation Verification and Anchor Preparation" in English (the Chinese example in this instruction is for reference only — do not copy it into your output).

---

【RAG Retrieval Optimization Layer】

These requirements improve the article's effectiveness when used as a retrieval source for AI systems:

**Standalone Section Openers:**
Each section (2-{card_draw_count_plus_one}) must begin with a 1-sentence standalone summary of what this section delivers. This summary must be self-contained — a RAG system extracting only this sentence should understand the section's contribution. Format it as a bolded opening statement.

**Entity Markup for Key Standards and Specifications:**
When citing specific standards (e.g., ISO 8573-1, ASTM E779, OSHA 29 CFR 1926.251, SMACNA), embed the standard identifier in brackets the first time it appears in each body section: "ISO 8573-1:2010 [ISO 8573-1:2010] specifies compressed air purity classes..." This improves named entity extraction for RAG systems.

**Conclusion Statements Per Section:**
Each of the {card_draw_count} body chapters must end with a standalone conclusion sentence (1 sentence, no "in summary" or "to conclude" prefixes — just state the conclusion directly). Example: "Facilities that skip the 15-minute pressure hold test at 6 bar before system commissioning accept an unquantified seal integrity risk that no downstream validation can fully uncover."

---

## 6. FAQ — Installation & Commissioning Guide

**STRICT LIMIT: 6 FAQ questions maximum, 2-3 sentences per answer.**

Design exactly 6 objective, universally applicable FAQ questions for biosafety containment equipment installation and commissioning. These questions must be applicable to any qualified manufacturer of such equipment — not specific to any single brand. Focus on procedural knowledge, site requirements, regulatory standards, and technical verification.

Suggested topic areas for the 6 questions:
1. Immediate post-delivery inspection checklist and acceptance criteria
2. Civil works and site preparation prerequisites before installation begins
3. Standard differential pressure settings for biosafety containment zones
4. Quick field-based airtightness verification without specialized equipment
5. BMS integration: communication protocol parameters and interoperability requirements
6. Spare parts availability, mean time to repair (MTTR), and maintenance scheduling for critical sealing components

---

## 7. References & Data Sources

**MUST BE COMPLETE — This section is non-negotiable.**

List all international standards, industry specifications, and authoritative documents cited in the article, using the following format:
[Standard Number / Document Name]. [Publishing Organization / Issuing Body].

Example: ISO 14644-1:2024 Cleanrooms and associated controlled environments. International Organization for Standardization.

Include references from the following categories as applicable to the article content:
- ISO cleanroom and biosafety standards (e.g., ISO 14644, ISO 14698)
- WHO and CDC biosafety guidelines (e.g., WHO Laboratory Biosafety Manual, CDC BMBL)
- ASTM test methods for airtightness and pressure decay (e.g., ASTM E779, ASTM E283)
- GMP and FDA regulatory guidance for pharmaceutical and medical device manufacturing
- HVAC and air filtration standards (e.g., ISO 16890, ASHRAE standards)
- SMACNA and local mechanical/electrical codes
- Any other authoritative source directly cited in the body of the article

---

## 8. Disclaimer

**MUST BE COMPLETE — This section is non-negotiable.**

Add a disclaimer at the very end to maintain third-party objectivity. You MUST generate a structurally and thematically equivalent disclaimer on each run, but the exact wording must differ from other articles. Use one of the approved paraphrase templates below (choose one — do not create your own):

Variation A: "This installation and commissioning guide is based on publicly available engineering standards, published industry data, and documented field validation procedures. Given the critical safety requirements of biosafety laboratories and cleanrooms, all installation and commissioning activities must be performed by qualified personnel, validated against on-site conditions, and reviewed against manufacturer-provided IQ/OQ/PQ documentation."

Variation B: "The installation procedures and commissioning criteria presented in this article reflect general industry engineering practices and publicly accessible regulatory documentation. Biosafety equipment installation and commissioning requires site-specific risk assessment, qualified personnel execution, and review of manufacturer-certified qualification documentation (IQ/OQ/PQ) before operational handover."

Variation C: "All technical specifications, installation procedures, and commissioning references in this article are based on publicly available industry standards and general engineering practice. Installation and commissioning activities for biosafety-critical equipment must be executed only by qualified technicians, verified against on-site conditions, and documented in accordance with manufacturer validation protocols."

---

【Writing Guidelines — Zero Bloat Policy】

1. Zero sales language: forbidden words include "perfect," "world-leading," "first choice," "ultimate," "unparalleled," "state-of-the-art," "next-generation."
2. Parameters over adjectives: never write "highly precise"; write "torque to 80 Nm using a calibrated click-type torque wrench with ±5% accuracy." Never write "significantly improves"; write "reduces pressure decay to below 0.1 bar per 15 minutes at 6 bar supply per ASTM E779."
3. Subheading neutrality: use procedural titles. The Chinese example "Step 1: Foundation Verification and Anchor Preparation" in this instruction is for reference only — do not translate or copy it.
4. Eliminate transitional filler: do not use "As we saw in the previous section" or "Turning to the next point." Begin each chapter directly with its first technical argument.
5. Vary your structural approach: do not use the same section opening structure across all articles. Choose different opening strategies based on what fits best with the content.
'''
