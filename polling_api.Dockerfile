
FROM python:3.11-slim-bullseye
LABEL maintainer="bindruid"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ADD uv.lock /home/dependencies/uv.lock
ADD pyproject.toml /home/dependencies/pyproject.toml
WORKDIR /home/dependencies

ENV UV_COMPILE_BYTECODE=1
ENV PATH="/home/dependencies/.venv/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache \
    uv sync --frozen --no-dev

ADD polling_api /home/polling_api
RUN mkdir /home/logs/
WORKDIR /home/

COPY deploy/docker/polling_api.sh /docker-entrypoint.sh

ENTRYPOINT ["sh", "/docker-entrypoint.sh"]

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/ht/ || exit 1

