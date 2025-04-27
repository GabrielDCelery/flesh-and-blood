#!/bin/bash

check_required_env() {
    local var_name="$1"
    if [ -z "${!var_name}" ]; then
        echo "Error: Required environment variable '$var_name' is not set"
        exit 1
    fi
}

path_join() {
    echo "${1%/}/${2#/}"
}

check_required_env "SOURCE_DIR"
check_required_env "TARGET_DIR"

mkdir -p $TARGET_DIR

for source_file in $SOURCE_DIR/*.webp; do
    if [[ $source_file =~ ^(.+)\.width-[0-9]+\.format-webp\.webp$ ]]; then
        source_file_name=$(basename $source_file)
        card_id=$(echo $source_file_name | cut -d'.' -f1)
        target_path="$(path_join "$TARGET_DIR" "$card_id").png"
        echo "converting source $source_file to $target_path"
        dwebp "$source_file" -o "$target_path"
        chmod 777 "$target_path"
    fi
done
