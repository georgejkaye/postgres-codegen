from abc import abstractmethod
from typing import Optional
from postgrescodegen.classes.postgres.core import PostgresObject
from postgrescodegen.classes.python import PythonPostgresModuleLookup


class Translator[T: PostgresObject]:
    @abstractmethod
    def get_postgres_object_for_statement(self, statement: str) -> Optional[T]:
        pass

    @abstractmethod
    def get_python_code_for_postgres_objects(
        self, modules: PythonPostgresModuleLookup, postgres_objects: list[T]
    ) -> str:
        pass
