from abc import abstractmethod

from postgrescodegen.postgres.core import PostgresObject
from postgrescodegen.postgres.types import PostgresTypes


class DumperTypes:
    @staticmethod
    @abstractmethod
    def from_postgres_base_type(type_name: str) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_optional_type(type_name: str) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_list_type(type_name: str) -> str:
        pass

    @staticmethod
    @abstractmethod
    def from_postgres_type(postgres_type: str) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_composite_type_name(postgres_type: str) -> str:
        pass


class Dumper[T: PostgresObject]:
    @staticmethod
    @abstractmethod
    def get_code_for_object(postgres_object: T) -> str:
        pass


class DumperProcessor[PG: PostgresObject, T: DumperTypes]:
    def __init__(self, dumper: Dumper[PG], dumper_types: T):
        self.dumper = dumper
        self.dumper_types = dumper_types

    def from_postgres_type(self, postgres_type: str) -> str:
        postgres_base_type = PostgresTypes.get_base_type(postgres_type)
        dumped_base_type = self.dumper_types.from_postgres_base_type(
            postgres_base_type
        )
        if PostgresTypes.is_array(postgres_type):
            if PostgresTypes.is_nullable(postgres_type[:-2]):
                dumped_base_type = self.dumper_types.get_optional_type(
                    dumped_base_type
                )
            return self.dumper_types.get_list_type(dumped_base_type)
        if PostgresTypes.is_nullable(postgres_type):
            dumped_base_type = self.dumper_types.get_optional_type(
                dumped_base_type
            )
        return dumped_base_type
