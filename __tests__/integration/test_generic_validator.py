from pathlib import Path

import pytest

from ids_validator.checks import checks_dict
from ids_validator.validator import Validator
from ids_validator.convention_versions import Conventions
from ids_validator.ids_node import Node
from ids_validator.utils import (
    read_schema,
    save_json
)

example_input = Path("__tests__/integration/example-input")
example_output = Path("__tests__/integration/example-output")


@pytest.mark.parametrize(
    "test_dir", [
        "generic_validator"
    ]
)
def test_generic_validators(test_dir, snapshot):

    ids_dir = example_input / test_dir
    ids = ids_dir / "schema.json"
    athena = ids_dir / "athena.json"

    ids_schema = read_schema(ids)
    athena_schema = read_schema(athena)

    generic_validator = Validator(
        ids=ids_schema,
        athena=athena_schema,
        convention_version=Conventions.GENERIC.value,
        checks_list=checks_dict[Conventions.GENERIC],
        ids_folder_path=ids_dir
    )
    generic_validator.validate_ids()
    logs = {
        k: v
        for k,v in generic_validator.property_failures.items()
        if v
    }

    out_path = example_output / test_dir / "failed_props.json"
    save_json(
        logs,
        out_path
    )

    snapshot.assert_match(logs)
    assert generic_validator.has_critical_failures
