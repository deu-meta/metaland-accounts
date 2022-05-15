from typing import Dict

from fastapi import HTTPException
from fastapi_sso.sso.base import SSOBase
from mtl_accounts.models import OpenID


class EmailError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


class KakaoSSO(SSOBase):
    provider = "kakao"
    scope = ["openid"]
    version = "v2"

    async def get_discovery_document(self) -> Dict[str, str]:
        return {
            "authorization_endpoint": f"https://kauth.kakao.com/oauth/authorize?client_id={self.client_secret}&response_type=code&redirect_uri={self.redirect_uri}",
            "token_endpoint": f"https://kauth.kakao.com/oauth/token",
            "userinfo_endpoint": f"https://kapi.kakao.com/{self.version}/user/me",
        }

    @classmethod
    async def openid_from_response(cls, response: dict) -> OpenID:
        if dict(response["kakao_account"]).get("email") is None:
            raise HTTPException(status_code=404, detail="Please check your email consent")
        return OpenID(display_name=response["properties"]["nickname"], email=response["kakao_account"]["email"], provider=cls.provider)
