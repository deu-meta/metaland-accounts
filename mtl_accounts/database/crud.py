from typing import Dict

from mtl_accounts.database.schema import Minecraft_Account, Users
from mtl_accounts.models import Minecraft, OpenID, Role, User
from sqlalchemy.orm import Session


def create_mincraft(session: Session, minecraft: Minecraft, email: str):
    users = Minecraft_Account(id=minecraft.id, user_email=email, provider=minecraft.provider, display_name=minecraft.display_name)
    session.add(users)
    session.commit()


def exists_mincraft(session: Session, id: str) -> bool:
    result = session.query(Minecraft_Account).filter(Minecraft_Account.id == id).first()
    if result:
        return True
    return False


def create_or_update_user(session: Session, user: OpenID) -> User:
    updates = session.query(Users).filter(Users.email == user.email).update(user.dict())
    if not updates:
        session.add(Users(**User(**user.dict()).dict()))
    session.commit()

    account = session.query(Users).filter(Users.email == user.email).first()
    return User.from_orm(account)  # https://pydantic-docs.helpmanual.io/usage/models/#orm-mode-aka-arbitrary-class-instances


def get_profile(session: Session, user_mail: str) -> Dict:
    profile = (
        session.query(Minecraft_Account, Users)
        .filter(Minecraft_Account.user_email == Users.email)
        .filter(Minecraft_Account.user_email == user_mail)
        .first()
    )
    return profile


def update_role(session: Session, email: str, role: Role):
    user = session.query(Users).filter(Users.email == email).first()
    user.role = role.value
    session.commit()
    session.refresh(user)
