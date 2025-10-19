from pathlib import Path
import re
from typing import Optional

from postgrescodegen.classes import (
    PostgresType,
    PostgresTypeField,
    PythonPostgresModule,
    PythonPostgresModuleLookup,
)
from postgrescodegen.generator import get_postgres_module_for_postgres_file
from postgrescodegen.pytypes import (
    get_python_type_for_postgres_type,
)

tab = "    "

type_regex = r"CREATE TYPE (.*) AS \((.*)\)"


def get_postgres_type_for_statement(
    statement: str,
) -> Optional[PostgresType]:
    type_matches = re.match(type_regex, statement)
    if type_matches is None:
        return None
    postgres_type_name = type_matches.group(1)
    type_fields_string = type_matches.group(2)
    postgres_type_fields: list[PostgresTypeField] = []
    for type_clause in type_fields_string.split(","):
        type_clause_clauses = type_clause.strip().split(" ", 1)
        postgres_type_field_name = type_clause_clauses[0]
        postgres_type_field_type = type_clause_clauses[1]
        postgres_type_field = PostgresTypeField(
            postgres_type_field_name, postgres_type_field_type
        )
        postgres_type_fields.append(postgres_type_field)
    return PostgresType(postgres_type_name, postgres_type_fields)


def get_python_for_postgres_type(postgres_type: PostgresType) -> str:
    python_type_name = postgres_type.get_python_name()
    python_type_declaration = f"class {python_type_name}:"
    python_lines = ["@dataclass", python_type_declaration]
    for type_field in postgres_type.type_fields:
        python_type = get_python_type_for_postgres_type(type_field.field_type)
        python_type_field_str = f"{tab}{type_field.field_name}: {python_type}"
        python_lines.append(python_type_field_str)
    return "\n".join(python_lines)


def check_if_type_in_code(python_code_str: str, type_to_check: str) -> bool:
    return (
        f": {type_to_check}" in python_code_str
        or f"[{type_to_check}]" in python_code_str
        or f"[{type_to_check}[" in python_code_str
    )


def get_imports_for_python_code_str(python_code_str: str) -> list[str]:
    python_imports: list[str] = ["from dataclasses import dataclass"]
    if check_if_type_in_code(python_code_str, "datetime"):
        python_imports.append("from datetime import datetime")
    if check_if_type_in_code(python_code_str, "timedelta"):
        python_imports.append("from datetime import timedelta")
    if check_if_type_in_code(python_code_str, "Decimal"):
        python_imports.append("from decimal import Decimal")
    if "Optional[" in python_code_str:
        python_imports.append("from typing import Optional")
    if check_if_type_in_code(python_code_str, "Range"):
        python_imports.append("from psycopg.types.range import Range")
    return python_imports


def get_python_code_for_postgres_types(
    python_postgres_module_lookup: PythonPostgresModuleLookup,
    postgres_types: list[PostgresType],
) -> str:
    python_type_codes = [
        get_python_for_postgres_type(postgres_type) for postgres_type in postgres_types
    ]
    python_code_str = "\n\n\n".join(python_type_codes)
    python_imports = get_imports_for_python_code_str(python_code_str)
    python_import_str = "\n".join(python_imports)
    return f"{python_import_str}\n\n{python_code_str}"


def get_postgres_types_for_postgres_statements(
    statements: list[str],
) -> list[PostgresType]:
    postgres_types = [
        postgres_type
        for statement in statements
        if (postgres_type := get_postgres_type_for_statement(statement)) is not None
    ]
    return postgres_types


def get_python_postgres_module_for_postgres_type_file(
    postgres_scripts_path: Path,
    python_package_name: str,
    python_output_module: str,
    python_postgres_module_lookup: PythonPostgresModuleLookup,
    file_path: Path,
) -> tuple[PythonPostgresModuleLookup, PythonPostgresModule[PostgresType]]:
    return get_postgres_module_for_postgres_file(
        get_postgres_type_for_statement,
        get_python_code_for_postgres_types,
        postgres_scripts_path,
        python_package_name,
        python_output_module,
        python_postgres_module_lookup,
        file_path,
    )
