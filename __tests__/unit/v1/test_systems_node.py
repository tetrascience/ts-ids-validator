import pytest
from pathlib import Path
from src.ids_node import Node
from src.checks.v1 import V1SystemNodeChecker
from src.validator import Validator
from src.utils import read_schema, Log


from src.checks.v1.rules import systems


UNIT_TEST_FILES = Path("__tests__/unit/v1/files/systems_node")

files_to_expected = {
    "valid_systems_node.json": {},
    "extended_systems_node_root_and_nested.json": {},
    "missing_required_values.json": {
        systems.ITEMS: [(
            "'required' must contain {'model'}",
            Log.CRITICAL.value
        )],
        systems.FIRMWARE_ITEMS: [(
            "'required' must contain {'version'}",
            Log.CRITICAL.value
        )],
        systems.SOFTWARE_ITEMS: [(
            "'required' must contain {'name'}",
            Log.CRITICAL.value
        )]
    },
    "missing_properties.json": {
        systems.SYSTEMS: [(
            "'properties' must contain ['vendor']",
            Log.CRITICAL.value
        )],
        systems.FIRMWARE: [(
            "'properties' must contain ['name']",
            Log.CRITICAL.value
        )],
        systems.SOFTWARE: [(
            "'properties' must contain ['serial_number']",
            Log.CRITICAL.value
        )]
    },
    "wrong_types_exhaustive.json": {
        systems.SYSTEMS: [(
            "'type' must be array",
            Log.CRITICAL.value
        )],
        systems.ITEMS: [(
            "'type' must be object",
            Log.CRITICAL.value
        )],
        systems.ID: [(
            "'type' must be ['string', 'null']",
            Log.CRITICAL.value
        )],
        systems.NAME: [(
            "'type' must be ['string', 'null']",
            Log.CRITICAL.value
        )],
        systems.VENDOR: [(
            "'type' must be ['string', 'null']",
            Log.CRITICAL.value
        )],
        systems.MODEL: [(
            "'type' must be ['string', 'null']",
            Log.CRITICAL.value
        )],
        systems.TYPE: [(
            "'type' must be ['string', 'null']",
            Log.CRITICAL.value
        )],
        systems.SERIAL_NUMBER: [(
            "'type' must be ['string', 'null']",
            Log.CRITICAL.value)],
        systems.FIRMWARE: [(
            "'type' must be array",
            Log.CRITICAL.value
        )],
        systems.FIRMWARE_ITEMS: [(
            "'type' must be object",
            Log.CRITICAL.value)],
        systems.FIRMWARE_NAME: [(
            "'type' must be ['string', 'null']",
            Log.CRITICAL.value)],
        systems.FIRMWARE_VERSION: [(
            "'type' must be ['string', 'null']",
            Log.CRITICAL.value
        )],
        systems.FIRMWARE_LAST_UPDATE: [(
            "'type' must be ['string', 'null']",
            Log.CRITICAL.value
        )],
        systems.SOFTWARE: [(
            "'type' must be array",
            Log.CRITICAL.value
        )],
        systems.SOFTWARE_ITEMS: [(
            "'type' must be object",
            Log.CRITICAL.value
        )],
        systems.SOFTWARE_NAME: [(
            "'type' must be ['string', 'null']",
            Log.CRITICAL.value
        )],
        systems.SOFTWARE_VERSION: [(
            "'type' must be ['string', 'null']",
            Log.CRITICAL.value
        )],
        systems.SOFTWARE_LAST_UPDATE: [(
            "'type' must be ['string', 'null']",
            Log.CRITICAL.value
        )]
    },
    "incomplete_system_node.json": {
        systems.SYSTEMS: [(
            "'properties' must contain ['model', 'type', 'vendor']", Log.CRITICAL.value
        )]
    }

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
        ids_folder_path=None
    )
    validator.validate_ids()
    logs = validator.property_failures
    systems.logs = {
        k: v for k, v in logs.items()
        if "root.properties.systems" in k and v
    }

    assert systems.logs == expected
