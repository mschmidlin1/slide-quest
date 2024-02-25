
from PyInstaller.utils.hooks import collect_submodules
import os

working_dir = os.getcwd()

modules_dir = os.path.join('', 'modules')
#hidden_imports = collect_submodules(os.path.join(working_dir, 'modules'))
module_names = os.listdir(modules_dir)
modules = ['modules'+'.'+name.split('.')[0] for name in module_names if name not in ['__pycache__']]





spec_file = f"""
# -*- mode: python ; coding: utf-8 -*-




a = Analysis(
    ['SlideQuest.py'],
    pathex=["{modules_dir}"],
    binaries=[],
    datas=[],
    hiddenimports=[{','.join(modules)}],
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

with open("SlideQuest.spec", 'w') as handle:
    handle.write(spec_file)