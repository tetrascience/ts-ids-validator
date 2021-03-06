import pytest
from pathlib import Path
from ids_validator.ids_node import Node
from ids_validator.checks.v1 import V1SystemNodeChecker
from ids_validator.validator import Validator
from ids_validator.utils import read_schema, Log


from ids_validator.checks.v1.rules import systems


UNIT_TEST_FILES = Path("__tests__/unit/v1/files/systems_node")

files_to_expected = {
    "valid_systems_node.json": {},
    "valid_systems_node_const_types.json": {},
    "extended_systems_node_root_and_nested.json": {},
    "invalid_systems_node_const_types.json": {
        systems.VENDOR: [
            (
                "'type' must be one of ['number', 'string', 'boolean', 'integer'] when 'const' is defined",
                Log.CRITICAL.value,
            )
        ]
    },
    "missing_required_values.json": {
        systems.ITEMS: [("'required' must contain {'model'}", Log.CRITICAL.value)],
        systems.FIRMWARE_ITEMS: [
            ("'required' must contain {'version'}", Log.CRITICAL.value)
        ],
        systems.SOFTWARE_ITEMS: [
            ("'required' must contain {'name'}", Log.CRITICAL.value)
        ],
    },
    "missing_properties.json": {
        systems.SYSTEMS: [("'properties' must contain ['vendor']", Log.CRITICAL.value)],
        systems.FIRMWARE: [("'properties' must contain ['name']", Log.CRITICAL.value)],
    },
    "wrong_types_exhaustive.json": {
        systems.SYSTEMS: [("'type' must be array", Log.CRITICAL.value)],
        systems.ITEMS: [("'type' must be object", Log.CRITICAL.value)],
        systems.ID: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        systems.NAME: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        systems.VENDOR: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        systems.MODEL: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        systems.TYPE: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        systems.SERIAL_NUMBER: [
            ("'type' must be ['string', 'null']", Log.CRITICAL.value)
        ],
        systems.FIRMWARE: [("'type' must be array", Log.CRITICAL.value)],
        systems.FIRMWARE_ITEMS: [("'type' must be object", Log.CRITICAL.value)],
        systems.FIRMWARE_NAME: [
            ("'type' must be ['string', 'null']", Log.CRITICAL.value)
        ],
        systems.FIRMWARE_VERSION: [
            ("'type' must be ['string', 'null']", Log.CRITICAL.value)
        ],
        systems.FIRMWARE_LAST_UPDATE: [
            ("'type' must be ['string', 'null']", Log.CRITICAL.value)
        ],
        systems.SOFTWARE: [("'type' must be array", Log.CRITICAL.value)],
        systems.SOFTWARE_ITEMS: [("'type' must be object", Log.CRITICAL.value)],
        systems.SOFTWARE_NAME: [
            ("'type' must be ['string', 'null']", Log.CRITICAL.value)
        ],
        systems.SOFTWARE_VERSION: [
            ("'type' must be ['null', 'string']", Log.CRITICAL.value)
        ],
        systems.SOFTWARE_LAST_UPDATE: [
            ("'type' must be ['string', 'null']", Log.CRITICAL.value)
        ],
    },
    "incomplete_system_node.json": {
        systems.SYSTEMS: [
            (
                "'properties' must contain ['model', 'type', 'vendor']",
                Log.CRITICAL.value,
            )
        ]
    },
}


@pytest.mark.parametrize("fname,expected", files_to_expected.items())
def test_systems_node(fname, expected):
    ids_file = UNIT_TEST_FILES / fname
    schema = read_schema(ids_file)
    validator = Validator(
        ids=schema,
        athena=None,
        convention_version=None,
        checks_list=[V1SystemNodeChecker()],
        ids_folder_path=None,
    )
    validator.validate_ids()
    logs = validator.property_failures
    systems_logs = {
        k: v for k, v in logs.items() if "root.properties.systems" in k and v
    }

    assert systems_logs == expected
