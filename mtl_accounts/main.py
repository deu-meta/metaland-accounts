import os

import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader, HTTPBearer
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from mtl_accounts.database.conn import db
from mtl_accounts.errors import exceptions as ex
from mtl_accounts.middlewares.token_validator import access_control
from mtl_accounts.middlewares.trusted_hosts import TrustedHostMiddleware

from .routes import auth, users

load_dotenv(verbose=True)


def create_app():
    app = FastAPI()

    db.init_app(app)

    app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=access_control)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"], except_path=["/health"])

    # HTTP Host Header 공격 방어
    # 모든 요청이 Host 헤더가 적절하게 세팅되었는지 강제하기 위한 미들웨어
    # except_path : AWS를 로드밸런싱으로 사용할때, 내부아이피로 health check를 한다
    # 그로 인해 모든 health check를 실패한다.

    # middleware 은 stack 으로 동작하기때문에 가장 나중에 넣은것부터 실행한다.

    @app.exception_handler(AuthJWTException)
    def authjwt_exception_handler(request: Request, exc: AuthJWTException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

    @app.exception_handler(ex.APIException)
    def api_exception_handler(request: Request, error: ex.APIException):
        error_dict = dict(status=error.status_code, msg=error.msg, detail=error.detail, code=error.code)
        return JSONResponse(status_code=error.status_code, content=error_dict)

    app.include_router(router=auth.router, tags=["JWT"], prefix="/jwt")
    app.include_router(router=users.router, tags=["Users"], prefix="/user")
    return app


app = create_app()

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
