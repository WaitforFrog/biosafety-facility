"""
本地脚本运行器 - 桌面应用
使用 Python 内置 tkinter
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import json
import os
from datetime import datetime
from pathlib import Path
import threading
import sys

# 配置路径
SCRIPTS_DIR = Path("/Users/guot/Desktop/杰昊/AI推广/域名推广/Code")
LOGS_DIR = SCRIPTS_DIR / "文章" / "汇总日志"
VENV_PYTHON = SCRIPTS_DIR / ".venv" / "bin" / "python3"

# 可运行的脚本
AVAILABLE_SCRIPTS = {
    "Trust_EN_html.py": "翻译并生成英文HTML",
    "Translate.py": "翻译脚本",
    "build_preview_site.py": "构建预览站点",
    "build_category_indexes.py": "构建分类索引",
    "build_articles_index.py": "构建文章索引",
    "delete_chinese_articles.py": "删除中文文章"
}


class ScriptRunnerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("脚本运行器")
        self.root.geometry("900x700")
        
        # 当前运行的任务
        self.current_process = None
        self.is_running = False
        
        self.setup_ui()
        self.load_history()
    
    def setup_ui(self):
        """设置UI"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # ===== 左侧：运行控制 =====
        left_frame = ttk.LabelFrame(main_frame, text="运行脚本", padding="10")
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # 脚本选择
        ttk.Label(left_frame, text="选择脚本:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.script_var = tk.StringVar()
        self.script_combo = ttk.Combobox(left_frame, textvariable=self.script_var, width=30)
        self.script_combo['values'] = [f"{k} - {v}" for k, v in AVAILABLE_SCRIPTS.items()]
        self.script_combo.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        if self.script_combo['values']:
            self.script_combo.current(0)
        
        # 运行按钮
        self.run_btn = ttk.Button(left_frame, text="运行脚本", command=self.run_script)
        self.run_btn.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # 停止按钮
        self.stop_btn = ttk.Button(left_frame, text="停止", command=self.stop_script, state=tk.DISABLED)
        self.stop_btn.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 状态显示
        self.status_label = ttk.Label(left_frame, text="就绪", foreground="green")
        self.status_label.grid(row=4, column=0, sticky=tk.W)
        
        # 输出区域
        ttk.Label(left_frame, text="输出:").grid(row=5, column=0, sticky=tk.W, pady=(10, 5))
        self.output_text = scrolledtext.ScrolledText(left_frame, width=40, height=20, state=tk.DISABLED)
        self.output_text.grid(row=6, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        left_frame.rowconfigure(6, weight=1)
        
        # ===== 右侧：历史记录 =====
        right_frame = ttk.LabelFrame(main_frame, text="运行历史", padding="10")
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        # 刷新按钮
        ttk.Button(right_frame, text="刷新", command=self.load_history).grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # 历史记录列表
        columns = ("time", "total", "success", "error")
        self.history_tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=15)
        self.history_tree.heading("time", text="运行时间")
        self.history_tree.heading("total", text="总数")
        self.history_tree.heading("success", text="成功")
        self.history_tree.heading("error", text="失败")
        
        self.history_tree.column("time", width=150)
        self.history_tree.column("total", width=50)
        self.history_tree.column("success", width=50)
        self.history_tree.column("error", width=50)
        
        self.history_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 滚动条
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        
        # 查看详情按钮
        ttk.Button(right_frame, text="查看详情", command=self.show_detail).grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)
        
        right_frame.rowconfigure(1, weight=1)
        right_frame.columnconfigure(0, weight=1)
        
        # 布局权重
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # 双击事件
        self.history_tree.bind("<Double-1>", lambda e: self.show_detail())
    
    def load_history(self):
        """加载历史记录"""
        # 清空现有数据
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        if not LOGS_DIR.exists():
            return
        
        # 获取所有日志文件
        log_files = sorted(LOGS_DIR.glob("*.json"), key=os.path.getmtime, reverse=True)
        
        for log_file in log_files[:50]:  # 最多显示50条
            try:
                log_data = json.loads(log_file.read_text(encoding='utf-8'))
                run_time = log_data.get("run_time", "未知")
                total = log_data.get("total_products", 0)
                success = log_data.get("success_count", 0)
                error = log_data.get("error_count", 0)
                
                self.history_tree.insert("", tk.END, values=(run_time, total, success, error), tags=(log_file.name,))
            except Exception as e:
                print(f"加载日志出错: {e}")
    
    def show_detail(self):
        """显示选中记录的详情"""
        selection = self.history_tree.selection()
        if not selection:
            messagebox.showinfo("提示", "请先选择一条记录")
            return
        
        item = self.history_tree.item(selection[0])
        values = item["values"]
        run_time = values[0]
        
        # 查找对应的日志文件
        log_files = sorted(LOGS_DIR.glob("*.json"), key=os.path.getmtime, reverse=True)
        target_log = None
        
        for log_file in log_files:
            log_data = json.loads(log_file.read_text(encoding='utf-8'))
            if log_data.get("run_time") == run_time:
                target_log = log_data
                break
        
        if not target_log:
            messagebox.showerror("错误", "找不到对应的日志文件")
            return
        
        # 创建详情窗口
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"运行详情 - {run_time}")
        detail_window.geometry("600x500")
        
        # 基本信息
        info_frame = ttk.Frame(detail_window, padding="10")
        info_frame.pack(fill=tk.X)
        
        ttk.Label(info_frame, text=f"运行时间: {target_log.get('run_time', '-')}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"产品总数: {target_log.get('total_products', 0)}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"成功: {target_log.get('success_count', 0)}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"失败: {target_log.get('error_count', 0)}").pack(anchor=tk.W)
        
        # 结果列表
        ttk.Label(detail_window, text="运行结果:").pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        result_frame = ttk.Frame(detail_window)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # 结果表格
        columns = ("product", "status", "path")
        result_tree = ttk.Treeview(result_frame, columns=columns, show="headings")
        result_tree.heading("product", text="产品名")
        result_tree.heading("status", text="状态")
        result_tree.heading("path", text="保存位置")
        
        result_tree.column("product", width=150)
        result_tree.column("status", width=80)
        result_tree.column("path", width=300)
        
        result_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=result_tree.yview)
        result_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 填充数据
        for result in target_log.get("results", []):
            product = result.get("product_name", "未知")
            status = "成功" if result.get("success") else "失败"
            path = result.get("backup_path", "-")
            result_tree.insert("", tk.END, values=(product, status, path))
    
    def run_script(self):
        """运行选中的脚本"""
        if self.is_running:
            return
        
        selected = self.script_var.get()
        if not selected:
            messagebox.showwarning("警告", "请先选择要运行的脚本")
            return
        
        # 提取脚本名
        script_name = selected.split(" - ")[0]
        script_path = SCRIPTS_DIR / script_name
        
        if not script_path.exists():
            messagebox.showerror("错误", f"脚本不存在: {script_name}")
            return
        
        # 更新状态
        self.is_running = True
        self.run_btn.configure(state=tk.DISABLED)
        self.stop_btn.configure(state=tk.NORMAL)
        self.status_label.configure(text="运行中...", foreground="orange")
        
        # 清空输出
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"正在运行 {script_name}...\n")
        self.output_text.configure(state=tk.DISABLED)
        
        # 在新线程中运行
        thread = threading.Thread(target=self._run_in_thread, args=(script_path,))
        thread.daemon = True
        thread.start()
    
    def _run_in_thread(self, script_path):
        """在线程中运行脚本"""
        try:
            # 确定使用哪个Python解释器
            if VENV_PYTHON.exists():
                python_exe = str(VENV_PYTHON)
            else:
                python_exe = "python3"
            
            self.current_process = subprocess.Popen(
                [python_exe, str(script_path)],
                cwd=str(SCRIPTS_DIR),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            # 实时读取输出
            for line in self.current_process.stdout:
                self.root.after(0, self._append_output, line)
            
            # 等待完成
            return_code = self.current_process.wait()
            self.current_process = None
            
            # 更新UI
            self.root.after(0, self._on_script_finished, return_code)
            
        except Exception as e:
            self.root.after(0, self._append_output, f"错误: {str(e)}\n")
            self.root.after(0, self._on_script_finished, -1)
    
    def _append_output(self, text):
        """追加输出文本"""
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)
        self.output_text.configure(state=tk.DISABLED)
    
    def _on_script_finished(self, return_code):
        """脚本运行完成回调"""
        self.is_running = False
        self.run_btn.configure(state=tk.NORMAL)
        self.stop_btn.configure(state=tk.DISABLED)
        
        if return_code == 0:
            self.status_label.configure(text="运行成功", foreground="green")
            messagebox.showinfo("成功", "脚本运行成功！")
            # 刷新历史记录
            self.load_history()
        else:
            self.status_label.configure(text="运行失败", foreground="red")
            messagebox.showerror("失败", f"脚本运行失败，返回码: {return_code}")
    
    def stop_script(self):
        """停止运行"""
        if self.current_process:
            self.current_process.terminate()
            self.current_process = None
            self.is_running = False
            self.run_btn.configure(state=tk.NORMAL)
            self.stop_btn.configure(state=tk.DISABLED)
            self.status_label.configure(text="已停止", foreground="red")
            self._append_output("\n[已手动停止]\n")


def main():
    root = tk.Tk()
    app = ScriptRunnerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
