from pathlib import Path
from postgrescodegen.access.file import FileWrapper
from postgrescodegen.classes.postgres.core import PostgresObject
from postgrescodegen.generators.translators.translator import Translator


class PostgresObjectParser[T: PostgresObject]:
    def __init__(self, file_wrapper: FileWrapper, translator: Translator[T]):
        self.file_wrapper = file_wrapper
        self.generator = translator

    def get_postgres_objects_for_postgres_file(
        self, file_path: Path
    ) -> list[T]:
        statements = self._get_statements_from_postgres_file(file_path)
        return [
            postgres_object
            for statement in statements
            if (
                postgres_object
                := self.generator.get_postgres_object_for_statement(statement)
            )
            is not None
        ]

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
