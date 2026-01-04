from dataclasses import dataclass
from typing import Optional

from api.db.types.bus.journey import (
   BusJourneyInData,
)

@dataclass
class BusLegInData:
    journey: Optional[BusJourneyInData]
    board_index: int
    alight_index: int