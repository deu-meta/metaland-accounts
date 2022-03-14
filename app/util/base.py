from fastapi_sso.sso.base import SSOBase


class CustomSSOBase(SSOBase):
    client_tenant: str = NotImplemented  # Microsoft

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        client_tenant: str,
        redirect_uri: str,
        allow_insecure_http: bool = False,
        use_state: bool = True,
    ):
        super().__init__(client_id, client_secret, redirect_uri, allow_insecure_http, use_state)
        self.client_tenant = client_tenant
