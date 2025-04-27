#!/bin/bash

for file in ./fab-cards/*.webp; do
    # Check if the file matches the pattern
    if [[ $file =~ ^(.+)\.width-[0-9]+\.format-webp\.webp$ ]]; then
        # BASH_REMATCH[1] contains the base name (e.g., "WTR_87")
        base_name="${BASH_REMATCH[1]}"
        # Convert to PNG
        dwebp "$file" -o "${base_name}.png"
        echo "Converted $file to ${base_name}.png"
    fi
done
