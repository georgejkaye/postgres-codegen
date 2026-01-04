from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from psycopg.types.range import Range

@dataclass
class TrainBrandOutData:
    brand_id: int
    brand_code: str
    brand_name: str
    brand_bg: Optional[str]
    brand_fg: Optional[str]


@dataclass
class TrainOperatorOutData:
    operator_id: int
    operator_code: str
    operator_name: str
    operator_bg: Optional[str]
    operator_fg: Optional[str]
    operation_range: Range[datetime]
    operator_brands: list[TrainBrandOutData]


@dataclass
class TrainOperatorDetailsOutData:
    operator_id: int
    is_brand: bool
    operator_code: str
    operator_name: str
    bg_colour: Optional[str]
    fg_colour: Optional[str]


@dataclass
class TrainOperatorHighOutData:
    operator_id: int
    operator_code: str
    operator_name: str