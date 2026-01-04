from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

from api.db.types.bus.user.leg import (
   BusCallDetails,
   BusLegServiceDetails,
)
from api.db.types.bus.operator import (
   BusOperatorDetails,
)

@dataclass
class BusVehicleLegDetails:
    leg_id: int
    bus_service: Optional[BusLegServiceDetails]
    board_call: Optional[BusCallDetails]
    alight_call: Optional[BusCallDetails]
    duration: Optional[timedelta]


@dataclass
class BusVehicleUserDetails:
    vehicle_id: int
    identifier: Optional[str]
    name: Optional[str]
    numberplate: Optional[str]
    operator: Optional[BusOperatorDetails]
    legs: list[BusVehicleLegDetails]
    duration: Optional[timedelta]