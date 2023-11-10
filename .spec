# -*- mode: python ; coding: utf-8 -*-

pf_foldr='C:\\Users\\Белеко Никита\\PycharmProjects\\LogicGames\\platforms\\'

a = Analysis(
    ['MainWindow.py'],
    pathex=[],
    binaries=[(pf_foldr+'qwindows.dll', 'platforms\\qwindows.dll')
             ],
    datas=[],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=['qwindows.dll'],
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='',
)
