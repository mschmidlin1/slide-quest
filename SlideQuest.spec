
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ["C:/source/slide-quest/SlideQuest.py"],
    pathex=["C:/source/slide-quest/SQ_modules"],
    binaries=[],
    datas=[],
    hiddenimports=['SQ_modules.configs', 'SQ_modules.DataTypes', 'SQ_modules.Game', 'SQ_modules.GameBoard', 'SQ_modules.GameEnums', 'SQ_modules.LevelBackground', 'SQ_modules.LevelCompleteScreen', 'SQ_modules.LevelEditor', 'SQ_modules.LevelIO', 'SQ_modules.MapConverter', 'SQ_modules.my_logging', 'SQ_modules.queue', 'SQ_modules.ShortestPath', 'SQ_modules.Sprites', 'SQ_modules.TitleScreen', 'SQ_modules.Window'],
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
    name='SlideQuest',
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
)
