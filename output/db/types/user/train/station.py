from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from api.db.types.train.station import (
   TrainStationHighOutData,
)
from api.db.types.train.operator import (
   TrainOperatorHighOutData,
)

@dataclass
class TransportUserTrainStationLegOutData:
    leg_id: int
    board_station: TrainStationHighOutData
    alight_station: TrainStationHighOutData
    plan_arr: Optional[datetime]
    act_arr: Optional[datetime]
    plan_dep: Optional[datetime]
    act_dep: Optional[datetime]
    operator: TrainOperatorHighOutData
    brand: Optional[TrainOperatorHighOutData]
    call_index: int
    calls_before: int
    calls_after: int


@dataclass
class TransportUserTrainStationOutData:
    station_id: int
    station_crs: str
    station_name: str
    station_operator: TrainOperatorHighOutData
    station_brand: Optional[TrainOperatorHighOutData]
    boards: int
    alights: int
    calls: int
    station_legs: list[TransportUserTrainStationLegOutData]


@dataclass
class TransportUserTrainStationHighOutData:
    station_id: int
    station_crs: str
    station_name: str
    station_operator: TrainOperatorHighOutData
    station_brand: Optional[TrainOperatorHighOutData]
    boards: int
    alights: int
    calls: int