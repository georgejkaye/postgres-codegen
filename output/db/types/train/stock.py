from dataclasses import dataclass
from typing import Optional

@dataclass
class TrainStockSubclassOutData:
    stock_subclass: Optional[int]
    stock_subclass_name: Optional[str]
    stock_cars: list[int]


@dataclass
class TrainStockOutData:
    stock_class: int
    stock_class_name: Optional[str]
    stock_subclasses: list[TrainStockSubclassOutData]


@dataclass
class TrainStockReportOutData:
    stock_class: Optional[int]
    stock_subclass: Optional[int]
    unit_number: Optional[int]
    cars: Optional[int]