
FROM python:3.11-slim-bullseye
LABEL maintainer="bindruid"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ADD ./users_api/uv.lock /home/dependencies/uv.lock
ADD ./users_api/pyproject.toml /home/dependencies/pyproject.toml
WORKDIR /home/dependencies

ENV UV_COMPILE_BYTECODE=1
ENV PATH="/home/dependencies/.venv/bin:$PATH"


RUN --mount=type=cache,target=/root/.cache \
    uv sync --frozen --no-dev

ADD ./users_api/src /home/users_api
WORKDIR /home/users_api

COPY deploy/docker/users_api.sh /docker-entrypoint.sh

ENTRYPOINT ["sh", "/docker-entrypoint.sh"]
