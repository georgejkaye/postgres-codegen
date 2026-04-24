from dataclasses import dataclass

from postgrescodegen.classes.postgres.core import PostgresObject
from postgrescodegen.classes.postgres.types import (
    get_python_name_for_postgres_type_name,
)


@dataclass
class PostgresDomain(PostgresObject):
    domain_name: str
    underlying_type: str

    def get_name(self) -> str:
        return self.domain_name

    def get_drop_statement(self) -> str:
        return f"DROP DOMAIN IF EXISTS {self.domain_name} CASCADE;"

    def get_python_name(self) -> str:
        return get_python_name_for_postgres_type_name(self.underlying_type)
