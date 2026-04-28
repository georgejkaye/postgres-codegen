import re
from typing import Optional
from postgrescodegen.parsers.parser import PostgresObjectParser
from postgrescodegen.postgres.functions import (
    PostgresFunction,
    PostgresFunctionArgument,
)


class PostgresFunctionParser(PostgresObjectParser[PostgresFunction]):
    @staticmethod
    def get_statement_regex() -> str:
        return r"CREATE(?: OR REPLACE)? FUNCTION ([A-z_]*)(?: )?\((.*)\).*RETURNS(?: SETOF)? (.*?) LANGUAGE"

    @staticmethod
    def get_postgres_object_for_match(
        match: re.Match[str],
    ) -> Optional[PostgresFunction]:
        function_name = match.group(1)
        function_args_str = match.group(2)
        function_return = match.group(3)
        postgres_function_args = PostgresFunctionParser._get_postgres_function_args_from_argument_str(
            function_args_str
        )
        return PostgresFunction(
            function_name, function_return, postgres_function_args
        )

    @staticmethod
    def _get_postgres_function_args_from_argument_str(
        argument_str: str,
    ) -> list[PostgresFunctionArgument]:
        if argument_str == "":
            return []
        function_arg_split = argument_str.split(",")
        postgres_function_args: list[PostgresFunctionArgument] = []
        for function_arg in function_arg_split:
            function_arg_split = function_arg.strip().split(maxsplit=1)
            function_arg_name = function_arg_split[0]
            function_arg_type = function_arg_split[1]
            function_arg_type_without_default = re.split(
                " DEFAULT", function_arg_type, flags=re.IGNORECASE
            )[0]
            postgres_function_arg = PostgresFunctionArgument(
                function_arg_name, function_arg_type_without_default
            )
            postgres_function_args.append(postgres_function_arg)
        return postgres_function_args
