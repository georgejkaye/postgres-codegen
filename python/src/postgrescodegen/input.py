from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class DbCredentials:
    host: str
    port: int
    name: str
    user: str
    password: str


@dataclass
class InputArgs:
    user_scripts_path: Path
    python_source_root: Path
    output_code_module: str
    resources_path: Path
    watch_files: bool
    roll_scripts: bool
    db_credentials: Optional[DbCredentials]
