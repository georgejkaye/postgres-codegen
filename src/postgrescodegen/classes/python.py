from dataclasses import dataclass

from postgrescodegen.classes.postgres.core import PostgresObject


@dataclass
class PythonPostgresModule[T: PostgresObject]:
    module_name: str
    module_objects: list[T]
    python_code: str


type PythonPostgresModuleLookup = dict[str, str]

type PythonImportDict = dict[str, set[str]]


@dataclass
class PythonImport:
    module: str
    token: str
