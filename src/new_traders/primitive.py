import asyncio
from types import TracebackType
from typing import Any, Final, TypeVar
# TODO: add .env support

from niquests import AsyncSession
from niquests._typing import QueryParameterType

from . import model

T = TypeVar("T")


class SpaceTraders:
    def __init__(self, token: str) -> None:
        self.BASE_URL: Final = "https://api.spacetraders.io/v2"
        self.session: AsyncSession = AsyncSession()
        self.token: str = token
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/json",
            },
        )

    async def close(self):
        await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        await self.close()

    async def _request(
        self,
        response_model: type[T],
        method: str,
        url: str,
        *,
        params: QueryParameterType | None = None,
        data: dict[str, Any] | None = None,
    ) -> T:
        response = await self.session.request(
            method,
            url,
            params=params,
            json=data,
        )
        json_data = await response.json()
        return response_model(**json_data)

    async def get_status(self) -> model.ServerStatsResponse:
        """Fetch the current status of the server."""
        url = f"{self.BASE_URL}/"
        server_status = await self._request(
            model.ServerStatsResponse,
            "GET",
            url,
        )
        return server_status

    async def register_new_agent(
        self,
        faction: model.FactionSymbol,
        agent_symbol: str,
        email: str,
    ) -> model.RegisterNewAgentResponse:
        """Creates a new agent and ties it to an account."""
        url = f"{self.BASE_URL}/register"
        data = {
            "faction": faction,
            "symbol": agent_symbol,
            "email": email,
        }
        agent = await self._request(
            model.RegisterNewAgentResponse,
            "POST",
            url,
            data=data,
        )
        return agent

    def update_token(self, token: str) -> None:
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})
