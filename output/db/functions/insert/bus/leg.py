from typing import (
   Optional,
)

from psycopg import Connection
from psycopg.rows import class_row

from api.db.types.bus.user.leg import (
   InsertBusLegResult,
)
from api.db.types.bus.leg import (
   BusLegInData,
)


def insert_bus_leg_fetchall(
    conn: Connection,
    users : list[int],
    leg : BusLegInData
) -> list[InsertBusLegResult]:
    p_users = users
    p_leg = leg
    try:
        with conn.cursor(row_factory=class_row(InsertBusLegResult)) as cur:
            rows = cur.execute(
                "SELECT * FROM insert_bus_leg(%s, %s)",
                [p_users, p_leg]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def insert_bus_leg_fetchone(
    conn: Connection,
    users : list[int],
    leg : BusLegInData
) -> Optional[InsertBusLegResult]:
    p_users = users
    p_leg = leg
    try:
        with conn.cursor(row_factory=class_row(InsertBusLegResult)) as cur:
            rows = cur.execute(
                "SELECT * FROM insert_bus_leg(%s, %s)",
                [p_users, p_leg]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise