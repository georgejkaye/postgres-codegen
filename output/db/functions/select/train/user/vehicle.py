from typing import (
   Optional,
)
from datetime import (
   datetime,
)

from psycopg import Connection
from psycopg.rows import class_row

from api.db.types.user.train.vehicle import (
   TransportUserTrainClassHighOutData,
   TransportUserTrainClassOutData,
   TransportUserTrainClassStats,
   TransportUserTrainUnitHighOutData,
   TransportUserTrainUnitOutData,
   TransportUserTrainUnitStats,
)


def select_transport_user_train_class_by_user_id_and_class_fetchall(
    conn: Connection,
    user_id : int,
    stock_class : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime]
) -> list[TransportUserTrainClassOutData]:
    p_user_id = user_id
    p_stock_class = stock_class
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainClassOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_transport_user_train_class_by_user_id_and_class(%s, %s, %s, %s)",
                [p_user_id, p_stock_class, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_transport_user_train_class_by_user_id_and_class_fetchone(
    conn: Connection,
    user_id : int,
    stock_class : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime]
) -> Optional[TransportUserTrainClassOutData]:
    p_user_id = user_id
    p_stock_class = stock_class
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainClassOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_transport_user_train_class_by_user_id_and_class(%s, %s, %s, %s)",
                [p_user_id, p_stock_class, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_transport_user_train_class_by_user_id_fetchall(
    conn: Connection,
    user_id : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime]
) -> list[TransportUserTrainClassHighOutData]:
    p_user_id = user_id
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainClassHighOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_transport_user_train_class_by_user_id(%s, %s, %s)",
                [p_user_id, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_transport_user_train_class_by_user_id_fetchone(
    conn: Connection,
    user_id : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime]
) -> Optional[TransportUserTrainClassHighOutData]:
    p_user_id = user_id
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainClassHighOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_transport_user_train_class_by_user_id(%s, %s, %s)",
                [p_user_id, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_top_transport_user_train_classes_by_user_id_fetchall(
    conn: Connection,
    user_id : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime],
    rows_to_return : Optional[int]
) -> list[TransportUserTrainClassHighOutData]:
    p_user_id = user_id
    p_search_start = search_start
    p_search_end = search_end
    p_rows_to_return = rows_to_return
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainClassHighOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_top_transport_user_train_classes_by_user_id(%s, %s, %s, %s)",
                [p_user_id, p_search_start, p_search_end, p_rows_to_return]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_top_transport_user_train_classes_by_user_id_fetchone(
    conn: Connection,
    user_id : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime],
    rows_to_return : Optional[int]
) -> Optional[TransportUserTrainClassHighOutData]:
    p_user_id = user_id
    p_search_start = search_start
    p_search_end = search_end
    p_rows_to_return = rows_to_return
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainClassHighOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_top_transport_user_train_classes_by_user_id(%s, %s, %s, %s)",
                [p_user_id, p_search_start, p_search_end, p_rows_to_return]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_transport_user_train_class_stats_by_user_id_fetchall(
    conn: Connection,
    user_id : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime]
) -> list[TransportUserTrainClassStats]:
    p_user_id = user_id
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainClassStats)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_transport_user_train_class_stats_by_user_id(%s, %s, %s)",
                [p_user_id, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_transport_user_train_class_stats_by_user_id_fetchone(
    conn: Connection,
    user_id : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime]
) -> Optional[TransportUserTrainClassStats]:
    p_user_id = user_id
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainClassStats)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_transport_user_train_class_stats_by_user_id(%s, %s, %s)",
                [p_user_id, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_transport_user_train_unit_by_user_id_and_number_fetchall(
    conn: Connection,
    user_id : int,
    stock_number : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime]
) -> list[TransportUserTrainUnitOutData]:
    p_user_id = user_id
    p_stock_number = stock_number
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainUnitOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_transport_user_train_unit_by_user_id_and_number(%s, %s, %s, %s)",
                [p_user_id, p_stock_number, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_transport_user_train_unit_by_user_id_and_number_fetchone(
    conn: Connection,
    user_id : int,
    stock_number : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime]
) -> Optional[TransportUserTrainUnitOutData]:
    p_user_id = user_id
    p_stock_number = stock_number
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainUnitOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_transport_user_train_unit_by_user_id_and_number(%s, %s, %s, %s)",
                [p_user_id, p_stock_number, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_transport_user_train_unit_by_user_id_fetchall(
    conn: Connection,
    user_id : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime]
) -> list[TransportUserTrainUnitHighOutData]:
    p_user_id = user_id
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainUnitHighOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_transport_user_train_unit_by_user_id(%s, %s, %s)",
                [p_user_id, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_transport_user_train_unit_by_user_id_fetchone(
    conn: Connection,
    user_id : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime]
) -> Optional[TransportUserTrainUnitHighOutData]:
    p_user_id = user_id
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainUnitHighOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_transport_user_train_unit_by_user_id(%s, %s, %s)",
                [p_user_id, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_top_transport_user_train_units_by_user_id_fetchall(
    conn: Connection,
    user_id : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime],
    rows_to_return : int
) -> list[TransportUserTrainUnitHighOutData]:
    p_user_id = user_id
    p_search_start = search_start
    p_search_end = search_end
    p_rows_to_return = rows_to_return
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainUnitHighOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_top_transport_user_train_units_by_user_id(%s, %s, %s, %s)",
                [p_user_id, p_search_start, p_search_end, p_rows_to_return]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_top_transport_user_train_units_by_user_id_fetchone(
    conn: Connection,
    user_id : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime],
    rows_to_return : int
) -> Optional[TransportUserTrainUnitHighOutData]:
    p_user_id = user_id
    p_search_start = search_start
    p_search_end = search_end
    p_rows_to_return = rows_to_return
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainUnitHighOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_top_transport_user_train_units_by_user_id(%s, %s, %s, %s)",
                [p_user_id, p_search_start, p_search_end, p_rows_to_return]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_transport_user_train_unit_stats_by_user_id_fetchall(
    conn: Connection,
    user_id : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime]
) -> list[TransportUserTrainUnitStats]:
    p_user_id = user_id
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainUnitStats)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_transport_user_train_unit_stats_by_user_id(%s, %s, %s)",
                [p_user_id, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_transport_user_train_unit_stats_by_user_id_fetchone(
    conn: Connection,
    user_id : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime]
) -> Optional[TransportUserTrainUnitStats]:
    p_user_id = user_id
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainUnitStats)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_transport_user_train_unit_stats_by_user_id(%s, %s, %s)",
                [p_user_id, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise