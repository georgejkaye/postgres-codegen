from typing import Optional

from postgrescodegen.pgtypes import (
    get_base_postgres_type_for_postgres_type,
    is_postgres_array_type,
)
from postgrescodegen.pynames import get_python_name_for_postgres_type_name

postgres_to_python_type_dict = {
    "VOID": "None",
    "TEXT": "Optional[str]",
    "TEXT_NOTNULL": "str",
    "INT": "Optional[int]",
    "INTEGER": "Optional[int]",
    "INTEGER_NOTNULL": "int",
    "BIGINT": "Optional[int]",
    "BIGINT_NOTNULL": "int",
    "DECIMAL": "Optional[Decimal]",
    "NUMERIC": "Optional[Decimal]",
    "DECIMAL_NOTNULL": "Decimal",
    "TIMESTAMP WITH TIME ZONE": "Optional[datetime]",
    "TIMESTAMP WITHOUT TIME ZONE": "Optional[datetime]",
    "TIMESTAMP_NOTNULL": "datetime",
    "INTERVAL": "Optional[timedelta]",
    "INTERVAL_NOTNULL": "timedelta",
    "DATERANGE": "Optional[Range[datetime]]",
    "DATERANGE_NOTNULL": "Range[datetime]",
    "BOOLEAN": "Optional[bool]",
    "BOOLEAN_NOTNULL": "bool",
}


def get_python_type_for_base_type_of_postgres_type(
    postgres_type_name: str,
) -> Optional[str]:
    if postgres_type_name[-2:] == "[]":
        postgres_type_name = postgres_type_name[:-2]
    return postgres_to_python_type_dict.get(postgres_type_name)


def is_user_defined_type(postgres_type_name: str) -> bool:
    return get_python_type_for_base_type_of_postgres_type(postgres_type_name) is None


def get_python_type_for_postgres_base_type(base_type_string: str) -> str:
    if (
        base_python_type := postgres_to_python_type_dict.get(base_type_string)
    ) is not None:
        return base_python_type
    return get_python_name_for_postgres_type_name(base_type_string)


def get_python_type_for_postgres_type(type_string: str) -> str:
    base_type_string = get_base_postgres_type_for_postgres_type(type_string)
    base_python_type = get_python_type_for_postgres_base_type(base_type_string)
    if is_postgres_array_type(type_string):
        return f"list[{base_python_type}]"
    return base_python_type
