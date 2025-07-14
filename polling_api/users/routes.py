from fastapi import APIRouter, status

from polling_api.core import exceptions
from polling_api.database import DbSession

from . import services
from .depends import CurrentUser, UserByID
from .models import UserDetail

auth_router = APIRouter()
user_router = APIRouter()


@user_router.get('/profile/{user_id}/', response_model=UserDetail)
def get_user_profile(db_session: DbSession, user: UserByID):
    return user


@user_router.patch('/{user_id}/mod/', status_code=status.HTTP_200_OK)
def update_user_role_to_moderator(current_user: CurrentUser, db_session: DbSession, user: UserByID):
    if current_user.id != user.id:
        raise exceptions.PermissionDenied
    services.update_user_to_moderator(db_session=db_session, user=user)
    return {'message': f'Updated user {user.username} role to be moderator'}


@user_router.patch('/{user_id}/unmod/', status_code=status.HTTP_200_OK)
def update_user_role_to_viewer(current_user: CurrentUser, db_session: DbSession, user: UserByID):
    if current_user.id != user.id:
        raise exceptions.PermissionDenied
    services.update_user_to_viewer(db_session=db_session, user=user)
    return {'message': f'Updated user {user.username} role to be viewer'}
