from starlette.responses import JSONResponse


class StatusCode:
    HTTP_500 = 500
    HTTP_400 = 400
    HTTP_401 = 401
    HTTP_403 = 403
    HTTP_404 = 404
    HTTP_405 = 405


class APIException(Exception):
    status_code: int
    code: str
    msg: str
    detail: str
    ex: Exception

    def __init__(
        self,
        *,
        status_code: int = StatusCode.HTTP_500,
        code: str = "000000",
        msg: str = None,
        detail: str = None,
        ex: Exception = None,
    ):
        self.status_code = status_code
        self.code = code
        self.msg = msg
        self.detail = detail
        self.ex = ex
        super().__init__(ex)


class NotFoundAuthEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            msg=f"Authorization 요청 헤더가 없습니다.",
            detail=f"Authorization is empty.",
            code=f"{StatusCode.HTTP_401}{'2001'}",
            ex=ex,
        )


class TokenInvalidEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            msg=f"토큰값이 유효하지 않아 인증에 실패했습니다.",
            detail="Token is invalid.",
            code=f"{StatusCode.HTTP_401}{'2003'}",
            ex=ex,
        )


class TokenDecodeEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            msg=f"Authorization 요청 헤더의 토큰 타입이 유효하지 않습니다.",
            detail="Token type is invalid.",
            code=f"{StatusCode.HTTP_401}{'2002'}",
            ex=ex,
        )


class AuthExpiredEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            msg=f"인증이 만료되었습니다.",
            detail=f"Authentication is expired",
            code=f"{StatusCode.HTTP_401}{'3001'}",
            ex=ex,
        )


class AccountExistsEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            msg=f"계정이 이미 존재합니다.",
            detail=f"Account is exists",
            code=f"{StatusCode.HTTP_401}{'3002'}",
            ex=ex,
        )
