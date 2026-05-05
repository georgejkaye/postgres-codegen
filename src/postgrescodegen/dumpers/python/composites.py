from postgrescodegen.dumpers.dumper import Dumper
from postgrescodegen.dumpers.python.types import PythonTypes
from postgrescodegen.generators.python.imports import PythonImports
from postgrescodegen.postgres.composites import (
    PostgresComposite,
)
from postgrescodegen.generators.python.python import (
    PythonImportDict,
    PythonPostgresModuleLookup,
)
from postgrescodegen.postgres.types import PostgresTypes

tab = "    "


class PythonCompositeDumper(Dumper[PostgresComposite]):
    def get_python_code_for_postgres_objects(
        self,
        modules: PythonPostgresModuleLookup,
        postgres_objects: list[PostgresComposite],
    ) -> str:
        python_composite_functions = [
            self._get_python_for_postgres_composite(postgres_composite)
            for postgres_composite in postgres_objects
        ]
        python_code_str = "\n\n\n".join(python_composite_functions)
        stdlib_python_imports = (
            PythonImports.get_stdlib_imports_for_python_code_str(
                python_code_str
            )
        )
        user_python_imports = self._get_user_imports_for_postgres_composites(
            modules, postgres_objects
        )
        return "\n\n".join(
            code_block
            for code_block in [
                stdlib_python_imports,
                user_python_imports,
                python_code_str,
            ]
            if code_block != ""
        )

    def _get_python_for_postgres_composite(
        self,
        postgres_composite: PostgresComposite,
    ) -> str:
        python_composite_name = PythonTypes.get_composite_type_name(
            postgres_composite.get_name()
        )
        python_composite_declaration = f"class {python_composite_name}:"
        python_lines = ["@dataclass", python_composite_declaration]
        for type_field in postgres_composite.composite_fields:
            python_type = PythonTypes.from_postgres_type(type_field.field_type)
            python_type_field_str = (
                f"{tab}{type_field.field_name}: {python_type}"
            )
            python_lines.append(python_type_field_str)
        return "\n".join(python_lines)

    def _get_user_imports_for_postgres_composites(
        self,
        python_postgres_module_lookup: PythonPostgresModuleLookup,
        postgres_composites: list[PostgresComposite],
    ) -> str:
        import_dict: PythonImportDict = {}
        postgres_composite_names = [
            postgres_type.get_name() for postgres_type in postgres_composites
        ]
        for postgres_composite in postgres_composites:
            for postgres_composite_field in postgres_composite.composite_fields:
                postgres_composite_field_type = (
                    postgres_composite_field.field_type
                )
                postgres_composite_field_base_type = (
                    PythonTypes.get_base_python_type(
                        postgres_composite_field_type
                    )
                )
                if (
                    PostgresTypes.is_composite(
                        postgres_composite_field_base_type
                    )
                    and postgres_composite_field_base_type
                    not in postgres_composite_names
                ):
                    python_type = PostgresTypes.get_base_type(
                        postgres_composite_field_base_type
                    )
                    postgres_composite_field_module = (
                        python_postgres_module_lookup.get(python_type)
                    )
                    if postgres_composite_field_module is not None:
                        import_dict = (
                            PythonImports.update_python_type_import_dict(
                                import_dict,
                                postgres_composite_field_module,
                                python_type,
                            )
                        )
                    else:
                        print(
                            f"WARNING: Could not find module for {postgres_composite_field_base_type}"
                        )
        return PythonImports.get_import_statements_for_python_import_dict(
            import_dict
        )
