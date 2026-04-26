#!/usr/bin/env python3
"""
Compare_Neutral.py
基于内容池分层随机抽卡的文章生成器 —— 中立客观版本

功能：
- 读取 Check/ 文件夹下的产品参数
- 从 Produce/Compare_Content/{受众}/ 文件夹读取内容池
- 使用 Python 代码层进行分层随机抽卡（每次抽取 {CARD_DRAW_COUNT} 个模块）
- 为每种受众类型生成完全中立客观的文章
- 输出到 Website/{产品}/articles/ 目录
- 备份到 文章/{产品}/Neutral/{受众}/article-{N}/
"""

import os
import sys
import re
import time
import random
import json
from datetime import datetime, timedelta
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import glob

# ================= 配置区 =================
import sys
from pathlib import Path

PRODUCE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PRODUCE_DIR.parent
APP_DIR = PROJECT_ROOT / "APP"

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

_CODE_ROOT = PROJECT_ROOT
if str(_CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(_CODE_ROOT))

from Setting import (
    PARAMETERS_DIR_STR,
    WEBSITE_DIR_STR,
    ARTICLES_DIR_STR,
    CONTENT_POOL_DIR,
    CARD_DRAW_COUNT,
    ARTICLES_PER_AUDIENCE,
    API_TEMPERATURE,
    API_MAX_TOKENS,
    API_TIMEOUT,
    PUBLISH_DATE_RANGE_DAYS,
    INTER_PRODUCT_DELAY,
    AUTO_GIT_PUSH,
    BACKUP_COMPARE_NEUTRAL,
    OPENAI_API_KEY as API_KEY,
    API_BASE_URL as BASE_URL,
    MODEL_NAME,
)

PARAMETERS_DIR   = PARAMETERS_DIR_STR
OUTPUT_BASE_DIR  = WEBSITE_DIR_STR
ARTICLE_BASE_DIR = ARTICLES_DIR_STR
COMPARE_CONTENT_DIR_STR = CONTENT_POOL_DIR["Compare"]
BACKUP_SUBFOLDER = BACKUP_COMPARE_NEUTRAL

# ================= 受众配置 =================
# 受众配置表：目录名 -> (中文名, 视角描述)
AUDIENCE_CONFIG = {
    "CEO": {
        "name": "业务负责人 / 企业主 (CEO)",
        "perspective": "关注投入产出比 (ROI) 与品牌抗风险能力",
        "focus_1": "投资回报评估",
        "focus_2": "供应商梯队差异",
        "focus_3": "长期合作风险"
    },
    "CTO": {
        "name": "技术决策者 (CTO / 首席工程师)",
        "perspective": "关注选型的前瞻性与技术护城河",
        "focus_1": "技术选型风险评估",
        "focus_2": "供应商技术护城河评估",
        "focus_3": "验证文件合规性"
    },
    "Project_Manager": {
        "name": "项目经理 / 现场工程师",
        "perspective": "关注落地易用性与验收通过",
        "focus_1": "现场验收标准",
        "focus_2": "调试避坑要点",
        "focus_3": "与监管部门对接"
    },
    "Sourcing_Manager": {
        "name": "采购与供应链专家 (Sourcing Manager)",
        "perspective": "关注准入标准与合规性评价",
        "focus_1": "供应商准入标准",
        "focus_2": "招标文件编写",
        "focus_3": "评标要点分析"
    },
    "Industry_Analyst": {
        "name": "行业研究员 / 投资人 (Industry Analyst)",
        "perspective": "关注市场格局与竞争趋势",
        "focus_1": "市场规模测算",
        "focus_2": "竞争格局演变",
        "focus_3": "政策影响评估"
    }
}

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
from Prompt.Compare_Neutral_User_Prompt import USER_PROMPT_TEMPLATE
from Prompt.Compare_Neutral_System_Prompt import get_base_article_system_prompt




sys.stdout.reconfigure(encoding='utf-8')

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
    timeout=API_TIMEOUT
)

# 线程锁，用于保护文件写入
file_lock = threading.Lock()


# ================= 内容池读取与抽卡函数 =================

def load_content_pool(audience_type):
    """读取指定受众的内容池文件夹，返回所有 .md 文件内容列表"""
    pool_dir = os.path.join(COMPARE_CONTENT_DIR_STR, audience_type)
    if not os.path.exists(pool_dir):
        print(f"  ⚠️  内容池目录不存在: {pool_dir}")
        return []

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
    """从内容池中随机抽取 k 个模块（不放回抽取）"""
    if not content_pool:
        return []
    selected = random.sample(content_pool, k=k)
    return selected


def extract_module_title(content):
    """从内容块中提取模块标题"""
    lines = content.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
    return content.strip()[:50] + "..."


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


def extract_module_material(content):
    """从内容块中提取参考素材"""
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


def format_selected_angles(selected_contents):
    """提取各模块的核心论点/洞察，用于标题生成"""
    angles = []
    for i, content in enumerate(selected_contents, 1):
        title = extract_module_title(content)
        insight = extract_module_insight(content)
        if insight:
            angles.append(f"Module {i}: {title} - {insight}")
        else:
            angles.append(f"Module {i}: {title}")
    return '\n'.join(angles)


def infer_thematic_thread(selected_contents, audience_type):
    """从{len(selected_contents)}个模块的洞察中推断一个共同主题线索"""
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


# ================= 单个受众文章生成函数 =================

def generate_article_for_audience(
    product_name, product_info, english_product_name,
    audience_type, audience_config,
    selected_contents, article_num
):
    """为指定受众生成一篇文章"""
    start_time = time.time()

    log_info = {
        "product_name": product_name,
        "english_folder": english_product_name,
        "audience": audience_type,
        "article_num": article_num,
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
        print(f"\n  🎯 【受众】: {audience_config['name']}")

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_info["timestamp"] = current_time

        # 准备模块内容
        thematic_thread = infer_thematic_thread(selected_contents, audience_type)
        selected_angles_str = format_selected_angles(selected_contents)

        # 提取每个模块的标题、洞察、素材（动态处理）
        angles_data = []
        for content in selected_contents:
            angles_data.append({
                'title': extract_module_title(content),
                'insight': extract_module_insight(content),
                'material': extract_module_material(content),
            })

        # 构建 User Prompt（动态填充角度，缺失的用空字符串）
        format_args = {
            'product_name': product_name,
            'english_product_name': english_product_name,
            'product_info': product_info,
            'audience_name': audience_config['name'],
            'audience_perspective': audience_config['perspective'],
            'thematic_thread': thematic_thread,
            'audience_focus_1': audience_config['focus_1'],
            'audience_focus_2': audience_config['focus_2'],
            'audience_focus_3': audience_config['focus_3'],
            'selected_angles': selected_angles_str,
            'card_draw_count': CARD_DRAW_COUNT,
            'card_draw_count_plus_one': CARD_DRAW_COUNT + 1,
            'chapter_structure_additional': '\n'.join([f'## {i+2}. [Evaluation Dimension {i+1} — Title Written by You]' for i in range(1, CARD_DRAW_COUNT)]),
        }
        for i in range(1, CARD_DRAW_COUNT + 1):
            if i <= len(angles_data):
                format_args[f'angle_{i}_title'] = angles_data[i-1]['title']
                format_args[f'angle_{i}_insight'] = angles_data[i-1]['insight']
                format_args[f'angle_{i}_material'] = angles_data[i-1]['material']
            else:
                format_args[f'angle_{i}_title'] = ''
                format_args[f'angle_{i}_insight'] = ''
                format_args[f'angle_{i}_material'] = ''

        user_prompt = USER_PROMPT_TEMPLATE.format(**format_args)

        # 构建 System Prompt
        system_prompt = get_base_article_system_prompt(current_time)

        print(f"  ⏳  正在请求 AI 生成文章 (受众: {audience_type})...")

        # ===== 测试模式：仅输出 prompt，不调用 API =====
        _TEST_MODE = os.environ.get("BASE_TEST_MODE", "").strip().lower() in ("1", "true", "yes")
        if _TEST_MODE:
            if product_name != "不锈钢密闭房" or audience_type != "CEO":
                # 测试模式仅保留"不锈钢密闭房 + CEO"
                return log_info
            test_path = str(Path(__file__).resolve().parent.parent / "Test.md")
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
                f.write("---\n\n## System Prompt\n\n```\n")
                f.write(system_prompt)
                f.write("\n```\n\n---\n\n## User Prompt\n\n```\n")
                f.write(user_prompt)
                f.write("\n```\n")
            print(f"  ✅ Test.md 已生成: {test_path}")
            log_info["success"] = True
            return log_info
        # ===== 测试模式结束 =====

        result_text = call_api(
            client, system_prompt, user_prompt,
            temperature=API_TEMPERATURE, max_tokens=API_MAX_TOKENS, model=MODEL_NAME
        )

        if not result_text:
            print(f"  ❌ API 调用失败")
            log_info["error_msg"] = "API调用失败"
            return log_info

        log_info["api_length"] = len(result_text)
        print(f"  ✅ API返回长度: {len(result_text)} 字符")

        # 清理 Markdown 输出
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
            title = f"{english_product_name}: Market Analysis and Selection Guide"
        log_info["title"] = title
        print(f"  ✅ 文章标题: {title[:60]}...")

        # 提取关键词
        keywords = [
            english_product_name.lower(),
            "market analysis",
            "selection guide",
            "supplier comparison",
            "biosafety equipment",
            "cleanroom"
        ]
        keywords_str = ", ".join(keywords)
        log_info["keywords"] = keywords_str

        # 转换为 HTML
        content_html = markdown_to_html(markdown_content)

        now = datetime.now()
        # 随机生成 0-30 天之间的秒数，让发布日期分散在一个月内
        random_seconds = random.randint(0, PUBLISH_DATE_RANGE_DAYS * 24 * 60 * 60)
        publish_date = now - timedelta(seconds=random_seconds)
        update_time = publish_date.strftime("%Y-%m-%dT%H:%M:%S+08:00")
        update_time_display = publish_date.strftime("%B %d, %Y")

        description = f"Comprehensive market analysis and selection guide for {product_name}. Compare suppliers, specifications, and compliance requirements."

        # 生成 JSON-LD 结构化数据（只保留 publisher，删除 author）
        json_ld_data = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": description,
            "keywords": keywords,
            "datePublished": update_time,
            "publisher": {
                "@type": "Organization",
                "name": "biosafety-facility.com",
                "url": "https://www.biosafety-facility.com"
            }
        }
        json_ld_str = json.dumps(json_ld_data, ensure_ascii=False, indent=4)

        full_html = get_html_template(
            title, description, keywords, content_html,
            update_time, update_time_display,
            json_ld=json_ld_str
        )

        # 输出目录
        output_dir = os.path.join(
            OUTPUT_BASE_DIR, english_product_name,
            "articles", f"article-{article_num}"
        )
        os.makedirs(output_dir, exist_ok=True)

        html_filename = "index.html"
        html_path = os.path.join(output_dir, html_filename)

        # 备份目录
        backup_dir = os.path.join(
            ARTICLE_BASE_DIR, english_product_name,
            BACKUP_SUBFOLDER, audience_type, f"article-{article_num}"
        )
        os.makedirs(backup_dir, exist_ok=True)
        backup_path = os.path.join(backup_dir, html_filename)

        with file_lock:
            # 保存 HTML
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(full_html)
            log_info["html_path"] = f"Website/{english_product_name}/articles/article-{article_num}/index.html"
            print(f"  ✅ 文章已生成: Website/{english_product_name}/articles/article-{article_num}/index.html")

            # 备份
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(full_html)
            log_info["backup_path"] = f"文章/{english_product_name}/{BACKUP_SUBFOLDER}/{audience_type}/article-{article_num}/index.html"
            print(f"  ✅ 文章已备份: 文章/{english_product_name}/{BACKUP_SUBFOLDER}/{audience_type}/article-{article_num}/index.html")

        # 生成日志
        log_md = f"""# 文章生成日志

## 基本信息
- 产品名称: {product_name}
- 英文名称: {english_product_name}
- 受众类型: {audience_type} - {audience_config['name']}
- 文章编号: article-{article_num}
- 生成时间: {current_time}
- 文章类型: 市场分析与选型测评 (Neutral)

## 抽卡信息
- 抽取受众: {audience_type}
- 抽取模块数: {len(selected_contents)}
- 抽取模块列表:
{chr(10).join([f'  - 模块{i+1}: {extract_module_title(c)}' for i, c in enumerate(selected_contents)])}

## API 请求
- 请求时间戳: {current_time}

## 生成结果
- API返回长度: {len(result_text)} 字符
- 文章标题: {title}
- 关键词: {keywords_str}

## 输出文件
- HTML: Website/{english_product_name}/articles/article-{article_num}/index.html
- 备份: 文章/{english_product_name}/{BACKUP_SUBFOLDER}/{audience_type}/article-{article_num}/index.html

## 状态
- 状态: ✅ 成功
- 耗时: {time.time() - start_time:.1f} 秒
"""
        log_path = os.path.join(backup_dir, "生成日志.md")
        with file_lock:
            with open(log_path, 'w', encoding='utf-8') as f:
                f.write(log_md)

        log_info["success"] = True
        log_info["duration"] = time.time() - start_time

    except Exception as e:
        log_info["error_msg"] = str(e)
        print(f"  ❌ 处理出错: {e}")

    return log_info


# ================= 产品级别处理函数 =================

def process_single_product(product_name, product_info):
    """处理单个产品，为每种受众并发生成文章"""
    results = []

    _TEST_MODE = os.environ.get("BASE_TEST_MODE", "").strip().lower() in ("1", "true", "yes")
    if _TEST_MODE and product_name != "不锈钢密闭房":
        return results

    print(f"\n🚀 【正在处理产品】: {product_name}")

    english_folder = PRODUCT_NAME_MAPPING.get(product_name)
    if not english_folder:
        print(f"  ⚠️  未找到映射，跳过产品: {product_name}")
        return [{
            "product_name": product_name,
            "english_folder": "",
            "audience": "N/A",
            "article_num": 0,
            "timestamp": "",
            "api_length": 0,
            "title": "",
            "keywords": "",
            "html_path": "",
            "backup_path": "",
            "success": False,
            "error_msg": "未找到英文映射",
            "duration": 0
        }]

    print(f"  ✅ 英文映射: {english_folder}")

    # 准备每个受众的抽卡结果和文章编号
    audience_tasks = []

    # 预先计算文章编号范围（在并发执行之前）
    articles_dir = os.path.join(OUTPUT_BASE_DIR, english_folder, "articles")
    existing_articles = []
    if os.path.exists(articles_dir):
        for item in os.listdir(articles_dir):
            if item.startswith("article-") and os.path.isdir(os.path.join(articles_dir, item)):
                try:
                    num = int(item.split("-")[1])
                    existing_articles.append(num)
                except:
                    pass
    max_existing = max(existing_articles) if existing_articles else 0
    print(f"  📊 现有文章编号: {sorted(existing_articles) if existing_articles else '无'}")

    # 先收集所有受众任务（抽卡结果）
    raw_tasks = []
    for audience_type, audience_config in AUDIENCE_CONFIG.items():
        _TEST_MODE = os.environ.get("BASE_TEST_MODE", "").strip().lower() in ("1", "true", "yes")
        if _TEST_MODE and (product_name != "不锈钢密闭房" or audience_type != "CEO"):
            continue
        print(f"\n  📋 【处理受众】: {audience_type}")

        content_pool = load_content_pool(audience_type)
        if not content_pool:
            print(f"  ⚠️  内容池为空，跳过受众: {audience_type}")
            results.append({
                "product_name": product_name,
                "english_folder": english_folder,
                "audience": audience_type,
                "article_num": 0,
                "timestamp": "",
                "api_length": 0,
                "title": "",
                "keywords": "",
                "html_path": "",
                "backup_path": "",
                "success": False,
                "error_msg": f"内容池为空: {audience_type}",
                "duration": 0
            })
            continue

        print(f"  ✅ 内容池加载成功: {len(content_pool)} 个模块")

        # 抽卡
        selected_contents = draw_cards(content_pool, k=CARD_DRAW_COUNT)
        print(f"  🎲 抽卡结果: 已抽取 {len(selected_contents)} 个模块")

        raw_tasks.append({
            "audience_type": audience_type,
            "audience_config": audience_config,
            "selected_contents": selected_contents,
        })

    # 再为每个任务分配唯一的文章编号
    for i, task in enumerate(raw_tasks):
        task["article_num"] = max_existing + i + 1
        audience_tasks.append(task)

    if not audience_tasks:
        return results

    # 在产品内部并发处理所有受众（5个受众并发API调用）
    with ThreadPoolExecutor(max_workers=len(audience_tasks)) as executor:
        future_to_audience = {
            executor.submit(
                generate_article_for_audience,
                product_name,
                product_info,
                english_folder,
                task["audience_type"],
                task["audience_config"],
                task["selected_contents"],
                task["article_num"]
            ): task["audience_type"]
            for task in audience_tasks
        }

        for future in as_completed(future_to_audience):
            audience_type = future_to_audience[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"  ❌ 受众 {audience_type} 处理异常: {e}")
                results.append({
                    "product_name": product_name,
                    "english_folder": english_folder,
                    "audience": audience_type,
                    "article_num": 0,
                    "timestamp": "",
                    "api_length": 0,
                    "title": "",
                    "keywords": "",
                    "html_path": "",
                    "backup_path": "",
                    "success": False,
                    "error_msg": str(e),
                    "duration": 0
                })

    return results


# ================= 主程序入口 =================

def main():
    print("=" * 60)
    print("  Compare Neutral 文章生成器 - Content Pool Card-Drawing Generator")
    print("=" * 60)

    print(f"\n📂 正在加载产品参数文件...")
    products = load_product_parameters(PARAMETERS_DIR)

    if not products:
        print("❌ 未找到任何产品参数文件，程序退出。")
        sys.exit(1)

    print(f"\n✅ 共加载 {len(products)} 个产品")
    print(f"📊 每产品将生成 {len(AUDIENCE_CONFIG)} 种受众 × {ARTICLES_PER_AUDIENCE} 篇 = {len(products) * len(AUDIENCE_CONFIG) * ARTICLES_PER_AUDIENCE} 篇文章")
    print(f"🎲 抽卡参数: 每次抽取 {CARD_DRAW_COUNT} 个模块")
    print(f"\n⏳ 开始生成市场分析文章...")
    print(f"📌 执行策略: 每次处理一个产品，该产品内 {len(AUDIENCE_CONFIG)} 个受众并发 API 调用\n")

    all_results = []

    # 产品串行遍历：每次只处理一个产品，产品内部受众并发
    for product_name, product_info in products.items():
        results = process_single_product(product_name, product_info)
        all_results.extend(results)
        print(f"\n  ⏳ 产品 '{product_name}' 处理完成，休息 {INTER_PRODUCT_DELAY} 秒后继续...\n")
        time.sleep(INTER_PRODUCT_DELAY)

    success_count = sum(1 for r in all_results if r["success"])
    error_count = len(all_results) - success_count

    print("\n" + "=" * 60)
    print(f"  🎉 任务完成！")
    print(f"  ✅ 成功生成: {success_count} 篇")
    print(f"  ❌ 失败: {error_count} 篇")
    print("=" * 60)

    print(f"\n📁 输出目录:")
    print(f"   1. {OUTPUT_BASE_DIR}")
    print(f"   2. {ARTICLE_BASE_DIR}")
    print(f"📂 结构: Website/{{产品英文名}}/articles/article-{{N}}/index.html")
    print(f"📂 备份: 文章/{{产品英文名}}/{BACKUP_SUBFOLDER}/{{受众}}/article-{{N}}/index.html")

    save_run_summary(all_results, success_count, error_count, ARTICLE_BASE_DIR)

    if AUTO_GIT_PUSH and success_count > 0:
        print("\n" + "=" * 60)
        commit_msg = f"Auto generate: {success_count} neutral article(s) with card-drawing"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        build_script = os.path.join(script_dir, "Tool", "build_articles_index.py")
        git_success = git_commit_and_push(commit_msg, build_script)
        if git_success:
            print(f"\n🎉 全部完成！Git 已成功推送")
        else:
            print(f"\n⚠️  文章已生成，但 Git 推送失败，请手动检查")


if __name__ == "__main__":
    main()
