# postgres-codegen

Tool to generate Python code for interacting with Postgres functions using [Psycopg 3](https://pypi.org/project/psycopg/).
Can function as a one-off script, or a watcher than continuously runs in new scripts to your db and updates the generated code.

## Overview

This tool scans all `*.sql` files in a directory of the following form:

```
scripts
| types
| | a.sql
| | b.sql
| views
| | c.sql
| functions
| | d.sql
| | e.sql
```

...and generates Python code for interacting with the functions in the following form:

```
 package
 | db
 | | types
 | | | a.py
 | | | b.py
 | | functions
 | | | d.py
 | | | e.py
```


## Running the tool

### Inputs

However you run the tool, there are several arguments you will need to specify, summarised below.

|Input|Argument (Python)|Environment variable (Docker)|Notes|When required|Default|
|-|-|-|-|-|-|
| Input scripts directory | | volume `/app/input` | The directory containing all of the Postgres `*.sql` files to process, structured as detailed above ||
| Output package directory | | volume `/app/output` |  The root directory of the Python package to generate the output ||
| Output module name | | `OUTPUT_MODULE_NAME` | The absolute name of the module to put the generated output in, including the package name (e.g. the above example would be `package.db`) ||
| Resources directory | `--module` | included in container | Path to the provided resources directory | | `<main.py>/../../resources` |
| Watch mode | `--watch` | `WATCH_FILES` | Whether to continuously monitor files in the scripts directory | | `0` |
| Roll mode | `--roll` | `ROLL_SCRIPTS` | Whether to roll in scripts to the db after generating code | | `0` |
| Database host | `--dbhost` | `DB_HOST` | Host of the db to roll scripts into | For rolling in scripts | `localhost` |
| Database port | `--dbport` | `DB_PORT` | Port of the db to roll scripts into | For rolling in scripts | `5432` |
| Database user | `--dbuser` | `DB_USER` | User of the db to roll scripts into | For rolling in scripts | |
| Database port | `--dbpassword` | `DB_PASSWORD_FILE` | Path to file containing the password for the db to roll scripts into | For rolling in scripts | |


### As a Python script

Dependencies for this project are managed by [Poetry](https://python-poetry.org/).
To set up the virtual environment, run:

```sh
poetry install
```

Once you have that installed, you can generate your code:

```sh
poetry run python src/pythoncodegen \
    --input <scripts directory> \
    --output <python project root> \
    --module <name of output python module>
```

To regenerate the generated code whenever a script file is edited, use the `--watch` flag.

```sh
poetry run python src/pythoncodegen \
    --input <scripts directory> \
    --output <python project root> \
    --module <name of output python module> \
    --watch
```

To also run in any scripts to your db at the same time, use the `--runscripts` flag.
With this you will need to specify your db connection details.

```sh
poetry run python src/pythoncodegen \
    --input <scripts directory> \
    --output <python project root> \
    --module <name of output python module> \
    --roll
    --dbhost <db host, default localhost> \
    --dbport <db port, default 5432> \
    --dbuser <db user> \
    --dbpassword <path to a file containing the db password>
```

### Docker Compose

To avoid faffing around with dependencies you can run the tool in a [Docker](https://www.docker.com/) container.
The easiest way to do this is by using [Docker Compose](https://docs.docker.com/compose/) and including the following in your `docker-compose.yml` file.

```yml
services:
    codegen:
        image: georgejkaye/postgres-codegen:latest
        environment:
            OUTPUT_MODULE_NAME: output.db
            WATCH_MODE: 1
            ROLL_MODE: 1
            DB_HOST: georgejkaye.com
            DB_PORT: 5432
            DB_USER: george
            DB_NAME: db
            DB_PASSWORD_FILE: /run/secrets/db_secret
        secrets:
            - db_secret

secrets:
    db_secret:
        file: db.secret
```

Running the tool is then as simple as:

```sh
docker compose up --build
```

An example `docker-compose.yml` file is provided in this repo, set up to receive environment variables from a `.env` file.

### Raw docker image

If you prefer, you can use the raw docker image and run it yourself.

```sh
# pull from docker hub
docker pull georgejkaye/docker-codegen:latest

# build locally
docker build -t docker-codegen .
```

Unfortunately secrets are a little more complicated in this scenario, so you may have to set up a [Docker Swarm](https://docs.docker.com/engine/swarm/) to set up your [secrets](https://docs.docker.com/engine/swarm/secrets/).

## Generating code

### Writing db code

First of course you'll need to write your db code!
The tool recognises types and functions of the following form
(modulo unnecessary whitespace, which is all stripped out before processing).

```sql
-- input/types/row.sql

CREATE TYPE output_row AS (
    field1 INT,
    field2 TEXT
);
```

```sql
-- input/functions/row.sql

CREATE OR REPLACE FUNCTION select_rows (
    arg1 INT,
    arg2 TEXT
)
RETURNS SETOF output_row
LANGUAGE sql -- other languages are available
AS
$$
SELECT field1, field2 FROM row_table;
$$;
```

As Postgres does not provide a native way to declare fields of types as nullable, by default all fields will be mapped
to `Optional` types in the generated Python code.
To avoid this, you can define your fields using the non-null domains defined in `resources/sql/domains.sql`.
These are run in automatically alongside the rest of your code in you use the `ROLL_SCRIPTS` option.

| Postgres type | Non-null domain |
|-|-|
| `TEXT` | `TEXT_NOTNULL` |
| `INTEGER` | `TEXT_NOTNULL` |
| `DECIMAL` | `TEXT_NOTNULL` |
| `TIMESTAMP WITH TIME ZONE` | `TIMESTAMP_NOTNULL` |
| `INTERVAL` | `INTERVAL_NOTNULL` |
| `BOOLEAN` | `BOOLEAN_NOTNULL` |

Note that returning nullable types is currently not supported,
and all returned composite types are treated as non-nullable accordingly.


### Registering the types

When talking to a Postgres database using Psycopg 3, you must *register* all the Postgres types used so they can be appropriately encoded.
To do this a `types/register.py` script is generated containing a function you can call to register all the types.

```py
def register_types(conn: psycopg.Connection) -> None
```

This can be called at the start of your program to initialise everything.
This ensures  that

```py
from psycopg import Connection

conn = Connection.connect(
    host="georgejkaye.com",
    dbname="db",
    user="db",
    password="password"
)
register_types(conn)
```

### Calling the functions

Then you can call the generated functions!
For each non-`VOID` returning function in the input script directory,
two python functions are generated: one to fetch a single row
(which may return `None` if the db function doesn't return a row at all),
and one to fetch all the rows.

```sql
CREATE OR REPLACE FUNCTION select_rows (
    arg1 INTEGER_NOTNULL,
    arg2 TEXT
)
RETURNS SETOF output_row
```

```py
def select_rows_fetchone(conn: psycopg.Connection, arg1: int, arg2: Optional[str]) -> Optional[OutputRow]:

def select_rows_fetchall(conn: psycopg.Connection, arg1: int, arg2: Optional[str]) -> list[OutputRow]:
```

For `VOID`-returning functions, there's no need for multiple functions so only a single one is created.


```sql
CREATE OR REPLACE FUNCTION insert_rows (
    arg1 TIMESTAMP_NOTNULL,
    arg2 row_data
)
RETURNS VOID
```

```py
def insert_rows(conn: psycopg.Connection, arg1: datetime, arg2: RowData) -> None:
```