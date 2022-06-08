from typing import Dict

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from mtl_accounts.models import OpenID

from .base import CustomSSOBase


class MicrosoftCustomSSO(CustomSSOBase):
    provider = "microsoft"
    scope = ["email", "openid", "profile", "User.Read"]
    version = "v1.0"

    async def get_discovery_document(self) -> Dict[str, str]:
        return {
            "authorization_endpoint": f"https://login.microsoftonline.com/{self.client_tenant}/oauth2/v2.0/authorize",
            "token_endpoint": f"https://login.microsoftonline.com/{self.client_tenant}/oauth2/v2.0/token",
            "userinfo_endpoint": f"https://graph.microsoft.com/{self.version}/me",
        }

    @classmethod
    async def openid_from_response(cls, response: dict) -> OpenID:
        openid = OpenID(
            display_name=response.get("display_name") or response.get("displayName") or response.get("name") or None,
            given_name=response.get("given_name") or response.get("givenName") or response.get("name") or None,
            job_title=response.get("job_title") or response.get("jobTitle") or None,
            email=response.get("email") or response.get("mail") or response.get("upn") or None,
            provider=cls.provider,
        )
        if openid.display_name is None or openid.email is None:
            raise HTTPException(
                status.HTTP_406_NOT_ACCEPTABLE,
                f"Given OpenID data does not satisfy constraint.",
                content=jsonable_encoder(
                    {
                        "openid": openid,
                    }
                ),
            )

        return openid
