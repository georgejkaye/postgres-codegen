import re
from typing import Optional

from postgrescodegen.postgres.domains import PostgresDomain
from postgrescodegen.generators.python.python import PythonPostgresModuleLookup
from postgrescodegen.generators.translators.translator import Translator

domain_regex = r"CREATE DOMAIN (.*) AS ([A-z_]*) (?:.*)"


class DomainTranslator(Translator[PostgresDomain]):
    def get_postgres_object_for_statement(
        self, statement: str
    ) -> Optional[PostgresDomain]:
        domain_matches = re.match(domain_regex, statement)
        if domain_matches is None:
            return None
        postgres_domain_name = domain_matches.group(1)
        postgres_underlying_type_name = domain_matches.group(2)
        return PostgresDomain(
            postgres_domain_name, postgres_underlying_type_name
        )

    def get_python_code_for_postgres_objects(
        self,
        modules: PythonPostgresModuleLookup,
        postgres_objects: list[PostgresDomain],
    ) -> str:
        return ""
