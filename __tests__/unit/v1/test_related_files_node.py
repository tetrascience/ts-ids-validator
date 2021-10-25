import pytest
from pathlib import Path
from src.utils import read_schema, Log
from src.checks.v1 import V1RelatedFilesChecker
from src.validator import Validator


UNIT_TEST_FILES = Path("__tests__/unit/v1/files/related_files")

files_to_expected = {
    "valid_related_files.json": {},
    "related_files_template_mismatch.json": {
        'root.properties.related_files': [(
            "'related_files' isn't an exact match of the template. Please refer to confluence docs.",
            Log.CRITICAL.value
        )]
    }
}


@pytest.mark.parametrize("fname,expected", files_to_expected.items())
def test_related_files_node(fname, expected):
    ids_file = UNIT_TEST_FILES / fname
    schema = read_schema(ids_file)
    validator = Validator(
        ids=schema,
        athena=None,
        convention_version=None,
        checks_list=[V1RelatedFilesChecker()],
    )
    validator.validate_ids()
    logs = validator.property_failures
    related_files_logs = {
        k: v for k, v in logs.items()
        if "root.properties.related_files" in k and v
    }

    assert related_files_logs == expected
