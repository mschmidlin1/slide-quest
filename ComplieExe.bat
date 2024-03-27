@echo on
REM Activate the virtual environment
call .\.venv\Scripts\activate.bat

REM Run the Python script
python "install_spec/create_spec.py"

REM Run PyInstaller to create the executable
pyinstaller --distpath="./" "SlideQuest.spec"

REM Deactivate the virtual environment and exit
call deactivate

REM Delete the "build" folder and all of its contents
rmdir /s /q build

REM Delete the .spec file
del SlideQuest.spec

REM Wait for user input before closing the terminal
pause