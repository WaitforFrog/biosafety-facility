#!/bin/bash
# 运行脚本管理器

cd "/Users/guot/Desktop/杰昊/AI推广/域名推广/Code"

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
"$PYTHON" script_manager_app.py

echo ""
echo "完成！按回车键关闭窗口..."
read
