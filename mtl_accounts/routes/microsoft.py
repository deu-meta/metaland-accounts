import json
import os

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi_jwt_auth import AuthJWT
from mtl_accounts.database.conn import db
from mtl_accounts.database.crud import create_or_update_user, update_profile_last_login
from mtl_accounts.models import Role
from mtl_accounts.util.sso.microsoft import MicrosoftCustomSSO
from sqlalchemy.orm import Session

router = APIRouter()

microsoft_sso = MicrosoftCustomSSO(
    client_id=os.getenv("MTL_ACCOUNTS_OAUTH2_MICROSOFT_CLIENT_ID"),
    client_secret=os.getenv("MTL_ACCOUNTS_OAUTH2_MICROSOFT_SECRET"),
    client_tenant=os.getenv("MTL_ACCOUNTS_OAUTH2_MICROSOFT_CLIENT_TENANT"),
    redirect_uri=os.getenv("MTL_ACCOUNTS_OAUTH2_MICROSOFT_REDIRECT_URI"),
    allow_insecure_http=True if os.getenv("MTL_ACCOUNTS_DEBUG", "false").lower() == "true" else False,
    use_state=False if os.getenv("MTL_ACCOUNTS_DEBUG", "false").lower() == "true" else True,
)

JWT_REDIRECT_URL = os.getenv("MTL_ACCOUNTS_JWT_REDIRECT_URL")


@router.get("/test")
async def authorize_test(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_raw_jwt()
    return {"test": current_user}


@router.get("/microsoft/login")
async def microsoft_login():
    return await microsoft_sso.get_login_redirect()


@router.get("/microsoft/callback")
async def microsoft_callback(request: Request, Authorize: AuthJWT = Depends(), session: Session = Depends(db.session)):
    user = await microsoft_sso.verify_and_process(request)

    defaults = {}
    # 재학생일 시 역할을 student로 설정
    if user.email.endswith("@office.deu.ac.kr"):
        defaults["role"] = Role.student

    account = create_or_update_user(session, user, defaults)

    access_token = Authorize.create_access_token(subject=account.id, user_claims=json.loads(account.json()))
    response = RedirectResponse(f"{JWT_REDIRECT_URL}#access_token={access_token}")

    refresh_token = Authorize.create_refresh_token(subject=account.id, user_claims=json.loads(account.json()))

    Authorize.set_refresh_cookies(refresh_token, response, max_age=1209600)

    return response


@router.post("/refresh")
def refresh(Authorize: AuthJWT = Depends(), session: Session = Depends(db.session)):
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_raw_jwt()
    current_user["type"] = "access"
    access_token = Authorize.create_access_token(subject=current_user["sub"], user_claims=current_user)

    update_profile_last_login(session, current_user["sub"])

    return {"access_token": access_token}


@router.delete("/delete")
def delete(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    Authorize.unset_jwt_cookies()
    return {"message": "Successfully logout"}
