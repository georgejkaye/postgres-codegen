from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta
from decimal import Decimal
from typing import Optional

from api.db.types.train.station import (
   TrainStationHighOutData,
)

@dataclass
class TransportUserTrainOperatorTrainLegOutData:
    train_leg_id: int
    board_station: TrainStationHighOutData
    alight_station: TrainStationHighOutData
    start_datetime: datetime
    distance: Optional[Decimal]
    duration: timedelta
    delay: Optional[int]


@dataclass
class TransportUserTrainOperatorOutData:
    train_operator_id: int
    operator_code: str
    operator_name: str
    leg_count: int
    leg_duration: timedelta
    leg_distance: Decimal
    leg_delay: int
    operator_legs: list[TransportUserTrainOperatorTrainLegOutData]


@dataclass
class TransportUserTrainOperatorHighOutData:
    train_operator_id: int
    operator_code: str
    operator_name: str
    is_brand: bool
    leg_count: int
    leg_duration: timedelta
    leg_distance: Decimal
    leg_delay: int


@dataclass
class TransportUserTrainOperatorStats:
    count: int