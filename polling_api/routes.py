from fastapi import APIRouter

from polling_api.core.config import settings
from polling_api.polls.routes import poll_router
from polling_api.users.routes import user_router

api_router = APIRouter(prefix=f'/{settings.GATEWAY_PREFIX}api/v1')

api_router.include_router(user_router, prefix='/users', tags=['Polling Users'])
api_router.include_router(poll_router, prefix='/polls', tags=['Polls'])
