def get_python_name_for_postgres_type_name(postgres_type_name: str) -> str:
    snake_case_name = "".join(
        x.capitalize() for x in postgres_type_name.lower().split("_")
    )
    if postgres_type_name[-8:].lower() == "_notnull":
        return snake_case_name[:-8]
    return snake_case_name


def get_python_name_for_postgres_function_name(
    postgres_function_name: str,
) -> str:
    return postgres_function_name.lower()
