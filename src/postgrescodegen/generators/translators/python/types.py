from postgrescodegen.generators.translators.python.names import (
    get_python_name_for_postgres_type_name,
)


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


def get_python_type_for_postgres_base_type(base_type_string: str) -> str:
    if (
        base_python_type := postgres_to_python_type_dict.get(base_type_string)
    ) is not None:
        return base_python_type
    return get_python_name_for_postgres_type_name(base_type_string)


def get_base_python_type_for_python_type(python_type: str) -> str:
    if len(python_type) > 5 and python_type[:5] == "list[":
        return get_base_python_type_for_python_type(python_type[5:-1])
    if len(python_type) > 9 and python_type[:9] == "Optional[":
        return get_base_python_type_for_python_type(python_type[9:-1])
    return python_type
