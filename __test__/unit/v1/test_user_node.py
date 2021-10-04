import pytest
from pathlib import Path

from src.ids_node import Node
from src.checks.v1 import V1UserNodeChecker
from src.validator import Validator
from src.utils import read_schema, Log


UNIT_TEST_FILES = Path("__test__/unit/v1/files/user_node")

files_to_expected = {
    "valid_user_node.json": {},
    "extra_prop_user_node copy.json": {},
    "invalid_types_user_node.json": {
        'root.properties.users': [("'type' must be array", Log.CRITICAL.value)],
        'root.properties.users.items': [("'type' must be object", Log.CRITICAL.value)],
        'root.properties.users.items.properties.name': [
            ("'type' must be ['string', 'null']", Log.CRITICAL.value)
        ]},
    "missing_property.json": {
        'root.properties.users': [("'properties' must contain ['type']", Log.CRITICAL.value)]
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
        checks_list=[V1UserNodeChecker()]
    )
    validator.validate_ids()
    logs = validator.property_failures
    users_logs = {
        k: v for k, v in logs.items()
        if "root.properties.users" in k and v
    }

    assert users_logs == expected
