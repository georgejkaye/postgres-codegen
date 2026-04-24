from pathlib import Path

from postgrescodegen.generators.composites import (
    get_python_module_for_postgres_composite_file,
)

test_dir = Path(__file__).parent


def test_one():
    (_, module) = get_python_module_for_postgres_composite_file(
        test_dir, "db", {}, test_dir / "one.sql"
    )

    assert len(module.module_objects) == 1

    type_a = module.module_objects[0]

    assert len(type_a.composite_fields) == 2

    assert type_a.composite_fields[0].field_name == "field_a"
    assert type_a.composite_fields[0].field_type == "INTEGER"

    assert type_a.composite_fields[1].field_name == "field_b"
    assert type_a.composite_fields[1].field_type == "TEXT"
