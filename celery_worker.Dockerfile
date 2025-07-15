# Base builder
FROM python:3.11-slim-bullseye AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Build stage envs
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    PATH="/home/dependencies/.venv/bin:$PATH"

WORKDIR /home/dependencies

ADD uv.lock pyproject.toml ./

# Install dependencies with uv
RUN --mount=type=cache,target=/root/.cache \
    uv sync --frozen --no-dev

# Final image
FROM python:3.11-slim-bullseye

LABEL maintainer="bindruid"

# envs
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/home/dependencies/.venv/bin:$PATH"

# Install runtime curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtualenv from builder
COPY --from=builder /home/dependencies/.venv /home/dependencies/.venv

# Copy app code
ADD polling_api /home/polling_api
RUN mkdir /home/logs/

WORKDIR /home/

# Entrypoint
COPY deploy/docker/celery_worker.sh /docker-entrypoint.sh

ENTRYPOINT ["sh", "/docker-entrypoint.sh"]
