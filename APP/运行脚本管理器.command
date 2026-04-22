#!/bin/bash
# 运行脚本管理器 (tkinter GUI版本，支持界面内终端输出)

# 获取脚本所在目录（APP 文件夹）
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Code 目录是 APP 的父目录
CODE_DIR="$( dirname "$SCRIPT_DIR" )"

cd "$CODE_DIR"

# 优先使用虚拟环境中的 Python
if [ -f ".venv/bin/python3" ]; then
    PYTHON=".venv/bin/python3"
elif [ -x "/usr/bin/python3" ]; then
    PYTHON="/usr/bin/python3"
elif [ -x "/opt/homebrew/bin/python3" ]; then
    PYTHON="/opt/homebrew/bin/python3"
else
    PYTHON="python3"
fi

# 运行脚本（使用 tkinter 版本，支持界面内终端输出）
"$PYTHON" APP/run_app.py
