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

### As a Python script

Dependencies for this project are managed by [Poetry](https://python-poetry.org/).
To set up the virtual environment, run:

```sh
poetry install
```

Once you have that installed, you can generate your code 

```
poetry run python src/pythoncodegen --input <scripts directory> --pyroot <python project root> --pymodule <name of output python module>
```

To regenerate the generated code whenever a script file is edited, use the `--watch` flag.

```
poetry run python src/pythoncodegen --input <scripts directory> --pyroot <python project root> --pymodule <name of output python module> --watch
```

To also run in any scripts to your db at the same time, use the `--runscripts` flag.

```
poetry run python src/pythoncodegen \
    --input <scripts directory> \
    --pyroot <python project root> \ 
    --pymodule <name of output python module> \
    --runscripts
    --dbhost <db host, default localhost> \
    --dbport <db port, default 5432> \
    --dbuser <db user> \
    --dbpassword <path to a file containing the db password>
```


