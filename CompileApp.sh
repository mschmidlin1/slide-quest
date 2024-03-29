#!/bin/bash
# Activate the virtual environment
source ./.venv/bin/activate

# Run the Python script
python "install_spec/create_spec.py"

# Run PyInstaller to create the executable
pyinstaller --distpath="./" "SlideQuest.spec"

# Deactivate the virtual environment
deactivate

# Delete the "build" folder and all of its contents
rm -rf build
rm -rf dist

# Delete the .spec file
rm SlideQuest.spec

# Wait for user input before closing the terminal
echo "Press enter to continue"
read