#!/bin/bash
# 打包杰昊脚本管理器.app
# 使用 PyInstaller --onedir 模式（更可靠）

cd "$(dirname "$0")"

echo "正在清理旧构建..."
rm -rf dist build *.spec

echo ""
echo "正在打包（--onedir 模式）..."
pyinstaller \
    --name="杰昊脚本管理器" \
    --onedir \
    --windowed \
    --icon="/Users/guot/Desktop/杰昊/AI推广/域名推广/Code/JIEHAO_LOGO.icns" \
    run_app.py

echo ""
echo "打包完成！"
echo "APP 文件位于: dist/杰昊脚本管理器.app"
echo ""
echo "你可以按住 Cmd 并拖动将它移到应用程序文件夹。"
