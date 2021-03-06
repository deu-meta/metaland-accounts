import json
import os

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi_jwt_auth import AuthJWT
from mtl_accounts.database.conn import db
from mtl_accounts.database.crud import create_or_update_user
from mtl_accounts.util.sso.kakao import KakaoSSO
from sqlalchemy.orm import Session

router = APIRouter()

kakao_sso = KakaoSSO(
    client_id=os.getenv("MTL_ACCOUNTS_OAUTH2_KAKAO_REST_API_KEY"),
    client_secret=os.getenv("MTL_ACCOUNTS_OAUTH2_KAKAO_SECRET"),
    redirect_uri=os.getenv("MTL_ACCOUNTS_OAUTH2_KAKAO_REDIRECT_URI"),
    allow_insecure_http=True if os.getenv("MTL_ACCOUNTS_DEBUG", "false").lower() == "true" else False,
    use_state=False if os.getenv("MTL_ACCOUNTS_DEBUG", "false").lower() == "true" else True,
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

    response = RedirectResponse(JWT_REDIRECT_URL)
    account = create_or_update_user(session, user)
    refresh_token = Authorize.create_refresh_token(subject=account.id, user_claims=json.loads(account.json()))
    Authorize.set_refresh_cookies(refresh_token, response, max_age=1209600)
    return response
