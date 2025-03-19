import os

def get_dependencies_recursive(folder_path: str) -> set[str]:
    """
    Recursively gets all the external dependencies from each python code file and returns the set of them.
    """
    module_files = os.listdir(folder_path)

    dependencies = set()

    for file in module_files:
        if "__" in file:#eliminates __pycache__, __init__.py, and others of the sort
            continue
        file_path = os.path.join(folder_path, file)
        if os.path.isdir(file_path):
            dependencies.update(get_dependencies_recursive(file_path))
        else:
            try:
                with open(file_path, 'r') as fhandle:
                    lines = fhandle.readlines()
                for line in lines:
                    if "import" in line and "sq_src" not in line:#find import statements that are importing external libraries
                        line = line.strip()
                        segments = line.split()
                        dependencies.add(segments[1])
            except:
                print(f"No file found {file_path}")
                print(file)
    return dependencies

def get_external_dependencies(folder = "sq_src") -> list[str]:
    """
    Get's a list of the external dependencies from the modules folder.
    """
    parent_dir = os.path.dirname(os.path.dirname(__file__))#get the parent directory of the current file.
    modules_dir = os.path.join(parent_dir, folder)
    
    return list(get_dependencies_recursive(modules_dir))

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
print(hidden_imports)
spec_file_content = f"""
# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['SlideQuest.py'],
    pathex=[],
    binaries=[],
    datas=[('./sq_src/', './sq_src/')],
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
    icon=['resources/images/icy_q_nobackground64x64.ico'],
)

"""


parent_dir = os.path.dirname(os.path.dirname(__file__))#get the parent directory of the current file.
with open(os.path.join(parent_dir, "SlideQuest.spec"), 'w') as file:
    file.write(spec_file_content)

#pyinstaller --noconfirm --onefile --noconsole --noupx --add-data "./SQ_modules/;./SQ_modules/" "SlideQuest.py"


#pyinstaller --noconfirm --onefile --noconsole --noupx --add-data "./SQ_modules/;./SQ_modules/" --hidden-import "pygame" --hidden-import "logging" --hidden-import "numpy" --hidden-import "sys" --hidden-import "time" --hidden-import "os" --hidden-import "collections" --hidden-import "enum" --hidden-import "datetime" --hidden-import "re" --hidden-import "functools" --hidden-import "copy" --hidden-import "random" --hidden-import "logging.config" --hidden-import "pygame.locals" "SlideQuest.py"