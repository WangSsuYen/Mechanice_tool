# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('mechanics_tools.db', '.'),  # 包含資料庫
        ('images/*.jpg', 'images'),     # 包含所有 JPG 圖片
        ('images/*.png', 'images'),     # 包含所有 PNG 圖片
        ('images/*.gif', 'images'),     # 包含所有 GIF 圖片
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
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
    name='mechanics',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # 如果不需要顯示命令行窗口，請設為 False
    icon='mechanics_tools.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='mechanics_tool',
    strip=False,
    upx=True,
    upx_exclude=[],
)