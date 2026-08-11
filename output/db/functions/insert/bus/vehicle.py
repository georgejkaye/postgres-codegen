from typing import (
   Optional,
)

from psycopg import Connection

from api.db.types.bus.vehicle import (
   BusModelInData,
   BusVehicleInData,
)


def insert_bus_models(
    conn: Connection,
    models : list[BusModelInData]
) -> None:
    p_models = models
    try:
        conn.execute(
            "SELECT * FROM insert_bus_models(%s)",
            [p_models]
        )
        conn.commit()
    except:
        conn.rollback()
        raise


def insert_bus_vehicles(
    conn: Connection,
    vehicles : list[BusVehicleInData]
) -> None:
    p_vehicles = vehicles
    try:
        conn.execute(
            "SELECT * FROM insert_bus_vehicles(%s)",
            [p_vehicles]
        )
        conn.commit()
    except:
        conn.rollback()
        raise


def insert_bus_models_and_vehicles(
    conn: Connection,
    models : list[BusModelInData],
    vehicles : list[BusVehicleInData]
) -> None:
    p_models = models
    p_vehicles = vehicles
    try:
        conn.execute(
            "SELECT * FROM insert_bus_models_and_vehicles(%s, %s)",
            [p_models, p_vehicles]
        )
        conn.commit()
    except:
        conn.rollback()
        raise