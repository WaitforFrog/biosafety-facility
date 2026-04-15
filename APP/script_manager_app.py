"""
域名推广脚本管理器 - 使用AppleScript对话框版本
功能：
- 通过AppleScript显示原生对话框
- 运行脚本并显示输出
"""

import subprocess
import json
import os
from datetime import datetime
from pathlib import Path
import threading

# 配置路径（动态获取，不依赖硬编码绝对路径）
SCRIPT_DIR = Path(__file__).parent.parent.resolve()
SCRIPTS_DIR = SCRIPT_DIR
LOGS_DIR = SCRIPTS_DIR / "文章" / "汇总日志"
PRODUCE_DIR = SCRIPTS_DIR / "Produce"
VENV_PYTHON = SCRIPTS_DIR / ".venv" / "bin" / "python3"
PYTHON_BIN = VENV_PYTHON if VENV_PYTHON.exists() else (Path("/usr/bin/python3") if Path("/usr/bin/python3").exists() else Path("/opt/homebrew/bin/python3"))

# 可管理的脚本（相对于 SCRIPTS_DIR）
AVAILABLE_SCRIPTS = {
    "Produce/Trust_EN_html.py": "翻译并生成英文HTML（中立科普）",
    "Produce/Compare_EN_html.py": "市场分析类文章生成器",
    "Translate.py": "翻译脚本",
    "Produce/Tool/build_preview_site.py": "构建预览站点",
    "Produce/Tool/build_category_indexes.py": "构建分类索引",
    "Produce/Tool/build_articles_index.py": "构建文章索引",
    "delete_chinese_articles.py": "删除中文文章"
}


def show_dialog(title, message, dialog_type="informational"):
    """显示AppleScript对话框"""
    if dialog_type == "warning":
        script = f'display dialog "{message}" with title "{title}" with icon caution buttons {{"确定"}}'
    elif dialog_type == "error":
        script = f'display dialog "{message}" with title "{title}" with icon stop buttons {{"确定"}}'
    else:
        script = f'display dialog "{message}" with title "{title}" with icon note buttons {{"确定"}}'
    
    subprocess.run(["osascript", "-e", script], capture_output=True)


def show_choice_dialog(title, message, choices):
    """显示选择对话框，返回用户选择的索引（0-based）"""
    choices_str = ", ".join([f'"{c}"' for c in choices])
    script = f'''
    set theAnswer to choose from list {{{choices_str}}} with title "{title}" with prompt "{message}" OK button name "选择" cancel button name "取消"
    if theAnswer is false then
        return "CANCEL"
    else
        return item 1 of theAnswer
    end if
    '''
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    return result.stdout.strip()


def run_script_and_get_output(script_path):
    """运行脚本并返回输出"""
    python_exe = str(PYTHON_BIN) if PYTHON_BIN.exists() else "python3"
    
    process = subprocess.Popen(
        [python_exe, str(script_path)],
        cwd=str(SCRIPTS_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    output_lines = []
    for line in process.stdout:
        output_lines.append(line)
    
    return_code = process.wait()
    return "".join(output_lines), return_code


def get_log_files():
    """获取所有日志文件"""
    log_files = []
    if LOGS_DIR.exists():
        log_files = sorted(LOGS_DIR.glob("*.json"), key=os.path.getmtime, reverse=True)
    return log_files


def show_log_calendar(script_name):
    """显示日历选择界面查看日志"""
    log_files = get_log_files()
    
    if not log_files:
        show_dialog("日志查看", "暂无运行日志", "informational")
        return
    
    # 按日期分组日志
    logs_by_date = {}
    for log_file in log_files:
        try:
            log_data = json.loads(log_file.read_text(encoding='utf-8'))
            run_time = log_data.get("run_time", "")
            date = run_time.split(" ")[0] if run_time else "未知"
            if date not in logs_by_date:
                logs_by_date[date] = []
            logs_by_date[date].append(log_data)
        except:
            pass
    
    dates = sorted(logs_by_date.keys(), reverse=True)
    
    if not dates:
        show_dialog("日志查看", "暂无运行日志", "informational")
        return
    
    # 让用户选择日期
    date_choices = [f"{date} ({len(logs_by_date[date])}次运行)" for date in dates]
    selected = show_choice_dialog("选择日期", f"选择要查看的日期：", date_choices)
    
    if selected == "CANCEL":
        return
    
    # 提取日期
    date = selected.split(" (")[0]
    logs = logs_by_date.get(date, [])
    
    # 显示日志详情
    detail_text = f"=== {date} 运行记录 ===\n\n"
    
    for i, log in enumerate(logs, 1):
        detail_text += f"--- 第 {i} 次运行 ---\n"
        detail_text += f"时间: {log.get('run_time', '-')}\n"
        detail_text += f"总数: {log.get('total_products', 0)}\n"
        detail_text += f"成功: {log.get('success_count', 0)}\n"
        detail_text += f"失败: {log.get('error_count', 0)}\n\n"
        
        results = log.get("results", [])
        if results:
            detail_text += "运行结果:\n"
            for r in results:
                product = r.get("product_name", "未知")
                status = "✅" if r.get("success") else "❌"
                detail_text += f"  {status} {product}\n"
                if r.get("backup_path"):
                    detail_text += f"      路径: {r.get('backup_path')}\n"
            detail_text += "\n"
    
    # 显示详情（通过临时文件）
    detail_file = SCRIPTS_DIR / ".log_detail.txt"
    detail_file.write_text(detail_text, encoding='utf-8')
    subprocess.run(["open", str(detail_file)])


def run_script_interactive(script_name, description):
    """交互式运行脚本"""
    script_path = SCRIPTS_DIR / script_name
    
    if not script_path.exists():
        show_dialog("错误", f"脚本不存在: {script_name}", "error")
        return
    
    # 确认运行
    confirm = subprocess.run(
        ["osascript", "-e", f'display dialog "确定要运行 {script_name} 吗？\\n\\n{description}" with title "确认运行" buttons {{"运行", "取消"}} default button 2'],
        capture_output=True,
        text=True
    )
    
    if "Cancel" in confirm.stdout or confirm.returncode != 0:
        show_dialog("取消", "已取消运行", "informational")
        return
    
    # 运行脚本
    show_dialog("运行中", f"正在运行 {script_name}...\n\n请查看终端输出", "informational")
    
    output, return_code = run_script_and_get_output(script_path)
    
    # 保存输出到文件
    output_file = SCRIPTS_DIR / f".run_output_{script_name}.txt"
    output_file.write_text(output, encoding='utf-8')
    
    # 显示结果
    if return_code == 0:
        show_dialog("成功", f"{script_name} 运行成功！\n\n输出已保存到桌面", "informational")
    else:
        show_dialog("失败", f"{script_name} 运行失败 (返回码: {return_code})", "warning")
    
    # 打开输出文件
    subprocess.run(["open", str(output_file)])


def main():
    """主函数 - 显示脚本选择菜单"""
    # 显示欢迎信息
    subprocess.run([
        "osascript", "-e",
        'display dialog "欢迎使用脚本管理器！\n\n请选择一个操作：" with title "域名推广脚本管理器" buttons {"运行脚本", "查看日志", "退出"} default button 1'
    ], capture_output=True)
    
    while True:
        # 显示脚本选择
        choices = list(AVAILABLE_SCRIPTS.keys()) + ["返回主菜单", "退出"]
        
        selected = show_choice_dialog(
            "脚本选择",
            "选择要运行的脚本：",
            choices
        )
        
        if selected == "CANCEL" or selected == "退出":
            break
        
        if selected == "返回主菜单":
            continue
        
        if selected in AVAILABLE_SCRIPTS:
            description = AVAILABLE_SCRIPTS[selected]
            
            # 询问操作
            action = show_choice_dialog(
                "选择操作",
                f"选择对 {selected} 的操作：",
                ["运行脚本", "查看日志", "返回"]
            )
            
            if action == "运行脚本":
                run_script_interactive(selected, description)
            elif action == "查看日志":
                show_log_calendar(selected)
            # 返回则继续循环


if __name__ == "__main__":
    main()