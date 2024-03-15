import os
import shutil

working_dir = os.getcwd()
SQ_modules_dir = os.path.join(working_dir, 'SQ_modules').replace("\\", "/")
module_names = os.listdir(SQ_modules_dir)
SQ_modules = ['SQ_modules.' + name.split('.')[0] for name in module_names if name not in ['__pycache__', '__init__.py']]
hidden_imports = '[' + ', '.join(f"'{module}'" for module in SQ_modules) + ']'
entry_point_file = os.path.join(working_dir, "SlideQuest.py").replace("\\", "/")
spec_file_content = f"""
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ["{entry_point_file}"],
    pathex=["{SQ_modules_dir}"],
    binaries=[],
    datas=[],
    hiddenimports={hidden_imports},
    hookspath=[],
    hooksconfig={{}},
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
"""

with open("SlideQuest.spec", 'w') as file:
    file.write(spec_file_content)




