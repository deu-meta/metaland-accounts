import time
from typing import Dict

import pytest
from faker import Faker
from fastapi_jwt_auth import AuthJWT
from httpx import AsyncClient

Authorize = AuthJWT()
fake = Faker("ko_KR")


def create_user():
    return {
        "displayName": fake.name(),
        "givenName": "null",
        "jobTitle": fake.job(),
        "mail": fake.email(),
        "provider": "office365",
        "role": "default",
    }


def build_access_token(
    expired: bool = False,
    issued_at: int = int(time.time()),
    claims: Dict[str, str] = None,
):
    expires = expires = issued_at - 1 if expired else issued_at + 900

    return Authorize._create_token(
        subject=claims["displayName"],
        type_token="access",
        exp_time=expires,
        algorithm="HS256",
        user_claims=claims,
    )


def build_access_token_expired():
    user = create_user()
    return build_access_token(expired=True, claims=user)


@pytest.mark.anyio
async def test_normal_user(app):
    issued_at = int(time.time())
    expires = issued_at + 900
    user = create_user()
    access_token = build_access_token(issued_at=issued_at, claims=user)
    async with AsyncClient(app=app, base_url="http://test", headers={"Authorization": "Bearer " + access_token}) as ac:
        response = await ac.get("jwt/test")

    assert response.status_code == 200


@pytest.mark.anyio
async def test_expired_token(app):
    access_token = build_access_token_expired()
    async with AsyncClient(app=app, base_url="http://test", headers={"Authorization": "Bearer " + access_token}) as ac:
        response = await ac.get("jwt/test")
    assert response.status_code == 422
    assert response.json() == {"detail": "Signature has expired"}


# python -m pytest -s
