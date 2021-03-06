from pathlib import Path

import pytest

from ids_validator.checks.generic import TypeChecker

from ids_validator.ids_node import Node
from ids_validator.utils import read_schema, Log


UNIT_TEST_FILES = Path("__tests__/unit/generic/files/type_check")

fname_to_expected = {
    "invalid_array_type_no_items.json": [
        ("'array' type must contain 'items: dict'", Log.CRITICAL.value)
    ],
    "invalid_array_type_no_items_type.json": [
        ("'array' type must contain items.type", Log.CRITICAL.value)
    ],
    "invalid_array_type_no_items_not_dict.json": [
        ("'array' type must contain 'items: dict'", Log.CRITICAL.value)
    ],
    "invalid_list_type.json": [
        ("Invalid 'type': ['invalid_type1', 'invalid_type2']", Log.CRITICAL.value)
    ],
    "invalid_list_type_all_null.json": [
        ("Invalid 'type': ['null', 'null']", Log.CRITICAL.value)
    ],
    "invalid_list_type_all_same.json": [
        ("Invalid 'type': ['string', 'string']", Log.CRITICAL.value)
    ],
    "invalid_object_type_no_properties.json": [
        ("'object' type must  contains non-empty 'properties'", Log.CRITICAL.value)
    ],
    "invalid_data_type.json": [("Invalid 'type': any_random_type", Log.CRITICAL.value)],
    "invalid_type_list_of_length_more_than_two.json": [
        ("Invalid 'type': ['string', 'number', 'null']", Log.CRITICAL.value)
    ],
    "invalid_list_no_null.json": [
        ("Invalid 'type': ['string', 'number']", Log.CRITICAL.value)
    ],
    "invalid_list_with_only_null_type.json": [
        ("Invalid 'type': ['null']", Log.CRITICAL.value)
    ],
    "invalid_type_with_const.json": [
        (
            "'type' must be one of ['number', 'string', 'boolean', 'integer'] when 'const' is defined",
            Log.CRITICAL.value,
        )
    ],
    "invalid_missing_type.json": [
        (
            "'root.alpha' has no 'type' defined. This could be caused by a missing 'type', or a typo in a 'type' or '$ref' keyword.",
            Log.CRITICAL,
        ),
        (
            "'root.beta' has no 'type' defined. This could be caused by a missing 'type', or a typo in a 'type' or '$ref' keyword.",
            Log.CRITICAL,
        ),
    ],
    "invalid_missing_type_due_to_typo.json": [
        (
            "'root.alpha' has no 'type' defined. This could be caused by a missing 'type', or a typo in a 'type' or '$ref' keyword.",
            Log.CRITICAL,
        ),
        (
            "'root.beta' has no 'type' defined. This could be caused by a missing 'type', or a typo in a 'type' or '$ref' keyword.",
            Log.CRITICAL,
        ),
    ],
    "valid_type_with_const.json": [],
    "valid_list_type.json": [],
    "valid_array_type.json": [],
    "valid_object_type.json": [],
    "valid_single_data_type_in_list.json": [],
    "valid_array_type_with_nullable_items_type.json": [],
}


@pytest.mark.parametrize("fname,expected", fname_to_expected.items())
def test_type_check(fname, expected):
    ids_file = UNIT_TEST_FILES / fname
    ids_schema = read_schema(ids_file)

    type_checker = TypeChecker()

    node = Node(name="root", ids_dict=ids_schema, path="root")
    logs = type_checker.run(node)

    assert logs == expected
