from re import Match
from typing import Optional
from postgrescodegen.parsers.parser import PostgresObjectParser
from postgrescodegen.postgres.domains import PostgresDomain


class PostgresDomainParser(PostgresObjectParser[PostgresDomain]):
    @staticmethod
    def get_statement_regex() -> str:
        return r"CREATE DOMAIN (.*) AS ([A-z_]*) (?:.*)"

    @staticmethod
    def get_postgres_object_for_statement(
        match: Match[str],
    ) -> Optional[PostgresDomain]:
        domain_name = match.group(1)
        underlying_type_name = match.group(2)
        return PostgresDomain(domain_name, underlying_type_name)
