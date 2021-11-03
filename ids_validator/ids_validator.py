import argparse
import sys
from pathlib import Path

from pydash import get

from ids_validator.utils import read_schema
from ids_validator.validator import Validator
from ids_validator.checks import checks_dict
from ids_validator.convention_versions import Conventions


def get_validator_type(version: str, ids: dict) -> Conventions:
    """Identify and return the type/version of validator to be used
    - If a supported versions is passed as CLI args, use it
    - If unsupported version is passed, exit validator
    - If no version is passed, try to read @idsConventionVersion from schema.json
    - If @idsConventionVersion is missing undefined, missing, or not supported,
    fallback to `generic` version.

    Args:
        version (str): version value passed as CLI argument
        ids (dict): python dict for schema.json

    Returns:
        Convention: Enum value for the convention version or generic type
    """
    if version is not None:
        result = Conventions.get_by_value(version)
        if result not in checks_dict:
            print(
                f"* Invalid Version passed. Supported Version: {Conventions.values()}")
            sys.exit(1)
        return result
    else:
        print(f"* Reading @idsConventionVersion from schema.json")
        convention = get(
            ids,
            "properties.@idsConventionVersion.const",
            None
        )
        if convention is None:
            print("* @idsConvention not specified in schema.json.")
            print("* Using Generic Validator")
            return Conventions.get_by_value("generic")

        if convention:
            convention_enum_value = Conventions.get_by_value(convention)

            if convention_enum_value is None:
                print(
                    f"* Invalid @idsConvention version ({convention}) specified in schema.json."
                )
                print("* Using Generic Validator")
                return Conventions.get_by_value("generic")

            if convention_enum_value in checks_dict:
                print(f"* Using {convention} validator")
                return convention_enum_value


def validate_ids(args):
    ids_dir = Path(args.ids_dir)
    version = args.version

    try:
        schema_file = ids_dir / "schema.json"
        athena_file = ids_dir / "athena.json"
        ids = read_schema(schema_file)
        athena = read_schema(athena_file)

        convention = get_validator_type(version, ids)
        checks_list = checks_dict.get(convention)

        validator = Validator(
            ids=ids,
            athena=athena,
            checks_list=checks_list,
            convention_version=convention.value,
            ids_folder_path=ids_dir
        )
        validator.validate_ids()
        if validator.has_critical_failures:
            validator.console.print(
                f"[b i red]\nValidation Failed with critical error.[/b i red]"
            )
            sys.exit(1)
        else:
            validator.console.print(
                f"[b i green]Validation Complete. No error found.[/b i green]"
            )
    except Exception as e:
        print(str(e))
        sys.exit(1)
