from uuid import uuid4

import mtl_accounts.database.crud as crud
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from mtl_accounts.database.conn import db
from mtl_accounts.database.redis import redis_conn
from mtl_accounts.database.schema import Page
from mtl_accounts.errors import exceptions as ex
from mtl_accounts.models import MessageOk, Minecraft, User, UserIn
from sqlalchemy.orm import Session
from starlette.requests import Request

router = APIRouter()

security = HTTPBearer()


@router.post("/verify")
async def post_verify(mincraftaccount: Minecraft, session: Session = Depends(db.session)):
    if crud.exists_mincraft(session, mincraftaccount.id):
        raise ex.AccountExistsException()

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
        raise ex.AuthExpiredException()

    crud.create_mincraft(session, Minecraft(id=minecraft[0], provider=minecraft[1], display_name=minecraft[2]), user_email)

    rd.delete(uuid)
    return MessageOk()


@router.get("/me")
async def get_profile(request: Request, Authorize: AuthJWT = Depends(), session: Session = Depends(db.session)):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()

    return crud.get_profile(session, user_id)


@router.get("", response_model=Page[User])
async def users(request: Request, Authorize: AuthJWT = Depends(), session: Session = Depends(db.session)):
    Authorize.jwt_required()
    jwt = Authorize.get_raw_jwt()
    if jwt["role"] not in ["staff", "admin"]:
        raise ex.TokenInvalidException()

    return crud.get_users(session)


@router.put("/{id}")
async def update_profile(user: UserIn, Authorize: AuthJWT = Depends(), session: Session = Depends(db.session)):
    Authorize.jwt_required()
    jwt = Authorize.get_raw_jwt()

    # only admin can grant role
    if user.role is not None and jwt["role"] != "admin":
        raise ex.TokenInvalidException()

    # check if user trying to modify other
    if jwt["sub"] != user.id and jwt["role"] not in ["staff", "admin"]:
        raise ex.TokenInvalidException()

    return crud.update_profile(session, user)
