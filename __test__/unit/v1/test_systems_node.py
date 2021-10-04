import pytest
from pathlib import Path
from src.ids_node import Node
from src.checks.v1 import V1SystemNodeChecker
from src.validator import Validator
from src.utils import read_schema, Log


from src.checks.v1.rules.systems import *


UNIT_TEST_FILES = Path("__test__/unit/v1/files/systems_node")

files_to_expected = {
    "valid_systems_node.json": {},
    "extended_systems_node_root_and_nested.json": {},
    "missing_required_values.json": {
        SYSTEMS_ITEMS: [("'required' must contain {'model'}", Log.CRITICAL.value)],
        SYSTEMS_FIRMWARE_ITEMS: [("'required' must contain {'version'}", Log.CRITICAL.value)],
        SYSTEMS_SOFTWARE_ITEMS: [("'required' must contain {'name'}", Log.CRITICAL.value)]
    },
    "missing_properties.json": {
        SYSTEMS: [("'properties' must contain ['vendor']", Log.CRITICAL.value)],
        SYSTEMS_FIRMWARE: [("'properties' must contain ['name']", Log.CRITICAL.value)],
        SYSTEMS_SOFTWARE: [
            ("'properties' must contain ['serial_number']", Log.CRITICAL.value)]
    },
    "wrong_types_exhaustive.json": {
        SYSTEMS: [("'type' must be array", Log.CRITICAL.value)],
        SYSTEMS_ITEMS: [("'type' must be object", Log.CRITICAL.value)],
        SYSTEMS_ID: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        SYSTEMS_NAME: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        SYSTEMS_VENDOR: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        SYSTEMS_MODEL: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        SYSTEMS_TYPE: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        SYSTEMS_SERIAL_NUMBER: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        SYSTEMS_FIRMWARE: [("'type' must be array", Log.CRITICAL.value)],
        SYSTEMS_FIRMWARE_ITEMS: [("'type' must be object", Log.CRITICAL.value)],
        SYSTEMS_FIRMWARE_NAME: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        SYSTEMS_FIRMWARE_VERSION: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        SYSTEMS_FIRMWARE_LAST_UPDATE: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        SYSTEMS_SOFTWARE: [("'type' must be array", Log.CRITICAL.value)],
        SYSTEMS_SOFTWARE_ITEMS: [("'type' must be object", Log.CRITICAL.value)],
        SYSTEMS_SOFTWARE_NAME: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        SYSTEMS_SOFTWARE_VERSION: [("'type' must be ['string', 'null']", Log.CRITICAL.value)],
        SYSTEMS_SOFTWARE_LAST_UPDATE: [
            ("'type' must be ['string', 'null']", Log.CRITICAL.value)]
    },
    "incomplete_system_node.json": {
        SYSTEMS: [("'properties' must contain ['firmware', 'id', 'model', 'name', 'serial_number', 'software', 'type', 'vendor']", Log.CRITICAL.value)]}

}


@pytest.mark.parametrize("fname,expected", files_to_expected.items())
def test_systems_node(fname, expected):
    ids_file = UNIT_TEST_FILES / fname
    schema = read_schema(ids_file)
    validator = Validator(
        ids=schema,
        athena=None,
        convention_version=None,
        checks_list=[V1SystemNodeChecker()]
    )
    validator.validate_ids()
    logs = validator.property_failures
    systems_logs = {
        k: v for k, v in logs.items()
        if "root.properties.systems" in k and v
    }

    assert systems_logs == expected
