# -*- mode: python ; coding: utf-8 -*-

import os

APP_NAME = "杰昊脚本管理器"
SCRIPT_PATH = os.path.join(os.getcwd(), "run_app.py")

a = Analysis(
    [SCRIPT_PATH],
    pathex=[os.getcwd()],
    binaries=[],
    datas=[
        ("./LOGO", "LOGO"),
        ("../Produce", "Produce"),
        ("../Check", "Check"),
        ("../Title", "Title"),
        ("../参数", "参数"),
        ("../Setting.md", "."),
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
