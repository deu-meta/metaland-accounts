import binascii
import json
import os

import mtl_accounts.database.crud as crud
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from mtl_accounts.database.conn import db
from mtl_accounts.database.redis import redis_conn
from mtl_accounts.errors import exceptions as ex
from mtl_accounts.models import MessageOk, MinecraftAccountIn, MinecraftProvider, User
from sqlalchemy.orm import Session

router = APIRouter()

security = HTTPBearer()


@router.post("/verify")
async def request_verify(minecraft_account: MinecraftAccountIn, Authorize: AuthJWT = Depends(), session: Session = Depends(db.session)):
    if crud.exists_mincraft(session, minecraft_account.id):
        raise ex.AccountExistsException(f"{minecraft_account.id} 마인크래프트 계정이 이미 존재합니다.")

    Authorize.jwt_required()
    user = Authorize.get_raw_jwt()
    if user.get("role") not in ["admin"]:
        raise ex.InsufficientPermissionException()

    rd = redis_conn()
    code = binascii.hexlify(os.urandom(20)).decode("utf-8")  # generate secure random code

    rd.lpush(code, json.dumps(minecraft_account.dict()))
    return {"code": code}


@router.get("/verify/{code}")
async def get_verify_information(code: str, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    rd = redis_conn()
    minecraft_account = json.loads(next(map(lambda s: s.decode("ascii"), rd.lrange(code, 0, -1))))
    if minecraft_account is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "요청한 내용이 존재하지 않습니다.")

    return minecraft_account


@router.post("/verify/{code}")
async def verify_code(code: str, Authorize: AuthJWT = Depends(), session: Session = Depends(db.session)):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()

    rd = redis_conn()
    try:
        minecraft_account = json.loads(next(map(lambda s: s.decode("ascii"), rd.lrange(code, 0, -1))))
    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "해당되는 코드가 존재하지 않습니다.")

    if minecraft_account.get("provider") not in MinecraftProvider._member_names_:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "잘못된 provider 입니다.")

    crud.create_mincraft(session, MinecraftAccountIn(**minecraft_account), user_id)

    rd.delete(code)
    return MessageOk()


@router.get("/{id}/user")
async def get_user_by_minecraft_account(id: str, Authorize: AuthJWT = Depends(), session: Session = Depends(db.session)) -> User:
    Authorize.jwt_required()
    user = Authorize.get_raw_jwt()
    if user.get("role") not in ["admin"]:
        raise ex.InsufficientPermissionException()

    minecraft_account = crud.get_minecraft_account(session, id)
    if minecraft_account is None:
        raise ex.AccountNotFoundException()

    return minecraft_account.user
