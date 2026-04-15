#!/bin/bash
# 双击运行脚本运行器

# 获取脚本所在目录的父目录（Code 目录）
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 使用系统Python（自带tkinter支持）
/usr/bin/python3 "$SCRIPT_DIR/APP/run_app.py"
