#!/usr/bin/env python3
import os
import re
from pathlib import Path

def is_pure_chinese(html_content):
    """检测HTML内容是否几乎全是中文"""
    # 提取HTML中的文本内容（去除标签）
    text = re.sub(r'<[^>]+>', ' ', html_content)
    # 去除多余空白
    text = re.sub(r'\s+', ' ', text).strip()
    
    if not text:
        return False
    
    # 统计中文字符
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    # 统计英文字母
    english_chars = re.findall(r'[a-zA-Z]', text)
    
    chinese_count = len(chinese_chars)
    english_count = len(english_chars)
    
    # 如果中文字符超过90%且英文少于10%，认为是纯中文
    total = chinese_count + english_count
    if total == 0:
        return False
    
    if chinese_count / total > 0.9 and english_count / total < 0.1:
        return True
    return False

# 扫描所有文章HTML文件
website_root = Path("/Users/guot/Desktop/杰昊/AI推广/域名推广/Code/Website")
chinese_articles = []

for html_file in website_root.rglob("articles/article-*/index.html"):
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if is_pure_chinese(content):
            chinese_articles.append(html_file)
    except Exception as e:
        print(f"Error reading {html_file}: {e}")

print(f"找到 {len(chinese_articles)} 个纯中文文章:\n")
for f in chinese_articles:
    print(f)

# 删除这些文件
print("\n删除这些文件...")
deleted_count = 0
for html_file in chinese_articles:
    try:
        folder = html_file.parent
        html_file.unlink()
        # 如果文件夹为空，删除文件夹
        if not any(folder.iterdir()):
            folder.rmdir()
            print(f"已删除文件夹: {folder}")
        else:
            print(f"已删除文件: {html_file}")
        deleted_count += 1
    except Exception as e:
        print(f"删除失败 {html_file}: {e}")

print(f"\n共删除 {deleted_count} 个纯中文文章")
