from __future__ import annotations

from enum import StrEnum

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, RootModel
from pydantic.alias_generators import to_camel


class BaseAPIModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class ActivityLevel(StrEnum):
    WEAK = "WEAK"
    GROWING = "GROWING"
    STRONG = "STRONG"
    RESTRICTED = "RESTRICTED"


class Agent(BaseAPIModel):
    account_id: str | None = Field(
        None,
        alias="accountId",
        description="Account ID that is tied to this agent. Only included on your own agent.",
        min_length=1,
    )
    symbol: str = Field(
        ...,
        description="Symbol of the agent.",
        max_length=14,
        min_length=3,
    )
    headquarters: str = Field(
        ...,
        description="The headquarters of the agent.",
    )
    credits: int = Field(
        ...,
        description="The number of credits the agent has available. Credits can be negative if funds have been overdrawn.",
    )
    starting_faction: str = Field(
        ...,
        alias="startingFaction",
        description="The faction the agent started with.",
        min_length=1,
    )
    ship_count: int = Field(
        ...,
        alias="shipCount",
        description="How many ships are owned by the agent.",
    )


class Type(StrEnum):
    PROCUREMENT = "PROCUREMENT"
    TRANSPORT = "TRANSPORT"
    SHUTTLE = "SHUTTLE"


class ContractDeliverGood(BaseAPIModel):
    trade_symbol: str = Field(
        ...,
        alias="tradeSymbol",
        description="The symbol of the trade good to deliver.",
        min_length=1,
    )
    destination_symbol: str = Field(
        ...,
        alias="destinationSymbol",
        description="The destination where goods need to be delivered.",
        min_length=1,
    )
    units_required: int = Field(
        ...,
        alias="unitsRequired",
        description="The number of units that need to be delivered on this contract.",
    )
    units_fulfilled: int = Field(
        ...,
        alias="unitsFulfilled",
        description="The number of units fulfilled on this contract.",
    )


class ContractPayment(BaseAPIModel):
    on_accepted: int = Field(
        ...,
        alias="onAccepted",
        description="The amount of credits received up front for accepting the contract.",
    )
    on_fulfilled: int = Field(
        ...,
        alias="onFulfilled",
        description="The amount of credits received when the contract is fulfilled.",
    )


class ContractTerms(BaseAPIModel):
    deadline: AwareDatetime = Field(
        ...,
        description="The deadline for the contract.",
    )
    payment: ContractPayment
    deliver: list[ContractDeliverGood] | None = Field(
        None,
        description="The cargo that needs to be delivered to fulfill the contract.",
    )


class Cooldown(BaseAPIModel):
    ship_symbol: str = Field(
        ...,
        alias="shipSymbol",
        description="The symbol of the ship that is on cooldown",
        min_length=1,
    )
    total_seconds: int = Field(
        ...,
        alias="totalSeconds",
        description="The total duration of the cooldown in seconds",
        ge=0,
    )
    remaining_seconds: int = Field(
        ...,
        alias="remainingSeconds",
        description="The remaining duration of the cooldown in seconds",
        ge=0,
    )
    expiration: AwareDatetime | None = Field(
        None,
        description="The date and time when the cooldown expires in ISO 8601 format",
    )


class FactionSymbol(StrEnum):
    COSMIC = "COSMIC"
    VOID = "VOID"
    GALACTIC = "GALACTIC"
    QUANTUM = "QUANTUM"
    DOMINION = "DOMINION"
    ASTRO = "ASTRO"
    CORSAIRS = "CORSAIRS"
    OBSIDIAN = "OBSIDIAN"
    AEGIS = "AEGIS"
    UNITED = "UNITED"
    SOLITARY = "SOLITARY"
    COBALT = "COBALT"
    OMEGA = "OMEGA"
    ECHO = "ECHO"
    LORDS = "LORDS"
    CULT = "CULT"
    ANCIENTS = "ANCIENTS"
    SHADOW = "SHADOW"
    ETHEREAL = "ETHEREAL"


class FactionTraitSymbol(StrEnum):
    BUREAUCRATIC = "BUREAUCRATIC"
    SECRETIVE = "SECRETIVE"
    CAPITALISTIC = "CAPITALISTIC"
    INDUSTRIOUS = "INDUSTRIOUS"
    PEACEFUL = "PEACEFUL"
    DISTRUSTFUL = "DISTRUSTFUL"
    WELCOMING = "WELCOMING"
    SMUGGLERS = "SMUGGLERS"
    SCAVENGERS = "SCAVENGERS"
    REBELLIOUS = "REBELLIOUS"
    EXILES = "EXILES"
    PIRATES = "PIRATES"
    RAIDERS = "RAIDERS"
    CLAN = "CLAN"
    GUILD = "GUILD"
    DOMINION = "DOMINION"
    FRINGE = "FRINGE"
    FORSAKEN = "FORSAKEN"
    ISOLATED = "ISOLATED"
    LOCALIZED = "LOCALIZED"
    ESTABLISHED = "ESTABLISHED"
    NOTABLE = "NOTABLE"
    DOMINANT = "DOMINANT"
    INESCAPABLE = "INESCAPABLE"
    INNOVATIVE = "INNOVATIVE"
    BOLD = "BOLD"
    VISIONARY = "VISIONARY"
    CURIOUS = "CURIOUS"
    DARING = "DARING"
    EXPLORATORY = "EXPLORATORY"
    RESOURCEFUL = "RESOURCEFUL"
    FLEXIBLE = "FLEXIBLE"
    COOPERATIVE = "COOPERATIVE"
    UNITED = "UNITED"
    STRATEGIC = "STRATEGIC"
    INTELLIGENT = "INTELLIGENT"
    RESEARCH_FOCUSED = "RESEARCH_FOCUSED"
    COLLABORATIVE = "COLLABORATIVE"
    PROGRESSIVE = "PROGRESSIVE"
    MILITARISTIC = "MILITARISTIC"
    TECHNOLOGICALLY_ADVANCED = "TECHNOLOGICALLY_ADVANCED"
    AGGRESSIVE = "AGGRESSIVE"
    IMPERIALISTIC = "IMPERIALISTIC"
    TREASURE_HUNTERS = "TREASURE_HUNTERS"
    DEXTEROUS = "DEXTEROUS"
    UNPREDICTABLE = "UNPREDICTABLE"
    BRUTAL = "BRUTAL"
    FLEETING = "FLEETING"
    ADAPTABLE = "ADAPTABLE"
    SELF_SUFFICIENT = "SELF_SUFFICIENT"
    DEFENSIVE = "DEFENSIVE"
    PROUD = "PROUD"
    DIVERSE = "DIVERSE"
    INDEPENDENT = "INDEPENDENT"
    SELF_INTERESTED = "SELF_INTERESTED"
    FRAGMENTED = "FRAGMENTED"
    COMMERCIAL = "COMMERCIAL"
    FREE_MARKETS = "FREE_MARKETS"
    ENTREPRENEURIAL = "ENTREPRENEURIAL"


class Type1(StrEnum):
    EXPORT = "EXPORT"
    IMPORT_ = "IMPORT"
    EXCHANGE = "EXCHANGE"


class Type2(StrEnum):
    PURCHASE = "PURCHASE"
    SELL = "SELL"


class Meta(BaseAPIModel):
    total: int = Field(
        ...,
        description="Shows the total amount of items of this kind that exist.",
        ge=0,
    )
    page: int = Field(
        ...,
        description="A page denotes an amount of items, offset from the first item. Each page holds an amount of items equal to the `limit`.",
        ge=1,
    )
    limit: int = Field(
        ...,
        description="The amount of items in each page. Limits how many items can be fetched at once.",
        ge=1,
        le=20,
    )


class Frame(BaseAPIModel):
    symbol: str = Field(
        ...,
        description="The symbol of the frame.",
    )


class Reactor(BaseAPIModel):
    symbol: str = Field(
        ...,
        description="The symbol of the reactor.",
    )


class Engine(BaseAPIModel):
    symbol: str = Field(
        ...,
        description="The symbol of the engine.",
    )


class Mount(BaseAPIModel):
    symbol: str = Field(
        ...,
        description="The symbol of the mount.",
    )


class ShipComponentCondition(RootModel[float]):
    root: float = Field(
        ...,
        description="The repairable condition of a component. A value of 0 indicates the component needs significant repairs, while a value of 1 indicates the component is in near perfect condition. As the condition of a component is repaired, the overall integrity of the component decreases.",
        ge=0.0,
        le=1.0,
    )


class ShipComponentIntegrity(RootModel[float]):
    root: float = Field(
        ...,
        description="The overall integrity of the component, which determines the performance of the component. A value of 0 indicates that the component is almost completely degraded, while a value of 1 indicates that the component is in near perfect condition. The integrity of the component is non-repairable, and represents permanent wear over time.",
        ge=0.0,
        le=1.0,
    )


class Symbol(StrEnum):
    REACTOR_OVERLOAD = "REACTOR_OVERLOAD"
    ENERGY_SPIKE_FROM_MINERAL = "ENERGY_SPIKE_FROM_MINERAL"
    SOLAR_FLARE_INTERFERENCE = "SOLAR_FLARE_INTERFERENCE"
    COOLANT_LEAK = "COOLANT_LEAK"
    POWER_DISTRIBUTION_FLUCTUATION = "POWER_DISTRIBUTION_FLUCTUATION"
    MAGNETIC_FIELD_DISRUPTION = "MAGNETIC_FIELD_DISRUPTION"
    HULL_MICROMETEORITE_STRIKES = "HULL_MICROMETEORITE_STRIKES"
    STRUCTURAL_STRESS_FRACTURES = "STRUCTURAL_STRESS_FRACTURES"
    CORROSIVE_MINERAL_CONTAMINATION = "CORROSIVE_MINERAL_CONTAMINATION"
    THERMAL_EXPANSION_MISMATCH = "THERMAL_EXPANSION_MISMATCH"
    VIBRATION_DAMAGE_FROM_DRILLING = "VIBRATION_DAMAGE_FROM_DRILLING"
    ELECTROMAGNETIC_FIELD_INTERFERENCE = "ELECTROMAGNETIC_FIELD_INTERFERENCE"
    IMPACT_WITH_EXTRACTED_DEBRIS = "IMPACT_WITH_EXTRACTED_DEBRIS"
    FUEL_EFFICIENCY_DEGRADATION = "FUEL_EFFICIENCY_DEGRADATION"
    COOLANT_SYSTEM_AGEING = "COOLANT_SYSTEM_AGEING"
    DUST_MICROABRASIONS = "DUST_MICROABRASIONS"
    THRUSTER_NOZZLE_WEAR = "THRUSTER_NOZZLE_WEAR"
    EXHAUST_PORT_CLOGGING = "EXHAUST_PORT_CLOGGING"
    BEARING_LUBRICATION_FADE = "BEARING_LUBRICATION_FADE"
    SENSOR_CALIBRATION_DRIFT = "SENSOR_CALIBRATION_DRIFT"
    HULL_MICROMETEORITE_DAMAGE = "HULL_MICROMETEORITE_DAMAGE"
    SPACE_DEBRIS_COLLISION = "SPACE_DEBRIS_COLLISION"
    THERMAL_STRESS = "THERMAL_STRESS"
    VIBRATION_OVERLOAD = "VIBRATION_OVERLOAD"
    PRESSURE_DIFFERENTIAL_STRESS = "PRESSURE_DIFFERENTIAL_STRESS"
    ELECTROMAGNETIC_SURGE_EFFECTS = "ELECTROMAGNETIC_SURGE_EFFECTS"
    ATMOSPHERIC_ENTRY_HEAT = "ATMOSPHERIC_ENTRY_HEAT"


class Component(StrEnum):
    FRAME = "FRAME"
    REACTOR = "REACTOR"
    ENGINE = "ENGINE"


class ShipConditionEvent(BaseAPIModel):
    symbol: Symbol
    component: Component
    name: str = Field(
        ...,
        description="The name of the event.",
    )
    description: str = Field(
        ...,
        description="A description of the event.",
    )


class Rotation(StrEnum):
    STRICT = "STRICT"
    RELAXED = "RELAXED"


class ShipCrew(BaseAPIModel):
    current: int = Field(
        ...,
        description="The current number of crew members on the ship.",
    )
    required: int = Field(
        ...,
        description="The minimum number of crew members required to maintain the ship.",
    )
    capacity: int = Field(
        ...,
        description="The maximum number of crew members the ship can support.",
    )
    rotation: Rotation = Field(
        ...,
        description="The rotation of crew shifts. A stricter shift improves the ship's performance. A more relaxed shift improves the crew's morale.",
    )
    morale: int = Field(
        ...,
        description="A rough measure of the crew's morale. A higher morale means the crew is happier and more productive. A lower morale means the ship is more prone to accidents.",
        ge=0,
        le=100,
    )
    wages: int = Field(
        ...,
        description="The amount of credits per crew member paid per hour. Wages are paid when a ship docks at a civilized waypoint.",
        ge=0,
    )


class Symbol1(StrEnum):
    ENGINE_IMPULSE_DRIVE_I = "ENGINE_IMPULSE_DRIVE_I"
    ENGINE_ION_DRIVE_I = "ENGINE_ION_DRIVE_I"
    ENGINE_ION_DRIVE_II = "ENGINE_ION_DRIVE_II"
    ENGINE_HYPER_DRIVE_I = "ENGINE_HYPER_DRIVE_I"


class Symbol2(StrEnum):
    FRAME_PROBE = "FRAME_PROBE"
    FRAME_DRONE = "FRAME_DRONE"
    FRAME_INTERCEPTOR = "FRAME_INTERCEPTOR"
    FRAME_RACER = "FRAME_RACER"
    FRAME_FIGHTER = "FRAME_FIGHTER"
    FRAME_FRIGATE = "FRAME_FRIGATE"
    FRAME_SHUTTLE = "FRAME_SHUTTLE"
    FRAME_EXPLORER = "FRAME_EXPLORER"
    FRAME_MINER = "FRAME_MINER"
    FRAME_LIGHT_FREIGHTER = "FRAME_LIGHT_FREIGHTER"
    FRAME_HEAVY_FREIGHTER = "FRAME_HEAVY_FREIGHTER"
    FRAME_TRANSPORT = "FRAME_TRANSPORT"
    FRAME_DESTROYER = "FRAME_DESTROYER"
    FRAME_CRUISER = "FRAME_CRUISER"
    FRAME_CARRIER = "FRAME_CARRIER"


class Consumed(BaseAPIModel):
    amount: int = Field(
        ...,
        description="The amount of fuel consumed by the most recent transit or action.",
        ge=0,
    )
    timestamp: AwareDatetime = Field(
        ...,
        description="The time at which the fuel was consumed.",
    )


class ShipFuel(BaseAPIModel):
    current: int = Field(
        ...,
        description="The current amount of fuel in the ship's tanks.",
        ge=0,
    )
    capacity: int = Field(
        ...,
        description="The maximum amount of fuel the ship's tanks can hold.",
        ge=0,
    )
    consumed: Consumed | None = Field(
        None,
        description="An object that only shows up when an action has consumed fuel in the process. Shows the fuel consumption data.",
    )


class ShipModificationTransaction(BaseAPIModel):
    waypoint_symbol: str = Field(
        ...,
        alias="waypointSymbol",
        description="The symbol of the waypoint where the transaction took place.",
    )
    ship_symbol: str = Field(
        ...,
        alias="shipSymbol",
        description="The symbol of the ship that made the transaction.",
    )
    trade_symbol: str = Field(
        ...,
        alias="tradeSymbol",
        description="The symbol of the trade good.",
    )
    total_price: int = Field(
        ...,
        alias="totalPrice",
        description="The total price of the transaction.",
        ge=0,
    )
    timestamp: AwareDatetime = Field(
        ...,
        description="The timestamp of the transaction.",
    )


class Symbol3(StrEnum):
    MODULE_MINERAL_PROCESSOR_I = "MODULE_MINERAL_PROCESSOR_I"
    MODULE_GAS_PROCESSOR_I = "MODULE_GAS_PROCESSOR_I"
    MODULE_CARGO_HOLD_I = "MODULE_CARGO_HOLD_I"
    MODULE_CARGO_HOLD_II = "MODULE_CARGO_HOLD_II"
    MODULE_CARGO_HOLD_III = "MODULE_CARGO_HOLD_III"
    MODULE_CREW_QUARTERS_I = "MODULE_CREW_QUARTERS_I"
    MODULE_ENVOY_QUARTERS_I = "MODULE_ENVOY_QUARTERS_I"
    MODULE_PASSENGER_CABIN_I = "MODULE_PASSENGER_CABIN_I"
    MODULE_MICRO_REFINERY_I = "MODULE_MICRO_REFINERY_I"
    MODULE_ORE_REFINERY_I = "MODULE_ORE_REFINERY_I"
    MODULE_FUEL_REFINERY_I = "MODULE_FUEL_REFINERY_I"
    MODULE_SCIENCE_LAB_I = "MODULE_SCIENCE_LAB_I"
    MODULE_JUMP_DRIVE_I = "MODULE_JUMP_DRIVE_I"
    MODULE_JUMP_DRIVE_II = "MODULE_JUMP_DRIVE_II"
    MODULE_JUMP_DRIVE_III = "MODULE_JUMP_DRIVE_III"
    MODULE_WARP_DRIVE_I = "MODULE_WARP_DRIVE_I"
    MODULE_WARP_DRIVE_II = "MODULE_WARP_DRIVE_II"
    MODULE_WARP_DRIVE_III = "MODULE_WARP_DRIVE_III"
    MODULE_SHIELD_GENERATOR_I = "MODULE_SHIELD_GENERATOR_I"
    MODULE_SHIELD_GENERATOR_II = "MODULE_SHIELD_GENERATOR_II"


class Symbol4(StrEnum):
    MOUNT_GAS_SIPHON_I = "MOUNT_GAS_SIPHON_I"
    MOUNT_GAS_SIPHON_II = "MOUNT_GAS_SIPHON_II"
    MOUNT_GAS_SIPHON_III = "MOUNT_GAS_SIPHON_III"
    MOUNT_SURVEYOR_I = "MOUNT_SURVEYOR_I"
    MOUNT_SURVEYOR_II = "MOUNT_SURVEYOR_II"
    MOUNT_SURVEYOR_III = "MOUNT_SURVEYOR_III"
    MOUNT_SENSOR_ARRAY_I = "MOUNT_SENSOR_ARRAY_I"
    MOUNT_SENSOR_ARRAY_II = "MOUNT_SENSOR_ARRAY_II"
    MOUNT_SENSOR_ARRAY_III = "MOUNT_SENSOR_ARRAY_III"
    MOUNT_MINING_LASER_I = "MOUNT_MINING_LASER_I"
    MOUNT_MINING_LASER_II = "MOUNT_MINING_LASER_II"
    MOUNT_MINING_LASER_III = "MOUNT_MINING_LASER_III"
    MOUNT_LASER_CANNON_I = "MOUNT_LASER_CANNON_I"
    MOUNT_MISSILE_LAUNCHER_I = "MOUNT_MISSILE_LAUNCHER_I"
    MOUNT_TURRET_I = "MOUNT_TURRET_I"


class Deposit(StrEnum):
    QUARTZ_SAND = "QUARTZ_SAND"
    SILICON_CRYSTALS = "SILICON_CRYSTALS"
    PRECIOUS_STONES = "PRECIOUS_STONES"
    ICE_WATER = "ICE_WATER"
    AMMONIA_ICE = "AMMONIA_ICE"
    IRON_ORE = "IRON_ORE"
    COPPER_ORE = "COPPER_ORE"
    SILVER_ORE = "SILVER_ORE"
    ALUMINUM_ORE = "ALUMINUM_ORE"
    GOLD_ORE = "GOLD_ORE"
    PLATINUM_ORE = "PLATINUM_ORE"
    DIAMONDS = "DIAMONDS"
    URANITE_ORE = "URANITE_ORE"
    MERITIUM_ORE = "MERITIUM_ORE"


class ShipNavFlightMode(StrEnum):
    DRIFT = "DRIFT"
    STEALTH = "STEALTH"
    CRUISE = "CRUISE"
    BURN = "BURN"


class ShipNavStatus(StrEnum):
    IN_TRANSIT = "IN_TRANSIT"
    IN_ORBIT = "IN_ORBIT"
    DOCKED = "DOCKED"


class Symbol5(StrEnum):
    REACTOR_SOLAR_I = "REACTOR_SOLAR_I"
    REACTOR_FUSION_I = "REACTOR_FUSION_I"
    REACTOR_FISSION_I = "REACTOR_FISSION_I"
    REACTOR_CHEMICAL_I = "REACTOR_CHEMICAL_I"
    REACTOR_ANTIMATTER_I = "REACTOR_ANTIMATTER_I"


class ShipRequirements(BaseAPIModel):
    power: int | None = Field(
        None,
        description="The amount of power required from the reactor.",
    )
    crew: int | None = Field(
        None,
        description="The number of crew required for operation.",
    )
    slots: int | None = Field(
        None,
        description="The number of module slots required for installation.",
    )


class ShipRole(StrEnum):
    FABRICATOR = "FABRICATOR"
    HARVESTER = "HARVESTER"
    HAULER = "HAULER"
    INTERCEPTOR = "INTERCEPTOR"
    EXCAVATOR = "EXCAVATOR"
    TRANSPORT = "TRANSPORT"
    REPAIR = "REPAIR"
    SURVEYOR = "SURVEYOR"
    COMMAND = "COMMAND"
    CARRIER = "CARRIER"
    PATROL = "PATROL"
    SATELLITE = "SATELLITE"
    EXPLORER = "EXPLORER"
    REFINERY = "REFINERY"


class ShipType(StrEnum):
    SHIP_PROBE = "SHIP_PROBE"
    SHIP_MINING_DRONE = "SHIP_MINING_DRONE"
    SHIP_SIPHON_DRONE = "SHIP_SIPHON_DRONE"
    SHIP_INTERCEPTOR = "SHIP_INTERCEPTOR"
    SHIP_LIGHT_HAULER = "SHIP_LIGHT_HAULER"
    SHIP_COMMAND_FRIGATE = "SHIP_COMMAND_FRIGATE"
    SHIP_EXPLORER = "SHIP_EXPLORER"
    SHIP_HEAVY_FREIGHTER = "SHIP_HEAVY_FREIGHTER"
    SHIP_LIGHT_SHUTTLE = "SHIP_LIGHT_SHUTTLE"
    SHIP_ORE_HOUND = "SHIP_ORE_HOUND"
    SHIP_REFINING_FREIGHTER = "SHIP_REFINING_FREIGHTER"
    SHIP_SURVEYOR = "SHIP_SURVEYOR"


class ShipType1(BaseAPIModel):
    type: ShipType


class Crew(BaseAPIModel):
    required: int
    capacity: int


class SupplyLevel(StrEnum):
    SCARCE = "SCARCE"
    LIMITED = "LIMITED"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    ABUNDANT = "ABUNDANT"


class Size(StrEnum):
    SMALL = "SMALL"
    MODERATE = "MODERATE"
    LARGE = "LARGE"


class SurveyDeposit(BaseAPIModel):
    symbol: str = Field(
        ...,
        description="The symbol of the deposit.",
    )


class SystemFaction(BaseAPIModel):
    symbol: FactionSymbol


class SystemSymbol(RootModel[str]):
    root: str = Field(
        ...,
        description="The symbol of the system.",
        min_length=1,
    )


class SystemType(StrEnum):
    NEUTRON_STAR = "NEUTRON_STAR"
    RED_STAR = "RED_STAR"
    ORANGE_STAR = "ORANGE_STAR"
    BLUE_STAR = "BLUE_STAR"
    YOUNG_STAR = "YOUNG_STAR"
    WHITE_DWARF = "WHITE_DWARF"
    BLACK_HOLE = "BLACK_HOLE"
    HYPERGIANT = "HYPERGIANT"
    NEBULA = "NEBULA"
    UNSTABLE = "UNSTABLE"


class TradeSymbol(StrEnum):
    PRECIOUS_STONES = "PRECIOUS_STONES"
    QUARTZ_SAND = "QUARTZ_SAND"
    SILICON_CRYSTALS = "SILICON_CRYSTALS"
    AMMONIA_ICE = "AMMONIA_ICE"
    LIQUID_HYDROGEN = "LIQUID_HYDROGEN"
    LIQUID_NITROGEN = "LIQUID_NITROGEN"
    ICE_WATER = "ICE_WATER"
    EXOTIC_MATTER = "EXOTIC_MATTER"
    ADVANCED_CIRCUITRY = "ADVANCED_CIRCUITRY"
    GRAVITON_EMITTERS = "GRAVITON_EMITTERS"
    IRON = "IRON"
    IRON_ORE = "IRON_ORE"
    COPPER = "COPPER"
    COPPER_ORE = "COPPER_ORE"
    ALUMINUM = "ALUMINUM"
    ALUMINUM_ORE = "ALUMINUM_ORE"
    SILVER = "SILVER"
    SILVER_ORE = "SILVER_ORE"
    GOLD = "GOLD"
    GOLD_ORE = "GOLD_ORE"
    PLATINUM = "PLATINUM"
    PLATINUM_ORE = "PLATINUM_ORE"
    DIAMONDS = "DIAMONDS"
    URANITE = "URANITE"
    URANITE_ORE = "URANITE_ORE"
    MERITIUM = "MERITIUM"
    MERITIUM_ORE = "MERITIUM_ORE"
    HYDROCARBON = "HYDROCARBON"
    ANTIMATTER = "ANTIMATTER"
    FAB_MATS = "FAB_MATS"
    FERTILIZERS = "FERTILIZERS"
    FABRICS = "FABRICS"
    FOOD = "FOOD"
    JEWELRY = "JEWELRY"
    MACHINERY = "MACHINERY"
    FIREARMS = "FIREARMS"
    ASSAULT_RIFLES = "ASSAULT_RIFLES"
    MILITARY_EQUIPMENT = "MILITARY_EQUIPMENT"
    EXPLOSIVES = "EXPLOSIVES"
    LAB_INSTRUMENTS = "LAB_INSTRUMENTS"
    AMMUNITION = "AMMUNITION"
    ELECTRONICS = "ELECTRONICS"
    SHIP_PLATING = "SHIP_PLATING"
    SHIP_PARTS = "SHIP_PARTS"
    EQUIPMENT = "EQUIPMENT"
    FUEL = "FUEL"
    MEDICINE = "MEDICINE"
    DRUGS = "DRUGS"
    CLOTHING = "CLOTHING"
    MICROPROCESSORS = "MICROPROCESSORS"
    PLASTICS = "PLASTICS"
    POLYNUCLEOTIDES = "POLYNUCLEOTIDES"
    BIOCOMPOSITES = "BIOCOMPOSITES"
    QUANTUM_STABILIZERS = "QUANTUM_STABILIZERS"
    NANOBOTS = "NANOBOTS"
    AI_MAINFRAMES = "AI_MAINFRAMES"
    QUANTUM_DRIVES = "QUANTUM_DRIVES"
    ROBOTIC_DRONES = "ROBOTIC_DRONES"
    CYBER_IMPLANTS = "CYBER_IMPLANTS"
    GENE_THERAPEUTICS = "GENE_THERAPEUTICS"
    NEURAL_CHIPS = "NEURAL_CHIPS"
    MOOD_REGULATORS = "MOOD_REGULATORS"
    VIRAL_AGENTS = "VIRAL_AGENTS"
    MICRO_FUSION_GENERATORS = "MICRO_FUSION_GENERATORS"
    SUPERGRAINS = "SUPERGRAINS"
    LASER_RIFLES = "LASER_RIFLES"
    HOLOGRAPHICS = "HOLOGRAPHICS"
    SHIP_SALVAGE = "SHIP_SALVAGE"
    RELIC_TECH = "RELIC_TECH"
    NOVEL_LIFEFORMS = "NOVEL_LIFEFORMS"
    BOTANICAL_SPECIMENS = "BOTANICAL_SPECIMENS"
    CULTURAL_ARTIFACTS = "CULTURAL_ARTIFACTS"
    FRAME_PROBE = "FRAME_PROBE"
    FRAME_DRONE = "FRAME_DRONE"
    FRAME_INTERCEPTOR = "FRAME_INTERCEPTOR"
    FRAME_RACER = "FRAME_RACER"
    FRAME_FIGHTER = "FRAME_FIGHTER"
    FRAME_FRIGATE = "FRAME_FRIGATE"
    FRAME_SHUTTLE = "FRAME_SHUTTLE"
    FRAME_EXPLORER = "FRAME_EXPLORER"
    FRAME_MINER = "FRAME_MINER"
    FRAME_LIGHT_FREIGHTER = "FRAME_LIGHT_FREIGHTER"
    FRAME_HEAVY_FREIGHTER = "FRAME_HEAVY_FREIGHTER"
    FRAME_TRANSPORT = "FRAME_TRANSPORT"
    FRAME_DESTROYER = "FRAME_DESTROYER"
    FRAME_CRUISER = "FRAME_CRUISER"
    FRAME_CARRIER = "FRAME_CARRIER"
    REACTOR_SOLAR_I = "REACTOR_SOLAR_I"
    REACTOR_FUSION_I = "REACTOR_FUSION_I"
    REACTOR_FISSION_I = "REACTOR_FISSION_I"
    REACTOR_CHEMICAL_I = "REACTOR_CHEMICAL_I"
    REACTOR_ANTIMATTER_I = "REACTOR_ANTIMATTER_I"
    ENGINE_IMPULSE_DRIVE_I = "ENGINE_IMPULSE_DRIVE_I"
    ENGINE_ION_DRIVE_I = "ENGINE_ION_DRIVE_I"
    ENGINE_ION_DRIVE_II = "ENGINE_ION_DRIVE_II"
    ENGINE_HYPER_DRIVE_I = "ENGINE_HYPER_DRIVE_I"
    MODULE_MINERAL_PROCESSOR_I = "MODULE_MINERAL_PROCESSOR_I"
    MODULE_GAS_PROCESSOR_I = "MODULE_GAS_PROCESSOR_I"
    MODULE_CARGO_HOLD_I = "MODULE_CARGO_HOLD_I"
    MODULE_CARGO_HOLD_II = "MODULE_CARGO_HOLD_II"
    MODULE_CARGO_HOLD_III = "MODULE_CARGO_HOLD_III"
    MODULE_CREW_QUARTERS_I = "MODULE_CREW_QUARTERS_I"
    MODULE_ENVOY_QUARTERS_I = "MODULE_ENVOY_QUARTERS_I"
    MODULE_PASSENGER_CABIN_I = "MODULE_PASSENGER_CABIN_I"
    MODULE_MICRO_REFINERY_I = "MODULE_MICRO_REFINERY_I"
    MODULE_SCIENCE_LAB_I = "MODULE_SCIENCE_LAB_I"
    MODULE_JUMP_DRIVE_I = "MODULE_JUMP_DRIVE_I"
    MODULE_JUMP_DRIVE_II = "MODULE_JUMP_DRIVE_II"
    MODULE_JUMP_DRIVE_III = "MODULE_JUMP_DRIVE_III"
    MODULE_WARP_DRIVE_I = "MODULE_WARP_DRIVE_I"
    MODULE_WARP_DRIVE_II = "MODULE_WARP_DRIVE_II"
    MODULE_WARP_DRIVE_III = "MODULE_WARP_DRIVE_III"
    MODULE_SHIELD_GENERATOR_I = "MODULE_SHIELD_GENERATOR_I"
    MODULE_SHIELD_GENERATOR_II = "MODULE_SHIELD_GENERATOR_II"
    MODULE_ORE_REFINERY_I = "MODULE_ORE_REFINERY_I"
    MODULE_FUEL_REFINERY_I = "MODULE_FUEL_REFINERY_I"
    MOUNT_GAS_SIPHON_I = "MOUNT_GAS_SIPHON_I"
    MOUNT_GAS_SIPHON_II = "MOUNT_GAS_SIPHON_II"
    MOUNT_GAS_SIPHON_III = "MOUNT_GAS_SIPHON_III"
    MOUNT_SURVEYOR_I = "MOUNT_SURVEYOR_I"
    MOUNT_SURVEYOR_II = "MOUNT_SURVEYOR_II"
    MOUNT_SURVEYOR_III = "MOUNT_SURVEYOR_III"
    MOUNT_SENSOR_ARRAY_I = "MOUNT_SENSOR_ARRAY_I"
    MOUNT_SENSOR_ARRAY_II = "MOUNT_SENSOR_ARRAY_II"
    MOUNT_SENSOR_ARRAY_III = "MOUNT_SENSOR_ARRAY_III"
    MOUNT_MINING_LASER_I = "MOUNT_MINING_LASER_I"
    MOUNT_MINING_LASER_II = "MOUNT_MINING_LASER_II"
    MOUNT_MINING_LASER_III = "MOUNT_MINING_LASER_III"
    MOUNT_LASER_CANNON_I = "MOUNT_LASER_CANNON_I"
    MOUNT_MISSILE_LAUNCHER_I = "MOUNT_MISSILE_LAUNCHER_I"
    MOUNT_TURRET_I = "MOUNT_TURRET_I"
    SHIP_PROBE = "SHIP_PROBE"
    SHIP_MINING_DRONE = "SHIP_MINING_DRONE"
    SHIP_SIPHON_DRONE = "SHIP_SIPHON_DRONE"
    SHIP_INTERCEPTOR = "SHIP_INTERCEPTOR"
    SHIP_LIGHT_HAULER = "SHIP_LIGHT_HAULER"
    SHIP_COMMAND_FRIGATE = "SHIP_COMMAND_FRIGATE"
    SHIP_EXPLORER = "SHIP_EXPLORER"
    SHIP_HEAVY_FREIGHTER = "SHIP_HEAVY_FREIGHTER"
    SHIP_LIGHT_SHUTTLE = "SHIP_LIGHT_SHUTTLE"
    SHIP_ORE_HOUND = "SHIP_ORE_HOUND"
    SHIP_REFINING_FREIGHTER = "SHIP_REFINING_FREIGHTER"
    SHIP_SURVEYOR = "SHIP_SURVEYOR"


class WaypointFaction(BaseAPIModel):
    symbol: FactionSymbol


class WaypointModifierSymbol(StrEnum):
    STRIPPED = "STRIPPED"
    UNSTABLE = "UNSTABLE"
    RADIATION_LEAK = "RADIATION_LEAK"
    CRITICAL_LIMIT = "CRITICAL_LIMIT"
    CIVIL_UNREST = "CIVIL_UNREST"


class WaypointOrbital(BaseAPIModel):
    symbol: str = Field(
        ...,
        description="The symbol of the orbiting waypoint.",
        min_length=1,
    )


class WaypointSymbol(RootModel[str]):
    root: str = Field(
        ...,
        description="The symbol of the waypoint.",
        min_length=1,
    )


class WaypointTraitSymbol(StrEnum):
    UNCHARTED = "UNCHARTED"
    UNDER_CONSTRUCTION = "UNDER_CONSTRUCTION"
    MARKETPLACE = "MARKETPLACE"
    SHIPYARD = "SHIPYARD"
    OUTPOST = "OUTPOST"
    SCATTERED_SETTLEMENTS = "SCATTERED_SETTLEMENTS"
    SPRAWLING_CITIES = "SPRAWLING_CITIES"
    MEGA_STRUCTURES = "MEGA_STRUCTURES"
    PIRATE_BASE = "PIRATE_BASE"
    OVERCROWDED = "OVERCROWDED"
    HIGH_TECH = "HIGH_TECH"
    CORRUPT = "CORRUPT"
    BUREAUCRATIC = "BUREAUCRATIC"
    TRADING_HUB = "TRADING_HUB"
    INDUSTRIAL = "INDUSTRIAL"
    BLACK_MARKET = "BLACK_MARKET"
    RESEARCH_FACILITY = "RESEARCH_FACILITY"
    MILITARY_BASE = "MILITARY_BASE"
    SURVEILLANCE_OUTPOST = "SURVEILLANCE_OUTPOST"
    EXPLORATION_OUTPOST = "EXPLORATION_OUTPOST"
    MINERAL_DEPOSITS = "MINERAL_DEPOSITS"
    COMMON_METAL_DEPOSITS = "COMMON_METAL_DEPOSITS"
    PRECIOUS_METAL_DEPOSITS = "PRECIOUS_METAL_DEPOSITS"
    RARE_METAL_DEPOSITS = "RARE_METAL_DEPOSITS"
    METHANE_POOLS = "METHANE_POOLS"
    ICE_CRYSTALS = "ICE_CRYSTALS"
    EXPLOSIVE_GASES = "EXPLOSIVE_GASES"
    STRONG_MAGNETOSPHERE = "STRONG_MAGNETOSPHERE"
    VIBRANT_AURORAS = "VIBRANT_AURORAS"
    SALT_FLATS = "SALT_FLATS"
    CANYONS = "CANYONS"
    PERPETUAL_DAYLIGHT = "PERPETUAL_DAYLIGHT"
    PERPETUAL_OVERCAST = "PERPETUAL_OVERCAST"
    DRY_SEABEDS = "DRY_SEABEDS"
    MAGMA_SEAS = "MAGMA_SEAS"
    SUPERVOLCANOES = "SUPERVOLCANOES"
    ASH_CLOUDS = "ASH_CLOUDS"
    VAST_RUINS = "VAST_RUINS"
    MUTATED_FLORA = "MUTATED_FLORA"
    TERRAFORMED = "TERRAFORMED"
    EXTREME_TEMPERATURES = "EXTREME_TEMPERATURES"
    EXTREME_PRESSURE = "EXTREME_PRESSURE"
    DIVERSE_LIFE = "DIVERSE_LIFE"
    SCARCE_LIFE = "SCARCE_LIFE"
    FOSSILS = "FOSSILS"
    WEAK_GRAVITY = "WEAK_GRAVITY"
    STRONG_GRAVITY = "STRONG_GRAVITY"
    CRUSHING_GRAVITY = "CRUSHING_GRAVITY"
    TOXIC_ATMOSPHERE = "TOXIC_ATMOSPHERE"
    CORROSIVE_ATMOSPHERE = "CORROSIVE_ATMOSPHERE"
    BREATHABLE_ATMOSPHERE = "BREATHABLE_ATMOSPHERE"
    THIN_ATMOSPHERE = "THIN_ATMOSPHERE"
    JOVIAN = "JOVIAN"
    ROCKY = "ROCKY"
    VOLCANIC = "VOLCANIC"
    FROZEN = "FROZEN"
    SWAMP = "SWAMP"
    BARREN = "BARREN"
    TEMPERATE = "TEMPERATE"
    JUNGLE = "JUNGLE"
    OCEAN = "OCEAN"
    RADIOACTIVE = "RADIOACTIVE"
    MICRO_GRAVITY_ANOMALIES = "MICRO_GRAVITY_ANOMALIES"
    DEBRIS_CLUSTER = "DEBRIS_CLUSTER"
    DEEP_CRATERS = "DEEP_CRATERS"
    SHALLOW_CRATERS = "SHALLOW_CRATERS"
    UNSTABLE_COMPOSITION = "UNSTABLE_COMPOSITION"
    HOLLOWED_INTERIOR = "HOLLOWED_INTERIOR"
    STRIPPED = "STRIPPED"


class WaypointType(StrEnum):
    PLANET = "PLANET"
    GAS_GIANT = "GAS_GIANT"
    MOON = "MOON"
    ORBITAL_STATION = "ORBITAL_STATION"
    JUMP_GATE = "JUMP_GATE"
    ASTEROID_FIELD = "ASTEROID_FIELD"
    ASTEROID = "ASTEROID"
    ENGINEERED_ASTEROID = "ENGINEERED_ASTEROID"
    ASTEROID_BASE = "ASTEROID_BASE"
    NEBULA = "NEBULA"
    DEBRIS_FIELD = "DEBRIS_FIELD"
    GRAVITY_WELL = "GRAVITY_WELL"
    ARTIFICIAL_GRAVITY_WELL = "ARTIFICIAL_GRAVITY_WELL"
    FUEL_STATION = "FUEL_STATION"


class Chart(BaseAPIModel):
    waypoint_symbol: WaypointSymbol | None = Field(
        None,
        alias="waypointSymbol",
    )
    submitted_by: str | None = Field(
        None,
        alias="submittedBy",
        description="The agent that submitted the chart for this waypoint.",
    )
    submitted_on: AwareDatetime | None = Field(
        None,
        alias="submittedOn",
        description="The time the chart for this waypoint was submitted.",
    )


class ConstructionMaterial(BaseAPIModel):
    trade_symbol: TradeSymbol = Field(
        ...,
        alias="tradeSymbol",
    )
    required: int = Field(
        ...,
        description="The number of units required.",
    )
    fulfilled: int = Field(
        ...,
        description="The number of units fulfilled toward the required amount.",
    )


class Contract(BaseAPIModel):
    id: str = Field(
        ...,
        description="ID of the contract.",
        min_length=1,
    )
    faction_symbol: str = Field(
        ...,
        alias="factionSymbol",
        description="The symbol of the faction that this contract is for.",
        min_length=1,
    )
    type: Type = Field(
        ...,
        description="Type of contract.",
    )
    terms: ContractTerms
    accepted: bool = Field(
        ...,
        description="Whether the contract has been accepted by the agent",
    )
    fulfilled: bool = Field(
        ...,
        description="Whether the contract has been fulfilled",
    )
    expiration: AwareDatetime = Field(
        ...,
        description="Deprecated in favor of deadlineToAccept",
    )
    deadline_to_accept: AwareDatetime | None = Field(
        None,
        alias="deadlineToAccept",
        description="The time at which the contract is no longer available to be accepted",
    )


class ExtractionYield(BaseAPIModel):
    symbol: TradeSymbol
    units: int = Field(
        ...,
        description="The number of units extracted that were placed into the ship's cargo hold.",
    )


class FactionTrait(BaseAPIModel):
    symbol: FactionTraitSymbol
    name: str = Field(
        ...,
        description="The name of the trait.",
    )
    description: str = Field(
        ...,
        description="A description of the trait.",
    )


class JumpGate(BaseAPIModel):
    symbol: WaypointSymbol
    connections: list[str] = Field(
        ...,
        description="All the gates that are connected to this waypoint.",
    )


class MarketTradeGood(BaseAPIModel):
    symbol: TradeSymbol
    type: Type1 = Field(
        ...,
        description="The type of trade good (export, import, or exchange).",
    )
    trade_volume: int = Field(
        ...,
        alias="tradeVolume",
        description="This is the maximum number of units that can be purchased or sold at this market in a single trade for this good. Trade volume also gives an indication of price volatility. A market with a low trade volume will have large price swings, while high trade volume will be more resilient to price changes.",
        ge=1,
    )
    supply: SupplyLevel
    activity: ActivityLevel | None = None
    purchase_price: int = Field(
        ...,
        alias="purchasePrice",
        description="The price at which this good can be purchased from the market.",
        ge=0,
    )
    sell_price: int = Field(
        ...,
        alias="sellPrice",
        description="The price at which this good can be sold to the market.",
        ge=0,
    )


class MarketTransaction(BaseAPIModel):
    waypoint_symbol: WaypointSymbol = Field(
        ...,
        alias="waypointSymbol",
    )
    ship_symbol: str = Field(
        ...,
        alias="shipSymbol",
        description="The symbol of the ship that made the transaction.",
    )
    trade_symbol: str = Field(
        ...,
        alias="tradeSymbol",
        description="The symbol of the trade good.",
    )
    type: Type2 = Field(
        ...,
        description="The type of transaction.",
    )
    units: int = Field(
        ...,
        description="The number of units of the transaction.",
        ge=0,
    )
    price_per_unit: int = Field(
        ...,
        alias="pricePerUnit",
        description="The price per unit of the transaction.",
        ge=0,
    )
    total_price: int = Field(
        ...,
        alias="totalPrice",
        description="The total price of the transaction.",
        ge=0,
    )
    timestamp: AwareDatetime = Field(
        ...,
        description="The timestamp of the transaction.",
    )


class RepairTransaction(BaseAPIModel):
    waypoint_symbol: WaypointSymbol = Field(
        ...,
        alias="waypointSymbol",
    )
    ship_symbol: str = Field(
        ...,
        alias="shipSymbol",
        description="The symbol of the ship.",
    )
    total_price: int = Field(
        ...,
        alias="totalPrice",
        description="The total price of the transaction.",
        ge=0,
    )
    timestamp: AwareDatetime = Field(
        ...,
        description="The timestamp of the transaction.",
    )


class ScannedSystem(BaseAPIModel):
    symbol: str = Field(..., description="Symbol of the system.", min_length=1)
    sector_symbol: str = Field(
        ...,
        alias="sectorSymbol",
        description="Symbol of the system's sector.",
        min_length=1,
    )
    type: SystemType
    x: int = Field(
        ...,
        description="Position in the universe in the x axis.",
    )
    y: int = Field(
        ...,
        description="Position in the universe in the y axis.",
    )
    distance: int = Field(
        ...,
        description="The system's distance from the scanning ship.",
    )


class ScrapTransaction(BaseAPIModel):
    waypoint_symbol: WaypointSymbol = Field(
        ...,
        alias="waypointSymbol",
    )
    ship_symbol: str = Field(
        ...,
        alias="shipSymbol",
        description="The symbol of the ship.",
    )
    total_price: int = Field(
        ...,
        alias="totalPrice",
        description="The total price of the transaction.",
        ge=0,
    )
    timestamp: AwareDatetime = Field(
        ...,
        description="The timestamp of the transaction.",
    )


class ShipCargoItem(BaseAPIModel):
    symbol: TradeSymbol
    name: str = Field(
        ...,
        description="The name of the cargo item type.",
    )
    description: str = Field(
        ...,
        description="The description of the cargo item type.",
    )
    units: int = Field(
        ...,
        description="The number of units of the cargo item.",
        ge=1,
    )


class ShipEngine(BaseAPIModel):
    symbol: Symbol1 = Field(
        ...,
        description="The symbol of the engine.",
    )
    name: str = Field(
        ...,
        description="The name of the engine.",
    )
    description: str = Field(
        ...,
        description="The description of the engine.",
    )
    condition: ShipComponentCondition
    integrity: ShipComponentIntegrity
    speed: int = Field(
        ...,
        description="The speed stat of this engine. The higher the speed, the faster a ship can travel from one point to another. Reduces the time of arrival when navigating the ship.",
        ge=1,
    )
    requirements: ShipRequirements


class ShipFrame(BaseAPIModel):
    symbol: Symbol2 = Field(
        ...,
        description="Symbol of the frame.",
    )
    name: str = Field(
        ...,
        description="Name of the frame.",
    )
    description: str = Field(
        ...,
        description="Description of the frame.",
    )
    condition: ShipComponentCondition
    integrity: ShipComponentIntegrity
    module_slots: int = Field(
        ...,
        alias="moduleSlots",
        description="The amount of slots that can be dedicated to modules installed in the ship. Each installed module take up a number of slots, and once there are no more slots, no new modules can be installed.",
        ge=0,
    )
    mounting_points: int = Field(
        ...,
        alias="mountingPoints",
        description="The amount of slots that can be dedicated to mounts installed in the ship. Each installed mount takes up a number of points, and once there are no more points remaining, no new mounts can be installed.",
        ge=0,
    )
    fuel_capacity: int = Field(
        ...,
        alias="fuelCapacity",
        description="The maximum amount of fuel that can be stored in this ship. When refueling, the ship will be refueled to this amount.",
        ge=0,
    )
    requirements: ShipRequirements


class ShipModule(BaseAPIModel):
    symbol: Symbol3 = Field(
        ...,
        description="The symbol of the module.",
    )
    capacity: int | None = Field(
        None,
        description="Modules that provide capacity, such as cargo hold or crew quarters will show this value to denote how much of a bonus the module grants.",
        ge=0,
    )
    range: int | None = Field(
        None,
        description="Modules that have a range will such as a sensor array show this value to denote how far can the module reach with its capabilities.",
        ge=0,
    )
    name: str = Field(
        ...,
        description="Name of this module.",
    )
    description: str = Field(
        ...,
        description="Description of this module.",
    )
    requirements: ShipRequirements


class ShipMount(BaseAPIModel):
    symbol: Symbol4 = Field(
        ...,
        description="Symbol of this mount.",
    )
    name: str = Field(
        ...,
        description="Name of this mount.",
    )
    description: str | None = Field(
        None,
        description="Description of this mount.",
    )
    strength: int | None = Field(
        None,
        description="Mounts that have this value, such as mining lasers, denote how powerful this mount's capabilities are.",
        ge=0,
    )
    deposits: list[Deposit] | None = Field(
        None,
        description="Mounts that have this value denote what goods can be produced from using the mount.",
    )
    requirements: ShipRequirements


class ShipNavRouteWaypoint(BaseAPIModel):
    symbol: str = Field(..., description="The symbol of the waypoint.", min_length=1)
    type: WaypointType
    system_symbol: SystemSymbol = Field(
        ...,
        alias="systemSymbol",
    )
    x: int = Field(
        ...,
        description="Position in the universe in the x axis.",
    )
    y: int = Field(
        ...,
        description="Position in the universe in the y axis.",
    )


class ShipReactor(BaseAPIModel):
    symbol: Symbol5 = Field(
        ...,
        description="Symbol of the reactor.",
    )
    name: str = Field(
        ...,
        description="Name of the reactor.",
    )
    description: str = Field(
        ...,
        description="Description of the reactor.",
    )
    condition: ShipComponentCondition
    integrity: ShipComponentIntegrity
    power_output: int = Field(
        ...,
        alias="powerOutput",
        description="The amount of power provided by this reactor. The more power a reactor provides to the ship, the lower the cooldown it gets when using a module or mount that taxes the ship's power.",
        ge=1,
    )
    requirements: ShipRequirements


class ShipRegistration(BaseAPIModel):
    name: str = Field(
        ...,
        description="The agent's registered name of the ship",
        min_length=1,
    )
    faction_symbol: str = Field(
        ...,
        alias="factionSymbol",
        description="The symbol of the faction the ship is registered with",
        min_length=1,
    )
    role: ShipRole


class ShipyardShip(BaseAPIModel):
    type: ShipType
    name: str
    description: str
    supply: SupplyLevel
    activity: ActivityLevel | None = None
    purchase_price: int = Field(
        ...,
        alias="purchasePrice",
    )
    frame: ShipFrame
    reactor: ShipReactor
    engine: ShipEngine
    modules: list[ShipModule]
    mounts: list[ShipMount]
    crew: Crew


class ShipyardTransaction(BaseAPIModel):
    waypoint_symbol: WaypointSymbol = Field(
        ...,
        alias="waypointSymbol",
    )
    ship_symbol: str = Field(
        ...,
        alias="shipSymbol",
        description="The symbol of the ship that was the subject of the transaction.",
    )
    ship_type: str = Field(
        ...,
        alias="shipType",
        description="The symbol of the ship that was the subject of the transaction.",
    )
    price: int = Field(
        ...,
        description="The price of the transaction.",
        ge=0,
    )
    agent_symbol: str = Field(
        ...,
        alias="agentSymbol",
        description="The symbol of the agent that made the transaction.",
    )
    timestamp: AwareDatetime = Field(
        ...,
        description="The timestamp of the transaction.",
    )


class SiphonYield(BaseAPIModel):
    symbol: TradeSymbol
    units: int = Field(
        ...,
        description="The number of units siphoned that were placed into the ship's cargo hold.",
    )


class Survey(BaseAPIModel):
    signature: str = Field(
        ...,
        description="A unique signature for the location of this survey. This signature is verified when attempting an extraction using this survey.",
        min_length=1,
    )
    symbol: str = Field(
        ...,
        description="The symbol of the waypoint that this survey is for.",
        min_length=1,
    )
    deposits: list[SurveyDeposit] = Field(
        ...,
        description="A list of deposits that can be found at this location. A ship will extract one of these deposits when using this survey in an extraction request. If multiple deposits of the same type are present, the chance of extracting that deposit is increased.",
    )
    expiration: AwareDatetime = Field(
        ...,
        description="The date and time when the survey expires. After this date and time, the survey will no longer be available for extraction.",
    )
    size: Size = Field(
        ...,
        description="The size of the deposit. This value indicates how much can be extracted from the survey before it is exhausted.",
    )


class SystemWaypoint(BaseAPIModel):
    symbol: WaypointSymbol
    type: WaypointType
    x: int = Field(
        ...,
        description="Relative position of the waypoint on the system's x axis. This is not an absolute position in the universe.",
    )
    y: int = Field(
        ...,
        description="Relative position of the waypoint on the system's y axis. This is not an absolute position in the universe.",
    )
    orbitals: list[WaypointOrbital] = Field(
        ...,
        description="Waypoints that orbit this waypoint.",
    )
    orbits: str | None = Field(
        None,
        description="The symbol of the parent waypoint, if this waypoint is in orbit around another waypoint. Otherwise this value is undefined.",
        min_length=1,
    )


class TradeGood(BaseAPIModel):
    symbol: TradeSymbol
    name: str = Field(
        ...,
        description="The name of the good.",
    )
    description: str = Field(
        ...,
        description="The description of the good.",
    )


class WaypointModifier(BaseAPIModel):
    symbol: WaypointModifierSymbol
    name: str = Field(
        ...,
        description="The name of the trait.",
    )
    description: str = Field(
        ...,
        description="A description of the trait.",
    )


class WaypointTrait(BaseAPIModel):
    symbol: WaypointTraitSymbol
    name: str = Field(
        ...,
        description="The name of the trait.",
    )
    description: str = Field(
        ...,
        description="A description of the trait.",
    )


class Construction(BaseAPIModel):
    symbol: str = Field(
        ...,
        description="The symbol of the waypoint.",
    )
    materials: list[ConstructionMaterial] = Field(
        ...,
        description="The materials required to construct the waypoint.",
    )
    is_complete: bool = Field(
        ...,
        alias="isComplete",
        description="Whether the waypoint has been constructed.",
    )


class Extraction(BaseAPIModel):
    ship_symbol: str = Field(
        ...,
        alias="shipSymbol",
        description="Symbol of the ship that executed the extraction.",
        min_length=1,
    )
    yield_: ExtractionYield = Field(
        ...,
        alias="yield",
    )


class Faction(BaseAPIModel):
    symbol: FactionSymbol
    name: str = Field(
        ...,
        description="Name of the faction.",
        min_length=1,
    )
    description: str = Field(
        ...,
        description="Description of the faction.",
        min_length=1,
    )
    headquarters: str = Field(
        ...,
        description="The waypoint in which the faction's HQ is located in.",
        min_length=1,
    )
    traits: list[FactionTrait] = Field(
        ...,
        description="list of traits that define this faction.",
    )
    is_recruiting: bool = Field(
        ...,
        alias="isRecruiting",
        description="Whether or not the faction is currently recruiting new agents.",
    )


class Market(BaseAPIModel):
    symbol: str = Field(
        ...,
        description="The symbol of the market. The symbol is the same as the waypoint where the market is located.",
    )
    exports: list[TradeGood] = Field(
        ...,
        description="The list of goods that are exported from this market.",
    )
    imports: list[TradeGood] = Field(
        ...,
        description="The list of goods that are sought as imports in this market.",
    )
    exchange: list[TradeGood] = Field(
        ...,
        description="The list of goods that are bought and sold between agents at this market.",
    )
    transactions: list[MarketTransaction] | None = Field(
        None,
        description="The list of recent transactions at this market. Visible only when a ship is present at the market.",
    )
    trade_goods: list[MarketTradeGood] | None = Field(
        None,
        alias="tradeGoods",
        description="The list of goods that are traded at this market. Visible only when a ship is present at the market.",
    )


class ScannedWaypoint(BaseAPIModel):
    symbol: WaypointSymbol
    type: WaypointType
    system_symbol: SystemSymbol = Field(
        ...,
        alias="systemSymbol",
    )
    x: int = Field(
        ...,
        description="Position in the universe in the x axis.",
    )
    y: int = Field(
        ...,
        description="Position in the universe in the y axis.",
    )
    orbitals: list[WaypointOrbital] = Field(
        ...,
        description="list of waypoints that orbit this waypoint.",
    )
    faction: WaypointFaction | None = None
    traits: list[WaypointTrait] = Field(
        ...,
        description="The traits of the waypoint.",
    )
    chart: Chart | None = None


class ShipCargo(BaseAPIModel):
    capacity: int = Field(
        ...,
        description="The max number of items that can be stored in the cargo hold.",
        ge=0,
    )
    units: int = Field(
        ...,
        description="The number of items currently stored in the cargo hold.",
        ge=0,
    )
    inventory: list[ShipCargoItem | None] = Field(
        ...,
        description="The items currently in the cargo hold.",
    )


class ShipNavRoute(BaseAPIModel):
    destination: ShipNavRouteWaypoint
    origin: ShipNavRouteWaypoint
    departure_time: AwareDatetime = Field(
        ...,
        alias="departureTime",
        description="The date time of the ship's departure.",
    )
    arrival: AwareDatetime = Field(
        ...,
        description="The date time of the ship's arrival. If the ship is in-transit, this is the expected time of arrival.",
    )


class Shipyard(BaseAPIModel):
    symbol: str = Field(
        ...,
        description="The symbol of the shipyard. The symbol is the same as the waypoint where the shipyard is located.",
        min_length=1,
    )
    ship_types: list[ShipType1] = Field(
        ...,
        alias="shipTypes",
        description="The list of ship types available for purchase at this shipyard.",
    )
    transactions: list[ShipyardTransaction] | None = Field(
        None,
        description="The list of recent transactions at this shipyard.",
    )
    ships: list[ShipyardShip] | None = Field(
        None,
        description="The ships that are currently available for purchase at the shipyard.",
    )
    modifications_fee: int = Field(
        ...,
        alias="modificationsFee",
        description="The fee to modify a ship at this shipyard. This includes installing or removing modules and mounts on a ship. In the case of mounts, the fee is a flat rate per mount. In the case of modules, the fee is per slot the module occupies.",
    )


class Siphon(BaseAPIModel):
    ship_symbol: str = Field(
        ...,
        alias="shipSymbol",
        description="Symbol of the ship that executed the siphon.",
        min_length=1,
    )
    yield_: SiphonYield = Field(
        ...,
        alias="yield",
    )


class System(BaseAPIModel):
    symbol: str = Field(
        ...,
        description="The symbol of the system.",
        min_length=1,
    )
    sector_symbol: str = Field(
        ...,
        alias="sectorSymbol",
        description="The symbol of the sector.",
        min_length=1,
    )
    type: SystemType
    x: int = Field(
        ...,
        description="Relative position of the system in the sector in the x axis.",
    )
    y: int = Field(
        ...,
        description="Relative position of the system in the sector in the y axis.",
    )
    waypoints: list[SystemWaypoint] = Field(
        ...,
        description="Waypoints in this system.",
    )
    factions: list[SystemFaction] = Field(
        ...,
        description="Factions that control this system.",
    )


class Waypoint(BaseAPIModel):
    symbol: WaypointSymbol
    type: WaypointType
    system_symbol: SystemSymbol = Field(
        ...,
        alias="systemSymbol",
    )
    x: int = Field(
        ...,
        description="Relative position of the waypoint on the system's x axis. This is not an absolute position in the universe.",
    )
    y: int = Field(
        ...,
        description="Relative position of the waypoint on the system's y axis. This is not an absolute position in the universe.",
    )
    orbitals: list[WaypointOrbital] = Field(
        ...,
        description="Waypoints that orbit this waypoint.",
    )
    orbits: str | None = Field(
        None,
        description="The symbol of the parent waypoint, if this waypoint is in orbit around another waypoint. Otherwise this value is undefined.",
        min_length=1,
    )
    faction: WaypointFaction | None = None
    traits: list[WaypointTrait] = Field(
        ...,
        description="The traits of the waypoint.",
    )
    modifiers: list[WaypointModifier] | None = Field(
        None,
        description="The modifiers of the waypoint.",
    )
    chart: Chart | None = None
    is_under_construction: bool = Field(
        ...,
        alias="isUnderConstruction",
        description="True if the waypoint is under construction.",
    )


class ShipNav(BaseAPIModel):
    system_symbol: SystemSymbol = Field(
        ...,
        alias="systemSymbol",
    )
    waypoint_symbol: WaypointSymbol = Field(
        ...,
        alias="waypointSymbol",
    )
    route: ShipNavRoute
    status: ShipNavStatus
    flight_mode: ShipNavFlightMode = Field(
        ...,
        alias="flightMode",
    )


class ScannedShip(BaseAPIModel):
    symbol: str = Field(
        ...,
        description="The globally unique identifier of the ship.",
    )
    registration: ShipRegistration
    nav: ShipNav
    frame: Frame | None = Field(
        None,
        description="The frame of the ship.",
    )
    reactor: Reactor | None = Field(
        None,
        description="The reactor of the ship.",
    )
    engine: Engine = Field(
        ...,
        description="The engine of the ship.",
    )
    mounts: list[Mount] | None = Field(
        None,
        description="list of mounts installed in the ship.",
    )


class Ship(BaseAPIModel):
    symbol: str = Field(
        ...,
        description="The globally unique identifier of the ship in the following format: `[AGENT_SYMBOL]-[HEX_ID]`",
    )
    registration: ShipRegistration
    nav: ShipNav
    crew: ShipCrew
    frame: ShipFrame
    reactor: ShipReactor
    engine: ShipEngine
    cooldown: Cooldown
    modules: list[ShipModule] = Field(
        ...,
        description="Modules installed in this ship.",
    )
    mounts: list[ShipMount] = Field(
        ...,
        description="Mounts installed in this ship.",
    )
    cargo: ShipCargo
    fuel: ShipFuel


class ServerStats(BaseAPIModel):
    agents: int = Field(
        ...,
        description="Number of registered agents in the game.",
    )
    ships: int = Field(
        ...,
        description="Total number of ships in the game.",
    )
    systems: int = Field(
        ...,
        description="Total number of systems in the game.",
    )
    waypoints: int = Field(
        ...,
        description="Total number of waypoints in the game.",
    )


class CreditLeader(BaseAPIModel):
    agent_symbol: str = Field(
        ...,
        description="Symbol of the agent.",
    )
    credits: int = Field(
        ...,
        description="Amount of credits.",
    )


class ChartLeader(BaseAPIModel):
    agent_symbol: str = Field(
        ...,
        description="Symbol of the agent.",
    )
    chart_count: int = Field(
        ...,
        description="Amount of charts done by the agent.",
    )


class Leaderboards(BaseAPIModel):
    most_credits: list[CreditLeader] = Field(
        ...,
        description="Top agents with the most credits.",
    )
    most_submitted_charts: list[ChartLeader] = Field(
        ...,
        description="Top agents with the most charted submitted.",
    )


class ServerResets(BaseAPIModel):
    next: str = Field(
        ...,
        description="The date and time with the game server will reset",
    )
    frequency: str = Field(
        ...,
        description="How often we intend to reset the game server",
    )


class Announcement(BaseAPIModel):
    title: str
    body: str


class Link(BaseAPIModel):
    name: str
    url: str


class ServerStatsData(BaseAPIModel):
    status: str = Field(
        ...,
        description="The current status of the game server.",
    )
    version: str = Field(
        ...,
        description="The current version of the API.",
    )
    reset_date: str = Field(
        ...,
        description="The date when the game server was last reset.",
    )
    stats: ServerStats
    description: str
    leaderboards: Leaderboards
    server_resets: ServerResets
    announcements: list[Announcement]
    links: list[Link]


class ServerStasResponse(BaseAPIModel):
    data: ServerStatsData


class RegisterNewAgentData(BaseAPIModel):
    agent: Agent = Field(
        ...,
        description="Agent details",
    )
    contract: Contract = Field(
        ...,
        description="Contract details",
    )
    faction: Faction = Field(
        ...,
        description="Faction details",
    )
    ship: Ship = Field(
        ...,
        description="Ship details",
    )
    token: str = Field(
        ...,
        description="A Bearer token for accessing secured API endpoints",
    )


class RegisterNewAgentResponse(BaseAPIModel):
    data: RegisterNewAgentData


class PaginationMetadata(BaseAPIModel):
    total: int = Field(
        ...,
        ge=0,
        description="Shows the total amount of items of this kind that exist.",
    )
    page: int = Field(
        default=1,
        ge=1,
        description="A page denotes an amount of items, offset from the first item.  Each page holds an amount of items equal to the limit.",
    )
    limit: int = Field(
        default=10,
        ge=1,
        le=20,
        description="The amount of items in each page.  Limits how many items can be fetched at once.",
    )


class ListAgentsResponse(BaseAPIModel):
    data: list[Agent]
    meta: PaginationMetadata


class ListContractsResponse(BaseAPIModel):
    data: list[Contract]
    meta: PaginationMetadata


class GetAgentResponse(BaseAPIModel):
    data: Agent


class GetContractResponse(BaseAPIModel):
    data: Contract


class AcceptContractData(BaseAPIModel):
    agent: Agent
    contract: Contract


class AcceptContractResponse(BaseAPIModel):
    data: AcceptContractData


class DeliverCargoToContractData(BaseAPIModel):
    contract: Contract
    cargo: ShipCargo


class DeliverCargoToContractResponse(BaseAPIModel):
    data: DeliverCargoToContractData


class FulfillContractData(BaseAPIModel):
    agent: Agent
    contract: Contract


class FulfillContractResponse(BaseAPIModel):
    data: FulfillContractData


class ListFactionsResponse(BaseAPIModel):
    data: list[Faction]
    meta: PaginationMetadata


class GetFactionResponse(BaseAPIModel):
    data: Faction


class ListShipsResponse(BaseAPIModel):
    data: list[Ship]
    meta: PaginationMetadata


class PurchaseShipData(BaseAPIModel):
    agent: Agent
    ship: Ship
    transaction: ShipyardTransaction


class PurchaseShipResponse(BaseAPIModel):
    data: PurchaseShipData


class GetShipResponse(BaseAPIModel):
    data: Ship


class GetShipCargoResponse(BaseAPIModel):
    data: ShipCargo


class OrbitShipResponse(BaseAPIModel):
    data: ShipNav


class SimpleGoods(BaseAPIModel):
    trade_symbol: TradeSymbol
    units: int


class ShipRefineData(BaseAPIModel):
    cargo: ShipCargo
    cooldown: Cooldown
    produced: list[SimpleGoods]
    consumed: list[SimpleGoods]


class ShipRefineResponse(BaseAPIModel):
    data: ShipRefineData


class CreateChartData(BaseAPIModel):
    chart: Chart
    waypoint: Waypoint


class CreateChartResponse(BaseAPIModel):
    data: CreateChartData


class GetShipCooldownResponse(BaseAPIModel):
    data: Cooldown


class DockShipResponse(BaseAPIModel):
    data: ShipNav


class CreateSurveyData(BaseAPIModel):
    cooldown: Cooldown
    surveys: list[Survey]


class CreateSurveyResponse(BaseAPIModel):
    data: CreateSurveyData


class ExtractResourcesData(BaseAPIModel):
    cooldown: Cooldown
    extraction: Extraction
    cargo: ShipCargo
    events: list[ShipConditionEvent | None]


class ExtractResourcesResponse(BaseAPIModel):
    data: ExtractResourcesData


class SiphonGasData(BaseAPIModel):
    cooldown: Cooldown
    siphon: Siphon
    cargo: ShipCargo
    events: list[ShipConditionEvent | None]


class SiphonGasResponse(BaseAPIModel):
    data: SiphonGasData


class ExtractResourcesWithSurveyData(BaseAPIModel):
    cooldown: Cooldown
    extraction: Extraction
    cargo: ShipCargo
    events: list[ShipConditionEvent | None]


class ExtractResourcesWithSurveyResponse(BaseAPIModel):
    data: ExtractResourcesWithSurveyData


class JettisonCargoResponse(BaseAPIModel):
    data: ShipCargo


class JettisonCargoObject(BaseAPIModel):
    symbol: TradeSymbol
    units: int = Field(
        ...,
        ge=1,
        description="Amount of units to jettison of this good.",
    )


class JumpShipData(BaseAPIModel):
    nav: ShipNav
    cooldown: Cooldown
    transaction: MarketTransaction
    agent: Agent


class JumpShipResponse(BaseAPIModel):
    data: JumpShipData


class NavigateShipData(BaseAPIModel):
    fuel: ShipFuel
    nav: ShipNav
    events: list[ShipConditionEvent | None]


class NavigateShipResponse(BaseAPIModel):
    data: NavigateShipData


class PatchShipNavResponse(BaseAPIModel):
    data: ShipNav


class GetShipNavResponse(BaseAPIModel):
    data: ShipNav


class WarpShipData(BaseAPIModel):
    fuel: ShipFuel
    nav: ShipNav


class WarpShipResponse(BaseAPIModel):
    data: WarpShipData


class SellCargoData(BaseAPIModel):
    agent: Agent
    cargo: ShipCargo
    transaction: MarketTransaction


class ScanSystemsData(BaseAPIModel):
    cooldown: Cooldown
    systems: list[System]


class SellCargoResponse(BaseAPIModel):
    data: SellCargoData


class SellCargoObject(BaseAPIModel):
    symbol: TradeSymbol
    units: int = Field(
        ...,
        ge=1,
        description="Amount of units to sell of the selected good.",
    )


class ScanSystemsResponse(BaseAPIModel):
    data: ScanSystemsData


class ScanWaypointsData(BaseAPIModel):
    cooldown: Cooldown
    waypoints: list[Waypoint]


class ScanWaypointsResponse(BaseAPIModel):
    data: ScanWaypointsData


class ScanShipsData(BaseAPIModel):
    cooldown: Cooldown
    waypoints: list[Ship]


class ScanShipsResponse(BaseAPIModel):
    data: ScanShipsData


class RefuelObject(BaseAPIModel):
    units: int = Field(
        ...,
        ge=1,
        description="The amount of fuel to fill in the ship's tanks. When not specified, the ship will be refueled to its maximum fuel capacity. If the amount specified is greater than the ship's remaining capacity, the ship will only be refueled to its maximum fuel capacity. The amount specified is not in market units but in ship fuel units.",
    )
    from_cargo: bool = Field(
        False,
        description="Whether to use the FUEL that's in your cargo or not. Default: false",
    )


class RefuelShipData(BaseAPIModel):
    agent: Agent
    fuel: ShipFuel
    transaction: MarketTransaction


class RefuelShipResponse(BaseAPIModel):
    data: RefuelShipData


class PurchaseCargoObject(BaseAPIModel):
    symbol: TradeSymbol
    units: int = Field(
        ...,
        description="Amounts of units to purchase.",
    )


class PurchaseCargoData(BaseAPIModel):
    agent: Agent
    cargo: ShipCargo
    transaction: MarketTransaction


class PurchaseCargoResponse(BaseAPIModel):
    data: PurchaseCargoData


class TransferCargoObject(BaseAPIModel):
    trade_symbol: TradeSymbol
    units: int = Field(
        ...,
        description="Amount of units to transfer.",
    )
    ship_symbol: str = Field(
        ...,
        description="The symbol of the ship to transfer to.",
    )


class TransferCargoData(BaseAPIModel):
    cargo: ShipCargo


class TransferCargoResponse(BaseAPIModel):
    data: TransferCargoData


class NegotiateContractResponse(BaseAPIModel):
    data: Contract


class GetMountsResponse(BaseAPIModel):
    data: list[ShipMount]


class InstallMountData(BaseAPIModel):
    agent: Agent
    mounts: list[ShipMount]
    cargo: ShipCargo
    transaction: ShipModificationTransaction


class InstallMountResponse(BaseAPIModel):
    data: InstallMountData


class RemoveMountData(BaseAPIModel):
    agent: Agent
    mounts: list[ShipMount]
    cargo: ShipCargo
    transaction: ShipModificationTransaction


class RemoveMountResponse(BaseAPIModel):
    data: RemoveMountData


class GetScrapShipData(BaseAPIModel):
    transaction: ScrapTransaction


class GetScrapShipResponse(BaseAPIModel):
    data: GetScrapShipData


class ScrapShipData(BaseAPIModel):
    agent: Agent
    transaction: ScrapTransaction


class ScrapShipResponse(BaseAPIModel):
    data: ScrapShipData


class GetRepairShipData(BaseAPIModel):
    transaction: RepairTransaction


class GetRepairShipResponse(BaseAPIModel):
    data: GetRepairShipData


class RepairShipData(BaseAPIModel):
    agent: Agent
    ship: Ship
    transaction: RepairTransaction


class RepairShipResponse(BaseAPIModel):
    data: RepairShipData


class ListSystemsResponse(BaseAPIModel):
    data: list[System]
    meta: PaginationMetadata


class GetSystemResponse(BaseAPIModel):
    data: System


class ListWaypointsInSystemResponse(BaseAPIModel):
    data: list[Waypoint]
    meta: PaginationMetadata


class ListWaypointsInSystemParameters(BaseAPIModel):
    limit: int = Field(
        10,
        ge=1,
        le=20,
        description="How many entries to return per page",
    )
    page: int = Field(
        1,
        ge=1,
        description="What entry offset to request",
    )
    traits: WaypointTraitSymbol | list[WaypointTraitSymbol]
    type: WaypointType


class PaginationParameters(BaseAPIModel):
    limit: int = Field(
        10,
        ge=1,
        le=20,
        description="How many entries to return per page",
    )
    page: int = Field(
        1,
        ge=1,
        description="What entry offset to request",
    )


class GetWaypointResponse(BaseAPIModel):
    data: Waypoint


class GetMarketResponse(BaseAPIModel):
    data: Market


class GetShipyardResponse(BaseAPIModel):
    data: Shipyard


class GetJumpGateResponse(BaseAPIModel):
    data: JumpGate


class GetConstructionSiteResponse(BaseAPIModel):
    data: Construction


class SupplyConstructionSiteData(BaseAPIModel):
    construction: Construction
    cargo: ShipCargo


class SupplyConstructionSiteResponse(BaseAPIModel):
    data: SupplyConstructionSiteData


class SupplyConstructionSiteObject(BaseAPIModel):
    ship_symbol: str = Field(
        ...,
        description="Symbol of the ship to use",
    )
    trade_symbol: str = Field(
        ...,
        description="The symbol of the good to supply.",
    )
    units: int = Field(
        ...,
        description="Amount of units to supply.",
    )
