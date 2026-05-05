from postgrescodegen.dumpers.dumper import Dumper
from postgrescodegen.dumpers.python.types import PythonTypes
from postgrescodegen.generators.python.imports import PythonImports
from postgrescodegen.postgres.functions import (
    PostgresFunction,
    PostgresFunctionArgument,
)
from postgrescodegen.generators.python.python import (
    PythonImportDict,
    PythonPostgresModuleLookup,
)
from postgrescodegen.postgres.types import PostgresTypes

tab = "    "


class PythonFunctionDumper(Dumper[PostgresFunction]):
    @staticmethod
    def get_code_for_object(postgres_object: PostgresFunction) -> str:
        python_functions: list[str] = []
        if postgres_object.function_return != "VOID":
            fetchall_function = (
                PythonFunctionDumper._get_code_for_postgres_function(
                    postgres_object, fetchall=True
                )
            )
            python_functions.append(fetchall_function)
        fetchone_function = (
            PythonFunctionDumper._get_code_for_postgres_function(
                postgres_object, fetchall=False
            )
        )
        python_functions.append(fetchone_function)
        return "\n\n".join(python_functions)

    @staticmethod
    def _get_code_for_postgres_function(
        postgres_function: PostgresFunction, fetchall: bool
    ) -> str:
        python_function_fetchall_declaration = (
            PythonFunctionDumper._get_function_declaration(
                postgres_function, fetchall
            )
        )
        python_db_inputs = PythonFunctionDumper._get_python_db_inputs(
            postgres_function.function_args, base_indent=1
        )
        python_try = PythonFunctionDumper._get_python_try(base_indent=1)
        if postgres_function.function_return == "VOID":
            python_conn_execution = PythonFunctionDumper._get_python_execution_for_postgres_function(
                postgres_function, is_cursor=False, base_indent=2
            )
            python_commit = PythonFunctionDumper._get_python_commit(
                base_indent=2
            )
            python_execution = "\n".join([python_conn_execution, python_commit])
        else:
            python_cursor_initialisation = PythonFunctionDumper._get_python_cursor_initialisation_for_postgres_function(
                postgres_function, base_indent=2
            )
            python_cursor_execution = PythonFunctionDumper._get_python_execution_for_postgres_function(
                postgres_function, is_cursor=True, base_indent=3
            )
            if fetchall:
                python_result_fetching = (
                    PythonFunctionDumper._get_python_fetchall(base_indent=3)
                )
            else:
                python_result_fetching = (
                    PythonFunctionDumper._get_python_fetchone(base_indent=3)
                )
            python_commit = PythonFunctionDumper._get_python_commit(
                base_indent=3
            )
            python_execution = "\n".join(
                [
                    python_cursor_initialisation,
                    python_cursor_execution,
                    python_commit,
                    python_result_fetching,
                ]
            )
        python_except = PythonFunctionDumper._get_python_except(base_indent=1)
        return "\n".join(
            [
                line
                for line in [
                    python_function_fetchall_declaration,
                    python_db_inputs,
                    python_try,
                    python_execution,
                    python_except,
                ]
                if line != ""
            ]
        )

    def _get_imports_for_postgres_function_file(
        self,
        python_postgres_module_lookup: PythonPostgresModuleLookup,
        postgres_functions: list[PostgresFunction],
    ) -> str:
        non_void_returning_function = False
        python_imports_dict: dict[str, set[str]] = {}
        user_imports_dict: dict[str, set[str]] = {}
        for postgres_function in postgres_functions:
            python_imports_dict, user_imports_dict = (
                self._get_import_for_postgres_type(
                    python_postgres_module_lookup,
                    python_imports_dict,
                    user_imports_dict,
                    postgres_function.function_return,
                    False,
                )
            )
            if postgres_function.function_return != "VOID":
                non_void_returning_function = True
            for function_arg in postgres_function.function_args:
                python_imports_dict, user_imports_dict = (
                    self._get_import_for_postgres_type(
                        python_postgres_module_lookup,
                        python_imports_dict,
                        user_imports_dict,
                        function_arg.argument_type,
                        True,
                    )
                )
        psycopg_imports = [
            "from psycopg import Connection",
        ]
        if non_void_returning_function:
            psycopg_imports.append("from psycopg.rows import class_row")
            PythonImports.update_python_type_import_dict(
                python_imports_dict, "typing", "Optional"
            )
        psycopg_imports_string = "\n".join(psycopg_imports)
        python_imports_string = (
            PythonImports.get_import_statements_for_python_import_dict(
                python_imports_dict
            )
        )
        user_imports_string = (
            PythonImports.get_import_statements_for_python_import_dict(
                user_imports_dict
            )
        )
        return "\n\n".join(
            [
                import_string
                for import_string in [
                    python_imports_string,
                    psycopg_imports_string,
                    user_imports_string,
                ]
                if import_string != ""
            ]
        )

    @staticmethod
    def _get_python_try(base_indent: int) -> str:
        return f"{base_indent * tab}try:"

    @staticmethod
    def _get_python_fetchone(base_indent: int) -> str:
        return f"{base_indent * tab}return rows.fetchone()"

    @staticmethod
    def _get_python_fetchall(base_indent: int) -> str:
        return f"{base_indent * tab}return rows.fetchall()"

    @staticmethod
    def _get_python_except(base_indent: int) -> str:
        except_line = f"{base_indent * tab}except:"
        rollback_line = f"{(base_indent + 1) * tab}conn.rollback()"
        raise_line = f"{(base_indent + 1) * tab}raise"
        return f"{except_line}\n{rollback_line}\n{raise_line}"

    @staticmethod
    def _get_python_commit(base_indent: int) -> str:
        return f"{base_indent * tab}conn.commit()"

    @staticmethod
    def _get_import_for_postgres_type(
        python_postgres_module_lookup: PythonPostgresModuleLookup,
        python_imports_dict: dict[str, set[str]],
        user_imports_dict: dict[str, set[str]],
        postgres_type_name: str,
        is_argument: bool,
    ) -> tuple[PythonImportDict, PythonImportDict]:
        python_type_name = PythonTypes.from_postgres_type(postgres_type_name)
        if "Optional[" in python_type_name:
            python_imports_dict = PythonImports.update_python_type_import_dict(
                python_imports_dict, "typing", "Optional"
            )
        if "datetime" in python_type_name:
            python_imports_dict = PythonImports.update_python_type_import_dict(
                python_imports_dict, "datetime", "datetime"
            )
        if "Decimal" in python_type_name:
            python_imports_dict = PythonImports.update_python_type_import_dict(
                python_imports_dict, "decimal", "Decimal"
            )
        if "list[" in python_type_name:
            python_type_name = python_type_name[5:-1]
        if PostgresTypes.is_composite(postgres_type_name) and is_argument:
            python_imports_dict = PythonImports.update_python_type_import_dict(
                python_imports_dict, "dataclasses", "astuple"
            )
        base_python_type = PythonTypes.get_base_python_type(python_type_name)
        type_module = python_postgres_module_lookup.get(base_python_type)
        if type_module is not None:
            user_imports_dict = PythonImports.update_python_type_import_dict(
                user_imports_dict, type_module, base_python_type
            )
        return python_imports_dict, user_imports_dict

    @staticmethod
    def _get_function_declaration(
        postgres_function: PostgresFunction, fetchall: bool
    ) -> str:
        arguments = [
            PythonFunctionDumper._get_function_argument(argument)
            for argument in postgres_function.function_args
        ]
        arguments = ["conn: Connection"] + arguments
        argument_string = f",\n{tab}".join(arguments)
        return_type_string = PythonTypes.from_postgres_type(
            postgres_function.function_return
        )
        if (
            len(return_type_string) > 9
            and return_type_string[:9] == "Optional["
        ):
            return_type_string = return_type_string[9:-1]
        if return_type_string == "None":
            return_type_string = "None"
            function_name = postgres_function.function_name
        elif fetchall:
            return_type_string = f"list[{return_type_string}]"
            function_name = f"{postgres_function.function_name}_fetchall"
        else:
            return_type_string = f"Optional[{return_type_string}]"
            function_name = f"{postgres_function.function_name}_fetchone"
        declaration = f"def {function_name}(\n{tab}{argument_string}\n) -> {return_type_string}:"
        return declaration

    @staticmethod
    def _get_function_argument(
        postgres_function_argument: PostgresFunctionArgument,
    ) -> str:
        python_type = PythonTypes.from_postgres_type(
            postgres_function_argument.argument_type
        )
        python_argument_name = PythonFunctionDumper._get_python_function_argument_name_for_postgres_function_argument_name(
            postgres_function_argument.argument_name
        )
        return f"{python_argument_name} : {python_type}"

    @staticmethod
    def _get_python_function_argument_name_for_postgres_function_argument_name(
        postgres_function_argument_name: str,
    ) -> str:
        if postgres_function_argument_name.startswith("p_"):
            return postgres_function_argument_name[2:]
        else:
            return postgres_function_argument_name

    @staticmethod
    def _get_python_db_inputs(
        postgres_function_args: list[PostgresFunctionArgument],
        base_indent: int,
    ) -> str:
        lines: list[str] = []
        for postgres_function_arg in postgres_function_args:
            db_argument_name = postgres_function_arg.argument_name
            python_argument_name = PythonFunctionDumper._get_python_function_argument_name_for_postgres_function_argument_name(
                postgres_function_arg.argument_name
            )
            postgres_argument_type = PostgresTypes.get_base_type(
                postgres_function_arg.argument_type
            )
            if not PostgresTypes.is_composite(postgres_argument_type):
                tuple_expression = python_argument_name
            elif "[]" in postgres_function_arg.argument_type:
                tuple_expression = PythonFunctionDumper._get_python_list_of_tuples_for_list_of_dataclasses(
                    postgres_function_arg
                )
            else:
                tuple_expression = (
                    PythonFunctionDumper._get_python_tuple_for_dataclass(
                        postgres_function_arg
                    )
                )
            db_input_line = (
                f"{base_indent * tab}{db_argument_name} = {tuple_expression}"
            )
            lines.append(db_input_line)
        return "\n".join(lines)

    @staticmethod
    def _get_python_list_of_tuples_for_list_of_dataclasses(
        postgres_function_arg: PostgresFunctionArgument,
    ) -> str:
        function_argname = PythonFunctionDumper._get_python_function_argument_name_for_postgres_function_argument_name(
            postgres_function_arg.argument_name
        )
        return f"[astuple(x) for x in {function_argname}]"

    @staticmethod
    def _get_python_tuple_for_dataclass(
        postgres_function_arg: PostgresFunctionArgument,
    ) -> str:
        function_argname = PythonFunctionDumper._get_python_function_argument_name_for_postgres_function_argument_name(
            postgres_function_arg.argument_name
        )
        return f"astuple({function_argname})"

    @staticmethod
    def _get_python_execution_for_postgres_function(
        postgres_function: PostgresFunction,
        is_cursor: bool,
        base_indent: int,
    ) -> str:
        argument_placeholder_string = ", ".join(
            ["%s"] * len(postgres_function.function_args)
        )
        argument_names = [
            function_arg.argument_name
            for function_arg in postgres_function.function_args
        ]
        variable_assignment = "rows = " if is_cursor else ""
        executing_object = "cur" if is_cursor else "conn"
        argument_list_string = f"[{', '.join(argument_names)}]"
        execute_line = f"{base_indent * tab}{variable_assignment}{executing_object}.execute("
        select_line = f'{(base_indent + 1) * tab}"SELECT * FROM {postgres_function.function_name}({argument_placeholder_string})",'
        argument_line = f"{(base_indent + 1) * tab}{argument_list_string}"
        closing_bracket_lines = f"{base_indent * tab})"
        lines = [
            execute_line,
            select_line,
            argument_line,
            closing_bracket_lines,
        ]
        return "\n".join(lines)

    @staticmethod
    def _get_python_cursor_initialisation_for_postgres_function(
        postgres_function: PostgresFunction, base_indent: int
    ) -> str:
        python_return_type = PythonTypes.from_postgres_type(
            postgres_function.function_return
        )
        if (
            len(python_return_type) > 9
            and python_return_type[:9] == "Optional["
        ):
            python_return_type = python_return_type[9:-1]
        return f"{base_indent * tab}with conn.cursor(row_factory=class_row({python_return_type})) as cur:"
