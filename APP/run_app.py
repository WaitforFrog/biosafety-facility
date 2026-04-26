#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
杰昊脚本管理器 - 入口模块
仅保留配置常量 + main() 启动代码，所有业务逻辑委托给各子模块。

模块结构：
  run_app.py         — 入口（约 30 行）
  ui_main.py         — 主界面（脚本选择 + 多选 + 循环次数）
  ui_run.py          — 运行界面（实时输出 + 截断 + 队列执行）
  ui_logs.py         — 日志界面（历史查看）
  process_manager.py — 进程管理（启动 / 读取 / 截断）
  logger.py          — 日志读写、索引管理
"""

import os
import sys
import tkinter as tk
from pathlib import Path

# ─── 配置常量 ───────────────────────────────────────────────────────────────
from APP.paths import PRODUCE_DIR

SCRIPTS_DIR = PRODUCE_DIR
LOG_DIR     = Path.home() / "Library" / "Logs" / "杰昊脚本管理器"
PYTHON_BIN  = sys.executable   # 使用 APP 自带的 Python（PyInstaller 打包后指向内置 Python）
APP_NAME    = "杰昊脚本管理器"

# 从 PRODUCE_DIR 自动扫描可执行脚本（排除 __init__ 和非脚本文件）
SCRIPTS = sorted([
    f.name for f in PRODUCE_DIR.iterdir()
    if f.is_file() and f.suffix == ".py" and not f.name.startswith("_")
])

# ─── 初始化全局目录 ───────────────────────────────────────────────────────────
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 注入 logger 模块的 LOG_DIR（避免循环导入时 logger.py 还未初始化）
import APP.logger as logger_mod
logger_mod.LOG_DIR = LOG_DIR


# ─── 主应用 ──────────────────────────────────────────────────────────────────
class ScriptManagerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("800x800")
        self.root.minsize(700, 500)
        self.root.configure(bg="white")

        # 延迟导入 UI 模块（避免循环引用）
        from APP.ui_main import MainUI
        from APP.ui_run  import RunUI
        from APP.ui_logs import LogsUI

        self._main_ui = MainUI(root)
        self._run_ui  = RunUI(root)
        self._logs_ui = LogsUI(root)

        self._show_main()

    # ── 视图切换 ─────────────────────────────────────────────────────────────

    def _show_main(self) -> None:
        self._main_ui.build(
            scripts=SCRIPTS,
            on_run=self._on_run,
            on_logs=self._show_logs,
            on_quit=self._on_quit,
        )

    def _show_logs(self) -> None:
        self._logs_ui.build(on_back=self._show_main)

    def _on_run(self, tasks: list[tuple[str, int]]) -> None:
        """运行按钮回调：tasks = [(script_name, repeat_count), ...]"""
        # 检查脚本文件是否存在
        for name, _ in tasks:
            p = SCRIPTS_DIR / name
            if not p.exists():
                from tkinter import messagebox
                messagebox.showerror("错误", f"脚本不存在：\n{p}")
                return

        self._run_ui.build(
            tasks=tasks,
            scripts_dir=str(SCRIPTS_DIR),
            python_bin=PYTHON_BIN,
            on_all_done=self._on_all_done,
            on_back=self._show_main,
        )

    def _on_all_done(self) -> None:
        from tkinter import messagebox
        messagebox.showinfo("全部完成", "所有任务已执行完毕！")

    # ── 退出 ─────────────────────────────────────────────────────────────────

    def _on_quit(self) -> None:
        from APP import process_manager
        process_manager.terminate_process()
        self.root.quit()
        self.root.destroy()


# ─── 启动 ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app  = ScriptManagerApp(root)
    root.protocol("WM_DELETE_WINDOW", app._on_quit)
    root.mainloop()
