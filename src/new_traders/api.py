from types import TracebackType
from typing import Any, TypeVar

from niquests import AsyncSession
from niquests._typing import QueryParameterType
from niquests.exceptions import JSONDecodeError as RequestsJSONDecodeError
from niquests.models import Response

from new_traders.errors import ERROR_MAPPING, SpaceTradersAPIError

from . import model

T = TypeVar("T")


class SpaceTraders:
    def __init__(self, token: str | None) -> None:
        self.session: AsyncSession = AsyncSession(
            base_url="https://api.spacetraders.io/v2"
        )
        self.token = token
        self.session.headers.update({"Accept": "application/json"})
        if self.token:
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})

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
        if not response.ok:
            self._handle_error(response)
        json_data = await response.json()
        return response_model(**json_data)

    def _handle_error(self, response: Response):
        response_json = {}
        try:
            response_json = response.json()
        except RequestsJSONDecodeError:
            response.raise_for_status()  # pyright: ignore[reportUnusedCallResult]

        error = response_json["error"]
        code = error["code"]
        message = error["message"]
        error_type = ERROR_MAPPING.get(code)

        try:
            response.raise_for_status()  # pyright: ignore[reportUnusedCallResult]
        except Exception as e:
            if not error_type:
                raise SpaceTradersAPIError(code, message, response_json) from e
            raise error_type(code, message, response_json) from e

    async def get_status(self) -> model.ServerStatsResponse:
        """Fetch the current status of the server."""
        return await self._request(
            model.ServerStatsResponse,
            "GET",
            "/",
        )

    async def register_new_agent(
        self,
        faction: model.FactionSymbol,
        agent_symbol: str,
        email: str,
    ) -> model.RegisterNewAgentResponse:
        """Creates a new agent and ties it to an account."""
        data = {
            "faction": faction,
            "symbol": agent_symbol,
            "email": email,
        }
        return await self._request(
            model.RegisterNewAgentResponse,
            "POST",
            "/register",
            data=data,
        )

    async def get_agent(self) -> model.GetAgentResponse:
        return await self._request(
            model.GetAgentResponse,
            "GET",
            "/my/agent",
        )

    async def list_agents(self, limit: int, page: int) -> model.ListAgentsResponse:
        params = {"limit": str(limit), "page": str(page)}
        return await self._request(
            model.ListAgentsResponse,
            "GET",
            "/agents",
            params=params,
        )

    async def get_public_agent(self, agent_symbol: str) -> model.GetAgentResponse:
        return await self._request(
            model.GetAgentResponse,
            "GET",
            f"/agents/{agent_symbol}",
        )

    async def list_contracts(
        self, limit: int, page: int
    ) -> model.ListContractsResponse:
        params = {"limit": str(limit), "page": str(page)}
        return await self._request(
            model.ListContractsResponse,
            "GET",
            "/my/contracts",
            params=params,
        )

    async def get_contract(self, contract_id: str) -> model.GetContractResponse:
        return await self._request(
            model.GetContractResponse,
            "GET",
            f"/my/contracts/{contract_id}",
        )

    async def accept_contract(self, contract_id: str) -> model.AcceptContractResponse:
        return await self._request(
            model.AcceptContractResponse,
            "POST",
            f"/my/contracts/{contract_id}/accept",
        )

    async def deliver_cargo_to_contract(
        self,
        contract_id: str,
        ship_symbol: str,
        trade_symbol: str,
        units: int,
    ) -> model.DeliverCargoToContractResponse:
        data = {
            "shipSymbol": ship_symbol,
            "tradeSymbol": trade_symbol,
            "units": units,
        }
        return await self._request(
            model.DeliverCargoToContractResponse,
            "POST",
            f"/my/contracts/{contract_id}/deliver",
            data=data,
        )

    async def fulfill_contract(self, contract_id: str) -> model.FulFillContractResponse:
        return await self._request(
            model.FulFillContractResponse,
            "POST",
            f"/my/contracts/{contract_id}/fulfill",
        )

    def update_token(self, token: str) -> None:
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})
