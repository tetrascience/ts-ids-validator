from pathlib import Path
from ids_validator.checks.generic import required_property

import pytest

from ids_validator.checks import RequiredPropertiesChecker
from ids_validator.ids_node import Node
from ids_validator.utils import read_schema, Log


UNIT_TEST_FILES = Path("__tests__/unit/generic/files/required_property")

fname_to_expected = {
    "required_property_not_defined.json": [(
        "Required Properties are missing: {'@idsType'}",
        Log.CRITICAL.value
    )],
}


@pytest.mark.parametrize("fname,expected", fname_to_expected.items())
def test_required_property_check(fname, expected):
    ids_file = UNIT_TEST_FILES / fname
    ids_schema = read_schema(ids_file)

    required_property_checker = RequiredPropertiesChecker()
    node = Node(name="root", ids_dict=ids_schema, path="root")
    logs = required_property_checker.run(node)

    assert logs == expected
