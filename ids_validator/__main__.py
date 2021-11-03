import argparse
from ids_validator.convention_versions import Conventions
from ids_validator.ids_validator import validate_ids


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Validate IDS Artifacts"
    )

    parser.add_argument("ids_dir", type=str, help="Path to the IDS folder")
    parser.add_argument("--version", type=str, required=False, default=None,
                        help=f"Supported Versions: {Conventions.values()}")
    args = parser.parse_args()
    validate_ids(args)