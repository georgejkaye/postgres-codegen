from postgrescodegen.generators.generator import Generator
from postgrescodegen.postgres.composites import PostgresComposite
from postgrescodegen.postgres.functions import PostgresFunction


class PythonGenerator(Generator):
    def generate_composite_file(self, input: list[PostgresComposite]) -> str:
        pass

    def generate_function_file(
        self, type_modules: dict[str, str], input: list[PostgresFunction]
    ) -> str:
        pass
