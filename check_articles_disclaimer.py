#!/usr/bin/env python3
import os
import re
import shutil

website_root = "/Users/guot/Desktop/杰昊/AI推广/域名推广/Code/Website"

# Find all product folders
product_folders = [d for d in os.listdir(website_root)
                   if os.path.isdir(os.path.join(website_root, d)) and d != "index.html"]

truncated_articles = []

for product in sorted(product_folders):
    articles_dir = os.path.join(website_root, product, "articles")
    if not os.path.isdir(articles_dir):
        continue

    # Find all article folders (named article-N)
    article_folders = [d for d in os.listdir(articles_dir)
                      if re.match(r"^article-\d+$", d)]

    for afolder in sorted(article_folders):
        html_file = os.path.join(articles_dir, afolder, "index.html")
        if not os.path.isfile(html_file):
            continue

        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if article is truncated (no disclaimer section)
        if re.search(r"(?i)disclaimer", content) is None:
            truncated_articles.append((product, afolder, html_file))
            # Delete the article folder
            shutil.rmtree(os.path.join(articles_dir, afolder))
            print(f"[TRUNCATED] Deleted: {product}/{afolder}")
        else:
            print(f"[OK]        {product}/{afolder}")

print(f"\n{'='*60}")
print(f"Total truncated articles deleted: {len(truncated_articles)}")
for product, afolder, _ in truncated_articles:
    print(f"  - {product}/{afolder}")
