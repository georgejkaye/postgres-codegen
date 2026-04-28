from pathlib import Path
from typing import Callable, Optional

from postgrescodegen.postgres.core import PostgresObject
from postgrescodegen.postgres.composites import (
    get_python_name_for_postgres_type_name,
)
from postgrescodegen.generators.python.python import (
    PythonPostgresModule,
    PythonPostgresModuleLookup,
)
from postgrescodegen.process.files import (
    get_python_module_name_for_postgres_file,
)

tab = "   "


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
