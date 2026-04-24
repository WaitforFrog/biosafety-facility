#!/usr/bin/env python3
import os
import re

base_path = "/Users/guot/Desktop/杰昊/AI推广/域名推广/Code/Website/biosafety-inflatable-airtight-doors/articles"

# Specific patterns that indicate a FAILED article generation
# These are patterns that would NOT appear in legitimate article content
FAIL_PATTERNS = [
    (r"kiro", "AI identifier 'kiro' found"),
    (r"无法生成", "Chinese: cannot generate article"),
    (r"只能编程", "Chinese: can only code"),
    (r"抱歉.{0,30}生成", "Apology about unable to generate"),
    (r"对不起.{0,30}生成", "Apology about unable to generate"),
    (r"I am (a )?(kiro|AI|人工智能)", "AI self-identification"),
    (r"I'?m (a )?kiro", "AI self-identification 'kiro'"),
    (r"我是kiro", "Chinese: I am kiro"),
    (r"我是一个.{0,20}(AI|人工智能|模型|编程)", "AI self-description"),
    (r"生成失败", "Article generation failed"),
    (r"系统错误", "System error"),
    (r"请求超时", "Request timeout"),
    (r"网络错误", "Network error"),
    (r"API.{0,20}错误", "API error"),
    (r"Failed to generate", "Failed to generate"),
    (r"Unable to (generate|create|write)", "Unable to generate content"),
    (r"Can'?t (help|assist|generate)", "Cannot help"),
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

    # Check for failure patterns
    for pattern, description in FAIL_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            return "failed", description

    # Check for truncation - article should have proper HTML structure
    content_lower = content.lower()

    # Remove HTML tags to count actual text
    text_only = re.sub(r'<[^>]+>', '', content)
    word_count = len(text_only.split())
    char_count = len(text_only.strip())

    # Very short articles might be truncated
    if word_count < 100:
        return "truncated", f"Very short content ({word_count} words)"

    # Check if article has basic structure
    has_h1 = bool(re.search(r'<h1[^>]*>', content, re.IGNORECASE))
    has_paragraphs = content.count('<p') >= 2

    if not has_h1 and word_count < 200:
        return "truncated", f"No H1 heading, low word count ({word_count})"

    if not has_paragraphs and word_count < 300:
        return "truncated", f"Few paragraphs ({content.count('<p')}), low word count ({word_count})"

    # Check if the article ends properly - legitimate articles should have closing tags
    stripped = content.strip()
    if not stripped.endswith('</div>') and not stripped.endswith('</article>') and not stripped.endswith('</section>'):
        # Check if it's a proper closing
        if stripped.endswith('</body>') or stripped.endswith('</html>'):
            pass  # ends with body/html, that's ok
        else:
            # Content ends abruptly
            lines = content.strip().split('\n')
            last_content_line = ''
            for line in reversed(lines):
                if line.strip() and not line.strip().startswith('<'):
                    last_content_line = line.strip()
                    break
            if last_content_line:
                # Check if it ends mid-sentence
                if not any(last_content_line.rstrip().endswith(end) for end in ['.', '>', '"', "'", ')', ']', '}', ';', '。', '！', '？', '—', ':']):
                    # Might be truncated, but let's check word count first
                    if word_count < 1000:
                        return "truncated", f"Content ends abruptly, only {word_count} words"

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
        print(f"\nTotal to delete: {len(to_delete)} folders")
    else:
        print(f"\nNo articles to delete.")

if __name__ == "__main__":
    main()
