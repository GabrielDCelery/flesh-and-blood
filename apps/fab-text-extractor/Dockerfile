FROM python:3.12-slim-bullseye AS builder

RUN pip install poetry

ENV POETRY_VIRTUALENVS_CREATE=true \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY README.md ./

RUN poetry install --only main --no-interaction --no-ansi --no-root

COPY src ./src

# Final stage
#
FROM python:3.12-slim-bullseye AS runner

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src

ENV PATH=/app/.venv/bin:$PATH
ENV PYTHONPATH=/app/src:$PATH

ENTRYPOINT [ "/app/.venv/bin/python", "-m" ]
CMD ["fab_extract"]
