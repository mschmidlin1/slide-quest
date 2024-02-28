import os
import shutil

working_dir = os.getcwd()
modules_dir = os.path.join(working_dir, 'modules').replace("\\", "/")
module_names = os.listdir(modules_dir)
modules = ['modules.' + name.split('.')[0] for name in module_names if name not in ['__pycache__', '__init__.py']]
hidden_imports = '[' + ', '.join(f"'{module}'" for module in modules) + ']'
entry_point_file = os.path.join(working_dir, "SlideQuest.py").replace("\\", "/")
spec_file_content = f"""
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ["{entry_point_file}"],
    pathex=["{modules_dir}"],
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




