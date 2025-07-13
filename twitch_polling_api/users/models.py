import enum
from typing import Optional

from pydantic.networks import EmailStr
from sqlalchemy import Boolean, Column, Enum, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from twitch_polling_api.core.pagination import Pagination
from twitch_polling_api.database import Base, PydanticBase, TimeStampedModel


class UserRole(enum.Enum):
    MODERATOR = 'MOD'
    VIEWER = 'VIEW'


class User(Base, TimeStampedModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True, index=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.VIEWER)
    first_name = Column(String(256), nullable=True)
    last_name = Column(String(256), nullable=True)
    email = Column(String(256), nullable=False, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    public_id = Column(UUID(as_uuid=True), unique=True, nullable=False, index=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_moderator(self) -> bool:
        return self.role == UserRole.MODERATOR

    @property
    def is_viewers(self) -> bool:
        return self.role == UserRole.VIEWER


class UserDetail(PydanticBase):
    id: int
    username: str
    email: EmailStr
    role: UserRole
    first_name: Optional[str] = ''
    last_name: Optional[str] = ''


class UserList(Pagination):
    items: list[UserDetail] = []
