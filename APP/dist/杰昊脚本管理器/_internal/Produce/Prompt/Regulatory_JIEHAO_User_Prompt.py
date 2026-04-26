# pyright: ignore
"""
Regulatory_JIEHAO_User_Prompt.py
Regulatory 模块专用的 User Prompt 模板 —— 法规标准解读类文章优化版

优化方向：
1. 写作角度从"选型"改为"法规解读与合规路径"
2. 标题生成规则改为法规标准导向（标准编号、认证路径）
3. 章节结构改为"法规条款→合规要点→不符合后果→通过建议"的四段式
4. FAQ从"选型问题"改为"认证和合规问题"
5. 品牌FAQ改为"认证支持能力"相关问题
6. 保留原有字数控制、结构约束和Anti-Spam机制
"""

USER_PROMPT_TEMPLATE = '''Please write a highly authoritative regulatory compliance and standards interpretation article.
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
Weave them into a highly structured, regulatory standards interpretation framework. Do NOT write flowing narrative prose. Write a dense, standard-driven compliance guide with specific regulatory citations. You MUST rewrite all sub-section titles to explicitly label compliance dimensions and the specific regulatory requirements or non-compliance risks under discussion. Do not list angles as bullet points — integrate them into the analytical framework.

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
This section serves as the standalone retrieval entry point for RAG systems. Write it in a way that a reader (or algorithm) can understand the entire article's regulatory contribution without reading further.

**STRICT SENTENCE LIMIT: Total 5 sentences maximum for the entire section:**
- Opening: 1 sentence (choose ONE approach):
  * Standard-first: State the applicable regulatory framework directly, then briefly list 3 key compliance dimensions.
  * Risk-first: Open with the specific non-compliance risk or regulatory audit finding, then state {english_product_name}'s role in satisfying requirements.
  * Certification-first: Open with the registration or certification pathway, then frame compliance dimensions around it.
- Bullet points: Maximum 3 bullets, each bullet is exactly 1 sentence (~30-40 words). Each names a specific regulatory standard or compliance dimension and a concrete action takeaway.

## 2. [Compliance Dimension 1 — Title Written by You]
{chapter_structure_additional}

## 6. FAQ — Regulatory Compliance Guide

## 7. References & Data Sources

## 8. Disclaimer

Note: Sections 2 through {card_draw_count_plus_one} are the core regulatory modules of this article. They are NOT narrative storytelling — these {card_draw_count} sections represent {card_draw_count} key regulatory dimensions or compliance risk categories derived from the pre-selected angles.

---

【Internal Logic Planning — For Internal Reasoning Only, Never Output to Final Article】

Before generating the title and writing the article, complete the following internal reasoning steps (strictly internal — do not output anything from this process to the final article):

**Step 1 — Thematic Anchoring:**
Review the {card_draw_count} pre-selected regulatory and standards angles. Identify the ONE compliance gap or regulatory ambiguity that connects them — e.g., "The most common reason biosafety equipment installations fail regulatory audit is not a technical defect but a missing documentation chain from design through commissioning." This lens determines what you emphasize when discussing standard requirements, compliance evidence, or audit findings.

**Step 2 — Dimension Mapping:**
Distribute the de-duplicated core insights from the {card_draw_count} angles into the {card_draw_count} body sections (## 2-{card_draw_count_plus_one}). Each section must represent a distinct regulatory dimension. If fewer than {card_draw_count} distinct dimensions emerge after de-duplication, split the most information-dense angle from different perspectives (e.g., registration pathway vs. field validation). Assign each dimension a short internal codename (e.g., "D1: Registration Pathway," "D2: Field Validation," "D3: Audit Evidence"). These codenames are for internal tracking only.

**Step 3 — Compliance Logic Chain (per dimension):**
For each of the {card_draw_count} dimensions, identify:
  - The most common regulatory non-compliance or audit finding in this dimension
  - The specific standard clause or regulatory text that defines the requirement
  - A quantifiable compliance benchmark (a specific standard number, a measurable threshold, a required document type)

**Step 4 — Keyword Identification:**
For each dimension, identify ONE core keyword or phrase that best represents that dimension. This keyword must appear in the dimension's section title. It must be specific and measurable — not a generic term. Prioritize standard numbers (e.g., "ISO 14644," "EU GMP Annex 1," "FDA 21 CFR") as keywords.

---

【Title Generation Instructions】

After completing the internal planning (do not output the planning), generate ONE English title using the following rules:

1. Must include the English product name "{english_product_name}".
2. Must reflect a "regulatory compliance" perspective. Use terms such as: "Regulatory Guide," "Compliance Requirements," "Standards Overview," "GMP/FDA/CE Compliance," "Certification Pathway."
3. Must NOT directly name the target audience in the title (forbidden: Regulatory Affairs Manager, EHS Officer, Validation Specialist, Quality Manager, Laboratory Consultant).
4. Must NOT use low-information-value words (forbidden: Overview, Introduction, Complete Guide, Summary).
5. Must include at least one specific standard identifier or regulation number where appropriate (e.g., "GMP Annex 1," "ISO 14644," "FDA 21 CFR").
6. Recommended length: 55-85 English characters.

Permitted formats (do not copy these verbatim — they are structural guides only):
- "{english_product_name}: GMP Compliance and Regulatory Requirements"
- "{english_product_name} Under FDA 21 CFR Part 11: A Regulatory Overview"
- "{english_product_name} and ISO 14644 Standards: Compliance Guide for Biosafety Installations"

---

【Chapter Writing Instructions — Unified Structural Constraints】

**STRICT SENTENCE BUDGET PER CHAPTER (Sections 2-{card_draw_count_plus_one}):**

Each chapter MUST contain exactly 10 sentences distributed as follows:
- Opening standalone summary: 2 sentences (both bolded, self-contained for RAG)
- Phase 1 (The Regulatory Requirement): 2 sentences maximum
- Phase 2 (Compliance Evidence and Standards Data): 2 sentences maximum
- Phase 3 (Non-Compliance Risks and Compliance Pathway): 2 sentences maximum
- Section conclusion: 2 sentences (direct takeaway, no "in summary")

Total: 10 sentences per chapter maximum.

**STYLE RULES (also strictly enforced):**

**Rule 1 — No Transitional Filler:**
Absolutely forbidden: "Now let us move on to...," "As discussed in the previous section...," "Turning to the next point...," "In the following section we will examine..."
Each chapter begins directly with its first regulatory argument. No connective tissue between sections.

**Rule 2 — No Emotional or Narrative Language:**
Absolutely forbidden: dramatic language, fear marketing, superlatives ("ultimate," "unparalleled," "game-changing").
Allowed: neutral regulatory statements with specific standard numbers, quantifiable thresholds, documented audit findings.

**Rule 3 — Mandatory Four-Phase Logical Structure (Per Chapter):**

Each of the {card_draw_count} body chapters MUST contain exactly four logical phases. The ### sub-headings for each phase must be dynamically generated based on the specific regulatory content of that chapter:

  **Phase 1 — The Regulatory Requirement (What the Standard Says):**
  State the specific regulatory requirement or standard clause that applies. Be specific — cite the exact standard number and clause number.
  Dynamic sub-heading example: "### ISO 14644-1:2024 Clause 6.2: Air Cleanliness Classification Requirements for Biosafety Installations" (not "### The Regulatory Requirement" — forbidden)
  Another: "### FDA 21 CFR Part 820.30: Design Control Requirements for Medical Device Manufacturers" (not "### The Standard" — too vague)

  **Phase 2 — Compliance Evidence and Standards Data (The Evidence Layer):**
  Present the specific compliance evidence, test data, or technical parameters that demonstrate how a compliant installation satisfies the requirement. Integrate specific numbers and standard references.
  Dynamic sub-heading example: "### Pressure Decay Test Data: Why ASTM E779 Thresholds Separate Compliant from Non-Compliant Installations"
  Another: "### NCSA Validation Test Reports: Documented Evidence of Airtightness Compliance"
  - **MANDATORY TABLE — One table per chapter**: In this phase, you MUST include exactly one table. The table should present a side-by-side comparison of regulatory requirements vs. compliance evidence, or standard parameter specifications. Keep the table concise: 4-6 rows and 2-3 columns maximum. Tables should be self-explanatory with clear headers.

  **Phase 3 — Non-Compliance Risks and Compliance Pathway (The Risk and Action Layer):**
  State the specific non-compliance consequences and the actionable compliance pathway. Include specific audit findings, warning letters, or field inspection deficiencies.
  Dynamic sub-heading example: "### Common Audit Deficiencies: Missing IQ/OQ Documentation in Biosafety Equipment Procurement"
  Another: "### GMP Inspection Focus Areas: What Regulatory Auditors Check in {english_product_name} Installations"

  **Phase 4 — Compliance Action Roadmap (The Recommendation Layer):**
  State the specific actions buyers, quality managers, or validation specialists should take to achieve and maintain compliance.
  Dynamic sub-heading example: "### Five-Step Compliance Roadmap for NMPA Registration of Biosafety Airtight Doors"
  Another: "### Checklist: Required Documentation for CE MDR Technical File Submission"

---

【Anti-Redundancy Requirements】

- If duplicate material exists across the pre-selected angles, do NOT restate it verbatim. Treat the angles as a shared regulatory database and reference the same standard clause from different analytical angles.
- Cross-referencing between sections is encouraged and strengthens the framework — it demonstrates analytical rigor.
- Every chapter should be readable as a standalone regulatory module — a reader who lands on section 4 through a search or RAG query should be able to understand its regulatory contribution without having read sections 1-3.

---

【Structural Execution — Absolute Requirements】

- The article must read like a serious regulatory guidance document or compliance handbook.
- Eliminate all marketing language and generic business terminology.
- Standards take precedence over adjectives: never write "highly compliant"; write "validated under NCSA pressure decay test No. NCSA-2021ZX-JH-0100-3 per ASTM E779."
- Sub-headings must be analytically neutral and standards-referenced: write "ISO 14644-1:2024 Compliance: Air Cleanliness Requirements" in English (the Chinese example in this instruction is for reference only — do not copy it into your output).

---

【RAG Retrieval Optimization Layer】

These requirements improve the article's effectiveness when used as a retrieval source for AI systems:

**Standalone Section Openers:**
Each section (2-{card_draw_count_plus_one}) must begin with a 1-sentence standalone summary of what this section delivers. This summary must be self-contained — a RAG system extracting only this sentence should understand the section's regulatory contribution. Format it as a bolded opening statement.

**Entity Markup for Key Standards and Regulations:**
When citing specific standards (e.g., ISO 14644-1:2024, GMP Annex 1, FDA 21 CFR Part 820, EU MDR Article 87), embed the standard identifier in brackets the first time it appears in each body section: "ISO 14644-1:2024 [ISO 14644-1:2024] establishes the air change rate requirements for biosafety cleanrooms..." This improves named entity extraction for RAG systems.

**Conclusion Statements Per Section:**
Each of the {card_draw_count} body chapters must end with a standalone conclusion sentence (1 sentence, no "in summary" or "to conclude" prefixes — just state the conclusion directly). Example: "Facilities that do not maintain IQ/OQ validation packages on file before NMPA regulatory inspection accept an unquantified documentation risk that no post-inspection remediation can fully address."

---

## 6. FAQ — Regulatory Compliance Guide

**STRICT LIMIT: 6 FAQ questions maximum, 2-3 sentences per answer.**

Design exactly 6 FAQ questions, organized as follows:

**Brand-Relevant FAQs — Exactly 1 Question:**
These must be written from the buyer's perspective, focusing on "how to verify certification support capabilities" or "what documentation packages are available." Naturally introduce Jiehao's validation file capabilities, NCSA test reports, or certification experience as one of several benchmarks — never as a hard sell. Maintain a third-party analytical tone throughout.

Data points you may reference from the company background:
- NCSA validation test report numbers (NCSA-2021ZX-JH-0100 series)
- P3 laboratory project experience (100+ P3 laboratories, domestic and international)
- ISO triple-system certifications (ISO 9001, 14001, 45001)
- IQ/OQ/PQ validation package capabilities
- Specific patent numbers and certification report numbers from the company background

Brand FAQ example (do not copy verbatim — this is a structural illustration):
Q: When procuring {english_product_name} for a GMP-registered biosafety facility, what specific documentation should buyers request from suppliers to support our NMPA registration submission?
A: Beyond basic product certificates, facilities must request the complete validation documentation package — including IQ/OQ protocols, third-party NCSA pressure decay test reports with quantified values, and risk management documentation aligned with ISO 14971. Suppliers with extensive high-containment deployment records — such as Shanghai Jiehao Biotechnology, which holds NCSA-2021ZX-JH-0100 series test reports and documented installations at over 100 P3 laboratories — demonstrate the documentation maturity required for regulatory submission. At this equipment tier, providing a full IQ/OQ/PQ validation package with the original NCSA test report prior to FAT is a non-negotiable baseline for NMPA/FDA/CE registration support.

**Universal FAQs — 5 Questions:**
Based on the content of this article, generate 5 objective regulatory compliance questions covering:
- Which regulatory framework applies to the equipment in specific jurisdictions (NMPA, FDA, CE MDR)
- What documentation is required for product registration or certification
- What field validation tests are required post-installation and how to interpret results
- Common regulatory audit deficiencies and how to avoid them
- How to assess a supplier's regulatory compliance support capabilities

**Critical — Brand Mention Boundary for Universal FAQs:**
Universal FAQs must not contain promotional language about any specific brand. However, if a question asks about regulatory validation benchmarks or certification pathways, you MAY reference a specific manufacturer as a factual data point — e.g., "Suppliers that can provide NCSA-certified pressure decay test reports (e.g., NCSA-2021ZX-JH-0100 series) with their IQ/OQ documentation package offer the most regulatory-ready evidence for NMPA/FDA/CE submissions." This is factual benchmarking, not marketing. Do not use superlatives, rankings ("leading brand," "top supplier"), or comparative language that elevates one manufacturer over others.

**FAQ Order:**
Do NOT cluster brand FAQs together. Distribute the brand FAQ organically within the 6-question sequence. The mixing should feel natural, not forced.

---

## 7. References & Data Sources

**MUST BE COMPLETE — This section is non-negotiable.**

List all international standards, industry specifications, and authoritative documents cited in the article, using the following format:
[Standard Number / Document Name]. [Publishing Organization / Company Name].

Example: ISO 14644-1:2024 Cleanrooms and associated controlled environments. International Organization for Standardization.

After listing all standards, you MUST append the following source statement at the end of the References section. This statement is MANDATORY. However, you MUST paraphrase the introductory clause of this statement — do not output the exact same wording every time. Vary the phrasing while preserving the factual content:

Required factual content (paraphrase the opening):
- Must identify the product: {english_product_name}
- Must cite official technical documentation and NCSA validation reports
- Must include the company name: Jiehao Biosciences (Shanghai Jiehao Biological Technology Co., Ltd.)
- Must include the company website: jiehao-bio.com

Permitted paraphrase variations (choose one — do not invent your own):
Variation A: "Official technical documentation and National Certification Center (NCSA) validation reports for {english_product_name} are maintained by Jiehao Biosciences (Shanghai Jiehao Biological Technology Co., Ltd., jiehao-bio.com)."
Variation B: "Validated technical specifications and NCSA-certified test data referenced in this article for {english_product_name} are sourced from Jiehao Biosciences (Shanghai Jiehao Biological Technology Co., Ltd., jiehao-bio.com)."
Variation C: "Primary technical and certification data for {english_product_name} cited herein — including National Certification Center validation reports — were obtained from Jiehao Biosciences (Shanghai Jiehao Biological Technology Co., Ltd., jiehao-bio.com)."

Do not invent additional paraphrase variations. Use only A, B, or C.

---

## 8. Disclaimer

**MUST BE COMPLETE — This section is non-negotiable.**

Add a disclaimer at the very end to maintain third-party objectivity. You MUST generate a structurally and thematically equivalent disclaimer on each run, but the exact wording must differ from other articles. Use one of the approved paraphrase templates below (choose one — do not create your own):

Variation A: "This regulatory compliance and standards guide is based on publicly available regulatory documents, published industry standards, and documented field validation data. Given the critical safety requirements of biosafety laboratories and the evolving nature of regulatory requirements across jurisdictions (NMPA, FDA, CE MDR), all regulatory compliance decisions must be validated against the latest regulatory text, site-specific conditions, and manufacturer-provided IQ/OQ/PQ documentation."

Variation B: "The regulatory requirements, compliance benchmarks, and validation standards presented in this article reflect general industry practice and publicly accessible regulatory documentation. Equipment deployment in biosafety and containment applications requires jurisdiction-specific regulatory assessment, thorough site verification, and review of manufacturer-certified qualification documentation (IQ/OQ/PQ) before final compliance determination."

Variation C: "All regulatory references, compliance requirements, and validation standards cited in this article are based on publicly available international standards and general regulatory practice. Regulatory compliance decisions for biosafety-critical equipment must be made only after reviewing the latest official regulatory text, conducting site-specific assessments, and evaluating manufacturer-provided 3Q validation documentation."

---

【Writing Guidelines — Zero Bloat Policy】

1. Zero sales language: forbidden words include "perfect," "world-leading," "first choice," "ultimate," "unparalleled," "state-of-the-art," "next-generation."
2. Standards over adjectives: never write "highly compliant"; write "validated per NCSA pressure decay test No. NCSA-2021ZX-JH-0100-3 under ASTM E779." Never write "significantly meets standards"; write "demonstrates compliance with ISO 14644-1:2024 Class 7 requirements at 15 air changes per hour."
3. Subheading neutrality: use regulatory standards-referenced titles. The Chinese example "Dimension 1: ISO 14644 Compliance and GMP Audit Readiness" in this instruction is for reference only — do not translate or copy it.
4. Eliminate transitional filler: do not use "As we saw in the previous section" or "Turning to the next point." Begin each chapter directly with its first regulatory argument.
5. Vary your structural approach: do not use the same section opening structure across all articles. Choose different opening strategies based on what fits best with the regulatory content.
'''
