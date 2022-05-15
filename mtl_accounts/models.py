from pydantic import Field
from pydantic.main import BaseModel


class MessageOk(BaseModel):
    message: str = Field(default="OK")


class OpenID(BaseModel):
    display_name: str = None
    given_name: str = None
    job_title: str = None
    email: str = None
    provider: str = None


class User(OpenID):
    provider: str = None
    role: str = None


class Minecraft(BaseModel):
    id: str = None
    provider: str = None
    displayName: str = None
