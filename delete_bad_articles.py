#!/usr/bin/env python3
import os
import re

base_path = "/Users/guot/Desktop/杰昊/AI推广/域名推广/Code/Website/biosafety-inflatable-airtight-doors/articles"

def check_article_has_disclaimer(article_path):
    """Check if article has a proper Disclaimer section."""
    index_path = os.path.join(article_path, "index.html")

    if not os.path.exists(index_path):
        return False, "No index.html found", 0

    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"Cannot read file: {e}", 0

    # Remove HTML tags to count actual text
    text_only = re.sub(r'<[^>]+>', '', content)
    word_count = len(text_only.split())

    # Check for Disclaimer section (case-insensitive)
    has_disclaimer = bool(re.search(r'(?i)(disclaimer|免责声明|免责声明)', text_only))

    return has_disclaimer, "Has Disclaimer" if has_disclaimer else "Missing Disclaimer", word_count

def main():
    articles_dir = base_path
    article_folders = []

    for item in os.listdir(articles_dir):
        item_path = os.path.join(articles_dir, item)
        if os.path.isdir(item_path) and item.startswith("article-"):
            article_folders.append(item)

    article_folders.sort(key=lambda x: int(x.replace("article-", "")))

    print(f"Found {len(article_folders)} article folders\n")

    results = {"good": [], "missing_disclaimer": []}

    for folder in article_folders:
        folder_path = os.path.join(articles_dir, folder)
        has_disclaimer, reason, word_count = check_article_has_disclaimer(folder_path)

        if has_disclaimer:
            results["good"].append((folder, reason, word_count))
            status_symbol = "✓"
        else:
            results["missing_disclaimer"].append((folder, reason, word_count))
            status_symbol = "✗"

        print(f"{status_symbol} {folder}: {reason} ({word_count} words)")

    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Has Disclaimer: {len(results['good'])}")
    print(f"  Missing Disclaimer: {len(results['missing_disclaimer'])}")

    if results['missing_disclaimer']:
        print(f"\n{'='*60}")
        print(f"Articles to DELETE (missing Disclaimer - truncated/incomplete):")
        for folder, reason, word_count in results['missing_disclaimer']:
            print(f"  - {folder}: {word_count} words")
        print(f"\nTotal to delete: {len(results['missing_disclaimer'])} folders")

        # Generate delete commands
        print(f"\n{'='*60}")
        print(f"Delete commands:")
        for folder, _, _ in results['missing_disclaimer']:
            folder_path = os.path.join(base_path, folder)
            print(f'  rm -rf "{folder_path}"')
    else:
        print(f"\nNo articles to delete - all have Disclaimer sections.")

if __name__ == "__main__":
    main()
