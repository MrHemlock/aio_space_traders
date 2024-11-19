import asyncio
from typing import Final, TypeVar
# TODO: add .env support

from niquests import AsyncSession
from niquests._typing import QueryParameterType
from pyrate_limiter import Duration, Limiter, InMemoryBucket, Rate

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

        self.rates: list[Rate] = [
            Rate(2, Duration.SECOND),
            Rate(30, Duration.MINUTE),
        ]
        self.bucket: InMemoryBucket = InMemoryBucket(self.rates)
        self.limiter: Limiter = Limiter(self.bucket)

    async def close(self):
        await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

    async def _request(
        self,
        response_model: type[T],
        method: str,
        url: str,
        *,
        params: QueryParameterType | None = None,
        data: dict[str, int | float | str] | None = None,
    ) -> T:
        self.limiter.try_acquire(url)
        response = await self.session.request(method, url, params=params, json=data)
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

    async def get_agent(self) -> model.Agent:
        url = f"{self.BASE_URL}/my/agent"
        self.limiter.try_acquire("/my/agent")
        async with self.session as session:
            response = await session.get(url)
            return response.json()

    async def get_agents(
        self,
        limit: int = 10,
        page: int = 1,
    ) -> model.ListAgentsResponse:
        url = f"{self.BASE_URL}/agents"
        self.limiter.try_acquire("/agents")
        async with self.session as session:
            response = await session.get(
                url,
                data={
                    "limit": limit,
                    "page": page,
                },
            )
            return response.json()

    async def get_public_agent(self, agent_symbol: str = "FEBA66") -> model.Agent:
        url = f"{self.BASE_URL}/agents/f{agent_symbol}"
        self.limiter.try_acquire(f"/agents/{agent_symbol}")
        async with self.session as session:
            response = await session.get(
                url,
                data={"agentSymbol": agent_symbol},
            )
            return response.json()

    async def list_contracts(
        self,
        limit: int = 10,
        page: int = 1,
    ) -> model.ListContractsResponse:
        url = f"{self.BASE_URL}/my/contracts"
        self.limiter.try_acquire("/my/contracts")
        async with self.session as session:
            response = await session.get(
                url,
                data={
                    "limit": limit,
                    "page": page,
                },
            )
            return response.json()

    async def get_contract(self, contract_id: str) -> model.Contract:
        url = f"{self.BASE_URL}/my/contracts/{contract_id}"
        self.limiter.try_acquire(f"/my/contracts/{contract_id}")
        async with self.session as session:
            response = await session.get(url)
            return response.json()

    async def accept_contract(self, contract_id: str): ...

    def update_token(self, token: str) -> None:
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})
