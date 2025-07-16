# Twitch Polling Gateway

A minimal polling and user management API stack with FastAPI, Django, PostgreSQL, Redis, Celery, and NGINX as a gateway.

## Prerequisites

- `Python 3.11`

## Architecture

| Service         | Description                               |
| --------------- |-------------------------------------------|
| `polling_db`    | PostgreSQL database for polling API       |
| `users_db`      | PostgreSQL database for user management   |
| `redis`         | Redis in-memory store for Celery broker   |
| `users_api`     | Djano app for user management api         |
| `polling_api`   | FastAPI app for polling api               |
| `docs_api`      | FastAPI app gateway serving documentation |
| `celery-worker` | Celery worker for async task processing   |
| `gateway`       | NGINX reverse proxy gateway for APIs      |

## Development

### `.env` files

In `deploy/docker/envs` all env variables are defined and categorized around their service names.

### Run Gateway

```shell
make dev
```

Check API documentation at `localhost:8000/docs`
