from typing import (
   Optional,
)
from datetime import (
   datetime,
)

from psycopg import Connection
from psycopg.rows import class_row

from api.db.types.user.train.operator import (
   TransportUserTrainOperatorHighOutData,
   TransportUserTrainOperatorOutData,
   TransportUserTrainOperatorStats,
)


def select_transport_user_train_operator_by_user_id_fetchall(
    conn: Connection,
    user_id : int,
    by_brands : bool,
    search_start : Optional[datetime],
    search_end : Optional[datetime]
) -> list[TransportUserTrainOperatorHighOutData]:
    p_user_id = user_id
    p_by_brands = by_brands
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainOperatorHighOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_transport_user_train_operator_by_user_id(%s, %s, %s, %s)",
                [p_user_id, p_by_brands, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_transport_user_train_operator_by_user_id_fetchone(
    conn: Connection,
    user_id : int,
    by_brands : bool,
    search_start : Optional[datetime],
    search_end : Optional[datetime]
) -> Optional[TransportUserTrainOperatorHighOutData]:
    p_user_id = user_id
    p_by_brands = by_brands
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainOperatorHighOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_transport_user_train_operator_by_user_id(%s, %s, %s, %s)",
                [p_user_id, p_by_brands, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_top_transport_user_train_operators_by_user_id_fetchall(
    conn: Connection,
    user_id : int,
    by_brands : bool,
    search_start : Optional[datetime],
    search_end : Optional[datetime],
    rows_to_return : Optional[int]
) -> list[TransportUserTrainOperatorHighOutData]:
    p_user_id = user_id
    p_by_brands = by_brands
    p_search_start = search_start
    p_search_end = search_end
    p_rows_to_return = rows_to_return
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainOperatorHighOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_top_transport_user_train_operators_by_user_id(%s, %s, %s, %s, %s)",
                [p_user_id, p_by_brands, p_search_start, p_search_end, p_rows_to_return]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_top_transport_user_train_operators_by_user_id_fetchone(
    conn: Connection,
    user_id : int,
    by_brands : bool,
    search_start : Optional[datetime],
    search_end : Optional[datetime],
    rows_to_return : Optional[int]
) -> Optional[TransportUserTrainOperatorHighOutData]:
    p_user_id = user_id
    p_by_brands = by_brands
    p_search_start = search_start
    p_search_end = search_end
    p_rows_to_return = rows_to_return
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainOperatorHighOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_top_transport_user_train_operators_by_user_id(%s, %s, %s, %s, %s)",
                [p_user_id, p_by_brands, p_search_start, p_search_end, p_rows_to_return]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_transport_user_train_operator_stats_by_user_id_fetchall(
    conn: Connection,
    user_id : int,
    by_brands : bool,
    search_start : Optional[datetime],
    search_end : Optional[datetime]
) -> list[TransportUserTrainOperatorStats]:
    p_user_id = user_id
    p_by_brands = by_brands
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainOperatorStats)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_transport_user_train_operator_stats_by_user_id(%s, %s, %s, %s)",
                [p_user_id, p_by_brands, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_transport_user_train_operator_stats_by_user_id_fetchone(
    conn: Connection,
    user_id : int,
    by_brands : bool,
    search_start : Optional[datetime],
    search_end : Optional[datetime]
) -> Optional[TransportUserTrainOperatorStats]:
    p_user_id = user_id
    p_by_brands = by_brands
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainOperatorStats)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_transport_user_train_operator_stats_by_user_id(%s, %s, %s, %s)",
                [p_user_id, p_by_brands, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_transport_user_train_operator_by_user_id_and_operator_id_fetchall(
    conn: Connection,
    user_id : int,
    operator_id : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime]
) -> list[TransportUserTrainOperatorOutData]:
    p_user_id = user_id
    p_operator_id = operator_id
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainOperatorOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_transport_user_train_operator_by_user_id_and_operator_id(%s, %s, %s, %s)",
                [p_user_id, p_operator_id, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_transport_user_train_operator_by_user_id_and_operator_id_fetchone(
    conn: Connection,
    user_id : int,
    operator_id : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime]
) -> Optional[TransportUserTrainOperatorOutData]:
    p_user_id = user_id
    p_operator_id = operator_id
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainOperatorOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_transport_user_train_operator_by_user_id_and_operator_id(%s, %s, %s, %s)",
                [p_user_id, p_operator_id, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_transport_user_train_brand_by_user_id_and_brand_id_fetchall(
    conn: Connection,
    user_id : int,
    operator_id : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime]
) -> list[TransportUserTrainOperatorOutData]:
    p_user_id = user_id
    p_operator_id = operator_id
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainOperatorOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_transport_user_train_brand_by_user_id_and_brand_id(%s, %s, %s, %s)",
                [p_user_id, p_operator_id, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_transport_user_train_brand_by_user_id_and_brand_id_fetchone(
    conn: Connection,
    user_id : int,
    operator_id : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime]
) -> Optional[TransportUserTrainOperatorOutData]:
    p_user_id = user_id
    p_operator_id = operator_id
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainOperatorOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_transport_user_train_brand_by_user_id_and_brand_id(%s, %s, %s, %s)",
                [p_user_id, p_operator_id, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise