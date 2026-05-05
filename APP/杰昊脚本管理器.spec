# -*- mode: python ; coding: utf-8 -*-

import os

APP_NAME  = "杰昊脚本管理器"
# 从 spec 文件所在目录推导路径（pyinstaller 从当前工作目录执行 spec）
# spec 在 APP/ 下，所以 CWD 就是 APP/
APP_DIR   = os.getcwd()
CODE_DIR  = os.path.dirname(APP_DIR)   # Code/
SCRIPT_PATH = "run_app.py"             # 与 spec 同目录

a = Analysis(
    [SCRIPT_PATH],
    pathex=[APP_DIR],
    binaries=[],
    datas=[
        ("./LOGO", "LOGO"),
        (os.path.join(CODE_DIR, "Produce"), "Produce"),
        (os.path.join(CODE_DIR, "Check"), "Check"),
        (os.path.join(CODE_DIR, "Title"), "Title"),
        (os.path.join(CODE_DIR, "参数"), "参数"),
        (os.path.join(CODE_DIR, "Setting.md"), "."),
        (os.path.join(CODE_DIR, "Setting.py"), "."),
    ],
    hiddenimports=[
        "tkinter",
        "tkinter.scrolledtext",
        "tkinter.ttk",
        "tkinter.messagebox",
        "openai",
        "requests",
        "markdown",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "matplotlib",
        "numpy",
        "pandas",
        "scipy",
        "PIL",
        "cv2",
        "PyQt5",
        "PyQt6",
        "PySide2",
        "PySide6",
        "dist",
        "build",
    ],
    cipher=None,
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="./LOGO/JIEHAO_LOGO.icns",
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name=APP_NAME,
)
app = BUNDLE(
    coll,
    name=f"{APP_NAME}.app",
    bundle_identifier="com.jiehao.scriptmanager",
    icon="./LOGO/JIEHAO_LOGO.icns",
    info_plist={
        "CFBundleName": APP_NAME,
        "CFBundleDisplayName": APP_NAME,
        "CFBundleIdentifier": "com.jiehao.scriptmanager",
        "CFBundleVersion": "1.0.0",
        "CFBundleShortVersionString": "1.0.0",
        "CFBundlePackageType": "APPL",
        "CFBundleExecutable": APP_NAME,
        "LSMinimumSystemVersion": "11.0",
        "NSHighResolutionCapable": True,
        "NSPrincipalClass": "NSApplication",
    },
)
