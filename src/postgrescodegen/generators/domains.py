from pathlib import Path
import re
from typing import Optional

from postgrescodegen.classes.postgres.domains import PostgresDomain
from postgrescodegen.classes.python import (
    PythonPostgresModule,
    PythonPostgresModuleLookup,
)
from postgrescodegen.generators.core import (
    get_postgres_module_for_postgres_file,
    get_postgres_objects_for_postgres_file,
)

domain_regex = r"CREATE DOMAIN (.*) AS ([A-z_]*) (?:.*)"


def get_postgres_domains_for_file(file_path: Path) -> list[PostgresDomain]:
    return get_postgres_objects_for_postgres_file(
        _get_postgres_domain_for_statement, file_path
    )


def get_postgres_module_for_postgres_domain_file(
    postgres_scripts_path: Path,
    python_output_module: str,
    python_postgres_module_lookup: PythonPostgresModuleLookup,
    file_path: Path,
) -> tuple[PythonPostgresModuleLookup, PythonPostgresModule[PostgresDomain]]:
    return get_postgres_module_for_postgres_file(
        _get_postgres_domain_for_statement,
        _get_python_code_for_postgres_domain,
        postgres_scripts_path,
        python_output_module,
        python_postgres_module_lookup,
        file_path,
    )


def _get_python_code_for_postgres_domain(
    python_postgres_module_lookup: PythonPostgresModuleLookup,
    postgres_domains: list[PostgresDomain],
) -> str:
    return ""


def _get_postgres_domain_for_statement(
    statement: str,
) -> Optional[PostgresDomain]:
    domain_matches = re.match(domain_regex, statement)
    if domain_matches is None:
        return None
    postgres_domain_name = domain_matches.group(1)
    postgres_underlying_type_name = domain_matches.group(2)
    return PostgresDomain(postgres_domain_name, postgres_underlying_type_name)
