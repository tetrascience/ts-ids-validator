import argparse
from pathlib import Path
import sys

from src.utils import read_schema
from src.validator import Validator
from src.checks import checks_dict
from src.convention_versions import Conventions

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Validate schema.json"
    )

    parser.add_argument("ids_dir", type=str, help="Path to the IDS folder")
    parser.add_argument("version", type=str, help=f"Conventions Version. Supported: {Conventions.values()}")
    args = parser.parse_args()
    ids_dir = Path(args.ids_dir)
    version = args.version

    convention = Conventions.get_by_value(version)
    if not convention:
        print("Invalid Convention Version")
        sys.exit(1)

    try:
        checks_list = checks_dict[convention]

        schema_file = ids_dir / "schema.json"
        athena_file = ids_dir / "athena.json"
        ids = read_schema(schema_file)
        athena = read_schema(athena_file)

        validator = Validator(
            ids=ids,
            athena=athena,
            checks_list=checks_list,
            convention_version=convention.value
        )
        validator.validate_ids()
        if validator.has_critical_failures:
            print("Validation Failed with critical failures.")
            sys.exit(1)
    except Exception as e:
        print(str(e))
        sys.exit(1)
