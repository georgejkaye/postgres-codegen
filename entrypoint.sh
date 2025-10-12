#!/bin/sh

INPUT_SCRIPT_DIR=$1
OUTPUT_PROJECT_ROOT_DIR=$2
OUTPUT_MODULE=$3

poetry run python \
    -u \
    src/watcher/main.py \
    $INPUT_SCRIPT_DIR \
    $OUTPUT_PROJECT_ROOT_DIR \
    $OUTPUT_MODULE 
