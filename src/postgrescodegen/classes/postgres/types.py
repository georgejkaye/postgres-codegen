from dataclasses import dataclass

from postgrescodegen.classes.postgres.core import PostgresObject


@dataclass
class PostgresTypeField:
    field_name: str
    field_type: str


def get_python_name_for_postgres_type_name(postgres_type_name: str) -> str:
    snake_case_name = "".join(
        x.capitalize() for x in postgres_type_name.lower().split("_")
    )
    if postgres_type_name[-8:].lower() == "_notnull":
        return snake_case_name[:-8]
    return snake_case_name


@dataclass
class PostgresType(PostgresObject):
    type_name: str
    type_fields: list[PostgresTypeField]

    def get_name(self) -> str:
        return self.type_name

    def get_drop_statement(self) -> str:
        return f"DROP TYPE IF EXISTS {self.type_name} CASCADE;"

    def get_python_name(self) -> str:
        return get_python_name_for_postgres_type_name(self.type_name)
