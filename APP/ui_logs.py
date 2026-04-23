#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志界面模块
左侧按日期分组的运行记录列表，右侧查看完整终端输出。
"""

import tkinter as tk
from tkinter import scrolledtext, ttk

from . import logger as logger_mod

# 配色
C_BG          = "#FFFFFF"
C_TEXT_MAIN   = "#1C1C1E"
C_TEXT_SUB    = "#8E8E93"
C_ACCENT      = "#007AFF"
C_DIVIDER     = "#E5E5EA"
C_BTN_SECOND  = "#F2F2F7"


class LogsUI:
    """
    日志界面构建类。

    使用方式：
        ui = LogsUI(root)
        ui.build(callback_on_back)
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self._log_list:       tk.Listbox = None
        self._detail_frame:   tk.Frame   = None
        self._grouped_logs:   dict       = {}

    # ── 公开 API ──────────────────────────────────────────────────────────────

    def build(self, on_back: callable) -> None:
        """
        构建日志界面。

        Args:
            on_back: 返回主界面按钮的回调（无参数）。
        """
        self._clear_root()

        container = tk.Frame(self.root, bg=C_BG)
        container.pack(expand=True, fill="both")

        # ── 顶部栏 ──────────────────────────────────────────────────────────
        top = tk.Frame(container, bg=C_BG)
        top.pack(fill="x", padx=20, pady=(20, 0))

        tk.Label(
            top,
            text="运行历史",
            font=("Helvetica Neue", 20, "bold"),
            fg=C_TEXT_MAIN,
            bg=C_BG,
        ).pack(side="left")

        tk.Button(
            top,
            text="返回主界面",
            font=("Helvetica Neue", 12),
            bg=C_BTN_SECOND,
            fg=C_ACCENT,
            activebackground="#E5E5EA",
            relief="flat",
            cursor="pointinghand",
            command=on_back,
        ).pack(side="right")

        sep = tk.Frame(container, bg=C_DIVIDER, height=1)
        sep.pack(fill="x", padx=20, pady=(12, 0))

        # ── 主体：左侧列表 + 右侧详情 ────────────────────────────────────────
        body = tk.Frame(container, bg=C_BG)
        body.pack(expand=True, fill="both", padx=20, pady=12)

        # 左侧列表
        list_frame = tk.Frame(body, bg="#F2F2F7", bd=0)
        list_frame.pack(side="left", fill="both", padx=(0, 10))

        scroll_y = ttk.Scrollbar(list_frame)
        scroll_y.pack(side="right", fill="y")

        scroll_x = ttk.Scrollbar(list_frame, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")

        self._log_list = tk.Listbox(
            list_frame,
            font=("Helvetica Neue", 13),
            bg="#F2F2F7",
            fg=C_TEXT_MAIN,
            selectbackground=C_ACCENT,
            selectforeground="white",
            relief="flat",
            bd=0,
            highlightthickness=0,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            activestyle="none",
        )
        self._log_list.pack(expand=True, fill="both")
        scroll_y.config(command=self._log_list.yview)
        scroll_x.config(command=self._log_list.xview)

        # 右侧详情
        self._detail_frame = tk.Frame(body, bg=C_BG)
        self._detail_frame.pack(side="left", expand=True, fill="both")

        tk.Label(
            self._detail_frame,
            text="选择一条记录查看完整输出",
            font=("Helvetica Neue", 13),
            fg=C_TEXT_SUB,
            bg=C_BG,
        ).pack(expand=True)

        # 加载数据
        self._grouped_logs = {}
        self._log_index = logger_mod.load_log_index()
        if self._log_index:
            self._grouped_logs = logger_mod.group_by_date(self._log_index)
            self._render_grouped_list(self._log_list)
        else:
            self._log_list.insert(tk.END, "暂无运行记录")
            self._log_list.itemconfig(0, fg=C_TEXT_SUB)

        self._log_list.bind("<<ListboxSelect>>", self._on_log_select)

    # ── 内部方法 ──────────────────────────────────────────────────────────────

    def _render_grouped_list(self, listbox: tk.Listbox) -> None:
        """按日期分组渲染列表：日期标题 + 时间戳·脚本名。"""
        import datetime

        listbox.delete(0, tk.END)
        for date, entries in self._grouped_logs.items():
            display = f"📅 {date}  ({len(entries)} 次运行)"
            listbox.insert(tk.END, display)
            listbox.itemconfig(tk.END, fg=C_ACCENT)

            for entry in entries:
                ts_full = entry.get("timestamp", "")
                try:
                    t = datetime.datetime.fromisoformat(ts_full).strftime("%H:%M:%S")
                except Exception:
                    t = ts_full
                script = entry.get("script", "未知")
                listbox.insert(tk.END, f"    ⏱ {t}  •  {script}")
                listbox.itemconfig(tk.END, fg=C_TEXT_SUB)

    def _on_log_select(self, event) -> None:
        selection = self._log_list.curselection()
        if not selection:
            return

        idx = selection[0]

        # 构建扁平索引
        flat = []
        for date, entries in self._grouped_logs.items():
            flat.append(("header", date, len(entries)))
            for e in entries:
                flat.append(("entry", e))

        if idx < len(flat):
            kind = flat[idx][0]
            if kind == "entry":
                entry = flat[idx][1]
                self._show_log_detail(entry)

    def _show_log_detail(self, entry: dict) -> None:
        for w in self._detail_frame.winfo_children():
            w.destroy()

        header = tk.Frame(self._detail_frame, bg="#F2F2F7")
        header.pack(fill="x", pady=(0, 8))

        info_text = (
            f"脚本: {entry.get('script', '未知')}  |  "
            f"时间: {entry.get('timestamp', '')}"
        )
        tk.Label(
            header,
            text=info_text,
            font=("Helvetica Neue", 12, "bold"),
            fg=C_TEXT_MAIN,
            bg="#F2F2F7",
            anchor="w",
        ).pack(anchor="w", padx=10, pady=6)

        output_box = scrolledtext.ScrolledText(
            self._detail_frame,
            font=("Menlo", 11),
            bg="#1E1E1E",
            fg="#D4D4D4",
            relief="flat",
            state="normal",
            wrap="word",
            padx=12,
            pady=12,
        )
        output_box.pack(expand=True, fill="both")
        output_box.insert("end", entry.get("output", "(无输出)"))
        output_box.config(state="disabled")

    def _clear_root(self) -> None:
        for w in self.root.winfo_children():
            w.destroy()
