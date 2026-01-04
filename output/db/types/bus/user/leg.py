from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta
from typing import Optional

from api.db.types.bus.operator import (
   BusOperatorDetails,
)
from api.db.types.bus.journey import (
   BusCallStopDetails,
)
from api.db.types.bus.vehicle import (
   BusVehicleDetails,
)

@dataclass
class BusLegServiceDetails:
    service_id: int
    service_line: Optional[str]
    bus_operator: Optional[BusOperatorDetails]
    outbound_description: Optional[str]
    inbound_description: Optional[str]
    bg_colour: Optional[str]
    fg_colour: Optional[str]


@dataclass
class BusCallDetails:
    bus_call_id: int
    call_index: Optional[int]
    bus_stop: Optional[BusCallStopDetails]
    plan_arr: Optional[datetime]
    act_arr: Optional[datetime]
    plan_dep: Optional[datetime]
    act_dep: Optional[datetime]


@dataclass
class BusLegUserDetails:
    leg_id: int
    service: Optional[BusLegServiceDetails]
    vehicle: Optional[BusVehicleDetails]
    calls: list[BusCallDetails]
    duration: Optional[timedelta]


@dataclass
class InsertBusLegResult:
    bus_leg_id: int