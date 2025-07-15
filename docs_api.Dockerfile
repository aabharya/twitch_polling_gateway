# Base builder
FROM python:3.11-slim-bullseye AS builder

LABEL maintainer="bindruid"

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Build stage envs
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    PATH="/home/dependencies/.venv/bin:$PATH"

WORKDIR /home/dependencies

# Install dependencies with uv
ADD ./docs_api/uv.lock ./docs_api/pyproject.toml ./
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
ADD ./docs_api/ /home/docs_api
RUN mkdir /home/logs/

WORKDIR /home/

# Entrypoint
COPY deploy/docker/docs_api.sh /docker-entrypoint.sh

ENTRYPOINT ["sh", "/docker-entrypoint.sh"]

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/ht/ || exit 1
