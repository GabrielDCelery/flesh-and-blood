FROM golang:1.24.2-bullseye AS builder

WORKDIR /app

COPY go.mod go.sum ./

RUN go mod download

COPY cmd/ ./cmd/
COPY internal/ ./internal/

RUN CGO_ENABLED=1 GOOS=linux go build -o /app/bin/main ./cmd/api/main.go

FROM debian:bullseye-20250428-slim AS runner

RUN apt update && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app/bin/main .

CMD ["/app/main"]
