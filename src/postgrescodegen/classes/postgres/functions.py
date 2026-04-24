from dataclasses import dataclass

from postgrescodegen.classes.postgres.core import PostgresObject


@dataclass
class PostgresFunctionArgument:
    argument_name: str
    argument_type: str


@dataclass
class PostgresFunction(PostgresObject):
    function_name: str
    function_return: str
    function_args: list[PostgresFunctionArgument]

    def get_name(self) -> str:
        return self.function_name

    def get_drop_statement(self) -> str:
        return f"DROP FUNCTION IF EXISTS {self.function_name};"

    def get_python_name(self) -> str:
        return self.function_name.lower()
