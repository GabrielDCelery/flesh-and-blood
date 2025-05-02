FROM python:3.12-slim-bullseye as builder

RUN pip install poetry

ENV POETRY_VIRTUALENVS_CREATE=true \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY README.md ./
COPY src ./src

RUN poetry install --only main --no-interaction --no-ansi

# Final stage
#
FROM python:3.12-slim-bullseye as runner

RUN mkdir /downloads

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src

ENV PATH=/app/.venv/bin:$PATH
ENV PYTHONPATH=/app/src:$PATH

ENTRYPOINT [ "/app/.venv/bin/python", "-m" ]
CMD ["fab_scraper"]
