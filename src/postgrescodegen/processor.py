import os
import shutil

from pathlib import Path
from typing import Callable, Optional

from postgrescodegen.classes import (
    DbCredentials,
    PostgresFunction,
    PostgresObject,
    PostgresType,
    PythonPostgresModule,
    PythonPostgresModuleLookup,
)
from postgrescodegen.files import (
    clean_output_directory,
    create_py_typed_files_in_directory,
    get_db_script_files,
    get_postgres_files_in_directory,
    write_python_file,
)
from postgrescodegen.funcgen import (
    get_python_postgres_module_for_postgres_function_file,
)
from postgrescodegen.register import get_register_module_code
from postgrescodegen.runner import run_in_script_file
from postgrescodegen.typegen import (
    get_python_postgres_module_for_postgres_type_file,
)


def process_script_file[T: PostgresObject](
    postgres_scripts_path: Path,
    python_output_module: str,
    python_package_path: Path,
    roll_scripts: bool,
    db_credentials: Optional[DbCredentials],
    python_postgres_module_lookup: PythonPostgresModuleLookup,
    get_script_file_module: Callable[
        [Path, str, PythonPostgresModuleLookup, Path],
        tuple[PythonPostgresModuleLookup, PythonPostgresModule[T]],
    ],
    script_file: Path,
) -> tuple[PythonPostgresModuleLookup, PythonPostgresModule[T]]:
    if roll_scripts and db_credentials is not None:
        run_in_script_file(db_credentials, script_file)
    python_postgres_module_lookup, script_file_module = get_script_file_module(
        postgres_scripts_path,
        python_output_module,
        python_postgres_module_lookup,
        script_file,
    )
    write_python_file(
        python_package_path,
        script_file_module.module_name,
        script_file_module.python_code,
    )
    return python_postgres_module_lookup, script_file_module


def process_type_script_file(
    postgres_input_root_path: Path,
    python_output_root_module: str,
    python_output_root_path: Path,
    roll_scripts: bool,
    db_credentials: Optional[DbCredentials],
    python_postgres_module_lookup: PythonPostgresModuleLookup,
    script_file: Path,
) -> tuple[PythonPostgresModuleLookup, PythonPostgresModule[PostgresType]]:
    print(f"Processing type file {script_file}")
    return process_script_file(
        postgres_input_root_path,
        python_output_root_module,
        python_output_root_path,
        roll_scripts,
        db_credentials,
        python_postgres_module_lookup,
        get_python_postgres_module_for_postgres_type_file,
        script_file,
    )


def process_view_script_file(
    roll_scripts: bool,
    db_credentials: Optional[DbCredentials],
    script_file: Path,
):
    print(f"Processing view file {script_file}")
    if roll_scripts and db_credentials is not None:
        run_in_script_file(db_credentials, script_file)


def process_function_script_file(
    postgres_input_root_path: Path,
    python_output_root_module: str,
    python_output_root_path: Path,
    roll_scripts: bool,
    db_credentials: Optional[DbCredentials],
    python_postgres_module_lookup: PythonPostgresModuleLookup,
    script_file: Path,
) -> tuple[PythonPostgresModuleLookup, PythonPostgresModule[PostgresFunction]]:
    print(f"Processing function file {script_file}")
    return process_script_file(
        postgres_input_root_path,
        python_output_root_module,
        python_output_root_path,
        roll_scripts,
        db_credentials,
        python_postgres_module_lookup,
        get_python_postgres_module_for_postgres_function_file,
        script_file,
    )


def process_internal_script_files(
    resources_path: Path,
    roll_scripts: bool,
    db_credentials: Optional[DbCredentials],
):
    internal_files = get_db_script_files(resources_path / "sql")
    for file in internal_files:
        if roll_scripts and db_credentials is not None:
            run_in_script_file(db_credentials, file)


def copy_python_resources(
    resources_path: Path, python_source_root: Path, output_code_module: str
):
    python_resources_path = resources_path / "python"
    for root, _, files in os.walk(python_resources_path):
        for file in files:
            full_path = Path(root) / file
            relative_path = full_path.relative_to(python_resources_path)
            dest_path = (
                python_source_root
                / output_code_module.split(".", maxsplit=1)[1].replace(".", "/")
                / relative_path
            )
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(full_path, dest_path)


def process_register_types_file(
    output_root_path: Path,
    output_module_name: str,
    python_postgres_module_lookup: PythonPostgresModuleLookup,
    postgres_types: list[PostgresType],
):
    register_type_module = get_register_module_code(
        python_postgres_module_lookup,
        postgres_types,
    )
    write_python_file(
        output_root_path, f"{output_module_name}.types.register", register_type_module
    )


def process_user_script_files(
    python_source_root: Path,
    output_code_module: str,
    user_scripts_path: Path,
    roll_scripts: bool,
    db_credentials: Optional[DbCredentials],
):
    user_files = get_postgres_files_in_directory(user_scripts_path)
    python_postgres_module_lookup: PythonPostgresModuleLookup = {}
    postgres_types: list[PostgresType] = []
    for file in user_files.type_files:
        python_postgres_module_lookup, module = process_type_script_file(
            user_scripts_path,
            output_code_module,
            python_source_root,
            roll_scripts,
            db_credentials,
            python_postgres_module_lookup,
            file,
        )
        postgres_types.extend(module.module_objects)
    process_register_types_file(
        python_source_root,
        output_code_module,
        python_postgres_module_lookup,
        postgres_types,
    )
    for file in user_files.view_files:
        process_view_script_file(roll_scripts, db_credentials, file)
    for file in user_files.function_files:
        process_function_script_file(
            user_scripts_path,
            output_code_module,
            python_source_root,
            roll_scripts,
            db_credentials,
            python_postgres_module_lookup,
            file,
        )


def process_all_script_files(
    resources_path: Path,
    user_scripts_path: Path,
    python_source_root: Path,
    output_code_module: str,
    roll_scripts: bool,
    db_credentials: Optional[DbCredentials],
):
    clean_output_directory(python_source_root, output_code_module)
    process_internal_script_files(resources_path, roll_scripts, db_credentials)
    copy_python_resources(resources_path, python_source_root, output_code_module)
    process_user_script_files(
        python_source_root,
        output_code_module,
        user_scripts_path,
        roll_scripts,
        db_credentials,
    )
    create_py_typed_files_in_directory(python_source_root, output_code_module)
