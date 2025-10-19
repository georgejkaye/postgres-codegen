import os
import shutil
from pathlib import Path

from postgrescodegen.classes import PostgresFileResult


def get_path_for_module(
    python_project_root: Path, python_module: str, is_leaf: bool
) -> Path:
    python_module_relative_path = Path(python_module.replace(".", "/"))
    python_module_path = python_project_root / f"{python_module_relative_path}"
    return Path(f"{python_module_path}.py") if is_leaf else python_module_path


def get_db_script_files(source_dir: Path) -> list[Path]:
    code_files: list[Path] = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            file_name, extension = os.path.splitext(file)
            if extension == ".sql":
                code_files.append(Path(os.path.join(root, f"{file_name}{extension}")))
    return code_files


def get_postgres_files_in_directory(code_dir: Path) -> PostgresFileResult:
    type_files = get_db_script_files(code_dir / "types")
    view_files = get_db_script_files(code_dir / "views")
    function_files = get_db_script_files(code_dir / "functions")
    return PostgresFileResult(type_files, view_files, function_files)


def clean_output_directory(python_package_path: Path, output_module: str):
    dest_module_path = get_path_for_module(
        python_package_path, output_module, is_leaf=False
    )
    if os.path.exists(dest_module_path):
        print(f"Cleaning {dest_module_path}")
        shutil.rmtree(dest_module_path)


def write_python_file(output_root_path: Path, module_name: str, file_contents: str):
    relative_module_path = Path(module_name.replace(".", "/"))
    output_path = output_root_path / f"{relative_module_path}.py"
    parent_directory = output_path.parent
    parent_directory.mkdir(parents=True, exist_ok=True)
    print(f"Writing {output_root_path.name}.{module_name} to {output_path}")
    with open(output_path, "w+") as f:
        f.write(file_contents)


def get_python_module_name_for_postgres_file(
    postgres_scripts_path: Path,
    source_file_path: Path,
    output_module_name: str,
) -> str:
    source_relative_path = source_file_path.relative_to(postgres_scripts_path)
    module_name = source_relative_path.stem
    if module_name[0].isdigit():
        module_name = module_name.split("_", maxsplit=1)[1]
    module_parent_names = list(source_relative_path.parts)[:-1]
    module_parts = [output_module_name]
    module_parts.extend(module_parent_names)
    module_parts.append(module_name)
    return ".".join(module_parts)


def create_py_typed_files_in_directory(
    python_package_path: Path, python_output_module: str
):
    python_output_module_path = get_path_for_module(
        python_package_path, python_output_module, False
    )
    for root, _, _ in os.walk(python_output_module_path):
        py_typed_file = Path(root) / "py.typed"
        with open(py_typed_file, "w") as _:
            pass
