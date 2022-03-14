import os

from dotenv import load_dotenv
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from util.authentication import create_jwt, decode_jwt
from util.microsoft import MicrosoftCustomSSO

load_dotenv(verbose=True)

router = APIRouter()

microsoft_sso = MicrosoftCustomSSO(
    client_id=os.getenv("MY_CLIENT_ID"),
    client_secret=os.getenv("MY_CLIENT_SECRET"),
    client_tenant=os.getenv("MY_CLIENT_TENANT"),
    redirect_uri=os.getenv("REDIRECT_URL"),
    allow_insecure_http=True,
    use_state=False,
)


@router.get("/microsoft/login")
async def microsoft_login():
    return await microsoft_sso.get_login_redirect()


@router.get("/microsoft/callback")
async def microsoft_callback(request: Request):
    user = await microsoft_sso.verify_and_process(request)
    return create_jwt(user)


@router.get("/")
async def main(request: Request):
    cookies = request.cookies.get("set-cookie")
    return decode_jwt(cookies)
