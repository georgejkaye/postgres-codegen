from dataclasses import dataclass

from postgrescodegen.classes.postgres.core import (
    PostgresObject,
    get_python_name_for_postgres_type_name,
)


@dataclass
class PostgresCompositeField:
    field_name: str
    field_type: str


@dataclass
class PostgresComposite(PostgresObject):
    type_name: str
    composite_fields: list[PostgresCompositeField]

    def get_name(self) -> str:
        return self.type_name

    def get_drop_statement(self) -> str:
        return f"DROP TYPE IF EXISTS {self.type_name} CASCADE;"

    def get_python_name(self) -> str:
        return get_python_name_for_postgres_type_name(self.type_name)
