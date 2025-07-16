import datetime

from sqlalchemy.orm import Session

from .models import User, UserRole


def get_user_by_email(*, db_session: Session, email: str):
    user = db_session.query(User).filter(User.email == email).one_or_none()
    return user


def get_user_by_username(*, db_session: Session, username: str):
    user = db_session.query(User).filter(User.username == username).one_or_none()
    return user


def create_user(
    *,
    db_session: Session,
    created_at: datetime.datetime,
    updated_at: datetime.datetime,
    username: str,
    email: str,
    public_id: str,
    first_name: str | None,
    last_name: str | None,
) -> User:
    user = User(
        created_at=created_at,
        updated_at=updated_at,
        email=email,
        username=username,
        public_id=public_id,
        first_name=first_name,
        last_name=last_name,
    )
    db_session.add(user)
    db_session.commit()
    return user


def update_user_fields(
    *,
    db_session: Session,
    user: User,
    updated_at: datetime.datetime,
    username: str,
    email: str,
    first_name: str | None,
    last_name: str | None,
) -> User:
    user.updated_at = updated_at
    user.email = email
    user.username = username
    user.first_name = first_name
    user.last_name = last_name
    db_session.add(user)
    db_session.commit()
    return user


def update_user_to_moderator(*, db_session: Session, user: User) -> None:
    user.role = UserRole.MODERATOR
    db_session.add(user)
    db_session.commit()


def update_user_to_viewer(*, db_session: Session, user: User) -> None:
    user.role = UserRole.VIEWER
    db_session.add(user)
    db_session.commit()
