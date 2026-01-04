from typing import (
   Optional,
)

from psycopg import Connection
from psycopg.rows import class_row

from api.db.types.bus.operator import (
   BusOperatorDetails,
)


def select_bus_operator_details_fetchall(
    conn: Connection
) -> list[BusOperatorDetails]:
    try:
        with conn.cursor(row_factory=class_row(BusOperatorDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_operator_details()",
                []
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_bus_operator_details_fetchone(
    conn: Connection
) -> Optional[BusOperatorDetails]:
    try:
        with conn.cursor(row_factory=class_row(BusOperatorDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_operator_details()",
                []
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_bus_operator_details_by_name_fetchall(
    conn: Connection,
    name : str
) -> list[BusOperatorDetails]:
    p_name = name
    try:
        with conn.cursor(row_factory=class_row(BusOperatorDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_operator_details_by_name(%s)",
                [p_name]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_bus_operator_details_by_name_fetchone(
    conn: Connection,
    name : str
) -> Optional[BusOperatorDetails]:
    p_name = name
    try:
        with conn.cursor(row_factory=class_row(BusOperatorDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_operator_details_by_name(%s)",
                [p_name]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_bus_operator_details_by_national_operator_code_fetchall(
    conn: Connection,
    noc : str
) -> list[BusOperatorDetails]:
    p_noc = noc
    try:
        with conn.cursor(row_factory=class_row(BusOperatorDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_operator_details_by_national_operator_code(%s)",
                [p_noc]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_bus_operator_details_by_national_operator_code_fetchone(
    conn: Connection,
    noc : str
) -> Optional[BusOperatorDetails]:
    p_noc = noc
    try:
        with conn.cursor(row_factory=class_row(BusOperatorDetails)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_bus_operator_details_by_national_operator_code(%s)",
                [p_noc]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise