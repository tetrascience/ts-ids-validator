import argparse
from pathlib import Path
import sys
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
    ids_dir = Path(args.ids_dir)

    try:
        result = validate_ids(ids_dir, args.version)
    except Exception as e:
        print(str(e))
        sys.exit(1)

    sys.exit(result)
