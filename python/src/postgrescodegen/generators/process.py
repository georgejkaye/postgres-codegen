from postgrescodegen.generators.generator import Generator


class GeneratorProcessor:
    def __init__(self, generator: Generator):
        self.generator = generator

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
