"""
本地脚本运行器 - 桌面应用
使用 Python 内置 tkinter
功能：
- 主菜单选择（运行脚本/查看日志）
- 实时显示脚本输出
- 运行历史查看
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

# 配置路径（动态获取，不依赖硬编码绝对路径）
SCRIPT_DIR = Path(__file__).parent.parent.resolve()
SCRIPTS_DIR = SCRIPT_DIR
LOGS_DIR = SCRIPTS_DIR / "文章" / "汇总日志"
VENV_PYTHON = SCRIPTS_DIR / ".venv" / "bin" / "python3"
PRODUCE_DIR = SCRIPTS_DIR / "Produce"

# 可运行的脚本（相对于 SCRIPTS_DIR）
AVAILABLE_SCRIPTS = {
    "Produce/Trust_EN_html.py": "翻译并生成英文HTML（中立科普）",
    "Produce/Compare_EN_html.py": "市场分析类文章生成器",
    "Produce/Compare_JIEHAO.py": "JIEHAO对比分析生成器",
    "Produce/Introduction_EN_html.py": "介绍类英文HTML生成器",
    "Translate.py": "翻译脚本",
    "Produce/Tool/build_preview_site.py": "构建预览站点",
    "Produce/Tool/build_category_indexes.py": "构建分类索引",
    "Produce/Tool/build_articles_index.py": "构建文章索引",
    "delete_chinese_articles.py": "删除中文文章"
}


class ScriptRunnerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("脚本管理器")
        self.root.geometry("1000x700")
        
        # 当前运行的任务
        self.current_process = None
        self.is_running = False
        
        # 当前选中的脚本
        self.selected_script = None
        
        self.show_main_menu()
    
    def show_main_menu(self):
        """显示主菜单"""
        # 清空所有组件
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 主框架居中
        center_frame = tk.Frame(self.root)
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # 标题
        title_label = tk.Label(
            center_frame, 
            text="脚本管理器", 
            font=("Arial", 24, "bold"),
            pady=30
        )
        title_label.pack()
        
        # 副标题
        subtitle_label = tk.Label(
            center_frame,
            text="请选择一个操作：",
            font=("Arial", 12),
            pady=10
        )
        subtitle_label.pack()
        
        # 运行脚本按钮
        run_btn = tk.Button(
            center_frame,
            text="运行脚本",
            font=("Arial", 14),
            width=20,
            height=2,
            bg="#4CAF50",
            fg="white",
            relief=tk.RAISED,
            command=self.show_script_selector
        )
        run_btn.pack(pady=15)
        
        # 查看日志按钮
        log_btn = tk.Button(
            center_frame,
            text="查看日志",
            font=("Arial", 14),
            width=20,
            height=2,
            bg="#2196F3",
            fg="white",
            relief=tk.RAISED,
            command=self.show_log_viewer
        )
        log_btn.pack(pady=15)
        
        # 退出按钮
        exit_btn = tk.Button(
            center_frame,
            text="退出",
            font=("Arial", 12),
            width=15,
            height=1,
            bg="#9E9E9E",
            fg="white",
            relief=tk.RAISED,
            command=self.root.quit
        )
        exit_btn.pack(pady=30)
    
    def show_script_selector(self):
        """显示脚本选择界面"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # 顶部标题栏
        header_frame = tk.Frame(main_frame, bg="#2C3E50", height=50)
        header_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E))
        header_frame.columnconfigure(0, weight=1)
        
        # 返回按钮
        back_btn = tk.Button(
            header_frame,
            text="< 返回",
            font=("Arial", 12),
            bg="#34495E",
            fg="white",
            relief=tk.FLAT,
            padx=15,
            command=self.show_main_menu
        )
        back_btn.grid(row=0, column=0, sticky=tk.W, pady=10, padx=10)
        
        # 标题
        title_label = tk.Label(
            header_frame,
            text="选择要运行的脚本",
            font=("Arial", 16, "bold"),
            bg="#2C3E50",
            fg="white",
            pady=10
        )
        title_label.grid(row=0, column=1, sticky=tk.W)
        
        # 脚本选择区域
        selector_frame = ttk.LabelFrame(main_frame, text="脚本列表", padding="10")
        selector_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 5))
        
        # 创建脚本列表
        self.script_listbox = tk.Listbox(
            selector_frame,
            font=("Arial", 11),
            height=8,
            selectmode=tk.SINGLE,
            bg="white",
            relief=tk.SOLID,
            bd=1
        )
        self.script_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 滚动条
        scrollbar = tk.Scrollbar(selector_frame, orient=tk.VERTICAL)
        scrollbar.config(command=self.script_listbox.yview)
        self.script_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 填充脚本列表
        self.script_items = []
        for script_path, description in AVAILABLE_SCRIPTS.items():
            display_text = f"{script_path} - {description}"
            self.script_listbox.insert(tk.END, display_text)
            self.script_items.append(script_path)
        
        if self.script_items:
            self.script_listbox.select_set(0)
        
        # 脚本描述显示
        desc_frame = ttk.Frame(main_frame)
        desc_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        self.desc_label = tk.Label(
            desc_frame,
            text="请从上方列表选择一个脚本",
            font=("Arial", 10),
            fg="#666"
        )
        self.desc_label.pack(anchor=tk.W)
        
        # 选中脚本时更新描述
        self.script_listbox.bind('<<ListboxSelect>>', self.on_script_select)
        
        # 运行和返回按钮
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # 返回按钮
        return_btn = tk.Button(
            button_frame,
            text="返回",
            font=("Arial", 12),
            width=10,
            bg="#95A5A6",
            fg="white",
            relief=tk.RAISED,
            command=self.show_main_menu
        )
        return_btn.pack(side=tk.LEFT, padx=5)
        
        # 运行按钮
        self.run_btn = tk.Button(
            button_frame,
            text="运行脚本",
            font=("Arial", 12),
            width=10,
            bg="#27AE60",
            fg="white",
            relief=tk.RAISED,
            command=self.run_selected_script
        )
        self.run_btn.pack(side=tk.LEFT, padx=5)
    
    def on_script_select(self, event):
        """脚本选中事件"""
        selection = self.script_listbox.curselection()
        if selection:
            index = selection[0]
            script_path = self.script_items[index]
            description = AVAILABLE_SCRIPTS.get(script_path, "")
            self.desc_label.config(text=f"已选择: {description}")
    
    def run_selected_script(self):
        """运行选中的脚本"""
        selection = self.script_listbox.curselection()
        if not selection:
            messagebox.showwarning("提示", "请先选择一个脚本")
            return
        
        index = selection[0]
        script_name = self.script_items[index]
        script_path = SCRIPTS_DIR / script_name
        
        if not script_path.exists():
            messagebox.showerror("错误", f"脚本不存在: {script_name}")
            return
        
        self.selected_script = script_name
        self.show_running_view(script_path)
    
    def show_running_view(self, script_path):
        """显示运行界面"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # 顶部标题栏
        header_frame = tk.Frame(main_frame, bg="#E74C3C", height=50)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        header_frame.columnconfigure(0, weight=1)
        
        # 标题
        title_label = tk.Label(
            header_frame,
            text=f"正在运行: {self.selected_script}",
            font=("Arial", 14, "bold"),
            bg="#E74C3C",
            fg="white",
            pady=15
        )
        title_label.pack()
        
        # 状态标签
        self.status_label = tk.Label(
            main_frame,
            text="⏳ 脚本运行中...",
            font=("Arial", 12),
            fg="#F39C12"
        )
        self.status_label.grid(row=1, column=0, sticky=tk.W, pady=10)
        
        # 输出区域框架
        output_frame = ttk.LabelFrame(main_frame, text="终端输出", padding="5")
        output_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        main_frame.rowconfigure(2, weight=1)
        
        # 输出文本区域
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            font=("Courier New", 10),
            bg="#1E1E1E",
            fg="#00FF00",
            insertbackground="white",
            relief=tk.SUNKEN,
            bd=2
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # 初始提示
        self.output_text.insert(tk.END, f"正在启动 {self.selected_script}...\n")
        self.output_text.insert(tk.END, "=" * 50 + "\n")
        self.output_text.see(tk.END)
        
        # 底部按钮
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # 停止按钮
        self.stop_btn = tk.Button(
            button_frame,
            text="停止",
            font=("Arial", 12),
            width=10,
            bg="#E74C3C",
            fg="white",
            relief=tk.RAISED,
            state=tk.NORMAL,
            command=self.stop_script
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # 返回按钮
        return_btn = tk.Button(
            button_frame,
            text="返回",
            font=("Arial", 12),
            width=10,
            bg="#95A5A6",
            fg="white",
            relief=tk.RAISED,
            state=tk.DISABLED,
            command=self.show_main_menu
        )
        return_btn.pack(side=tk.LEFT, padx=5)
        
        # 保存返回按钮引用
        self.return_btn_after_finish = return_btn
        
        # 在新线程中运行脚本
        self.is_running = True
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
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)
    
    def _on_script_finished(self, return_code):
        """脚本运行完成回调"""
        self.is_running = False
        
        # 添加完成标记
        self.output_text.insert(tk.END, "\n" + "=" * 50 + "\n")
        
        if return_code == 0:
            self.status_label.config(text="✓ 运行成功", fg="#27AE60")
            self.output_text.insert(tk.END, "\n脚本已成功完成运行！\n")
        else:
            self.status_label.config(text=f"✗ 运行失败 (返回码: {return_code})", fg="#E74C3C")
            self.output_text.insert(tk.END, f"\n脚本运行失败，返回码: {return_code}\n")
        
        self.output_text.see(tk.END)
        
        # 启用返回按钮
        self.stop_btn.config(state=tk.DISABLED)
        self.return_btn_after_finish.config(state=tk.NORMAL)
        
        # 自动刷新历史记录
        self.load_history()
    
    def stop_script(self):
        """停止运行"""
        if self.current_process:
            self.current_process.terminate()
            try:
                self.current_process.wait(timeout=5)
            except:
                self.current_process.kill()
            self.current_process = None
        
        self.is_running = False
        self.status_label.config(text="已停止", fg="#E74C3C")
        self.output_text.insert(tk.END, "\n[已手动停止]\n")
        self.stop_btn.config(state=tk.DISABLED)
        self.return_btn_after_finish.config(state=tk.NORMAL)
    
    def show_log_viewer(self):
        """显示日志查看界面"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # 顶部标题栏
        header_frame = tk.Frame(main_frame, bg="#3498DB", height=50)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))
        header_frame.columnconfigure(0, weight=1)
        
        # 返回按钮
        back_btn = tk.Button(
            header_frame,
            text="< 返回",
            font=("Arial", 12),
            bg="#2980B9",
            fg="white",
            relief=tk.FLAT,
            padx=15,
            command=self.show_main_menu
        )
        back_btn.grid(row=0, column=0, sticky=tk.W, pady=10, padx=10)
        
        # 标题
        title_label = tk.Label(
            header_frame,
            text="运行历史记录",
            font=("Arial", 16, "bold"),
            bg="#3498DB",
            fg="white",
            pady=10
        )
        title_label.grid(row=0, column=1, sticky=tk.W)
        
        # 历史记录表格
        columns = ("time", "script", "total", "success", "error")
        self.history_tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=20)
        
        self.history_tree.heading("time", text="运行时间")
        self.history_tree.heading("script", text="脚本名称")
        self.history_tree.heading("total", text="总数")
        self.history_tree.heading("success", text="成功")
        self.history_tree.heading("error", text="失败")
        
        self.history_tree.column("time", width=150)
        self.history_tree.column("script", width=250)
        self.history_tree.column("total", width=60)
        self.history_tree.column("success", width=60)
        self.history_tree.column("error", width=60)
        
        self.history_tree.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=2, sticky=(tk.N, tk.S), pady=10)
        
        # 按钮框架
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # 刷新按钮
        refresh_btn = tk.Button(
            button_frame,
            text="刷新",
            font=("Arial", 12),
            width=10,
            bg="#27AE60",
            fg="white",
            relief=tk.RAISED,
            command=self.load_history
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # 查看详情按钮
        detail_btn = tk.Button(
            button_frame,
            text="查看详情",
            font=("Arial", 12),
            width=10,
            bg="#3498DB",
            fg="white",
            relief=tk.RAISED,
            command=self.show_detail
        )
        detail_btn.pack(side=tk.LEFT, padx=5)
        
        # 返回按钮
        return_btn = tk.Button(
            button_frame,
            text="返回",
            font=("Arial", 12),
            width=10,
            bg="#95A5A6",
            fg="white",
            relief=tk.RAISED,
            command=self.show_main_menu
        )
        return_btn.pack(side=tk.LEFT, padx=5)
        
        main_frame.rowconfigure(1, weight=1)
        
        # 双击事件
        self.history_tree.bind("<Double-1>", lambda e: self.show_detail())
        
        # 加载历史记录
        self.load_history()
    
    def load_history(self):
        """加载历史记录"""
        # 清空现有数据
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        if not LOGS_DIR.exists():
            return
        
        # 获取所有日志文件
        log_files = sorted(LOGS_DIR.glob("*.json"), key=os.path.getmtime, reverse=True)
        
        for log_file in log_files[:100]:  # 最多显示100条
            try:
                log_data = json.loads(log_file.read_text(encoding='utf-8'))
                run_time = log_data.get("run_time", "未知")
                script_name = log_data.get("script_name", log_file.stem)
                total = log_data.get("total_products", 0)
                success = log_data.get("success_count", 0)
                error = log_data.get("error_count", 0)
                
                self.history_tree.insert("", tk.END, values=(run_time, script_name, total, success, error))
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
            try:
                log_data = json.loads(log_file.read_text(encoding='utf-8'))
                if log_data.get("run_time") == run_time:
                    target_log = log_data
                    break
            except:
                continue
        
        if not target_log:
            messagebox.showerror("错误", "找不到对应的日志文件")
            return
        
        # 创建详情窗口
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"运行详情 - {run_time}")
        detail_window.geometry("700x500")
        
        # 基本信息
        info_frame = ttk.Frame(detail_window, padding="10")
        info_frame.pack(fill=tk.X)
        
        script_name = target_log.get("script_name", "-")
        ttk.Label(info_frame, text=f"脚本: {script_name}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"运行时间: {target_log.get('run_time', '-')}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"产品总数: {target_log.get('total_products', 0)}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"成功: {target_log.get('success_count', 0)}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"失败: {target_log.get('error_count', 0)}").pack(anchor=tk.W)
        
        # 结果列表
        ttk.Label(detail_window, text="运行结果:", font=("Arial", 11, "bold")).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
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
        result_tree.column("path", width=400)
        
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


def main():
    root = tk.Tk()
    app = ScriptRunnerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
