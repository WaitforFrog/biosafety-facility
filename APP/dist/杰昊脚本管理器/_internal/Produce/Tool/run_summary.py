"""
运行汇总日志工具
"""
import os
import json
from datetime import datetime


def save_run_summary(results, success_count, error_count, article_base_dir):
    """保存运行汇总到 JSON 文件"""
    summary_dir = os.path.join(article_base_dir, "汇总日志")
    os.makedirs(summary_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}.json"
    filepath = os.path.join(summary_dir, filename)

    simplified_results = []
    for r in results:
        item = {
            "product_name": r["product_name"],
            "success": r["success"]
        }
        if r["success"]:
            item["backup_path"] = r["backup_path"]
        simplified_results.append(item)

    summary = {
        "run_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_products": len(results),
        "success_count": success_count,
        "error_count": error_count,
        "results": simplified_results
    }

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"\n汇总日志已保存: {filepath}")
    return filepath
