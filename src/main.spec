# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('gui\\assets\\*', 'gui\\assets\\'), ('resources_rc.py', '.')],
    hiddenimports=[
        'psutil', 
        'pkgutil', 
        'PyQt6.sip', 
        'PyQt6.QtCore', 
        'PyQt6.QtWidgets', 
        'qtawesome', 
        'qdarktheme', 
        'graphviz', 
        'pygetwindow', 
        'pyautogui', 
        'pymem', 
        'markdown', 
        'RPA', 
        'RPA.Windows', 
        'integrations.tools.bintext', 
        'integrations.tools.die', 
        'integrations.tools.peid', 
        'integrations.tools.scylla', 
        'integrations.tools.upx'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['gui\\assets\\app_icon.ico'],
)
