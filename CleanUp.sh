#!/bin/bash

# Get the current user's home directory
USER_HOME=$HOME

# Specify the folders and files to remove
ITEMS_TO_REMOVE=("levels" "mapgen_resources" "resources" "SQ_modules" "SlideQuest" "SlideQuest-Intel")

# Loop through each item and remove it from the user's home directory
for item in "${ITEMS_TO_REMOVE[@]}"
do
    if [ -e "${USER_HOME}/${item}" ]; then
        rm -rf "${USER_HOME}/${item}"
        echo "Removed ${item} from ${USER_HOME}"
    else
        echo "${item} does not exist in ${USER_HOME} and cannot be removed."
    fi
done

echo "Cleanup completed."
