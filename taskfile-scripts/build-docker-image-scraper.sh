#!/bin/bash
docker build . \
    -f ./docker/Dockerfile.image-scraper \
    -t fab/image-scraper:latest
