from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

from api.db.types.train.station import (
   TrainStationHighOutData,
)
from api.db.types.train.operator import (
   TrainOperatorHighOutData,
)

@dataclass
class TrainLegServiceInData:
    unique_identifier: str
    run_date: datetime
    headcode: str
    operator_id: int
    brand_id: Optional[int]
    power: Optional[str]


@dataclass
class TrainLegServiceEndpointInData:
    unique_identifier: str
    run_date: datetime
    station_name: str
    origin: bool


@dataclass
class TrainLegServiceCallInData:
    unique_identifier: str
    run_date: datetime
    station_crs: str
    platform: Optional[str]
    plan_arr: Optional[datetime]
    act_arr: Optional[datetime]
    plan_dep: Optional[datetime]
    act_dep: Optional[datetime]
    mileage: Optional[Decimal]


@dataclass
class TrainLegAssociatedServiceInData:
    unique_identifier: str
    run_date: datetime
    station_crs: str
    plan_arr: Optional[datetime]
    act_arr: Optional[datetime]
    plan_dep: Optional[datetime]
    act_dep: Optional[datetime]
    assoc_unique_identifier: str
    assoc_run_date: datetime
    assoc_type: int


@dataclass
class TrainLegServiceCallAssociatedServiceInData:
    associated_unique_identifier: str
    associated_run_date: datetime
    associated_type: str


@dataclass
class TrainLegCallCallInData:
    service_uid: str
    service_run_date: datetime
    plan_arr: Optional[datetime]
    act_arr: Optional[datetime]
    plan_dep: Optional[datetime]
    act_dep: Optional[datetime]


@dataclass
class TrainLegCallInData:
    station_crs: str
    station_name: str
    arr_call: Optional[TrainLegCallCallInData]
    dep_call: Optional[TrainLegCallCallInData]
    mileage: Optional[Decimal]
    associated_type_id: Optional[int]


@dataclass
class TrainLegStockSegmentInData:
    stock_class: Optional[int]
    stock_subclass: Optional[int]
    stock_number: Optional[int]
    stock_cars: Optional[int]
    start_call_service_uid: str
    start_call_service_run_date: datetime
    start_call_station_crs: str
    start_call_plan_dep: Optional[datetime]
    start_call_act_dep: Optional[datetime]
    end_call_service_uid: str
    end_call_service_run_date: datetime
    end_call_station_crs: str
    end_call_plan_arr: Optional[datetime]
    end_call_act_arr: Optional[datetime]
    mileage: Optional[Decimal]


@dataclass
class TrainLegInData:
    leg_services: list[TrainLegServiceInData]
    service_endpoints: list[TrainLegServiceEndpointInData]
    service_calls: list[TrainLegServiceCallInData]
    service_associations: list[TrainLegAssociatedServiceInData]
    leg_calls: list[TrainLegCallInData]
    leg_stock: list[TrainLegStockSegmentInData]
    leg_distance: Optional[Decimal]


@dataclass
class TrainLegAssociatedServiceOutData:
    service_id: int
    association_type: int


@dataclass
class TrainLegCallOutData:
    station: TrainStationHighOutData
    platform: Optional[str]
    plan_arr: Optional[datetime]
    act_arr: Optional[datetime]
    plan_dep: Optional[datetime]
    act_dep: Optional[datetime]
    service_association_type: Optional[str]
    mileage: Optional[Decimal]


@dataclass
class TrainLegServiceOutData:
    service_id: int
    unique_identifier: str
    run_date: datetime
    headcode: str
    start_datetime: datetime
    origins: list[TrainStationHighOutData]
    destinations: list[TrainStationHighOutData]
    operator: TrainOperatorHighOutData
    brand: Optional[TrainOperatorHighOutData]


@dataclass
class TrainLegStockReportOutData:
    stock_class: Optional[int]
    stock_subclass: Optional[int]
    stock_number: Optional[int]
    stock_cars: Optional[int]


@dataclass
class TrainLegStockSegmentOutData:
    stock_start: TrainStationHighOutData
    stock_end: TrainStationHighOutData
    stock_reports: list[TrainLegStockReportOutData]


@dataclass
class TrainLegOutData:
    leg_id: int
    services: list[TrainLegServiceOutData]
    calls: list[TrainLegCallOutData]
    stock: list[TrainLegStockSegmentOutData]


@dataclass
class TrainLegCallPointOutData:
    platform: Optional[str]
    latitude: Decimal
    longitude: Decimal


@dataclass
class TrainLegCallPointsOutData:
    station_id: int
    station_crs: str
    station_name: str
    platform: Optional[str]
    plan_arr: Optional[datetime]
    act_arr: Optional[datetime]
    plan_dep: Optional[datetime]
    act_dep: Optional[datetime]
    points: list[TrainLegCallPointOutData]


@dataclass
class TrainLegPointsOutData:
    leg_id: int
    operator_id: int
    brand_id: Optional[int]
    call_points: list[TrainLegCallPointsOutData]


@dataclass
class InsertTrainLegResult:
    train_leg_id: int