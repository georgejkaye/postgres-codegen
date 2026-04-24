from pathlib import Path
import unittest

from postgrescodegen.generators.composites import (
    get_python_module_for_postgres_composite_file,
)

test_dir = Path(__file__).parent


class GeneratorsCompositesTests(unittest.TestCase):
    def test_get_postgres_composites_for_postgres_statements(self):
        (_, module) = get_python_module_for_postgres_composite_file(
            test_dir, "db", {}, test_dir / "test.sql"
        )

        self.assertEqual(len(module.module_objects), 2)


if __name__ == "__main__":
    unittest.main()
