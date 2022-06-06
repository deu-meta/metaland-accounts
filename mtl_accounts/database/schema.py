import uuid
from datetime import datetime
from math import ceil
from typing import Generic, List, Sequence, TypeVar

from fastapi_pagination import Params
from fastapi_pagination.bases import AbstractPage, AbstractParams
from mtl_accounts.database.conn import Base
from mtl_accounts.models import Role
from sqlalchemy import TIMESTAMP, VARCHAR, Column, ForeignKey


class Users(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "metaland_accounts"}
    id = Column(VARCHAR(36), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(VARCHAR(50), primary_key=True, index=True)
    role = Column(VARCHAR(50), default=Role.default.value)
    phone_number = Column(VARCHAR(50), nullable=True)
    provider = Column(VARCHAR(50), nullable=True)
    display_name = Column(VARCHAR(50), nullable=True)
    given_name = Column(VARCHAR(50), nullable=True)
    job_title = Column(VARCHAR(50), nullable=True)
    date_joined = Column(TIMESTAMP(), default=datetime.now)
    last_login = Column(TIMESTAMP(), default=datetime.now)


class Minecraft_Account(Base):
    __tablename__ = "minecraft_account"
    __table_args__ = {"schema": "metaland_accounts"}
    id = Column(VARCHAR(50), primary_key=True, index=True)
    user_id = Column(VARCHAR(50), ForeignKey("metaland_accounts.users.id"))
    provider = Column(VARCHAR(50), nullable=True)
    display_name = Column(VARCHAR(50), nullable=True)


T = TypeVar("T")


class Page(AbstractPage[T], Generic[T]):
    count: int
    results: List[T]
    total_pages: int

    __params_type__ = Params

    @classmethod
    def create(cls, results: Sequence[T], count: int, params: AbstractParams):
        if not isinstance(params, cls.__params_type__):
            raise TypeError(f"Params must be {cls.__params_type__}")

        return cls(
            count=count,
            total_pages=ceil(count / params.size) if count > 0 else 1,
            results=results,
        )
