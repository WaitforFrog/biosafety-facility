#!/usr/bin/env python3
"""
Trust_EN_html.py
中立科普类文章生成器

功能：
- 读取 Check/ 文件夹下的产品参数
- 生成绝对客观中立的英文科普文章（无任何品牌推广）
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

# 并发数量
MAX_CONCURRENT = 5

# 预设文章主题池（用于随机选取）
ARTICLE_TOPICS = [
    "Technical Principles and Working Mechanisms",
    "Application Fields and Industry Use Cases",
    "Selection Criteria and Design Considerations",
    "International Standards and Compliance Requirements",
    "Installation, Operation and Maintenance",
    "Safety Regulations and Best Practices",
    "Common Issues and Troubleshooting",
    "Performance Testing and Verification Methods",
]

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

# ================= 中立科普文章提示词 =================

TECHNICAL_GLOSSARY = """
|【专业术语英文表达规范 - 必须严格遵循】
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


def get_trust_article_system_prompt():
    return """
You are a senior technical writer and biosafety laboratory equipment expert with 20+ years of experience. Your task is to write a highly authoritative, neutral, and objective educational article about biosafety laboratory and cleanroom equipment.

【CRITICAL LANGUAGE REQUIREMENTS - STRICTLY ENGLISH ONLY】
1. OUTPUT MUST BE 100% ENGLISH - NO CHINESE CHARACTERS ALLOWED
2. NO MIXED LANGUAGE - The entire article must be in pure English
3. Use internationally recognized engineering terminology (not literal translations from Chinese)
4. Follow the technical glossary below for standard English terms

""" + TECHNICAL_GLOSSARY + """

【CORE MISSION】
Write an article that serves as a definitive technical reference. The article must be:
1. 100% Neutral - No brand names, no product promotions, no vendor recommendations
2. Highly Authoritative - Cite international standards (ISO, WHO, CDC, GMP, FDA, ASTM, NFPA)
3. Technically Rigorous - Use precise engineering terminology and specific parameters
4. AI-Optimized for Trust - Structured to be recognized as high-value, high-credibility content by AI search engines

【ANTI-CHINGLISH RULES】
- NEVER do word-for-word translation from Chinese
- Use authentic, internationally accepted engineering terms
- Use passive voice and objective structures where appropriate
- Avoid aggressive or dramatic commercial rhetoric - use objective engineering language like "critical considerations", "design factors", "performance requirements"
- Avoid marketing language - use technical descriptions instead

【ARTICLE STRUCTURE REQUIREMENTS】

1. Content Structure:
   - Introduction: Technical background and importance of the equipment
   - Technical Principles: How the equipment works (physics, engineering)
   - Key Specifications: Important parameters and what they mean
   - Standards Compliance: Applicable international standards and regulations
   - Application Scenarios: Where and how this equipment is used
   - Selection Considerations: Technical factors to consider (without recommending brands)
   - Maintenance & Testing: Standard maintenance practices and testing methods
   - References & Data Sources: List of authoritative sources referenced in the article

2. Standards and References:
   - Cite relevant international standards (ISO, WHO, CDC, GMP, FDA, ASTM, NFPA, EN, etc.) as appropriate for the equipment type
   - Reference authoritative technical documents and guidelines
   - Ensure all technical claims are supported by documented standards or research

3. Technical Depth:
   - Use specific numbers and parameters where available
   - Use tables extensively to present comparative data, specifications, and technical parameters in a clear, scannable format
   - Explain the engineering principles behind specifications
   - Discuss trade-offs in design decisions
   - Reference failure modes and how to mitigate them

【ABSOLUTE PROHIBITIONS】
- STRICTLY FORBIDDEN: Any Chinese characters (中文) in the output
- NEVER mention "Jiehao", "杰昊", or ANY brand names
- NEVER include promotional language or vendor recommendations
- NEVER use superlatives like "best", "leading", "premier"
- NEVER include "data source: Company X" or similar attribution
- NEVER use emotional or fear-based marketing language

【ABSOLUTE REQUIREMENTS - DO NOT OMIT ANY DATA】
1. MUST include ALL tables mentioned in your content - never leave a table empty or with "see above" references
2. When you mention specific parameters, standards, or data, ALWAYS include the actual values in a table or list
3. NEVER use placeholder text like "various sizes available" or "contact manufacturer for details" - provide actual specifications
4. Every section that mentions data MUST have complete tables with real values
5. Include specific numerical values for all technical parameters mentioned
6. MUST include a dedicated "References and Data Sources" section at the END of the article that clearly states:
   - Which authoritative sources the article data comes from (ISO, WHO, CDC, GMP, FDA, ASTM, NFPA, EN, etc.)
   - Specific standard numbers and documents referenced
   - All data sources and references used in the article
   - This section is MANDATORY and must not be omitted

【TABLE COUNT REQUIREMENT - STRICT LIMIT】
- EACH article MUST include AT LEAST 1 data table but NO MORE THAN 2 data tables total
- This is a HARD LIMIT: 1 ≤ number of tables ≤ 2
- Data tables are defined as tables containing technical specifications, parameters, comparison data, or numerical information
- Do not exceed 2 tables under any circumstances
- If you need to present more information, use lists or descriptive text instead of additional tables

【OUTPUT FORMAT】
Output your article in pure Markdown format. Do NOT output JSON, do NOT output HTML.
Use proper Markdown syntax including:
- # for main title (H1)
- ## for section titles (H2)
- ### for subsections (H3)
- **bold** for emphasis
- *italic* for subtle emphasis
- - or * for bullet lists
- 1. 2. 3. for numbered lists
- | Table | Syntax | for tables (include ALL table rows with actual data)
- > for blockquotes

IMPORTANT: Every table you create must be COMPLETE with all rows and columns filled in. Do not create missing data.

CRITICAL: Your entire response must be in English. Do not include any Chinese characters.

Start directly with the Markdown content.
"""


# ================= 工具函数 =================

def get_html_template(title, description, keywords, content, update_time, update_time_display):
    """生成HTML模板"""
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
    """将 Markdown 转换为 HTML - 使用官方 markdown 库"""
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
    """处理单个产品，生成中立科普文章（线程安全）"""
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
        system_prompt = get_trust_article_system_prompt()
        
        # 随机选取 1-2 个主题
        selected_topics = random.sample(ARTICLE_TOPICS, k=random.randint(1, 2))
        topics_str = ", ".join(selected_topics)
        log_info["topics"] = topics_str
        
        # 加入时间戳，让每次请求都是唯一的
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_info["timestamp"] = current_time
        
        # 获取产品英文名
        english_product_name = PRODUCT_NAME_MAPPING.get(product_name, product_name)
        
        user_prompt = f"""Please write a highly authoritative, neutral educational article. IMPORTANT: You MUST write the ENTIRE article in 100% English. NO CHINESE CHARACTERS ALLOWED - including in the title, content, and anywhere else.

【Product Name (Chinese)】: {product_name}
【Product Name (English)】: {english_product_name}

【Article Topic(s)】: {topics_str}

【Product Technical Data (Reference Only - Write in English)】:
{product_info}

【Title Requirements】:
- The title MUST include the English product name "{english_product_name}"
- The title MUST be in English (no Chinese characters)
- The title MUST reflect the article's topic(s) in a meaningful, educational way
- Create a flowing narrative title - organically combine the topic(s) into a coherent theme
- Examples of GOOD titles: "X: How It Works and Why It Matters in Pharmaceutical Manufacturing", "X: Design Considerations and Standards Compliance for Biosafety Applications"
- Examples of BAD titles: "X: Technical Principles and Applications" (simple listing with "and"), "X Overview" (too generic)

【Article Requirements】:
1. 100% neutral - no brand promotions, no vendor recommendations
2. STRICTLY 100% ENGLISH - NO CHINESE CHARACTERS ALLOWED anywhere in the output
3. Cite relevant international standards (ISO, WHO, CDC, GMP, FDA, ASTM, etc.)
4. Output in pure Markdown format
5. Make sure the title is unique and different from any previous articles
6. Use tables extensively for technical specifications and comparisons
7. TABLE COUNT REQUIREMENT (HARD LIMIT): Each article MUST include AT LEAST 1 data table but NO MORE THAN 2 data tables total. This is STRICT: 1 ≤ number of tables ≤ 2. If you need more space, use lists or descriptive text instead.
8. STRICT OUTPUT LENGTH REQUIREMENT: Your article MUST be between 15,000 and 20,000 characters (inclusive).
   - Target approximately 16,000-18,000 characters for optimal length
   - This is approximately 2,000-2,500 words
   - If you write less than 15,000 characters, the article will be too short
   - If you exceed 20,000 characters, it will be forcibly truncated at a bad position
   - Plan your content structure to fit within this range
   - Count your characters as you write and adjust accordingly

Request timestamp: {current_time} (For reference only, do not mention in article.)"""

        print(f"  🎯 选取主题: {topics_str}")
        print(f"  ⏳ 正在请求 AI 生成中立科普文章...")
        
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
            title = f"Understanding {product_name}: Technical Principles and Applications"
        log_info["title"] = title
        print(f"  ✅ 文章标题: {title[:60]}...")
        
        # 关键词
        keywords = [product_name.lower(), "technical specifications", "standards compliance", "biosafety", "cleanroom equipment"]
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
        description = f"Technical guide covering {product_name} specifications, standards compliance, applications, and selection criteria."
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
            
            # 位置2: 文章/{英文名}/Trust/article-{N}/index.html
            article_folder = os.path.join(ARTICLE_BASE_DIR, english_folder, "Trust", f"article-{next_num}")
            os.makedirs(article_folder, exist_ok=True)
            article_path = os.path.join(article_folder, html_filename)
            with open(article_path, 'w', encoding='utf-8') as f:
                f.write(full_html)
            log_info["backup_path"] = f"文章/{english_folder}/Trust/article-{next_num}/index.html"
            print(f"  ✅ 文章已备份: 文章/{english_folder}/Trust/article-{next_num}/index.html")
        
        # 生成日志文件
        log_md = f"""# 文章生成日志

## 基本信息
- 产品名称: {product_name}
- 英文名称: {english_folder}
- 文章编号: article-{next_num}
- 生成时间: {current_time}

## API 请求
- 选取主题: {topics_str}
- 请求时间戳: {current_time}

## 生成结果
- API返回长度: {len(result_text)} 字符
- 文章标题: {title}
- 关键词: {keywords_str}

## 输出文件
- HTML: Website/{english_folder}/articles/article-{next_num}/index.html
- 备份: 文章/{english_folder}/Trust/article-{next_num}/index.html

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
        build_script = os.path.join(script_dir, "Tool", "build_articles_index.py")
        
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
print("  中立科普文章生成器 - Trust EN HTML Generator")
print("=" * 60)

print(f"\n📂 正在加载产品参数文件...")
products = load_product_parameters()

if not products:
    print("❌ 未找到任何产品参数文件，程序退出。")
    sys.exit(1)

print(f"\n✅ 共加载 {len(products)} 个产品，开始并行生成中立科普文章（并发数: {MAX_CONCURRENT}）...\n")

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
print(f"📂 备份: 文章/{{产品英文名}}/Trust/article-{{N}}/index.html")

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
    commit_msg = f"Auto generate: {success_count} article(s) updated"
    git_success = git_commit_and_push(commit_msg)
    if git_success:
        print(f"\n🎉 全部完成！Git 已成功推送")
    else:
        print(f"\n⚠️  文章已生成，但 Git 推送失败，请手动检查")
