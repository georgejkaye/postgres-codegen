from typing import (
   Optional,
)

from psycopg import Connection
from psycopg.rows import class_row

from api.db.types.train.leg import (
   InsertTrainLegResult,
   TrainLegInData,
)


def insert_train_leg_fetchall(
    conn: Connection,
    users : list[int],
    leg : TrainLegInData
) -> list[InsertTrainLegResult]:
    p_users = users
    p_leg = leg
    try:
        with conn.cursor(row_factory=class_row(InsertTrainLegResult)) as cur:
            rows = cur.execute(
                "SELECT * FROM insert_train_leg(%s, %s)",
                [p_users, p_leg]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def insert_train_leg_fetchone(
    conn: Connection,
    users : list[int],
    leg : TrainLegInData
) -> Optional[InsertTrainLegResult]:
    p_users = users
    p_leg = leg
    try:
        with conn.cursor(row_factory=class_row(InsertTrainLegResult)) as cur:
            rows = cur.execute(
                "SELECT * FROM insert_train_leg(%s, %s)",
                [p_users, p_leg]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise