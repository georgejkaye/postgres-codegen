from typing import (
   Optional,
)

from psycopg import Connection
from psycopg.rows import class_row

from api.db.types.user.user import (
   TransportUserOutData,
   TransportUserPublicOutData,
)


def select_users_fetchall(
    conn: Connection
) -> list[TransportUserOutData]:
    try:
        with conn.cursor(row_factory=class_row(TransportUserOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_users()",
                []
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_users_fetchone(
    conn: Connection
) -> Optional[TransportUserOutData]:
    try:
        with conn.cursor(row_factory=class_row(TransportUserOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_users()",
                []
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_user_public_data_fetchall(
    conn: Connection
) -> list[TransportUserPublicOutData]:
    try:
        with conn.cursor(row_factory=class_row(TransportUserPublicOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_user_public_data()",
                []
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_user_public_data_fetchone(
    conn: Connection
) -> Optional[TransportUserPublicOutData]:
    try:
        with conn.cursor(row_factory=class_row(TransportUserPublicOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_user_public_data()",
                []
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise


def select_user_by_username_fetchall(
    conn: Connection,
    username : Optional[str]
) -> list[TransportUserOutData]:
    p_username = username
    try:
        with conn.cursor(row_factory=class_row(TransportUserOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_user_by_username(%s)",
                [p_username]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def select_user_by_username_fetchone(
    conn: Connection,
    username : Optional[str]
) -> Optional[TransportUserOutData]:
    p_username = username
    try:
        with conn.cursor(row_factory=class_row(TransportUserOutData)) as cur:
            rows = cur.execute(
                "SELECT * FROM select_user_by_username(%s)",
                [p_username]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise