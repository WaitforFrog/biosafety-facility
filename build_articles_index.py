#!/usr/bin/env python3
"""
build_articles_index.py
为 Website/<产品>/articles/ 生成静态文章列表页（无 JavaScript fetch）

解决：客户端 fetch 在某些网络环境下失败导致 "No articles found" 的问题
改为：构建时预先生成完整 HTML，直接包含文章列表
"""

import os
import re
from pathlib import Path

WEBSITE_ROOT = Path(__file__).parent / "Website"

# 与现有 index.html 一致的样式
TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{category_name} - Articles</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{description}">
  <meta name="robots" content="index, follow">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.8; color: #333; background: #f5f5f5; }}
    .container {{ max-width: 900px; margin: 0 auto; padding: 20px; background: #fff; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
    header {{ border-bottom: 3px solid #2c3e50; padding-bottom: 20px; margin-bottom: 30px; }}
    h1 {{ font-size: 2em; color: #2c3e50; margin-bottom: 10px; }}
    .category-description {{ color: #666; font-size: 1.1em; }}
    h2 {{ font-size: 1.5em; color: #34495e; margin: 30px 0 15px; padding-bottom: 8px; border-bottom: 1px solid #ecf0f1; }}
    .article-link {{ margin-bottom: 15px; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden; }}
    .article-link summary {{ padding: 15px 20px; background: #f8f9fa; cursor: pointer; font-weight: 600; color: #2c3e50; }}
    .article-link[open] summary {{ background: #e9ecef; }}
    .article-link .article-meta {{ padding: 10px 20px; background: #fff; }}
    .article-link .last-updated {{ color: #7f8c8d; font-size: 0.85em; }}
    .article-link .read-link {{ display: inline-block; margin-top: 10px; color: #3498db; text-decoration: none; }}
    .article-link .read-link:hover {{ text-decoration: underline; }}
    .error {{ color: #e74c3c; }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1 data-entity="category-name">{category_name}</h1>
      <p class="category-description" data-entity="category-description">{description}</p>
    </header>

    <section data-entity="articles-list">
      <h2>Articles</h2>
      <div id="articles-container">
{article_items}
      </div>
    </section>
  </div>
</body>
</html>
'''


def extract_title_and_time(html_path: Path) -> tuple[str, str, str]:
    """从文章 HTML 提取 h1 标题、datetime、显示文本"""
    try:
        text = html_path.read_text(encoding="utf-8")
    except Exception:
        return ("(Untitled)", "", "")
    m = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.DOTALL | re.IGNORECASE)
    title = (m.group(1).strip() if m else "(Untitled)").replace("&", "&amp;").replace("<", "&lt;")
    m2 = re.search(r'<time[^>]*itemprop="dateModified"[^>]*datetime="([^"]*)"[^>]*>([^<]*)</time>', text, re.IGNORECASE)
    if m2:
        return (title, m2.group(1), m2.group(2).strip())
    m3 = re.search(r'<time[^>]*datetime="([^"]*)"[^>]*>([^<]*)</time>', text, re.IGNORECASE)
    if m3:
        return (title, m3.group(1), m3.group(2).strip())
    return (title, "", "")


def slug_to_category(slug: str) -> str:
    """stainless-steel-cleanroom-doors -> Stainless Steel Cleanroom Doors"""
    return slug.replace("-", " ").title()


def build_articles_index(articles_dir: Path) -> bool:
    """为单个产品的 articles 目录生成 index.html"""
    product_slug = articles_dir.parent.name
    category_name = slug_to_category(product_slug)
    description = f"Technical articles and procurement guides for {category_name.lower()}."

    items = []
    for entry in sorted(os.listdir(articles_dir)):
        if not re.match(r"^article-\d+$", entry):
            continue
        slug = entry
        html_path = articles_dir / slug / "index.html"
        if not html_path.exists():
            continue
        title, dt_attr, time_display = extract_title_and_time(html_path)
        items.append({
            "slug": slug,
            "title": title,
            "datetime": dt_attr,
            "time_display": time_display,
        })

    if not items:
        article_items = '        <p class="error">No articles found.</p>'
    else:
        lines = []
        for it in items:
            lines.append(f'''        <details class="article-link" data-slug="{it["slug"]}">
          <summary data-entity="article-title">{it["title"]}</summary>
          <div class="article-meta">
            <p class="last-updated"><time itemprop="dateModified" datetime="{it["datetime"]}">{it["time_display"]}</time></p>
            <a href="{it["slug"]}/index.html" class="read-link" data-entity="link">Read Article</a>
          </div>
        </details>''')
        article_items = "\n".join(lines)

    html = TEMPLATE.format(
        category_name=category_name,
        description=description,
        article_items=article_items,
    )
    out_path = articles_dir / "index.html"
    out_path.write_text(html, encoding="utf-8")
    return len(items) > 0


def main():
    for product_dir in WEBSITE_ROOT.iterdir():
        if not product_dir.is_dir():
            continue
        articles_dir = product_dir / "articles"
        if not articles_dir.is_dir():
            continue
        index_path = articles_dir / "index.html"
        if not index_path.exists():
            continue
        n = len([d for d in articles_dir.iterdir() if d.is_dir() and re.match(r"^article-\d+$", d.name)])
        if n == 0:
            continue
        ok = build_articles_index(articles_dir)
        print(f"{product_dir.name}/articles: {n} articles -> {'OK' if ok else 'empty'}")


if __name__ == "__main__":
    main()
    print("Done.")
