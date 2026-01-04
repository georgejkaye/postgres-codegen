from typing import (
   Optional,
)

from psycopg import Connection
from psycopg.rows import class_row

from api.db.types.bus.user.stop import (
   BusStopUserDetails,
)


def select_bus_stop_user_details_by_user_id_and_stop_id_fetchall(
    conn: Connection,
    user_id : int,
    stop_id : int
) -> list[BusStopUserDetails]:
    p_user_id = user_id
    p_stop_id = stop_id
    try:
        with conn.cursor(row_factory=class_row(BusStopUserDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_stop_user_details_by_user_id_and_stop_id(%s, %s)",
                [p_user_id, p_stop_id]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_bus_stop_user_details_by_user_id_and_stop_id_fetchone(
    conn: Connection,
    user_id : int,
    stop_id : int
) -> Optional[BusStopUserDetails]:
    p_user_id = user_id
    p_stop_id = stop_id
    try:
        with conn.cursor(row_factory=class_row(BusStopUserDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_stop_user_details_by_user_id_and_stop_id(%s, %s)",
                [p_user_id, p_stop_id]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_bus_stop_user_details_by_user_id_and_atco_fetchall(
    conn: Connection,
    user_id : int,
    atco : str
) -> list[BusStopUserDetails]:
    p_user_id = user_id
    p_atco = atco
    try:
        with conn.cursor(row_factory=class_row(BusStopUserDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_stop_user_details_by_user_id_and_atco(%s, %s)",
                [p_user_id, p_atco]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_bus_stop_user_details_by_user_id_and_atco_fetchone(
    conn: Connection,
    user_id : int,
    atco : str
) -> Optional[BusStopUserDetails]:
    p_user_id = user_id
    p_atco = atco
    try:
        with conn.cursor(row_factory=class_row(BusStopUserDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_stop_user_details_by_user_id_and_atco(%s, %s)",
                [p_user_id, p_atco]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_bus_stop_user_details_by_user_id_fetchall(
    conn: Connection,
    user_id : int
) -> list[BusStopUserDetails]:
    p_user_id = user_id
    try:
        with conn.cursor(row_factory=class_row(BusStopUserDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_stop_user_details_by_user_id(%s)",
                [p_user_id]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_bus_stop_user_details_by_user_id_fetchone(
    conn: Connection,
    user_id : int
) -> Optional[BusStopUserDetails]:
    p_user_id = user_id
    try:
        with conn.cursor(row_factory=class_row(BusStopUserDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_stop_user_details_by_user_id(%s)",
                [p_user_id]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise