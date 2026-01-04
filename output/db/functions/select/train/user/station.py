from typing import (
   Optional,
)
from datetime import (
   datetime,
)

from psycopg import Connection
from psycopg.rows import class_row

from api.db.types.user.train.station import (
   TransportUserTrainStationHighOutData,
   TransportUserTrainStationOutData,
)


def select_transport_user_train_stations_by_user_id_fetchall(
    conn: Connection,
    user_id : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime]
) -> list[TransportUserTrainStationHighOutData]:
    p_user_id = user_id
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainStationHighOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_transport_user_train_stations_by_user_id(%s, %s, %s)",
                [p_user_id, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_transport_user_train_stations_by_user_id_fetchone(
    conn: Connection,
    user_id : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime]
) -> Optional[TransportUserTrainStationHighOutData]:
    p_user_id = user_id
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainStationHighOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_transport_user_train_stations_by_user_id(%s, %s, %s)",
                [p_user_id, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_transport_user_train_station_by_user_id_and_station_id_fetchall(
    conn: Connection,
    user_id : int,
    train_station_id : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime]
) -> list[TransportUserTrainStationOutData]:
    p_user_id = user_id
    p_train_station_id = train_station_id
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainStationOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_transport_user_train_station_by_user_id_and_station_id(%s, %s, %s, %s)",
                [p_user_id, p_train_station_id, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_transport_user_train_station_by_user_id_and_station_id_fetchone(
    conn: Connection,
    user_id : int,
    train_station_id : int,
    search_start : Optional[datetime],
    search_end : Optional[datetime]
) -> Optional[TransportUserTrainStationOutData]:
    p_user_id = user_id
    p_train_station_id = train_station_id
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainStationOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_transport_user_train_station_by_user_id_and_station_id(%s, %s, %s, %s)",
                [p_user_id, p_train_station_id, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_transport_user_train_station_by_user_id_and_station_crs_fetchall(
    conn: Connection,
    user_id : int,
    station_crs : str,
    search_start : Optional[datetime],
    search_end : Optional[datetime]
) -> list[TransportUserTrainStationOutData]:
    p_user_id = user_id
    p_station_crs = station_crs
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainStationOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_transport_user_train_station_by_user_id_and_station_crs(%s, %s, %s, %s)",
                [p_user_id, p_station_crs, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_transport_user_train_station_by_user_id_and_station_crs_fetchone(
    conn: Connection,
    user_id : int,
    station_crs : str,
    search_start : Optional[datetime],
    search_end : Optional[datetime]
) -> Optional[TransportUserTrainStationOutData]:
    p_user_id = user_id
    p_station_crs = station_crs
    p_search_start = search_start
    p_search_end = search_end
    try:
        with conn.cursor(row_factory=class_row(TransportUserTrainStationOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_transport_user_train_station_by_user_id_and_station_crs(%s, %s, %s, %s)",
                [p_user_id, p_station_crs, p_search_start, p_search_end]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise