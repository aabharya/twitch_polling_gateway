from fastapi import APIRouter, status

from twitch_polling_api.core import exceptions
from twitch_polling_api.database import DbSession
from twitch_polling_api.users.depends import CurrentUser

from . import services, tasks
from .depends import PollByID
from .models import PollCreatePayload, PollDetail, PollOptionCreatePayload, VoteCreatePayload

poll_router = APIRouter()


@poll_router.post('/', response_model=PollDetail, status_code=status.HTTP_201_CREATED)
def create_new_poll(db_session: DbSession, current_user: CurrentUser, payload: PollCreatePayload):
    if not current_user.is_moderator:
        raise exceptions.PermissionDenied(detail='You are not allowed to create a poll')
    new_poll = services.create_poll(db_session=db_session, title=payload.title, user_id=current_user.id)
    tasks.finish_poll_after_countdown.apply_async(args=[new_poll.id], countdown=new_poll.COUNT_DOWN)
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


@poll_router.post('/{poll_id}/vote/', response_model=PollDetail, status_code=status.HTTP_201_CREATED)
def create_new_vote(db_session: DbSession, current_user: CurrentUser, poll: PollByID, payload: VoteCreatePayload):
    if poll.is_finished:
        raise exceptions.PermissionDenied(detail=f'Poll #{poll.id} has already been finished')
    services.create_vote(db_session=db_session, user_id=current_user.id, poll_id=poll.id, option_id=payload.option_id)
    return poll


@poll_router.get('/{poll_id}/', response_model=PollDetail)
def get_poll_info(db_session: DbSession, poll: PollByID):
    tasks.celery_ping_test.apply_async(args=[poll.id])
    return poll
