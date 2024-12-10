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
            base_url="https://api.spacetraders.io/v2",
        )
        self.token = token
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )
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
                raise SpaceTradersAPIError(
                    code,
                    message,
                    response_json,
                ) from e
            raise error_type(
                code,
                message,
                response_json,
            ) from e

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

    async def list_agents(
        self,
        limit: int = 10,
        page: int = 1,
    ) -> model.ListAgentsResponse:
        params = {"limit": str(limit), "page": str(page)}
        return await self._request(
            model.ListAgentsResponse,
            "GET",
            "/agents",
            params=params,
        )

    async def get_public_agent(
        self,
        agent_symbol: str = "FEBA66",
    ) -> model.GetAgentResponse:
        return await self._request(
            model.GetAgentResponse,
            "GET",
            f"/agents/{agent_symbol}",
        )

    async def list_contracts(
        self,
        limit: int = 10,
        page: int = 1,
    ) -> model.ListContractsResponse:
        params = {"limit": str(limit), "page": str(page)}
        return await self._request(
            model.ListContractsResponse,
            "GET",
            "/my/contracts",
            params=params,
        )

    async def get_contract(
        self,
        contract_id: str,
    ) -> model.GetContractResponse:
        return await self._request(
            model.GetContractResponse,
            "GET",
            f"/my/contracts/{contract_id}",
        )

    async def accept_contract(
        self,
        contract_id: str,
    ) -> model.AcceptContractResponse:
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

    async def fulfill_contract(
        self,
        contract_id: str,
    ) -> model.FulFillContractResponse:
        return await self._request(
            model.FulFillContractResponse,
            "POST",
            f"/my/contracts/{contract_id}/fulfill",
        )

    async def list_factions(
        self,
        limit: int = 10,
        page: int = 1,
    ) -> model.ListFactionsResponse:
        params = {"limit": str(limit), "page": str(page)}
        return await self._request(
            model.ListFactionsResponse,
            "GET",
            "/factions",
            params=params,
        )

    async def get_faction(
        self,
        faction_symbol: model.FactionSymbol,
    ) -> model.GetFactionResponse:
        return await self._request(
            model.GetFactionResponse,
            "GET",
            f"/factions/{faction_symbol}",
        )

    async def list_ships(
        self,
        limit: int = 10,
        page: int = 1,
    ) -> model.ListShipsResponse:
        params = {"limit": str(limit), "page": str(page)}
        return await self._request(
            model.ListShipsResponse,
            "GET",
            "/my/ships",
            params=params,
        )

    async def purchase_ship(
        self,
        ship_type: model.ShipType,
        waypoint_symbol: str,
    ) -> model.PurchaseShipResponse:
        data = {"shipType": ship_type, "waypointSymbol": waypoint_symbol}
        return await self._request(
            model.PurchaseShipResponse,
            "POST",
            "/my/ships",
            data=data,
        )

    async def get_ship(
        self,
        ship_symbol: str,
    ) -> model.GetShipResponse:
        return await self._request(
            model.GetShipResponse,
            "GET",
            f"/my/ships/{ship_symbol}",
        )

    async def get_ship_cargo(
        self,
        ship_symbol: str,
    ) -> model.GetShipCargoResponse:
        return await self._request(
            model.GetShipCargoResponse,
            "GET",
            f"/my/ships/{ship_symbol}/cargo",
        )

    async def orbit_ship(
        self,
        ship_symbol: str,
    ) -> model.OrbitShipResponse:
        return await self._request(
            model.OrbitShipResponse,
            "POST",
            f"/my/ships/{ship_symbol}/orbit",
        )

    async def ship_refine(
        self,
        ship_symbol: str,
        produce: str,
    ) -> model.ShipRefineResponse:
        data = {"produce": produce}
        return await self._request(
            model.ShipRefineResponse,
            "POST",
            f"/my/ships/{ship_symbol}/refine",
            data=data,
        )

    async def create_chart(
        self,
        ship_symbol: str,
    ) -> model.CreateChartResponse:
        return await self._request(
            model.CreateChartResponse,
            "POST",
            f"/my/ships/{ship_symbol}/chart",
        )

    async def get_ship_cooldown(
        self,
        ship_symbol: str,
    ) -> model.GetShipCooldownResponse:
        return await self._request(
            model.GetShipCooldownResponse,
            "GET",
            f"/my/ships/{ship_symbol}/cooldown",
        )

    async def dock_ship(
        self,
        ship_symbol: str,
    ) -> model.DockShipResponse:
        return await self._request(
            model.DockShipResponse,
            "POST",
            f"/my/ships/{ship_symbol}/dock",
        )

    async def create_survey(
        self,
        ship_symbol: str,
    ) -> model.CreateSurveyResponse:
        return await self._request(
            model.CreateSurveyResponse,
            "POST",
            f"/my/ships/{ship_symbol}/survey",
        )

    async def extract_resources(
        self,
        ship_symbol: str,
        survey: model.Survey,
    ) -> model.ExtractResourcesResponse:
        data = {"survey": survey.model_dump()}
        return await self._request(
            model.ExtractResourcesResponse,
            "POST",
            f"/my/ships/{ship_symbol}/extract",
            data=data,
        )

    async def siphon_resources(
        self,
        ship_symbol: str,
    ) -> model.SiphonGasResponse:
        return await self._request(
            model.SiphonGasResponse,
            "POST",
            f"/my/ships/{ship_symbol}/siphon",
        )

    async def extract_resources_with_survey(
        self,
        ship_symbol: str,
        survey: model.Survey,
    ) -> model.ExtractResourcesWithSurveyResponse:
        return await self._request(
            model.ExtractResourcesWithSurveyResponse,
            "POST",
            f"/my/ships/{ship_symbol}/extract/survey",
            data=survey.model_dump(),
        )

    async def jettison_cargo(
        self,
        ship_symbol: str,
        cargo_to_jettison: model.JettisonCargoObject,
    ) -> model.JettisonCargoResponse:
        return await self._request(
            model.JettisonCargoResponse,
            "POST",
            f"/my/ships/{ship_symbol}/jettison",
            data=cargo_to_jettison.model_dump(),
        )

    async def jump_ship(
        self,
        ship_symbol: str,
        waypoint_symbol: str,
    ) -> model.JumpShipResponse:
        return await self._request(
            model.JumpShipResponse,
            "POST",
            f"/my/ships/{ship_symbol}/jump",
            data={"waypointSymbol": waypoint_symbol},
        )

    async def navigate_ship(
        self,
        ship_symbol: str,
        waypoint_symbol: str,
    ) -> model.NavigateShipResponse:
        return await self._request(
            model.NavigateShipResponse,
            "POST",
            f"/my/ships/{ship_symbol}/navigate",
            data={"waypointSymbol": waypoint_symbol},
        )

    async def patch_ship_nav(
        self,
        ship_symbol: str,
        flight_mode: model.ShipNavFlightMode = model.ShipNavFlightMode.CRUISE,
    ) -> model.PatchShipNavResponse:
        return await self._request(
            model.PatchShipNavResponse,
            "PATCH",
            f"/my/ships/{ship_symbol}/nav",
            data={"flightMode": flight_mode},
        )

    async def get_ship_nav(
        self,
        ship_symbol: str,
    ) -> model.GetShipNavResponse:
        return await self._request(
            model.GetShipNavResponse,
            "GET",
            f"/my/ships/{ship_symbol}/nav",
        )

    async def warp_ship(
        self,
        ship_symbol: str,
        waypoint_symbol: str,
    ) -> model.WarpShipResponse:
        return await self._request(
            model.WarpShipResponse,
            "POST",
            f"/my/ships/{ship_symbol}/warp",
            data={"waypointSymbol": waypoint_symbol},
        )

    async def sell_cargo(
        self,
        ship_symbol: str,
        cargo_to_sell: model.SellCargoObject,
    ) -> model.SellCargoResponse:
        return await self._request(
            model.SellCargoResponse,
            "POST",
            f"/my/ships/{ship_symbol}/sell",
            data=cargo_to_sell.model_dump(),
        )

    async def scan_systems(
        self,
        ship_symbol: str,
    ) -> model.ScanSystemsResponse:
        return await self._request(
            model.ScanSystemsResponse,
            "POST",
            f"/my/ships/{ship_symbol}/scan/systems",
        )

    async def scan_waypoints(
        self,
        ship_symbol: str,
    ) -> model.ScanWaypointsResponse:
        return await self._request(
            model.ScanWaypointsResponse,
            "POST",
            f"/my/ships/{ship_symbol}/scan/waypoints",
        )

    async def scan_ships(
        self,
        ship_symbol: str,
    ) -> model.ScanShipsResponse:
        return await self._request(
            model.ScanShipsResponse,
            "POST",
            f"/my/ships/{ship_symbol}/scan/ships",
        )

    async def refuel_ship(
        self,
        ship_symbol: str,
        refuel_object: model.RefuelObject,
    ) -> model.RefuelShipResponse:
        return await self._request(
            model.RefuelShipResponse,
            "POST",
            f"/my/ships/{ship_symbol}/refuel",
            data=refuel_object.model_dump(),
        )

    async def purchase_cargo(
        self,
        ship_symbol: str,
        purchase_object: model.PurchaseCargoObject,
    ) -> model.PurchaseCargoResponse:
        return await self._request(
            model.PurchaseCargoResponse,
            "POST",
            f"/my/ships/{ship_symbol}/purchase",
            data=purchase_object.model_dump(),
        )

    async def transfer_cargo(
        self,
        ship_symbol: str,
        transfer_object: model.TransferCargoObject,
    ) -> model.TransferCargoResponse:
        return await self._request(
            model.TransferCargoResponse,
            "POST",
            f"/my/ships/{ship_symbol}/transfer",
            data=transfer_object.model_dump(),
        )

    async def negotiate_contract(
        self,
        ship_symbol: str,
    ) -> model.NegotiateContractResponse:
        return await self._request(
            model.NegotiateContractResponse,
            "POST",
            f"/my/ships/{ship_symbol}/negotiate/contract",
        )

    async def get_mounts(
        self,
        ship_symbol: str,
    ) -> model.GetMountsResponse:
        return await self._request(
            model.GetMountsResponse,
            "GET",
            f"/my/ships/{ship_symbol}/mounts",
        )

    async def install_mount(
        self,
        ship_symbol: str,
        mount_symbol: str,
    ) -> model.InstallMountResponse:
        return await self._request(
            model.InstallMountResponse,
            "POST",
            f"/my/ships/{ship_symbol}/mounts/install",
            data={"symbol": mount_symbol},
        )

    async def remove_mount(
        self,
        ship_symbol: str,
        mount_symbol: str,
    ) -> model.RemoveMountResponse:
        return await self._request(
            model.RemoveMountResponse,
            "POST",
            f"/my/ships/{ship_symbol}/mounts/remove",
            data={"symbol": mount_symbol},
        )

    async def get_scrap_ship(
        self,
        ship_symbol: str,
    ) -> model.GetScrapShipResponse:
        return await self._request(
            model.GetScrapShipResponse,
            "GET",
            f"/my/ships/{ship_symbol}/scrap",
        )

    async def scrap_ship(
        self,
        ship_symbol: str,
    ) -> model.ScrapShipResponse:
        return await self._request(
            model.ScrapShipResponse,
            "POST",
            f"/my/ships/{ship_symbol}/scrap",
        )

    async def get_repair_ship(
        self,
        ship_symbol: str,
    ) -> model.GetRepairShipResponse:
        return await self._request(
            model.GetRepairShipResponse,
            "GET",
            f"/my/ships/{ship_symbol}/repair",
        )

    async def repair_ship(
        self,
        ship_symbol: str,
    ) -> model.RepairShipResponse:
        return await self._request(
            model.RepairShipResponse,
            "POST",
            f"/my/ships/{ship_symbol}/repair",
        )

    def update_token(
        self,
        token: str,
    ) -> None:
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})
