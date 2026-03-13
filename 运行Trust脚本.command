#!/bin/bash
# 双击运行 Trust_EN_html.py（翻译并生成英文HTML）
# 无需 tkinter，直接运行

cd "/Users/guot/Desktop/杰昊/AI推广/域名推广/Code"

# 优先使用虚拟环境（有依赖包），否则用系统 Python
if [ -f ".venv/bin/python3" ]; then
    .venv/bin/python3 Trust_EN_html.py
else
    /usr/bin/python3 Trust_EN_html.py
fi

echo ""
echo "完成！按回车键关闭窗口..."
read
