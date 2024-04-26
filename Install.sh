#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$(dirname "$0")"

# Get the current user's home directory
USER_HOME=$HOME

# Specify the folders and files to copy
ITEMS_TO_COPY=("resources" "SQ_modules" "SlideQuest" "SlideQuest-Intel")

# Loop through each item and copy it to the user's home directory
for item in "${ITEMS_TO_COPY[@]}"
do
    if [ -e "${SCRIPT_DIR}/${item}" ]; then
        cp -R "${SCRIPT_DIR}/${item}" "${USER_HOME}/"
        echo "Copied ${item} to ${USER_HOME}"
    else
        echo "${item} does not exist in ${SCRIPT_DIR} and will not be copied."
    fi
done

echo "Selected items copied to ${USER_HOME}"
