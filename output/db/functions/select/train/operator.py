from typing import (
   Optional,
)
from datetime import (
   datetime,
)

from psycopg import Connection
from psycopg.rows import class_row

from api.db.types.train.operator import (
   TrainBrandOutData,
   TrainOperatorDetailsOutData,
   TrainOperatorOutData,
)


def select_brands_by_operator_code_fetchall(
    conn: Connection,
    operator_code : str,
    run_date : datetime
) -> list[TrainBrandOutData]:
    p_operator_code = operator_code
    p_run_date = run_date
    try:
        with conn.cursor(row_factory=class_row(TrainBrandOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_brands_by_operator_code(%s, %s)",
                [p_operator_code, p_run_date]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_brands_by_operator_code_fetchone(
    conn: Connection,
    operator_code : str,
    run_date : datetime
) -> Optional[TrainBrandOutData]:
    p_operator_code = operator_code
    p_run_date = run_date
    try:
        with conn.cursor(row_factory=class_row(TrainBrandOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_brands_by_operator_code(%s, %s)",
                [p_operator_code, p_run_date]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_train_operator_by_operator_code_fetchall(
    conn: Connection,
    operator_code : str,
    run_date : datetime
) -> list[TrainOperatorOutData]:
    p_operator_code = operator_code
    p_run_date = run_date
    try:
        with conn.cursor(row_factory=class_row(TrainOperatorOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_operator_by_operator_code(%s, %s)",
                [p_operator_code, p_run_date]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_train_operator_by_operator_code_fetchone(
    conn: Connection,
    operator_code : str,
    run_date : datetime
) -> Optional[TrainOperatorOutData]:
    p_operator_code = operator_code
    p_run_date = run_date
    try:
        with conn.cursor(row_factory=class_row(TrainOperatorOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_operator_by_operator_code(%s, %s)",
                [p_operator_code, p_run_date]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_train_operator_details_fetchall(
    conn: Connection
) -> list[TrainOperatorDetailsOutData]:
    try:
        with conn.cursor(row_factory=class_row(TrainOperatorDetailsOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_operator_details()",
                []
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_train_operator_details_fetchone(
    conn: Connection
) -> Optional[TrainOperatorDetailsOutData]:
    try:
        with conn.cursor(row_factory=class_row(TrainOperatorDetailsOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_operator_details()",
                []
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise