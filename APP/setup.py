#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyInstaller 打包配置 - 杰昊脚本管理器
"""

from PyInstaller.building.build_main import (
    Analysis, PYZ, EXE, COLLECT, BUNDLE
)
from PyInstaller.utils.win32 import versioninfo
import os
import sys

block_cipher = None

APP_NAME = "杰昊脚本管理器"
SCRIPT_PATH = os.path.join(os.getcwd(), "run_app.py")
DIST_PATH = os.path.join(os.getcwd(), "dist")
BUILD_PATH = os.path.join(os.getcwd(), "build")

a = Analysis(
    [SCRIPT_PATH],
    pathex=[os.getcwd()],
    binaries=[],
    datas=[],
    hiddenimports=[
        "tkinter",
        "tkinter.scrolledtext",
        "tkinter.ttk",
        "tkinter.messagebox",
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
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

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
    icon=None,
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
