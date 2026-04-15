#!/bin/bash
# 运行脚本管理器

# 获取脚本所在目录（APP 文件夹）
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Code 目录是 APP 的父目录
CODE_DIR="$( dirname "$SCRIPT_DIR" )"

cd "$CODE_DIR"

# 优先使用系统 Python，避免 Homebrew Python 与 macOS 版本不兼容导致的崩溃
# （如 "macOS 15 (1507) or later required, have instead 15 (1506)" 错误）
if [ -x "/usr/bin/python3" ]; then
    PYTHON="/usr/bin/python3"
elif [ -x "/opt/homebrew/bin/python3" ]; then
    PYTHON="/opt/homebrew/bin/python3"
else
    PYTHON="python3"
fi

# 运行脚本
"$PYTHON" APP/script_manager_app.py

echo ""
echo "完成！按回车键关闭窗口..."
read
