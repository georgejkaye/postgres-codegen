from typing import (
   Optional,
)

from psycopg import Connection
from psycopg.rows import class_row

from api.db.types.bus.service import (
   BusServiceDetails,
)


def select_bus_service_details_fetchall(
    conn: Connection
) -> list[BusServiceDetails]:
    try:
        with conn.cursor(row_factory=class_row(BusServiceDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_service_details()",
                []
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_bus_service_details_fetchone(
    conn: Connection
) -> Optional[BusServiceDetails]:
    try:
        with conn.cursor(row_factory=class_row(BusServiceDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_service_details()",
                []
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_bus_service_details_by_operator_id_and_line_name_fetchall(
    conn: Connection,
    operator_id : int,
    line_name : str
) -> list[BusServiceDetails]:
    p_operator_id = operator_id
    p_line_name = line_name
    try:
        with conn.cursor(row_factory=class_row(BusServiceDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_service_details_by_operator_id_and_line_name(%s, %s)",
                [p_operator_id, p_line_name]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_bus_service_details_by_operator_id_and_line_name_fetchone(
    conn: Connection,
    operator_id : int,
    line_name : str
) -> Optional[BusServiceDetails]:
    p_operator_id = operator_id
    p_line_name = line_name
    try:
        with conn.cursor(row_factory=class_row(BusServiceDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_service_details_by_operator_id_and_line_name(%s, %s)",
                [p_operator_id, p_line_name]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_bus_service_details_by_national_operator_code_and_line_name_fetchall(
    conn: Connection,
    national_operator_code : str,
    line_name : str
) -> list[BusServiceDetails]:
    p_national_operator_code = national_operator_code
    p_line_name = line_name
    try:
        with conn.cursor(row_factory=class_row(BusServiceDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_service_details_by_national_operator_code_and_line_name(%s, %s)",
                [p_national_operator_code, p_line_name]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_bus_service_details_by_national_operator_code_and_line_name_fetchone(
    conn: Connection,
    national_operator_code : str,
    line_name : str
) -> Optional[BusServiceDetails]:
    p_national_operator_code = national_operator_code
    p_line_name = line_name
    try:
        with conn.cursor(row_factory=class_row(BusServiceDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_service_details_by_national_operator_code_and_line_name(%s, %s)",
                [p_national_operator_code, p_line_name]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_bus_service_details_by_operator_name_and_line_name_fetchall(
    conn: Connection,
    operator_name : str,
    line_name : str
) -> list[BusServiceDetails]:
    p_operator_name = operator_name
    p_line_name = line_name
    try:
        with conn.cursor(row_factory=class_row(BusServiceDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_service_details_by_operator_name_and_line_name(%s, %s)",
                [p_operator_name, p_line_name]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_bus_service_details_by_operator_name_and_line_name_fetchone(
    conn: Connection,
    operator_name : str,
    line_name : str
) -> Optional[BusServiceDetails]:
    p_operator_name = operator_name
    p_line_name = line_name
    try:
        with conn.cursor(row_factory=class_row(BusServiceDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_service_details_by_operator_name_and_line_name(%s, %s)",
                [p_operator_name, p_line_name]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise