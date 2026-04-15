"""
HTML 模板与 Markdown 转换工具
"""
import markdown
import re


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
