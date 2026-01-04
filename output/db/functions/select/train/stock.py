from typing import (
   Optional,
)
from datetime import (
   datetime,
)

from psycopg import Connection
from psycopg.rows import class_row

from api.db.types.train.stock import (
   TrainStockOutData,
)


def select_train_operator_stock_fetchall(
    conn: Connection,
    operator_id : int,
    brand_id : Optional[int],
    run_date : datetime
) -> list[TrainStockOutData]:
    p_operator_id = operator_id
    p_brand_id = brand_id
    p_run_date = run_date
    try:
        with conn.cursor(row_factory=class_row(TrainStockOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_operator_stock(%s, %s, %s)",
                [p_operator_id, p_brand_id, p_run_date]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_train_operator_stock_fetchone(
    conn: Connection,
    operator_id : int,
    brand_id : Optional[int],
    run_date : datetime
) -> Optional[TrainStockOutData]:
    p_operator_id = operator_id
    p_brand_id = brand_id
    p_run_date = run_date
    try:
        with conn.cursor(row_factory=class_row(TrainStockOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_operator_stock(%s, %s, %s)",
                [p_operator_id, p_brand_id, p_run_date]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise