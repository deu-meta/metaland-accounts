from uuid import uuid4

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from mtl_accounts.database.conn import db
from mtl_accounts.database.crud import (
    create_mincraft,
    exists_mincraft,
    get_profile,
)
from mtl_accounts.database.redis import redis_conn
from mtl_accounts.errors import exceptions as ex
from mtl_accounts.models import MessageOk, Minecraft
from sqlalchemy.orm import Session
from starlette.requests import Request

router = APIRouter()

security = HTTPBearer()


@router.post("/verify")
async def post_verify(mincraftaccount: Minecraft, session: Session = Depends(db.session)):
    if exists_mincraft(session, mincraftaccount.id):
        raise ex.AccountExistsEx

    rd = redis_conn()
    uuid = uuid4()

    rd.lpush(str(uuid), *mincraftaccount.dict().values())
    return {"uuid": uuid}


@router.get("/verify/{uuid}")
async def get_verify(request: Request, uuid: str, Authorize: AuthJWT = Depends(), session: Session = Depends(db.session)):
    Authorize.jwt_required()
    user_email = Authorize.get_jwt_subject()

    rd = redis_conn()
    minecraft = rd.lrange(uuid, 0, -1)
    minecraft = list(map(lambda s: s.decode("ascii"), minecraft))

    if minecraft is None:
        raise ex.AuthExpiredEx

    create_mincraft(session, Minecraft(id=minecraft[0], provider=minecraft[1], display_name=minecraft[2]), user_email)

    rd.delete(uuid)
    return MessageOk()


@router.get("/me")
async def get_verify(request: Request, Authorize: AuthJWT = Depends(), session: Session = Depends(db.session)):
    Authorize.jwt_required()
    user_mail = Authorize.get_jwt_subject()

    return get_profile(session, user_mail)
