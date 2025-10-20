from uuid import uuid4

import enum
import httpx


def new_id():
    return str(uuid4())


class Provider(enum.Enum):
    GITHUB = "https://github.com/login/oauth/access_token"


class Oauth:
    def __init__(
        self, provider: Provider, client_id: str, client_secret: str, redirect_uri: str
    ):
        self.provider = provider
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    async def get_token(self, code: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.provider.value,
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                    "redirect_uri": self.redirect_uri,
                },
                headers={"Accept": "application/json"},
            )
            response.raise_for_status()
            return response.json().get("access_token")
