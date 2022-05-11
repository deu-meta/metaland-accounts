

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
        msg: str = None,
        ex: Exception = None,
    ):
        self.status_code = status_code
        self.msg = msg
        self.ex = ex
        super().__init__(ex)


class AccountExistsEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            message=f"Account is exists",
            ex=ex,
        )


class AuthExpiredEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            msg=f"Authentication is expired",
            ex=ex,
        )
