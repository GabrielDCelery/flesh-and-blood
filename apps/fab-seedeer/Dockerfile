FROM golang:1.24.2-bullseye AS builder

WORKDIR /app

COPY go.mod go.sum ./

RUN go mod download

COPY src/ ./src/
COPY migrations/ ./migrations/

RUN CGO_ENABLED=1 GOOS=linux go build -o /app/bin/main ./src/main.go

FROM debian:bullseye-20250428-slim AS runner

RUN apt update && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app/bin/main .
COPY --from=builder /app/migrations ./migrations

RUN mkdir -p /mnt/fab-cards-text-extracts-db

CMD ["/app/main"]
