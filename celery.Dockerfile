
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


RUN --mount=type=cache,target=/root/.cache \
    uv sync --frozen --no-dev

ADD twitch_polling_api /home/twitch_polling_api
RUN mkdir /home/logs/
WORKDIR /home/

COPY deploy/docker/twitch_api_celery_worker/entrypoint.sh /docker-entrypoint.sh

ENTRYPOINT ["sh", "/docker-entrypoint.sh"]
