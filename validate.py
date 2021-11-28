#!/usr/bin/env python3
#
# Install dependencies before running this script:
#  python3 -m pip install -U -r requirements.txt
#
import json
import jsonschema
from jsonschema import Draft202012Validator, validators
from enum import Enum, auto
from pathlib import Path
import toml
import yaml
import argparse

schema_file = "lwc.schema.json"

parser = argparse.ArgumentParser(description='Validate LWC design files.')
parser.add_argument('design_file')
parser.add_argument(
    '--write-toml', action=argparse.BooleanOptionalAction, default=False)
parser.add_argument(
    '--write-json', action=argparse.BooleanOptionalAction, default=False)
parser.add_argument(
    '--write-yaml', action=argparse.BooleanOptionalAction, default=False)
parser.add_argument(
    '--with-defaults', type=bool, default=False)

args = parser.parse_args()

design_file_path = Path(args.design_file)


class DesignFileType(Enum):
    JSON = auto()
    TOML = auto()
    YAML = auto()


if design_file_path.suffix == '.json':
    design_file_type = DesignFileType.JSON
elif design_file_path.suffix == '.toml':
    design_file_type = DesignFileType.TOML
elif design_file_path.suffix == '.yaml':
    design_file_type = DesignFileType.YAML
else:
    raise Exception("unknown design file extension")


with open(schema_file) as sf:
    schema = json.load(sf)

with open(design_file_path) as df:
    if design_file_type == DesignFileType.JSON:
        design = json.load(df)
    elif design_file_type == DesignFileType.TOML:
        design = toml.load(df)
    elif design_file_type == DesignFileType.YAML:
        design = yaml.load(df)


def extend_with_default(validator_class):
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for property, subschema in properties.items():
            if "default" in subschema:
                instance.setdefault(property, subschema["default"])

        for error in validate_properties(
            validator, properties, instance, schema,
        ):
            yield error

    return validators.extend(
        validator_class, {"properties": set_defaults},
    )

validator = extend_with_default(Draft202012Validator) if args.with_defaults else Draft202012Validator

v = validator(schema)
failed = False
for error in sorted(v.iter_errors(design), key=str):
    print(f"[ERROR] {'.'.join(error.path)}: {error.message}")
    failed = True
if failed:
    print("Design file is INVALID")
    exit(1)

for files in [design['rtl']['sources'], design.get('rtl', {}).get('includes', []), design.get('tb', {}).get('sources', []), design.get('tb', {}).get('includes', []), ]:
    for f in files:
        path = Path(f)
        assert path.exists(), f"file {path} does not exist."
        assert path.is_file(), f"{path} is not a regular file."

if failed:
    print("Design file is INVALID")
    exit(1)

print("Design file is VALID")

if args.write_toml:
    with open(design_file_path.with_suffix(".toml"), "w") as tf:
        toml.dump(design, tf)

if args.write_yaml:
    with open(design_file_path.with_suffix(".yaml"), "w") as tf:
        yaml.dump(design, tf, sort_keys=False)

if args.write_json:
    with open(design_file_path.with_suffix(".json"), "w") as tf:
        json.dump(design, tf, sort_keys=False, indent=4)
