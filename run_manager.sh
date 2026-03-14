#!/bin/bash
# 启动脚本管理器应用

cd "/Users/guot/Desktop/杰昊/AI推广/域名推广/Code"

# 检查虚拟环境
if [ -f ".venv/bin/python3" ]; then
    PYTHON=".venv/bin/python3"
else
    PYTHON="python3"
fi

# 运行脚本管理器
exec "$PYTHON" script_manager_app.py