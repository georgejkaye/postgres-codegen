from psycopg import Connection
from psycopg.types.composite import CompositeInfo, register_composite


def register_type(conn: Connection, name: str, factory: type):
    info = CompositeInfo.fetch(conn, name)
    if info is not None:
        register_composite(info, conn, factory)
    else:
        raise RuntimeError(f"Could not find composite type {name}")
