from fastapi import APIRouter

from polling_api.polls.routes import poll_router
from polling_api.users.routes import auth_router, user_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix='/auth', tags=['Authentication'])
api_router.include_router(user_router, prefix='/users', tags=['Users'])
api_router.include_router(poll_router, prefix='/polls', tags=['Polls'])


@api_router.get('/healthcheck/', include_in_schema=False)
def healthcheck():
    return {'status': 'ok'}
