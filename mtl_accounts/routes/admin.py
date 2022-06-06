from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from mtl_accounts.database.conn import db
from mtl_accounts.database.crud import update_role
from mtl_accounts.errors import exceptions as ex
from mtl_accounts.models import MessageOk, Role
from sqlalchemy.orm import Session
from starlette.requests import Request

router = APIRouter()

security = HTTPBearer()


@router.put("/update-role")
async def update_profile(request: Request, email: str, role: Role, Authorize: AuthJWT = Depends(), session: Session = Depends(db.session)):
    Authorize.jwt_required()
    jwt = Authorize.get_raw_jwt()
    if jwt["role"] != "admin":
        raise ex.TokenInvalidEx
    update_role(session, email, role)
    return MessageOk()
