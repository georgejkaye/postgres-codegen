from typing import (
   Optional,
)
from datetime import (
   datetime,
)

from psycopg import Connection
from psycopg.rows import class_row

from api.db.types.train.leg import (
   TrainLegOutData,
   TrainLegPointsOutData,
)


def select_train_leg_by_id_fetchall(
    conn: Connection,
    train_leg_id : int
) -> list[TrainLegOutData]:
    p_train_leg_id = train_leg_id
    try:
        with conn.cursor(row_factory=class_row(TrainLegOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_leg_by_id(%s)",
                [p_train_leg_id]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_train_leg_by_id_fetchone(
    conn: Connection,
    train_leg_id : int
) -> Optional[TrainLegOutData]:
    p_train_leg_id = train_leg_id
    try:
        with conn.cursor(row_factory=class_row(TrainLegOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_leg_by_id(%s)",
                [p_train_leg_id]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_train_legs_by_ids_fetchall(
    conn: Connection,
    train_leg_ids : list[int]
) -> list[TrainLegOutData]:
    p_train_leg_ids = train_leg_ids
    try:
        with conn.cursor(row_factory=class_row(TrainLegOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_legs_by_ids(%s)",
                [p_train_leg_ids]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_train_legs_by_ids_fetchone(
    conn: Connection,
    train_leg_ids : list[int]
) -> Optional[TrainLegOutData]:
    p_train_leg_ids = train_leg_ids
    try:
        with conn.cursor(row_factory=class_row(TrainLegOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_legs_by_ids(%s)",
                [p_train_leg_ids]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_train_leg_points_by_leg_id_fetchall(
    conn: Connection,
    train_leg_id : int
) -> list[TrainLegPointsOutData]:
    p_train_leg_id = train_leg_id
    try:
        with conn.cursor(row_factory=class_row(TrainLegPointsOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_leg_points_by_leg_id(%s)",
                [p_train_leg_id]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_train_leg_points_by_leg_id_fetchone(
    conn: Connection,
    train_leg_id : int
) -> Optional[TrainLegPointsOutData]:
    p_train_leg_id = train_leg_id
    try:
        with conn.cursor(row_factory=class_row(TrainLegPointsOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_leg_points_by_leg_id(%s)",
                [p_train_leg_id]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_train_leg_points_by_leg_ids_fetchall(
    conn: Connection,
    train_leg_ids : list[int]
) -> list[TrainLegPointsOutData]:
    p_train_leg_ids = train_leg_ids
    try:
        with conn.cursor(row_factory=class_row(TrainLegPointsOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_leg_points_by_leg_ids(%s)",
                [p_train_leg_ids]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_train_leg_points_by_leg_ids_fetchone(
    conn: Connection,
    train_leg_ids : list[int]
) -> Optional[TrainLegPointsOutData]:
    p_train_leg_ids = train_leg_ids
    try:
        with conn.cursor(row_factory=class_row(TrainLegPointsOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_leg_points_by_leg_ids(%s)",
                [p_train_leg_ids]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_train_leg_points_by_user_id_fetchall(
    conn: Connection,
    user_id : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime]
) -> list[TrainLegPointsOutData]:
    p_user_id = user_id
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(TrainLegPointsOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_leg_points_by_user_id(%s, %s, %s)",
                [p_user_id, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_train_leg_points_by_user_id_fetchone(
    conn: Connection,
    user_id : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime]
) -> Optional[TrainLegPointsOutData]:
    p_user_id = user_id
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(TrainLegPointsOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_leg_points_by_user_id(%s, %s, %s)",
                [p_user_id, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise