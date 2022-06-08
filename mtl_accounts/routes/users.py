import binascii
import json
import os

import mtl_accounts.database.crud as crud
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from mtl_accounts.database.conn import db
from mtl_accounts.database.schema import Page
from mtl_accounts.errors import exceptions as ex
from mtl_accounts.models import User, UserIn
from sqlalchemy.orm import Session
from starlette.requests import Request

router = APIRouter()

security = HTTPBearer()


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
