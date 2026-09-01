<<<<<<< HEAD:python/src/postgrescodegen/generators/python/register.py
from postgrescodegen.postgres.core import PostgresObject
from postgrescodegen.postgres.domains import PostgresDomain
from postgrescodegen.postgres.composites import PostgresComposite
from postgrescodegen.generators.python.python import (
=======
from postgrescodegen.classes import (
    PostgresDomain,
    PostgresType,
    PsycopgDomainDetails,
    PsycopgLoader,
>>>>>>> a484201a59c621dfdf218d3154460b4e347e82f6:src/postgrescodegen/register.py
    PythonImportDict,
    PythonPostgresModuleLookup,
)
from postgrescodegen.generators.python.imports import (
    get_import_statements_for_python_import_dict,
    update_python_type_import_dict,
)


tab = "    "
<<<<<<< HEAD:python/src/postgrescodegen/generators/python/register.py
notnull_domains = [
    "TEXT_NOTNULL",
    "INTEGER_NOTNULL",
    "BIGINT_NOTNULL",
    "DECIMAL_NOTNULL",
    "TIMESTAMP_NOTNULL",
    "INTERVAL_NOTNULL",
    "DATERANGE_NOTNULL",
    "BOOLEAN_NOTNULL",
]


=======


def get_make_sequence_function() -> str:
    lines = [
        "def make_sequence(t : object, info : CompositeInfo) -> Sequence[Any]:",
        f"{tab}return [getattr(t, name) for name in info.field_names]",
    ]
    return "\n".join(lines)


def get_register_composite_type_function() -> str:
    lines = [
        "def register_composite_type(",
        f"{tab}conn: Connection,",
        f"{tab}type_name: str,",
        f"{tab}factory: type",
        ") -> None:",
        f"{tab}info = CompositeInfo.fetch(conn, type_name)",
        f"{tab}if info is not None:",
        f"{tab * 2}register_composite(info, conn, factory, make_sequence=make_sequence)",
        f"{tab}else:",
        f'{tab*2}raise RuntimeError(f"Could not find composite type {{type_name}}")',
    ]
    return "\n".join(lines)


def get_register_composite_domain_function() -> str:
    lines = [
        "def register_composite_domain_type(",
        f"{tab}conn: Connection,",
        f"{tab}domain_name: str,",
        f"{tab}underlying_type_name: str,",
        f"{tab}factory: type",
        ") -> None:",
        f"{tab}domain_info = CompositeInfo.fetch(conn, domain_name)",
        f"{tab}underlying_type_info = CompositeInfo.fetch(conn, underlying_type_name)",
        f"{tab}if domain_info is not None and underlying_type_info is not None:",
        f"{tab * 2}domain_info.register(conn)",
        f"{tab * 2}domain_info.field_names = underlying_type_info.field_names",
        f"{tab * 2}domain_info.field_types = underlying_type_info.field_types",
        f"{tab * 2}domain_info.array_oid = underlying_type_info.array_oid",
        f"{tab * 2}register_composite(domain_info, conn, factory, make_sequence=make_sequence)",
        f"{tab}elif domain_info is None:",
        f'{tab*2}raise RuntimeError(f"Could not find domain {{domain_name}}")',
        f"{tab}else:",
        f'{tab*2}raise RuntimeError(f"Could not find underlying type {{underlying_type_name}}")',
    ]
    return "\n".join(lines)


def get_register_domain_type_function() -> str:
    lines = [
        "def register_domain_type(",
        f"{tab}conn: Connection,",
        f"{tab}domain_name: str,",
        f"{tab}loader: Optional[type]",
        ") -> None:",
        f"{tab}info = TypeInfo.fetch(conn, domain_name)",
        f"{tab}if info is not None:",
        f"{tab * 2}info.register(conn)",
        f"{tab * 2}if loader is not None:",
        f"{tab * 3}conn.adapters.register_loader(domain_name, loader)",
        f"{tab}else:",
        f'{tab*2}raise RuntimeError(f"Could not find domain type {{domain_name}}")',
    ]
    return "\n".join(lines)


def get_register_type_function_call(
    indent: int, postgres_type: PythonablePostgresObject
) -> str:
    return f'{tab * indent}register_composite_type(conn, "{postgres_type.get_name()}", {postgres_type.get_python_name()})'


def get_register_domain_type_function_call(
    indent: int, domain_details: PsycopgDomainDetails
) -> str:
    loader_string = (
        domain_details.loader.loader_name if domain_details.loader else "None"
    )
    return f'{tab * indent}register_domain_type(conn, "{domain_details.domain_name}", {loader_string})'


def get_register_composite_domain_type_function_call(
    indent: int, postgres_domain: PostgresDomain
) -> str:
    return f'{tab * indent}register_composite_domain_type(conn, "{postgres_domain.domain_name}", "{postgres_domain.underlying_type}", {postgres_domain.get_python_name()})'


primitive_notnull_domains = [
    PsycopgDomainDetails("text_notnull", None),
    PsycopgDomainDetails(
        "integer_notnull", PsycopgLoader("IntLoader", "psycopg.types.numeric")
    ),
    PsycopgDomainDetails(
        "bigint_notnull", PsycopgLoader("IntLoader", "psycopg.types.numeric")
    ),
    PsycopgDomainDetails(
        "decimal_notnull", PsycopgLoader("NumericLoader", "psycopg.types.numeric")
    ),
    PsycopgDomainDetails(
        "timestamp_notnull",
        PsycopgLoader("TimestamptzLoader", "psycopg.types.datetime"),
    ),
    PsycopgDomainDetails(
        "interval_notnull", PsycopgLoader("IntervalLoader", "psycopg.types.datetime")
    ),
    PsycopgDomainDetails(
        "daterange_notnull", PsycopgLoader("DateRangeLoader", "psycopg.types.range")
    ),
    PsycopgDomainDetails(
        "boolean_notnull", PsycopgLoader("BoolLoader", "psycopg.types.bool")
    ),
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
        get_register_domain_type_function_call(indent, domain)
        for domain in primitive_notnull_domains
    )
    python_domain_composite_registers = "\n".join(
        get_register_composite_domain_type_function_call(indent, postgres_domain)
        for postgres_domain in postgres_domains
    )
    return "\n\n".join(
        [
            python_type_registers,
            python_primitive_notnull_domain_registers,
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
    for primitive_domain in primitive_notnull_domains:
        if primitive_domain.loader is not None:
            python_postgres_module_lookup[primitive_domain.loader.loader_name] = (
                primitive_domain.loader.loader_module
            )
            import_dict = update_python_type_import_dict_for_type_name(
                python_postgres_module_lookup,
                primitive_domain.loader,
                import_dict,
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


>>>>>>> a484201a59c621dfdf218d3154460b4e347e82f6:src/postgrescodegen/register.py
def get_register_module_code(
    python_postgres_module_lookup: PythonPostgresModuleLookup,
    postgres_types: list[PostgresComposite],
    postgres_domains: list[PostgresDomain],
) -> str:
    psycopg_imports = "\n".join(
        [
            "from typing import Any, Optional, Sequence",
            "\n",
            "from psycopg import Connection",
            "from psycopg.types import TypeInfo",
            "from psycopg.types.composite import CompositeInfo, register_composite",
        ]
    )
    type_imports = _get_register_types_imports(
        python_postgres_module_lookup, postgres_types, postgres_domains
    )
    imports = "\n\n".join([psycopg_imports, type_imports])
<<<<<<< HEAD:python/src/postgrescodegen/generators/python/register.py
    register_type_function = _get_register_type_function()
    register_domain_function = _get_register_domain_function()
    register_primitive_notnull_domain_function = (
        _get_register_primitive_notnull_domain_function()
    )
    register_all_types_function = _get_register_all_types_function(
=======
    make_sequence_function = get_make_sequence_function()
    register_composite_type_function = get_register_composite_type_function()
    register_domain_type_function = get_register_domain_type_function()
    register_composite_domain_function = get_register_composite_domain_function()
    register_all_types_function = get_register_all_types_function(
>>>>>>> a484201a59c621dfdf218d3154460b4e347e82f6:src/postgrescodegen/register.py
        postgres_types, postgres_domains
    )
    return "\n\n\n".join(
        [
            imports,
            make_sequence_function,
            register_composite_type_function,
            register_composite_domain_function,
            register_domain_type_function,
            register_all_types_function,
        ]
    )


def _get_register_type_function() -> str:
    lines = [
        "def register_type(conn: Connection, type_name: str, factory: type):",
        f"{tab}info = CompositeInfo.fetch(conn, type_name)",
        f"{tab}if info is not None:",
        f"{tab * 2}register_composite(info, conn, factory)",
        f"{tab}else:",
        f'{tab * 2}raise RuntimeError(f"Could not find composite type {{type_name}}")',
    ]
    return "\n".join(lines)


def _get_register_domain_function() -> str:
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
        f'{tab * 2}raise RuntimeError(f"Could not find domain {{domain_name}}")',
        f"{tab}else:",
        f'{tab * 2}raise RuntimeError(f"Could not find underlying type {{underlying_type_name}}")',
    ]
    return "\n".join(lines)


def _get_register_primitive_notnull_domain_function() -> str:
    lines = [
        "def register_primitive_notnull_domain(conn: Connection, domain_name: str):",
        f"{tab}info = TypeInfo.fetch(conn, domain_name)",
        f"{tab}if info is not None:",
        f"{tab * 2}info.register(conn)",
        f"{tab}else:",
        f'{tab * 2}raise RuntimeError(f"Could not find primitive notnull domain {{domain_name}}")',
    ]
    return "\n".join(lines)


def _get_register_type_function_call(
    indent: int, postgres_type: PostgresObject
) -> str:
    return f'{tab * indent}register_type(conn, "{postgres_type.get_name()}", {postgres_type.get_python_name()})'


def _get_register_domain_function_call(
    indent: int, postgres_domain: PostgresDomain
) -> str:
    return f'{tab * indent}register_primitive_notnull_domain(conn, "{postgres_domain.domain_name}")'


def _get_register_primitive_notnull_domain_function_call(
    indent: int, postgres_domain: str
) -> str:
    return f'{tab * indent}register_primitive_notnull_domain(conn, "{postgres_domain}")'


def _get_register_types_function_calls(
    indent: int,
    postgres_types: list[PostgresComposite],
    postgres_domains: list[PostgresDomain],
) -> str:
    python_type_registers = "\n".join(
        _get_register_type_function_call(indent, postgres_type)
        for postgres_type in postgres_types
    )
    python_domain_registers = "\n".join(
        _get_register_domain_function_call(indent, postgres_domain)
        for postgres_domain in postgres_domains
    )
    python_primitive_notnull_domain_registers = "\n".join(
        _get_register_primitive_notnull_domain_function_call(
            indent, domain_name
        )
        for domain_name in notnull_domains
    )
    return "\n\n".join(
        [
            python_type_registers,
            python_primitive_notnull_domain_registers,
            python_domain_registers,
        ]
    )


def _update_python_type_import_dict_for_type_name(
    python_postgres_module_lookup: PythonPostgresModuleLookup,
    python_type: PostgresObject,
    import_dict: PythonImportDict,
) -> PythonImportDict:
    python_name = python_type.get_python_name()
    module_name = python_postgres_module_lookup[python_name]
    import_dict = update_python_type_import_dict(
        import_dict, module_name, python_name
    )
    return import_dict


def _get_register_types_imports(
    python_postgres_module_lookup: PythonPostgresModuleLookup,
    postgres_types: list[PostgresComposite],
    postgres_domains: list[PostgresDomain],
) -> str:
    import_dict: PythonImportDict = {}
    for postgres_type in postgres_types:
        import_dict = _update_python_type_import_dict_for_type_name(
            python_postgres_module_lookup, postgres_type, import_dict
        )
    for postgres_domain in postgres_domains:
        import_dict = _update_python_type_import_dict_for_type_name(
            python_postgres_module_lookup, postgres_domain, import_dict
        )
    return get_import_statements_for_python_import_dict(import_dict)


def _get_register_all_types_function(
    postgres_types: list[PostgresComposite],
    postgres_domains: list[PostgresDomain],
) -> str:
    function_declaration = "def register_types(conn: Connection):"
    return f"{function_declaration}\n{_get_register_types_function_calls(1, postgres_types, postgres_domains)}"
