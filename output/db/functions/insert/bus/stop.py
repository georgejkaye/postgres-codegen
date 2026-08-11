from typing import (
   Optional,
)

from psycopg import Connection

from api.db.types.bus.stop import (
   BusStopInData,
)


def insert_bus_stops(
    conn: Connection,
    stops : list[BusStopInData]
) -> None:
    p_stops = stops
    try:
        conn.execute(
            "SELECT * FROM insert_bus_stops(%s)",
            [p_stops]
        )
        conn.commit()
    except:
        conn.rollback()
        raise