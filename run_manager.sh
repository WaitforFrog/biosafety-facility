#!/bin/bash
# 启动脚本管理器应用（使用动态路径）

# 获取脚本所在目录的父目录（Code 目录）
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
APP_DIR="$SCRIPT_DIR/APP"

# 检查虚拟环境
if [ -f ".venv/bin/python3" ]; then
    PYTHON=".venv/bin/python3"
else
    PYTHON="python3"
fi

# 运行脚本管理器
exec "$PYTHON" APP/script_manager_app.py
