from typing import Dict
from uuid import uuid4

from black import Dict
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from mtl_accounts.database.conn import db
from mtl_accounts.database.crud import create_mincraft
from mtl_accounts.database.redis import redis_conn
from mtl_accounts.database.schema import Minecraft_Account, Users
from mtl_accounts.errors import exceptions as ex
from mtl_accounts.models import MessageOk, MinecraftToken
from sqlalchemy.orm import Session
from starlette.requests import Request

router = APIRouter()

security = HTTPBearer()


@router.post("/verify")
async def post_verify(mincraftaccount: MinecraftToken, session: Session = Depends(db.session)):
    result = session.query(Minecraft_Account).filter(Minecraft_Account.id == mincraftaccount.id).first()
    if result is not None:
        raise ex.AccountExistsEx
    rd = redis_conn()
    uuid = uuid4()

    rd.lpush(str(uuid), *mincraftaccount.dict().values())
    return {"uuid": uuid}


@router.get("/verify/{uuid}")
async def get_verify(request: Request, uuid: str, Authorize: AuthJWT = Depends(), session: Session = Depends(db.session)):
    Authorize.jwt_required()
    user_mail = Authorize.get_jwt_subject()

    rd = redis_conn()
    minecraft = rd.lrange(uuid, 0, -1)
    minecraft = list(map(lambda s: s.decode("ascii"), minecraft))

    if minecraft is None:
        raise ex.AuthExpiredEx

    create_mincraft(session, MinecraftToken(id=minecraft[0], provider=minecraft[1], displayName=minecraft[2]), user_mail)

    rd.delete(uuid)
    return MessageOk()


@router.get("/me")
async def get_verify(request: Request, Authorize: AuthJWT = Depends(), session: Session = Depends(db.session)):
    Authorize.jwt_required()
    user_mail = Authorize.get_jwt_subject()

    result = (
        session.query(Minecraft_Account, Users)
        .filter(Minecraft_Account.user_mail == Users.mail)
        .filter(Minecraft_Account.user_mail == user_mail)
        .first()
    )
    return result


@router.put("/update-profile")
async def update_profile(request: Request, user: Dict[str, str], Authorize: AuthJWT = Depends(), session: Session = Depends(db.session)):
    Authorize.jwt_required()
    user_mail = Authorize.get_jwt_subject()

    session.query(Users).filter(Users.mail == user_mail).update(user)
    session.commit()
    return MessageOk()
