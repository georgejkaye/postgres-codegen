import re
from pathlib import Path
from typing import Optional

from postgrescodegen.classes.postgres.composites import (
    PostgresComposite,
    PostgresCompositeField,
)
from postgrescodegen.classes.python import (
    PythonImportDict,
    PythonPostgresModule,
    PythonPostgresModuleLookup,
)
from postgrescodegen.generators.core import (
    get_base_postgres_type_for_postgres_type,
    get_base_python_type_for_postgres_type,
    get_import_statements_for_python_import_dict,
    get_postgres_module_for_postgres_file,
    get_python_type_for_postgres_type,
    is_user_defined_type,
    update_python_type_import_dict,
)

tab = "    "

composite_regex = r"CREATE TYPE (.*) AS \((.*)\)"


def get_python_module_for_postgres_composite_file(
    postgres_scripts_path: Path,
    python_output_module: str,
    python_postgres_module_lookup: PythonPostgresModuleLookup,
    file_path: Path,
) -> tuple[PythonPostgresModuleLookup, PythonPostgresModule[PostgresComposite]]:
    return get_postgres_module_for_postgres_file(
        _get_postgres_composite_for_statement,
        _get_python_code_for_postgres_composites,
        postgres_scripts_path,
        python_output_module,
        python_postgres_module_lookup,
        file_path,
    )


def _get_python_code_for_postgres_composites(
    python_postgres_module_lookup: PythonPostgresModuleLookup,
    postgres_composites: list[PostgresComposite],
) -> str:
    python_composite_functions = [
        _get_python_for_postgres_composite(postgres_composite)
        for postgres_composite in postgres_composites
    ]
    python_code_str = "\n\n\n".join(python_composite_functions)
    stdlib_python_imports = _get_stdlib_imports_for_python_code_str(
        python_code_str
    )
    user_python_imports = _get_user_imports_for_postgres_composites(
        python_postgres_module_lookup, postgres_composites
    )
    return "\n\n".join(
        code_block
        for code_block in [
            stdlib_python_imports,
            user_python_imports,
            python_code_str,
        ]
        if code_block != ""
    )


def _get_postgres_composite_for_statement(
    statement: str,
) -> Optional[PostgresComposite]:
    composite_matches = re.match(composite_regex, statement)
    if composite_matches is None:
        return None
    postgres_composite_name = composite_matches.group(1)
    type_fields_string = composite_matches.group(2)
    postgres_composite_fields: list[PostgresCompositeField] = []
    for type_clause in type_fields_string.split(","):
        type_clause_clauses = type_clause.strip().split(" ", 1)
        postgres_composite_field_name = type_clause_clauses[0]
        postgres_composite_field_type = type_clause_clauses[1]
        postgres_composite_field = PostgresCompositeField(
            postgres_composite_field_name, postgres_composite_field_type
        )
        postgres_composite_fields.append(postgres_composite_field)
    return PostgresComposite(postgres_composite_name, postgres_composite_fields)


def _get_python_for_postgres_composite(
    postgres_composite: PostgresComposite,
) -> str:
    python_composite_name = postgres_composite.get_python_name()
    python_composite_declaration = f"class {python_composite_name}:"
    python_lines = ["@dataclass", python_composite_declaration]
    for type_field in postgres_composite.composite_fields:
        python_type = get_python_type_for_postgres_type(type_field.field_type)
        python_type_field_str = f"{tab}{type_field.field_name}: {python_type}"
        python_lines.append(python_type_field_str)
    return "\n".join(python_lines)


def _check_if_type_in_code(python_code_str: str, type_to_check: str) -> bool:
    return (
        f": {type_to_check}" in python_code_str
        or f"[{type_to_check}]" in python_code_str
        or f"[{type_to_check}[" in python_code_str
    )


def _get_stdlib_imports_for_python_code_str(
    python_code_str: str,
) -> str:
    python_imports: list[str] = ["from dataclasses import dataclass"]
    if _check_if_type_in_code(python_code_str, "datetime"):
        python_imports.append("from datetime import datetime")
    if _check_if_type_in_code(python_code_str, "timedelta"):
        python_imports.append("from datetime import timedelta")
    if _check_if_type_in_code(python_code_str, "Decimal"):
        python_imports.append("from decimal import Decimal")
    if "Optional[" in python_code_str:
        python_imports.append("from typing import Optional")
    if _check_if_type_in_code(python_code_str, "Range"):
        python_imports.append("from psycopg.types.range import Range")
    return "\n".join(python_imports)


def _get_user_imports_for_postgres_composites(
    python_postgres_module_lookup: PythonPostgresModuleLookup,
    postgres_composites: list[PostgresComposite],
) -> str:
    import_dict: PythonImportDict = {}
    postgres_composite_names = [
        postgres_type.get_name() for postgres_type in postgres_composites
    ]
    for postgres_composite in postgres_composites:
        for postgres_composite_field in postgres_composite.composite_fields:
            postgres_composite_field_type = postgres_composite_field.field_type
            postgres_composite_field_base_type = (
                get_base_postgres_type_for_postgres_type(
                    postgres_composite_field_type
                )
            )
            if (
                is_user_defined_type(postgres_composite_field_base_type)
                and postgres_composite_field_base_type
                not in postgres_composite_names
            ):
                python_type = get_base_python_type_for_postgres_type(
                    postgres_composite_field_base_type
                )
                postgres_composite_field_module = (
                    python_postgres_module_lookup.get(python_type)
                )
                if postgres_composite_field_module is not None:
                    import_dict = update_python_type_import_dict(
                        import_dict,
                        postgres_composite_field_module,
                        python_type,
                    )
                else:
                    print(
                        f"WARNING: Could not find module for {postgres_composite_field_base_type}"
                    )
    return get_import_statements_for_python_import_dict(import_dict)
