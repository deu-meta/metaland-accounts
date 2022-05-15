import os

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi_jwt_auth import AuthJWT
from mtl_accounts.database.conn import db
from mtl_accounts.database.crud import create_users
from mtl_accounts.database.schema import Users
from mtl_accounts.models import User
from mtl_accounts.util.sso.kakao import KakaoSSO
from sqlalchemy.orm import Session

router = APIRouter()

kakao_sso = KakaoSSO(
    client_id=os.getenv("MTL_ACCOUNTS_OAUTH2_KAKAO_REST_API_KEY"),
    client_secret=os.getenv("MTL_ACCOUNTS_OAUTH2_KAKAO_REST_API_KEY"),
    redirect_uri=os.getenv("MTL_ACCOUNTS_OAUTH2_KAKAO_REDIRECT_URI"),
    use_state=False,
    allow_insecure_http=True,
)

JWT_REDIRECT_URL = os.getenv("MTL_ACCOUNTS_JWT_REDIRECT_URL")


@router.get("/test")
async def authorize_test(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_raw_jwt()
    return {"test": current_user}


@router.get("/kakao/login")
async def kakao_login():
    return await kakao_sso.get_login_redirect()


@router.get("/kakao/callback")
async def kakao_callback(request: Request, Authorize: AuthJWT = Depends(), session: Session = Depends(db.session)):
    user = await kakao_sso.verify_and_process(request)

    user = User(**user.dict(), role="default")

    account = session.query(Users).filter(Users.mail == user.email).first()

    if account is None:
        create_users(session, user)
    else:
        user.role = account.role

    access_token = Authorize.create_access_token(subject=user.email, user_claims=user.dict())
    response = RedirectResponse(f"{JWT_REDIRECT_URL}#access_token={access_token}")

    refresh_token = Authorize.create_refresh_token(subject=user.email, user_claims=user.dict())

    Authorize.set_refresh_cookies(refresh_token, response, max_age=1209600)

    return response
