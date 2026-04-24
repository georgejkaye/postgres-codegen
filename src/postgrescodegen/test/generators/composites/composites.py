from pathlib import Path
import unittest

from postgrescodegen.generators.composites import (
    get_python_module_for_postgres_composite_file,
)

test_dir = Path(__file__).parent


class GeneratorsCompositesTests(unittest.TestCase):
    def one(self):
        (_, module) = get_python_module_for_postgres_composite_file(
            test_dir, "db", {}, test_dir / "one.sql"
        )

        self.assertEqual(len(module.module_objects), 1)

        type_a = module.module_objects[0]

        self.assertEqual(len(type_a.composite_fields), 2)

        self.assertEqual(type_a.composite_fields[0].field_name, "field_a")
        self.assertEqual(type_a.composite_fields[0].field_type, "INTEGER")

        self.assertEqual(type_a.composite_fields[1].field_name, "field_b")
        self.assertEqual(type_a.composite_fields[1].field_type, "TEXT")


if __name__ == "__main__":
    unittest.main()
