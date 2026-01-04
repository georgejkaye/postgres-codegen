from typing import (
   Optional,
)
from datetime import (
   datetime,
)

from psycopg import Connection
from psycopg.rows import class_row

from api.db.types.user.train.leg import (
   TransportUserTrainLegOutData,
   TransportUserTrainLegStats,
)


def select_transport_user_train_leg_stats_by_user_id_fetchall(
    conn: Connection,
    user_id : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime],
    rows_to_return : Optional[int]
) -> list[TransportUserTrainLegStats]:
    p_user_id = user_id
    p_search_start = search_start
    p_search_end = search_end
    p_rows_to_return = rows_to_return
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainLegStats)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_transport_user_train_leg_stats_by_user_id(%s, %s, %s, %s)",
                [p_user_id, p_search_start, p_search_end, p_rows_to_return]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_transport_user_train_leg_stats_by_user_id_fetchone(
    conn: Connection,
    user_id : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime],
    rows_to_return : Optional[int]
) -> Optional[TransportUserTrainLegStats]:
    p_user_id = user_id
    p_search_start = search_start
    p_search_end = search_end
    p_rows_to_return = rows_to_return
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainLegStats)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_transport_user_train_leg_stats_by_user_id(%s, %s, %s, %s)",
                [p_user_id, p_search_start, p_search_end, p_rows_to_return]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_transport_user_train_legs_by_user_id_fetchall(
    conn: Connection,
    user_id : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime]
) -> list[TransportUserTrainLegOutData]:
    p_user_id = user_id
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainLegOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_transport_user_train_legs_by_user_id(%s, %s, %s)",
                [p_user_id, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_transport_user_train_legs_by_user_id_fetchone(
    conn: Connection,
    user_id : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime]
) -> Optional[TransportUserTrainLegOutData]:
    p_user_id = user_id
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainLegOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_transport_user_train_legs_by_user_id(%s, %s, %s)",
                [p_user_id, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_longest_transport_user_train_legs_by_user_id_fetchall(
    conn: Connection,
    user_id : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime],
    rows_to_return : Optional[int]
) -> list[TransportUserTrainLegOutData]:
    p_user_id = user_id
    p_search_start = search_start
    p_search_end = search_end
    p_rows_to_return = rows_to_return
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainLegOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_longest_transport_user_train_legs_by_user_id(%s, %s, %s, %s)",
                [p_user_id, p_search_start, p_search_end, p_rows_to_return]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_longest_transport_user_train_legs_by_user_id_fetchone(
    conn: Connection,
    user_id : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime],
    rows_to_return : Optional[int]
) -> Optional[TransportUserTrainLegOutData]:
    p_user_id = user_id
    p_search_start = search_start
    p_search_end = search_end
    p_rows_to_return = rows_to_return
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainLegOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_longest_transport_user_train_legs_by_user_id(%s, %s, %s, %s)",
                [p_user_id, p_search_start, p_search_end, p_rows_to_return]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_shortest_transport_user_train_legs_by_user_id_fetchall(
    conn: Connection,
    user_id : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime],
    rows_to_return : Optional[int]
) -> list[TransportUserTrainLegOutData]:
    p_user_id = user_id
    p_search_start = search_start
    p_search_end = search_end
    p_rows_to_return = rows_to_return
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainLegOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_shortest_transport_user_train_legs_by_user_id(%s, %s, %s, %s)",
                [p_user_id, p_search_start, p_search_end, p_rows_to_return]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_shortest_transport_user_train_legs_by_user_id_fetchone(
    conn: Connection,
    user_id : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime],
    rows_to_return : Optional[int]
) -> Optional[TransportUserTrainLegOutData]:
    p_user_id = user_id
    p_search_start = search_start
    p_search_end = search_end
    p_rows_to_return = rows_to_return
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainLegOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_shortest_transport_user_train_legs_by_user_id(%s, %s, %s, %s)",
                [p_user_id, p_search_start, p_search_end, p_rows_to_return]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise