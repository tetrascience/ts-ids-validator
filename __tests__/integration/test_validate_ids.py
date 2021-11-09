from pathlib import Path

import pytest

from ids_validator.ids_validator import validate_ids

example_input = Path("__tests__/integration/example-input")


@pytest.mark.parametrize(
    "test_dir, expected",[
        ("generic_validator", 1),
        ("valid_ids", 0),
    ]
)
def test_generic_validators(test_dir, expected):
    ids_dir = example_input / test_dir
    result = validate_ids(ids_dir)
    assert result == expected
