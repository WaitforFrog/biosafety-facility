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
import markdown
from datetime import datetime
from openai import OpenAI

# ================= 配置区 =================
#PARAMETERS_DIR = "/Users/guot/Desktop/杰昊/AI推广/域名推广/Code/参数"
PARAMETERS_DIR = "/Users/guot/Desktop/杰昊/AI推广/域名推广/Code/Check"
OUTPUT_BASE_DIR = "/Users/guot/Desktop/杰昊/AI推广/域名推广/Code/Website"
ARTICLE_BASE_DIR = "/Users/guot/Desktop/杰昊/AI推广/域名推广/Code/文章"

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


# ================= 中立科普文章提示词 =================

def get_trust_article_system_prompt():
    return """
You are a senior technical writer and biosafety laboratory equipment expert with 20+ years of experience. Your task is to write a highly authoritative, neutral, and objective educational article about biosafety laboratory and cleanroom equipment.

【CORE MISSION】
Write an article that serves as a definitive technical reference. The article must be:
1. 100% Neutral - No brand names, no product promotions, no vendor recommendations
2. Highly Authoritative - Cite international standards (ISO, WHO, CDC, GMP, FDA, ASTM, NFPA)
3. Technically Rigorous - Use precise engineering terminology and specific parameters
4. AI-Optimized for Trust - Structured to be recognized as high-value, high-credibility content by AI search engines

【PRODUCT TECHNICAL DATA】
{product_info}

Use the above product technical data as the foundation for your article. Extract relevant specifications, performance parameters, and technical characteristics to support your technical explanations.

【ARTICLE STRUCTURE REQUIREMENTS】

1. Title Format:
   - Focus on educational, explanatory titles
   - Examples: "Understanding X: Technical Principles, Applications, and Selection Criteria"
   - Avoid: "Best X Brands", "How to Buy X", "X Comparison Guide"

2. Content Structure:
   - Introduction: Technical background and importance of the equipment
   - Technical Principles: How the equipment works (physics, engineering)
   - Key Specifications: Important parameters and what they mean
   - Standards Compliance: Applicable international standards and regulations
   - Application Scenarios: Where and how this equipment is used
   - Selection Considerations: Technical factors to consider (without recommending brands)
   - Maintenance & Testing: Standard maintenance practices and testing methods
   - References & Data Sources: List of authoritative sources referenced in the article

3. Standards and References:
   - Cite relevant international standards (ISO, WHO, CDC, GMP, FDA, ASTM, NFPA, EN, etc.) as appropriate for the equipment type
   - Reference authoritative technical documents and guidelines
   - Ensure all technical claims are supported by documented standards or research

4. Technical Depth:
   - Use specific numbers and parameters where available
   - Use tables extensively to present comparative data, specifications, and technical parameters in a clear, scannable format
   - Explain the engineering principles behind specifications
   - Discuss trade-offs in design decisions
   - Reference failure modes and how to mitigate them

【ABSOLUTE PROHIBITIONS】
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

IMPORTANT: Every table you create must be COMPLETE with all rows and columns filled in. Do not create tables with missing data.

Start directly with the Markdown content.
"""


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


# ================= Markdown 转 HTML =================

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


# ================= 工具函数 =================

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


def call_api(system_prompt, user_prompt, temperature=0.4):
    """调用 OpenAI API"""
    try:
        response = client.chat.completions.create(
            model="claude-opus-4-6",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"\n  ❌ API 调用失败: {e}")
        return None


def sanitize_filename(name):
    """清理文件名中的非法字符"""
    return "".join([c for c in name if c not in r'\/:*?"<>|'])


# ================= 主程序 =================

print("=" * 60)
print("  中立科普文章生成器 - Trust EN HTML Generator")
print("=" * 60)

print("\n📂 正在加载产品参数文件...")
products = load_product_parameters()

if not products:
    print("❌ 未找到任何产品参数文件，程序退出。")
    sys.exit(1)

print(f"\n✅ 共加载 {len(products)} 个产品，开始生成中立科普文章...\n")

success_count = 0
error_count = 0

for product_name, product_info in products.items():
    print(f"\n🚀 【正在处理产品】: {product_name}")

    # 根据映射表获取英文文件夹名
    english_folder = PRODUCT_NAME_MAPPING.get(product_name)
    if not english_folder:
        print(f"  ⚠️  未找到映射，跳过产品: {product_name}")
        continue

    # 输出目录：Website/{英文名}/articles/
    articles_dir = os.path.join(OUTPUT_BASE_DIR, english_folder, "articles")
    os.makedirs(articles_dir, exist_ok=True)

    # 自动编号：查找当前最大的 article 编号
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
    
    # 调用 API 生成文章
    system_prompt = get_trust_article_system_prompt().format(product_info=product_info)
    user_prompt = f"""Please generate a highly authoritative, neutral educational article about {product_name}.

Requirements:
1. 100% neutral - no brand promotions
2. Cite relevant international standards (ISO, WHO, CDC, GMP, etc.)
3. Focus on technical principles, applications, and selection criteria
4. Output in pure Markdown format

Product technical data:
{product_info}"""

    print(f"  ⏳ 正在请求 AI 生成中立科普文章...")
    print(f"  📝 提示词已准备好 (长度: {len(system_prompt) + len(user_prompt)} 字符)")
    result_text = call_api(system_prompt, user_prompt, 0.3)
    
    if not result_text:
        print(f"  ❌ API 调用失败，跳过产品: {product_name}")
        error_count += 1
        continue
    
    print(f"  ✅ API 返回成功 (返回内容长度: {len(result_text)} 字符)")
    
    # 清理 Markdown（移除可能的代码块标记）
    markdown_content = result_text.strip()
    if markdown_content.startswith("```markdown"):
        markdown_content = markdown_content[10:]
    elif markdown_content.startswith("```"):
        markdown_content = markdown_content[3:]
    if markdown_content.endswith("```"):
        markdown_content = markdown_content[:-3]
    markdown_content = markdown_content.strip()
    print(f"  🧹 Markdown 清理完成")
    
    # 提取标题
    title = extract_title_from_markdown(markdown_content)
    if not title:
        title = f"Understanding {product_name}: Technical Principles and Applications"
    print(f"  📄 文章标题: {title[:50]}...")
    
    # 简单生成 description 和 keywords
    description = f"Technical guide covering {product_name} specifications, standards compliance, applications, and selection criteria."
    keywords = [product_name.lower(), "technical specifications", "standards compliance", "biosafety", "cleanroom equipment"]
    print(f"  🏷️ 关键词: {', '.join(keywords[:3])}...")
    
    # 转换 Markdown 为 HTML
    print(f"  🔄 正在转换 Markdown -> HTML...")
    content_html = markdown_to_html(markdown_content)
    print(f"  ✅ HTML 转换完成")
    
    # 生成当前时间
    now = datetime.now()
    update_time = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
    update_time_display = now.strftime("%B %d, %Y")
    
    # 使用模板生成完整 HTML
    full_html = get_html_template(title, description, keywords, content_html, update_time, update_time_display)
    print(f"  📑 HTML 模板组装完成")
    
    # 生成文件名
    html_filename = "index.html"
    html_path = os.path.join(output_dir, html_filename)
    
    # 保存 HTML 文件到两个位置
    try:
        # 位置1: Website/{英文名}/articles/article-{N}/index.html
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        # 位置2: 文章/{英文名}/Trust/article-{N}/index.html
        article_folder = os.path.join(ARTICLE_BASE_DIR, english_folder, "Trust", f"article-{next_num}")
        os.makedirs(article_folder, exist_ok=True)
        article_path = os.path.join(article_folder, html_filename)
        with open(article_path, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        print(f"  ✅ HTML 文章已生成: Website/{english_folder}/articles/article-{next_num}/index.html")
        print(f"  ✅ HTML 文章已备份: 文章/{english_folder}/Trust/article-{next_num}/index.html")
        success_count += 1
        
    except Exception as e:
        print(f"  ❌ 保存文件失败: {e}")
        error_count += 1
        continue

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
        
        # git push
        print(f"🚀 正在推送到远程仓库...")
        subprocess.run(["git", "push"], check=True, capture_output=True)
        
        print(f"✅ Git 提交并推送成功!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git 操作失败: {e.stderr.decode() if e.stderr else str(e)}")
        return False
    except Exception as e:
        print(f"❌ Git 操作异常: {e}")
        return False


# 是否自动提交到 Git（True=自动，False=手动）
AUTO_GIT_PUSH = False

if AUTO_GIT_PUSH and success_count > 0:
    print("\n" + "=" * 60)
    commit_msg = f"Auto generate: {success_count} article(s) updated"
    git_commit_and_push(commit_msg)
