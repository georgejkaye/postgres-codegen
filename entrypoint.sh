#!/bin/sh

poetry run python \
    -u \
    src/watcher/main.py \
    --input $INPUT_SCRIPT_DIR \
    --output $OUTPUT_PACKAGE_DIR \
    --module $OUTPUT_MODULE_NAME \
    --watch $WATCH_FILES \
    --roll $ROLL_SCRIPTS \
    --dbhost $DB_HOST \
    --dbport $DB_PORT \
    --dbuser $DB_USER \
    --dbname $DB_NAME \
    --dbpassword $DB_PASSWORD_FILE
