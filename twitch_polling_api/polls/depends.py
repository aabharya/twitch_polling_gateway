from typing import Annotated

from fastapi import Depends

from twitch_polling_api.core import exceptions
from twitch_polling_api.database import DbSession

from .models import Poll


def get_poll_by_id(poll_id: int, db_session: DbSession) -> Poll:
    poll = db_session.query(Poll).filter(Poll.id == poll_id).one_or_none()
    if poll is None:
        raise exceptions.NotFound(detail=f'Poll {poll_id} not found')
    return poll


PollByID = Annotated[Poll, Depends(get_poll_by_id)]
