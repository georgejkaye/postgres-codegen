from dataclasses import dataclass
from typing import Optional

from api.db.types.bus.operator import (
   BusOperatorDetails,
)

@dataclass
class BusModelInData:
    model_name: str


@dataclass
class BusVehicleInData:
    operator_id: int
    vehicle_identifier: Optional[str]
    bustimes_id: Optional[str]
    vehicle_numberplate: str
    vehicle_model: Optional[str]
    vehicle_livery_style: Optional[str]
    vehicle_name: Optional[str]


@dataclass
class BusVehicleDetails:
    bus_vehicle_id: int
    bus_operator: Optional[BusOperatorDetails]
    vehicle_identifier: Optional[str]
    bustimes_id: Optional[str]
    vehicle_numberplate: str
    vehicle_model: Optional[str]
    vehicle_livery_style: Optional[str]
    vehicle_name: Optional[str]