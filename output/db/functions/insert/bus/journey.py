from typing import (
   Optional,
)

from psycopg import Connection
from psycopg.rows import class_row

from api.db.types.bus.journey import (
   BusCallInData,
   BusJourneyInData,
)


def insert_bus_calls(
    conn: Connection,
    journey_id : int,
    calls : list[BusCallInData]
) -> None:
    p_journey_id = journey_id
    p_calls = calls
    try:
        conn.execute(
            "SELECT * FROM insert_bus_calls(%s, %s)",
            [p_journey_id, p_calls]
        )
        conn.commit()
    except:
        conn.rollback()
        raise


def insert_bus_journey_fetchall(
    conn: Connection,
    journey : BusJourneyInData
) -> list[int]:
    p_journey = journey
    try:
        with conn.cursor(row_factory=class_row(int)) as cur:
            rows = cur.execute(
                "SELECT * FROM insert_bus_journey(%s)",
                [p_journey]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def insert_bus_journey_fetchone(
    conn: Connection,
    journey : BusJourneyInData
) -> Optional[int]:
    p_journey = journey
    try:
        with conn.cursor(row_factory=class_row(int)) as cur:
            rows = cur.execute(
                "SELECT * FROM insert_bus_journey(%s)",
                [p_journey]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise