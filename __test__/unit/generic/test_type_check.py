from pathlib import Path

import pytest

from src.checks.generic import TypeChecker

from src.ids_node import Node
from src.utils import read_schema, Log


UNIT_TEST_FILES = Path("__test__/unit/generic/files/type_check")

fname_to_expected = {
    "invalid_array_type_no_items.json": [
        ("'array' type must contain items.properties", Log.CRITICAL.value)
    ],
    "invalid_array_type_no_properties.json": [
        ("'array' type must contain items.properties", Log.CRITICAL.value)
    ],
    "invalid_list_type.json": [("Invalid 'type': ['invalid_type1', 'invalid_type2']", Log.CRITICAL.value)],
    "invalid_list_type_all_null.json": [("Invalid 'type': ['null', 'null']", Log.CRITICAL.value)],
    "invalid_list_type_all_same.json": [("Invalid 'type': ['string', 'string']", Log.CRITICAL.value)],
    "invalid_object_type_no_properties.json": [('object Type must contain properties', Log.CRITICAL.value)],
    "invalid_data_type.json": [("Invalid 'type': any_random_type", Log.CRITICAL.value)],
    "invalid_list_type_length.json": [("Invalid 'type': ['string', 'number', 'null']", Log.CRITICAL.value)],
    "valid_list_type.json": [],
    "valid_array_type.json": [],
    "valid_object_type.json": [],
}


@pytest.mark.parametrize("fname,expected", fname_to_expected.items())
def test_type_check(fname, expected):
    ids_file = UNIT_TEST_FILES / fname
    ids_schema = read_schema(ids_file)

    type_checker = TypeChecker()

    node = Node(name="root", ids_dict=ids_schema, path="root")
    logs = type_checker.run(node)

    assert logs == expected
