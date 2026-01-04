from dataclasses import dataclass
from typing import Optional

from api.db.types.bus.operator import (
   BusOperatorDetails,
)

@dataclass
class BusServiceInData:
    service_line: str
    bods_line_id: str
    service_operator_national_code: str
    service_outbound_description: str
    service_inbound_description: str


@dataclass
class BusServiceViaInData:
    bods_line_id: str
    is_outbound: bool
    via_name: str
    via_index: int


@dataclass
class BusServiceDetails:
    bus_service_id: int
    bus_operator: BusOperatorDetails
    service_line: str
    description_outbound: Optional[str]
    service_outbound_vias: list[str]
    description_inbound: Optional[str]
    service_inbound_vias: list[str]
    bg_colour: Optional[str]
    fg_colour: Optional[str]