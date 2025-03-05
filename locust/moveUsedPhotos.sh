#!/bin/bash

# Configuration variables
SOURCE_DIR="photos"
DEST_DIR="/usedphotos"
LOG_FILE="locust.log"

# Create destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Process log file and move photos
grep 'Photo: ' "$LOG_FILE" | \
  sed -n 's/.*Photo: \(.*\)/\1/p' | \
  sort -u | \
  while IFS= read -r filename; do
    source_path="$SOURCE_DIR/$filename"
    dest_path="$DEST_DIR/$filename"
    
    if [ -f "$source_path" ]; then
      mv -- "$source_path" "$dest_path"
      echo "Moved: $filename"
    else
      echo "Warning: File not found - $filename" >&2
    fi
  done

echo "Operation completed"
