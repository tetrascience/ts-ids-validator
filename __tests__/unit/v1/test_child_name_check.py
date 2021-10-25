from pathlib import Path

import pytest

from src.checks.v1 import V1ChildNameChecker

from src.ids_node import Node
from src.utils import read_schema, Log


UNIT_TEST_FILES = Path("__tests__/unit/v1/files/child_name_check")

fname_to_expected = {
    "valid_child_naming.json": [],
    "child_name_starts_with_parent_name.json": [(
        "Child property prefix uses the same name as the parent property 'project'",
        Log.WARNING.value
    )]
}


@pytest.mark.parametrize("fname,expected", fname_to_expected.items())
def test_type_check(fname, expected):
    ids_file = UNIT_TEST_FILES / fname
    ids_schema = read_schema(ids_file)

    child_name_checker = V1ChildNameChecker()

    node = Node(name="project",
                ids_dict=ids_schema["project"], path="root.project")
    logs = child_name_checker.run(node)

    assert logs == expected
