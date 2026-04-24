postgres_primitives = set(
    [
        "VOID",
        "TEXT",
        "INT",
        "INTEGER",
        "BIGINT",
        "DECIMAL",
        "NUMERIC",
        "TIMESTAMP",
        "TIMESTAMP WITH TIME ZONE",
        "TIMESTAMP WITHOUT TIME ZONE",
        "INTERVAL",
        "DATERANGE",
        "BOOLEAN",
    ]
)


def is_user_defined_type(postgres_type_name: str) -> bool:
    return (
        get_base_postgres_type_for_postgres_type(postgres_type_name)
        not in postgres_primitives
    )


def is_postgres_array_type(postgres_type_name: str) -> bool:
    return postgres_type_name[-2:] == "[]"


def get_base_postgres_type_for_postgres_type(postgres_type_name: str) -> str:
    if is_postgres_array_type(postgres_type_name):
        postgres_type_name = postgres_type_name[:-2]
    if not is_postgres_type_nullable(postgres_type_name):
        return postgres_type_name[:-8]
    return postgres_type_name


def is_postgres_type_nullable(postgres_type: str) -> bool:
    return len(postgres_type) < 8 or postgres_type[-8:].lower() != "_notnull"
