#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主界面模块（脚本选择）
- macOS Force Quit 风格 UI
- 多选脚本 + 循环次数（Spinbox）
- ttk.Treeview 三列：☑ | 脚本名 | 循环次数
"""

import tkinter as tk
from tkinter import ttk

# 配色常量
C_BG          = "#FFFFFF"   # 背景
C_TEXT_MAIN   = "#1C1C1E"   # 主文字
C_TEXT_SUB    = "#8E8E93"   # 辅助文字
C_ACCENT      = "#007AFF"   # macOS 标准蓝
C_DIVIDER     = "#E5E5EA"   # 分隔线
C_BTN_SECOND  = "#F2F2F7"   # 次要按钮底色
C_DANGER      = "#FF3B30"   # 危险操作
C_RUNNING     = "#34C759"   # 运行中绿
C_RUNNING_DK  = "#248A3D"   # 深绿
C_BLUE_DK     = "#0056CC"   # 深蓝（active）
C_DANGER_DK   = "#D32F2F"   # 深红（active）


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
        self._task_list:  list[str] = []  # 所有可用脚本

        # 回调（由外部设置）
        self.on_run:   callable = None
        self.on_logs:  callable = None
        self.on_quit:  callable = None

    # ── 公开 API ──────────────────────────────────────────────────────────────

    def get_selected_tasks(self) -> list[tuple[str, int]]:
        """返回当前勾选的任务列表，格式为 [(script_name, repeat_count), ...]。"""
        tasks = []
        for name, var in self._script_vars.items():
            if var.get():
                try:
                    count = int(self._spin_vars[name].get())
                except ValueError:
                    count = 1
                count = max(1, min(99, count))
                tasks.append((name, count))
        return tasks

    def refresh_script_list(self, scripts: list[str]) -> None:
        """更新脚本列表（在构建界面后调用可刷新，但通常 build 时传入即可）。"""
        self._task_list = scripts
        # 同步 _script_vars / _spin_vars
        for s in scripts:
            if s not in self._script_vars:
                self._script_vars[s] = tk.BooleanVar(value=False)
            if s not in self._spin_vars:
                self._spin_vars[s] = tk.StringVar(value="1")

    # ── 构建界面 ──────────────────────────────────────────────────────────────

    def build(
        self,
        scripts: list[str],
        on_run:  callable,
        on_logs: callable,
        on_quit: callable,
    ) -> None:
        """
        构建主界面。

        Args:
            scripts:  可选脚本名列表，如 ["Compare_JIEHAO.py", "Introduction_EN_html.py"]
            on_run:   "运行"按钮回调
            on_logs:  "查看日志"按钮回调
            on_quit:  "退出"按钮回调
        """
        self._task_list = scripts
        self.on_run  = on_run
        self.on_logs = on_logs
        self.on_quit = on_quit

        # 初始化变量
        for s in scripts:
            if s not in self._script_vars:
                self._script_vars[s] = tk.BooleanVar(value=False)
            if s not in self._spin_vars:
                self._spin_vars[s] = tk.StringVar(value="1")

        self._clear_root()

        # ── 整体居中框架 ────────────────────────────────────────────────────
        center = tk.Frame(self.root, bg=C_BG)
        center.pack(expand=True, fill="both", padx=40, pady=40)

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
        ).pack(pady=(0, 24))

        # ── 脚本列表（Treeview）───────────────────────────────────────────────
        list_frame = tk.Frame(center, bg=C_BG)
        list_frame.pack(pady=(0, 24), fill="x")

        # 表头
        col_labels = ["", "脚本名称", "循环次数"]
        for i, lbl in enumerate(col_labels):
            tk.Label(
                list_frame,
                text=lbl,
                font=("Helvetica Neue", 12, "bold"),
                fg=C_TEXT_SUB,
                bg=C_BG,
                anchor="w",
            ).grid(row=0, column=i, sticky="w", padx=4, pady=(0, 6))

        for row, name in enumerate(scripts, start=1):
            var   = self._script_vars[name]
            spin  = self._spin_vars[name]

            # 勾选框
            cb = tk.Checkbutton(
                list_frame,
                variable=var,
                bg=C_BG,
                activebackground=C_BG,
                fg=C_ACCENT,
                selectcolor=C_ACCENT,
                highlightthickness=0,
                padx=4,
                pady=4,
            )
            cb.grid(row=row, column=0, sticky="w", padx=4)

            # 脚本名
            tk.Label(
                list_frame,
                text=name,
                font=("Helvetica Neue", 15),
                fg=C_TEXT_MAIN,
                bg=C_BG,
                anchor="w",
            ).grid(row=row, column=1, sticky="w", padx=4, pady=2)

            # 循环次数 Spinbox
            sp = tk.Spinbox(
                list_frame,
                from_=1,
                to=99,
                width=4,
                textvariable=spin,
                font=("Helvetica Neue", 13),
                fg=C_TEXT_MAIN,
                bg=C_BG,
                buttonbackground=C_BG,
                relief="solid",
                bd=1,
                highlightthickness=1,
                highlightcolor=C_ACCENT,
                highlightbackground=C_DIVIDER,
                justify="center",
            )
            sp.grid(row=row, column=2, sticky="w", padx=4, pady=2)

        # ── 分隔线 ───────────────────────────────────────────────────────────
        sep = tk.Frame(center, bg=C_DIVIDER, height=1)
        sep.pack(fill="x", pady=(0, 20))

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
            messagebox.showwarning("未选择脚本", "请至少勾选一个脚本后运行。")
            return
        if self.on_run:
            self.on_run(tasks)

    def _clear_root(self) -> None:
        for w in self.root.winfo_children():
            w.destroy()
