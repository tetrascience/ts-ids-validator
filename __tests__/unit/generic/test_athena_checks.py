from pathlib import Path

import pytest

from ids_validator.checks import AthenaChecker
from ids_validator.ids_node import Node
from ids_validator.utils import read_schema, Log


UNIT_TEST_FILES = Path("__tests__/unit/generic/files/athena")

dirs_to_expected = {
    "invalid_path": [
        (
            ("Athena.js: Cannot find following " "properties in IDS: ['project.time']"),
            Log.CRITICAL.value,
        )
    ],
    "partition_name_path_conflict": [
        (
            ("Athena.js: Following names are " "conflicting with path: project_name"),
            Log.CRITICAL.value,
        )
    ],
    "inside_array": [
        (
            "Athena.js: Following paths are either array type or nested in array types: ['array_property.simple_property']",
            Log.CRITICAL.value,
        )
    ],
    "invalid_schema": [
        (
            "JSON schema validation failed : 'root' is a required property",
            Log.CRITICAL.value,
        )
    ],
    "valid_root_level_property_partition": [],
}


@pytest.mark.parametrize("test_dir,expected", dirs_to_expected.items())
def test_athena_check(test_dir, expected):
    ids_dir = UNIT_TEST_FILES / test_dir
    ids = ids_dir / "schema.json"
    athena = ids_dir / "athena.json"

    ids_schema = read_schema(ids)
    athena_schema = read_schema(athena)

    context = {"schema.json": ids_schema, "athena.json": athena_schema}

    athena_checker = AthenaChecker()
    node = Node(name="root", ids_dict=ids_schema, path="root")
    logs = athena_checker.run(node, context)

    assert sorted(logs) == sorted(expected)
