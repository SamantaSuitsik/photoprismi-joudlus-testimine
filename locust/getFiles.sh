#!/bin/bash
files=()
while IFS= read -r file; do
  files+=("\"$(basename "$file")\"")
done < <(find photos -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \))
echo "["$(IFS=,; echo "${files[*]}")"]" > fileList.json
