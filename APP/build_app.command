#!/bin/bash
# 启动脚本运行器应用（使用动态路径）

# 获取脚本所在目录（APP 文件夹）
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 检查是否已安装 pyinstaller
if ! command -v pyinstaller &> /dev/null; then
    echo "正在安装 pyinstaller..."
    pip install pyinstaller
fi

# 打包成 macOS 应用
cd "$SCRIPT_DIR"
pyinstaller --name="脚本运行器" --windowed --onefile run_app.py

echo "打包完成！应用在 dist 目录下"
open dist
