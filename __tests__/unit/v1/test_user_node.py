import pytest
from pathlib import Path

from ids_validator.checks.v1 import V1UserNodeChecker
from ids_validator.validator import Validator
from ids_validator.utils import read_schema, Log
from ids_validator.checks.v1.rules import users

UNIT_TEST_FILES = Path("__tests__/unit/v1/files/user_node")

files_to_expected = {
    "valid_user_node.json": {},
    "extra_prop_user_node.json": {},
    "invalid_types_user_node.json": {
        users.USERS: [(
            "'type' must be array",
            Log.CRITICAL.value
        )],
        users.ITEMS: [(
            "'type' must be object",
            Log.CRITICAL.value
        )],
        users.NAME: [(
            "'type' must be ['string', 'null']",
            Log.CRITICAL.value
        )]
    },
    "missing_property.json": {
        users.USERS: [(
            "'properties' must contain ['type']",
            Log.CRITICAL.value
        )]
    },
}

@pytest.mark.parametrize("fname,expected", files_to_expected.items())
def test_user_node(fname, expected):
    ids_file = UNIT_TEST_FILES / fname
    schema = read_schema(ids_file)
    validator = Validator(
        ids=schema,
        athena=None,
        convention_version=None,
        checks_list=[V1UserNodeChecker()],
        ids_folder_path=None
    )
    validator.validate_ids()
    logs = validator.property_failures
    users_logs = {
        k: v for k, v in logs.items()
        if "root.properties.users" in k and v
    }

    assert users_logs == expected
