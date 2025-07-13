
FROM python:3.11-slim-bullseye
LABEL maintainer="bindruid"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ADD ./twitch_user_management/uv.lock /home/dependencies/uv.lock
ADD ./twitch_user_management/pyproject.toml /home/dependencies/pyproject.toml
WORKDIR /home/dependencies

ENV UV_COMPILE_BYTECODE=1
ENV PATH="/home/dependencies/.venv/bin:$PATH"


RUN --mount=type=cache,target=/root/.cache \
    uv sync --frozen --no-dev

ADD ./twitch_user_management/src /home/user_management
WORKDIR /home/user_management

COPY ./deploy/docker/user_management_gunicorn/entrypoint.sh /docker-entrypoint.sh

ENTRYPOINT ["sh", "/docker-entrypoint.sh"]
