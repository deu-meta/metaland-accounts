from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import Field
from pydantic.main import BaseModel


class MessageOk(BaseModel):
    message: str = Field(default="OK")


class Role(str, Enum):
    admin = "admin"
    student = "student"
    staff = "staff"
    default = "default"


class OpenID(BaseModel):
    display_name: str = None
    given_name: str = None
    job_title: str = None
    email: str = None
    provider: str = None


class UserIn(BaseModel):
    id: str
    role: Optional[str]
    phone_number: Optional[str]


class User(OpenID):
    id: str = None
    role: str = Role.default.value
    date_joined: datetime = None
    last_login: datetime = None

    class Config:
        orm_mode = True


class Minecraft(BaseModel):
    id: str = None
    provider: str = None
    display_name: str = None
