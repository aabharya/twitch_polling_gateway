from typing import Annotated

from fastapi import Depends, Request

from polling_api.core import exceptions
from polling_api.database import DbSession

from .models import User


def get_current_user(db_session: DbSession, request: Request) -> User:
    if request.state.user.is_anonymous:
        raise exceptions.NotAuthenticated
    user = db_session.query(User).filter(User.public_id == request.state.user.public_id).one_or_none()
    if user is None:
        raise exceptions.NotAuthenticated
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_user_by_name(username: str, db_session: DbSession) -> User:
    user = db_session.query(User).filter(User.username == username).one_or_none()
    if user is None:
        raise exceptions.NotFound(detail=f'User {username} not found')
    return user


UserByName = Annotated[User, Depends(get_user_by_name)]


def get_user_by_id(user_id: int, db_session: DbSession) -> User:
    user = db_session.query(User).filter(User.id == user_id).one_or_none()
    if user is None:
        raise exceptions.NotFound(detail=f'User {user_id} not found')
    return user


UserByID = Annotated[User, Depends(get_user_by_id)]
