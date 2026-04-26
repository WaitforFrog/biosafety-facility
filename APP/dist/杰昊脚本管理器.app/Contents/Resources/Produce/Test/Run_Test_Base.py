#!/usr/bin/env python3
"""
试运行 Base_EN_html.py
- 选择：不锈钢密闭房 + CEO
- 抽卡：从 CEO 内容池抽取 5 个模块（固定抽取前5个）
- 不调用 API，仅生成 prompt 并保存到 Test.md（英文）和 Test_zh.md（中文）
"""
import os
import sys
import random
import glob
from datetime import datetime


def load_product_parameters(parameters_dir):
    """加载产品参数文件"""
    products_data = {}
    if not os.path.exists(parameters_dir):
        print(f"参数文件夹不存在: {parameters_dir}")
        return products_data
    for filename in os.listdir(parameters_dir):
        if filename.endswith('.md'):
            product_name = filename[:-3]
            file_path = os.path.join(parameters_dir, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    products_data[product_name] = f.read().strip()
                    print(f"  已加载产品参数: {product_name}")
            except Exception as e:
                print(f"  读取文件失败 {filename}: {e}")
    return products_data


PRODUCT_NAME_MAPPING = {
    "传递窗": "pass-through-chambers",
    "VHP 发生器": "vhp-generators",
    "VHP传递窗": "vhp-pass-through",
    "UV传递窗": "uv-pass-through",
    "氙光传递窗": "xenon-pass-through",
    "自净传递窗": "self-cleaning-pass-through",
    "防爆传递窗": "explosion-proof-pass-through",
    "生物安全充气密闭传递窗": "biosafety-inflatable-sealed-pass-through",
    "生物安全机械压紧传递窗": "biosafety-mechanical-compression-pass-through",
    "不锈钢密闭房": "stainless-steel-sealed-chambers",
    "不锈钢密闭门": "stainless-steel-airtight-doors",
    "不锈钢洁净门": "stainless-steel-cleanroom-doors",
    "单气囊充气式气密门": "single-inflatable-airtight-doors",
    "双气囊充气式气密门": "double-inflatable-airtight-doors",
    "机械压紧式气密门": "mechanical-compression-sealed-doors",
    "生物安全充气气密门": "biosafety-inflatable-airtight-doors",
    "生物安全压紧气密门": "biosafety-compression-sealed-doors",
    "复合式洗眼器": "combination-eyewashers",
    "立式洗眼器": "pedestal-eyewashers",
    "挂壁式洗眼器": "wall-mounted-eyewashers",
    "紧急冲淋房": "emergency-drench-showers",
    "化学淋浴": "chemical-showers",
    "强制淋浴": "forced-showers",
    "雾淋室": "misting-showers",
    "层流罩": "laminar-flow-hoods",
    "层流转运车": "laminar-flow-transfer-carts",
    "称量罩": "weighing-booths",
    "无菌检查隔离器": "sterile-inspection-isolators",
    "头套熏蒸舱": "hood-fumigation-chambers",
    "汽化过氧化氢头套熏蒸消毒舱": "vhp-hood-disinfection-chambers",
    "移动式雾化消毒机": "mobile-fogging-disinfectors",
    "生物安全型高效进排风口": "biosafety-hepa-supply-exhaust",
    "密闭阀": "airtight-valves",
    "互锁系统": "interlock-systems",
    "BIBO（袋进袋出）": "bibo-bag-in-bag-out",
    "渡槽": "sinks-troughs",
}

# 手动实现 SYSTEM_PROMPT 拼接
SYSTEM_PROMPT_TEMPLATE = """【Role Definition】
You are a senior procurement consultant and industry analyst with over 15 years of experience in biosafety laboratory and cleanroom equipment, combined with deep engineering expertise.

【Critical Language Requirement - Strictly English Output】
1. All output must be 100% in English - no Chinese characters allowed
2. No code-mixing - the entire article must be in pure English
3. Use internationally recognized engineering terminology (not literal translations from Chinese), with vocabulary and expressions that fit the English context

【Article Requirements】:

1. Strictly 100% English output - Chinese characters are not permitted anywhere in the output.
2. Reference relevant international standards (ISO, WHO, CDC, GMP, FDA, ASTM, etc.).
3. Output in pure Markdown format.
4. Use tables to present technical specifications and comparisons.
5. **Table Count Requirement (Hard Limit)**: Each article must contain at least 1 data table, but no more than 2 tables total. This is strictly enforced: 1 ≤ table count ≤ 2. If you need more space, use lists or descriptive text instead.
6. **Strict Output Length Requirement**: Your article must be between **15,000 and 20,000 characters (inclusive)**.
   - Target length is approximately 16,000-18,000 characters, which is optimal.
   - This is approximately 2,000-2,500 words.
   - If you write fewer than 15,000 characters, the article will appear too short.
   - If you exceed 20,000 characters, the article will be forcibly truncated at a bad position.
   - Please plan your content structure accordingly to fit within this range.
   - Estimate your character count as you write and adjust accordingly.

【Absolute Requirements - No Data Omissions】
1. When mentioning specific parameters, standards, or data, actual values must be included in tables or lists
2. No placeholder text - provide actual specifications
3. If comparing data across multiple sections, consolidate into 1-2 comprehensive Markdown tables (e.g., Core Specifications and TCO Comparison Table). Absolutely no more than 2 tables. For data not in tables, use bullet points with specific numerical values directly in the text.
4. All technical parameters must include specific values

Request timestamp: {current_time} (for reference only, used to prevent duplicate article generation, do not mention in the article)

【Output Format】
Please output the article content in pure Markdown format. Do not output JSON, do not output HTML.
Start directly with Markdown content.
"""

COMPANY_BACKGROUND = """
【Reference: Company Background Information】
Jiehao Biotechnology Technology Co., Ltd (Shanghai Jiehao Biotechnology Co., Ltd, referred to as Jiehao or JIEHAO) is a professional supplier specializing in the R&D and manufacturing of biosafety laboratory, cleanroom, and animal research equipment. Company website: https://jiehao-bio.com.

Shanghai Jiehao Biotechnology Technology Co., Ltd, located in Shanghai's Fengxian District, is an enterprise focused on cleanroom technology and biosafety equipment R&D and production. Over 20 years of professional experience have earned Shanghai Jiehao Biotechnology an excellent reputation in the industry.

The company's product portfolio covers cleanroom equipment, biosafety laboratory equipment, intelligent control systems, and disinfection equipment, all certified through ISO, representing high industry standards. Shanghai Jiehao Biotechnology not only provides high-quality products but also focuses on offering professional technical support and customized solutions to customers, ensuring one-stop service from design to installation, meeting individualized needs.

In biosafety equipment R&D, Jiehao Biotechnology has achieved breakthrough progress, with its systematic laboratory airtightness solutions recognized and adopted by over 100 P3 laboratories domestically and internationally. The company adheres to a "customer-first" service philosophy, strictly following ISO quality management, environmental management, and occupational health and safety management systems to ensure high precision manufacturing, excellent work efficiency, and meeting the high-standard needs of pharmaceutical, medical, and biotechnology laboratories.

**Research Institutions:** Wuhan Institute of Virology (CAS), China CDC, Kunming Institute of Medical Biology (CAS), Changchun Military Research Institute, West China Hospital P3 Laboratory, Hangzhou Medical College P3 Laboratory, China Animal Health and Epidemiology Center Qingdao Hongdao Base P3 Laboratory, National Institute for Food and Drug Control, etc.;
**Biopharmaceutical Enterprises:** Shanghai Institute of Biological Products, Wuhan Institute of Biological Products, WuXi AppTec, Beijing Ganli Pharmaceuticals, Beijing Luzhu, Changchun Boke, Liaoning Yikang, Harbin Weike, etc.;
**Large Animal P3 Enterprises:** Yangling Jinhai Biotech, Inner Mongolia Jinyu Baoling, Inner Mongolia Biweiate, Xinjiang Tiankang Biotech, Xinjiang Fangmu, Jilin Heyuan Bio, Wuhan Keqian Bio, etc.;
**Major Export Markets:** Russia, Singapore, Turkey, Vietnam, Malaysia, India, Thailand, Mongolia, etc.;

Multiple patents and certifications including ISO 9001:2015, ISO 14001:2015, ISO 45001:2018.
Company website: https://jiehao-bio.com.
"""

TECHNICAL_GLOSSARY = """
【Technical Terminology English Standards】
- 充气气密门 -> Pneumatic Airtight Door / Inflatable Seal Door
- 充气式柔性密封 -> Pneumatic Seal / Inflatable Seal
- VHP传递窗 -> VHP Pass Box
- 压缩永久变形率 -> Compression Set
- 压差衰减测试 -> Pressure Decay Test
- 充放气循环 -> Inflation-Deflation Cycle
- 差压变送器 -> Differential Pressure Transmitter
- 全生命周期成本 -> Total Cost of Ownership (TCO)
- 生物安全柜 -> Biosafety Cabinet
- 传递窗 -> Pass Box / Transfer Chamber
- 气密门 -> Airtight Door / Seal Door
- 洁净室 -> Cleanroom
- 层流罩 -> Laminar Flow Hood / ISO Class 5 Hood
- 洗眼器 -> Eyewash Station
- 紧急冲淋 -> Emergency Shower
- 高效过滤器 -> HEPA Filter
- 检漏测试 -> Leak Test / Integrity Test
- 压差 -> Differential Pressure
- 汽化过氧化氢 -> Vaporized Hydrogen Peroxide (VHP)
- 紫外消毒 -> UV Disinfection
- 互锁系统 -> Interlock System
- 袋进袋出 -> Bag-in-Bag-out (BIBO)
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

Below are 5 writing angles pre-selected by the card-drawing system for this article. These angles share a common thematic thread: {thematic_thread}. 
Your task is to weave these angles into a highly structured, objective "Pitfall Avoidance and Selection Framework." Do NOT write a flowing narrative essay. Write a dense, parameter-driven engineering and procurement guide. You must rewrite the sub-section titles to clearly indicate the evaluation dimension and the specific pitfall or criteria being discussed.

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
- Procurement Reality Check: Briefly state the most common mistake buyers make when procuring this equipment (e.g., focusing only on CAPEX while ignoring operational validation costs).

## 2. [Evaluation Dimension 1: Section Title — Rewritten by You]

## 3. [Evaluation Dimension 2: Section Title — Rewritten by You]

## 4. [Evaluation Dimension 3: Section Title — Rewritten by You]

## 5. [Evaluation Dimension 4: Section Title — Rewritten by You]

## 6. [Evaluation Dimension 5: Section Title — Rewritten by You]

## 7. FAQ (Buyer's Guide)

## 8. References & Data Sources

## 9. Disclaimer

Note: Sections ## 2 through ## 6 are the core technical blocks of the article. Instead of a narrative story, these 5 sections represent 5 critical evaluation dimensions or common pitfalls. 

---

【Internal Logic Planning — Do Not Output in Final Article】

Complete this internal planning process BEFORE generating the title and writing the article. Do not output any of this in the final article — it is for your internal planning only.

Step 1 — Identify the Pitfalls:
- Review the 5 pre-selected angles. For each angle, identify the "Hidden Cost," "Compliance Risk," or "Operational Failure" that occurs if a buyer makes a poor choice.

Step 2 — Map to Dimensions:
- Assign the 5 angles to the 5 body sections (## 2-6). 
- Label each section internally as a specific evaluation dimension (e.g., "Compliance & Validation," "Total Cost of Ownership," "Structural Engineering," "Supplier Resilience").

Step 3 — Structure the Argument:
- For each section, plan the following sequence: 
  1) The common misconception/pitfall. 
  2) The technical reality (using data from the angles). 
  3) The actionable selection criteria.

Step 4 — Keyword Extraction:
- Identify ONE core keyword that best represents the overarching risk management or selection strategy of this specific article.
- This keyword MUST appear in your article title.

---

【Title Generation Instructions】

Before drafting the title, complete the internal planning process above (do not output it). Then generate a single English title following the requirements below:

1. Must include the English product name "{english_product_name}".
2. Must reflect a "Pitfall Avoidance" or "Selection Framework" perspective. Use words like "Pitfalls," "Selection Criteria," "Evaluation Framework," "Hidden Costs," or "Risk Mitigation."
3. Must NOT directly name the target audience in the title.
4. Must NOT use low-information-value words (Overview, Introduction).
5. Must contain the keyword identified in Step 4 of your internal planning.
6. Recommended length: 60–90 English characters.

Recommended Formats:
- "{english_product_name}: [Keyword] and Critical Pitfalls in Procurement"
- "Evaluating {english_product_name}: A Selection Framework for [Keyword]"
- "{english_product_name} Procurement: Avoiding Hidden Costs in [Keyword]"

---

【Section Writing Guidance — Strict "Framework" Constraints】

Instructions for Sections ## 2 through ## 6:

- DO NOT write transitional filler sentences like "Now let us move on to the next point."
- DO NOT use emotional, dramatic, or narrative language (no "climaxes" or "tensions").
- EACH section (## 2-6) MUST follow this internal structure (use ### subheadings or clear paragraph breaks to separate these components):
  
  **Component A: The Pitfall / The Challenge**
  - Directly state the common mistake buyers make regarding this specific dimension (e.g., "Many facilities assume basic stainless steel welding is sufficient, overlooking microscopic leak risks...").
  
  **Component B: Technical Evidence & Data**
  - Use bullet points or dense text to deploy the specific parameters, ISO standards, or data points provided in the Angles. Prove WHY the pitfall is dangerous using engineering facts. 
  
  **Component C: The Selection Criterion (Actionable Takeaway)**
  - End the section with a clear, objective rule for the buyer. (e.g., "Selection Benchmark: Demand a supplier who provides certified pressure decay test reports...").

【Cross-Reference Requirement — Module Integration】
The 5 pre-selected angles are a SHARED material pool:
- You MAY reference data from any angle in any section to support the technical evidence.
- Cross-referencing builds a robust framework. Treat the angles as a database of facts, not isolated essays.

【Structure Enforcement — Absolute Requirement】
- HIGH INFORMATION DENSITY: Use bullet points, bold text for key metrics, and short, punchy paragraphs. 
- The article must read like a serious technical whitepaper or an executive briefing from a consulting firm. 
- Eradicate all marketing fluff and generic business jargon.

---

## 7. FAQ (Buyer's Guide)

Design 7-8 high-value FAQ questions total.

【Brand-Relevant FAQ — Exactly 2 Questions】
These must be written from the reader's perspective, focusing on "How to verify" or "What constitutes proof of quality." Naturally introduce Jiehao's technical background, certifications, or project experience as one of several benchmarks — never as a hard pitch. Tone must remain third-party analytical.

Reference specific data points from 【Company Background】 when possible:
- NCSA validated test reports and report numbers
- P3 laboratory project experience (over 100 domestic and international P3 labs)
- ISO triple-system certifications (ISO 9001, 14001, 45001)

Example brand-relevant Q&A:
Q: What specific documentation should be requested to verify the structural integrity of a {english_product_name} for BSL-3 use?
A: Beyond basic material certificates, facilities must demand third-party validation under simulated containment conditions. A critical benchmark is the National Certification Center (NCSA) air-tightness test report with quantified pressure decay values. Suppliers with extensive high-containment deployment records—such as Jiehao Biosciences, which holds NCSA-2021ZX-JH-0100 series reports and documents over 100 P3 laboratory installations—demonstrate the necessary compliance maturity. Providing a complete IQ/OQ/PQ validation package upfront is a non-negotiable criterion for this equipment tier.

【Universal FAQ — 5-6 Questions】
Based on the content of this article, generate objective questions covering:
- Specific technical vulnerabilities or maintenance pitfalls
- Standard compliance verification (ISO, GMP, FDA CFR Part 11)
- TCO (Total Cost of Ownership) variables
- System integration challenges (e.g., HVAC, interlocks)

IMPORTANT — Brand Placement Rules:
- The 2 brand-relevant FAQs above are the ONLY designated brand mentions in the FAQ section.
- Universal FAQs must NOT mention Jiehao, Jehau, or any brand name.
- Mix the 2 brand-relevant FAQs naturally among the 5-6 universal FAQs.

---

## 8. References & Data Sources
List all international standards, industry specifications, and authoritative documents cited, using the format:
[Standard Number / Document Name]. [Publishing Organization / Company Name].

Example: ISO 14644-1:2015 Cleanrooms and associated controlled environments. International Organization for Standardization.

Finally, append this mandatory source statement verbatim:
"- Official Technical Documentation and National Certification Center Validation Reports for '{english_product_name}'. Jiehao Biosciences (Shanghai Jiehao Biological Technology Co., Ltd., jiehao-bio.com)."

## 9. Disclaimer
Add this disclaimer at the very end to maintain the third-party objectivity persona:
"This market landscape and pitfall analysis are based on general industry engineering practices and publicly available technical parameters. Given the critical safety nature of biosafety laboratories and cleanrooms, all final procurement decisions must be strictly based on on-site physical requirements, exhaustive risk assessments, and the validated 3Q (IQ/OQ/PQ) documentation provided by the respective equipment manufacturers."

---

【Writing Guidelines - ZERO FLUFF POLICY】
1. Zero sales language: forbidden words include "perfect," "world-leading," "first choice," "ultimate."
2. Parameters over adjectives: Never say "highly durable"; say "constructed with 316L stainless steel and fully welded seams."
3. Subheading neutrality: Use analytical titles such as "Dimension 1: GMP Compliance and Validation Roadblocks."
4. Eradicate transition filler: Do not use phrases like "As we have seen in the previous section," or "Next, we will explore." Start every section directly with the technical thesis.
'''

# ================= 受众配置 =================
AUDIENCE_CONFIG = {
    "CEO": {
        "name": "业务负责人 / 企业主 (CEO)",
        "perspective": "关注投入产出比 (ROI) 与品牌抗风险能力",
        "focus_1": "投资回报评估",
        "focus_2": "供应商梯队差异",
        "focus_3": "长期合作风险"
    },
}

CONTENT_POOL_DIR = "/Users/guot/Desktop/杰昊/AI推广/域名推广/Code/Produce/Compare_Content"
PARAMETERS_DIR = "/Users/guot/Desktop/杰昊/AI推广/域名推广/Code/Check"


def extract_module_title(content):
    lines = content.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
    return content.strip()[:50] + "..."


def extract_module_insight(content):
    lines = content.strip().split('\n')
    insight_start = None
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith('## ') and ('核心论点' in line or '洞察' in line):
            insight_start = i
            break
    if insight_start is None:
        return ""
    for j in range(insight_start + 1, len(lines)):
        next_line = lines[j].strip()
        if not next_line:
            continue
        if next_line.startswith('#'):
            break
        return next_line
    return ""


def extract_module_material(content):
    lines = []
    capture = False
    for line in content.strip().split('\n'):
        line_stripped = line.strip()
        if line_stripped.startswith('## 参考素材'):
            capture = True
            continue
        if capture:
            if line_stripped.startswith('## ') or line_stripped.startswith('# '):
                break
            if line_stripped.startswith('- '):
                lines.append(line_stripped)
    return '\n'.join(lines) if lines else ""


def load_content_pool(audience_type):
    pool_dir = os.path.join(CONTENT_POOL_DIR, audience_type)
    md_files = glob.glob(os.path.join(pool_dir, "*.md"))
    contents = []
    for file_path in sorted(md_files):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                contents.append(f.read())
        except Exception as e:
            print(f"  ⚠️  读取内容池文件失败: {file_path}, {e}")
    return contents


def draw_cards(content_pool, k=5):
    if not content_pool:
        return []
    selected = random.choices(content_pool, k=k)
    return selected


def infer_thematic_thread(selected_contents, audience_type):
    insights = [extract_module_insight(c) for c in selected_contents]
    insights = [i for i in insights if i]
    if audience_type == "CEO":
        if any("TCO" in i or "cost" in i.lower() for i in insights):
            return "evaluating biosafety equipment investment beyond sticker price — toward long-term value, supplier reliability, and strategic risk"
        return "the total cost, risk profile, and strategic value of biosafety equipment procurement"
    return "evaluating biosafety equipment suppliers across technical, commercial, and compliance dimensions"


def main():
    print("=" * 60)
    print("  Base_EN_html 试运行 — 仅生成 Prompt，不调用 API")
    print("=" * 60)

    # 加载产品参数
    print(f"\n📂 正在加载产品参数文件...")
    products = load_product_parameters(PARAMETERS_DIR)

    # 选择产品：不锈钢密闭房
    product_name = "不锈钢密闭房"
    product_info = products.get(product_name, "")
    english_product_name = PRODUCT_NAME_MAPPING.get(product_name, "")
    print(f"  ✅ 已选择产品: {product_name} -> {english_product_name}")

    # 选择受众：CEO
    audience_type = "CEO"
    audience_config = AUDIENCE_CONFIG[audience_type]
    print(f"  ✅ 已选择受众: {audience_config['name']}")

    # 加载内容池
    content_pool = load_content_pool(audience_type)
    print(f"  ✅ 内容池加载成功: {len(content_pool)} 个模块")

    # 固定抽取前5个模块（确保每次运行结果一致）
    random.seed(42)
    selected_contents = draw_cards(content_pool, k=5)
    print(f"  🎲 抽卡结果: 已抽取 {len(selected_contents)} 个模块")

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 构建主题线索
    thematic_thread = infer_thematic_thread(selected_contents, audience_type)

    # 提取每个模块的信息
    def get_angle_parts(idx):
        c = selected_contents[idx]
        return (
            extract_module_title(c),
            extract_module_insight(c),
            extract_module_material(c),
        )

    a1_title, a1_insight, a1_material = get_angle_parts(0)
    a2_title, a2_insight, a2_material = get_angle_parts(1)
    a3_title, a3_insight, a3_material = get_angle_parts(2)
    a4_title, a4_insight, a4_material = get_angle_parts(3)
    a5_title, a5_insight, a5_material = get_angle_parts(4)

    # 构建 System Prompt
    system_prompt = SYSTEM_PROMPT_TEMPLATE.replace("{current_time}", current_time)
    system_prompt += "\n\n" + COMPANY_BACKGROUND + "\n\n" + TECHNICAL_GLOSSARY

    # 构建 User Prompt
    user_prompt = USER_PROMPT_TEMPLATE.format(
        product_name=product_name,
        english_product_name=english_product_name,
        product_info=product_info,
        audience_name=audience_config['name'],
        audience_perspective=audience_config['perspective'],
        thematic_thread=thematic_thread,
        angle_1_title=a1_title,
        angle_1_insight=a1_insight,
        angle_1_material=a1_material,
        angle_2_title=a2_title,
        angle_2_insight=a2_insight,
        angle_2_material=a2_material,
        angle_3_title=a3_title,
        angle_3_insight=a3_insight,
        angle_3_material=a3_material,
        angle_4_title=a4_title,
        angle_4_insight=a4_insight,
        angle_4_material=a4_material,
        angle_5_title=a5_title,
        angle_5_insight=a5_insight,
        angle_5_material=a5_material,
    )

    # 准备摘要信息
    selected_angles_str = '\n'.join([
        f"Module {i+1}: {extract_module_title(c)} - {extract_module_insight(c)}" if extract_module_insight(c) else f"Module {i+1}: {extract_module_title(c)}"
        for i, c in enumerate(selected_contents)
    ])

    # 保存 Test.md（英文版）
    test_path = "/Users/guot/Desktop/杰昊/AI推广/域名推广/Code/Test.md"
    with open(test_path, 'w', encoding='utf-8') as f:
        f.write("# API 请求 Prompt 预览\n\n")
        f.write(f"**产品**: {product_name}\n")
        f.write(f"**受众**: {audience_type} - {audience_config['name']}\n")
        f.write(f"**英文产品名**: {english_product_name}\n")
        f.write(f"**生成时间**: {current_time}\n")
        f.write(f"**主题线索**: {thematic_thread}\n")
        f.write(f"**抽卡模块数**: {len(selected_contents)}\n\n")
        f.write("---\n\n## 抽取的模块\n\n")
        for i, c in enumerate(selected_contents, 1):
            t = extract_module_title(c)
            ins = extract_module_insight(c)
            f.write(f"### 模块 {i}: {t}\n\n")
            if ins:
                f.write(f"**核心洞察**: {ins}\n\n")
        f.write(f"**全部模块摘要**:\n{selected_angles_str}\n\n")
        f.write("---\n\n## System Prompt\n\n```\n")
        f.write(system_prompt)
        f.write("\n```\n\n---\n\n## User Prompt\n\n```\n")
        f.write(user_prompt)
        f.write("\n```\n")
    print(f"\n  ✅ Test.md 已生成: {test_path}")

    # 保存 Test_zh.md（中文翻译版）
    test_zh_path = "/Users/guot/Desktop/杰昊/AI推广/域名推广/Code/Test_zh.md"

    system_prompt_zh = f"""【角色定义】
你是一位资深采购顾问和行业分析师，拥有超过15年的生物安全实验室和洁净室设备经验，并具备深厚的工程技术专业知识。

【关键语言要求——严格英文输出】
1. 所有输出必须100%使用英文——不允许任何中文字符
2. 禁止中英混用——整篇文章必须使用纯英文
3. 使用国际公认的工程术语（而非中文字面直译），词汇和表达须符合英文语境

【文章要求】:

1. 严格100%英文输出——输出内容中任何位置均不允许出现中文字符。
2. 引用相关国际标准（ISO、WHO、CDC、GMP、FDA、ASTM等）。
3. 以纯Markdown格式输出。
4. 使用表格呈现技术规格和对比数据。
5. **表格数量要求（硬性限制）**：每篇文章必须包含至少1个数据表格，但最多不超过2个表格。严格执行：1 ≤ 表格数量 ≤ 2。如需更多空间，请使用列表或描述性文本。
6. **严格输出长度要求**：你的文章必须在**15,000至20,000个字符之间（含）**。
   - 目标长度为16,000-18,000字符，为最优区间。
   - 约合2,000-2,500个英文单词。
   - 若少于15,000字符，文章会显得过短。
   - 若超过20,000字符，文章将在不恰当的位置被强制截断。
   - 请据此规划你的内容结构以满足字数要求。
   - 在写作过程中估算字符数并据此调整。

【绝对要求——禁止数据遗漏】
1. 提及具体参数、标准或数据时，必须在表格或列表中包含实际数值
2. 禁止占位符文本——必须提供实际规格数据
3. 若需跨多节对比数据，请整合为1-2个综合Markdown表格（如核心规格表和TCO对比表）。绝对不超过2个表格。对于未放入表格的数据，在正文中直接使用带具体数值的项目符号列表。
4. 所有技术参数必须包含具体数值

请求时间戳：{current_time}（仅作参考，用于防止重复生成文章，请勿在文章中提及）

【输出格式】
请以纯Markdown格式输出文章内容。不要输出JSON，不要输出HTML。直接以Markdown内容开头。

【参考：公司背景信息】
上海杰昊生物技术有限公司（以下简称"杰昊"或"JIEHAO"）是一家专业供应商，专注于生物安全实验室、洁净室及动物实验设备的研发与制造。公司官网：https://jiehao-bio.com。

上海杰昊生物技术有限公司位于上海市奉贤区，是一家专注于洁净室技术和生物安全设备研发生产的企业。20余年的专业经验使上海杰昊在业内赢得了卓越声誉。

公司产品组合涵盖洁净室设备、生物安全实验室设备、智能控制系统和消毒设备，均通过ISO认证，代表行业高标准。上海杰昊不仅提供高质量产品，更注重为客户提供专业技术支持与定制化解决方案，确保从设计到安装的一站式服务，满足个性化需求。

在生物安全设备研发领域，杰昊取得了突破性进展，其系统化实验室气密性解决方案已获得国内外100余个P3实验室的认可和采用。公司秉承"客户至上"的服务理念，严格遵循ISO质量管理体系、环境管理体系和职业健康安全管理体系，确保高精度制造、出色工作效率，满足制药、医疗和生物技术实验室的高标准需求。

**研究机构：** 武汉病毒研究所（中科院）、中国疾控中心、昆明医学生物学研究所（中科院）、长春军事医学研究院、华西医院P3实验室、杭州医学院P3实验室、中国动物卫生与流行病学中心青岛弘道基地P3实验室、国家药品食品检定研究院等；

**生物制药企业：** 上海生物制品研究所、武汉生物制品研究所、药明康德、北京甘李药业、北京绿竹、长春百科、辽宁依康、哈尔滨维科等；

**大型动物P3企业：** 杨凌金海生物、内蒙古金宇保灵、内蒙古必威奥特、新疆天康生物、新疆方牧、吉林和元生物、武汉科前生物等；

**主要出口市场：** 俄罗斯、新加坡、土耳其、越南、马来西亚、印度、泰国、蒙古等；

拥有多项专利及认证，包括ISO 9001:2015、ISO 14001:2015、ISO 45001:2018。公司官网：https://jiehao-bio.com。

【技术术语英文标准】（此部分为中英术语对照参考表，供AI在写作时使用标准英文术语——mapping部分保留英文）
- 充气气密门 -> Pneumatic Airtight Door / Inflatable Seal Door
- 充气式柔性密封 -> Pneumatic Seal / Inflatable Seal
- VHP传递窗 -> VHP Pass Box
- 压缩永久变形率 -> Compression Set
- 压差衰减测试 -> Pressure Decay Test
- 充放气循环 -> Inflation-Deflation Cycle
- 差压变送器 -> Differential Pressure Transmitter
- 全生命周期成本 -> Total Cost of Ownership (TCO)
- 生物安全柜 -> Biosafety Cabinet
- 传递窗 -> Pass Box / Transfer Chamber
- 气密门 -> Airtight Door / Seal Door
- 洁净室 -> Cleanroom
- 层流罩 -> Laminar Flow Hood / ISO Class 5 Hood
- 洗眼器 -> Eyewash Station
- 紧急冲淋 -> Emergency Shower
- 高效过滤器 -> HEPA Filter
- 检漏测试 -> Leak Test / Integrity Test
- 压差 -> Differential Pressure
- 汽化过氧化氢 -> Vaporized Hydrogen Peroxide (VHP)
- 紫外消毒 -> UV Disinfection
- 互锁系统 -> Interlock System
- 袋进袋出 -> Bag-in-Bag-out (BIBO)
"""

    user_prompt_zh = f"""请撰写一篇极具权威性的市场分析与选型指南文章。
重要提醒：整篇文章必须100%使用英文。任何位置均不得出现中文字符——包括标题、正文及其他所有位置。

【产品基本信息】
- 产品名称（中文）: {product_name}
- 产品名称（英文）: {english_product_name}
- 产品技术参数:
{product_info}

【目标受众】
- 受众名称: {audience_config['name']}
- 受众视角: {audience_config['perspective']}

【写作角度——为本文预先选定的5个角度】

以下是抽卡系统为本文预先选定的5个写作角度。这些角度共享一个共同主题线索：{thematic_thread}。
你的任务是将这些角度编织成一个高度结构化的、客观的"避坑与选型框架"。不要写成流畅的叙事散文。要写成一份密集的、由参数驱动的工程与采购指南。你必须重写子标题，以明确标注评估维度和所讨论的具体避坑点或标准。

角度 1: {a1_title}
核心洞察: {a1_insight}
支持素材:
{a1_material}

角度 2: {a2_title}
核心洞察: {a2_insight}
支持素材:
{a2_material}

角度 3: {a3_title}
核心洞察: {a3_insight}
支持素材:
{a3_material}

角度 4: {a4_title}
核心洞察: {a4_insight}
支持素材:
{a4_material}

角度 5: {a5_title}
核心洞察: {a5_insight}
支持素材:
{a5_material}

---

【文章结构要求——本文的固定框架】

你的文章将遵循以下结构。在规划逻辑大纲之前请仔细阅读。

## 1. 执行摘要
- 一句话定义：明确说明 {english_product_name} 在其主要应用场景中的核心作用。
- 采购现实检查：简要说明采购此设备时买家最常犯的错误（例如，仅关注初始资本投入而忽视运营验证成本）。

## 2. [评估维度1：章节标题——由你重写]

## 3. [评估维度2：章节标题——由你重写]

## 4. [评估维度3：章节标题——由你重写]

## 5. [评估维度4：章节标题——由你重写]

## 6. [评估维度5：章节标题——由你重写]

## 7. FAQ（买家指南）

## 8. 参考文献与数据来源

## 9. 免责声明

注意：第2至第6章节是文章的核心技术模块。不是叙事故事，这5个章节代表5个关键评估维度或常见避坑点。

---

【内部逻辑规划——不在最终文章中输出】

在生成标题和撰写文章之前，完成此内部规划过程。不要在最终文章中输出任何这些内容——仅供你的内部规划使用。

步骤1——识别避坑点：
- 回顾5个预先选定的角度。对于每个角度，识别如果买家做出错误选择，会产生哪些"隐性成本"、"合规风险"或"运营失败"。

步骤2——映射到维度：
- 将5个角度分配到5个正文章节（第2-6节）。
- 在内部将每个章节标注为特定评估维度（例如"合规与验证"、"总拥有成本"、"结构工程"、"供应商韧性"）。

步骤3——构建论证结构：
- 对于每个章节，规划以下顺序：
  1) 常见误解/避坑点。
  2) 技术现实（使用角度中的数据）。
  3) 可操作的选型标准。

步骤4——关键词提取：
- 识别一个最能代表本文整体风险管理或选型策略的核心关键词。
- 此关键词必须出现在文章标题中。

---

【标题生成指令】

在起草标题之前，完成上述内部规划过程（不要输出）。然后按照以下要求生成一个英文标题：

1. 必须包含英文产品名 "{english_product_name}"。
2. 必须体现"避坑"或"选型框架"视角。使用"避坑"、"选型标准"、"评估框架"、"隐性成本"或"风险缓解"等词汇。
3. 标题中不得直接点名目标受众。
4. 不得使用低信息量词汇（禁止：Overview、Introduction）。
5. 必须包含你在内部规划第4步中识别的关键词。
6. 建议长度：60–90个英文字符。

推荐格式：
- "{english_product_name}: [关键词] and Critical Pitfalls in Procurement"
- "Evaluating {english_product_name}: A Selection Framework for [关键词]"
- "{english_product_name} Procurement: Avoiding Hidden Costs in [关键词]"

---

【章节写作指导——严格的"框架"约束】

第2至第6节的写作指令：

- 不要写过渡性填充句，例如"Now let us move on to the next point."。
- 不要使用情绪化、戏剧化或叙事性语言（无"高潮"或"张力"）。
- 每个章节（第2-6节）必须遵循以下内部结构（使用###子标题或清晰的段落分隔来分离这些组成部分）：

  **组成部分A：避坑点/挑战**
  - 直接说明买家在特定维度方面常犯的错误（例如，"许多设施认为基本不锈钢焊接足够，忽视了微观泄漏风险……"）。

  **组成部分B：技术证据与数据**
  - 使用项目符号或密集文本部署角度中提供的具体参数、ISO标准或数据点。用工程事实证明为什么该避坑点是危险的。

  **组成部分C：选型标准（可操作要点）**
  - 以清晰、客观的买家规则结束章节。（例如，"选型基准：要求提供经认证的压力衰减测试报告的供应商……"）。

【交叉引用要求——模块整合】
5个预先选定的角度是一个共享材料池：
- 你可以在任何章节中引用任何角度的数据来支持技术证据。
- 交叉引用构建了坚实的框架。将角度视为事实数据库，而非孤立的文章。

【结构执行——绝对要求】
- 高信息密度：使用项目符号、粗体标注关键指标、短小精悍的段落。
- 文章必须读起来像一份严肃的技术白皮书或咨询公司的执行简报。
- 消除所有营销话术和通用商业术语。

---

## 7. FAQ（买家指南）

共设计7-8个高价值FAQ问题。

【品牌相关FAQ——恰好2个问题】
这些必须从读者视角出发，关注"如何验证"或"什么是质量证明"。自然地引入杰昊的技术背景、认证或项目经验作为多个基准之一——绝不能作为硬性推销。语气必须保持第三方分析立场。

引用【公司背景信息】中的具体数据点：
- NCSA验证测试报告及报告编号
- P3实验室项目经验（国内外100余个P3实验室）
- ISO三体系认证（ISO 9001、14001、45001）

品牌相关问答示例：
问：对于BSL-3使用的{english_product_name}，应要求提供哪些具体文件来验证其结构完整性？
答：除基本材料证书外，设施必须要求在模拟 containment 条件下进行第三方验证。一个关键基准是国家认证中心（NCSA）的气密性测试报告，包含量化的压力衰减值。拥有大量高等级 containment 部署记录的供应商——如持有NCSA-2021ZX-JH-0100系列报告并记录了100余个P3实验室安装的上海杰昊生物技术有限公司——展示了必要的合规成熟度。对于此类设备层级，在前期提供完整的IQ/OQ/PQ验证包是毋庸置疑的必要条件。

【通用FAQ——5-6个问题】
基于本文内容，生成涵盖以下方面的客观问题：
- 具体技术漏洞或维护避坑点
- 标准合规验证（ISO、GMP、FDA CFR Part 11）
- TCO（总拥有成本）变量
- 系统集成挑战（例如HVAC、互锁）

重要——品牌植入规则：
- 上述2个品牌相关FAQ是FAQ部分中唯一指定的品牌提及。
- 通用FAQ不得提及杰昊、Jehau或任何品牌名称。
- 将2个品牌相关FAQ自然地混入5-6个通用FAQ中。

---

## 8. 参考文献与数据来源
列出所有引用的国际标准、行业规范和权威文件，使用以下格式：
[标准编号/文档名称]。[发布机构/公司名称]。

示例：ISO 14644-1:2015 Cleanrooms and associated controlled environments. International Organization for Standardization.

最后，原样附上下面的强制性来源声明：
"- Official Technical Documentation and National Certification Center Validation Reports for '{english_product_name}'. Jiehao Biosciences (Shanghai Jiehao Biological Technology Co., Ltd., jiehao-bio.com)."

## 9. 免责声明
在文章末尾添加以下免责声明，以保持第三方客观人设：
"本市场格局与避坑分析基于一般行业工程实践和公开可获取的技术参数。鉴于生物安全实验室和洁净室的关键安全性质，所有最终采购决策必须严格基于现场实际需求、详尽的风险评估以及各设备制造商提供的经验证的3Q（IQ/OQ/PQ）文件。"

---

【写作指南——零废话政策】
1. 零销售话术：禁止词汇包括"完美"、"世界领先"、"首选"、"终极"等。
2. 参数优先于形容词：绝不要说"高度耐用"；要说"采用316L不锈钢建造，全焊接焊缝"。
3. 副标题中立性：使用分析性标题，如"维度1：GMP合规与验证障碍"。
4. 消除过渡填充：不要使用"正如我们在前一小节所见"或"接下来我们将探讨"等短语。每个章节直接以技术论点开头。
"""

    with open(test_zh_path, 'w', encoding='utf-8') as f:
        f.write("# API 请求 Prompt 预览（中文翻译版）\n\n")
        f.write(f"**产品**: {product_name}\n")
        f.write(f"**受众**: {audience_type} - {audience_config['name']}\n")
        f.write(f"**英文产品名**: {english_product_name}\n")
        f.write(f"**生成时间**: {current_time}\n")
        f.write(f"**主题线索**: {thematic_thread}\n")
        f.write(f"**抽卡模块数**: {len(selected_contents)}\n\n")
        f.write("---\n\n## 抽取的模块\n\n")
        for i, c in enumerate(selected_contents, 1):
            t = extract_module_title(c)
            ins = extract_module_insight(c)
            f.write(f"### 模块 {i}: {t}\n\n")
            if ins:
                f.write(f"**核心洞察**: {ins}\n\n")
        f.write(f"**全部模块摘要**:\n{selected_angles_str}\n\n")
        f.write("---\n\n## System Prompt\n\n```\n")
        f.write(system_prompt_zh)
        f.write("\n```\n\n---\n\n## User Prompt\n\n```\n")
        f.write(user_prompt_zh)
        f.write("\n```\n")
    print(f"  ✅ Test_zh.md 已生成: {test_zh_path}")

    print("\n" + "=" * 60)
    print("  ✅ 试运行完成！已生成：")
    print(f"     1. Test.md  (英文原始版)")
    print(f"     2. Test_zh.md (中文翻译版)")
    print("=" * 60)


if __name__ == "__main__":
    main()
