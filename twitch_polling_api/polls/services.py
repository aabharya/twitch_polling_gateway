from sqlalchemy.orm import Session

from .models import Poll, PollOption, PollStatus, Vote


def create_poll(*, db_session: Session, title: str, user_id: int):
    poll = Poll(title=title, created_by_id=user_id, status=PollStatus.STARTED)
    db_session.add(poll)
    db_session.commit()
    return poll


def create_poll_option(*, db_session: Session, title: str, poll_id: int):
    poll_option = PollOption(title=title, poll_id=poll_id)
    db_session.add(poll_option)
    db_session.commit()
    return poll_option


def create_vote(*, db_session: Session, user_id: int, poll_id: int, option_id: int):
    vote = Vote(user_id=user_id, poll_id=poll_id, option_id=option_id)
    db_session.add(vote)
    db_session.commit()
    return vote
