#!/bin/sh
poetry run python \
    -u \
    src/postgrescodegen/main.py \
    /app/input \
    /app/output \
    $OUTPUT_MODULE_NAME \
    --resources /app/resources \
    --watch $WATCH_FILES \
    --roll $ROLL_SCRIPTS \
    --dbhost $DB_HOST \
    --dbport $DB_PORT \
    --dbuser $DB_USER \
    --dbname $DB_NAME \
    --dbpassword $DB_PASSWORD_FILE
