from abc import abstractmethod
from re import Match
from typing import Optional

from postgrescodegen.postgres.core import PostgresObject


class PostgresObjectParser[T: PostgresObject]:
    @staticmethod
    @abstractmethod
    def get_statement_regex() -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_postgres_object_for_match(match: Match[str]) -> Optional[T]:
        pass
