#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主界面模块（脚本选择）
- macOS Force Quit 风格 UI
- 多选脚本 + 循环次数（Spinbox，可设为 0 跳过）
- 可滚动脚本列表区域，底部固定按钮
"""

import tkinter as tk
from tkinter import ttk

# 配色常量
C_BG          = "#FFFFFF"
C_TEXT_MAIN   = "#1C1C1E"
C_TEXT_SUB    = "#8E8E93"
C_ACCENT      = "#007AFF"
C_DIVIDER     = "#E5E5EA"
C_BTN_SECOND  = "#F2F2F7"
C_DANGER      = "#FF3B30"
C_RUNNING     = "#34C759"
C_RUNNING_DK  = "#248A3D"
C_BLUE_DK     = "#0056CC"
C_DANGER_DK   = "#D32F2F"
C_LIST_BG     = "#F5F5F7"
C_LIST_BORDER = "#D1D1D6"


class MainUI:
    """
    主界面构建类。

    使用方式：
        ui = MainUI(root)
        ui.build(callback_on_run, callback_on_logs, callback_on_quit)
        # 外部通过 ui.get_selected_tasks() 获取 [(script_name, repeat_count), ...]
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self._script_vars: dict[str, tk.BooleanVar] = {}
        self._spin_vars:  dict[str, tk.StringVar]  = {}
        self._task_list:  list[str] = []

        self.on_run:   callable = None
        self.on_logs:  callable = None
        self.on_quit:  callable = None

    # ── 公开 API ──────────────────────────────────────────────────────────────

    def get_selected_tasks(self) -> list[tuple[str, int]]:
        """返回当前勾选的任务列表，格式为 [(script_name, repeat_count), ...]。
        循环次数为 0 的脚本自动跳过。"""
        tasks = []
        for name, var in self._script_vars.items():
            if var.get():
                try:
                    count = int(self._spin_vars[name].get())
                except ValueError:
                    count = 0
                count = max(0, min(99, count))
                if count > 0:
                    tasks.append((name, count))
        return tasks

    def refresh_script_list(self, scripts: list[str]) -> None:
        """更新脚本列表。"""
        self._task_list = scripts
        for s in scripts:
            if s not in self._script_vars:
                self._script_vars[s] = tk.BooleanVar(value=False)
            if s not in self._spin_vars:
                self._spin_vars[s] = tk.StringVar(value="0")

    # ── 构建界面 ──────────────────────────────────────────────────────────────

    def build(
        self,
        scripts: list[str],
        on_run:  callable,
        on_logs: callable,
        on_quit: callable,
    ) -> None:
        self._task_list = scripts
        self.on_run   = on_run
        self.on_logs  = on_logs
        self.on_quit  = on_quit

        for s in scripts:
            if s not in self._script_vars:
                self._script_vars[s] = tk.BooleanVar(value=False)
            if s not in self._spin_vars:
                self._spin_vars[s] = tk.StringVar(value="0")

        self._clear_root()

        # ── 整体居中框架 ────────────────────────────────────────────────────
        center = tk.Frame(self.root, bg=C_BG)
        center.pack(expand=True, fill="both", padx=40, pady=(30, 20))

        # ── 标题 ──────────────────────────────────────────────────────────────
        tk.Label(
            center,
            text="杰昊脚本管理器",
            font=("Helvetica Neue", 28, "bold"),
            fg=C_TEXT_MAIN,
            bg=C_BG,
        ).pack(pady=(0, 6))

        tk.Label(
            center,
            text="勾选要运行的脚本，填写循环次数，点击运行",
            font=("Helvetica Neue", 14),
            fg=C_TEXT_SUB,
            bg=C_BG,
        ).pack(pady=(0, 16))

        # ── 表头 ───────────────────────────────────────────────────────────────
        header = tk.Frame(center, bg=C_BG)
        header.pack(pady=(0, 6), fill="x")

        tk.Label(
            header, text="", font=("Helvetica Neue", 11, "bold"),
            fg=C_TEXT_SUB, bg=C_BG, width=4,
        ).pack(side="left")
        tk.Label(
            header, text="脚本名称", font=("Helvetica Neue", 12, "bold"),
            fg=C_TEXT_SUB, bg=C_BG,
        ).pack(side="left", padx=(8, 0))
        tk.Label(
            header, text="循环次数", font=("Helvetica Neue", 12, "bold"),
            fg=C_TEXT_SUB, bg=C_BG,
        ).pack(side="right")

        # ── 可滚动脚本列表区域（带边框卡片）────────────────────────────────────
        list_card = tk.Frame(center, bg=C_LIST_BORDER, bd=0)
        list_card.pack(pady=(0, 20), fill="x")

        canvas_frame = tk.Frame(list_card, bg=C_LIST_BG)
        canvas_frame.pack(fill="x")

        canvas_h = max(min(len(scripts) * 44, 400), 220)
        canvas = tk.Canvas(
            canvas_frame,
            bg=C_LIST_BG,
            height=canvas_h,
            bd=0,
            highlightthickness=0,
            confine=True,
        )
        canvas.pack(side="left", fill="x", expand=True)

        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.config(yscrollcommand=scrollbar.set)

        inner = tk.Frame(canvas, bg=C_LIST_BG)
        canvas_window = canvas.create_window((0, 0), window=inner, anchor="nw")

        def _on_frame_config(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
            if len(scripts) * 44 > canvas_h:
                canvas.pack(side="left", fill="x", expand=True)
            else:
                scrollbar.pack_forget()

        inner.bind("<Configure>", _on_frame_config)

        for row, name in enumerate(scripts):
            row_frame = tk.Frame(inner, bg=C_LIST_BG, cursor="hand2")
            row_frame.pack(fill="x", padx=0, pady=0)

            var  = self._script_vars[name]
            spin = self._spin_vars[name]

            # 勾选框
            cb = tk.Checkbutton(
                row_frame,
                variable=var,
                bg=C_LIST_BG,
                activebackground=C_LIST_BG,
                fg=C_ACCENT,
                selectcolor=C_ACCENT,
                highlightthickness=0,
                padx=8,
                pady=8,
            )
            cb.pack(side="left")

            # 脚本名
            lbl = tk.Label(
                row_frame,
                text=name,
                font=("Helvetica Neue", 15),
                fg=C_TEXT_MAIN,
                bg=C_LIST_BG,
                anchor="w",
            )
            lbl.pack(side="left", fill="x", expand=True, padx=(0, 8), pady=8)

            # 循环次数 Spinbox（最小值改为 0）
            sp = tk.Spinbox(
                row_frame,
                from_=0,
                to=99,
                width=4,
                textvariable=spin,
                font=("Helvetica Neue", 13),
                fg=C_TEXT_MAIN,
                bg=C_LIST_BG,
                buttonbackground=C_LIST_BG,
                relief="solid",
                bd=1,
                highlightthickness=1,
                highlightcolor=C_ACCENT,
                highlightbackground=C_DIVIDER,
                justify="center",
            )
            sp.pack(side="right", padx=(0, 12), pady=8)

            # 分隔线（最后一行不加）
            if row < len(scripts) - 1:
                sep = tk.Frame(inner, bg=C_DIVIDER, height=1)
                sep.pack(fill="x")

            # 鼠标悬停效果
            def _on_enter(e, rf=row_frame):
                rf.config(bg="#ECECED")
                for child in rf.winfo_children():
                    try:
                        child.config(bg="#ECECED")
                    except Exception:
                        pass
            def _on_leave(e, rf=row_frame):
                rf.config(bg=C_LIST_BG)
                for child in rf.winfo_children():
                    try:
                        child.config(bg=C_LIST_BG)
                    except Exception:
                        pass
            row_frame.bind("<Enter>", _on_enter)
            row_frame.bind("<Leave>", _on_leave)

        # 滚动区域绑定鼠标滚轮
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # ── 分隔线 ───────────────────────────────────────────────────────────
        sep = tk.Frame(center, bg=C_DIVIDER, height=1)
        sep.pack(fill="x", pady=(0, 16))

        # ── 按钮区域 ─────────────────────────────────────────────────────────
        btn_frame = tk.Frame(center, bg=C_BG)
        btn_frame.pack(pady=(0, 0))

        def _flat_btn(
            text: str,
            bg: str,
            active_bg: str,
            fg: str = "white",
            cmd: callable = None,
        ) -> tk.Button:
            b = tk.Button(
                btn_frame,
                text=text,
                font=("Helvetica Neue", 15, "bold"),
                bg=bg,
                fg=fg,
                activebackground=active_bg,
                activeforeground=fg,
                relief="flat",
                width=12,
                height=2,
                cursor="pointinghand",
                command=cmd,
            )
            return b

        _flat_btn("运行", C_ACCENT,  C_BLUE_DK,  "white", self._handle_run).pack(side="left", padx=8)
        _flat_btn("查看日志", C_RUNNING, C_RUNNING_DK, "white", self.on_logs).pack(side="left", padx=8)
        _flat_btn("退出",  C_DANGER,  C_DANGER_DK, "white", self.on_quit).pack(side="left", padx=8)

    # ── 内部方法 ──────────────────────────────────────────────────────────────

    def _handle_run(self) -> None:
        tasks = self.get_selected_tasks()
        if not tasks:
            from tkinter import messagebox
            messagebox.showwarning("未选择脚本", "请至少勾选一个循环次数大于 0 的脚本后运行。")
            return
        if self.on_run:
            self.on_run(tasks)

    def _clear_root(self) -> None:
        try:
            self.root.unbind_all("<MouseWheel>")
        except Exception:
            pass
        for w in self.root.winfo_children():
            w.destroy()
