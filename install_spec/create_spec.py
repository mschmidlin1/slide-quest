import os



def get_external_dependencies(folder = "SQ_modules") -> list[str]:
    """
    Get's a list of the external dependencies from the modules folder.
    """
    parent_dir = os.path.dirname(os.path.dirname(__file__))#get the parent directory of the current file.
    modules_dir = os.path.join(parent_dir, folder)
    module_files = os.listdir(modules_dir)

    dependencies = set()

    for file in module_files:
        if "__" in file:#eliminates __pycache__, __init__.py, and others of the sort
            continue
        file_path = os.path.join(modules_dir, file)
        try:
            with open(file_path, 'r') as fhandle:
                lines = fhandle.readlines()
            for line in lines:
                if "import" in line and "SQ_module" not in line:#find import statements that are importing external libraries
                    line = line.strip()
                    segments = line.split()
                    dependencies.add(segments[1])
        except:
            print(f"No file found {file_path}")
            print(file)

    return list(dependencies)

def list_to_str(l: list[str]) -> str:
    """
    Turns a list of strings into a string representation of the list.

    Example:
    --------
    ```
    l = ['a', 'b', 'c']
    l_str = list_to_str(l)

    print(l_str)
    "['a', 'b', 'c']"
    ```
    """
    return '[' + ', '.join(f"'{e}'" for e in l) + ']'

hidden_imports = list_to_str(get_external_dependencies())

spec_file_content = f"""
# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['SlideQuest.py'],
    pathex=[],
    binaries=[],
    datas=[('./SQ_modules/', './SQ_modules/')],
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
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['resources\\\images\\\icy_q_nobackground64x64.ico'],
)

"""


parent_dir = os.path.dirname(os.path.dirname(__file__))#get the parent directory of the current file.
with open(os.path.join(parent_dir, "SlideQuest.spec"), 'w') as file:
    file.write(spec_file_content)

#pyinstaller --noconfirm --onefile --noconsole --noupx --add-data "./SQ_modules/;./SQ_modules/" "SlideQuest.py"


#pyinstaller --noconfirm --onefile --noconsole --noupx --add-data "./SQ_modules/;./SQ_modules/" --hidden-import "pygame" --hidden-import "logging" --hidden-import "numpy" --hidden-import "sys" --hidden-import "time" --hidden-import "os" --hidden-import "collections" --hidden-import "enum" --hidden-import "datetime" --hidden-import "re" --hidden-import "functools" --hidden-import "copy" --hidden-import "random" --hidden-import "logging.config" --hidden-import "pygame.locals" "SlideQuest.py"