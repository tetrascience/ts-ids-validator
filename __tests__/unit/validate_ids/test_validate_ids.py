from pathlib import Path

import pytest

from ids_validator.ids_validator import validate_ids

example_input = Path("__tests__/unit/validate_ids/files")


@pytest.mark.parametrize(
    "test_dir, expected",[
        ("invalid_ids", False),
        ("valid_ids", True),
    ]
)
def test_generic_validators(test_dir, expected):
    ids_dir = example_input / test_dir
    result = validate_ids(ids_dir)
    assert result == expected
