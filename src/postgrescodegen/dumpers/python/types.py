from postgrescodegen.dumpers.dumper import DumperTypes


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


class PythonTypes(DumperTypes):
    @staticmethod
    def from_postgres_base_type(type_name: str) -> str:
        if (
            base_python_type := postgres_to_python_type_dict.get(type_name)
        ) is not None:
            return base_python_type
        return PythonTypes.get_composite_type_name(type_name)

    @staticmethod
    def get_optional_type(type_name: str) -> str:
        return f"Optional[{type_name}]"

    @staticmethod
    def get_list_type(type_name: str) -> str:
        return f"list[{type_name}]"

    @staticmethod
    def get_base_python_type(python_type: str) -> str:
        if len(python_type) > 5 and python_type[:5] == "list[":
            return PythonTypes.get_base_python_type(python_type[5:-1])
        if len(python_type) > 9 and python_type[:9] == "Optional[":
            return PythonTypes.get_base_python_type(python_type[9:-1])
        return python_type

    @staticmethod
    def get_composite_type_name(postgres_type: str) -> str:
        snake_case_name = "".join(
            x.capitalize() for x in postgres_type.lower().split("_")
        )
        if postgres_type[-8:].lower() == "_notnull":
            return snake_case_name[:-8]
        return snake_case_name
