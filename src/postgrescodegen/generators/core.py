from pathlib import Path
from typing import Callable, Optional

from postgrescodegen.classes.postgres.core import PostgresObject
from postgrescodegen.classes.postgres.composites import (
    get_python_name_for_postgres_type_name,
)
from postgrescodegen.classes.python import (
    PythonImport,
    PythonImportDict,
    PythonPostgresModule,
    PythonPostgresModuleLookup,
)
from postgrescodegen.process.files import (
    get_python_module_name_for_postgres_file,
)

tab = "   "

postgres_primitives = set(
    [
        "VOID",
        "TEXT",
        "INT",
        "INTEGER",
        "BIGINT",
        "DECIMAL",
        "NUMERIC",
        "TIMESTAMP",
        "TIMESTAMP WITH TIME ZONE",
        "TIMESTAMP WITHOUT TIME ZONE",
        "INTERVAL",
        "DATERANGE",
        "BOOLEAN",
    ]
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


def update_python_type_import_dict(
    imports_dict: PythonImportDict, type_module: str, type_name: str
) -> PythonImportDict:
    module_result = imports_dict.get(type_module)
    if module_result is None:
        imports_dict[type_module] = set([type_name])
        return imports_dict
    if type_name in module_result:
        return imports_dict
    imports_dict[type_module].add(type_name)
    return imports_dict


def get_import_statements_for_python_import_dict(
    import_dict: PythonImportDict,
) -> str:
    import_statements = [
        _get_import_statement_for_module(module, import_dict[module])
        for module in import_dict.keys()
    ]
    return "\n".join(import_statements)


def get_base_python_type_for_postgres_type(type_string: str) -> str:
    base_type_string = get_base_postgres_type_for_postgres_type(type_string)
    return _get_python_type_for_postgres_base_type(base_type_string)


def _get_import_statement_for_module(module_name: str, tokens: set[str]) -> str:
    lines = [f"from {module_name} import ("]
    sorted_tokens = sorted(tokens)
    for token in sorted_tokens:
        lines.append(f"{tab}{token},")
    lines.append(")")
    return "\n".join(lines)


def get_import_statements_for_python_imports(
    imports: list[PythonImport],
) -> str:
    import_dict: dict[str, set[str]] = {}
    for import_token in imports:
        if import_dict.get(import_token.module) is None:
            import_dict[import_token.module] = set([import_token.token])
        else:
            import_dict[import_token.module].add(import_token.token)
    return get_import_statements_for_python_import_dict(import_dict)


def normalise_postgres_file_contents(file_contents: str) -> str:
    one_line_contents = file_contents.replace("\n", " ")
    space_normalised_contents = " ".join(one_line_contents.split())
    return space_normalised_contents


def get_statements_from_postgres_file_contents(
    file_contents: str, delimiter: str = ";"
) -> list[str]:
    normalised_file_contents = normalise_postgres_file_contents(file_contents)
    statements = normalised_file_contents.split(delimiter)
    return [statement.strip() for statement in statements if len(statement) > 0]


def get_statements_from_postgres_file(
    file_path: str | Path, delimiter: str = ";"
) -> list[str]:
    with open(file_path, "r") as f:
        file_contents = f.read()
    return get_statements_from_postgres_file_contents(file_contents, delimiter)


def get_postgres_objects_for_postgres_file[T: PostgresObject](
    get_postgres_object_for_statement: Callable[[str], Optional[T]],
    file_path: Path,
) -> list[T]:
    postgres_statements = get_statements_from_postgres_file(file_path)
    return [
        postgres_object
        for statement in postgres_statements
        if (postgres_object := get_postgres_object_for_statement(statement))
        is not None
    ]


def get_postgres_module_for_postgres_file[T: PostgresObject](
    get_postgres_object_for_statement: Callable[[str], Optional[T]],
    get_python_code_for_postgres_objects: Callable[
        [PythonPostgresModuleLookup, list[T]], str
    ],
    postgres_scripts_path: Path,
    python_output_module: str,
    python_postgres_module_lookup: PythonPostgresModuleLookup,
    file_path: Path,
) -> tuple[PythonPostgresModuleLookup, PythonPostgresModule[T]]:
    postgres_objects = get_postgres_objects_for_postgres_file(
        get_postgres_object_for_statement, file_path
    )
    python_module_name = get_python_module_name_for_postgres_file(
        postgres_scripts_path,
        file_path,
        python_output_module,
    )
    python_code = get_python_code_for_postgres_objects(
        python_postgres_module_lookup, postgres_objects
    )
    for postgres_object in postgres_objects:
        python_name = postgres_object.get_python_name()
        python_postgres_module_lookup[python_name] = python_module_name
    python_postgres_module = PythonPostgresModule(
        python_module_name, postgres_objects, python_code
    )
    return (python_postgres_module_lookup, python_postgres_module)


def get_base_python_type_for_python_type(python_type: str) -> str:
    if len(python_type) > 5 and python_type[:5] == "list[":
        return get_base_python_type_for_python_type(python_type[5:-1])
    if len(python_type) > 9 and python_type[:9] == "Optional[":
        return get_base_python_type_for_python_type(python_type[9:-1])
    return python_type


def _get_list_type(python_type: str) -> str:
    return f"list[{python_type}]"


def _get_optional_type(python_type: str) -> str:
    return f"Optional[{python_type}]"


def get_python_type_for_postgres_type(type_string: str) -> str:
    base_type_string = get_base_postgres_type_for_postgres_type(type_string)
    base_python_type = _get_python_type_for_postgres_base_type(base_type_string)
    if _is_postgres_array_type(type_string):
        if _is_postgres_type_nullable(type_string[:-2]):
            type_string = _get_optional_type(base_python_type)
        return _get_list_type(base_python_type)
    if _is_postgres_type_nullable(type_string):
        base_python_type = _get_optional_type(base_python_type)
    return base_python_type


def get_base_postgres_type_for_postgres_type(postgres_type_name: str) -> str:
    if _is_postgres_array_type(postgres_type_name):
        postgres_type_name = postgres_type_name[:-2]
    if not _is_postgres_type_nullable(postgres_type_name):
        return postgres_type_name[:-8]
    return postgres_type_name


def is_user_defined_type(postgres_type_name: str) -> bool:
    return (
        get_base_postgres_type_for_postgres_type(postgres_type_name)
        not in postgres_primitives
    )


def _is_postgres_array_type(postgres_type_name: str) -> bool:
    return postgres_type_name[-2:] == "[]"


def _is_postgres_type_nullable(postgres_type: str) -> bool:
    return len(postgres_type) < 8 or postgres_type[-8:].lower() != "_notnull"


def _get_python_type_for_postgres_base_type(base_type_string: str) -> str:
    if (
        base_python_type := postgres_to_python_type_dict.get(base_type_string)
    ) is not None:
        return base_python_type
    return get_python_name_for_postgres_type_name(base_type_string)
