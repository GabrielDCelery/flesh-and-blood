FROM python:3.13-alpine as builder

# Install poetry
RUN pip install poetry

# ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
#     POETRY_NO_INTERACTION=1

# Copy project files
WORKDIR /app
COPY pyproject.toml poetry.lock ./
COPY README.md ./
COPY src ./src

# Install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi

# Final stage
FROM python:3.13-alpine

RUN mkdir /downloads

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /app/src /app/src

# Set Python path
#ENV PYTHONPATH=/app/fabimage-scraper

# Run script1
CMD ["python", "-m", "fab_image_scraper"]
