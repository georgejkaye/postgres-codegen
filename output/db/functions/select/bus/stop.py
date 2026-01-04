from typing import (
   Optional,
)

from psycopg import Connection
from psycopg.rows import class_row

from api.db.types.bus.stop import (
   BusStopDetails,
)


def select_bus_stop_details_fetchall(
    conn: Connection
) -> list[BusStopDetails]:
    try:
        with conn.cursor(row_factory=class_row(BusStopDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_stop_details()",
                []
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_bus_stop_details_fetchone(
    conn: Connection
) -> Optional[BusStopDetails]:
    try:
        with conn.cursor(row_factory=class_row(BusStopDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_stop_details()",
                []
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_bus_stop_details_by_name_fetchall(
    conn: Connection,
    name : str
) -> list[BusStopDetails]:
    p_name = name
    try:
        with conn.cursor(row_factory=class_row(BusStopDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_stop_details_by_name(%s)",
                [p_name]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_bus_stop_details_by_name_fetchone(
    conn: Connection,
    name : str
) -> Optional[BusStopDetails]:
    p_name = name
    try:
        with conn.cursor(row_factory=class_row(BusStopDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_stop_details_by_name(%s)",
                [p_name]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_bus_stop_details_by_atcos_fetchall(
    conn: Connection,
    atcos : list[str]
) -> list[BusStopDetails]:
    p_atcos = atcos
    try:
        with conn.cursor(row_factory=class_row(BusStopDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_stop_details_by_atcos(%s)",
                [p_atcos]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_bus_stop_details_by_atcos_fetchone(
    conn: Connection,
    atcos : list[str]
) -> Optional[BusStopDetails]:
    p_atcos = atcos
    try:
        with conn.cursor(row_factory=class_row(BusStopDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_stop_details_by_atcos(%s)",
                [p_atcos]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_bus_stop_details_by_journey_id_fetchall(
    conn: Connection,
    journey_id : int
) -> list[BusStopDetails]:
    p_journey_id = journey_id
    try:
        with conn.cursor(row_factory=class_row(BusStopDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_stop_details_by_journey_id(%s)",
                [p_journey_id]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_bus_stop_details_by_journey_id_fetchone(
    conn: Connection,
    journey_id : int
) -> Optional[BusStopDetails]:
    p_journey_id = journey_id
    try:
        with conn.cursor(row_factory=class_row(BusStopDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_stop_details_by_journey_id(%s)",
                [p_journey_id]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise