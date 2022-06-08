from fastapi import HTTPException, status


class AccountExistsException(HTTPException):
    def __init__(self, detail: str = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail or "계정이 이미 존재합니다.",
        )


class AccountNotFoundException(HTTPException):
    def __init__(self, detail: str = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail or "해당 사용자가 존재하지 않습니다.",
        )


class AuthExpiredException(HTTPException):
    def __init__(self, detail: str = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail or "인증이 만료되었습니다.",
        )


class NotFoundAuthException(HTTPException):
    def __init__(self, detail: str = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail or "Authorization 요청 헤더가 없습니다.",
        )


class TokenInvalidException(HTTPException):
    def __init__(self, detail: str = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail or "토큰값이 유효하지 않아 인증에 실패했습니다.",
        )


class TokenDecodeException(HTTPException):
    def __init__(self, detail: str = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail or "Authorization 요청 헤더의 토큰 타입이 유효하지 않습니다.",
        )


class InsufficientPermissionException(HTTPException):
    def __init__(self, detail: str = None):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail or "권한이 없습니다",
        )
