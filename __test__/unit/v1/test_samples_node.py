import pytest
from pathlib import Path
from src.ids_node import Node
from src.utils import read_schema, Log
from src.checks.v1 import V1SampleNodeChecker
from src.validator import Validator

from src.checks.v1.rules.samples.samples_root import *
from src.checks.v1.rules.samples.sample_properties import *
from src.checks.v1.rules.samples.samples_labels import *
from src.checks.v1.rules.samples.samples_locations import *

UNIT_TEST_FILES = Path("__test__/unit/v1/files/samples_node")

files_to_expected = {
    "valid_samples_node.json": {},
    "extended_samples_root.json": {
        SAMPLES_ITEMS: [("'properties' must only contain ['id', "
                         "'barcode', 'name', 'batch', 'set', 'lot', "
                         "'location', 'properties', 'labels']",
                         Log.CRITICAL.value)]
    },
    "missing_samples_node_root_property.json": {
        SAMPLES_ITEMS: [("'properties' must only contain ['id', "
                         "'barcode', 'name', 'batch', 'set', 'lot', "
                         "'location', 'properties', 'labels']",
                         Log.CRITICAL.value)]
    },
    "extended_nested_properties.json": {},  # Nested properties are extensible
    "missing_nested_essential_properties.json": {
        SAMPLES_BATCH: [("'properties' must contain ['name']", Log.CRITICAL.value)],
        LABELS: [("'properties' must contain ['name']", Log.CRITICAL.value)],
        LABELS_SOURCE: [("'properties' must contain ['name']", Log.CRITICAL.value)],
        LABELS_TIME: [("'properties' must contain ['lookup']", Log.CRITICAL.value)],
        LOCATION: [("'properties' must contain ['column']", Log.CRITICAL.value)],
        LOCATION_HOLDER: [("'properties' must contain ['type']", Log.CRITICAL.value)],
        SAMPLES_LOT: [("'properties' must contain ['name']", Log.CRITICAL.value)],
        PROPERTIES: [("'properties' must contain ['string_value']", Log.CRITICAL.value)],
        PROPERTIES_SOURCE: [("'properties' must contain ['name']", Log.CRITICAL.value)],
        PROPERTIES_TIME: [("'properties' must contain ['lookup']", Log.CRITICAL.value)],
        SAMPLES_SET: [("'properties' must contain ['id']", Log.CRITICAL.value)],
    },
    "invalid_types_samples_root.json": {
        SAMPLES: [("'type' must be array", Log.CRITICAL.value)],
        SAMPLES_ITEMS: [("'type' must be object", Log.CRITICAL.value)],
        SAMPLES_ID: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        SAMPLES_BARCODE: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        SAMPLES_NAME: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        SAMPLES_BATCH: [("'type' must be object", Log.CRITICAL.value)],
        SAMPLES_BATCH_ID: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        SAMPLES_BATCH_NAME: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        SAMPLES_BATCH_BARCODE: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        SAMPLES_SET: [("'type' must be object", Log.CRITICAL.value)],
        SAMPLES_SET_ID: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        SAMPLES_SET_NAME: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        SAMPLES_LOT: [("'type' must be object", Log.CRITICAL.value)],
        SAMPLES_LOT_ID: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        SAMPLES_LOT_NAME: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        SAMPLES_LOCATION: [("'type' must be object", Log.CRITICAL.value)],
        SAMPLES_PROPERTIES: [("'type' must be array", Log.CRITICAL.value)],
        SAMPLES_LABELS: [("'type' must be array", Log.CRITICAL.value)]
    },
    "invalid_types_samples_location.json": {
        LOCATION: [("'type' must be object", Log.CRITICAL.value)],
        LOCATION_POSITION: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        LOCATION_ROW: [("'type' must be ['number', 'null']", Log.CRITICAL.value)],
        LOCATION_COLUMN: [("'type' must be ['number', 'null']", Log.CRITICAL.value)],
        LOCATION_HOLDER: [("'type' must be object", Log.CRITICAL.value)],
        LOCATION_HOLDER_NAME: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        LOCATION_HOLDER_TYPE: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        LOCATION_HOLDER_BARCODE: [("'type' must be ['string', 'null']", Log.CRITICAL.value)]
    },
    "invalid_types_samples_properties.json": {
        PROPERTIES: [("'type' must be array", Log.CRITICAL.value)],
        PROPERTIES_ITEMS: [("'type' must be object", Log.CRITICAL.value)],
        PROPERTIES_SOURCE: [("'type' must be object", Log.CRITICAL.value)],
        PROPERTIES_SOURCE_NAME: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        PROPERTIES_SOURCE_TYPE: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        PROPERTIES_NAME: [("'type' must be string", Log.CRITICAL.value)],
        PROPERTIES_VALUE: [("'type' must be string", Log.CRITICAL.value)],
        PROPERTIES_VALUE_DATA_TYPE: [("'type' must be string", Log.CRITICAL.value)],
        PROPERTIES_STRING_VALUE: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        PROPERTIES_NUMERICAL_VALUE: [("'type' must be ['number', 'null']", Log.CRITICAL.value)],
        PROPERTIES_NUMERICAL_VALUE_UNIT: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        PROPERTIES_BOOLEAN_VALUE: [("'type' must be ['boolean', 'null']", Log.CRITICAL.value)],
        PROPERTIES_TIME: [("'type' must be object", Log.CRITICAL.value)],
        PROPERTIES_TIME_LOOKUP: [("'type' must be ['string', 'null']", Log.CRITICAL.value)]
    },
    "invalid_types_samples_labels.json": {
        LABELS: [("'type' must be array", Log.CRITICAL.value)],
        LABELS_ITEMS: [("'type' must be object", Log.CRITICAL.value)],
        LABELS_SOURCE: [("'type' must be object", Log.CRITICAL.value)],
        LABELS_SOURCE_NAME: [("'type' must be string", Log.CRITICAL.value)],
        LABELS_SOURCE_TYPE: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        LABELS_NAME: [("'type' must be string", Log.CRITICAL.value)],
        LABELS_VALUE: [("'type' must be string", Log.CRITICAL.value)],
        LABELS_TIME: [("'type' must be object", Log.CRITICAL.value)],
        LABELS_TIME_LOOKUP: [("'type' must be ['string', 'null']", Log.CRITICAL.value)]
    }
}


@pytest.mark.parametrize("fname,expected", files_to_expected.items())
def test_samples_node(fname, expected):
    ids_file = UNIT_TEST_FILES / fname
    schema = read_schema(ids_file)
    validator = Validator(
        ids=schema,
        athena=None,
        convention_version=None,
        checks_list=[V1SampleNodeChecker()]
    )
    validator.validate_ids()
    logs = validator.property_failures
    samples_logs = {
        k: v for k, v in logs.items()
        if "root.properties.samples" in k and v
    }

    assert samples_logs == expected
