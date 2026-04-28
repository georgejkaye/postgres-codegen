from abc import abstractmethod
import re
from typing import Optional

from postgrescodegen.generators.parsers.process import PostgresObjectParser
from postgrescodegen.postgres.composites import (
    PostgresComposite,
    PostgresCompositeField,
)


class PostgresCompositeParser(PostgresObjectParser[PostgresComposite]):
    @staticmethod
    @abstractmethod
    def get_statement_regex() -> str:
        return r"CREATE TYPE (.*) AS \((.*)\)"

    @staticmethod
    def get_postgres_object_for_match(
        match: re.Match[str],
    ) -> Optional[PostgresComposite]:
        name = match.group(1)
        fields_string = match.group(2)
        fields: list[PostgresCompositeField] = []
        for type_clause in fields_string.split(","):
            type_clause_clauses = type_clause.strip().split(" ", 1)
            field_name = type_clause_clauses[0]
            field_type = type_clause_clauses[1]
            field = PostgresCompositeField(field_name, field_type)
            fields.append(field)
        return PostgresComposite(name, fields)
