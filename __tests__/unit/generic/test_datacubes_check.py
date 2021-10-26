from pathlib import Path

import pytest

from src.checks.generic.datacubes import (
    DatacubesChecker,
    Message
)
from src.ids_node import Node
from src.utils import read_schema, Log


UNIT_TEST_FILES = Path("__tests__/unit/generic/files/datacubes")

files_to_failures = {
    "valid_datacubes.json": [],
    "missing_required_value.json": {(
        Message.REQUIRED_CHECK.value,
        Log.CRITICAL.value
    )},
    "required_undefined.json": {(
        Message.REQUIRED_CHECK.value,
        Log.CRITICAL.value
    )},
    "missing_required_property.json": {(
        Message.PROPERTY_CHECK.value,
        Log.CRITICAL.value
    )},
    "measure_min_max_mismatch.json": {
        (Message.MEASURE_MIN_MAX_CHECK.value, Log.CRITICAL.value),
        (Message.DIMENSIONS_MIN_MAX_CHECK.value, Log.CRITICAL.value)
    },
    "missing_min_max_items.json": [
        (Message.MEASURE_MIN_MAX_MISSING.value, Log.CRITICAL.value),
        (Message.DIMENSIONS_MIN_MAX_MISSING.value, Log.CRITICAL.value),
        (Message.MEASURES_VALUES_DIMENSIONALITY_ERROR.value, Log.CRITICAL.value)
    ],
    "measures_value_dimensionality_error.json": {(
        Message.MEASURES_VALUES_DIMENSIONALITY_ERROR.value,
        Log.CRITICAL.value
    )},

    # Checks if any nested "items" inside "measures.value" is Non-Array type
    # Except the inner most one
    "measures_values_invalid_items_type.json": [(
        Message.MEASURES_VALUES_NESTED_ARRAY_TYPE_ERROR.value,
        Log.CRITICAL.value
    )],
    "measures_values_invalid_data_type.json": [(
        Message.MEASURES_VALUES_TYPE_ERROR.value,
        Log.CRITICAL.value
    )],
    "dimensions_scale_invalid_type.json": [(
        Message.DIMENSIONS_SCALE_TYPE_ERROR.value,
        Log.CRITICAL.value
    )],
    "dimensions_scale_items_invalid_type.json": [(
        Message.DIMENSIONS_SCALE_ITEMS_TYPE_ERROR.value,
        Log.CRITICAL.value
    )],
    "dimensions_scale_items_valid_type_nullable_number.json":[]
}


@pytest.mark.parametrize("fname,expected", files_to_failures.items())
def test_datacubes_check(fname, expected, mocker):
    schema_path = UNIT_TEST_FILES / fname
    schema = read_schema(schema_path)

    datacubes = schema.get("datacubes")
    data_cubes_checker = DatacubesChecker()
    node = Node(name="datacubes", ids_dict=datacubes,
                path="root.properties.datacubes")

    logs = data_cubes_checker.run(node)
    assert sorted(logs) == sorted(list(expected))
