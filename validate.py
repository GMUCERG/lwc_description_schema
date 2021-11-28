#!/usr/bin/env python3
#
# Install dependencies before running this script:
#  python3 -m pip install -U -r requirements.txt
#
import json
from typing import Any, Dict, Mapping, Type
import jsonschema
from jsonschema import Draft202012Validator, validators
from enum import Enum, auto
from pathlib import Path
import toml
import yaml
import argparse
from functools import reduce

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
    '--with-defaults', action='store_true')

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
        design = yaml.load(df, Loader=yaml.Loader)


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


# if args.with_defaults else Draft202012Validator
validator = extend_with_default(Draft202012Validator)

default_reference = validator(schema, format_checker=jsonschema.draft202012_format_checker)
failed = False
for error in sorted(default_reference.iter_errors(design), key=str):
    print(f"[ERROR] {'.'.join(error.path)}: {error.message}")
    failed = True
if failed:
    print("Design file is INVALID")
    exit(1)

def get_path(dct: Dict[str, Any], path, sep='.'):
    if isinstance(path, str):
        path = path.split(sep)
    try:
        return reduce(dict.__getitem__, path, dct)
    except:
        return None

def set_path(dct: Dict[str, Any], path, value, sep='.'):
    if isinstance(path, str):
        path = path.split(sep)
    k = path[0]
    if len(path) == 1:
        dct[k] = value
    else:
        if k not in dct:
            dct[k] = {}
        set_path(dct[k], path[1:], value, sep)


## add missing properties from other properties
defaults = {
    'lwc.ports.sdi.bit_width' : 'lwc.ports.pdi.bit_width',
    'lwc.ports.sdi.num_shares': 'lwc.ports.pdi.num_shares',
    'lwc.ports.do.bit_width'  : 'lwc.ports.pdi.bit_width',
    'lwc.ports.do.num_shares' : 'lwc.ports.pdi.num_shares',
}

for k, default_reference in defaults.items():
    if get_path(design, k) is None:
        default_value = get_path(design, default_reference)
        print(f"missing {k} set to {default_reference} = {default_value}")
        set_path(design, k, default_value)

for files in [design['rtl']['sources'], design.get('rtl', {}).get('includes', []), design.get('tb', {}).get('sources', []), design.get('tb', {}).get('includes', []), ]:
    for f in files:
        path = Path(f)
        assert path.exists(), f"file {path} does not exist."
        assert path.is_file(), f"{path} is not a regular file."

if failed:
    print("Design file is INVALID")
    exit(1)



assert (get_path(design, 'lwc.sca_protection.order') > 0) == (get_path(design, 'lwc.ports.pdi.num_shares') > 1)


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
