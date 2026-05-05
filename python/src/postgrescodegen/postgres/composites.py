from dataclasses import dataclass

from postgrescodegen.postgres.core import (
    PostgresObject,
)


@dataclass
class PostgresCompositeField:
    field_name: str
    field_type: str


@dataclass
class PostgresComposite(PostgresObject):
    type_name: str
    composite_fields: list[PostgresCompositeField]

    @staticmethod
    def get_statement_regex() -> str:
        return r"CREATE TYPE (.*) AS \((.*)\)"

    def get_name(self) -> str:
        return self.type_name

    def get_drop_statement(self) -> str:
        return f"DROP TYPE IF EXISTS {self.type_name} CASCADE;"
