from pathlib import Path

import pytest
from ids_validator.checks.v1 import V1SampleNodeChecker
from ids_validator.checks.v1.rules.samples import sample_properties as properties
from ids_validator.checks.v1.rules.samples import samples_labels as labels
from ids_validator.checks.v1.rules.samples import samples_location as location
from ids_validator.checks.v1.rules.samples import samples_root as samples
from ids_validator.utils import Log, read_schema
from ids_validator.validator import Validator

UNIT_TEST_FILES = Path("__tests__/unit/v1/files/samples_node")

files_to_expected = {
    "valid_samples_node.json": {},
    "valid_samples_node_with_source_type_warning.json": {
        labels.SOURCE_NAME: [
            (
                "'type' 'string' is deprecated but allowed for backward compatibility, "
                "please use `['string', 'null']` instead.",
                Log.WARNING,
            )
        ]
    },
    "extended_samples_root.json": {
        samples.ITEMS: [
            (
                "'properties' must only contain ['barcode', 'batch', 'id', "
                "'labels', 'location', 'lot', 'name', 'properties', 'set']. "
                "Extra properties found: {'extra_node'}",
                Log.CRITICAL.value,
            )
        ]
    },
    "missing_samples_node_root_property.json": {
        samples.ITEMS: [
            (
                (
                    "'properties' must only contain ['barcode', 'batch', 'id', "
                    "'labels', 'location', 'lot', 'name', 'properties', 'set']. "
                    "Missing properties: {'set'}"
                ),
                Log.CRITICAL.value,
            )
        ]
    },
    "both_missing_and_extra_property.json": {
        samples.ITEMS: [
            (
                "'properties' must only contain "
                "['barcode', 'batch', 'id', 'labels', "
                "'location', 'lot', 'name', 'properties', "
                "'set']. Extra properties found: "
                "{'extra_property'}",
                Log.CRITICAL.value,
            ),
            (
                "'properties' must only contain "
                "['barcode', 'batch', 'id', 'labels', "
                "'location', 'lot', 'name', 'properties', "
                "'set']. Missing properties: {'barcode'}",
                Log.CRITICAL.value,
            ),
        ]
    },
    "extended_nested_properties.json": {},  # Nested properties are extensible
    "missing_nested_essential_properties.json": {
        samples.BATCH: [("'properties' must contain ['name']", Log.CRITICAL.value)],
        labels.LABELS: [("'properties' must contain ['name']", Log.CRITICAL.value)],
        labels.SOURCE: [("'properties' must contain ['name']", Log.CRITICAL.value)],
        labels.TIME: [("'properties' must contain ['lookup']", Log.CRITICAL.value)],
        location.LOCATION: [
            ("'properties' must contain ['column']", Log.CRITICAL.value)
        ],
        location.HOLDER: [("'properties' must contain ['type']", Log.CRITICAL.value)],
        samples.LOT: [("'properties' must contain ['name']", Log.CRITICAL.value)],
        properties.PROPERTIES: [
            ("'properties' must contain ['string_value']", Log.CRITICAL.value)
        ],
        properties.SOURCE: [("'properties' must contain ['name']", Log.CRITICAL.value)],
        properties.TIME: [("'properties' must contain ['lookup']", Log.CRITICAL.value)],
        samples.SET: [("'properties' must contain ['id']", Log.CRITICAL.value)],
    },
    "invalid_types_samples_root.json": {
        samples.SAMPLES: [("'type' must be array", Log.CRITICAL.value)],
        samples.ITEMS: [("'type' must be object", Log.CRITICAL.value)],
        samples.ID: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        samples.BARCODE: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        samples.NAME: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        samples.BATCH: [("'type' must be object", Log.CRITICAL.value)],
        samples.BATCH_ID: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        samples.BATCH_NAME: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        samples.BATCH_BARCODE: [
            ("'type' must be ['string', 'null']", Log.CRITICAL.value)
        ],
        samples.SET: [("'type' must be object", Log.CRITICAL.value)],
        samples.SET_ID: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        samples.SET_NAME: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        samples.LOT: [("'type' must be object", Log.CRITICAL.value)],
        samples.LOT_ID: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        samples.LOT_NAME: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        samples.LOCATION: [("'type' must be object", Log.CRITICAL.value)],
        samples.PROPERTIES: [("'type' must be array", Log.CRITICAL.value)],
        samples.LABELS: [("'type' must be array", Log.CRITICAL.value)],
    },
    "invalid_types_samples_location.json": {
        location.LOCATION: [("'type' must be object", Log.CRITICAL.value)],
        location.POSITION: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        location.ROW: [("'type' must be ['number', 'null']", Log.CRITICAL.value)],
        location.COLUMN: [("'type' must be ['number', 'null']", Log.CRITICAL.value)],
        location.HOLDER: [("'type' must be object", Log.CRITICAL.value)],
        location.HOLDER_NAME: [
            ("'type' must be ['string', 'null']", Log.CRITICAL.value)
        ],
        location.HOLDER_TYPE: [
            ("'type' must be ['string', 'null']", Log.CRITICAL.value)
        ],
        location.HOLDER_BARCODE: [
            ("'type' must be ['string', 'null']", Log.CRITICAL.value)
        ],
    },
    "invalid_types_samples_properties.json": {
        properties.PROPERTIES: [("'type' must be array", Log.CRITICAL.value)],
        properties.ITEMS: [("'type' must be object", Log.CRITICAL.value)],
        properties.SOURCE: [("'type' must be object", Log.CRITICAL.value)],
        properties.SOURCE_NAME: [
            ("'type' must be ['string', 'null']", Log.CRITICAL.value)
        ],
        properties.SOURCE_TYPE: [
            ("'type' must be ['string', 'null']", Log.CRITICAL.value)
        ],
        properties.NAME: [("'type' must be string", Log.CRITICAL.value)],
        properties.VALUE: [("'type' must be string", Log.CRITICAL.value)],
        properties.VALUE_DATA_TYPE: [("'type' must be string", Log.CRITICAL.value)],
        properties.STRING_VALUE: [
            ("'type' must be ['string', 'null']", Log.CRITICAL.value)
        ],
        properties.NUMERICAL_VALUE: [
            ("'type' must be ['number', 'null']", Log.CRITICAL.value)
        ],
        properties.NUMERICAL_VALUE_UNIT: [
            ("'type' must be ['string', 'null']", Log.CRITICAL.value)
        ],
        properties.BOOLEAN_VALUE: [
            ("'type' must be ['boolean', 'null']", Log.CRITICAL.value)
        ],
        properties.TIME: [("'type' must be object", Log.CRITICAL.value)],
        properties.TIME_LOOKUP: [
            ("'type' must be ['string', 'null']", Log.CRITICAL.value)
        ],
    },
    "invalid_types_samples_labels.json": {
        labels.LABELS: [("'type' must be array", Log.CRITICAL.value)],
        labels.ITEMS: [("'type' must be object", Log.CRITICAL.value)],
        labels.SOURCE: [("'type' must be object", Log.CRITICAL.value)],
        labels.SOURCE_NAME: [
            (
                "'type' must be ['string', 'null'], or one of these deprecated "
                "types: ('string',)",
                Log.CRITICAL,
            )
        ],
        labels.SOURCE_TYPE: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        labels.NAME: [("'type' must be string", Log.CRITICAL.value)],
        labels.VALUE: [("'type' must be string", Log.CRITICAL.value)],
        labels.TIME: [("'type' must be object", Log.CRITICAL.value)],
        labels.TIME_LOOKUP: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
    },
}


@pytest.mark.parametrize("fname,expected", files_to_expected.items())
def test_samples_node(fname, expected):
    """Test that the samples node checker creates the expected logs from valid and
    invalid samples schemas
    """
    ids_file = UNIT_TEST_FILES / fname
    schema = read_schema(ids_file)
    validator = Validator(
        ids=schema,
        athena=None,
        convention_version=None,
        checks_list=[V1SampleNodeChecker()],
        ids_folder_path=None,
    )
    validator.validate_ids()
    logs = validator.property_failures
    samples_logs = {
        k: v for k, v in logs.items() if "root.properties.samples" in k and v
    }

    assert samples_logs == expected
