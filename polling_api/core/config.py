from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import ConfigDict, PostgresDsn
from pydantic_settings import BaseSettings


class Environment(str, Enum):
    LOCAL = 'LOCAL'
    TEST = 'TEST'
    STAGING = 'STAGING'
    PRODUCTION = 'PRODUCTION'

    @property
    def is_debug(self):
        return self in (self.LOCAL, self.STAGING, self.TEST)

    @property
    def is_testing(self):
        return self == self.TEST

    @property
    def is_deployed(self) -> bool:
        return self in (self.STAGING, self.PRODUCTION)


class Paths:
    ROOT_DIR: Path = Path(__file__).parent.parent.parent
    BASE_DIR: Path = ROOT_DIR / 'polling_api'


class Settings(BaseSettings):
    model_config = ConfigDict(env_file='.env')

    @property
    def PATHS(self) -> Paths:
        return Paths()

    ENVIRONMENT: Environment
    SECRET_KEY: str
    SENTRY_ENABLED: bool = False
    SENTRY_DSN: str
    DEBUG: bool = True
    DB_URL: PostgresDsn
    CORS_ORIGINS: list[str] = ['*']
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str] = ['*']
    PAGINATION_PER_PAGE: int = 20
    REDIS_ULR: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    JWT_SIGNING_KEY: str
    JWT_ALGORITHM: str = 'HS256'
    JWT_LIFETIME: int = 300  # Seconds
    JWT_USER_KEY: str
    GATEWAY_PREFIX: str
    GATEWAY_USER_CREATE_TASK_NAME: str
    GATEWAY_USER_UPDATE_TASK_NAME: str


settings = Settings()

app_configs: dict[str, Any] = {
    'title': 'Twitch Polling API',
    'description': 'Minimal twitch polling api built with FastAPI',
    'debug': settings.DEBUG,
    'openapi_url': '/polling/schema/',
    'swagger_ui_parameters': {'defaultModelsExpandDepth': -1},
}
