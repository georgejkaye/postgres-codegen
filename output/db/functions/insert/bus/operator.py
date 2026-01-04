from typing import (
   Optional,
)

from psycopg import Connection

from api.db.types.bus.operator import (
   BusOperatorInData,
)


def insert_bus_operators(
    conn: Connection,
    operators : list[BusOperatorInData]
) -> None:
    p_operators = operators
    try:
        conn.execute(
            "SELECT * FROM insert_bus_operators(%s)",
            [p_operators]
        )
        conn.commit()
    except:
        conn.rollback()
        raise