from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from api.db.types.bus.user.leg import (
   BusCallDetails,
   BusLegServiceDetails,
)

@dataclass
class BusStopLegDetails:
    leg_id: int
    bus_service: Optional[BusLegServiceDetails]
    board_call: Optional[BusCallDetails]
    alight_call: Optional[BusCallDetails]
    this_call: Optional[BusCallDetails]
    stops_before: Optional[int]
    stops_after: Optional[int]


@dataclass
class BusStopUserDetails:
    stop_id: int
    atco_code: Optional[str]
    naptan_code: Optional[str]
    stop_name: Optional[str]
    landmark_name: Optional[str]
    street_name: Optional[str]
    crossing_name: Optional[str]
    indicator: Optional[str]
    bearing: Optional[str]
    locality_name: Optional[str]
    parent_locality_name: Optional[str]
    grandparent_locality_name: Optional[str]
    town_name: Optional[str]
    suburb_name: Optional[str]
    latitude: Optional[Decimal]
    longitude: Optional[Decimal]
    stop_legs: list[BusStopLegDetails]