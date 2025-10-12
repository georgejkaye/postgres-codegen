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
 project
 | db
 | | types
 | | | a.py
 | | | b.py
 | | functions
 | | | d.py
 | | | e.py
```


## Usage

### Inputs

However you run the tool, there are several arguments you will need to specify, summarised below.

|Input|Python argument|Environment variable|Notes|When required|Default|
|-|-|-|-|-|-|
| Input scripts directory | `--input` | `INPUT_SCRIPTS_DIR` | The directory containing all of the Postgres `*.sql` files to process ||
| Output package directory | `--output` | `OUTPUT_PACKAGE_DIR`|  The root directory of the Python package to generate the output it ||
| Output module name | `--module` | `OUTPUT_MODULE_NAME` | The absolute name of the module to put the generated output in, including the package root name ||
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

Once you have that installed, you can generate your code

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
            INPUT_SCRIPTS_DIR: /app/input
            OUTPUT_PACKAGE_DIR: /app/output
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