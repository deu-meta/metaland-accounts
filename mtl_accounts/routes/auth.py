import os

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_jwt_auth import AuthJWT
from mtl_accounts.database.conn import db
from mtl_accounts.database.crud import create_users
from mtl_accounts.database.schema import Users
from mtl_accounts.models import UserToken
from mtl_accounts.util.microsoft import MicrosoftCustomSSO
from pydantic import BaseModel
from sqlalchemy.orm import Session

router = APIRouter()

security = HTTPBearer()

microsoft_sso = MicrosoftCustomSSO(
    client_id=os.getenv("MTL_ACCOUNTS_OAUTH2_MICROSOFT_CLIENT_ID"),
    client_secret=os.getenv("MTL_ACCOUNTS_OAUTH2_MICROSOFT_SECRET"),
    client_tenant=os.getenv("MTL_ACCOUNTS_OAUTH2_MICROSOFT_CLIENT_TENANT"),
    redirect_uri=os.getenv("MTL_ACCOUNTS_OAUTH2_MICROSOFT_REDIRECT_URL"),
    allow_insecure_http=True,
    use_state=False,
)


class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv("MTL_ACCOUNTS_SECRET_KEY")
    # 쿠키에서 JWT를 저장하고 가져오도록 애플리케이션 구성
    authjwt_token_location: set = {"cookies", "headers"}
    # Disable CSRF Protection for this example. default is True
    authjwt_cookie_csrf_protect: bool = False


@AuthJWT.load_config
def get_config():
    return Settings()


@router.get("/test")
async def authorize_test(credentials: HTTPAuthorizationCredentials = Depends(security), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_raw_jwt()
    return {"test": current_user}


@router.get("/microsoft/login")
async def microsoft_login():
    return await microsoft_sso.get_login_redirect()


@router.get("/microsoft/callback")
async def microsoft_callback(request: Request, Authorize: AuthJWT = Depends(), session: Session = Depends(db.session)):
    user = await microsoft_sso.verify_and_process(request)

    account = session.query(Users).filter(Users.mail == user["mail"]).first()

    user = UserToken(**user, provider="office365", role="default")
    if account is None:
        create_users(session, user)
    else:
        user.role = account.role

    access_token = Authorize.create_access_token(subject=user.mail, user_claims=user.dict())
    refresh_token = Authorize.create_refresh_token(subject=user.mail, user_claims=user.dict())
    Authorize.set_refresh_cookies(refresh_token)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh")
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_raw_jwt()
    current_user["type"] = "access"
    new_access_token = Authorize.create_access_token(subject=current_user["sub"], user_claims=current_user)
    return {"new_access_token": new_access_token}


@router.delete("/delete")
def delete(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    Authorize.unset_jwt_cookies()
    return {"msg": "Successfully logout"}
