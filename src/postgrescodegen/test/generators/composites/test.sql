CREATE TYPE test_type_a AS (
    field_a INTEGER,
    field_b TEXT
);

CREATE TYPE test_type_b AS (
    field_a INTEGER_NOTNULL,
    field_b TEXT_NOTNULL,
    field_c test_type_a
);