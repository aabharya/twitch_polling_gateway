from fastapi import APIRouter, status

from polling_api.core import exceptions
from polling_api.core.events import send_event
from polling_api.database import DbSession
from polling_api.users.depends import CurrentUser

from . import services, tasks
from .depends import PollByID
from .models import PollCreatePayload, PollDetail, PollOptionCreatePayload, VoteCreatePayload

poll_router = APIRouter()


@poll_router.post('/', response_model=PollDetail, status_code=status.HTTP_201_CREATED)
async def create_new_poll(db_session: DbSession, current_user: CurrentUser, payload: PollCreatePayload):
    if not current_user.is_moderator:
        raise exceptions.PermissionDenied(detail='You are not allowed to create a poll')
    new_poll = services.create_poll(db_session=db_session, title=payload.title, user_id=current_user.id)
    await send_event(event_type='new_polling', message=f'created new poll #{new_poll.id}')
    return new_poll


@poll_router.post('/{poll_id}/options/', response_model=PollDetail, status_code=status.HTTP_201_CREATED)
def create_new_poll_option(
    db_session: DbSession, current_user: CurrentUser, poll: PollByID, payload: PollOptionCreatePayload
):
    if not current_user.is_moderator:
        raise exceptions.PermissionDenied(detail='You are not allowed to create a poll')
    if poll.is_finished:
        raise exceptions.PermissionDenied(detail=f'Poll #{poll.id} has already been finished')
    services.create_poll_option(db_session=db_session, title=payload.title, poll_id=poll.id)
    return poll


@poll_router.post('/{poll_id}/start/', response_model=PollDetail, status_code=status.HTTP_200_OK)
def start_poll(db_session: DbSession, current_user: CurrentUser, poll: PollByID):
    if not current_user.is_moderator:
        raise exceptions.PermissionDenied(detail='You are not allowed to create a poll')
    if poll.is_started:
        raise exceptions.PermissionDenied(detail=f'Poll #{poll.id} has already been started')
    poll = services.start_poll(db_session=db_session, poll=poll)
    tasks.finish_poll_after_countdown.apply_async(args=[poll.id], countdown=poll.COUNT_DOWN)
    return poll


@poll_router.post('/{poll_id}/vote/', response_model=PollDetail, status_code=status.HTTP_201_CREATED)
def create_new_vote(db_session: DbSession, current_user: CurrentUser, poll: PollByID, payload: VoteCreatePayload):
    if poll.is_finished:
        raise exceptions.PermissionDenied(detail=f'Poll #{poll.id} has already been finished')
    services.create_vote(db_session=db_session, user_id=current_user.id, poll_id=poll.id, option_id=payload.option_id)
    return poll


@poll_router.get('/{poll_id}/', response_model=PollDetail)
def get_poll_info(db_session: DbSession, poll: PollByID):
    return poll
