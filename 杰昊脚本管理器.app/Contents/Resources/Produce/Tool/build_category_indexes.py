import os
import sys
import pathlib
from datetime import datetime
from pathlib import Path

_CODE_ROOT = Path(__file__).resolve().parent.parent
_CODE_ROOT_PARENT = _CODE_ROOT.parent  # 指向 Code 目录（Setting.py 所在）
if str(_CODE_ROOT_PARENT) not in sys.path:
    sys.path.insert(0, str(_CODE_ROOT_PARENT))
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from Setting import WEBSITE_DIR, APP_DIR

"""
根据当前 Website 的结构，为每个「产品 / 引流层」目录生成一个二级 index.html 列表页。

目录结构约定：
Website/
  <产品名>/
    引流层/
      <文章标题>/
        <文章标题>_EN.html

生成结果：
Website/<产品名>/引流层/index.html
  - 标题：产品名 + 引流层文章列表
  - 列出该产品下所有文章标题，并链接到对应 HTML
  - 设计成简单、干净的列表页，适合作为从主页点击后的「二级导航页」

注意：
- 不改动现有文章 HTML，只是新增 / 覆盖 引流层/index.html
- 可以多次运行，重复生成不会有问题
"""

PREVIEW_ROOT = str(WEBSITE_DIR)


def find_article_pages(yinliu_dir: str):
    """
    在某个 引流层 目录下，找出所有文章 HTML：
    返回列表：[(文章标题, 相对路径)]，相对路径从该 引流层 目录出发。
    """
    items = []
    for entry in sorted(os.listdir(yinliu_dir)):
        entry_path = os.path.join(yinliu_dir, entry)
        if not os.path.isdir(entry_path):
            continue

        # 子目录名即文章标题目录
        article_dir = entry_path
        # 在该子目录中找 *_EN.html
        html_name = None
        for fname in os.listdir(article_dir):
            if fname.endswith(".html"):
                html_name = fname
                break
        if not html_name:
            continue

        rel_path = os.path.join(entry, html_name)
        # 去掉 _EN 后缀，更像中文/完整标题
        title = pathlib.Path(html_name).stem.replace("_EN", "")
        items.append((title, rel_path))
    return items


def build_category_index(product_dir: str, yinliu_dir: str):
    """
    为某个产品的 引流层 目录生成 index.html。
    """
    product_name = pathlib.Path(product_dir).name
    articles = find_article_pages(yinliu_dir)

    if not articles:
        return

    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 简洁的二级列表页模板
    html_lines = [
        "<!DOCTYPE html>",
        "<html lang=\"zh-CN\">",
        "<head>",
        "  <meta charset=\"UTF-8\">",
        f"  <title>{product_name} · 引流文章列表</title>",
        "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">",
        "  <style>",
        "    :root {",
        "      --bg: #020617;",
        "      --card: #0b1120;",
        "      --border: rgba(148, 163, 184, 0.5);",
        "      --accent: #38bdf8;",
        "      --text-main: #e5e7eb;",
        "      --text-soft: #9ca3af;",
        "    }",
        "    * { box-sizing: border-box; }",
        "    body {",
        "      margin: 0;",
        "      min-height: 100vh;",
        "      font-family: system-ui, -apple-system, BlinkMacSystemFont, \"SF Pro Text\", \"Segoe UI\", sans-serif;",
        "      background: radial-gradient(130% 180% at 10% 0%, #0f172a 0%, #020617 45%, #020617 100%);",
        "      color: var(--text-main);",
        "      -webkit-font-smoothing: antialiased;",
        "    }",
        "    .page {",
        "      max-width: 960px;",
        "      margin: 0 auto;",
        "      padding: 32px 18px 48px;",
        "    }",
        "    header {",
        "      margin-bottom: 20px;",
        "    }",
        "    h1 {",
        "      font-size: 22px;",
        "      margin: 0 0 8px;",
        "    }",
        "    .meta {",
        "      font-size: 12px;",
        "      color: var(--text-soft);",
        "    }",
        "    .card {",
        "      margin-top: 20px;",
        "      border-radius: 16px;",
        "      border: 1px solid var(--border);",
        "      background: radial-gradient(circle at 0 0, rgba(56, 189, 248, 0.18), transparent 60%), var(--card);",
        "      padding: 16px 16px 14px;",
        "      box-shadow: 0 22px 60px rgba(15, 23, 42, 0.9);",
        "    }",
        "    .card-title {",
        "      font-size: 13px;",
        "      letter-spacing: 0.14em;",
        "      text-transform: uppercase;",
        "      color: var(--text-soft);",
        "      margin-bottom: 10px;",
        "    }",
        "    ul.list {",
        "      list-style: none;",
        "      margin: 0;",
        "      padding: 0;",
        "      display: flex;",
        "      flex-direction: column;",
        "      gap: 8px;",
        "      font-size: 14px;",
        "    }",
        "    .list li {",
        "      display: flex;",
        "      align-items: flex-start;",
        "      gap: 8px;",
        "    }",
        "    .dot {",
        "      width: 6px;",
        "      height: 6px;",
        "      border-radius: 999px;",
        "      margin-top: 7px;",
        "      background: var(--accent);",
        "      flex-shrink: 0;",
        "    }",
        "    a {",
        "      color: var(--text-main);",
        "      text-decoration: none;",
        "      border-bottom: 1px solid transparent;",
        "      padding-bottom: 1px;",
        "    }",
        "    a:hover {",
        "      color: #f9fafb;",
        "      border-bottom-color: rgba(56, 189, 248, 0.8);",
        "    }",
        "    .back {",
        "      display: inline-flex;",
        "      align-items: center;",
        "      gap: 4px;",
        "      font-size: 12px;",
        "      color: var(--text-soft);",
        "      margin-bottom: 12px;",
        "    }",
        "  </style>",
        "</head>",
        "<body>",
        '  <div class="page">',
        '    <a class="back" href="../..">&#8592; 返回首页矩阵</a>',
        "    <header>",
        f"      <h1>{product_name} · 引流文章列表</h1>",
        f"      <div class=\"meta\">共 {len(articles)} 篇 · 最近生成于 {generated_at}</div>",
        "    </header>",
        '    <section class="card">',
        '      <div class="card-title">Articles · 引流文章</div>',
        '      <ul class="list">',
    ]

    for title, rel_path in articles:
        html_lines.append("        <li>")
        html_lines.append('          <span class="dot"></span>')
        html_lines.append(f'          <a href="{rel_path}">{title}</a>')
        html_lines.append("        </li>")

    html_lines.extend(
        [
            "      </ul>",
            "    </section>",
            "  </div>",
            "</body>",
            "</html>",
        ]
    )

    out_path = os.path.join(yinliu_dir, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html_lines))

    rel_for_log = os.path.relpath(out_path, PREVIEW_ROOT)
    print(f"Generated: {rel_for_log}")


def walk_and_build():
    """
    遍历 preview_site，找到所有「*/引流层」目录并生成 index.html。
    """
    for root, dirs, files in os.walk(PREVIEW_ROOT):
        base = os.path.basename(root)
        if base == "引流层":
            product_dir = os.path.dirname(root)
            build_category_index(product_dir, root)


if __name__ == "__main__":
    print(f"Preview root: {PREVIEW_ROOT}")
    walk_and_build()
    print("Done.")

