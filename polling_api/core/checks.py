import logging

from celery.exceptions import TaskRevokedError, TimeoutError
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from polling_api.core.tasks import dummy_task

logger = logging.getLogger('polling_api:checks')


def health_check_db_celery(db_session: Session):
    try:
        result = dummy_task.apply_async(args=[4, 4]).get(timeout=3)
        if result != 8:
            raise ValueError('Unexpected result')
        db_session.execute(text('SELECT 1'))
    except (OSError, NotImplementedError, TaskRevokedError, TimeoutError, OperationalError, ValueError) as exp:
        logger.error(str(exp))
        return JSONResponse(status_code=500, content={'error': str(exp)})
    return {'status': 'ok'}
