import pytest
from ids_validator.checks import AthenaChecker


test_cases = {
    'ABC': "abc",
    'Abc123': "abc123",
    'Abc_aBc': "abc_abc",
    'abC_123': "abc_123",
    '_abC_123_': "abc_123_",
    "_abc": "abc",
    "_+aBc": "abc",
    "___aBc": "abc",
    "abc__123": "abc_123",
    "abc___123": "abc_123",
    "abc___123__abc": "abc_123_abc",
    "@abc_123": "abc_123",
    "<>.,';|@abc_123": "abc_123",
    "abc@___\"123": "abc_123",
    "abc::[]{}@#$%^&*()-=+!123": "abc_123",
    "aBc_/_123_\\_abc": "abc_123_abc",
}


@pytest.mark.parametrize("input_,expected", test_cases.items())
def test_name_normalization(input_, expected):
    result = AthenaChecker.normalize_path_name(input_)
    assert result == expected
