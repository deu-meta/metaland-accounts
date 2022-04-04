from pydantic import Field
from pydantic.main import BaseModel


class MessageOk(BaseModel):
    message: str = Field(default="OK")


class UserToken(BaseModel):
    displayName: str = None
    givenName: str = None
    jobTitle: str = None
    mail: str = None
    provider: str = None
    role: str = None


class MinecraftToken(BaseModel):
    id: str = None
    provider: str = None
    displayName: str = None
