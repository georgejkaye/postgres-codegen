from abc import abstractmethod


class PythonableObject:
    @abstractmethod
    def get_python_name(self) -> str:
        pass
