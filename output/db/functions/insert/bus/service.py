from typing import (
   Optional,
)

from psycopg import Connection

from api.db.types.bus.service import (
   BusServiceInData,
   BusServiceViaInData,
)


def insert_bus_services(
    conn: Connection,
    services : list[BusServiceInData]
) -> None:
    p_services = services
    try:
        conn.execute(
            "SELECT * FROM insert_bus_services(%s)",
            [p_services]
        )
        conn.commit()
    except:
        conn.rollback()
        raise


def insert_bus_service_vias(
    conn: Connection,
    vias : list[BusServiceViaInData]
) -> None:
    p_vias = vias
    try:
        conn.execute(
            "SELECT * FROM insert_bus_service_vias(%s)",
            [p_vias]
        )
        conn.commit()
    except:
        conn.rollback()
        raise


def insert_transxchange_bus_data(
    conn: Connection,
    services : list[BusServiceInData],
    vias : list[BusServiceViaInData]
) -> None:
    p_services = services
    p_vias = vias
    try:
        conn.execute(
            "SELECT * FROM insert_transxchange_bus_data(%s, %s)",
            [p_services, p_vias]
        )
        conn.commit()
    except:
        conn.rollback()
        raise