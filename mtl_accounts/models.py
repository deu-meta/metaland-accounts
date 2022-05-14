from pydantic import Field
from pydantic.main import BaseModel


class MessageOk(BaseModel):
    message: str = Field(default="OK")


class User(BaseModel):
    display_name: str = None
    given_name: str = None
    job_title: str = None
    email: str = None


class UserToken(User):
    provider: str = None
    role: str = None


class MinecraftToken(BaseModel):
    id: str = None
    provider: str = None
    displayName: str = None
