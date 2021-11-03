import argparse
import sys

from ids_validator.convention_versions import Conventions
from ids_validator.ids_validator import validate_ids


def run() -> None:
    parser = argparse.ArgumentParser(
        description="Validate IDS Artifacts"
    )

    parser.add_argument("ids_dir", type=str, help="Path to the IDS folder")
    parser.add_argument("--version", type=str, required=False, default=None,
                        help=f"Supported Versions: {Conventions.values()}")
    cli_args = sys.argv[1:]
    parsed_args = parser.parse_args(cli_args)
    validate_ids(parsed_args)


if __name__ == '__main__':
    run()
