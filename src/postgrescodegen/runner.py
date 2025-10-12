import os
import subprocess
from pathlib import Path
from typing import Mapping

from postgrescodegen.classes import DbCredentials


def run_in_script_file(db_credentials: DbCredentials, script_file: Path):
    print(f"Running in {script_file}")
    env: Mapping[str, str] = dict(os.environ)
    env["PGPASSWORD"] = db_credentials.password
    try:
        subprocess.check_output(
            [
                "psql",
                "-h",
                db_credentials.host,
                "-p",
                str(db_credentials.port),
                "-d",
                db_credentials.name,
                "-U",
                db_credentials.user,
                "-f",
                str(script_file),
                "-q",
            ],
            stderr=subprocess.STDOUT,
            env=env,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error while running in {script_file}", flush=True)
        error_output = e.output.decode("utf-8")
        print(error_output, flush=True)
        print()
    else:
        pass
