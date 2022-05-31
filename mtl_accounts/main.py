import inspect
import os
import re

from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from mtl_accounts.database.conn import db
from mtl_accounts.errors.exceptions import APIException
from mtl_accounts.middlewares.trusted_hosts import TrustedHostMiddleware
from mtl_accounts.routes import admin, kakao, microsoft, users

# https://nuggy875.tistory.com/106


def create_app():
    app = FastAPI()

    db.init_app(app)
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

    class Settings(BaseModel):
        authjwt_secret_key: str = os.getenv("MTL_ACCOUNTS_SECRET_KEY")
        # 쿠키에서 JWT를 저장하고 가져오도록 애플리케이션 구성
        authjwt_token_location: set = {"cookies", "headers"}
        # Disable CSRF Protection for this example. default is True
        authjwt_cookie_csrf_protect: bool = False

    @AuthJWT.load_config
    def get_config():
        return Settings()

    @app.exception_handler(AuthJWTException)
    def authjwt_exception_handler(request: Request, exc: AuthJWTException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

    @app.exception_handler(Exception)
    def exception_handler(request: Request, exc: APIException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

    app.include_router(router=kakao.router, tags=["JWT"], prefix="/jwt")
    app.include_router(router=microsoft.router, tags=["JWT"], prefix="/jwt")
    app.include_router(router=users.router, tags=["Users"], prefix="/users")
    app.include_router(router=admin.router, tags=["Admin"], prefix="/admin")

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title="My Auth API",
            version="1.0",
            description="An API with an Authorize Button",
            routes=app.routes,
        )

        openapi_schema["components"]["securitySchemes"] = {
            "Bearer Auth": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization",
                "description": "Enter: **'Bearer &lt;JWT&gt;'**, where JWT is the access token",
            }
        }

        # Get all routes where jwt_optional() or jwt_required
        api_router = [route for route in app.routes if isinstance(route, APIRoute)]

        for route in api_router:
            path = getattr(route, "path")
            endpoint = getattr(route, "endpoint")
            methods = [method.lower() for method in getattr(route, "methods")]

            for method in methods:
                # access_token
                if (
                    re.search("jwt_required", inspect.getsource(endpoint))
                    or re.search("fresh_jwt_required", inspect.getsource(endpoint))
                    or re.search("jwt_optional", inspect.getsource(endpoint))
                ):
                    openapi_schema["paths"][path][method]["security"] = [{"Bearer Auth": []}]

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi
    return app


app = create_app()
