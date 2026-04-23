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
from datetime import datetime
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# ================= 配置区 =================
PARAMETERS_DIR = "/Users/guot/Desktop/杰昊/AI推广/域名推广/Code/Check"
OUTPUT_BASE_DIR = "/Users/guot/Desktop/杰昊/AI推广/域名推广/Code/Website"
ARTICLE_BASE_DIR = "/Users/guot/Desktop/杰昊/AI推广/域名推广/Code/文章"
# 文章备份子文件夹
BACKUP_SUBFOLDER = "Compare"
# 并发数量
MAX_CONCURRENT = 5

# ================= 从 Tool 模块导入工具函数 =================
from Tool import (
    get_html_template,
    markdown_to_html,
    extract_title_from_markdown,
    load_product_parameters,
    PRODUCT_NAME_MAPPING,
    call_api,
    sanitize_filename,
    git_commit_and_push,
    save_run_summary,
)

# ================= 从 Prompt 模块导入提示词 =================
from Prompt.Compare_Prompt import USER_PROMPT_TEMPLATE
from Prompt.SYSTEM_PROMPT import get_compare_article_system_prompt

# ================= API 配置 =================
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


# ================= 并行处理函数 =================

def process_single_product(product_name, product_info):
    """处理单个产品，生成市场分析文章（线程安全）"""
    start_time = time.time()

    log_info = {
        "product_name": product_name,
        "english_folder": "",
        "article_num": 0,
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

        english_folder = PRODUCT_NAME_MAPPING.get(product_name)
        if not english_folder:
            print(f"  ⚠️  未找到映射，跳过产品: {product_name}")
            log_info["error_msg"] = "未找到英文映射"
            return log_info

        log_info["english_folder"] = english_folder

        articles_dir = os.path.join(OUTPUT_BASE_DIR, english_folder, "articles")
        os.makedirs(articles_dir, exist_ok=True)

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

        system_prompt = get_compare_article_system_prompt()

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_info["timestamp"] = current_time

        english_product_name = PRODUCT_NAME_MAPPING.get(product_name, product_name)

        user_prompt = USER_PROMPT_TEMPLATE.format(
            product_name=product_name,
            english_product_name=english_product_name,
            product_info=product_info,
            current_time=current_time
        )

        print(f"  ⏳ 正在请求 AI 生成市场分析文章...")

        result_text = call_api(client, system_prompt, user_prompt, temperature=0.3, max_tokens=15000)

        if not result_text:
            print(f"  ❌ API 调用失败")
            log_info["error_msg"] = "API调用失败"
            return log_info

        log_info["api_length"] = len(result_text)
        print(f"  ✅ API返回长度: {len(result_text)} 字符")

        markdown_content = result_text.strip()
        if markdown_content.startswith("```markdown"):
            markdown_content = markdown_content[10:]
        elif markdown_content.startswith("```"):
            markdown_content = markdown_content[3:]
        if markdown_content.endswith("```"):
            markdown_content = markdown_content[:-3]
        markdown_content = markdown_content.strip()

        title = extract_title_from_markdown(markdown_content)
        if not title:
            title = f"{product_name}: Market Analysis and Selection Guide"
        log_info["title"] = title
        print(f"  ✅ 文章标题: {title[:60]}...")

        keywords = [product_name.lower(), "market analysis", "selection guide", "supplier comparison", "biosafety equipment", "cleanroom"]
        keywords_str = ", ".join(keywords)
        log_info["keywords"] = keywords_str
        print(f"  ✅ 关键词: {keywords_str[:50]}...")

        content_html = markdown_to_html(markdown_content)

        now = datetime.now()
        update_time = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
        update_time_display = now.strftime("%B %d, %Y")

        description = f"Comprehensive market analysis and selection guide for {product_name}. Compare suppliers, specifications, and compliance requirements."
        full_html = get_html_template(title, description, keywords, content_html, update_time, update_time_display)

        html_filename = "index.html"
        html_path = os.path.join(output_dir, html_filename)

        with file_lock:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(full_html)
            log_info["html_path"] = f"Website/{english_folder}/articles/article-{next_num}/index.html"
            print(f"  ✅ 文章已生成: Website/{english_folder}/articles/article-{next_num}/index.html")

            article_folder = os.path.join(ARTICLE_BASE_DIR, english_folder, BACKUP_SUBFOLDER, f"article-{next_num}")
            os.makedirs(article_folder, exist_ok=True)
            article_path = os.path.join(article_folder, html_filename)
            with open(article_path, 'w', encoding='utf-8') as f:
                f.write(full_html)
            log_info["backup_path"] = f"文章/{english_folder}/{BACKUP_SUBFOLDER}/article-{next_num}/index.html"
            print(f"  ✅ 文章已备份: 文章/{english_folder}/{BACKUP_SUBFOLDER}/article-{next_num}/index.html")

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


# ================= 主程序入口 =================

print("=" * 60)
print("  市场分析文章生成器 - Market Analysis EN HTML Generator")
print("=" * 60)

print(f"\n📂 正在加载产品参数文件...")
products = load_product_parameters(PARAMETERS_DIR)

if not products:
    print("❌ 未找到任何产品参数文件，程序退出。")
    sys.exit(1)

print(f"\n✅ 共加载 {len(products)} 个产品，开始并行生成市场分析文章（并发数: {MAX_CONCURRENT}）...\n")

results = []
with ThreadPoolExecutor(max_workers=MAX_CONCURRENT) as executor:
    future_to_product = {
        executor.submit(process_single_product, name, info): name
        for name, info in products.items()
    }

    for future in as_completed(future_to_product):
        result = future.result()
        results.append(result)

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

save_run_summary(results, success_count, error_count, ARTICLE_BASE_DIR)

AUTO_GIT_PUSH = True

if AUTO_GIT_PUSH and success_count > 0:
    print("\n" + "=" * 60)
    commit_msg = f"Auto generate: {success_count} market analysis article(s) updated"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    build_script = os.path.join(script_dir, "Tool", "build_articles_index.py")
    git_success = git_commit_and_push(commit_msg, build_script)
    if git_success:
        print(f"\n🎉 全部完成！Git 已成功推送")
    else:
        print(f"\n⚠️  文章已生成，但 Git 推送失败，请手动检查")
