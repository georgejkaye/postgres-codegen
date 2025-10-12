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
    --ouput <python project root> \
    --module <name of output python module>
```

To regenerate the generated code whenever a script file is edited, use the `--watch` flag.

```sh
poetry run python src/pythoncodegen \
    --input <scripts directory> \
    --pyroot <python project root> \
    --pymodule <name of output python module> \
    --watch
```

To also run in any scripts to your db at the same time, use the `--runscripts` flag.
With this you will need to specify your db connection details.

```sh
poetry run python src/pythoncodegen \
    --input <scripts directory> \
    --output <python project root> \
    --module <name of output python module> \
    --runscripts
    --dbhost <db host, default localhost> \
    --dbport <db port, default 5432> \
    --dbuser <db user> \
    --dbpassword <path to a file containing the db password>
```

### As a Docker image

Rather than having to faff with dependencies you can run the tool using [Docker](https://www.docker.com/).
You can retrieve the latest prebuilt image by pulling it from Docker Hub:

```sh
# To get latest main version
docker pull georgejkaye/postgres-codegen:latest
```

You can then run the image using `docker run`:

```sh
# Specify variables explicitly
docker run georgejkaye/postgres-codegen \
    -e INPUT_SCRIPTS_DIR=/home/george/scripts \
    -e OUTPUT_PACKAGE_DIR=/home/george/output \
    -e OUTPUT_MODULE_NAME=output.db \
    -e WATCH_MODE=1 \
    -e ROLL_MODE=1 \
    -e DB_HOST=georgejkaye.com \
    -e DB_PORT=5432 \
    -e DB_USER=george \
    -e DB_NAME=db \
    -e DB_PASSWORD_FILE=db.secret

# Use .env file
docker run georgejkaye/postgres-codegen --env-file .env
```

Alternatively you can build the image yourself locally.

```sh
docker build . -t postgres-codegen
docker run postgres-codegen ...
```

### Docker Compose

In a large project you may be using [Docker Compose](https://docs.docker.com/compose/) to orchestrate your containers.
In this case you can just include the image in your `docker-compose.yml` file.

```yml
services:
    codegen:
        image: georgejkaye/docker-codegen
        environment:
            INPUT_SCRIPTS_DIR: /home/george/scripts
            OUTPUT_PACKAGE_DIR: /home/george/output
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
    db_secret: db.secret
```

