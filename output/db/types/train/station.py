from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

@dataclass
class TrainStationNamePointInData:
    station_name: str
    platform: Optional[str]


@dataclass
class TrainStationOutData:
    station_id: int
    station_crs: str
    station_name: str
    operator_id: int
    brand_id: Optional[int]


@dataclass
class TrainStationLegNamesInData:
    station_names: list[str]


@dataclass
class TrainStationPointOutData:
    platform: Optional[str]
    latitude: Decimal
    longitude: Decimal


@dataclass
class TrainStationPointsOutData:
    station_id: int
    station_crs: str
    station_name: str
    search_name: str
    platform_points: list[TrainStationPointOutData]


@dataclass
class TrainStationLegPointsOutData:
    leg_stations: list[TrainStationPointsOutData]


@dataclass
class TrainStationHighOutData:
    station_id: int
    station_crs: str
    station_name: str