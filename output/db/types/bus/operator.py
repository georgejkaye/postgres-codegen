from dataclasses import dataclass
from typing import Optional

@dataclass
class BusOperatorInData:
    operator_name: str
    national_operator_code: str


@dataclass
class BusOperatorDetails:
    bus_operator_id: int
    operator_name: str
    national_operator_code: str
    bg_colour: Optional[str]
    fg_colour: Optional[str]