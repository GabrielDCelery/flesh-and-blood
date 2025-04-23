#!/bin/bash

docker run --rm \
-e PAGE_URL="$PAGE_URL" \
-e LOG_LEVEL="$LOG_LEVEL" \
-e DOWNLOAD_DIR="/downloads" \
-e DOWNLOAD_CONCURRENCY="$DOWNLOAD_CONCURRENCY" \
-v "$DOCKER_VOLUME_NAME":/downloads \
fab/image-scraper:latest

