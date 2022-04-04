from typing import Dict, List
from uuid import uuid4

from black import Dict
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_jwt_auth import AuthJWT
from mtl_accounts.database.conn import db
from mtl_accounts.database.crud import create_mincraft
from mtl_accounts.database.redis import redis_conn
from mtl_accounts.database.schema import Minecraft_Account, Users
from mtl_accounts.errors import exceptions as ex
from mtl_accounts.models import MessageOk, MinecraftToken, UserToken
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import JSONResponse

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
async def get_verify(
    request: Request, uuid: str, credentials: HTTPAuthorizationCredentials = Depends(security), session: Session = Depends(db.session)
):
    rd = redis_conn()
    minecraft = rd.lrange(uuid, 0, -1)
    minecraft = list(map(lambda s: s.decode("ascii"), minecraft))

    if minecraft is None:
        raise ex.AuthExpiredEx

    create_mincraft(session, MinecraftToken(id=minecraft[0], provider=minecraft[1], displayName=minecraft[2]), request.state.user.mail)

    rd.delete(uuid)
    return MessageOk()


@router.get("/me")
async def get_verify(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security), session: Session = Depends(db.session)):
    result = (
        session.query(Minecraft_Account, Users)
        .filter(Minecraft_Account.user_mail == Users.mail)
        .filter(Minecraft_Account.user_mail == request.state.user.mail)
        .first()
    )
    return result


@router.put("/update-profile")
async def update_profile(
    request: Request, user: Dict[str, str], credentials: HTTPAuthorizationCredentials = Depends(security), session: Session = Depends(db.session)
):
    session.query(Users).filter(Users.mail == request.state.user.mail).update(user)
    session.commit()
    return MessageOk()
