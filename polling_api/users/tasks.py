import logging

from polling_api.core.celery import app
from polling_api.database.depends import get_db_session
from polling_api.users import services

logger = logging.getLogger('tasks')


@app.task(name='create_user_from_gateway')
def create_user_from_gateway(username: str, email: str, first_name: str, last_name: str, public_id):
    db_session = get_db_session()
    services.create_user(
        db_session=db_session,
        username=username,
        email=email,
        public_id=public_id,
        first_name=first_name,
        last_name=last_name,
    )
    db_session.close()
