import os
import pathlib
from datetime import datetime

# 源 Markdown 根目录（所有产品/文章的 EN 版）
SOURCE_ROOT = "/Users/guot/Desktop/杰昊/AI推广/文章"
# 输出 HTML 根目录（本地站点，已切换为 Website 作为主目录）
OUTPUT_ROOT = "/Users/guot/Desktop/杰昊/AI推广/域名推广/Code/Website"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <title>{title}</title>
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
    <style>
        body {{
            max-width: 900px;
            margin: 40px auto;
            padding: 0 20px;
            font-family: -apple-system, BlinkMacSystemFont, \"Segoe UI\", sans-serif;
            line-height: 1.7;
            color: #222;
        }}
        h1, h2, h3, h4 {{
            color: #111;
        }}
        pre, code {{
            font-family: Menlo, Monaco, Consolas, \"Courier New\", monospace;
        }}
        hr {{
            margin: 2em 0;
        }}
        a {{ color: #0b79d0; }}
    </style>
</head>
<body>
    <header>
        <p style=\"font-size: 0.85em; color: #666;\">
            Local preview generated at {generated_at}
        </p>
        <hr>
    </header>
    <main>
    {content}
    </main>
</body>
</html>
"""


def simple_markdown_to_html(md_text: str) -> str:
    """
    一个非常简化的 Markdown 转 HTML：
    - 支持标题: #, ##, ### 开头的行
    - 支持普通段落（按空行分段）
    - 支持无序列表: 以 -, *, + 开头的行
    - 不支持复杂表格 / 代码块，但预览阅读够用
    """
    lines = md_text.splitlines()
    html_lines = []
    in_list = False

    def close_list():
        nonlocal in_list
        if in_list:
            html_lines.append("</ul>")
            in_list = False

    for raw in lines:
        line = raw.rstrip("\n")
        stripped = line.strip()

        # 空行 → 结束段落/列表
        if not stripped:
            close_list()
            html_lines.append("")
            continue

        # 标题
        if stripped.startswith("### "):
            close_list()
            content = stripped[4:].strip()
            html_lines.append(f"<h3>{content}</h3>")
            continue
        if stripped.startswith("## "):
            close_list()
            content = stripped[3:].strip()
            html_lines.append(f"<h2>{content}</h2>")
            continue
        if stripped.startswith("# "):
            close_list()
            content = stripped[2:].strip()
            html_lines.append(f"<h1>{content}</h1>")
            continue

        # 无序列表
        if stripped.startswith(("- ", "* ", "+ ")):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            item = stripped[2:].strip()
            html_lines.append(f"<li>{item}</li>")
            continue

        # 普通段落
        close_list()
        html_lines.append(f"<p>{stripped}</p>")

    close_list()
    # 用换行把所有行拼回去
    return "\n".join(html_lines)


def extract_title_from_markdown(md_text: str, fallback: str) -> str:
    """从 Markdown 文本中提取第一个一级标题作为页面 title，没有就用文件名。"""
    for line in md_text.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line.lstrip("# ").strip()
    return fallback


def build_output_path(md_path: str) -> str:
    """把源 md 路径映射为输出 html 路径，保留产品/引流层/文章标题结构。"""
    rel_path = os.path.relpath(md_path, SOURCE_ROOT)
    rel_without_ext = os.path.splitext(rel_path)[0]
    html_rel_path = rel_without_ext + ".html"
    return os.path.join(OUTPUT_ROOT, html_rel_path)


def convert_md_file(md_path: str):
    """转换单个 *_EN.md 文件为 HTML。"""
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    fallback_title = pathlib.Path(md_path).stem.replace("_EN", "")
    title = extract_title_from_markdown(md_text, fallback=fallback_title)

    # 使用内置的简单 Markdown 转换，避免依赖外部库
    html_body = simple_markdown_to_html(md_text)

    full_html = HTML_TEMPLATE.format(
        title=title,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        content=html_body,
    )

    out_path = build_output_path(md_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"Generated: {out_path}")


def walk_and_build():
    for root, dirs, files in os.walk(SOURCE_ROOT):
        for name in files:
            if not name.endswith("_EN.md"):
                continue
            md_path = os.path.join(root, name)
            convert_md_file(md_path)


if __name__ == "__main__":
    print(f"Source root: {SOURCE_ROOT}")
    print(f"Output root: {OUTPUT_ROOT}")
    walk_and_build()
    print("Done.")
