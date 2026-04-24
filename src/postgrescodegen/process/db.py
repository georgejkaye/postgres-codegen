import os
import subprocess
from pathlib import Path
from typing import Mapping, Optional

from postgrescodegen.classes.input import DbCredentials


def run_psql(db_credentials: DbCredentials, args: list[str]):
    env: Mapping[str, str] = dict(os.environ)
    env["PGPASSWORD"] = db_credentials.password
    base_args = [
        "psql",
        "-h",
        db_credentials.host,
        "-p",
        str(db_credentials.port),
        "-d",
        db_credentials.name,
        "-U",
        db_credentials.user,
    ]
    all_args = base_args + args
    try:
        subprocess.check_output(
            all_args,
            stderr=subprocess.STDOUT,
            env=env,
        )
    except subprocess.CalledProcessError as e:
        error_output = e.output.decode("utf-8")
        print(error_output, flush=True)
        print()
        raise
    else:
        pass


def run_in_query(
    db_credentials: DbCredentials, query: str, message: Optional[str] = None
):
    if message is not None:
        print(message)
    else:
        print(f"Running in query {query}")
    run_psql(db_credentials, ["-c", query, "-q"])


def run_in_script_file(db_credentials: DbCredentials, script_file: Path):
    print(f"Running in {script_file}")
    run_psql(db_credentials, ["-f", str(script_file), "-q"])
