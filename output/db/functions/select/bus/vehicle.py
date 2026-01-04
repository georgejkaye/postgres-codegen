from typing import (
   Optional,
)

from psycopg import Connection
from psycopg.rows import class_row

from api.db.types.bus.vehicle import (
   BusVehicleDetails,
)


def select_bus_vehicle_details_fetchall(
    conn: Connection,
    operator_id : Optional[int],
    vehicle_id : str
) -> list[BusVehicleDetails]:
    p_operator_id = operator_id
    p_vehicle_id = vehicle_id
    try:
        with conn.cursor(row_factory=class_row(BusVehicleDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_vehicle_details(%s, %s)",
                [p_operator_id, p_vehicle_id]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_bus_vehicle_details_fetchone(
    conn: Connection,
    operator_id : Optional[int],
    vehicle_id : str
) -> Optional[BusVehicleDetails]:
    p_operator_id = operator_id
    p_vehicle_id = vehicle_id
    try:
        with conn.cursor(row_factory=class_row(BusVehicleDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_vehicle_details(%s, %s)",
                [p_operator_id, p_vehicle_id]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise