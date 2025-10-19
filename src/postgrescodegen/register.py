from postgrescodegen.classes import (
    PostgresType,
    PythonImportDict,
    PythonPostgresModuleLookup,
)
from postgrescodegen.generator import (
    get_import_statements_for_python_import_dict,
    update_python_type_import_dict,
)

tab = "    "


def get_register_type_function() -> str:
    lines = [
        "def register_type(conn: Connection, name: str, factory: type):",
        f"{tab}info = CompositeInfo.fetch(conn, name)",
        f"{tab}if info is not None:",
        f"{tab * 2}register_composite(info, conn, factory)",
        f"{tab}else:",
        f'{tab*2}raise RuntimeError(f"Could not find composite type {{name}}")',
    ]
    return "\n".join(lines)


def get_register_type_function_call(indent: int, postgres_type: PostgresType) -> str:
    return f'{tab * indent}register_type(conn, "{postgres_type.type_name}", {postgres_type.get_python_name()})'


def get_register_types_function_calls(
    indent: int, postgres_types: list[PostgresType]
) -> str:
    return "\n".join(
        get_register_type_function_call(indent, postgres_type)
        for postgres_type in postgres_types
    )


def get_register_types_imports(
    python_postgres_module_lookup: PythonPostgresModuleLookup,
    postgres_types: list[PostgresType],
) -> str:
    import_dict: PythonImportDict = {}
    for postgres_type in postgres_types:
        module_name = python_postgres_module_lookup[postgres_type.get_python_name()]
        python_name = postgres_type.get_python_name()
        import_dict = update_python_type_import_dict(
            import_dict, module_name, python_name
        )
    return get_import_statements_for_python_import_dict(import_dict)


def get_register_all_types_function(
    postgres_types: list[PostgresType],
) -> str:
    function_declaration = "def register_types(conn: Connection):"
    return f"{function_declaration}\n{get_register_types_function_calls(1, postgres_types)}"


def get_register_module_code(
    python_postgres_module_lookup: PythonPostgresModuleLookup,
    postgres_types: list[PostgresType],
) -> str:
    psycopg_imports = "\n".join(
        [
            "from psycopg import Connection",
            "from psycopg.types.composite import CompositeInfo, register_composite",
        ]
    )
    type_imports = get_register_types_imports(
        python_postgres_module_lookup, postgres_types
    )
    imports = "\n\n".join([psycopg_imports, type_imports])
    register_type_function = get_register_type_function()
    register_all_types_function = get_register_all_types_function(postgres_types)
    return "\n\n\n".join([imports, register_type_function, register_all_types_function])
