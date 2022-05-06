import base64
import hmac
import os
import re
import time
import typing

import jwt
import mtl_accounts.errors.exceptions as ex
from dotenv import load_dotenv
from jwt.exceptions import DecodeError, ExpiredSignatureError
from mtl_accounts.errors.exceptions import APIException
from mtl_accounts.models import UserToken
from mtl_accounts.util.authentication import decode_jwt
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

SECRET_KEY = os.getenv("MTL_ACCOUNTS_SECRET_KEY")
ALGORITHM = os.getenv("MTL_ACCOUNTS_JWT_ALGORITHM")
EXCEPT_PATH_LIST = ["/", "/openapi.json", "/user/verify"]
EXCEPT_PATH_REGEX = "^(/docs|/redoc|/jwt)"


async def access_control(request: Request, call_next: RequestResponseEndpoint) -> Response:
    request.state.start = time.time()
    request.state.inspect = None
    request.state.user = None
    request.state.service = None

    # ip = request.headers["x-forwarded-for"] if "x-forwarded-for" in request.headers.keys() else request.client.host
    # request.state.ip = ip.split(",")[0] if "," in ip else ip
    # AWS 사용자 IP

    headers = request.headers
    cookies = request.cookies

    url = request.url.path
    if await url_pattern_check(url, EXCEPT_PATH_REGEX) or url in EXCEPT_PATH_LIST:
        response = await call_next(request)  # https://blog.neonkid.xyz/271
        return response

    try:
        if "authorization" not in headers.keys():
            raise ex.NotFoundAuthEx()
        try:
            token_info = await decode_jwt(access_token=str(headers.get("authorization")).split(" ")[1])
            request.state.user = UserToken(**token_info)
        except ExpiredSignatureError:
            raise ex.TokenInvalidEx()
        except DecodeError:
            raise ex.TokenDecodeEx()
        response = await call_next(request)
    except Exception as e:
        error = await exception_handler(e)
        error_dict = dict(status=error.status_code, msg=error.msg, detail=error.detail, code=error.code)
        response = JSONResponse(status_code=error.status_code, content=error_dict)

    return response


async def url_pattern_check(path, pattern):
    result = re.match(pattern, path)
    if result:
        return True
    return False


async def exception_handler(error: Exception):
    print(error)
    if not isinstance(error, APIException):
        error = APIException(ex=error, detail=str(error))
    return error
