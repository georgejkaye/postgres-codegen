from pathlib import Path
import re
from typing import Optional
from postgrescodegen.access.file import FileWrapper
from postgrescodegen.generators.parsers.parser import PostgresObjectParser
from postgrescodegen.postgres.core import PostgresObject
from postgrescodegen.generators.python.python import (
    PythonPostgresModule,
    PythonPostgresModuleLookup,
)
from postgrescodegen.generators.translators.translator import Translator
from postgrescodegen.process.files import (
    get_python_module_name_for_postgres_file,
)


class PostgresObjectParserProcessor[T: PostgresObject]:
    def __init__(
        self, file_wrapper: FileWrapper, parser: PostgresObjectParser[T]
    ):
        self.file_wrapper = file_wrapper
        self.parser = parser

    def get_postgres_objects_for_postgres_file(
        self, file_path: Path
    ) -> list[T]:
        statements = self._get_statements_from_postgres_file(file_path)
        return [
            postgres_object
            for statement in statements
            if (
                postgres_object := self._get_postgres_object_for_statement(
                    statement
                )
            )
            is not None
        ]

    def get_postgres_module_for_postgres_file(
        self,
        postgres_scripts_path: Path,
        python_output_module: str,
        python_postgres_module_lookup: PythonPostgresModuleLookup,
        file_path: Path,
    ) -> tuple[PythonPostgresModuleLookup, PythonPostgresModule[T]]:
        postgres_objects = self.get_postgres_objects_for_postgres_file(
            file_path
        )
        python_module_name = get_python_module_name_for_postgres_file(
            postgres_scripts_path,
            file_path,
            python_output_module,
        )
        python_code = self.generator.get_python_code_for_postgres_objects(
            python_postgres_module_lookup, postgres_objects
        )
        for postgres_object in postgres_objects:
            python_name = postgres_object.get_python_name()
            python_postgres_module_lookup[python_name] = python_module_name
        python_postgres_module = PythonPostgresModule(
            python_module_name, postgres_objects, python_code
        )
        return (python_postgres_module_lookup, python_postgres_module)

    def _get_statements_from_postgres_file(
        self, file_path: Path, delimiter: str = ";"
    ) -> list[str]:
        contents = self.file_wrapper.read_file(file_path)
        normalised_contents = self._normalise_postgres_file_contents(contents)
        statements = normalised_contents.split(delimiter)
        return [
            statement.strip() for statement in statements if len(statement) > 0
        ]

    def _normalise_postgres_file_contents(self, file_contents: str) -> str:
        one_line_contents = file_contents.replace("\n", " ")
        space_normalised_contents = " ".join(one_line_contents.split())
        return space_normalised_contents

    def _get_postgres_object_for_statement(self, statement: str) -> Optional[T]:
        match = re.match(self.parser.get_statement_regex(), statement)
        if match is None:
            return None
        return self.parser.get_postgres_object_for_statement(match)
