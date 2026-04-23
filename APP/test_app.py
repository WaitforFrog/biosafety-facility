import sys
import os
print(f"Python: {sys.executable}")
print(f"Version: {sys.version}")
try:
    import tkinter as tk
    root = tk.Tk()
    root.title("Test")
    tk.Label(root, text="Hello from tkinter!").pack(padx=20, pady=20)
    root.after(2000, root.destroy)  # Auto-close after 2 seconds
    root.mainloop()
    print("SUCCESS: tkinter worked!")
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
