import logging
from datetime import datetime

from polling_api.core.celery import app
from polling_api.database.depends import get_db_session
from polling_api.polls.models import Poll, PollStatus

logger = logging.getLogger('tasks')


@app.task(name='finish_poll_after_countdown')
def finish_poll_after_countdown(poll_id: int):
    db_session = get_db_session()
    poll = db_session.query(Poll).filter_by(id=poll_id).one_or_none()
    if not poll:
        logger.error(f'"Finish Poll Task": Poll #{poll_id} not found')
    poll.status = PollStatus.FINISHED
    poll.finished_at = datetime.utcnow()
    db_session.add(poll)
    db_session.commit()
    db_session.close()
    logger.error(f'"Finish Poll Task": Poll #{poll_id} status was set to finished')
