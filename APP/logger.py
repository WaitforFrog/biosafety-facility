#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志读写、索引管理模块
负责 ~/Library/Logs/杰昊脚本管理器/index.json 的增删改查
"""

import json
import datetime
from pathlib import Path


# ─── 配置（由 run_app.py 导入时注入）────────────────────────────────────────
LOG_DIR: Path = None  # 运行时由 run_app.py 设置


def _log_index_path() -> Path:
    return LOG_DIR / "index.json"


# ─── 索引读写 ──────────────────────────────────────────────────────────────

def load_log_index() -> list[dict]:
    """加载运行记录索引列表。失败时返回空列表。"""
    p = _log_index_path()
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []


def save_log_index(index: list[dict]) -> None:
    """持久化运行记录索引列表。"""
    p = _log_index_path()
    p.write_text(
        json.dumps(index, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


# ─── 日志条目管理 ──────────────────────────────────────────────────────────

def save_run_log(script_name: str, output: str) -> dict:
    """
    保存一条新的运行记录到索引。
    - 追加到列表最前面（最新优先）
    - 最多保留 500 条
    """
    index = load_log_index()
    entry = {
        "id": datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"),
        "script": script_name,
        "timestamp": datetime.datetime.now().isoformat(),
        "output": output,
    }
    index.insert(0, entry)
    if len(index) > 500:
        index = index[:500]
    save_log_index(index)
    return entry


def group_by_date(logs: list[dict]) -> dict[str, list[dict]]:
    """将日志列表按日期（YYYY-MM-DD）分组，返回 {date: [entries]}。"""
    grouped = {}
    for entry in logs:
        ts = entry.get("timestamp", "")[:10]
        if ts not in grouped:
            grouped[ts] = []
        grouped[ts].append(entry)
    return grouped
