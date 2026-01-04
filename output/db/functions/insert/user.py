from typing import (
   Optional,
)

from psycopg import Connection
from psycopg.rows import class_row


def insert_user_fetchall(
    conn: Connection,
    username : Optional[str],
    display_name : Optional[str],
    hashed_password : Optional[str]
) -> list[int]:
    p_username = username
    p_display_name = display_name
    p_hashed_password = hashed_password
    try:
        with conn.cursor(row_factory=class_row(int)) as cur:
            rows = cur.execute(
                "SELECT * FROM insert_user(%s, %s, %s)",
                [p_username, p_display_name, p_hashed_password]
            )
            conn.commit()
            return rows.fetchall()
    except:
        conn.rollback()
        raise


def insert_user_fetchone(
    conn: Connection,
    username : Optional[str],
    display_name : Optional[str],
    hashed_password : Optional[str]
) -> Optional[int]:
    p_username = username
    p_display_name = display_name
    p_hashed_password = hashed_password
    try:
        with conn.cursor(row_factory=class_row(int)) as cur:
            rows = cur.execute(
                "SELECT * FROM insert_user(%s, %s, %s)",
                [p_username, p_display_name, p_hashed_password]
            )
            conn.commit()
            return rows.fetchone()
    except:
        conn.rollback()
        raise