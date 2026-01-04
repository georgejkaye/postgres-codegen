from typing import (
   Optional,
)
from datetime import (
   datetime,
)

from psycopg import Connection
from psycopg.rows import class_row

from api.db.types.bus.user.leg import (
   BusLegUserDetails,
)


def select_bus_leg_user_details_fetchall(
    conn: Connection,
    user_id : int
) -> list[BusLegUserDetails]:
    p_user_id = user_id
    try:
        with conn.cursor(row_factory=class_row(BusLegUserDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_leg_user_details(%s)",
                [p_user_id]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_bus_leg_user_details_fetchone(
    conn: Connection,
    user_id : int
) -> Optional[BusLegUserDetails]:
    p_user_id = user_id
    try:
        with conn.cursor(row_factory=class_row(BusLegUserDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_leg_user_details(%s)",
                [p_user_id]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_bus_leg_user_details_by_user_id_and_datetime_fetchall(
    conn: Connection,
    user_id : int,
    search_start : datetime,
    search_end : datetime
) -> list[BusLegUserDetails]:
    p_user_id = user_id
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(BusLegUserDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_leg_user_details_by_user_id_and_datetime(%s, %s, %s)",
                [p_user_id, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_bus_leg_user_details_by_user_id_and_datetime_fetchone(
    conn: Connection,
    user_id : int,
    search_start : datetime,
    search_end : datetime
) -> Optional[BusLegUserDetails]:
    p_user_id = user_id
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(BusLegUserDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_leg_user_details_by_user_id_and_datetime(%s, %s, %s)",
                [p_user_id, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_bus_leg_user_details_by_user_id_and_start_datetime_fetchall(
    conn: Connection,
    user_id : int,
    search_start : datetime
) -> list[BusLegUserDetails]:
    p_user_id = user_id
    p_search_start = search_start
    try:
        with conn.cursor(row_factory=class_row(BusLegUserDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_leg_user_details_by_user_id_and_start_datetime(%s, %s)",
                [p_user_id, p_search_start]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_bus_leg_user_details_by_user_id_and_start_datetime_fetchone(
    conn: Connection,
    user_id : int,
    search_start : datetime
) -> Optional[BusLegUserDetails]:
    p_user_id = user_id
    p_search_start = search_start
    try:
        with conn.cursor(row_factory=class_row(BusLegUserDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_leg_user_details_by_user_id_and_start_datetime(%s, %s)",
                [p_user_id, p_search_start]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_bus_leg_user_details_by_user_id_and_end_datetime_fetchall(
    conn: Connection,
    user_id : int,
    search_end : datetime
) -> list[BusLegUserDetails]:
    p_user_id = user_id
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(BusLegUserDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_leg_user_details_by_user_id_and_end_datetime(%s, %s)",
                [p_user_id, p_search_end]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_bus_leg_user_details_by_user_id_and_end_datetime_fetchone(
    conn: Connection,
    user_id : int,
    search_end : datetime
) -> Optional[BusLegUserDetails]:
    p_user_id = user_id
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(BusLegUserDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_leg_user_details_by_user_id_and_end_datetime(%s, %s)",
                [p_user_id, p_search_end]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_bus_leg_user_details_by_user_id_and_leg_id_fetchall(
    conn: Connection,
    user_id : int,
    leg_id : int
) -> list[BusLegUserDetails]:
    p_user_id = user_id
    p_leg_id = leg_id
    try:
        with conn.cursor(row_factory=class_row(BusLegUserDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_leg_user_details_by_user_id_and_leg_id(%s, %s)",
                [p_user_id, p_leg_id]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_bus_leg_user_details_by_user_id_and_leg_id_fetchone(
    conn: Connection,
    user_id : int,
    leg_id : int
) -> Optional[BusLegUserDetails]:
    p_user_id = user_id
    p_leg_id = leg_id
    try:
        with conn.cursor(row_factory=class_row(BusLegUserDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_leg_user_details_by_user_id_and_leg_id(%s, %s)",
                [p_user_id, p_leg_id]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_bus_leg_user_details_by_user_id_and_leg_ids_fetchall(
    conn: Connection,
    user_id : int,
    leg_ids : list[int]
) -> list[BusLegUserDetails]:
    p_user_id = user_id
    p_leg_ids = leg_ids
    try:
        with conn.cursor(row_factory=class_row(BusLegUserDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_leg_user_details_by_user_id_and_leg_ids(%s, %s)",
                [p_user_id, p_leg_ids]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_bus_leg_user_details_by_user_id_and_leg_ids_fetchone(
    conn: Connection,
    user_id : int,
    leg_ids : list[int]
) -> Optional[BusLegUserDetails]:
    p_user_id = user_id
    p_leg_ids = leg_ids
    try:
        with conn.cursor(row_factory=class_row(BusLegUserDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_leg_user_details_by_user_id_and_leg_ids(%s, %s)",
                [p_user_id, p_leg_ids]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise