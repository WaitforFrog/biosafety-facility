#!/bin/bash
# 构建脚本管理器 .app 应用

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 检查是否已安装 pyinstaller
if ! command -v pyinstaller &> /dev/null; then
    echo "正在安装 pyinstaller..."
    pip install pyinstaller
fi

# 删除旧的构建
rm -rf build dist "脚本管理器.app"

# 打包成 macOS 应用（使用 run_app.py - tkinter GUI 版本）
cd "$SCRIPT_DIR"
pyinstaller --name="脚本管理器" --windowed --onefile run_app.py

# 移动到原位置
mv dist/脚本管理器.app .

echo "打包完成！"
open .
