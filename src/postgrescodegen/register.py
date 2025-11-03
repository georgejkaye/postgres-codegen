from postgrescodegen.classes import (
    PostgresDomain,
    PostgresType,
    PythonImportDict,
    PythonPostgresModuleLookup,
    PythonableObject,
    PythonablePostgresObject,
)
from postgrescodegen.generator import (
    get_import_statements_for_python_import_dict,
    update_python_type_import_dict,
)

tab = "    "


def get_register_type_function() -> str:
    lines = [
        "def register_type(conn: Connection, type_name: str, factory: type):",
        f"{tab}info = CompositeInfo.fetch(conn, type_name)",
        f"{tab}if info is not None:",
        f"{tab * 2}register_composite(info, conn, factory)",
        f"{tab}else:",
        f'{tab*2}raise RuntimeError(f"Could not find composite type {{type_name}}")',
    ]
    return "\n".join(lines)


def get_register_composite_domain_function() -> str:
    lines = [
        "def register_domain(conn: Connection, domain_name: str, underlying_type_name: str, factory: type):",
        f"{tab}domain_info = CompositeInfo.fetch(conn, domain_name)",
        f"{tab}underlying_type_info = CompositeInfo.fetch(conn, underlying_type_name)",
        f"{tab}if domain_info is not None and underlying_type_info is not None:",
        f"{tab * 2}domain_info.field_names = underlying_type_info.field_names",
        f"{tab * 2}domain_info.field_types = underlying_type_info.field_types",
        f"{tab * 2}domain_info.array_oid = underlying_type_info.array_oid",
        f"{tab * 2}register_composite(domain_info, conn, factory)",
        f"{tab}elif domain_info is None:",
        f'{tab*2}raise RuntimeError(f"Could not find domain {{domain_name}}")',
        f"{tab}else:",
        f'{tab*2}raise RuntimeError(f"Could not find underlying type {{underlying_type_name}}")',
    ]
    return "\n".join(lines)


def get_register_domain_type_function() -> str:
    lines = [
        "def register_domain_type(conn: Connection, domain_name: str):",
        f"{tab}info = TypeInfo.fetch(conn, domain_name)",
        f"{tab}if info is not None:",
        f"{tab * 2}info.register(conn)",
        f"{tab}else:",
        f'{tab*2}raise RuntimeError(f"Could not find primitive notnull domain {{domain_name}}")',
    ]
    return "\n".join(lines)


def get_register_type_function_call(
    indent: int, postgres_type: PythonablePostgresObject
) -> str:
    return f'{tab * indent}register_type(conn, "{postgres_type.get_name()}", {postgres_type.get_python_name()})'


def get_register_composite_domain_type_function_call(
    indent: int, postgres_domain: PostgresDomain
) -> str:
    return f'{tab * indent}register_composite_domain_type(conn, "{postgres_domain.domain_name}")'


def get_register_domain_type_function_call(indent: int, postgres_domain: str) -> str:
    return f'{tab * indent}register_domain_type(conn, "{postgres_domain}")'


primitive_notnull_domains = [
    "TEXT_NOTNULL",
    "INTEGER_NOTNULL",
    "BIGINT_NOTNULL",
    "DECIMAL_NOTNULL",
    "TIMESTAMP_NOTNULL",
    "INTERVAL_NOTNULL",
    "DATERANGE_NOTNULL",
    "BOOLEAN_NOTNULL",
]


def get_register_types_function_calls(
    indent: int,
    postgres_types: list[PostgresType],
    postgres_domains: list[PostgresDomain],
) -> str:
    python_type_registers = "\n".join(
        get_register_type_function_call(indent, postgres_type)
        for postgres_type in postgres_types
    )
    python_primitive_notnull_domain_registers = "\n".join(
        get_register_domain_type_function_call(indent, domain_name)
        for domain_name in primitive_notnull_domains
    )
    python_domain_registers = "\n".join(
        get_register_domain_type_function_call(indent, postgres_domain.domain_name)
        for postgres_domain in postgres_domains
    )
    python_domain_composite_registers = "\n".join(
        get_register_composite_domain_type_function_call(indent, postgres_domain)
        for postgres_domain in postgres_domains
    )
    return "\n\n".join(
        [
            python_type_registers,
            python_primitive_notnull_domain_registers,
            python_domain_registers,
            python_domain_composite_registers,
        ]
    )


def update_python_type_import_dict_for_type_name(
    python_postgres_module_lookup: PythonPostgresModuleLookup,
    python_type: PythonableObject,
    import_dict: PythonImportDict,
) -> PythonImportDict:
    python_name = python_type.get_python_name()
    module_name = python_postgres_module_lookup[python_name]
    import_dict = update_python_type_import_dict(import_dict, module_name, python_name)
    return import_dict


def get_register_types_imports(
    python_postgres_module_lookup: PythonPostgresModuleLookup,
    postgres_types: list[PostgresType],
    postgres_domains: list[PostgresDomain],
) -> str:
    import_dict: PythonImportDict = {}
    for postgres_type in postgres_types:
        import_dict = update_python_type_import_dict_for_type_name(
            python_postgres_module_lookup, postgres_type, import_dict
        )
    for postgres_domain in postgres_domains:
        import_dict = update_python_type_import_dict_for_type_name(
            python_postgres_module_lookup, postgres_domain, import_dict
        )
    return get_import_statements_for_python_import_dict(import_dict)


def get_register_all_types_function(
    postgres_types: list[PostgresType],
    postgres_domains: list[PostgresDomain],
) -> str:
    function_declaration = "def register_types(conn: Connection):"
    return f"{function_declaration}\n{get_register_types_function_calls(1, postgres_types, postgres_domains)}"


def get_register_module_code(
    python_postgres_module_lookup: PythonPostgresModuleLookup,
    postgres_types: list[PostgresType],
    postgres_domains: list[PostgresDomain],
) -> str:
    psycopg_imports = "\n".join(
        [
            "from psycopg import Connection",
            "from psycopg.types import TypeInfo",
            "from psycopg.types.composite import CompositeInfo, register_composite",
        ]
    )
    type_imports = get_register_types_imports(
        python_postgres_module_lookup, postgres_types, postgres_domains
    )
    imports = "\n\n".join([psycopg_imports, type_imports])
    register_type_function = get_register_type_function()
    register_domain_function = get_register_composite_domain_function()
    register_primitive_notnull_domain_function = get_register_domain_type_function()
    register_all_types_function = get_register_all_types_function(
        postgres_types, postgres_domains
    )
    return "\n\n\n".join(
        [
            imports,
            register_type_function,
            register_domain_function,
            register_primitive_notnull_domain_function,
            register_all_types_function,
        ]
    )
