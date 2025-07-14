import enum
from datetime import datetime

from pydantic import Field, model_validator
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from typing_extensions import Self

from polling_api.database import Base, PydanticBase, TimeStampedModel
from polling_api.users.models import UserDetail


class PollStatus(enum.Enum):
    STARTED = 'ST'
    FINISHED = 'FN'
    CANCELED = 'CN'


class Poll(Base, TimeStampedModel):
    __tablename__ = 'polls'
    __table_args__ = (Index('idx_polls_finished_at', 'finished_at'),)

    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False)
    status = Column(Enum(PollStatus), nullable=False, default=PollStatus.STARTED)
    finished_at = Column(DateTime, nullable=True)

    created_by_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_by = relationship('User', foreign_keys='Poll.created_by_id')

    COUNT_DOWN = 300  # Poll last 5 minutes

    def __str__(self):
        return f'{self.title}'

    @property
    def is_finished(self) -> bool:
        return self.status == PollStatus.FINISHED


class PollOption(Base, TimeStampedModel):
    __tablename__ = 'poll_options'

    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False)

    poll_id = Column(Integer, ForeignKey('polls.id', ondelete='CASCADE'), nullable=False)
    poll = relationship('Poll', backref='options', foreign_keys='PollOption.poll_id')

    def __str__(self):
        return f'{self.title} (Poll ID: {self.poll_id})'


class Vote(Base, TimeStampedModel):
    __tablename__ = 'votes'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User', backref='votes', foreign_keys='Vote.user_id')

    poll_id = Column(Integer, ForeignKey('polls.id', ondelete='CASCADE'), nullable=False)
    poll = relationship('Poll', backref='votes', foreign_keys='Vote.poll_id')

    option_id = Column(Integer, ForeignKey('poll_options.id', ondelete='CASCADE'), nullable=False)
    option = relationship('PollOption', backref='votes', foreign_keys='Vote.option_id')

    __table_args__ = (UniqueConstraint('user_id', 'poll_id', name='unique_vote_user_poll'),)

    def __str__(self):
        return f'{self.user_id} -> {self.option_id} (Poll ID: {self.poll_id})'


class PollCreatePayload(PydanticBase):
    title: str


class PollOptionCreatePayload(PydanticBase):
    title: str


class VoteCreatePayload(PydanticBase):
    option_id: int


class VoteDetail(PydanticBase):
    id: int


class PollOptionDetail(PydanticBase):
    id: int
    title: str
    votes: list[VoteDetail] = Field(default_factory=list, exclude=True)
    votes_count: int = 0

    @model_validator(mode='before')
    def count_votes(self) -> Self:
        self.votes_count = len(self.votes or [])
        return self


class PollDetail(PydanticBase):
    id: int
    title: str
    status: str
    created_at: datetime
    updated_at: datetime
    finished_at: datetime | None
    created_by: UserDetail
    options: list[PollOptionDetail] = []
