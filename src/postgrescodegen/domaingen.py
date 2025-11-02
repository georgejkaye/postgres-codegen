import re
from typing import Optional
from postgrescodegen.classes import PostgresDomain, PythonPostgresModuleLookup

domain_regex = r"CREATE DOMAIN (.*) AS ([A-z_]*) (?:.*)"


def get_postgres_domain_for_statement(
    statement: str,
) -> Optional[PostgresDomain]:
    domain_matches = re.match(domain_regex, statement)
    if domain_matches is None:
        return None
    postgres_domain_name = domain_matches.group(1)
    postgres_underlying_type_name = domain_matches.group(2)
    return PostgresDomain(postgres_domain_name, postgres_underlying_type_name)


def get_python_code_for_postgres_domain(
    python_postgres_module_lookup: PythonPostgresModuleLookup,
    postgres_domains: list[PostgresDomain],
) -> str:
    return ""
