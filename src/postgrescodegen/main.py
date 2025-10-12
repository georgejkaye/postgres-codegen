import argparse

from pathlib import Path

from postgrescodegen.classes import InputArgs
from postgrescodegen.processor import process_all_script_files
from postgrescodegen.watcher import start_watcher


def parse_arguments() -> InputArgs:
    parser = argparse.ArgumentParser(
        description="Generate Python code from PostgreSQL scripts"
    )
    parser.add_argument(
        "--input",
        type=Path,
        help="Path to the directory containing user Postgres scripts",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Path to the root directory of the Python package that will contain the generated code",
    )
    parser.add_argument(
        "--module",
        type=str,
        help="Name of the output Python module (e.g. 'api.db').",
    )
    parser.add_argument(
        "--watch",
        nargs="?",
        type=parse_bool_string,
        default=False,
        const=True,
        help="Watch for changes in the user scripts directory and regenerate code automatically.",
    )
    parser.add_argument(
        "--roll",
        nargs="?",
        type=parse_bool_string,
        default=False,
        const=True,
        help="Roll any scripts into the database before generating code",
    )
    parser.add_argument(
        "--dbhost",
        type=str,
        default="localhost",
        help="Host of the db the scripts should be rolled into",
    )
    parser.add_argument(
        "--dbport",
        type=int,
        default=5432,
        help="Port of the db the scripts should be rolled into",
    )
    parser.add_argument(
        "--dbname",
        type=str,
        default=None,
        help="Name of the db the scripts should be rolled into",
    )
    parser.add_argument(
        "--dbuser",
        type=str,
        default=None,
        help="User to use to roll the scripts into the db",
    )
    parser.add_argument(
        "--dbpassword",
        type=Path,
        default=None,
        help="Path to a file containing a password for the db the scripts should be rolled into",
    )
    args = parser.parse_args()
    return InputArgs(
        user_scripts_path=args.input,
        python_source_root=args.output,
        output_code_module=args.module,
        watch_files=args.watch,
        roll_scripts=args.roll,
        db_host=args.dbhost,
        db_port=args.dbport,
        db_name=args.dbname,
        db_user=args.dbuser,
        db_password_file=args.dbpassword,
    )


def main():
    args = parse_arguments()
    internal_scripts_path = Path(__file__) / ".." / ".." / "scripts"
    process_all_script_files(
        internal_scripts_path,
        args.user_scripts_path,
        args.python_source_root,
        args.output_code_module,
        args.roll_scripts,
    )
    if args.watch_files:
        start_watcher(
            internal_scripts_path,
            args.user_scripts_path,
            args.python_source_root,
            args.output_code_module,
            args.roll_scripts,
        )


def parse_bool_string(value: str) -> bool:
    return value != "0"


if __name__ == "__main__":
    main()
