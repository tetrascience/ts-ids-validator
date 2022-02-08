from pathlib import Path

import pytest

from ids_validator.checks.v1 import V1SnakeCaseChecker

from ids_validator.ids_node import Node
from ids_validator.utils import read_schema, Log


UNIT_TEST_FILES = Path("__tests__/unit/v1/files/child_name_check")

node_name_to_expected = {
    "1": [],
    "CamelCase": [("'CamelCase' should be named as snake_case.", Log.CRITICAL.value)],
    "_underscore_prefix": [],
    "underscore_suffix_": [],
    "invalid.special.char": [
        ("'invalid.special.char' should be named as snake_case.", Log.CRITICAL.value)
    ],
    "@idsConventionVersion": [],
    "snake_case_1": [],
    "1_snake_case": [],
    "not_snake@case": [
        ("'not_snake@case' should be named as snake_case.", Log.CRITICAL.value)
    ],
    "snake1_case": [],
}


@pytest.mark.parametrize("node_name, expected", node_name_to_expected.items())
def test_snake_case_check(node_name, expected):
    snake_case_checker = V1SnakeCaseChecker()
    node = Node(name=node_name, ids_dict={}, path=f"root.{node_name}")
    logs = snake_case_checker.run(node)

    assert logs == expected


@pytest.mark.parametrize("node_name, expected", node_name_to_expected.items())
def test_ignore_snake_case_check_for_definitions(node_name, expected):
    snake_case_checker = V1SnakeCaseChecker()
    node = Node(name=node_name, ids_dict={}, path=f"root.definitions.{node_name}")
    logs = snake_case_checker.run(node)
    assert logs == []
