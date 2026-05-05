from abc import abstractmethod
from postgrescodegen.dumpers.dumper import Dumper
from postgrescodegen.postgres.functions import PostgresFunction


class FunctionDumper(Dumper[PostgresFunction]):
    @staticmethod
    @abstractmethod
    def get_fetchone_code(function: PostgresFunction) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_fetchall_code(function: PostgresFunction) -> str:
        pass
