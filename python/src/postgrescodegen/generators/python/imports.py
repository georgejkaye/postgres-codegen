from postgrescodegen.generators.python.python import PythonImportDict

tab = "    "


class PythonImports:
    @staticmethod
    def get_stdlib_imports_for_python_code_str(
        python_code_str: str,
    ) -> str:
        python_imports: list[str] = ["from dataclasses import dataclass"]
        if PythonImports._check_if_type_in_code(python_code_str, "datetime"):
            python_imports.append("from datetime import datetime")
        if PythonImports._check_if_type_in_code(python_code_str, "timedelta"):
            python_imports.append("from datetime import timedelta")
        if PythonImports._check_if_type_in_code(python_code_str, "Decimal"):
            python_imports.append("from decimal import Decimal")
        if "Optional[" in python_code_str:
            python_imports.append("from typing import Optional")
        if PythonImports._check_if_type_in_code(python_code_str, "Range"):
            python_imports.append("from psycopg.types.range import Range")
        return "\n".join(python_imports)

    @staticmethod
    def get_import_statements_for_python_import_dict(
        import_dict: PythonImportDict,
    ) -> str:
        import_statements = [
            PythonImports._get_import_statement_for_module(
                module, import_dict[module]
            )
            for module in import_dict.keys()
        ]
        return "\n".join(import_statements)

    @staticmethod
    def update_python_type_import_dict(
        imports_dict: PythonImportDict, type_module: str, type_name: str
    ) -> PythonImportDict:
        module_result = imports_dict.get(type_module)
        if module_result is None:
            imports_dict[type_module] = set([type_name])
            return imports_dict
        if type_name in module_result:
            return imports_dict
        imports_dict[type_module].add(type_name)
        return imports_dict

    @staticmethod
    def _get_import_statement_for_module(
        module_name: str, tokens: set[str]
    ) -> str:
        lines = [f"from {module_name} import ("]
        sorted_tokens = sorted(tokens)
        for token in sorted_tokens:
            lines.append(f"{tab}{token},")
        lines.append(")")
        return "\n".join(lines)

    @staticmethod
    def _check_if_type_in_code(
        python_code_str: str, type_to_check: str
    ) -> bool:
        return (
            f": {type_to_check}" in python_code_str
            or f"[{type_to_check}]" in python_code_str
            or f"[{type_to_check}[" in python_code_str
        )
