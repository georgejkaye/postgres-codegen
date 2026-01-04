from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from api.db.types.bus.operator import (
   BusOperatorDetails,
)
from api.db.types.bus.vehicle import (
   BusVehicleDetails,
)

@dataclass
class BusCallInData:
    call_index: int
    stop_name: str
    stop_atco: str
    plan_arr: Optional[datetime]
    act_arr: Optional[datetime]
    plan_dep: Optional[datetime]
    act_dep: Optional[datetime]


@dataclass
class BusJourneyInData:
    bustimes_id: int
    service_id: int
    journey_calls: list[BusCallInData]
    vehicle_id: Optional[int]


@dataclass
class BusJourneyServiceDetails:
    service_id: int
    service_operator: Optional[BusOperatorDetails]
    service_line: str
    bg_colour: Optional[str]
    fg_colour: Optional[str]


@dataclass
class BusCallStopDetails:
    bus_stop_id: Optional[int]
    stop_atco: Optional[str]
    stop_name: Optional[str]
    stop_locality: Optional[str]
    stop_street: Optional[str]
    stop_indicator: Optional[str]


@dataclass
class BusJourneyCallDetails:
    call_id: int
    call_index: Optional[int]
    bus_stop: Optional[BusCallStopDetails]
    plan_arr: Optional[datetime]
    act_arr: Optional[datetime]
    plan_dep: Optional[datetime]
    act_dep: Optional[datetime]


@dataclass
class BusJourneyDetails:
    journey_id: int
    journey_service: Optional[BusJourneyServiceDetails]
    journey_calls: list[BusJourneyCallDetails]
    journey_vehicle: Optional[BusVehicleDetails]