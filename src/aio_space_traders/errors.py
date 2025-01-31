from typing import Any


class SpaceTradersAPIError(Exception):
    def __init__(
        self,
        status_code: int | None,
        error_code: int,
        error_message: str,
        data: dict[str, Any],
    ) -> None:
        if status_code == error_code:
            super().__init__(f"{{{status_code}}}: {error_message}")
        else:
            super().__init__(f"{{{status_code}}} ({error_code}): {error_message}")
        self.status_code = status_code
        self.error_code = error_code
        self.error_message = error_message
        self.data = data


# General Error Codes
class CooldownConflictError(SpaceTradersAPIError):
    """Error Code: 4000"""


class WaypointNoAccessError(SpaceTradersAPIError):
    """Error Code: 4001"""


# Account Error Codes
class TokenEmptyError(SpaceTradersAPIError):
    """Error Code: 4100"""


class TokenMissingSubjectError(SpaceTradersAPIError):
    """Error Code: 4101"""


class TokenInvalidSubjectError(SpaceTradersAPIError):
    """Error Code: 4102"""


class MissingTokenRequestError(SpaceTradersAPIError):
    """Error Code: 4103"""


class InvalidTokenRequestError(SpaceTradersAPIError):
    """Error Code: 4104"""


class InvalidTokenSubjectError(SpaceTradersAPIError):
    """Error Code: 4105"""


class AccountNotExistsError(SpaceTradersAPIError):
    """Error Code: 4106"""


class AgentNotExistsError(SpaceTradersAPIError):
    """Error Code: 4107"""


class AccountHasNoAgentError(SpaceTradersAPIError):
    """Error Code: 4108"""


class RegisterAgentExistsError(SpaceTradersAPIError):
    """Error Code: 4109"""


class RegisterAgentSymbolReservedError(SpaceTradersAPIError):
    """Error Code: 4110"""


class RegisterAgentConflictsSymbolError(SpaceTradersAPIError):
    """Error Code: 4111"""


# Ship Error Codes
class NavigateInTransitError(SpaceTradersAPIError):
    """Error Code: 4200"""


class NavigateInvalidDestinationError(SpaceTradersAPIError):
    """Error Code: 4201"""


class NavigateOutsideSystemError(SpaceTradersAPIError):
    """Error Code: 4202"""


class NavigateInsufficientFuelError(SpaceTradersAPIError):
    """Error Code: 4203"""


class NavigateSameDestinationError(SpaceTradersAPIError):
    """Error Code: 4204"""


class ShipExtractInvalidWaypointError(SpaceTradersAPIError):
    """Error Code: 4205"""


class ShipExtractPermissionError(SpaceTradersAPIError):
    """Error Code: 4206"""


class ShipJumpNoSystemError(SpaceTradersAPIError):
    """Error Code: 4207"""


class ShipJumpSameSystemError(SpaceTradersAPIError):
    """Error Code: 4208"""


class ShipJumpMissingModuleError(SpaceTradersAPIError):
    """Error Code: 4210"""


class ShipJumpNoValidWaypointError(SpaceTradersAPIError):
    """Error Code: 4211"""


class ShipJumpMissingAntimatterError(SpaceTradersAPIError):
    """Error Code: 4212"""


class ShipInTransitError(SpaceTradersAPIError):
    """Error Code: 4214"""


class ShipMissingSensorArraysError(SpaceTradersAPIError):
    """Error Code: 4215"""


class PurchaseShipCreditsError(SpaceTradersAPIError):
    """Error Code: 4216"""


class ShipCargoExceedsLimitError(SpaceTradersAPIError):
    """Error Code: 4217"""


class ShipCargoMissingError(SpaceTradersAPIError):
    """Error Code: 4218"""


class ShipCargoUnitCountError(SpaceTradersAPIError):
    """Error Code: 4219"""


class ShipSurveyVerificationError(SpaceTradersAPIError):
    """Error Code: 4220"""


class ShipSurveyExpirationError(SpaceTradersAPIError):
    """Error Code: 4221"""


class ShipSurveyWaypointTypeError(SpaceTradersAPIError):
    """Error Code: 4222"""


class ShipSurveyOrbitError(SpaceTradersAPIError):
    """Error Code: 4223"""


class ShipSurveyExhaustedError(SpaceTradersAPIError):
    """Error Code: 4224"""


class ShipRefuelDockedError(SpaceTradersAPIError):
    """Error Code: 4225"""


class ShipRefuelInvalidWaypointError(SpaceTradersAPIError):
    """Error Code: 4226"""


class ShipMissingMountsError(SpaceTradersAPIError):
    """Error Code: 4227 and 4251"""


class ShipCargoFullError(SpaceTradersAPIError):
    """Error Code: 4228"""


class ShipJumpFromGateToGateError(SpaceTradersAPIError):
    """Error Code: 4229"""


class WaypointChartedError(SpaceTradersAPIError):
    """Error Code: 4230"""


class ShipTransferShipNotFound(SpaceTradersAPIError):
    """Error Code: 4231"""


class ShipTransferAgentConflict(SpaceTradersAPIError):
    """Error Code: 4232"""


class ShipTransferSameShipConflict(SpaceTradersAPIError):
    """Error Code: 4233"""


class ShipTransferLocationConflict(SpaceTradersAPIError):
    """Error Code: 4234"""


class WarpInsideSystemError(SpaceTradersAPIError):
    """Error Code: 4235"""


class ShipNotInOrbitError(SpaceTradersAPIError):
    """Error Code: 4236"""


class ShipInvalidRefineryGoodError(SpaceTradersAPIError):
    """Error Code: 4237"""


class ShipInvalidRefineryTypeError(SpaceTradersAPIError):
    """Error Code: 4238"""


class ShipMissingRefineryError(SpaceTradersAPIError):
    """Error Code: 4239"""


class ShipMissingSurveyorError(SpaceTradersAPIError):
    """Error Code: 4240"""


class ShipMissingWarpDriveError(SpaceTradersAPIError):
    """Error Code: 4241"""


class ShipMissingMineralProcessorError(SpaceTradersAPIError):
    """Error Code: 4242"""


class ShipMissingMiningLasersError(SpaceTradersAPIError):
    """Error Code: 4243"""


class ShipNotDockedError(SpaceTradersAPIError):
    """Error Code: 4244"""


class PurchaseShipNotPresentError(SpaceTradersAPIError):
    """Error Code: 4245"""


class ShipMountNoShipyardError(SpaceTradersAPIError):
    """Error Code: 4246"""


class ShipMissingMountError(SpaceTradersAPIError):
    """Error Code: 4247"""


class ShipMountInsufficientCreditsError(SpaceTradersAPIError):
    """Error Code: 4248"""


class ShipMissingPowerError(SpaceTradersAPIError):
    """Error Code: 4249"""


class ShipMissingSlotsError(SpaceTradersAPIError):
    """Error Code: 4250"""


class ShipMissingCrewError(SpaceTradersAPIError):
    """Error Code: 4252"""


class ShipExtractDestabilizedError(SpaceTradersAPIError):
    """Error Code: 4253"""


class ShipJumpInvalidOriginError(SpaceTradersAPIError):
    """Error Code: 4254"""


class ShipJumpInvalidWaypointError(SpaceTradersAPIError):
    """Error Code: 4255"""


class ShipJumpOriginUnderConstructionError(SpaceTradersAPIError):
    """Error Code: 4256"""


class ShipMissingGasProcessorError(SpaceTradersAPIError):
    """Error Code: 4257"""


class ShipMissingGasSiphonsError(SpaceTradersAPIError):
    """Error Code: 4258"""


class ShipSiphonInvalidWaypointError(SpaceTradersAPIError):
    """Error Code: 4259"""


class ShipSiphonPermissionError(SpaceTradersAPIError):
    """Error Code: 4260"""


class WaypointNoYieldError(SpaceTradersAPIError):
    """Error Code: 4261"""


class ShipJumpDestinationUnderConstructionError(SpaceTradersAPIError):
    """Error Code: 4262"""


# Contract Error Codes
class AcceptContractNotAuthorizedError(SpaceTradersAPIError):
    """Error Code: 4500"""


class AcceptContractConflictError(SpaceTradersAPIError):
    """Error Code: 4501"""


class FulfillContractDeliveryError(SpaceTradersAPIError):
    """Error Code: 4502"""


class ContractDeadlineError(SpaceTradersAPIError):
    """Error Code: 4503"""


class ContractFulfilledError(SpaceTradersAPIError):
    """Error Code: 4504"""


class ContractNotAcceptedError(SpaceTradersAPIError):
    """Error Code: 4505"""


class ContractNotAuthorizedError(SpaceTradersAPIError):
    """Error Code: 4506"""


class ShipDeliverTermsError(SpaceTradersAPIError):
    """Error Code: 4508"""


class ShipDeliverFulfilledError(SpaceTradersAPIError):
    """Error Code: 4509"""


class ShipDeliverInvalidLocationError(SpaceTradersAPIError):
    """Error Code: 4510"""


class ExistingContractError(SpaceTradersAPIError):
    """Error Code: 4511"""


# Market Error Codes
class MarketTradeInsufficientCreditsError(SpaceTradersAPIError):
    """Error Code: 4600"""


class MarketTradeNoPurchaseError(SpaceTradersAPIError):
    """Error Code: 4601"""


class MarketTradeNotSoldError(SpaceTradersAPIError):
    """Error Code: 4602"""


class MarketNotFoundError(SpaceTradersAPIError):
    """Error Code: 4603"""


class MarketTradeUnitLimitError(SpaceTradersAPIError):
    """Error Code: 4604"""


# Faction Error Codes
class WaypointNoFactionError(SpaceTradersAPIError):
    """Error Code: 4700"""


# Construction Error Code
class ConstructionMaterialNotRequired(SpaceTradersAPIError):
    """Error Code: 4800"""


class ConstructionMaterialFulfilled(SpaceTradersAPIError):
    """Error Code: 4801"""


class ShipConstructionInvalidLocationError(SpaceTradersAPIError):
    """Error Code: 4802"""


ERROR_MAPPING: dict[int, type[SpaceTradersAPIError]] = {
    4000: CooldownConflictError,
    4001: WaypointNoAccessError,
    4100: TokenEmptyError,
    4101: TokenMissingSubjectError,
    4102: TokenInvalidSubjectError,
    4103: MissingTokenRequestError,
    4104: InvalidTokenRequestError,
    4105: InvalidTokenSubjectError,
    4106: AccountNotExistsError,
    4107: AgentNotExistsError,
    4108: AccountHasNoAgentError,
    4109: RegisterAgentExistsError,
    4110: RegisterAgentSymbolReservedError,
    4111: RegisterAgentConflictsSymbolError,
    4200: NavigateInTransitError,
    4201: NavigateInvalidDestinationError,
    4202: NavigateOutsideSystemError,
    4203: NavigateInsufficientFuelError,
    4204: NavigateSameDestinationError,
    4205: ShipExtractInvalidWaypointError,
    4206: ShipExtractPermissionError,
    4207: ShipJumpNoSystemError,
    4208: ShipJumpSameSystemError,
    4210: ShipJumpMissingModuleError,
    4211: ShipJumpNoValidWaypointError,
    4212: ShipJumpMissingAntimatterError,
    4214: ShipInTransitError,
    4215: ShipMissingSensorArraysError,
    4216: PurchaseShipCreditsError,
    4217: ShipCargoExceedsLimitError,
    4218: ShipCargoMissingError,
    4219: ShipCargoUnitCountError,
    4220: ShipSurveyVerificationError,
    4221: ShipSurveyExpirationError,
    4222: ShipSurveyWaypointTypeError,
    4223: ShipSurveyOrbitError,
    4224: ShipSurveyExhaustedError,
    4225: ShipRefuelDockedError,
    4226: ShipRefuelInvalidWaypointError,
    4227: ShipMissingMountsError,
    4228: ShipCargoFullError,
    4229: ShipJumpFromGateToGateError,
    4230: WaypointChartedError,
    4231: ShipTransferShipNotFound,
    4232: ShipTransferAgentConflict,
    4233: ShipTransferSameShipConflict,
    4234: ShipTransferLocationConflict,
    4235: WarpInsideSystemError,
    4236: ShipNotInOrbitError,
    4237: ShipInvalidRefineryGoodError,
    4238: ShipInvalidRefineryTypeError,
    4239: ShipMissingRefineryError,
    4240: ShipMissingSurveyorError,
    4241: ShipMissingWarpDriveError,
    4242: ShipMissingMineralProcessorError,
    4243: ShipMissingMiningLasersError,
    4244: ShipNotDockedError,
    4245: PurchaseShipNotPresentError,
    4246: ShipMountNoShipyardError,
    4247: ShipMissingMountError,
    4248: ShipMountInsufficientCreditsError,
    4249: ShipMissingPowerError,
    4250: ShipMissingSlotsError,
    4251: ShipMissingMountsError,
    4252: ShipMissingCrewError,
    4253: ShipExtractDestabilizedError,
    4254: ShipJumpInvalidOriginError,
    4255: ShipJumpInvalidWaypointError,
    4256: ShipJumpOriginUnderConstructionError,
    4257: ShipMissingGasProcessorError,
    4258: ShipMissingGasSiphonsError,
    4259: ShipSiphonInvalidWaypointError,
    4260: ShipSiphonPermissionError,
    4261: WaypointNoYieldError,
    4262: ShipJumpDestinationUnderConstructionError,
    4500: AcceptContractNotAuthorizedError,
    4501: AcceptContractConflictError,
    4502: FulfillContractDeliveryError,
    4503: ContractDeadlineError,
    4504: ContractFulfilledError,
    4505: ContractNotAcceptedError,
    4506: ContractNotAuthorizedError,
    4508: ShipDeliverTermsError,
    4509: ShipDeliverFulfilledError,
    4510: ShipDeliverInvalidLocationError,
    4511: ExistingContractError,
    4600: MarketTradeInsufficientCreditsError,
    4601: MarketTradeNoPurchaseError,
    4602: MarketTradeNotSoldError,
    4603: MarketNotFoundError,
    4604: MarketTradeUnitLimitError,
    4700: WaypointNoFactionError,
    4800: ConstructionMaterialNotRequired,
    4801: ConstructionMaterialFulfilled,
    4802: ShipConstructionInvalidLocationError,
}
