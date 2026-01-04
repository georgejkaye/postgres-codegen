from typing import (
   Optional,
)

from psycopg import Connection
from psycopg.rows import class_row

from api.db.types.train.station import (
   TrainStationLegNamesInData,
   TrainStationLegPointsOutData,
   TrainStationOutData,
   TrainStationPointsOutData,
)


def select_train_station_by_crs_fetchall(
    conn: Connection,
    station_crs : str
) -> list[TrainStationOutData]:
    p_station_crs = station_crs
    try:
        with conn.cursor(row_factory=class_row(TrainStationOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_station_by_crs(%s)",
                [p_station_crs]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_train_station_by_crs_fetchone(
    conn: Connection,
    station_crs : str
) -> Optional[TrainStationOutData]:
    p_station_crs = station_crs
    try:
        with conn.cursor(row_factory=class_row(TrainStationOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_station_by_crs(%s)",
                [p_station_crs]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_train_station_by_name_fetchall(
    conn: Connection,
    station_name : str
) -> list[TrainStationOutData]:
    p_station_name = station_name
    try:
        with conn.cursor(row_factory=class_row(TrainStationOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_station_by_name(%s)",
                [p_station_name]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_train_station_by_name_fetchone(
    conn: Connection,
    station_name : str
) -> Optional[TrainStationOutData]:
    p_station_name = station_name
    try:
        with conn.cursor(row_factory=class_row(TrainStationOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_station_by_name(%s)",
                [p_station_name]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_train_stations_by_name_substring_fetchall(
    conn: Connection,
    name_substring : str
) -> list[TrainStationOutData]:
    p_name_substring = name_substring
    try:
        with conn.cursor(row_factory=class_row(TrainStationOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_stations_by_name_substring(%s)",
                [p_name_substring]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_train_stations_by_name_substring_fetchone(
    conn: Connection,
    name_substring : str
) -> Optional[TrainStationOutData]:
    p_name_substring = name_substring
    try:
        with conn.cursor(row_factory=class_row(TrainStationOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_stations_by_name_substring(%s)",
                [p_name_substring]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_train_station_points_fetchall(
    conn: Connection
) -> list[TrainStationPointsOutData]:
    try:
        with conn.cursor(row_factory=class_row(TrainStationPointsOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_station_points()",
                []
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_train_station_points_fetchone(
    conn: Connection
) -> Optional[TrainStationPointsOutData]:
    try:
        with conn.cursor(row_factory=class_row(TrainStationPointsOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_station_points()",
                []
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_train_station_points_by_crses_fetchall(
    conn: Connection,
    station_crses : list[str]
) -> list[TrainStationPointsOutData]:
    p_station_crses = station_crses
    try:
        with conn.cursor(row_factory=class_row(TrainStationPointsOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_station_points_by_crses(%s)",
                [p_station_crses]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_train_station_points_by_crses_fetchone(
    conn: Connection,
    station_crses : list[str]
) -> Optional[TrainStationPointsOutData]:
    p_station_crses = station_crses
    try:
        with conn.cursor(row_factory=class_row(TrainStationPointsOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_station_points_by_crses(%s)",
                [p_station_crses]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_train_station_points_by_name_fetchall(
    conn: Connection,
    station_name : str
) -> list[TrainStationPointsOutData]:
    p_station_name = station_name
    try:
        with conn.cursor(row_factory=class_row(TrainStationPointsOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_station_points_by_name(%s)",
                [p_station_name]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_train_station_points_by_name_fetchone(
    conn: Connection,
    station_name : str
) -> Optional[TrainStationPointsOutData]:
    p_station_name = station_name
    try:
        with conn.cursor(row_factory=class_row(TrainStationPointsOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_station_points_by_name(%s)",
                [p_station_name]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_train_station_points_by_names_fetchall(
    conn: Connection,
    station_names : list[str]
) -> list[TrainStationPointsOutData]:
    p_station_names = station_names
    try:
        with conn.cursor(row_factory=class_row(TrainStationPointsOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_station_points_by_names(%s)",
                [p_station_names]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_train_station_points_by_names_fetchone(
    conn: Connection,
    station_names : list[str]
) -> Optional[TrainStationPointsOutData]:
    p_station_names = station_names
    try:
        with conn.cursor(row_factory=class_row(TrainStationPointsOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_station_points_by_names(%s)",
                [p_station_names]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_train_station_leg_points_by_name_lists_fetchall(
    conn: Connection,
    station_names : list[TrainStationLegNamesInData]
) -> list[TrainStationLegPointsOutData]:
    p_station_names = station_names
    try:
        with conn.cursor(row_factory=class_row(TrainStationLegPointsOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_station_leg_points_by_name_lists(%s)",
                [p_station_names]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_train_station_leg_points_by_name_lists_fetchone(
    conn: Connection,
    station_names : list[TrainStationLegNamesInData]
) -> Optional[TrainStationLegPointsOutData]:
    p_station_names = station_names
    try:
        with conn.cursor(row_factory=class_row(TrainStationLegPointsOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_train_station_leg_points_by_name_lists(%s)",
                [p_station_names]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise