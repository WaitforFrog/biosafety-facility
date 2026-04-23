#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
进程管理模块
负责子进程的启动、输出读取、截断。
"""

import os
import signal
import subprocess
import threading
from pathlib import Path
from typing import Callable, Optional

# 共享进程对象（子进程）
_process: Optional[subprocess.Popen] = None
# 停止信号
_stop_event = threading.Event()


def start_process(
    script_path: Path,
    python_bin: str,
    on_output: Callable[[str], None],
    on_finished: Callable[[int], None],
) -> None:
    """
    启动一个 Python 脚本子进程，异步读取其 stdout/stderr 并回调。

    Args:
        script_path:  脚本文件的绝对路径
        python_bin:   Python 解释器路径（如 /opt/homebrew/bin/python3）
        on_output:    每次读到一行输出时的回调，签名为 (line: str) -> None
        on_finished: 进程结束时回调，签名为 (return_code: int) -> None
    """
    global _process, _stop_event

    _stop_event.clear()
    _full_output: list[str] = []

    def _read():
        global _process
        if not _process:
            return
        try:
            for line in iter(_process.stdout.readline, ""):
                if not line:
                    break
                _full_output.append(line)
                on_output(line)
        except Exception:
            pass
        finally:
            try:
                _process.stdout.close()
            except Exception:
                pass

        # 等待进程退出
        try:
            rc = _process.wait()
        except Exception:
            rc = -1

        # 用 after 回调主线程（因为 tkinter 不是线程安全的）
        on_finished(rc)

    try:
        _process = subprocess.Popen(
            [python_bin, str(script_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            text=True,
            preexec_fn=os.setsid,
        )
    except Exception as e:
        on_output(f"\n❌ 启动失败: {e}\n")
        on_finished(-1)
        return

    t = threading.Thread(target=_read, daemon=True)
    t.start()


def kill_process(
    on_killed: Optional[Callable[[str], None]] = None,
) -> bool:
    """
    向当前进程发送 SIGINT 截断信号。

    Returns:
        True  - 成功发送
        False - 当前无进程或进程已结束
    """
    global _process
    if _process and _process.poll() is None:
        try:
            os.killpg(os.getpgid(_process.pid), signal.SIGINT)
            if on_killed:
                on_killed("\n\n⚠️ 已发送截断信号（SIGINT）...\n")
            return True
        except Exception as e:
            if on_killed:
                on_killed(f"\n\n❌ 截断失败: {e}\n")
            return False
    return False


def terminate_process() -> None:
    """强制结束当前进程（SIGTERM）。"""
    global _process
    if _process and _process.poll() is None:
        try:
            os.killpg(os.getpgid(_process.pid), signal.SIGTERM)
        except Exception:
            pass
    _process = None


def set_stop_flag() -> None:
    """设置停止标志，让读线程安全退出。"""
    _stop_event.set()


def is_running() -> bool:
    """判断当前是否有进程在运行。"""
    return _process is not None and _process.poll() is None
