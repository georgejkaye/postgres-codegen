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


class PostgresTypes:
    @staticmethod
    def is_array(type_name: str) -> bool:
        return type_name[-2:] == "[]"

    @staticmethod
    def is_nullable(type_name: str) -> bool:
        return len(type_name) < 8 or type_name[-8:].lower() != "_notnull"

    @staticmethod
    def get_base_type(type_name: str) -> str:
        if PostgresTypes.is_array(type_name):
            type_name = type_name[:-2]
        if not PostgresTypes.is_nullable(type_name):
            return type_name[:-8]
        return type_name

    @staticmethod
    def is_composite(type_name: str) -> bool:
        return PostgresTypes.get_base_type(type_name) not in postgres_primitives
