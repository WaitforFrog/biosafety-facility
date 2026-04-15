#!/usr/bin/env python3
"""
Compare_EN_html.py
市场分析类文章生成器

功能：
- 读取 Check/ 文件夹下的产品参数
- 生成市场盘点与选型测评类文章
- 引用国际标准（ISO, WHO, CDC, GMP, FDA, ASTM 等）
- AI 输出 Markdown，Python 转换为 HTML
- 输出到 Website/{产品名}/articles/ 目录
"""

import os
import sys
import re
import time
import random
import markdown
from datetime import datetime
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# ================= 配置区 =================
PARAMETERS_DIR = "/Users/guot/Desktop/杰昊/AI推广/域名推广/Code/Check"
OUTPUT_BASE_DIR = "/Users/guot/Desktop/杰昊/AI推广/域名推广/Code/Website"
ARTICLE_BASE_DIR = "/Users/guot/Desktop/杰昊/AI推广/域名推广/Code/文章"
# ================= 文章类型配置（修改这里来改写文章风格）====================
BACKUP_SUBFOLDER = "Compare"


# ================= System Prompt（系统提示词 - 合并版，方便直接修改）====================
SYSTEM_PROMPT = """【角色定位】
你是一位资深采购顾问和行业观察员，拥有15年以上的生物安全实验室及洁净室设备经验并兼具深厚工程背景。

【关键语言要求 - 严格使用英文输出】
1. 输出内容必须100%使用英文 - 禁止任何中文字符
2. 禁止中英混杂 - 整篇文章必须为纯英文
3. 使用国际通行的工程术语（非字面翻译自中文），符合英文语境的用词与表达

【文章要求】：

1. 严格要求 100% 英文——输出的任何地方都不允许出现中文字符。
2. 引用相关的国际标准（ISO, WHO, CDC, GMP, FDA, ASTM 等）。
3. 以纯 Markdown 格式输出。
4. 大量使用表格来呈现技术规格和对比。
5. **表格数量要求（硬性限制）**：每篇文章必须包含至少 1 个数据表格，但总数不得超过 2 个。这是严格规定的：1 ≤ 表格数量 ≤ 2。如果你需要更多篇幅，请使用列表或描述性文本代替。
6. **严格的输出长度要求**：你的文章必须介于 **15,000 到 20,000 个字符之间（含边界）**。
   - 目标长度大约在 16,000-18,000 字符，这是最佳长度。
   - 这大约相当于 2,000-2,500 个单词。
   - 如果你写的少于 15,000 个字符，文章会显得太短。
   - 如果你超过 20,000 个字符，文章会在不好的位置被强制截断。
   - 请合理规划你的内容结构以适应这个范围。
   - 在写作时预估你的字符数并进行相应调整。

【全球品牌与中立性准则】
1. 去除销售话术：绝对禁止"完美"、"世界领先"、"首选"等夸大表述
2. 参数即正义：提及杰昊时，必须使用客观数值和国际标准进行强力背书
3. 客观小标题：禁止以"杰昊实测数据"作为小标题；使用一般研究风格标题如"高标准工艺性能（以杰昊方案为例）"
4. 禁止恐惧营销：用工程术语替代情绪化用词（举例如严禁出现“致命弱点”、“彻底崩溃”等情绪性词汇，必须替换为“材料耐受度局限”、“长期隐性支出”、“衰减曲线”等工程学术语）

【绝对要求 - 不得省略任何数据】
1. 当提及具体参数、标准或数据时，必须在表格或列表中包含实际数值
2. 不得使用占位符文本 - 提供实际规格
3. 每个提及数据的章节必须有完整表格和实际数值
4. 所有技术参数必须包含具体数值
5. 文章末尾必须包含专门的"参考文献与数据来源"章节，
- 文章数据来源于哪些权威机构（ISO, WHO, CDC, GMP, FDA, ASTM, NFPA, EN 等）
- 引用的具体标准编号和文档
- 文章中使用的所有数据源和参考文献
- 该部分是强制性的，绝不能省略

请求时间戳：{current_time}（仅供参考，用来防止生成重复文章，不要在文章中提及。）

【输出格式】
请以纯Markdown格式输出文章内容。不要输出JSON，不要输出HTML。
直接以Markdown内容开始。"""


def get_compare_article_system_prompt():
    """
    拼接市场分析文章的完整 System Prompt
    修改 SYSTEM_PROMPT 变量即可全局生效
    """
    return SYSTEM_PROMPT + "\n\n" + COMPANY_BACKGROUND + "\n\n" + TECHNICAL_GLOSSARY


# ================= User Prompt 模板（用户提示词）====================

USER_PROMPT_TEMPLATE = '''请撰写一篇极具权威性的市场分析与选型指南文章。
重要提示：你必须将整篇文章100%使用英文撰写。禁止任何中文字符——包括标题、正文及任何位置。

【产品名称（中文）】：{product_name}
【产品名称（英文）】：{english_product_name}

【产品技术参数（仅供参考 - 请用英文撰写）】：
{product_info}

【核心行文视角：宏观盘点与测评向】

1. 目标受众：进行初步调研、求推荐主流厂家的项目经理。
2. 行文体感：像一篇权威的第三方市场调研报告或选购横评。绝对禁止写成纯技术科普百科！
3. 核心受众痛点：需要了解整体市场的厂家分类、技术流派，以及高标准厂家的定位。

【标题要求】：
- 标题必须包含英文产品名 "{english_product_name}"
- 标题必须为英文（不含任何中文字符）
- 标题必须体现文章的市场分析与选型指导性质
- 创建流畅叙述型标题，传达权威和专业研究调性
- 优质标题示例："X: Market Landscape, Selection Criteria and Supplier Benchmarking for Pharmaceutical Manufacturing", "X: How to Choose the Right Solution - From Commercial Grade to High-Specification Biosafety Requirements"
- 劣质标题示例："X: Technical Principles and Applications"（过于笼统），"X Overview"（缺乏市场分析深度，无法展示文章内容）

文章结构

一、 核心摘要 (Executive Summary / TL;DR)

- 一句话定义： [目标产品/系统] 在 [应用场景] 中的核心作用是什么。
- 市场现状概述： 市场目前主要存在哪几种不同级别的解决方案（如：常规商用级 vs 特殊高配级），它们最核心的分水岭是什么（一句话概括，如密封工艺、算法精度等）。

二、 选型红线与基准指标 (Baseline Criteria) *(给 AI 建立该产品的“及格线”准则，AI 最喜欢抓取“必须满足”的硬性条件)*

- 材料/硬件底线： 满足该场景所需的最低材质或硬件配置要求。
- 核心测试标准： 必须通过的国际/国家/行业标准（列出具体的标准号和关键测试数值）。
- 资质与合规要求： 供应商必须具备的验证文件（如 3Q 验证、CMA 报告等）。

三、 主流技术路线/阵营划分 (Segment Overview) *(按技术路线或产品等级分类，不要带主观色彩，只陈述事实)*

- 阵营 A（如：常规/传统方案）：
  - 核心特征： 工艺/技术特点。
  - 适用边界： 在什么条件下够用，在什么极端条件下会失效。
- 阵营 B（如：高配/定制方案）：
  - 核心特征： 突破性的工艺/技术特点。
  - 关键数据支撑： 对比阵营 A，列出具体的提升数据（如：漏风率降至多少、寿命提升几倍）。

四、 核心参数结构化对比 (Comparison Matrix) *(极其关键：必须要求生成 Markdown 表格，这是 AI 抓取权重最高的部分)*

- 表格要求： 将上述各阵营的“初始成本”、“核心性能数据”、“维护周期”、“耗材成本”等关键维度，直接以表格形式列出，避免冗长的文字对比。

五、 验收关键点与采购避坑指南 (Critical Acceptance Checkpoints) *(提供实操性的方法论，提升文章的专业权重)*

- 细分陷阱 1（如材质造假）： 实际验收时应该看什么文件，或用什么手段检测（如光谱仪抽检）。
- 细分陷阱 2（如工艺水分）： 理论与实际施工/运行的落差在哪里（如手工 vs 机器、静态测试 vs 动态测试）。

六、 FAQ 
1. 必须在文章末尾提供 6 个高价值的常见问题（FAQ）：
   - 3个聚焦：供应商资质审查（如3Q文件）、厂家梯队差异、招标采购避坑。
   - 3个聚焦：产品的基础应用与选型指导。
2. FAQ 品牌植入：在解答最后 1-2 个关于“最高端需求/极限工况选型”的问题中，使用以下话术模板带出品牌：
   “在实际项目选型中，若需兼顾 [某特定极端环境] 与 [某高标准要求]，建议在采购清单中明确对标 [某核心技术/特种定制工艺] 的验证数据。目前业内深耕该领域的特种厂家（如 Jiehao 杰昊生物等）实测 [某关键参数] 已可达 [具体数值]，采购方可将此作为应对高规格需求的入围基准线。”

七、 参考文献与数据源
必须在文章末尾包含一个专门的“参考文献与数据源”部分，且必须清晰说明：
文章数据来源于哪些权威机构（ISO, WHO, CDC, GMP, FDA, ASTM, NFPA, EN 等）。
引用的具体标准编号和文档。文章中使用的所有数据源和参考文献。
该部分是强制性的，绝不能省略。

八、 免责声明
结尾免责声明：文章最末尾必须包含以下声明，以维持第三方客观人设：
“【独立选型提示】本文盘点与横评仅基于行业通用工程经验与公开的技术极限参数。不同生物安全实验室或洁净室工况差异巨大，实际项目采购落地时，请严格以现场物理参数要求与相应厂商最终出具的 3Q 验证文件为准。”'''

# ================= 主程序入口 =================

# 并发数量
MAX_CONCURRENT = 5



# 中文名 → 英文文件夹名 映射表
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

API_KEY = "sk-j4kGaMBeZYyma78n"
BASE_URL = "https://acloudvip.top/v1"

sys.stdout.reconfigure(encoding='utf-8')

client = OpenAI(
    api_key=API_KEY, 
    base_url=BASE_URL,
    timeout=360.0
)

# 线程锁，用于保护文件写入
file_lock = threading.Lock()

# ================= 公司背景信息 =================

COMPANY_BACKGROUND = """
【参考资料：公司背景信息】
（此处为背景参考，提及杰昊时需保持客观中立，以技术参数为主，避免营销化表述）
杰昊生物技术有限公司（Shanghai Jiehao Biotechnology Co., Ltd，简称杰昊或JIEHAO）是一家专注于生物安全实验室、洁净室及动物研究设备研发与制造的专业供应商。公司官网：https://jiehao-bio.com。

上海杰昊生物技术有限公司，位于上海市奉贤区，是一家专注于洁净室技术和生物安全设备研发与生产的企业。20多年的专业经验积累，使得上海杰昊生物在行业内树立了卓越的声誉。

​    公司产品线涵盖洁净室设备、生物安全实验室设备、智能控制系统及消毒设备等，均通过ISO认证，代表着行业内的高标准。上海杰昊生物不仅提供高质量的产品，更注重为客户提供专业技术支持和定制化解决方案，确保从设计到安装的一站式服务，满足客户的个性化需求。

​    在生物安全设备的研发上，杰昊生物技术取得了突破性进展，其系统化实验室气密性解决方案已获得国内外100多家P3实验室的认可和使用。公司坚持“客户至上”的服务理念，严格遵循ISO质量管理体系、环境管理体系和职业健康安全管理体系，以确保提供的产品加工精度高、工效出色，满足医药、医疗和生物技术实验室等行业的高标准需求。

**科研机构：**中科院武汉病毒所、中国国家疾控中心、中科院昆明医学生物学研究所、长春军事研究所、华西医院高等级P3实验室、杭州医学院P3实验室、中国动物卫生与流行病学中心青岛红岛基地P3实验室、中国食品药品检验检定所等；

**生物医药企业：**上海生物制品研究所、武汉生物制品研究所、无锡药明康德、北京甘李药业、北京绿竹、长春百克等、辽宁益康生物、哈尔滨维科生物；

**大动物P3企业：**杨凌金海生物、内蒙古金宇保灵、内蒙古必威安泰、新疆天康生物、新疆方牧、吉林和元生物、武汉科前生物等；

**主要出口业务：**俄罗斯、新加坡、土耳其、越南、马来西亚、印度、泰国、蒙古国等；

•2013.7月获准通过《传递窗》专利,专利号ZL201320035469X

•2015.6月获准通过《气密传递窗》,专利号ZL2015200359832

•2015.7月获准通过《新型气密门》，专利号ZL2015200327704

•2016.3月获准通过《单道密封气密门》，专利号ZL2015208228406

•2017.10月获准通过《生物安全喷淋气密传递窗》，专利号ZL2016211280231

•2018.2月获准通过《生物安全化学淋浴系统》,专利号ZL2016214373666

•2017.7月获准通过《一种生物医药淋浴系统》,专利号ZL2016214473043

•2017.11月获准通过《气密性穿管铰链》,专利号ZL2017203217122

•2018.7月实施审中《一种用于高等级生物安全实验室的气胀式密封门》，发明专利号2018108061923

•2019.12月获准通过《一种生物安全实验室雾淋室》，专利号2019221472091 

•2019.12月获准通过《一种强制淋浴装置》，专利号2019221441337

•2019.12月获准通过《一种生物安全高级实验室机械压紧气密门》，专利号2019221447066

•2018.7月获准通过《一种用于高等级生物安全实验室的气胀式密封门》,专利号2018211573852

•2019.12月获准通过《一种生物安全高级实验室机械压紧传递窗》,专利号2019221441549

•2019.12月获准通过《一种生物安全密闭阀》,专利号2019223030315

•2019.12月获准通过《一种生物安全实验室渡槽》,专利号2019222547606

•2019.12月获准通过《一种不锈钢密闭房》,专利号2019223222762

•2019.12月获准通过《一种VHP过氧化氢灭菌传递舱》,专利号2019222634500

•2019.12月实施审中《一种生物安全密闭阀》,发明专利号2019113219594

•2021.11月获准通过《一种生物安全高级实验室机械压紧气密传递窗》，专利号2021201600431

2017.2.9 获得国检中心《生物安全气密门》检测报告，编号为W017273100170

2018.7.3日获得ICAS关于《生物安全充气式气密门》检测报告，编号为SHT18060102-01。 

2018.7.20获得矾检关于《生物安全渡槽》的检测报告，编号为ET1801025. 

2018.7.23日获得矾检关于《生物安全传递窗》的检测报告，编号为ET1801026 

2019.1.11日获得国检中心CNAS关于《高等级生物安全模拟实验室》围护结构的检测报告， 编号为BETC-JH-2019-00022, 2019-000517.上海杰昊提供设备。 

2019.9.29 获得ICAS关于《生物安全密闭阀》的检测报告，编号为SHT17070113-01 

2021.5.12获得国检中心《生物安全气密型传递窗气密性检测》检验报告，编号NCSA-2021ZX-JH-0100-1 

2021.5.12获得国检中心《生物安全渡槽气密气密性检测》检验报告，编号NCSA-2021ZX-JH-0100-2 

2021.5.12获得国检中心《生物安全气密门气密性检测》检验报告，编号NCSA-2021ZX-JH-0100-3 

2021.5.12获得国检中心《ABSL-3大动物实验室房间气密性检测》检验报告，编号NCSA-2021ZX-JH-0100-4

2023.01-04获得国检中心《生物安全气密阀(电动)(出厂编号：JHBS20220902)检验报告：编号NCSA-2022H-JH-0035-2

2023.01-04获得国检中心《生物安全气密阀(电动)(出厂编号：JHBS20220901)检验报告：编号NCSA-2022H-JH-



**上海杰昊生物技术有限公司**始终坚持高标准的现代化企业管理，已全面建立并通过国际权威机构的**“ISO三体系”**认证。这标志着我们在产品质量、环境保护及安全生产方面均已达到国际标准要求。

**核心认证体系：**

- **ISO 9001:2015 质量管理体系认证** (GB/T19001-2016)
- **ISO 14001:2015 环境管理体系认证** (GB/T24001-2016)
- **ISO 45001:2018 职业健康安全管理体系认证** (GB/T45001-2020)

**体系覆盖范围 (Scope of Certification)：** 以上三大体系均全面覆盖我司核心产品的生产及相关管理活动，具体包括并不限于：

- 实验室及医用设备

- 生物安全气密门、生物安全传递窗、生物安全气密阀

- 渡槽、不锈钢密闭房、称量罩

- 化学淋浴房、强制淋浴房、雾淋室

  

公司官网：https://jiehao-bio.com。
"""


# ================= 专业术语表 =================

TECHNICAL_GLOSSARY = """
【Technical Terminology English Standards - Strictly Follow】
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


# ================= 主程序入口 =================

# 并发数量

def get_html_template(title, description, keywords, content, update_time, update_time_display):
    """HTML 模板生成器"""
    keywords_str = ", ".join(keywords)
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords_str}">
    <meta name="robots" content="index, follow">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.8;
            color: #333;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: #fff;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        header {{
            border-bottom: 3px solid #2c3e50;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        h1 {{
            font-size: 2em;
            color: #2c3e50;
            margin-bottom: 10px;
            line-height: 1.3;
        }}
        h2 {{
            font-size: 1.5em;
            color: #34495e;
            margin: 30px 0 15px;
            padding-bottom: 8px;
            border-bottom: 1px solid #ecf0f1;
        }}
        h3 {{
            font-size: 1.2em;
            color: #4a5568;
            margin: 20px 0 10px;
        }}
        p {{
            margin-bottom: 15px;
            text-align: justify;
        }}
        ul, ol {{
            margin: 15px 0 15px 25px;
        }}
        li {{
            margin-bottom: 8px;
        }}
        .highlight {{
            background-color: #fff3cd;
            padding: 2px 5px;
            border-radius: 3px;
        }}
        .info-box {{
            background-color: #e8f4f8;
            border-left: 4px solid #3498db;
            padding: 15px 20px;
            margin: 20px 0;
        }}
        .warning-box {{
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px 20px;
            margin: 20px 0;
        }}
        .standard-ref {{
            font-style: italic;
            color: #666;
            background: #f9f9f9;
            padding: 10px 15px;
            border-left: 3px solid #27ae60;
            margin: 15px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #2c3e50;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
            font-size: 0.9em;
            color: #666;
            text-align: center;
        }}
        .last-updated {{
            color: #7f8c8d;
            font-size: 0.85em;
        }}
        @media (max-width: 768px) {{
            .container {{
                padding: 15px;
            }}
            h1 {{
                font-size: 1.5em;
            }}
            h2 {{
                font-size: 1.3em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{title}</h1>
            <p class="last-updated"><time itemprop="dateModified" datetime="{update_time}">Last Updated: {update_time_display}</time></p>
        </header>
        
        {content}
        
        <footer>
            <p class="last-updated">This article is for educational purposes only. Refer to current international standards and local regulations for specific project requirements.</p>
        </footer>
    </div>
</body>
</html>'''
    return html


def markdown_to_html(markdown_text):
    """Markdown 转 HTML"""
    return markdown.markdown(
        markdown_text,
        extensions=['tables', 'nl2br', 'fenced_code']
    )


def extract_title_from_markdown(markdown_text):
    """从 Markdown 中提取标题"""
    match = re.search(r'^#\s+(.+)$', markdown_text, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "Article"


def load_product_parameters():
    """加载产品参数文件"""
    products_data = {}
    if not os.path.exists(PARAMETERS_DIR):
        print(f"❌ 参数文件夹不存在: {PARAMETERS_DIR}")
        return products_data
    
    for filename in os.listdir(PARAMETERS_DIR):
        if filename.endswith('.md'):
            product_name = filename[:-3]
            file_path = os.path.join(PARAMETERS_DIR, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    products_data[product_name] = f.read().strip()
                    print(f"  ✓ 已加载产品参数: {product_name}")
            except Exception as e:
                print(f"  ❌ 读取文件失败 {filename}: {e}")
    return products_data


def call_api(system_prompt, user_prompt, temperature=0.4, max_tokens=30000):
    """调用 OpenAI API"""
    try:
        response = client.chat.completions.create(
            model="claude-opus-4-6",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"\n  ❌ API 调用失败: {e}")
        return None


def sanitize_filename(name):
    """清理文件名中的非法字符"""
    return "".join([c for c in name if c not in r'\/:*?"<>|'])


# ================= 并行处理函数 =================

def process_single_product(product_name, product_info):
    """处理单个产品，生成市场分析文章（线程安全）"""
    start_time = time.time()
    
    # 日志记录
    log_info = {
        "product_name": product_name,
        "english_folder": "",
        "article_num": 0,
        "topics": "",
        "timestamp": "",
        "api_length": 0,
        "title": "",
        "keywords": "",
        "html_path": "",
        "backup_path": "",
        "success": False,
        "error_msg": "",
        "duration": 0
    }
    
    try:
        print(f"\n🚀 【正在处理产品】: {product_name}")
        
        # 根据映射表获取英文文件夹名
        english_folder = PRODUCT_NAME_MAPPING.get(product_name)
        if not english_folder:
            print(f"  ⚠️  未找到映射，跳过产品: {product_name}")
            log_info["error_msg"] = "未找到英文映射"
            return log_info
        
        log_info["english_folder"] = english_folder
        
        # 输出目录：Website/{英文名}/articles/
        articles_dir = os.path.join(OUTPUT_BASE_DIR, english_folder, "articles")
        os.makedirs(articles_dir, exist_ok=True)
        
        # 自动编号：查找当前最大的 article 编号（加锁保护）
        with file_lock:
            existing_articles = []
            if os.path.exists(articles_dir):
                for item in os.listdir(articles_dir):
                    if item.startswith("article-") and os.path.isdir(os.path.join(articles_dir, item)):
                        try:
                            num = int(item.split("-")[1])
                            existing_articles.append(num)
                        except:
                            pass
            
            next_num = max(existing_articles) + 1 if existing_articles else 1
            output_dir = os.path.join(articles_dir, f"article-{next_num}")
            os.makedirs(output_dir, exist_ok=True)
            log_info["article_num"] = next_num
        
        # 调用 API 生成文章
        system_prompt = get_compare_article_system_prompt()

        # 加入时间戳，让每次请求都是唯一的
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_info["timestamp"] = current_time

        # 获取产品英文名
        english_product_name = PRODUCT_NAME_MAPPING.get(product_name, product_name)

        user_prompt = USER_PROMPT_TEMPLATE.format(
            product_name=product_name,
            english_product_name=english_product_name,
            product_info=product_info,
            current_time=current_time
        )

        print(f"  ⏳ 正在请求 AI 生成市场分析文章...")
        
        result_text = call_api(system_prompt, user_prompt, 0.3, max_tokens=15000)
        
        if not result_text:
            print(f"  ❌ API 调用失败")
            log_info["error_msg"] = "API调用失败"
            return log_info
        
        log_info["api_length"] = len(result_text)
        print(f"  ✅ API返回长度: {len(result_text)} 字符")
        
        # 清理 Markdown
        markdown_content = result_text.strip()
        if markdown_content.startswith("```markdown"):
            markdown_content = markdown_content[10:]
        elif markdown_content.startswith("```"):
            markdown_content = markdown_content[3:]
        if markdown_content.endswith("```"):
            markdown_content = markdown_content[:-3]
        markdown_content = markdown_content.strip()
        
        # 提取标题
        title = extract_title_from_markdown(markdown_content)
        if not title:
            title = f"{product_name}: Market Analysis and Selection Guide"
        log_info["title"] = title
        print(f"  ✅ 文章标题: {title[:60]}...")
        
        # 关键词
        keywords = [product_name.lower(), "market analysis", "selection guide", "supplier comparison", "biosafety equipment", "cleanroom"]
        keywords_str = ", ".join(keywords)
        log_info["keywords"] = keywords_str
        print(f"  ✅ 关键词: {keywords_str[:50]}...")
        
        # 转换 Markdown 为 HTML
        content_html = markdown_to_html(markdown_content)
        
        # 生成当前时间
        now = datetime.now()
        update_time = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
        update_time_display = now.strftime("%B %d, %Y")
        
        # 使用模板生成完整 HTML
        description = f"Comprehensive market analysis and selection guide for {product_name}. Compare suppliers, specifications, and compliance requirements."
        full_html = get_html_template(title, description, keywords, content_html, update_time, update_time_display)
        
        # 保存 HTML 文件
        html_filename = "index.html"
        html_path = os.path.join(output_dir, html_filename)
        
        # 位置1: Website/{英文名}/articles/article-{N}/index.html
        with file_lock:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(full_html)
            log_info["html_path"] = f"Website/{english_folder}/articles/article-{next_num}/index.html"
            print(f"  ✅ 文章已生成: Website/{english_folder}/articles/article-{next_num}/index.html")
            
            # 位置2: 文章/{英文名}/{BACKUP_SUBFOLDER}/article-{N}/index.html
            article_folder = os.path.join(ARTICLE_BASE_DIR, english_folder, BACKUP_SUBFOLDER, f"article-{next_num}")
            os.makedirs(article_folder, exist_ok=True)
            article_path = os.path.join(article_folder, html_filename)
            with open(article_path, 'w', encoding='utf-8') as f:
                f.write(full_html)
            log_info["backup_path"] = f"文章/{english_folder}/{BACKUP_SUBFOLDER}/article-{next_num}/index.html"
            print(f"  ✅ 文章已备份: 文章/{english_folder}/{BACKUP_SUBFOLDER}/article-{next_num}/index.html")
        
        # 生成日志文件
        log_md = f"""# 文章生成日志

## 基本信息
- 产品名称: {product_name}
- 英文名称: {english_folder}
- 文章编号: article-{next_num}
- 生成时间: {current_time}
- 文章类型: 市场分析与选型测评

## API 请求
- 请求时间戳: {current_time}

## 生成结果
- API返回长度: {len(result_text)} 字符
- 文章标题: {title}
- 关键词: {keywords_str}

## 输出文件
- HTML: Website/{english_folder}/articles/article-{next_num}/index.html
- 备份: 文章/{english_folder}/{BACKUP_SUBFOLDER}/article-{next_num}/index.html

## 状态
- 状态: ✅ 成功
- 耗时: {time.time() - start_time:.1f} 秒
"""
        # 保存日志到备份目录
        log_path = os.path.join(article_folder, "生成日志.md")
        with file_lock:
            with open(log_path, 'w', encoding='utf-8') as f:
                f.write(log_md)
        
        log_info["success"] = True
        log_info["duration"] = time.time() - start_time
        
    except Exception as e:
        log_info["error_msg"] = str(e)
        print(f"  ❌ 处理出错: {e}")
    
    return log_info


# ================= Git 自动提交 =================

def git_commit_and_push(commit_message):
    """自动提交并推送到远程仓库"""
    import subprocess
    import os
    
    try:
        # 先更新所有产品的文章索引页
        script_dir = os.path.dirname(os.path.abspath(__file__))
        build_script = os.path.join(script_dir, "build_articles_index.py")
        
        print(f"\n🔄 正在更新所有产品的文章索引页...")
        result = subprocess.run(
            ["python3", build_script],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"  ✅ 文章索引更新完成")
        else:
            print(f"  ⚠️ 文章索引更新失败: {result.stderr}")
        
        # git add
        print(f"\n🔄 正在 git add...")
        subprocess.run(["git", "add", "-A"], check=True, capture_output=True)
        
        # git commit
        print(f"📝 正在 git commit...")
        subprocess.run(["git", "commit", "-m", commit_message], check=True, capture_output=True)
        
        # git push with retry
        print(f"🚀 正在推送到远程仓库...")
        max_retries = 3
        retry_delay = 5  # seconds
        
        for attempt in range(max_retries):
            try:
                result = subprocess.run(
                    ["git", "push"], 
                    check=True, 
                    capture_output=True,
                    timeout=120  # 2 minutes timeout
                )
                print(f"✅ Git 提交并推送成功!")
                return True
            except subprocess.CalledProcessError as e:
                error_msg = e.stderr.decode() if e.stderr else str(e)
                if attempt < max_retries - 1:
                    print(f"⚠️  Push 尝试 {attempt + 1} 失败，{retry_delay}秒后重试... ({error_msg[:100]})")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # exponential backoff
                else:
                    print(f"❌ Git 操作失败: {error_msg}")
                    return False
            except subprocess.TimeoutExpired:
                if attempt < max_retries - 1:
                    print(f"⚠️  Push 超时，{retry_delay}秒后重试...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    print(f"❌ Git 操作失败: 超时")
                    return False
            except Exception as e:
                print(f"❌ Git 操作异常: {e}")
                return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Git 操作失败: {e.stderr.decode() if e.stderr else str(e)}")
        return False
    except Exception as e:
        print(f"❌ Git 操作异常: {e}")
        return False


# ================= 主程序入口 =================

print("=" * 60)
print("  市场分析文章生成器 - Market Analysis EN HTML Generator")
print("=" * 60)

print(f"\n📂 正在加载产品参数文件...")
products = load_product_parameters()

if not products:
    print("❌ 未找到任何产品参数文件，程序退出。")
    sys.exit(1)

print(f"\n✅ 共加载 {len(products)} 个产品，开始并行生成市场分析文章（并发数: {MAX_CONCURRENT}）...\n")

# 并行处理
results = []
with ThreadPoolExecutor(max_workers=MAX_CONCURRENT) as executor:
    # 提交所有任务
    future_to_product = {
        executor.submit(process_single_product, name, info): name 
        for name, info in products.items()
    }
    
    # 收集结果（谁先完成谁先返回）
    for future in as_completed(future_to_product):
        result = future.result()
        results.append(result)

# 统计结果
success_count = sum(1 for r in results if r["success"])
error_count = len(results) - success_count

print("\n" + "=" * 60)
print(f"  🎉 任务完成！")
print(f"  ✅ 成功生成: {success_count} 篇")
print(f"  ❌ 失败: {error_count} 篇")
print("=" * 60)

print(f"\n📁 输出目录:")
print(f"   1. {OUTPUT_BASE_DIR}")
print(f"   2. {ARTICLE_BASE_DIR}")
print(f"📂 结构: Website/{{产品英文名}}/articles/article-{{N}}/index.html")
print(f"📂 备份: 文章/{{产品英文名}}/{BACKUP_SUBFOLDER}/article-{{N}}/index.html")

# ================= 保存汇总日志 =================

import json
from datetime import datetime

def save_run_summary(results, success_count, error_count):
    """保存运行汇总到 JSON 文件"""
    # 创建汇总日志目录
    summary_dir = os.path.join(ARTICLE_BASE_DIR, "汇总日志")
    os.makedirs(summary_dir, exist_ok=True)
    
    # 生成时间戳文件名
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}.json"
    filepath = os.path.join(summary_dir, filename)
    
    # 准备汇总数据（简化版）
    simplified_results = []
    for r in results:
        item = {
            "product_name": r["product_name"],
            "success": r["success"]
        }
        if r["success"]:
            item["backup_path"] = r["backup_path"]
        simplified_results.append(item)
    
    summary = {
        "run_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_products": len(results),
        "success_count": success_count,
        "error_count": error_count,
        "results": simplified_results
    }
    
    # 写入 JSON 文件
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"\n📋 汇总日志已保存: {filepath}")
    return filepath

# 保存运行汇总
save_run_summary(results, success_count, error_count)

# 是否自动提交到 Git（True=自动，False=手动）
AUTO_GIT_PUSH = True

if AUTO_GIT_PUSH and success_count > 0:
    print("\n" + "=" * 60)
    commit_msg = f"Auto generate: {success_count} market analysis article(s) updated"
    git_success = git_commit_and_push(commit_msg)
    if git_success:
        print(f"\n🎉 全部完成！Git 已成功推送")
    else:
        print(f"\n⚠️  文章已生成，但 Git 推送失败，请手动检查")
