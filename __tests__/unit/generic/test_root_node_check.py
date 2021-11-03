from pathlib import Path

import pytest

from ids_validator.checks.generic import RootNodeChecker

from ids_validator.ids_node import Node
from ids_validator.utils import read_schema, Log


UNIT_TEST_FILES = Path("__tests__/unit/generic/files/root_node")

fname_to_expected = {
    "invalid_required_type.json": [
        (
            "'root.required' must be a list",
            Log.CRITICAL.value
        ),
        (
            "'required' must contain: @idsNamespace, @idsType, @idsVersion",
            Log.CRITICAL.value
        )
    ],
    "undefined_required.json": [
        (
            "'root.required' must be a list",
            Log.CRITICAL.value
        ),
        (
            "'required' must contain: @idsNamespace, @idsType, @idsVersion",
            Log.CRITICAL.value
        )
    ],
    "missing_required_value.json": [(
        "'required' must contain: @idsNamespace, @idsType, @idsVersion",
        Log.CRITICAL.value
    )],
    "invalid_meta_properties.json": [
        (
            "'properties.@idsType' must be present with type 'string' with non-empty 'const'",
            Log.CRITICAL.value
        ),
        (
            "'properties.@idsVersion' must be present with type 'string' with non-empty 'const'",
            Log.CRITICAL.value
        )
    ]
}


@pytest.mark.parametrize("fname,expected", fname_to_expected.items())
def test_root_node_check(fname, expected):
    ids_file = UNIT_TEST_FILES / fname
    ids_schema = read_schema(ids_file)

    root_node_checker = RootNodeChecker()

    node = Node(name="root", ids_dict=ids_schema, path="root")
    logs = root_node_checker.run(node)

    assert logs == expected
