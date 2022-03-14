import os
from time import time
from typing import Dict

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, Request
from starlette.responses import JSONResponse

load_dotenv(verbose=True)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


def create_jwt(user: Dict) -> Dict[str, str]:
    expires = {"expires": time() + 600}
    payload = dict(user, **expires)

    token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)

    response = JSONResponse({"status": "authenticated"})
    response.set_cookie(key="set-cookie", value=token, httponly=True)
    return response


def decode_jwt(token: str):
    decoded_token = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
    if decoded_token["expires"] >= time():
        return decoded_token
    else:
        raise HTTPException(status_code=400, detail="Certification Expired")
