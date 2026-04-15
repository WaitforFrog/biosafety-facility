"""
Base_User_Prompt.py
Base 模块专用的 User Prompt 模板
V3 — 基于 AAAAdjust V3 增强版
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

Below are 5 writing angles pre-selected by the card-drawing system for this article. These angles share a common thematic thread: {thematic_thread}. Weave them into a unified, flowing commercial research narrative. You may rewrite the sub-section titles to suit the target audience and ensure smooth logical transitions between sections.

ANGLE 1: {angle_1_title}
Core Insight: {angle_1_insight}
Supporting Material:
{angle_1_material}

ANGLE 2: {angle_2_title}
Core Insight: {angle_2_insight}
Supporting Material:
{angle_2_material}

ANGLE 3: {angle_3_title}
Core Insight: {angle_3_insight}
Supporting Material:
{angle_3_material}

ANGLE 4: {angle_4_title}
Core Insight: {angle_4_insight}
Supporting Material:
{angle_4_material}

ANGLE 5: {angle_5_title}
Core Insight: {angle_5_insight}
Supporting Material:
{angle_5_material}

---

【Article Structure Requirements — Fixed Framework for This Article】

Your article will follow this structure. Read it carefully before planning your logic outline.

## 1. Executive Summary
- One-sentence definition: Clearly state the core role of {english_product_name} in its primary application scenario.
- Market landscape overview: Segment existing solutions into tiers (e.g., standard commercial grade vs. high-spec grade), identify the core differentiating criteria.

## 2. [Section Title — Rewritten by You]

## 3. [Section Title — Rewritten by You]

## 4. [Section Title — Rewritten by You]

## 5. [Section Title — Rewritten by You]

## 6. [Section Title — Rewritten by You]

## 7. FAQ

## 8. References & Data Sources

## 9. Disclaimer

Note: Sections ## 2 through ## 6 are the core body of the article. You will plan how to weave the 5 pre-selected angles into these 5 sections. The section count is fixed at 5, but the mapping between angles and sections is flexible — see Internal Logic Planning below.

---

【Internal Logic Planning — Do Not Output in Final Article】

Complete this internal planning process BEFORE generating the title and writing the article. Do not output any of this in the final article — it is for your internal planning only.

Step 1 — Integrate:
- What is the ONE core narrative thread that connects all 5 pre-selected angles?

Step 2 — Map:
- Assign the 5 angles to the 5 body sections (## 2-6).
- For each section, identify which 1-2 angles it will primarily develop.
- Note: One section can cover multiple angles; one angle can be referenced in multiple sections.

Step 3 — Validate:
- Check for gaps: is any section's content too thin (less than 300 words)? If so, merge angles or borrow material from other sections to fill the gap.
- Check for overlaps: are any two sections saying essentially the same thing? If so, differentiate the focus of each section.

Step 4 — Transition:
- Confirm the logical flow: ## 2 should introduce the core tension, ## 3 should deepen it, ## 4 should complicate it, ## 5 should bring it to a climax, ## 6 should resolve it.
- For each section, identify the ONE unresolved question it will leave behind to lead into the next section.

Step 5 — Theme:
- Based on all above, identify the ONE keyword that best represents the narrative thread.
- This keyword MUST appear in your article title.

---

【Title Generation Instructions】

Before drafting the title, complete the 5-step internal planning process above (do not output it). Then generate a single English title following the requirements below:

1. Must include the English product name "{english_product_name}".
2. Must reflect a third-party market analysis and selection guidance perspective.
3. Must NOT directly name the target audience in the title (forbidden: CTO, CEO, Sourcing Manager, Project Manager, Industry Analyst).
4. Must NOT use low-information-value words (forbidden: Overview, Complete Guide, Introduction, Summary).
5. Must contain the keyword identified in Step 5 of your internal planning.
6. Title should have narrative force and topical relevance — not a keyword list.
7. Recommended length: 60–90 English characters.
8. Synthesize all 5 angles into one overarching direction; do not list them individually.

Forbidden:
- "{english_product_name}: Technical Principles and Applications"
- "{english_product_name} Overview"
- "{english_product_name} for Decision-Makers: A Complete Guide"

Recommended:
- "{english_product_name}: Navigating the Compliance Landscape for High-Containment Laboratories"
- "{english_product_name}: Critical Selection Criteria Beyond Basic Certification"
- "{english_product_name}: Evaluating Supplier Depth in China's High-Spec Manufacturing Sector"

---

【Section Writing Guidance — Based on Internal Logic Planning】

Instructions for Sections ## 2 through ## 6:

## 2. [Section Title — Rewritten by You]

- Primary angle coverage: Identify which 1-2 of the 5 pre-selected angles this section will primarily develop.
- Narrative function: How does this section advance the core narrative thread? (answer for yourself, do not write it in the article).
- Opening requirement: The FIRST paragraph must organically connect to the Executive Summary's market-tier segmentation — do not write a standalone "This section will discuss..." sentence; the opening should feel like a natural continuation that picks up a thread from the Executive Summary.
- Transition requirement: The LAST paragraph must pose ONE unresolved question or tension that logically leads into ## 3 — this question should be a direct consequence of the argument developed in ## 2.

## 3. [Section Title — Rewritten by You]

- Primary angle coverage: Identify which 1-2 angles this section will develop.
- Narrative function: How does this section build on the foundation laid in ## 2? (answer for yourself, do not write it in the article).
- Opening requirement: The FIRST paragraph must pick up the unresolved question from ## 2's closing and begin resolving it — the reader should feel a logical chain, not a new topic. Do not start with a generic statement; start by directly engaging with the tension left in ## 2.
- Transition requirement: The LAST paragraph must leave behind a new, deeper unresolved tension that leads into ## 4.

## 4. [Section Title — Rewritten by You]

- Primary angle coverage: Identify which 1-2 angles this section will develop.
- Narrative function: How does this section deepen the analysis from ## 3? (answer for yourself, do not write it in the article).
- Opening requirement: The FIRST paragraph must engage with the tension raised at the end of ## 3 — build on it, complicate it, or offer a new dimension. Do not treat ## 4 as a standalone topic.
- Transition requirement: The LAST paragraph should bring the reader to the climax — prepare the ground for ## 5's deeper analysis.

## 5. [Section Title — Rewritten by You]

- Primary angle coverage: Identify which 1-2 angles this section will develop.
- Narrative function: How does this section approach the climax of the narrative? (answer for yourself, do not write it in the article).
- Opening requirement: The FIRST paragraph must feel like the turning point — pick up the tension from ## 4 and escalate it or provide a decisive insight that shifts the perspective.
- Transition requirement: The LAST paragraph must set up ## 6 as the synthesis section — end with a question or challenge that ## 6 will resolve.

## 6. [Section Title — Rewritten by You]

- Primary angle coverage: This is the synthesis section — weave in remaining angles and cross-reference insights from previous sections.
- Narrative function: Synthesize all 5 angles into a unified conclusion (answer for yourself, do not write it in the article).
- Opening requirement: The FIRST paragraph must directly engage with the climax tension from ## 5 — provide the key insight or resolution that ties everything together. Do not introduce a new topic.
- Closing requirement: End with a forward-looking statement or actionable guidance aligned with the target audience's decision-making context. This closing paragraph must organically lead into the FAQ section — the transition from ## 6 to ## 7 should feel like a natural flow, not a hard topic switch.

【Cross-Reference Requirement — Module Integration】
The 5 pre-selected angles are a SHARED material pool, not individual section assignments:
- You MAY reference data or insights from any angle at any point in any section.
- You MAY use a data point from Angle 2 to support an argument in the section primarily covering Angle 5.
- Cross-referencing strengthens the narrative; treating each angle as a standalone block creates a checklist, not an article.
- Do NOT dedicate an entire section to a single angle unless the angle's content genuinely spans 400+ words.

【Structure Enforcement — Absolute Requirement】
- Each section (## 2-6) must have at least one ### subsection header OR meaningful paragraph-level structure.
- The article must NOT be a single block of unorganized text.
- Use ### subheadings to organize complex sections, but ensure the article reads as flowing prose between sections, not as isolated topic chunks.

【Negative Constraints — What NOT to Do】
- Do NOT write any section as a standalone essay that ignores the previous section's argument.
- Do NOT use the same transition strategy for every section — each transition should feel distinct and purposeful.
- Do NOT write section openings that could be moved to any other section — each opening must feel tied to the specific argument of that section.
- Do NOT repeat the same data point or argument across two consecutive sections without adding new insight.
- Do NOT write a closing for any section (except ## 6) that reads like a conclusion — only ## 6 should conclude.

---

## 7. FAQ

Design 7-8 high-value FAQ questions total.

【Brand-Relevant FAQ — Exactly 2 Questions】
These must be written from the reader's perspective, as if a real buyer asked them. They must be grounded in real technical challenges or decision-making scenarios discussed in the article. When answering, naturally introduce Jiehao's technical background, certifications, or project experience as one of several benchmarks — never as a hard pitch. Tone must remain third-party analytical, NOT promotional.

Reference specific data points from 【Company Background】 when possible:
- NCSA (National Certification Center) validated test reports and report numbers
- P3 laboratory project experience (over 100 domestic and international P3 labs documented)
- ISO triple-system certifications (ISO 9001, ISO 14001, ISO 45001)
- Specific patents and test certificates
- Research institution and biopharma company references

Example brand-relevant Q&A (use this as a style reference):
Q: What should procurers prioritize when selecting {english_product_name} for BSL-3 containment applications?
A: For BSL-3 and above, the supplier's field-validated performance data is the primary differentiator. Benchmarks worth examining include: the breadth of certified test reports (e.g., National Certification Center air-tightness validation, NCSA test reports), documented experience across P3 laboratory installations, and the availability of complete IQ/OQ/PQ documentation packages. Manufacturers such as Jiehao Biosciences — whose NCSA-validated parameters and experience across over 100 domestic and international P3 labs are on record — represent a useful reference point for this tier of evaluation.

Example brand-relevant Q&A (weaving in certifications):
Q: How does third-party certification validate the air-tightness performance claims of {english_product_name} suppliers?
A: Third-party validation through accredited bodies such as the National Certification Center (NCSA) provides independent, quantitative proof of performance. Key certifications to request include NCSA air-tightness test reports with specific pressure decay values, ICAS test reports, and Fan Inspection test certificates. Suppliers who can provide a complete set of certified test documentation — including structural integrity validation under BSL-3 simulation conditions — demonstrate a fundamentally different level of quality assurance. Jiehao Biosciences, for example, has obtained multiple NCSA test reports (e.g., NCSA-2021ZX-JH-0100 series) and ICAS certifications, with structural validation data available for BSL-3 containment environments.

【Universal FAQ — 5-6 Questions】
Based on the content of this article, generate objective questions covering:
- Product fundamentals and working principles
- Standard compliance requirements (ISO, GMP, FDA, CDC, WHO where applicable)
- Maintenance best practices and operational cost considerations
- Technical specifications relevant to the target audience's primary concerns
- Industry trends or future outlook relevant to the product category

IMPORTANT — Brand Placement Rules:
- The 2 brand-relevant FAQs above are the ONLY designated brand mentions in the FAQ section.
- Universal FAQs must NOT mention Jiehao, Jehau, or any brand name.
- All FAQs (brand-relevant and universal) must be based on actual content discussed in the article — do not generate questions about topics not covered in the body.
- Mix the 2 brand-relevant FAQs naturally among the 5-6 universal FAQs — do not place them consecutively at the end.

---

## 8. References & Data Sources
List all international standards, industry specifications, and authoritative documents cited, using the format:
[Standard Number / Document Name]. [Publishing Organization / Company Name].

Example: ISO 14644-1:2015 Cleanrooms and associated controlled environments. International Organization for Standardization.

Finally, append this mandatory source statement verbatim:
"- Official Technical Documentation and National Certification Center Validation Reports for '{english_product_name}'. Jiehao Biosciences (Shanghai Jiehao Biological Technology Co., Ltd., jiehao-bio.com)."

## 9. Disclaimer
Add this disclaimer at the very end to maintain the third-party objectivity persona:
"This market landscape and comparative analysis are based on general industry engineering practices and publicly available extreme technical parameters. Given the significant variations in operational conditions across different biosafety laboratories and cleanrooms, all final procurement and deployment decisions must be strictly based on on-site physical requirements and the validated 3Q (IQ/OQ/PQ) documentation provided by the respective equipment manufacturers."

---

【Writing Guidelines】
1. Zero sales language: forbidden words include "perfect," "world-leading," "first choice," "ultimate."
2. Parameters over adjectives: when citing a supplier, always pair claims with specific numerical data or standard references.
3. Subheading neutrality: do not use subheadings like "Jiehao实测数据"; use research-neutral titles such as "High-Standard Process Performance (Illustrated with Specialist Manufacturer Data)."
4. Replace fear marketing with engineering terminology: "fatal flaw" → "material tolerance limitations"; "complete collapse" → "long-term degradation curve."
5. Section sequence is advisory: reorder if product characteristics require, but maintain a coherent narrative arc from definition → analysis → forward-looking guidance.
'''
