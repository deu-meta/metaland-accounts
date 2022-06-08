from datetime import datetime
from typing import Dict, Optional

import mtl_accounts.errors.exceptions as ex
from fastapi_pagination.ext.sqlalchemy import paginate
from mtl_accounts.database.schema import Minecraft_Account, Users
from mtl_accounts.models import (
    MinecraftAccountIn,
    MinecraftAccountOut,
    OpenID,
    User,
    UserIn,
)
from sqlalchemy import and_
from sqlalchemy.orm import Session


def create_mincraft(session: Session, minecraft: MinecraftAccountIn, user_id: str):
    minecraft_account = Minecraft_Account(id=minecraft.id, user_id=user_id, provider=minecraft.provider, display_name=minecraft.display_name)
    session.add(minecraft_account)
    session.commit()


def get_minecraft_account(session: Session, id: str) -> Optional[MinecraftAccountOut]:
    return session.query(Minecraft_Account).get(id)


def exists_mincraft(session: Session, id: str) -> bool:
    result = session.query(Minecraft_Account).filter(Minecraft_Account.id == id).first()
    if result:
        return True
    return False


def create_or_update_user(session: Session, openid: OpenID, defaults: Dict = {}) -> User:
    updates = session.query(Users).filter(and_(Users.provider == openid.provider, Users.email == openid.email)).update(openid.dict())
    if not updates:
        session.add(Users(**User(**{**openid.dict(), **defaults}).dict()))
    session.commit()

    account = session.query(Users).filter(and_(Users.provider == openid.provider, Users.email == openid.email)).first()
    return User.from_orm(account)  # https://pydantic-docs.helpmanual.io/usage/models/#orm-mode-aka-arbitrary-class-instances


def get_profile(session: Session, user_id: str) -> Dict:
    user = session.query(Users).get(user_id)
    minecraft_accounts = session.query(Minecraft_Account).filter(Minecraft_Account.user_id == user_id).all()
    user.minecraft_accounts = minecraft_accounts
    return user


def update_profile(session: Session, user: UserIn):
    updates = session.query(Users).filter(Users.id == user.id).update(user.dict())
    if not updates:
        raise ex.AccountNotExistsException()
    session.commit()
    return session.query(Users).get(user.id)


def get_users(session: Session):
    users = session.query(Users)
    return paginate(users)


def update_profile_last_login(session: Session, user_id: str):
    session.query(Users).filter(Users.id == user_id).update({Users.last_login: datetime.now()})
    session.commit()
