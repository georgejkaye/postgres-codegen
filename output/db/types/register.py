from typing import Any, Optional, Sequence


from psycopg import Connection
from psycopg.types import TypeInfo
from psycopg.types.composite import CompositeInfo, register_composite

from api.db.types.bus.operator import (
   BusOperatorDetails,
   BusOperatorInData,
)
from api.db.types.bus.vehicle import (
   BusModelInData,
   BusVehicleDetails,
   BusVehicleInData,
)
from api.db.types.bus.journey import (
   BusCallInData,
   BusCallStopDetails,
   BusJourneyCallDetails,
   BusJourneyDetails,
   BusJourneyInData,
   BusJourneyServiceDetails,
)
from api.db.types.bus.leg import (
   BusLegInData,
)
from api.db.types.bus.service import (
   BusServiceDetails,
   BusServiceInData,
   BusServiceViaInData,
)
from api.db.types.bus.stop import (
   BusStopDetails,
   BusStopInData,
)
from api.db.types.bus.user.leg import (
   BusCallDetails,
   BusLegServiceDetails,
   BusLegUserDetails,
   InsertBusLegResult,
)
from api.db.types.bus.user.stop import (
   BusStopLegDetails,
   BusStopUserDetails,
)
from api.db.types.bus.user.vehicle import (
   BusVehicleLegDetails,
   BusVehicleUserDetails,
)
from api.db.types.train.operator import (
   TrainBrandOutData,
   TrainOperatorDetailsOutData,
   TrainOperatorHighOutData,
   TrainOperatorOutData,
)
from api.db.types.train.station import (
   TrainStationHighOutData,
   TrainStationLegNamesInData,
   TrainStationLegPointsOutData,
   TrainStationNamePointInData,
   TrainStationOutData,
   TrainStationPointOutData,
   TrainStationPointsOutData,
)
from api.db.types.train.leg import (
   InsertTrainLegResult,
   TrainLegAssociatedServiceInData,
   TrainLegAssociatedServiceOutData,
   TrainLegCallCallInData,
   TrainLegCallInData,
   TrainLegCallOutData,
   TrainLegCallPointOutData,
   TrainLegCallPointsOutData,
   TrainLegInData,
   TrainLegOutData,
   TrainLegPointsOutData,
   TrainLegServiceCallAssociatedServiceInData,
   TrainLegServiceCallInData,
   TrainLegServiceEndpointInData,
   TrainLegServiceInData,
   TrainLegServiceOutData,
   TrainLegStockReportOutData,
   TrainLegStockSegmentInData,
   TrainLegStockSegmentOutData,
)
from api.db.types.train.stock import (
   TrainStockOutData,
   TrainStockReportOutData,
   TrainStockSubclassOutData,
)
from api.db.types.user.train.station import (
   TransportUserTrainStationHighOutData,
   TransportUserTrainStationLegOutData,
   TransportUserTrainStationOutData,
)
from api.db.types.user.train.leg import (
   TransportUserTrainLegOutData,
   TransportUserTrainLegStats,
)
from api.db.types.user.train.operator import (
   TransportUserTrainOperatorHighOutData,
   TransportUserTrainOperatorOutData,
   TransportUserTrainOperatorStats,
   TransportUserTrainOperatorTrainLegOutData,
)
from api.db.types.user.train.vehicle import (
   TransportUserTrainClassHighOutData,
   TransportUserTrainClassLegOutData,
   TransportUserTrainClassLegUnitOutData,
   TransportUserTrainClassOutData,
   TransportUserTrainClassStats,
   TransportUserTrainLegUnitSegmentOutData,
   TransportUserTrainUnitHighOutData,
   TransportUserTrainUnitLegOutData,
   TransportUserTrainUnitOutData,
   TransportUserTrainUnitStats,
)
from api.db.types.user.user import (
   TransportUserOutData,
   TransportUserPublicOutData,
)
from psycopg.types.numeric import (
   IntLoader,
   NumericLoader,
)
from psycopg.types.datetime import (
   IntervalLoader,
   TimestamptzLoader,
)
from psycopg.types.range import (
   DateRangeLoader,
)
from psycopg.types.bool import (
   BoolLoader,
)


def make_sequence(t : object, info : CompositeInfo) -> Sequence[Any]:
    return [getattr(t, name) for name in info.field_names]


def register_composite_type(
    conn: Connection,
    type_name: str,
    factory: type
) -> None:
    info = CompositeInfo.fetch(conn, type_name)
    if info is not None:
        register_composite(info, conn, factory, make_sequence=make_sequence)
    else:
        raise RuntimeError(f"Could not find composite type {type_name}")


def register_composite_domain_type(
    conn: Connection,
    domain_name: str,
    underlying_type_name: str,
    factory: type
) -> None:
    domain_info = CompositeInfo.fetch(conn, domain_name)
    underlying_type_info = CompositeInfo.fetch(conn, underlying_type_name)
    if domain_info is not None and underlying_type_info is not None:
        domain_info.register(conn)
        domain_info.field_names = underlying_type_info.field_names
        domain_info.field_types = underlying_type_info.field_types
        domain_info.array_oid = underlying_type_info.array_oid
        register_composite(domain_info, conn, factory, make_sequence=make_sequence)
    elif domain_info is None:
        raise RuntimeError(f"Could not find domain {domain_name}")
    else:
        raise RuntimeError(f"Could not find underlying type {underlying_type_name}")


def register_domain_type(
    conn: Connection,
    domain_name: str,
    loader: Optional[type]
) -> None:
    info = TypeInfo.fetch(conn, domain_name)
    if info is not None:
        info.register(conn)
        if loader is not None:
            conn.adapters.register_loader(domain_name, loader)
    else:
        raise RuntimeError(f"Could not find domain type {domain_name}")


def register_types(conn: Connection):
    register_composite_type(conn, "bus_operator_in_data", BusOperatorInData)
    register_composite_type(conn, "bus_operator_details", BusOperatorDetails)
    register_composite_type(conn, "bus_model_in_data", BusModelInData)
    register_composite_type(conn, "bus_vehicle_in_data", BusVehicleInData)
    register_composite_type(conn, "bus_vehicle_details", BusVehicleDetails)
    register_composite_type(conn, "bus_call_in_data", BusCallInData)
    register_composite_type(conn, "bus_journey_in_data", BusJourneyInData)
    register_composite_type(conn, "bus_journey_service_details", BusJourneyServiceDetails)
    register_composite_type(conn, "bus_call_stop_details", BusCallStopDetails)
    register_composite_type(conn, "bus_journey_call_details", BusJourneyCallDetails)
    register_composite_type(conn, "bus_journey_details", BusJourneyDetails)
    register_composite_type(conn, "bus_leg_in_data", BusLegInData)
    register_composite_type(conn, "bus_service_in_data", BusServiceInData)
    register_composite_type(conn, "bus_service_via_in_data", BusServiceViaInData)
    register_composite_type(conn, "bus_service_details", BusServiceDetails)
    register_composite_type(conn, "bus_stop_in_data", BusStopInData)
    register_composite_type(conn, "bus_stop_details", BusStopDetails)
    register_composite_type(conn, "bus_leg_service_details", BusLegServiceDetails)
    register_composite_type(conn, "bus_call_details", BusCallDetails)
    register_composite_type(conn, "bus_leg_user_details", BusLegUserDetails)
    register_composite_type(conn, "insert_bus_leg_result", InsertBusLegResult)
    register_composite_type(conn, "bus_stop_leg_details", BusStopLegDetails)
    register_composite_type(conn, "bus_stop_user_details", BusStopUserDetails)
    register_composite_type(conn, "bus_vehicle_leg_details", BusVehicleLegDetails)
    register_composite_type(conn, "bus_vehicle_user_details", BusVehicleUserDetails)
    register_composite_type(conn, "train_brand_out_data", TrainBrandOutData)
    register_composite_type(conn, "train_operator_out_data", TrainOperatorOutData)
    register_composite_type(conn, "train_operator_details_out_data", TrainOperatorDetailsOutData)
    register_composite_type(conn, "train_operator_high_out_data", TrainOperatorHighOutData)
    register_composite_type(conn, "train_station_name_point_in_data", TrainStationNamePointInData)
    register_composite_type(conn, "train_station_out_data", TrainStationOutData)
    register_composite_type(conn, "train_station_leg_names_in_data", TrainStationLegNamesInData)
    register_composite_type(conn, "train_station_point_out_data", TrainStationPointOutData)
    register_composite_type(conn, "train_station_points_out_data", TrainStationPointsOutData)
    register_composite_type(conn, "train_station_leg_points_out_data", TrainStationLegPointsOutData)
    register_composite_type(conn, "train_station_high_out_data", TrainStationHighOutData)
    register_composite_type(conn, "train_leg_service_in_data", TrainLegServiceInData)
    register_composite_type(conn, "train_leg_service_endpoint_in_data", TrainLegServiceEndpointInData)
    register_composite_type(conn, "train_leg_service_call_in_data", TrainLegServiceCallInData)
    register_composite_type(conn, "train_leg_associated_service_in_data", TrainLegAssociatedServiceInData)
    register_composite_type(conn, "train_leg_service_call_associated_service_in_data", TrainLegServiceCallAssociatedServiceInData)
    register_composite_type(conn, "train_leg_call_call_in_data", TrainLegCallCallInData)
    register_composite_type(conn, "train_leg_call_in_data", TrainLegCallInData)
    register_composite_type(conn, "train_leg_stock_segment_in_data", TrainLegStockSegmentInData)
    register_composite_type(conn, "train_leg_in_data", TrainLegInData)
    register_composite_type(conn, "train_leg_associated_service_out_data", TrainLegAssociatedServiceOutData)
    register_composite_type(conn, "train_leg_call_out_data", TrainLegCallOutData)
    register_composite_type(conn, "train_leg_service_out_data", TrainLegServiceOutData)
    register_composite_type(conn, "train_leg_stock_report_out_data", TrainLegStockReportOutData)
    register_composite_type(conn, "train_leg_stock_segment_out_data", TrainLegStockSegmentOutData)
    register_composite_type(conn, "train_leg_out_data", TrainLegOutData)
    register_composite_type(conn, "train_leg_call_point_out_data", TrainLegCallPointOutData)
    register_composite_type(conn, "train_leg_call_points_out_data", TrainLegCallPointsOutData)
    register_composite_type(conn, "train_leg_points_out_data", TrainLegPointsOutData)
    register_composite_type(conn, "insert_train_leg_result", InsertTrainLegResult)
    register_composite_type(conn, "train_stock_subclass_out_data", TrainStockSubclassOutData)
    register_composite_type(conn, "train_stock_out_data", TrainStockOutData)
    register_composite_type(conn, "train_stock_report_out_data", TrainStockReportOutData)
    register_composite_type(conn, "transport_user_train_station_leg_out_data", TransportUserTrainStationLegOutData)
    register_composite_type(conn, "transport_user_train_station_out_data", TransportUserTrainStationOutData)
    register_composite_type(conn, "transport_user_train_station_high_out_data", TransportUserTrainStationHighOutData)
    register_composite_type(conn, "transport_user_train_leg_out_data", TransportUserTrainLegOutData)
    register_composite_type(conn, "transport_user_train_leg_stats", TransportUserTrainLegStats)
    register_composite_type(conn, "transport_user_train_operator_train_leg_out_data", TransportUserTrainOperatorTrainLegOutData)
    register_composite_type(conn, "transport_user_train_operator_out_data", TransportUserTrainOperatorOutData)
    register_composite_type(conn, "transport_user_train_operator_high_out_data", TransportUserTrainOperatorHighOutData)
    register_composite_type(conn, "transport_user_train_operator_stats", TransportUserTrainOperatorStats)
    register_composite_type(conn, "transport_user_train_leg_unit_segment_out_data", TransportUserTrainLegUnitSegmentOutData)
    register_composite_type(conn, "transport_user_train_class_leg_unit_out_data", TransportUserTrainClassLegUnitOutData)
    register_composite_type(conn, "transport_user_train_class_leg_out_data", TransportUserTrainClassLegOutData)
    register_composite_type(conn, "transport_user_train_class_out_data", TransportUserTrainClassOutData)
    register_composite_type(conn, "transport_user_train_class_high_out_data", TransportUserTrainClassHighOutData)
    register_composite_type(conn, "transport_user_train_unit_leg_out_data", TransportUserTrainUnitLegOutData)
    register_composite_type(conn, "transport_user_train_unit_out_data", TransportUserTrainUnitOutData)
    register_composite_type(conn, "transport_user_train_unit_high_out_data", TransportUserTrainUnitHighOutData)
    register_composite_type(conn, "transport_user_train_class_stats", TransportUserTrainClassStats)
    register_composite_type(conn, "transport_user_train_unit_stats", TransportUserTrainUnitStats)
    register_composite_type(conn, "transport_user_out_data", TransportUserOutData)
    register_composite_type(conn, "transport_user_public_out_data", TransportUserPublicOutData)

    register_domain_type(conn, "text_notnull", None)
    register_domain_type(conn, "integer_notnull", IntLoader)
    register_domain_type(conn, "bigint_notnull", IntLoader)
    register_domain_type(conn, "decimal_notnull", NumericLoader)
    register_domain_type(conn, "timestamp_notnull", TimestamptzLoader)
    register_domain_type(conn, "interval_notnull", IntervalLoader)
    register_domain_type(conn, "daterange_notnull", DateRangeLoader)
    register_domain_type(conn, "boolean_notnull", BoolLoader)

    register_composite_domain_type(conn, "bus_operator_in_data_notnull", "bus_operator_in_data", BusOperatorInData)
    register_composite_domain_type(conn, "bus_operator_details_notnull", "bus_operator_details", BusOperatorDetails)
    register_composite_domain_type(conn, "bus_model_in_data_notnull", "bus_model_in_data", BusModelInData)
    register_composite_domain_type(conn, "bus_vehicle_in_data_notnull", "bus_vehicle_in_data", BusVehicleInData)
    register_composite_domain_type(conn, "bus_vehicle_details_notnull", "bus_vehicle_details", BusVehicleDetails)
    register_composite_domain_type(conn, "bus_call_in_data_notnull", "bus_call_in_data", BusCallInData)
    register_composite_domain_type(conn, "bus_journey_in_data_notnull", "bus_journey_in_data", BusJourneyInData)
    register_composite_domain_type(conn, "bus_journey_service_details_notnull", "bus_journey_service_details", BusJourneyServiceDetails)
    register_composite_domain_type(conn, "bus_call_stop_details_notnull", "bus_call_stop_details", BusCallStopDetails)
    register_composite_domain_type(conn, "bus_journey_call_details_notnull", "bus_journey_call_details", BusJourneyCallDetails)
    register_composite_domain_type(conn, "bus_journey_details_notnull", "bus_journey_details", BusJourneyDetails)
    register_composite_domain_type(conn, "bus_leg_in_data_notnull", "bus_leg_in_data", BusLegInData)
    register_composite_domain_type(conn, "bus_service_in_data_notnull", "bus_service_in_data", BusServiceInData)
    register_composite_domain_type(conn, "bus_service_via_in_data_notnull", "bus_service_via_in_data", BusServiceViaInData)
    register_composite_domain_type(conn, "bus_service_details_notnull", "bus_service_details", BusServiceDetails)
    register_composite_domain_type(conn, "bus_stop_in_data_notnull", "bus_stop_in_data", BusStopInData)
    register_composite_domain_type(conn, "bus_stop_details_notnull", "bus_stop_details", BusStopDetails)
    register_composite_domain_type(conn, "bus_leg_service_details_notnull", "bus_leg_service_details", BusLegServiceDetails)
    register_composite_domain_type(conn, "bus_call_details_notnull", "bus_call_details", BusCallDetails)
    register_composite_domain_type(conn, "bus_leg_user_details_notnull", "bus_leg_user_details", BusLegUserDetails)
    register_composite_domain_type(conn, "bus_stop_leg_details_notnull", "bus_stop_leg_details", BusStopLegDetails)
    register_composite_domain_type(conn, "bus_stop_user_details_notnull", "bus_stop_user_details", BusStopUserDetails)
    register_composite_domain_type(conn, "bus_vehicle_leg_details_notnull", "bus_vehicle_leg_details", BusVehicleLegDetails)
    register_composite_domain_type(conn, "bus_vehicle_user_details_notnull", "bus_vehicle_user_details", BusVehicleUserDetails)
    register_composite_domain_type(conn, "train_brand_out_data_notnull", "train_brand_out_data", TrainBrandOutData)
    register_composite_domain_type(conn, "train_operator_out_data_notnull", "train_operator_out_data", TrainOperatorOutData)
    register_composite_domain_type(conn, "train_operator_details_out_data_notnull", "train_operator_details_out_data", TrainOperatorDetailsOutData)
    register_composite_domain_type(conn, "train_operator_high_out_data_notnull", "train_operator_high_out_data", TrainOperatorHighOutData)
    register_composite_domain_type(conn, "train_station_name_point_in_data_notnull", "train_station_name_point_in_data", TrainStationNamePointInData)
    register_composite_domain_type(conn, "train_station_out_data_notnull", "train_station_out_data", TrainStationOutData)
    register_composite_domain_type(conn, "train_station_leg_names_in_data_notnull", "train_station_leg_names_in_data", TrainStationLegNamesInData)
    register_composite_domain_type(conn, "train_station_point_out_data_notnull", "train_station_point_out_data", TrainStationPointOutData)
    register_composite_domain_type(conn, "train_station_points_out_data_notnull", "train_station_points_out_data", TrainStationPointsOutData)
    register_composite_domain_type(conn, "train_station_leg_points_out_data_notnull", "train_station_leg_points_out_data", TrainStationLegPointsOutData)
    register_composite_domain_type(conn, "train_station_high_out_data_notnull", "train_station_high_out_data", TrainStationHighOutData)
    register_composite_domain_type(conn, "train_leg_service_in_data_notnull", "train_leg_service_in_data", TrainLegServiceInData)
    register_composite_domain_type(conn, "train_leg_service_endpoint_in_data_notnull", "train_leg_service_endpoint_in_data", TrainLegServiceEndpointInData)
    register_composite_domain_type(conn, "train_leg_service_call_in_data_notnull", "train_leg_service_call_in_data", TrainLegServiceCallInData)
    register_composite_domain_type(conn, "train_leg_associated_service_in_data_notnull", "train_leg_associated_service_in_data", TrainLegAssociatedServiceInData)
    register_composite_domain_type(conn, "train_leg_service_call_associated_service_in_data_notnull", "train_leg_service_call_associated_service_in_data", TrainLegServiceCallAssociatedServiceInData)
    register_composite_domain_type(conn, "train_leg_call_call_in_data_notnull", "train_leg_call_call_in_data", TrainLegCallCallInData)
    register_composite_domain_type(conn, "train_leg_call_in_data_notnull", "train_leg_call_in_data", TrainLegCallInData)
    register_composite_domain_type(conn, "train_leg_stock_segment_in_data_notnull", "train_leg_stock_segment_in_data", TrainLegStockSegmentInData)
    register_composite_domain_type(conn, "train_leg_in_data_notnull", "train_leg_in_data", TrainLegInData)
    register_composite_domain_type(conn, "train_leg_associated_service_out_data_notnull", "train_leg_associated_service_out_data", TrainLegAssociatedServiceOutData)
    register_composite_domain_type(conn, "train_leg_call_out_data_notnull", "train_leg_call_out_data", TrainLegCallOutData)
    register_composite_domain_type(conn, "train_leg_service_out_data_notnull", "train_leg_service_out_data", TrainLegServiceOutData)
    register_composite_domain_type(conn, "train_leg_stock_report_out_data_notnull", "train_leg_stock_report_out_data", TrainLegStockReportOutData)
    register_composite_domain_type(conn, "train_leg_stock_segment_out_data_notnull", "train_leg_stock_segment_out_data", TrainLegStockSegmentOutData)
    register_composite_domain_type(conn, "train_leg_out_data_notnull", "train_leg_out_data", TrainLegOutData)
    register_composite_domain_type(conn, "train_leg_call_point_out_data_notnull", "train_leg_call_point_out_data", TrainLegCallPointOutData)
    register_composite_domain_type(conn, "train_leg_call_points_out_data_notnull", "train_leg_call_points_out_data", TrainLegCallPointsOutData)
    register_composite_domain_type(conn, "train_leg_points_out_data_notnull", "train_leg_points_out_data", TrainLegPointsOutData)
    register_composite_domain_type(conn, "train_stock_subclass_out_data_notnull", "train_stock_subclass_out_data", TrainStockSubclassOutData)
    register_composite_domain_type(conn, "train_stock_out_data_notnull", "train_stock_out_data", TrainStockOutData)
    register_composite_domain_type(conn, "train_stock_report_out_data_notnull", "train_stock_report_out_data", TrainStockReportOutData)
    register_composite_domain_type(conn, "transport_user_train_station_leg_out_data_notnull", "transport_user_train_station_leg_out_data", TransportUserTrainStationLegOutData)
    register_composite_domain_type(conn, "transport_user_train_station_out_data_notnull", "transport_user_train_station_out_data", TransportUserTrainStationOutData)
    register_composite_domain_type(conn, "transport_user_train_station_high_out_data_notnull", "transport_user_train_station_high_out_data", TransportUserTrainStationHighOutData)
    register_composite_domain_type(conn, "transport_user_train_leg_out_data_notnull", "transport_user_train_leg_out_data", TransportUserTrainLegOutData)
    register_composite_domain_type(conn, "transport_user_train_operator_train_leg_out_data_notnull", "transport_user_train_operator_train_leg_out_data", TransportUserTrainOperatorTrainLegOutData)
    register_composite_domain_type(conn, "transport_user_train_operator_out_data_notnull", "transport_user_train_operator_out_data", TransportUserTrainOperatorOutData)
    register_composite_domain_type(conn, "transport_user_train_operator_high_out_data_notnull", "transport_user_train_operator_high_out_data", TransportUserTrainOperatorHighOutData)
    register_composite_domain_type(conn, "transport_user_train_leg_unit_segment_out_data_notnull", "transport_user_train_leg_unit_segment_out_data", TransportUserTrainLegUnitSegmentOutData)
    register_composite_domain_type(conn, "transport_user_train_class_leg_unit_out_data_notnull", "transport_user_train_class_leg_unit_out_data", TransportUserTrainClassLegUnitOutData)
    register_composite_domain_type(conn, "transport_user_train_class_leg_out_data_notnull", "transport_user_train_class_leg_out_data", TransportUserTrainClassLegOutData)
    register_composite_domain_type(conn, "transport_user_train_class_out_data_notnull", "transport_user_train_class_out_data", TransportUserTrainClassOutData)
    register_composite_domain_type(conn, "transport_user_train_class_high_out_data_notnull", "transport_user_train_class_high_out_data", TransportUserTrainClassHighOutData)
    register_composite_domain_type(conn, "transport_user_train_unit_out_data_notnull", "transport_user_train_unit_out_data", TransportUserTrainUnitOutData)
    register_composite_domain_type(conn, "transport_user_train_unit_high_out_data_notnull", "transport_user_train_unit_high_out_data", TransportUserTrainUnitHighOutData)
    register_composite_domain_type(conn, "transport_user_out_data_notnull", "transport_user_out_data", TransportUserOutData)
    register_composite_domain_type(conn, "transport_user_public_out_data_notnull", "transport_user_public_out_data", TransportUserPublicOutData)