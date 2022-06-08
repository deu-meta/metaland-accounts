from fastapi import HTTPException, status


class StatusCode:
    HTTP_500 = 500
    HTTP_400 = 400
    HTTP_401 = 401
    HTTP_403 = 403
    HTTP_404 = 404
    HTTP_405 = 405


class APIException(Exception):
    status_code: int
    message: str
    ex: Exception

    def __init__(
        self,
        *,
        status_code: int = StatusCode.HTTP_500,
        message: str = None,
        ex: Exception = None,
    ):
        self.status_code = status_code
        self.message = message
        self.ex = ex
        super().__init__(ex)


class AccountExistsException(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            message=f"Account is exists",
            ex=ex,
        )


class AccountNotExistsException(HTTPException):
    def __init__(self, detail: str = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail or f"해당 사용자가 존재하지 않습니다.",
        )


class AuthExpiredException(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            message=f"Authentication is expired",
            ex=ex,
        )


class NotFoundAuthException(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            message=f"Authorization 요청 헤더가 없습니다.",
            ex=ex,
        )


class TokenInvalidException(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            message=f"토큰값이 유효하지 않아 인증에 실패했습니다.",
            ex=ex,
        )


class TokenDecodeException(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            message=f"Authorization 요청 헤더의 토큰 타입이 유효하지 않습니다.",
            ex=ex,
        )
