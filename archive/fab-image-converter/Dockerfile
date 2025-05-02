FROM ubuntu:25.04

RUN apt update && \
    apt install -y webp && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./src/convert-fab-original-webp-to-png.sh ./run.sh

RUN chmod +x /app/run.sh

CMD ["/app/run.sh"]
