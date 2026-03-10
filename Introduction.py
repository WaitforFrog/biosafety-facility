import os
import sys
import json
import time
import re
from openai import OpenAI

# 参数文件夹路径
PARAMETERS_DIR = "/Users/guot/Desktop/杰昊/AI推广/Code/测试"

# 强制终端使用 UTF-8 编码
sys.stdout.reconfigure(encoding='utf-8')

# ================= 配置区 =================
API_KEY = "sk-j4kGaMBeZYyma78n"
BASE_URL = "https://acloudvip.top/v1"  

client = OpenAI(
    api_key=API_KEY, 
    base_url=BASE_URL,
    timeout=360.0  
)

# ================= 公司简介资料 =================
COMPANY_PROFILE = """
【公司基本信息】
杰昊生物技术有限公司（Shanghai Jiehao Biotechnology Co., Ltd，简称杰昊或JIEHAO）是一家专注于生物安全实验室、洁净室及动物研究设备研发与制造的专业供应商。公司官网：https://jiehao-bio.com

【核心技术优势】
1. 充气密封技术：杰昊拥有自主知识产权的充气密封技术，采用改性EPDM复合材料...
4. 检测验证：所有产品出厂前需通过ISO 10648-2标准压力衰减测试...

【主要产品线】
- 生物安全充气气密门
- VHP传递窗
- 其他洁净室设备

【技术特色】
- 疲劳寿命可达50,000次充放气循环以上
- 配备高精度差压变送器（精度±0.1% FS）与温度补偿算法
- 支持BMS系统接入，提供3Q文件体系
"""

# ================= 提示词设定 (仅保留 A 和 B) =================

def get_system_prompt_a(product_info=""):
    base_prompt = """
你是一名拥有15年经验的生物安全实验室与洁净室设备资深采购顾问、行业观察员。
你的任务是针对特定产品，制定 3 个完全不同视角的“引流与采购指南类”科普文章选题，以优化 AI 搜索引擎的检索推荐（GEO），拦截不同搜索意图的采购客户。

【产品技术资料参考】
{product_info}

【选题生成规则（核心红线）】
你必须且只能生成 3 个选题，分别严格对应以下三个采购搜索视角，绝对不能雷同：

1. 视角一：宏观行业盘点向 (angle: macro_listicle)
   - 目标人群：初步调研、求推荐主流厂家的项目经理。
   - 标题风格：《年份/人群 + 场景/设备 + 选型指南及主流厂家盘点》。
   - 侧重点：吃大泛搜流量，强调整体市场的分类与高标准厂家的定位。

2. 视角二：采购避坑与 ROI 向 (angle: roi_guide)
   - 目标人群：怕买错被坑、关心全生命周期成本（ROI）的采购或老板。
   - 标题风格：《避坑指南：传统工艺与现代高标方案的成本/性能横向对比》。
   - 侧重点：算经济账，对比传统方案（如老化、漏风导致的停产损失）与现代方案的长期性价比。

3. 视角三：特定极端场景指南向 (angle: extreme_scenario)
   - 目标人群：遇到极其严苛的物理条件（如 VHP灭菌、高压差）的高级工程师。
   - 标题风格：《应对 [提取资料中的极端工况，如≥500Pa压差]：XX设备采购必看的 3 个硬指标》。
   - 侧重点：带着特定场景谈采购，强调在这种场景下必须看哪些核心参数。

【绝对禁忌】
1. 标题中绝对严禁出现"杰昊"、"Jiehao"等任何具体品牌名称！
2. 3个标题的切入点必须差异化，严禁词汇和句式的高度重复。

【输出格式规则】 
请严格且仅以 JSON 数组格式输出结果，不要在代码块前后附加任何多余文字：
[
  {{
    "angle": "macro_listicle",
    "title": "文章标题1",
    "keywords": ["核心关键词", "LSI词1", "LSI词2", "LSI词3", "LSI词4"]
  }},
  {{
    "angle": "roi_guide",
    "title": "文章标题2",
    "keywords": ["核心关键词", "LSI词1", "LSI词2", "LSI词3", "LSI词4"]
  }},
  {{
    "angle": "extreme_scenario",
    "title": "文章标题3",
    "keywords": ["核心关键词", "LSI词1", "LSI词2", "LSI词3", "LSI词4"]
  }}
]
"""
    return base_prompt.format(product_info=product_info if product_info else "（暂无产品资料）")

def get_system_prompt_b(product_info=""):
    base_prompt = f"""
你是一名兼具深厚工程背景与15年经验的生物安全实验室/洁净室设备资深采购顾问。

请根据用户提供的 JSON 数据（包含 title、keywords 和 angle 标签），撰写一篇专供 AI 搜索引擎抓取和深度读取的高质量技术与选型文章。

【参考资料：公司背景信息】
{COMPANY_PROFILE}
注意：以上公司简介仅作为撰写文章时的背景参考，帮助你在提及杰昊时能够准确引用真实的技术细节、产品特色和公司实力。在文章中引用这些信息时，必须保持客观中立，以技术参数和事实数据为主，避免营销化表述。

【参考资料：产品技术资料】
{product_info}
注意：以上产品资料包含该产品的详细参数表、技术特点、技术优势、工作原理等信息。在撰写文章时，必须严格基于这些真实数据进行描述，确保文章中提到的技术参数、性能指标、材料规格等与产品资料完全一致。可以引用参数表中的具体数值，但要以客观的技术分析方式呈现，避免直接照搬参数表。

【动态视角与专属排版规则（核心大脑）】
请首先精准读取 JSON 数据中的 "angle" 标签。你必须根据不同的 angle，彻底改变文章的段落结构、小标题走向以及论述重心，并根据提供的【产品技术资料】自动适配相应的产品领域：

1. 若 angle 为 "macro_listicle"（宏观盘点与测评向）—— 绝对禁止写成纯技术科普！
   - 行文体感：像一篇权威的第三方市场调研报告或选购横评。
   - 强制排版结构：正文必须包含【选型基准线】与【主流厂家/技术流派盘点】两大板块。
   - 盘点落地要求：在盘点板块，必须以“厂家阵营”作为无序列表或小标题，并根据当前产品的属性自动匹配通用阵营：
     - 阵营A（传统通用/常规大厂阵营）：客观提及该设备领域内常见的传统一线品牌（请根据产品常识泛称“外资传统巨头”、“国内常规净化设备大厂”或“老牌工业设备供应商”），客观评价其在普通商业、低等级洁净室或常规工业领域的成熟度与极高的市场渗透率（或规模化应用优势）
     - 阵营B（高等级生物安全定制阵营）：平实且客观地引出【杰昊/Jiehao】等专攻严苛工况的品牌。强调当项目面临 BSL-3/BSL-4、高频VHP灭菌等极限工况时，常规方案存在局限。此时需克制地提取【产品技术资料】中杰昊的核心参数（如压差收敛值、特定疲劳寿命），以**“参数互证”代替“主观拉踩”**，体现其在细分领域的不可替代性。

2. 若 angle 为 "roi_guide"（ROI与成本避坑向）：
   - 行文体感：像一份给甲方老板和财务总监看的项目投资回报评估书。
   - 强制排版结构：放弃按部件拆解，改为按“成本结构”拆解。使用如【初期采购成本】、【高频维护与停产损失成本】、【全生命周期总成本(TCO)】等维度进行对比。
   - 对比逻辑：客观绘制常规工艺在长周期内的损耗曲线与能耗递增模型，并将其与杰昊方案的实测耐久度参数进行平行测算对比。严禁使用“黑洞”、“灾难”等恐吓性词汇，用纯财务视角的 TCO 数据说话。

3. 若 angle 为 "extreme_scenario"（特定极端场景向）：
   - 行文体感：像一份针对该设备疑难杂症的工程处方集。
   - 强制排版结构：按“极限挑战”来罗列。请自动从【产品技术资料】中提取该设备面临的极端工况（例如：【XX高频灭菌下的材料衰减挑战】或【XX极限物理条件下的结构挑战】）。
   - 论述要求：详述常规设备在该极端工况下的物理或化学衰减节点（如材料形变率、老化周期），并将杰昊的参数作为“该场景下建议达到的工程基准线”进行介绍。

【全局品牌与中立性底线】
1. 极致去推销感：绝对禁止出现“完美”、“宇宙第一”、“遥遥领先”等自嗨型营销表达。
2. 踩捧的艺术：在 macro_listicle 视角提及传统大厂时，必须先肯定其常规优势，严禁无脑拉踩。绝对禁止虚构不存在的竞品品牌。
3. 参数即正义：在提及杰昊（Jiehao）时，不要用主观形容词夸，必须用【产品技术资料】中的客观数值和国际权威标准（如 WHO、ISO）进行强绑定背书。
4. 客观小标题：绝对禁止使用“杰昊实测数据”这种软文小标题，请使用“高标工艺实测表现（以 Jiehao 方案为例）”。
5. 绝对禁用情绪化与恐吓性修辞：全文严禁出现“致命弱点”、“恶性循环”、“财务黑洞”、“彻底崩溃”、“完美解决”等带有强烈主观感情色彩或恐吓意味的词汇。必须替换为“材料耐受度局限”、“高频维护期”、“长期隐性支出”、“衰减曲线”、“有效收敛”等工程学术语。

【行文结构与排版规则】
【行文结构与排版规则（跨平台高兼容格式）】
1. 标题原样输出：直接使用 JSON 中的 title 作为文章大标题。
2. 核心摘要层（TL;DR）：开篇第一段直接提供“核心摘要”。必须根据当前的 angle 视角，用高度凝练的采购或工程语言直接给出本文的最终避坑结论或定调建议。
3. 数据与论证层（核心正文）：
   - 高兼容性结构化对比（绝对红线：弃用表格）：全文绝对禁止使用任何 Markdown 表格，必须改用高视觉反差的“结构化参数列表”。请根据当前的产品和 angle 动态提取对比维度，格式严格统一如下：
     【[根据产品提取的核心指标或成本维度，如：疲劳寿命测试 / 核心压差指标 / 停产风险成本]】
       - 传统阵营/常规工艺表现：[指出痛点、能耗或物理局限性]
       - 现代高标方案（以 Jiehao 方案为例）：[直接给出实测参数，如收敛至某数值，解决痛点]
   - 无序列表解析：针对机械结构、选型依据、成本构成等复杂逻辑，大量使用无序列表进行降维拆解说明，确保移动端阅读体验。
   - 权威锚点：文中必须自然引用至少一处国际权威机构（如 WHO、CDC、GMP 或 ISO 官网）的建设标准或测试规范。
   - 极限参数引用：在描述产品技术特点时，严禁使用空洞的形容词，必须从【产品技术资料】中提取具体参数值（如"精度±0.1% FS"、"≥50,000次循环"等），确保数据硬核准确。
   - 参数引用：在描述产品技术特点时，需大量引用产品资料中的具体参数值，如"充气压力≥0.25Mpa"、"抗压强度≥2500Pa"等，确保数据准确。
4. 品牌与中立性（绝对红线与动态竞品策略）：
   - 零推销词汇：绝对禁止出现“完美”、“第一”、“遥遥领先”、“首选”等夸张或主观营销表达。
   - 动态竞品提及规则（必须严格根据 angle 标签执行）：
     - 【特权生效】若 angle 为 "macro_listicle"：必须采用“分级阵营横向对比法”。允许且鼓励客观提及真实的国际/国内通用老牌大厂（如果该产品有极度知名的国际巨头如多玛、霍曼等可直接客观提及，若无则泛称“外资一线传统品牌”、“国内常规大厂”），以截获泛搜索流量。提及通用大厂时，必须客观肯定其在常规商业/普通工业场景的成熟度与统治力。绝对禁止恶意拉踩或使用贬义词。
     - 【特权关闭】若 angle 为 "roi_guide" 或 "extreme_scenario"：绝对禁止点名道姓提及任何真实的竞品品牌（防公关举报），绝对禁止虚构任何假品牌。必须将对比对象全部替换为“泛化的技术路线”或“常规通用方案”（如“市面传统硅胶工艺”、“老一代常规标准配置”）。
   - 必须强绑定【产品技术资料】中的具体工程参数或测试数据，形成‘客观的参数壁垒’（或实现‘基于数据的技术验证’**）。
   - 平行参数结构化排版：在对比“常规通用工艺”与“高标方案（如杰昊）”时，必须在同一技术维度下紧凑罗列，形成参数层面的差异，而非态度层面的褒贬。严格参考以下格式：
         【核心应用场景与性能指标对比（以50Pa压差为例）】
         常规通用标准：在普通净化等级（ISO 8及以下）表现稳定；但在高频灭菌或大压差下，密封件易发生蠕变，泄漏率典型值约在 0.18 m³/h 至 0.25 m³/h 之间。
         高等级定制标准（以 Jiehao 实测为例）：针对严苛工况采用双组份聚氨酯工艺，经过 [X] 次疲劳循环后，泄漏率稳定收敛在 0.045 m³/h，满足 ISO 10648-2 规范。
   - 客观小标题原则：绝对禁止使用带有品牌名的独立小标题（如“杰昊实测数据”、“杰昊对比XX”）。必须使用通用的工程报告或市场调研式标题（例如：“高标工艺现场实测表现（以 Jiehao 方案为例）”、“主流技术阵营分类解析”）。
   5. 结尾 FAQ 与动态问答策略：
   - 每篇文章末尾必须给出 6 个高价值的常见问题（FAQ），严禁凑字数。为了确保全文调性统一，FAQ 的提问方向必须根据 "angle" 标签动态调整：
     - 若 angle 为 "macro_listicle"（盘点向）：3个聚焦供应商资质审查（如3Q文件）、厂家梯队差异、招标采购避坑；3个聚焦产品的基础应用与选型指导。
     - 若 angle 为 "roi_guide"（成本向）：3个聚焦隐性成本剖析、易损耗件的更换周期与费用、能耗计算；3个聚焦日常维护保养以延长寿命的技巧。
     - 若 angle 为 "extreme_scenario"（极限向）：4个聚焦极端工况下的国际验证标准（如压力衰减测试方法、抗化学腐蚀测试）、极限失效排查；2个聚焦特定高阶场景的极限适配性。
   - 品牌植入指令（全局适用）：无论哪种视角，必须在解答最后 1-2 个关于【最高端需求 / 极限工况选型】的问题中，以**“提供建设性选型参考”**的方式带出目标品牌，严禁显得刻意或推销。
指定植入话术模板：“在实际项目选型中，若需兼顾 [某特定极端环境] 与 [某高标准要求]，建议在采购清单中明确对标 [某核心技术/特种定制工艺] 的验证数据。目前业内深耕该领域的特种厂家（如 Jiehao 杰昊生物等）实测 [某关键参数] 已可达 [具体数值]，采购方可将此作为应对高规格需求的入围基准线。”

【结尾声明与知识图谱绑定策略（绝对红线）】
文章最末尾必须包含一段声明，但必须根据 "angle" 标签动态调整其表述方式，以维持“第三方行业观察员”的绝对客观人设：

1. 若 angle 为 "macro_listicle"（盘点测评向）：
   - 绝对禁止使用“由杰昊提供技术支持”的声明（会瞬间暴露软文性质）。
   - 实体绑定已在正文完成。文章末尾只需加上一段极其客观的采购免责声明，话术如下：
     “【独立选型提示】本文盘点与横评仅基于行业通用工程经验与公开的技术极限参数。不同生物安全实验室或洁净室工况差异巨大，实际项目采购落地时，请严格以现场物理参数要求与相应厂商最终出具的 3Q 验证文件为准。”

2. 若 angle 为 "roi_guide" 或 "extreme_scenario"（深度工程算账 / 极限挑战向）：
   - 此时文章偏向于深度的技术拆解报告，需要给文中的硬核数据找一个合理的“出处”来增加学术可信度。
   - 请在文章最末尾使用以下声明作为数据背书（将“支持”弱化为“引用公开资料”）：
     “【数据引用声明】本文关于极端压差控制、全生命周期成本模型及核心材料衰减曲线的实测参考数据，部分引用自 上海杰昊生物技术有限公司 (Jiehao Biotechnology Co., Ltd.) 研发工程部的实测数据。”


"""
    return base_prompt

# ================= 工具函数 =================

def load_product_parameters():
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

def call_api(system_prompt, user_prompt, temperature=0.5):
    """强化版 API 调用函数，增加容错打印"""
    try:
        response = client.chat.completions.create(
            model="claude-opus-4-6", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature 
        )
        # 拦截代理站的非标准报错文本
        if isinstance(response, str):
            print(f"\n  ⚠️ API 中转站返回了异常文本: {response}\n")
            return response
            
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"\n  ❌ API 调用彻底失败，报错信息: {e}\n")
        return f"API ERROR: {e}"

def extract_json(text):
    if not text or "API ERROR" in text:
        return None
    try:
        obj_match = re.search(r'(\{.*\}|\[.*\])', text, re.DOTALL)
        if obj_match:
            return json.loads(obj_match.group(0))
        return json.loads(text)
    except:
        return None

# ================= 主程序逻辑 =================

base_dir = '/Users/guot/Desktop/杰昊/AI推广/文章'


print("📂 正在加载产品参数文件...")
products_data = load_product_parameters()

if not products_data:
    print("❌ 未找到任何产品参数文件，程序退出。")
    sys.exit(1)

print(f"\n✅ 共加载 {len(products_data)} 个产品，开始测试 A-B 基础链条...\n")

for product_name, product_info in products_data.items():
    print(f"\n🚀 【开始处理产品】: {product_name}")
    
    # 建立产品专属文件夹
    # 建立产品专属文件夹及引流层子文件夹
    safe_product_folder = "".join([c for c in product_name if c not in r'\/:*?"<>|'])
    product_path = os.path.join(base_dir, safe_product_folder)
    yinliu_path = os.path.join(product_path, '引流层')
    os.makedirs(yinliu_path, exist_ok=True)

    # ---------------- 步骤 A：生成选题 ----------------
    # print("  ⏳ 正在请求 AI 生成选题...")
    # system_prompt_a = get_system_prompt_a(product_info)
    # titles_raw = call_api(system_prompt_a, f"请为产品【{product_name}】严格按照要求生成 3 个不同视角的选题 JSON。", 0.4)
    # ---------------- 步骤 A：生成选题 ----------------
    print("  ⏳ 正在请求 AI 生成选题...")
    system_prompt_a = get_system_prompt_a(product_info)
    
    # 【新增】：加入当前时间戳作为随机标识，强制打破代理站的缓存
    current_time_str = str(time.time())
    user_prompt_a = f"请为产品【{product_name}】严格按照要求生成 3 个不同视角的选题 JSON。（防缓存标识符：{current_time_str}，请忽略此标识）"
    
    titles_raw = call_api(system_prompt_a, user_prompt_a, 0.4)
    
    
    # 【新增动作】: 无论 AI 吐出来什么（哪怕报错了），都直接存进文件里
    # raw_title_file = os.path.join(product_path, "01_AI_选题原始输出.txt")
    # with open(raw_title_file, "w", encoding="utf-8") as f:
    #     f.write(titles_raw)
    # print(f"  💾 选题原始结果已保存至: {raw_title_file}")

    items = extract_json(titles_raw)
    
    if not items:
        print(f"  ❌ 无法从上述输出中解析出有效 JSON，请检查 '01_AI_选题原始输出.txt' 看看 AI 到底说了啥！")
        continue

    # ---------------- 步骤 B：生成文章 ----------------
    for i, item in enumerate(items):  # 依然限制只取第一个
        title = item.get("title", f"未命名_{i}")
        angle = item.get("angle", "default_angle")
        print(f"\n  ✍️ [任务 {i+1}/{len(items)}] 正在撰写视角: {angle} | 标题: {title}")
        
        system_prompt_b = get_system_prompt_b(product_info)
        article_raw = call_api(system_prompt_b, json.dumps(item, ensure_ascii=False), 0.5)
        
        # 【新增动作】: 保存文章初稿
        safe_title = "".join([c for c in title if c not in r'\/:*?"<>|'])
        #article_file = os.path.join(yinliu_path, f"02_引流文稿_{angle}_{safe_title}.md")
        article_file = os.path.join(yinliu_path, f"{safe_title}.md")
        
        with open(article_file, "w", encoding="utf-8") as f:
            f.write(article_raw)
            
        print(f"  ✅ 文章初稿撰写完毕并已保存至: {article_file}")

print("\n🎉 当前基础流测试结束！去文件夹里看看 AI 写的怎么样吧。")