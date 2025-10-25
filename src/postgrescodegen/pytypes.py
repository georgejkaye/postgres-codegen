from typing import Optional

from postgrescodegen.pgtypes import (
    get_base_postgres_type_for_postgres_type,
    is_postgres_array_type,
    is_postgres_type_nullable,
)
from postgrescodegen.pynames import get_python_name_for_postgres_type_name

postgres_to_python_type_dict = {
    "VOID": "None",
    "TEXT": "str",
    "INT": "int",
    "INTEGER": "int",
    "BIGINT": "int",
    "DECIMAL": "Decimal",
    "NUMERIC": "Decimal",
    "TIMESTAMP": "datetime",
    "TIMESTAMP WITH TIME ZONE": "datetime",
    "TIMESTAMP WITHOUT TIME ZONE": "datetime",
    "INTERVAL": "timedelta",
    "DATERANGE": "Range[datetime]",
    "BOOLEAN": "bool",
}


def get_python_type_for_base_type_of_postgres_type(
    postgres_type_name: str,
) -> Optional[str]:
    if postgres_type_name[-2:] == "[]":
        postgres_type_name = postgres_type_name[:-2]
    return postgres_to_python_type_dict.get(postgres_type_name)


def get_python_type_for_postgres_base_type(base_type_string: str) -> str:
    if (
        base_python_type := postgres_to_python_type_dict.get(base_type_string)
    ) is not None:
        return base_python_type
    return get_python_name_for_postgres_type_name(base_type_string)


def get_list_type(python_type: str) -> str:
    return f"list[{python_type}]"


def get_optional_type(python_type: str) -> str:
    return f"Optional[{python_type}]"


def get_python_type_for_postgres_type(type_string: str) -> str:
    base_type_string = get_base_postgres_type_for_postgres_type(type_string)
    base_python_type = get_python_type_for_postgres_base_type(base_type_string)
    if is_postgres_array_type(type_string):
        if is_postgres_type_nullable(type_string[:-2]):
            type_string = get_optional_type(base_python_type)
        return get_list_type(base_python_type)
    if is_postgres_type_nullable(type_string):
        base_python_type = get_optional_type(base_python_type)
    return base_python_type


def get_base_python_type_for_postgres_type(type_string: str) -> str:
    base_type_string = get_base_postgres_type_for_postgres_type(type_string)
    return get_python_type_for_postgres_base_type(base_type_string)
