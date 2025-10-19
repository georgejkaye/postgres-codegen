def is_postgres_array_type(postgres_type_name: str) -> bool:
    return postgres_type_name[-2:] == "[]"


def get_base_postgres_type_for_postgres_type(postgres_type_name: str) -> str:
    if is_postgres_array_type(postgres_type_name):
        return postgres_type_name[:-2]
    return postgres_type_name
