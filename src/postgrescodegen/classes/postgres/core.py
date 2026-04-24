from abc import abstractmethod


class PostgresObject:
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_drop_statement(self) -> str:
        pass

    @abstractmethod
    def get_python_name(self) -> str:
        pass
