from pathlib import Path

import pytest

from src.checks import AdditionalPropertyChecker
from src.ids_node import Node
from src.utils import read_schema, Log


UNIT_TEST_FILES = Path("__tests__/unit/generic/files") / "additional_property"

fname_to_expected = {
    "additional_property_true.json": [(
        "'additionalProperties' must be present and set to 'false' for 'object' types",
        Log.CRITICAL.value
    )],
    "additional_property_type_conflict.json": [(
        "'additionalProperties' can only be defined for 'type = object'",
        Log.CRITICAL.value
    )],
    "additional_property_is_null.json": [(
        "'additionalProperties' must be present and set to 'false' for 'object' types",
        Log.CRITICAL.value)],
    "additional_property_is_0.json": [(
        "'additionalProperties' must be present and set to 'false' for 'object' types",
        Log.CRITICAL.value
    )
    ],
    "additional_property_not_defined_for_object_type.json": [(
        "'additionalProperties' must be present and set to 'false' for 'object' types",
        Log.CRITICAL.value
    )],
    "additional_property_is_defined_but_no_type.json": [(
        "'additionalProperties' can only be defined for 'type = object'",
        Log.CRITICAL.value
    )],
}


@pytest.mark.parametrize("fname,expected", fname_to_expected.items())
def test_additional_property_check(fname, expected):
    ids_file = UNIT_TEST_FILES / fname
    ids_schema = read_schema(ids_file)

    node = Node(name="root", ids_dict=ids_schema, path="root")
    additional_property_check = AdditionalPropertyChecker()

    logs = additional_property_check.run(node)
    assert sorted(logs) == sorted(expected)
