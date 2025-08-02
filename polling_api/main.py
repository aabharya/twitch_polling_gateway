from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentry_asgi import SentryMiddleware

from polling_api.core import checks
from polling_api.core.config import app_configs, settings
from polling_api.core.events import event_router
from polling_api.core.lifespan import lifespan
from polling_api.core.middleware import AuthenticationMiddleware, ExceptionMiddleware, LoggingMiddleware
from polling_api.database import DbSession
from polling_api.routes import api_router


def get_application() -> FastAPI:
    app = FastAPI(**app_configs, lifespan=lifespan)
    app.include_router(api_router)
    app.include_router(event_router, tags=['Events'])
    return app


api = get_application()

api.add_middleware(SentryMiddleware)
api.add_middleware(LoggingMiddleware)
api.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=('GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'),
    allow_headers=settings.CORS_HEADERS,
)
api.add_middleware(AuthenticationMiddleware)
api.add_middleware(ExceptionMiddleware)


@api.get('/ht/', include_in_schema=False)
def healthcheck_api(db_session: DbSession):
    return checks.health_check_db_celery(db_session)
