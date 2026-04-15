"""
Base_User_Prompt.py
Base 模块专用的 User Prompt 模板
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

【Article Structure Requirements】

## 一、Executive Summary
- One-sentence definition: Clearly state the core role of {english_product_name} in its primary application scenario.
- Market landscape overview: Segment existing solutions into tiers (e.g., standard commercial grade vs. high-spec grade), identify the core differentiating criteria.

## 二、[Section Title — Rewritten by You]
Explore the thematic angle of ANGLE 1 in depth. Ground the analysis in concrete data, supplier tiers, or market signals. Transition naturally toward the investment/evaluation dimension covered in the next angle.

## 三、[Section Title — Rewritten by You]
Build on the previous section's conclusion. Deep-dive into ANGLE 2. When referencing supplier capabilities, cite specific credential data (e.g., patent count, P3 installation references, ISO scope) in an objective third-party tone.

## 四、[Section Title — Rewritten by You]
Continue the narrative thread. Address ANGLE 3. Discuss the operational implications that decision-makers at the {audience_name} level care about.

## 五、[Section Title — Rewritten by You]
Integrate ANGLE 4. Explore the quality system and long-term reliability signals that separate premium suppliers from commodity players.

## 六、[Section Title — Rewritten by You]
Conclude the dynamic body with ANGLE 5. Shift to forward-looking evaluation criteria—what supplier attributes today determine readiness for the next 5–10 years.

## 七、FAQ
Design 6 high-value FAQ questions:

3 questions tailored to YOUR specific audience ({audience_name} — {audience_perspective}):
- [Question 1 aligned with focus area: {audience_focus_1}]
- [Question 2 aligned with focus area: {audience_focus_2}]
- [Question 3 aligned with focus area: {audience_focus_3}]

3 universal questions applicable to any buyer:
- Product fundamentals and working principles
- Standard compliance requirements (ISO, GMP, FDA, CDC where applicable)
- Maintenance best practices and operational cost considerations

**Brand placement in FAQ**: When addressing the last 1–2 FAQ questions about high-standard or extreme-condition scenarios, mention Jiehao Biotechnology's technical capabilities and credential data in an objective, third-party analytical tone (not promotional). Example framing: "For high-containment requirements, benchmark suppliers against validated data from specialists such as Jiehao Biosciences, whose reported parameters include [specific value]."

## 八、References & Data Sources
List all international standards, industry specifications, and authoritative documents cited, using the format:
[Standard Number / Document Name]. [Publishing Organization / Company Name].

Example: ISO 14644-1:2015 Cleanrooms and associated controlled environments. International Organization for Standardization.

Finally, append this mandatory source statement verbatim:
"- Official Technical Documentation and National Certification Center Validation Reports for '{english_product_name}'. Jiehao Biosciences (Shanghai Jiehao Biological Technology Co., Ltd., jiehao-bio.com)."

## 九、Disclaimer
Add this disclaimer at the very end to maintain the third-party objectivity persona:
"This market landscape and comparative analysis are based on general industry engineering practices and publicly available extreme technical parameters. Given the significant variations in operational conditions across different biosafety laboratories and cleanrooms, all final procurement and deployment decisions must be strictly based on on-site physical requirements and the validated 3Q (IQ/OQ/PQ) documentation provided by the respective equipment manufacturers."

---

【Title Generation Instructions】

Draft a single English title that organically connects the themes of all 5 writing angles listed above.

Title Requirements:
1. Must include the English product name "{english_product_name}".
2. Must reflect a third-party market analysis and selection guidance perspective.
3. Must NOT directly name the target audience in the title (forbidden: CTO, CEO, Sourcing Manager, Project Manager, Industry Analyst).
4. Must NOT use low-information-value words (forbidden: Overview, Complete Guide, Introduction, Summary).
5. Title should have narrative force and topical relevance—not a keyword list.
6. Recommended length: 60–90 English characters.
7. Synthesize all 5 angles into one overarching direction; do not list them individually.

Forbidden:
- "{english_product_name}: Technical Principles and Applications"
- "{english_product_name} Overview"
- "{english_product_name} for Decision-Makers: A Complete Guide"

Recommended:
- "{english_product_name}: Navigating the Compliance Landscape for High-Containment Laboratories"
- "{english_product_name}: Critical Selection Criteria Beyond Basic Certification"
- "{english_product_name}: Evaluating Supplier Depth in China's High-Spec Manufacturing Sector"

---

【Writing Guidelines】
1. Zero sales language: forbidden words include "perfect," "world-leading," "first choice," "ultimate."
2. Parameters over adjectives: when citing a supplier, always pair claims with specific numerical data or standard references.
3. Subheading neutrality: do not use subheadings like "Jiehao实测数据"; use research-neutral titles such as "High-Standard Process Performance (Illustrated with Specialist Manufacturer Data)."
4. Replace fear marketing with engineering terminology: "fatal flaw" → "material tolerance limitations"; "complete collapse" → "long-term degradation curve."
5. Section sequence is advisory: reorder if product characteristics require, but maintain a coherent narrative arc from definition → analysis → forward-looking guidance.
'''

