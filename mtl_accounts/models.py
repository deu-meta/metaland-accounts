from enum import Enum

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


class User(OpenID):
    role: str = Role.default.value

    class Config:
        orm_mode = True


class Minecraft(BaseModel):
    id: str = None
    provider: str = None
    display_name: str = None
