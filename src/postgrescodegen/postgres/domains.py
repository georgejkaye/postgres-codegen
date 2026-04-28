from dataclasses import dataclass

from postgrescodegen.generators.python.core import PythonableObject
from postgrescodegen.generators.translators.names import (
    get_python_name_for_postgres_type_name,
)
from postgrescodegen.postgres.core import (
    PostgresObject,
)


@dataclass
class PostgresDomain(PostgresObject, PythonableObject):
    domain_name: str
    underlying_type: str

    def get_name(self) -> str:
        return self.domain_name

    def get_drop_statement(self) -> str:
        return f"DROP DOMAIN IF EXISTS {self.domain_name} CASCADE;"

    def get_python_name(self) -> str:
        return get_python_name_for_postgres_type_name(self.underlying_type)
