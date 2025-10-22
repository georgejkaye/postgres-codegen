from pathlib import Path
from typing import Callable, Optional

from postgrescodegen.classes import (
    PythonImport,
    PythonImportDict,
    PythonablePostgresObject,
    PythonPostgresModule,
    PythonPostgresModuleLookup,
)
from postgrescodegen.files import (
    get_python_module_name_for_postgres_file,
)

tab = "   "


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


def get_import_statement_for_module(module_name: str, tokens: set[str]) -> str:
    lines = [f"from {module_name} import ("]
    sorted_tokens = sorted(tokens)
    for token in sorted_tokens:
        lines.append(f"{tab}{token},")
    lines.append(")")
    return "\n".join(lines)


def get_import_statements_for_python_import_dict(import_dict: PythonImportDict) -> str:
    import_statements = [
        get_import_statement_for_module(module, import_dict[module])
        for module in import_dict.keys()
    ]
    return "\n".join(import_statements)


def get_import_statements_for_python_imports(imports: list[PythonImport]) -> str:
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


def get_postgres_module_for_postgres_file[T: PythonablePostgresObject](
    get_postgres_object_for_statement: Callable[[str], Optional[T]],
    get_python_code_for_postgres_objects: Callable[
        [PythonPostgresModuleLookup, list[T]], str
    ],
    postgres_scripts_path: Path,
    python_output_module: str,
    python_postgres_module_lookup: PythonPostgresModuleLookup,
    file_path: Path,
) -> tuple[PythonPostgresModuleLookup, PythonPostgresModule[T]]:
    postgres_statements = get_statements_from_postgres_file(file_path)
    postgres_objects = [
        postgres_object
        for statement in postgres_statements
        if (postgres_object := get_postgres_object_for_statement(statement)) is not None
    ]
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
