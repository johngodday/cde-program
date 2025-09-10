#!/usr/bin/env bash
################################################
##### MOVE FILES SCRIPT
################################################

if [ -f .env ]; then
    source .env
else
    echo "ERROR: .env file not found!"
    exit 1
fi

# Create target directory if it doesn't exist
SOURCE_DIR="$FILE_DIR"
TARGET_DIR="$JSON_CSV_DIR"


###############################################################
##### MOVE FILES
###############################################################

shopt -s nullglob  # prevents literal "*.csv" if no matches
files=("$SOURCE_DIR"/*.csv "$SOURCE_DIR"/*.json)

if [ ${#files[@]} -eq 0 ]; then
    echo "No CSV or JSON files found in $SOURCE_DIR"
    exit 0
fi

# Move the files
for file in "${files[@]}"; do
    echo "Moving $(basename "$file") to $TARGET_DIR"
    mv "$file" "$TARGET_DIR/"
done

echo "All CSV and JSON files have been moved to $TARGET_DIR"



###################################################################
##### END OF SCRIPT
###################################################################