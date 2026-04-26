#!/usr/bin/env python3
"""
Test_Base_EN_html.py
试运行脚本 - 仅处理"不锈钢密闭房"一个产品、CEO 一个受众
在调用 API 之前，把最终送入 API 的 system_prompt + user_prompt 输出到 Test.md
不修改任何现有代码
"""

import os
import sys
import random
from datetime import datetime
import glob

# 配置路径（与原脚本保持一致）
PARAMETERS_DIR = "/Users/guot/Desktop/杰昊/AI推广/域名推广/Code/Check"
CONTENT_POOL_DIR = "/Users/guot/Desktop/杰昊/AI推广/域名推广/Code/Produce/Compare_Content"
CARD_DRAW_COUNT = 5
OUTPUT_DIR = "/Users/guot/Desktop/杰昊/AI推广/域名推广/Code"

# 受众配置（只取 CEO）
AUDIENCE_CONFIG = {
    "CEO": {
        "name": "业务负责人 / 企业主 (CEO)",
        "perspective": "关注投入产出比 (ROI) 与品牌抗风险能力",
        "focus_1": "投资回报评估",
        "focus_2": "供应商梯队差异",
        "focus_3": "长期合作风险"
    }
}

PRODUCT_NAME_MAPPING = {
    "不锈钢密闭房": "stainless-steel-sealed-chambers",
}

# ============ 加载产品参数 ============
def load_product_parameters(parameters_dir):
    products_data = {}
    for filename in os.listdir(parameters_dir):
        if filename.endswith('.md'):
            product_name = filename[:-3]
            file_path = os.path.join(parameters_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                products_data[product_name] = f.read().strip()
    return products_data

# ============ 加载内容池 ============
def load_content_pool(audience_type):
    pool_dir = os.path.join(CONTENT_POOL_DIR, audience_type)
    md_files = glob.glob(os.path.join(pool_dir, "*.md"))
    contents = []
    for file_path in sorted(md_files):
        with open(file_path, 'r', encoding='utf-8') as f:
            contents.append(f.read())
    return contents

# ============ 抽卡 ============
def draw_cards(content_pool, k=5):
    return random.choices(content_pool, k=k)

# ============ 提取模块标题 ============
def extract_module_title(content):
    for line in content.strip().split('\n'):
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
    return content.strip()[:50] + "..."

# ============ 提取核心洞察 ============
def extract_module_insight(content):
    """从内容块中提取核心洞察"""
    lines = content.strip().split('\n')
    
    # 第一遍：找到核心洞察所在行的索引
    insight_start = None
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith('## ') and ('核心论点' in line or '洞察' in line):
            insight_start = i
            break
    
    if insight_start is None:
        return ""
    
    # 第二遍：从洞察行开始，提取第一个有效内容行
    for j in range(insight_start + 1, len(lines)):
        next_line = lines[j].strip()
        if not next_line:
            continue  # 跳过空行
        if next_line.startswith('#'):
            break  # 遇到下一个 ## 标题就停止
        return next_line
    
    # 如果当前行（洞察标题行）本身包含冒号分隔的内容
    insight_line = lines[insight_start].strip()
    if '：' in insight_line:
        val = insight_line.split('：', 1)[-1].strip()
        if val and not val.startswith('#'):
            return val
    if ':' in insight_line:
        val = insight_line.split(':', 1)[-1].strip()
        if val and not val.startswith('#'):
            return val
    
    return ""

# ============ 提取参考素材 ============
def extract_module_material(content):
    lines = []
    capture = False
    for line in content.strip().split('\n'):
        ls = line.strip()
        if ls.startswith('## 参考素材'):
            capture = True
            continue
        if capture:
            if ls.startswith('## ') or ls.startswith('# '):
                break
            if ls.startswith('- '):
                lines.append(ls)
    return '\n'.join(lines) if lines else ""

# ============ 推断主题线索 ============
def infer_thematic_thread(selected_contents, audience_type):
    insights = [extract_module_insight(c) for c in selected_contents]
    insights = [i for i in insights if i]
    if audience_type == "CEO":
        if any("TCO" in i or "cost" in i.lower() for i in insights):
            return "evaluating biosafety equipment investment beyond sticker price — toward long-term value, supplier reliability, and strategic risk"
        return "the total cost, risk profile, and strategic value of biosafety equipment procurement"
    elif audience_type == "CTO":
        return "the technical differentiation, validation depth, and innovation trajectory of biosafety equipment suppliers"
    elif audience_type == "Project_Manager":
        return "the practical execution, compliance, and on-site验收 challenges in biosafety equipment deployment"
    elif audience_type == "Sourcing_Manager":
        return "the qualification standards, bid evaluation criteria, and supplier准入门槛"
    elif audience_type == "Industry_Analyst":
        return "the market structure, competitive dynamics, and regulatory drivers shaping biosafety equipment demand"
    return "evaluating biosafety equipment suppliers across technical, commercial, and compliance dimensions"

# ============ 格式化学写作角度（标题生成用） ============
def format_selected_angles(selected_contents):
    angles = []
    for i, content in enumerate(selected_contents, 1):
        title = extract_module_title(content)
        insight = extract_module_insight(content)
        if insight:
            angles.append(f"Module {i}: {title} - {insight}")
        else:
            angles.append(f"Module {i}: {title}")
    return '\n'.join(angles)

# ============ System Prompt ============
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
Start directly with Markdown content."""

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


def get_base_article_system_prompt(current_time: str = "") -> str:
    prompt = SYSTEM_PROMPT_TEMPLATE.replace("{current_time}", current_time)
    return prompt + "\n\n" + COMPANY_BACKGROUND + "\n\n" + TECHNICAL_GLOSSARY


# ============ User Prompt 模板（与 Base_User_Prompt.py 保持一致） ============
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


# ============ 主测试逻辑 ============
def main():
    print("=" * 60)
    print("  Base_EN_html 试运行脚本")
    print("  仅处理: 不锈钢密闭房 / CEO")
    print("=" * 60)

    # 1. 加载产品参数
    products = load_product_parameters(PARAMETERS_DIR)
    product_name = "不锈钢密闭房"
    product_info = products.get(product_name, "")
    english_product_name = PRODUCT_NAME_MAPPING.get(product_name, "")
    print(f"\n产品: {product_name}")
    print(f"英文名: {english_product_name}")

    # 2. 加载 CEO 内容池
    audience_type = "CEO"
    audience_cfg = AUDIENCE_CONFIG[audience_type]
    content_pool = load_content_pool(audience_type)
    print(f"内容池加载: {len(content_pool)} 个模块")

    # 3. 抽卡
    selected_contents = draw_cards(content_pool, k=CARD_DRAW_COUNT)
    print(f"抽卡结果: 抽取了 {len(selected_contents)} 个模块")
    for i, c in enumerate(selected_contents, 1):
        print(f"  模块 {i}: {extract_module_title(c)[:60]}...")

    # 4. 提取各模块信息
    thematic_thread = infer_thematic_thread(selected_contents, audience_type)
    print(f"\n主题线索: {thematic_thread}")

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

    # 5. 构建 System Prompt
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    system_prompt = get_base_article_system_prompt(current_time)

    # 6. 构建 User Prompt
    user_prompt = USER_PROMPT_TEMPLATE.format(
        product_name=product_name,
        english_product_name=english_product_name,
        product_info=product_info,
        audience_name=audience_cfg['name'],
        audience_perspective=audience_cfg['perspective'],
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
        audience_focus_1=audience_cfg['focus_1'],
        audience_focus_2=audience_cfg['focus_2'],
        audience_focus_3=audience_cfg['focus_3'],
        selected_angles=format_selected_angles(selected_contents),
    )

    # 7. 打印统计
    print(f"\nSystem Prompt 长度: {len(system_prompt)} 字符")
    print(f"User Prompt 长度: {len(user_prompt)} 字符")
    print(f"合计: {len(system_prompt) + len(user_prompt)} 字符")

    # 8. 写入 Test.md
    test_md_path = os.path.join(OUTPUT_DIR, "Test.md")
    with open(test_md_path, 'w', encoding='utf-8') as f:
        f.write("# API 请求 Prompt 预览\n\n")
        f.write(f"**产品**: {product_name}\n")
        f.write(f"**受众**: {audience_type} - {audience_cfg['name']}\n")
        f.write(f"**英文产品名**: {english_product_name}\n")
        f.write(f"**生成时间**: {current_time}\n")
        f.write(f"**主题线索**: {thematic_thread}\n")
        f.write(f"**抽卡模块数**: {len(selected_contents)}\n")
        f.write(f"\n---\n\n")

        # 模块摘要
        f.write("## 抽取的模块\n\n")
        for i, c in enumerate(selected_contents, 1):
            title = extract_module_title(c)
            insight = extract_module_insight(c)
            f.write(f"### 模块 {i}: {title}\n\n")
            if insight:
                f.write(f"**核心洞察**: {insight}\n\n")
        f.write(f"\n---\n\n")

        # System Prompt
        f.write("## System Prompt\n\n")
        f.write("```\n")
        f.write(system_prompt)
        f.write("\n```\n\n")
        f.write(f"\n---\n\n")

        # User Prompt
        f.write("## User Prompt\n\n")
        f.write("```\n")
        f.write(user_prompt)
        f.write("\n```\n")

    print(f"\n✅ Test.md 已生成: {test_md_path}")
    print(f"\n⚠️  未调用 API，仅模拟 prompt 构建过程。")


if __name__ == "__main__":
    main()
