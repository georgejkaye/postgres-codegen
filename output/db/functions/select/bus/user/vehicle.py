from typing import (
   Optional,
)

from psycopg import Connection
from psycopg.rows import class_row

from api.db.types.bus.user.vehicle import (
   BusVehicleUserDetails,
)


def select_bus_vehicle_user_details_by_user_id_fetchall(
    conn: Connection,
    user_id : int
) -> list[BusVehicleUserDetails]:
    p_user_id = user_id
    try:
        with conn.cursor(row_factory=class_row(BusVehicleUserDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_vehicle_user_details_by_user_id(%s)",
                [p_user_id]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_bus_vehicle_user_details_by_user_id_fetchone(
    conn: Connection,
    user_id : int
) -> Optional[BusVehicleUserDetails]:
    p_user_id = user_id
    try:
        with conn.cursor(row_factory=class_row(BusVehicleUserDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_vehicle_user_details_by_user_id(%s)",
                [p_user_id]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_bus_vehicle_user_details_by_user_id_and_vehicle_id_fetchall(
    conn: Connection,
    user_id : int,
    vehicle_id : int
) -> list[BusVehicleUserDetails]:
    p_user_id = user_id
    p_vehicle_id = vehicle_id
    try:
        with conn.cursor(row_factory=class_row(BusVehicleUserDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_vehicle_user_details_by_user_id_and_vehicle_id(%s, %s)",
                [p_user_id, p_vehicle_id]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_bus_vehicle_user_details_by_user_id_and_vehicle_id_fetchone(
    conn: Connection,
    user_id : int,
    vehicle_id : int
) -> Optional[BusVehicleUserDetails]:
    p_user_id = user_id
    p_vehicle_id = vehicle_id
    try:
        with conn.cursor(row_factory=class_row(BusVehicleUserDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_vehicle_user_details_by_user_id_and_vehicle_id(%s, %s)",
                [p_user_id, p_vehicle_id]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise