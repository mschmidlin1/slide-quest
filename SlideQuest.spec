
# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['SlideQuest.py'],
    pathex=[],
    binaries=[],
    datas=[('./sq_src/', './sq_src/')],
    hiddenimports=['time', 'sq_src.screens.splash_screen', 'sq_src.singletons.my_logging', 'sq_src.singletons.level_manager', 'sq_src.singletons.user_data', 'sq_src.screens.welcome_screen', 'sq_src.screens.level_complete_screen', 'sq_src.data_structures.data_types', 'sys', 'sq_src.core.game', 'sq_src.singletons.game_audio', 'pygame', 'sq_src.singletons.navigation_manager', 'sq_src.level_generation.level_io', 'os', 'sq_src.screens.options_screen', 'sq_src.data_structures.game_enums', 'sq_src.configs', 'sq_src.screens.title_screen'],
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
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['resources/images/icy_q_nobackground64x64.ico'],
)

