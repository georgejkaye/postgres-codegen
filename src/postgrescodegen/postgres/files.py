from dataclasses import dataclass
from pathlib import Path


@dataclass
class PostgresFileResult:
    type_files: list[Path]
    view_files: list[Path]
    function_files: list[Path]
