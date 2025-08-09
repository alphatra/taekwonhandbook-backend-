# syntax=docker/dockerfile:1
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl && rm -rf /var/lib/apt/lists/*

# Dependencies
# Rye lock includes "-e file:." which requires the project metadata to be present
# in the working directory. Copy minimal project files before installing.
COPY requirements.lock /app/requirements.lock
COPY pyproject.toml /app/pyproject.toml
COPY src /app/src
RUN pip install --upgrade pip && pip install -r /app/requirements.lock

# App code
COPY backend /app/backend

WORKDIR /app/backend
ENV DJANGO_SETTINGS_MODULE=core.settings

# Non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Collect static at build (optional; requires env)
ARG DJANGO_SECRET_KEY=build-secret
ARG DJANGO_DEBUG=0
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

CMD ["/app/backend/entrypoint.sh"]

