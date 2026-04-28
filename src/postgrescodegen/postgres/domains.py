from dataclasses import dataclass

from postgrescodegen.postgres.core import (
    PostgresObject,
)


@dataclass
class PostgresDomain(PostgresObject):
    domain_name: str
    underlying_type: str

    def get_name(self) -> str:
        return self.domain_name

    def get_drop_statement(self) -> str:
        return f"DROP DOMAIN IF EXISTS {self.domain_name} CASCADE;"
