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
class TransportUserTrainLegOutData:
    leg_id: int
    board_station: TrainStationHighOutData
    alight_station: TrainStationHighOutData
    start_datetime: datetime
    operator: TrainOperatorHighOutData
    brand: Optional[TrainOperatorHighOutData]
    distance: Optional[Decimal]
    duration: Optional[timedelta]
    delay: Optional[int]


@dataclass
class TransportUserTrainLegStats:
    count: int
    total_distance: Decimal
    longest_distance: Decimal
    longest_distance_legs: list[TransportUserTrainLegOutData]
    shortest_distance: Decimal
    shortest_distance_legs: list[TransportUserTrainLegOutData]
    total_duration: timedelta
    longest_duration: timedelta
    longest_duration_legs: list[TransportUserTrainLegOutData]
    shortest_duration: timedelta
    shortest_duration_legs: list[TransportUserTrainLegOutData]
    total_delay: int
    longest_delay: int
    longest_delay_legs: list[TransportUserTrainLegOutData]
    shortest_delay: int
    shortest_delay_legs: list[TransportUserTrainLegOutData]