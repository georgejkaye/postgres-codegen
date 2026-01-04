from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta
from decimal import Decimal
from typing import Optional

from api.db.types.train.station import (
   TrainStationHighOutData,
)
from api.db.types.train.operator import (
   TrainOperatorHighOutData,
)

@dataclass
class TransportUserTrainLegUnitSegmentOutData:
    start_station: TrainStationHighOutData
    plan_dep: Optional[datetime]
    act_dep: Optional[datetime]
    end_station: TrainStationHighOutData
    plan_arr: Optional[datetime]
    act_arr: Optional[datetime]


@dataclass
class TransportUserTrainClassLegUnitOutData:
    stock_number: Optional[int]
    stock_subclass: Optional[int]
    stock_cars: Optional[int]
    segments: list[TransportUserTrainLegUnitSegmentOutData]
    duration: Optional[timedelta]
    distance: Optional[Decimal]


@dataclass
class TransportUserTrainClassLegOutData:
    leg_id: int
    leg_start: datetime
    board: TrainStationHighOutData
    alight: TrainStationHighOutData
    operator: Optional[TrainOperatorHighOutData]
    brand: Optional[TrainOperatorHighOutData]
    units: list[TransportUserTrainClassLegUnitOutData]
    distance: Optional[Decimal]
    duration: Optional[timedelta]


@dataclass
class TransportUserTrainClassOutData:
    class_no: int
    class_name: Optional[str]
    class_count: int
    distance: Optional[Decimal]
    duration: timedelta
    class_legs: list[TransportUserTrainClassLegOutData]


@dataclass
class TransportUserTrainClassHighOutData:
    class_no: int
    class_name: Optional[str]
    class_count: int
    distance: Optional[Decimal]
    duration: timedelta


@dataclass
class TransportUserTrainUnitLegOutData:
    leg_id: int
    leg_start: datetime
    board: TrainStationHighOutData
    alight: TrainStationHighOutData
    operator: Optional[TrainOperatorHighOutData]
    brand: Optional[TrainOperatorHighOutData]
    segments: list[TransportUserTrainLegUnitSegmentOutData]
    distance: Optional[Decimal]
    duration: Optional[timedelta]


@dataclass
class TransportUserTrainUnitOutData:
    unit_number: int
    unit_class: int
    unit_subclass: Optional[int]
    unit_cars: Optional[int]
    unit_count: int
    distance: Optional[Decimal]
    duration: timedelta
    unit_legs: list[TransportUserTrainUnitLegOutData]


@dataclass
class TransportUserTrainUnitHighOutData:
    unit_number: int
    unit_class: int
    unit_subclass: Optional[int]
    unit_cars: Optional[int]
    unit_count: int
    distance: Optional[Decimal]
    duration: timedelta


@dataclass
class TransportUserTrainClassStats:
    count: int


@dataclass
class TransportUserTrainUnitStats:
    count: int