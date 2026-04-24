import os
import shutil

from pathlib import Path
from typing import Callable, Optional

from postgrescodegen.classes.input import DbCredentials
from postgrescodegen.classes.postgres.core import PostgresObject
from postgrescodegen.classes.postgres.domains import PostgresDomain
from postgrescodegen.classes.postgres.functions import PostgresFunction
from postgrescodegen.classes.postgres.types import PostgresType
from postgrescodegen.classes.python import (
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
from postgrescodegen.generators.domains import (
    get_postgres_domains_for_file,
    get_postgres_module_for_postgres_domain_file,
)
from postgrescodegen.generators.functions import (
    get_python_postgres_module_for_postgres_function_file,
)
from postgrescodegen.generators.register import get_register_module_code
from postgrescodegen.process.db import run_in_query, run_in_script_file
from postgrescodegen.generators.types import (
    get_python_postgres_module_for_postgres_type_file,
)


def roll_script_file[T: PostgresObject](
    db_credentials: DbCredentials, script_file: Path, module_objects: list[T]
):
    drop_statements = [
        module_object.get_drop_statement() for module_object in module_objects
    ]
    drop_query = " ".join(drop_statements)
    run_in_query(
        db_credentials,
        drop_query,
        f"Running drop statements for {script_file}",
    )
    run_in_script_file(db_credentials, script_file)


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
) -> Optional[
    tuple[PythonPostgresModuleLookup, PythonPostgresModule[T], Optional[Path]]
]:
    try:
        python_postgres_module_lookup, script_file_module = (
            get_script_file_module(
                postgres_scripts_path,
                python_output_module,
                python_postgres_module_lookup,
                script_file,
            )
        )
        if roll_scripts and db_credentials is not None:
            roll_script_file(
                db_credentials, script_file, script_file_module.module_objects
            )
        if len(script_file_module.module_objects) > 0:
            generated_file_path = write_python_file(
                python_package_path,
                script_file_module.module_name,
                script_file_module.python_code,
            )
        else:
            generated_file_path = None
        return (
            python_postgres_module_lookup,
            script_file_module,
            generated_file_path,
        )
    except Exception as e:
        print(f"Error processing script file {script_file}: {e}")
        return None


def process_type_script_file(
    postgres_input_root_path: Path,
    python_output_root_module: str,
    python_output_root_path: Path,
    roll_scripts: bool,
    db_credentials: Optional[DbCredentials],
    python_postgres_module_lookup: PythonPostgresModuleLookup,
    script_file: Path,
) -> Optional[
    tuple[
        PythonPostgresModuleLookup,
        PythonPostgresModule[PostgresType],
        Optional[Path],
    ]
]:
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
) -> Optional[
    tuple[
        PythonPostgresModuleLookup,
        PythonPostgresModule[PostgresFunction],
        Optional[Path],
    ]
]:
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
    if roll_scripts and db_credentials is not None:
        if Path(resources_path / "domains").is_dir():
            internal_domain_files = get_db_script_files(resources_path / "sql")
            for file in internal_domain_files:
                domains = get_postgres_domains_for_file(file)
                roll_script_file(db_credentials, file, domains)


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
    postgres_domains: list[PostgresDomain],
) -> Path:
    register_type_module = get_register_module_code(
        python_postgres_module_lookup, postgres_types, postgres_domains
    )
    return write_python_file(
        output_root_path,
        f"{output_module_name}.types.register",
        register_type_module,
    )


def process_user_script_files(
    python_source_root: Path,
    output_code_module: str,
    user_scripts_path: Path,
    roll_scripts: bool,
    db_credentials: Optional[DbCredentials],
) -> list[Path]:
    user_files = get_postgres_files_in_directory(user_scripts_path)
    python_postgres_module_lookup: PythonPostgresModuleLookup = {}
    generated_files: list[Path] = []
    postgres_types: list[PostgresType] = []
    postgres_domains: list[PostgresDomain] = []
    for file in user_files.type_files:
        type_module_result = process_type_script_file(
            user_scripts_path,
            output_code_module,
            python_source_root,
            roll_scripts,
            db_credentials,
            python_postgres_module_lookup,
            file,
        )
        if type_module_result is None:
            continue
        python_postgres_module_lookup, module, generated_file_path = (
            type_module_result
        )
        if generated_file_path is not None:
            postgres_types.extend(module.module_objects)
            generated_files.append(generated_file_path)
        python_postgres_module_lookup, domain_module_result = (
            get_postgres_module_for_postgres_domain_file(
                user_scripts_path,
                output_code_module,
                python_postgres_module_lookup,
                file,
            )
        )
        postgres_domains.extend(domain_module_result.module_objects)
    generated_file_path = process_register_types_file(
        python_source_root,
        output_code_module,
        python_postgres_module_lookup,
        postgres_types,
        postgres_domains,
    )
    generated_files.append(generated_file_path)
    for file in user_files.view_files:
        process_view_script_file(roll_scripts, db_credentials, file)
    for file in user_files.function_files:
        type_module_result = process_function_script_file(
            user_scripts_path,
            output_code_module,
            python_source_root,
            roll_scripts,
            db_credentials,
            python_postgres_module_lookup,
            file,
        )
        if type_module_result is None:
            continue
        _, _, generated_file_path = type_module_result
        if generated_file_path is not None:
            generated_files.append(generated_file_path)
    return generated_files


def process_all_script_files(
    resources_path: Path,
    user_scripts_path: Path,
    python_source_root: Path,
    output_code_module: str,
    roll_scripts: bool,
    db_credentials: Optional[DbCredentials],
):
    process_internal_script_files(resources_path, roll_scripts, db_credentials)
    copy_python_resources(
        resources_path, python_source_root, output_code_module
    )
    generated_files = process_user_script_files(
        python_source_root,
        output_code_module,
        user_scripts_path,
        roll_scripts,
        db_credentials,
    )
    generated_py_typed_files = create_py_typed_files_in_directory(
        python_source_root, output_code_module
    )
    clean_output_directory(
        python_source_root,
        output_code_module,
        generated_files + generated_py_typed_files,
    )
