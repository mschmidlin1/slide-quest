#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$(dirname "$0")"

# Get the current user's home directory
USER_HOME=$HOME

# Copy everything from the script's directory to the user's home directory
# The -R option ensures directories are copied recursively
cp -R "${SCRIPT_DIR}/"* "${USER_HOME}/"

echo "Files copied from ${SCRIPT_DIR} to ${USER_HOME}"