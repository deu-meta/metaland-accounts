from typing import Dict

from fastapi_sso.sso.base import OpenID

from .base import CustomSSOBase


class MicrosoftCustomSSO(CustomSSOBase):
    provider = "microsoft"
    scope = ["openid"]
    version = "v1.0"

    async def get_discovery_document(self) -> Dict[str, str]:
        return {
            "authorization_endpoint": f"https://login.microsoftonline.com/{self.client_tenant}/oauth2/v2.0/authorize",
            "token_endpoint": f"https://login.microsoftonline.com/{self.client_tenant}/oauth2/v2.0/token",
            "userinfo_endpoint": f"https://graph.microsoft.com/{self.version}/me",
        }

    @classmethod
    async def openid_from_response(cls, response: dict) -> OpenID:
        return response
