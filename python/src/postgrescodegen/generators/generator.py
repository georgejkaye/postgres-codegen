from abc import abstractmethod

from postgrescodegen.postgres.composites import PostgresComposite
from postgrescodegen.postgres.functions import PostgresFunction


class Generator:
    @abstractmethod
    def generate_composite_file(self, input: list[PostgresComposite]) -> str:
        pass

    @abstractmethod
    def generate_function_file(
        self, type_modules: dict[str, str], input: list[PostgresFunction]
    ) -> str:
        pass
