#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行界面模块（实时输出 + 截断按钮）
支持队列式顺序执行：多脚本 × 各自循环次数，执行完一个等待5分钟再下一个。
"""

import tkinter as tk
from tkinter import scrolledtext

from . import process_manager
from . import logger as logger_mod

# 配色
C_BG          = "#FFFFFF"
C_TEXT_MAIN   = "#1C1C1E"
C_TEXT_SUB    = "#8E8E93"
C_ACCENT      = "#007AFF"
C_DIVIDER     = "#E5E5EA"
C_BTN_SECOND  = "#F2F2F7"
C_DANGER      = "#FF3B30"
C_DANGER_DK   = "#D32F2F"
C_TERMINAL_BG = "#1E1E1E"
C_TERMINAL_FG = "#D4D4D4"
C_DIV         = "─" * 50


class RunUI:
    """
    运行界面构建类。

    使用方式：
        ui = RunUI(root)
        ui.build(tasks, callbacks)
        # tasks: [(script_name, repeat_count), ...]
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self._output_box: scrolledtext.ScrolledText = None
        self._kill_btn:   tk.Button = None
        self._back_btn:  tk.Button = None
        self._status_dot: tk.Label = None
        self._info_label: tk.Label = None

        self._queue_cancelled = False
        self._current_running = False
        self._tasks: list[tuple[str, int]] = []
        self._task_index = 0
        self._current_repeat = 0

        self._full_output: list[str] = []
        self._scripts_dir  = None
        self._python_bin    = None

        # 外部回调
        self.on_all_done:  callable = None
        self.on_back:      callable = None

    # ── 公开 API ──────────────────────────────────────────────────────────────

    def build(
        self,
        tasks: list[tuple[str, int]],
        scripts_dir: str,
        python_bin: str,
        on_all_done: callable,
        on_back:     callable,
    ) -> None:
        """
        构建运行界面并开始执行任务队列。

        Args:
            tasks:        任务列表 [(script_name, repeat_count), ...]
            scripts_dir:  脚本所在目录（字符串路径）
            python_bin:   Python 解释器路径
            on_all_done:  全部完成时的回调（无参数）
            on_back:      返回按钮回调（无参数）
        """
        self._tasks        = tasks
        self._task_index   = 0
        self._current_repeat = 0
        self._full_output  = []
        self._scripts_dir  = scripts_dir
        self._python_bin   = python_bin
        self._queue_cancelled = False
        self._current_running  = False
        self.on_all_done  = on_all_done
        self.on_back      = on_back

        self._clear_root()

        # ── 容器 ──────────────────────────────────────────────────────────────
        container = tk.Frame(self.root, bg=C_BG)
        container.pack(expand=True, fill="both")

        # ── 顶部栏 ────────────────────────────────────────────────────────────
        top = tk.Frame(container, bg=C_BG)
        top.pack(fill="x", padx=20, pady=(20, 0))

        tk.Label(
            top,
            text="代码开始运行",
            font=("Helvetica Neue", 16, "bold"),
            fg=C_TEXT_MAIN,
            bg=C_BG,
        ).pack(side="left")

        self._status_dot = tk.Label(
            top, text="●", font=("Helvetica Neue", 16),
            fg=C_TEXT_SUB, bg=C_BG
        )
        self._status_dot.pack(side="left", padx=(8, 0))

        # 进度信息
        total_tasks = sum(r for _, r in tasks)
        self._info_label = tk.Label(
            top,
            text=f"队列: 0/{total_tasks}",
            font=("Helvetica Neue", 12),
            fg=C_TEXT_SUB,
            bg=C_BG,
        )
        self._info_label.pack(side="left", padx=(16, 0))

        self._back_btn = tk.Button(
            top,
            text="返回主界面",
            font=("Helvetica Neue", 12),
            bg=C_BTN_SECOND,
            fg=C_ACCENT,
            activebackground="#E5E5EA",
            relief="flat",
            cursor="pointinghand",
            command=self._on_back,
        )
        self._back_btn.pack(side="right")

        sep = tk.Frame(container, bg=C_DIVIDER, height=1)
        sep.pack(fill="x", padx=20, pady=(12, 0))

        # ── 副标题 ─────────────────────────────────────────────────────────────
        tk.Label(
            container,
            text="终端输出内容如下：",
            font=("Helvetica Neue", 13),
            fg=C_TEXT_SUB,
            bg=C_BG,
        ).pack(anchor="w", padx=20, pady=(12, 4))

        # ── 终端输出框 ─────────────────────────────────────────────────────────
        self._output_box = scrolledtext.ScrolledText(
            container,
            font=("Menlo", 12),
            bg=C_TERMINAL_BG,
            fg=C_TERMINAL_FG,
            insertbackground="white",
            relief="flat",
            state="disabled",
            wrap="word",
            padx=12,
            pady=12,
        )
        self._output_box.pack(expand=True, fill="both", padx=20, pady=(0, 12))

        # ── 底部按钮 ───────────────────────────────────────────────────────────
        bottom = tk.Frame(container, bg=C_BG)
        bottom.pack(fill="x", padx=20, pady=(0, 16))

        self._kill_btn = tk.Button(
            bottom,
            text="截断（停止后续队列）",
            font=("Helvetica Neue", 14, "bold"),
            bg=C_DANGER,
            fg="white",
            activebackground=C_DANGER_DK,
            activeforeground="white",
            relief="flat",
            width=20,
            height=2,
            cursor="pointinghand",
            command=self._on_kill,
        )
        self._kill_btn.pack(side="right")

        # 开始执行
        self._append_output(f"▶ 任务队列已建立，共 {len(tasks)} 个任务，{total_tasks} 次执行\n")
        self._append_output(f"▶ Python: {python_bin}\n")
        self._append_output(f"{C_DIV}\n\n")
        self._run_next_if_allowed()

    # ── 队列执行引擎 ─────────────────────────────────────────────────────────

    def _run_next_if_allowed(self) -> None:
        """检查队列状态，开始执行下一个任务（如果有）。"""
        if self._queue_cancelled:
            self._append_output("\n⏹ 队列已被截断，不再执行后续脚本。\n")
            self._disable_run_button("已截断")
            return

        if self._task_index >= len(self._tasks):
            self._all_done()
            return

        script_name, total_repeats = self._tasks[self._task_index]
        if self._current_repeat >= total_repeats:
            # 当前脚本完成，进入下一个脚本
            self._task_index += 1
            self._current_repeat = 0
            if self._task_index >= len(self._tasks):
                self._all_done()
                return
            script_name, total_repeats = self._tasks[self._task_index]

        # 显示等待还是开始
        if self._current_repeat > 0:
            # 前一次执行刚结束，等待5分钟
            self._append_output(f"\n⏳ 等待 5 分钟...\n")
            self._status_dot.config(fg=C_TEXT_SUB)
            self._kill_btn.config(state="disabled", text="等待中...")
            # 用 after 每秒倒计时
            self._wait_countdown(300, script_name, total_repeats)
        else:
            self._begin_task(script_name, total_repeats)

    def _wait_countdown(self, seconds: int, script_name: str, total_repeats: int) -> None:
        """每秒倒计时，等待 seconds 秒后执行下一个任务。"""
        if self._queue_cancelled:
            self._append_output("⏹ 等待期间队列被截断。\n")
            self._disable_run_button("已截断")
            return

        if seconds > 0:
            mins, secs = divmod(seconds, 60)
            self._info_label.config(
                text=f"等待中 {mins:02d}:{secs:02d} | {script_name} ({self._current_repeat + 1}/{total_repeats})"
            )
            self.root.after(1000, self._wait_countdown, seconds - 1, script_name, total_repeats)
        else:
            self._info_label.config(text="")
            self._append_output("✅ 等待结束，开始执行下一任务...\n")
            self._begin_task(script_name, total_repeats)

    def _begin_task(self, script_name: str, total_repeats: int) -> None:
        """真正启动一个脚本子进程。"""
        self._current_running = True
        self._kill_btn.config(state="normal", text="截断（停止后续队列）")

        repeat_display = self._current_repeat + 1
        self._info_label.config(
            text=f"执行: {script_name} ({repeat_display}/{total_repeats})"
        )
        self._status_dot.config(fg="#34C759")

        self._append_output(f"\n{'='*50}\n")
        self._append_output(f"▶ 启动 [{repeat_display}/{total_repeats}]: {script_name}\n")
        self._append_output(f"{C_DIV}\n\n")

        import os
        script_path = os.path.join(self._scripts_dir, script_name)
        from pathlib import Path
        process_manager.start_process(
            script_path=Path(script_path),
            python_bin=self._python_bin,
            on_output=self._append_output,
            on_finished=self._on_task_finished,
        )

    def _on_task_finished(self, return_code: int) -> None:
        """单个任务（一次执行）完成后的回调。"""
        self._current_running = False

        # 保存日志
        full_text = "".join(self._full_output)
        script_name = self._tasks[self._task_index][0]
        threading_current = __import__("threading")
        threading_current.Thread(
            target=logger_mod.save_run_log,
            args=(script_name, full_text),
            daemon=True,
        ).start()

        # 判断结束原因
        if self._queue_cancelled:
            self._append_output(f"\n{C_DIV}\n")
            self._append_output("⏹ 任务在运行期间被截断（SIGINT）\n")
            self._disable_run_button("已截断")
            return

        if return_code == 0:
            self._append_output(f"\n{C_DIV}\n")
            self._append_output(f"✅ [{self._current_repeat + 1}/{self._tasks[self._task_index][1]}] 执行完毕（正常退出）\n")
        elif return_code == -2:
            self._append_output(f"\n{C_DIV}\n")
            self._append_output(f"⚠️ 任务被截断（SIGINT）\n")
        else:
            self._append_output(f"\n{C_DIV}\n")
            self._append_output(f"⚠️ 任务已退出（退出码: {return_code}）\n")

        # 更新当前脚本的重复计数
        self._current_repeat += 1

        # 更新队列进度
        completed = sum(
            r for i, (_, r) in enumerate(self._tasks)
            if i < self._task_index
        ) + self._current_repeat
        total_tasks = sum(r for _, r in self._tasks)
        self._info_label.config(text=f"队列: {completed}/{total_tasks}")

        # 继续下一个
        self._run_next_if_allowed()

    def _all_done(self) -> None:
        self._status_dot.config(fg="#34C759")
        self._info_label.config(text="全部完成")
        self._append_output(f"\n{'='*50}\n")
        self._append_output("🎉 全部任务执行完毕！\n")
        self._kill_btn.config(state="disabled", text="已完成")
        if self.on_all_done:
            self.root.after(500, self.on_all_done)

    # ── 事件处理 ──────────────────────────────────────────────────────────────

    def _on_kill(self) -> None:
        """截断当前运行 + 标记队列停止。"""
        self._queue_cancelled = True
        if self._current_running:
            success = process_manager.kill_process(on_killed=self._append_output)
            if success:
                self._kill_btn.config(state="disabled", text="截断中...")
        else:
            # 当前没有进程在跑，但队列已标记取消
            self._append_output("\n⏹ 队列已停止，不再执行后续脚本。\n")
            self._disable_run_button("已截断")

    def _on_back(self) -> None:
        """返回主界面：停止当前进程 + 标记队列取消。"""
        self._queue_cancelled = True
        process_manager.terminate_process()
        if self.on_back:
            self.on_back()

    def _disable_run_button(self, text: str) -> None:
        self._kill_btn.config(state="disabled", text=text)

    # ── 辅助 ──────────────────────────────────────────────────────────────────

    def _append_output(self, text: str) -> None:
        if not self._output_box:
            return

        def _append():
            self._full_output.append(text)
            self._output_box.config(state="normal")
            self._output_box.insert("end", text)
            self._output_box.see("end")
            self._output_box.config(state="disabled")

        try:
            self.root.after(0, _append)
        except Exception:
            pass

    def _clear_root(self) -> None:
        for w in self.root.winfo_children():
            w.destroy()
