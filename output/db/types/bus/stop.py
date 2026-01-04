from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

@dataclass
class BusStopInData:
    atco_code: str
    naptan_code: str
    stop_name: str
    landmark_name: Optional[str]
    street_name: str
    crossing_name: Optional[str]
    indicator: Optional[str]
    bearing: str
    locality_name: str
    parent_locality_name: Optional[str]
    grandparent_locality_name: Optional[str]
    town_name: Optional[str]
    suburb_name: Optional[str]
    latitude: Optional[Decimal]
    longitude: Optional[Decimal]


@dataclass
class BusStopDetails:
    bus_stop_id: int
    atco_code: str
    naptan_code: str
    stop_name: str
    landmark_name: Optional[str]
    street_name: str
    crossing_name: Optional[str]
    indicator: Optional[str]
    bearing: str
    locality_name: str
    parent_locality_name: Optional[str]
    grandparent_locality_name: Optional[str]
    town_name: Optional[str]
    suburb_name: Optional[str]
    latitude: Optional[Decimal]
    longitude: Optional[Decimal]