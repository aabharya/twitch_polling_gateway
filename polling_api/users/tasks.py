import logging
from datetime import timezone

from dateutil.parser import parse

from polling_api.core.celery import app
from polling_api.core.config import settings
from polling_api.database.depends import get_db_session
from polling_api.users import services
from polling_api.users.models import User

logger = logging.getLogger('tasks')


def parse_datetime_utc(dt_str: str):
    dt = parse(dt_str)
    return dt.replace(tzinfo=timezone.utc)


def ensure_utc(dt):
    return dt.replace(tzinfo=timezone.utc)


@app.task(name=settings.GATEWAY_USER_CREATE_TASK_NAME, queue=settings.CELERY_QUEUE_NAME)
def create_user_from_gateway(
    created_at: str,
    updated_at: str,
    username: str,
    email: str,
    first_name: str,
    last_name: str,
    public_id,
):
    logger.info(f'Creating user from gateway with public id #{public_id}')
    db_session = get_db_session()
    created_at_dt = parse_datetime_utc(created_at)
    updated_at_dt = parse_datetime_utc(updated_at)
    services.create_user(
        db_session=db_session,
        created_at=created_at_dt,
        updated_at=updated_at_dt,
        username=username,
        email=email,
        public_id=public_id,
        first_name=first_name,
        last_name=last_name,
    )
    db_session.close()


@app.task(name=settings.GATEWAY_USER_UPDATE_TASK_NAME, queue=settings.CELERY_QUEUE_NAME)
def update_user_from_gateway(
    created_at: str,
    updated_at: str,
    username: str,
    email: str,
    first_name: str,
    last_name: str,
    public_id,
):
    logger.info(f'Updating user from gateway with public id #{public_id}')
    db_session = get_db_session()
    updated_at_dt = parse_datetime_utc(updated_at)
    user = db_session.query(User).filter(User.public_id == public_id).one_or_none()
    if user is None or ensure_utc(user.updated_at) > updated_at_dt:
        logger.info(f'Skipped updating user from gateway with public id #{public_id} because current snapshot if newer')
        return
    services.update_user_fields(
        db_session=db_session,
        user=user,
        updated_at=updated_at_dt,
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    db_session.close()
