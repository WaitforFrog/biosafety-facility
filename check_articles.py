#!/usr/bin/env python3
import os

base_path = "/Users/guot/Desktop/杰昊/AI推广/域名推广/Code/Website/biosafety-inflatable-airtight-doors/articles"

# Keywords that indicate a failed or truncated article
FAIL_KEYWORDS = [
    "kiro",
    "无法生成",
    "只能编程",
    "抱歉",
    "对不起，我",
    "I cannot",
    "I'm sorry",
    "I can't",
    "cannot generate",
    "unable to generate",
    "生成失败",
    "错误",
    "Error:",
    "error:",
]

TRUNCATED_PATTERNS = [
    "</article>",
    "</div>",
    "</body>",
    "</html>",
]

def check_article(article_path):
    """Check if an article is good, truncated, or failed."""
    index_path = os.path.join(article_path, "index.html")

    if not os.path.exists(index_path):
        return "missing", "No index.html found"

    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return "error", f"Cannot read file: {e}"

    content_lower = content.lower()

    # Check for failure keywords
    for kw in FAIL_KEYWORDS:
        if kw.lower() in content_lower:
            return "failed", f"Contains failure keyword: {kw}"

    # Check for truncated articles
    # A proper HTML article should have closing tags
    if "</article>" not in content and "</section>" not in content:
        # No article/section closing tag might indicate truncation
        # Check if it ends abruptly (no proper closing structure)
        stripped = content.strip()
        if not stripped.endswith("</div>") and not stripped.endswith("</article>") and not stripped.endswith("</section>"):
            # Check if it has a decent length
            if len(content) < 500:
                return "truncated", f"Very short content ({len(content)} chars), no article closing tag"
            # Check if it ends mid-sentence without proper closure
            lines = content.strip().split('\n')
            last_lines = '\n'.join(lines[-5:]) if len(lines) > 5 else content.strip()
            if last_lines and not any(last_lines.rstrip().endswith(end) for end in ['.', '>', '"', "'", ')', ']', '}', ';', '。', '！', '？']):
                return "truncated", f"Content ends abruptly, no proper closing"

    # More thorough check: if HTML ends without proper closing
    if content.strip().endswith("</div>") or content.strip().endswith("</article>") or content.strip().endswith("</section>"):
        # Good ending, check if there's proper HTML structure
        if "</body>" not in content or "</html>" not in content:
            return "truncated", "Missing closing HTML tags (</body></html>)"

    # Check word count - a good article should have substantial content
    # Remove HTML tags to count actual text
    import re
    text_only = re.sub(r'<[^>]+>', '', content)
    word_count = len(text_only.split())
    char_count = len(text_only)

    if word_count < 50:
        return "truncated", f"Very few words ({word_count})"

    # Check if the article has substantial content
    # Look for common article structure indicators
    has_heading = any(tag in content for tag in ['<h1', '<h2', '<h3'])
    has_paragraphs = content.count('<p>') >= 2

    if not has_heading and word_count < 200:
        return "truncated", f"No headings, low word count ({word_count})"

    if not has_paragraphs and word_count < 300:
        return "truncated", f"Few paragraphs, low word count ({word_count})"

    return "good", f"OK ({word_count} words, {char_count} chars)"

def main():
    articles_dir = base_path
    article_folders = []

    for item in os.listdir(articles_dir):
        item_path = os.path.join(articles_dir, item)
        if os.path.isdir(item_path) and item.startswith("article-"):
            article_folders.append(item)

    article_folders.sort(key=lambda x: int(x.replace("article-", "")))

    print(f"Found {len(article_folders)} article folders\n")

    results = {"good": [], "truncated": [], "failed": [], "error": []}

    for folder in article_folders:
        folder_path = os.path.join(articles_dir, folder)
        status, reason = check_article(folder_path)

        results[status if status in results else "error"].append((folder, reason))

        status_symbol = {"good": "✓", "truncated": "⚠", "failed": "✗", "error": "?"}[status]
        print(f"{status_symbol} {folder}: {reason}")

    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Good: {len(results['good'])}")
    print(f"  Truncated: {len(results['truncated'])}")
    print(f"  Failed: {len(results['failed'])}")
    print(f"  Error: {len(results['error'])}")

    if results['truncated'] or results['failed']:
        to_delete = results['truncated'] + results['failed']
        print(f"\n{'='*60}")
        print(f"Articles to delete ({len(to_delete)}):")
        for folder, reason in to_delete:
            print(f"  - {folder}: {reason}")

if __name__ == "__main__":
    main()
