#!/usr/bin/env python3
#
# Install dependencies before running this script:
#  python3 -m pip install -U -r requirements.txt
#
import json
from logging import getLogger
import logging
from typing import Any, Dict, OrderedDict, Optional
from jsonschema import Draft202012Validator, draft202012_format_checker, validators, RefResolver
from enum import Enum, auto
from pathlib import Path
import toml
import yaml
import argparse
from functools import reduce
import json


try:
    from rich.console import Console
    console: Optional[Console] = Console()
except:
    console = None

def dump_data(design):
    if console:
        console.print_json(data=design)
    else:
        print(json.dumps(design, sort_keys=False, indent=2))

VALIDATE_ROOT = Path(__file__).parent.absolute()

log = getLogger(__name__)

log.setLevel(logging.INFO)


def get_path(dct: Dict[str, Any], path, sep='.'):
    if isinstance(path, str):
        path = path.split(sep)
    try:
        return reduce(dict.__getitem__, path, dct)
    except KeyError as e:
        log.warning(
            "[get_path] Key '%s' in path %s was not found! Full ",
            e.args[0], ".".join(path)
        )
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


parser = argparse.ArgumentParser(description='Validate LWC design files.')

parser.add_argument('design_file', help="LWC variant description file")
parser.add_argument('--schema-file', type=Path,
                    default=VALIDATE_ROOT.parent / "lwc.schema.json")
parser.add_argument('--write-toml', type=str, default=None)
parser.add_argument('--write-json', type=str, default=None)
parser.add_argument('--write-yaml', type=str, default=None)
parser.add_argument('--check-paths', action='store_true')
parser.add_argument('--verbose', action='store_true')

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


with open(args.schema_file) as sf:
    schema = json.load(sf)


with open(design_file_path) as df:
    if design_file_type == DesignFileType.JSON:
        design = json.load(df)
    elif design_file_type == DesignFileType.TOML:
        design = toml.load(df)
    elif design_file_type == DesignFileType.YAML:
        design = yaml.load(df, Loader=yaml.Loader)


def all_required(schem, k=None):
    t = schem.get('type')
    if t is None:
        print(f"[WARNING] {k} has no type")
        return
    if t != "object":
        return
    schem['required'] = []
    if "default" not in schem:
        schem["default"] = {}

    prop = schem.get('properties')
    if prop is None:
        print(f"[WARNING] {k} has no properties")
        return
    for k, v in prop.items():
        # print(f"k={k}")
        if v.get("optional"):
            continue
        schem['required'].append(k)
        all_required(v, k)


def extend_with_default(validator_class):
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for property, subschema in properties.items():
            if "default" in subschema:
                if property not in instance:
                    instance[property] = subschema["default"]
                instance.setdefault(property, subschema["default"])

        for error in validate_properties(
            validator, properties, instance, schema,
        ):
            yield error

    return validators.extend(
        validator_class, {"properties": set_defaults},
    )


all_required(schema)
# print(schema)

# if args.with_defaults else Draft202012Validator
validator = extend_with_default(Draft202012Validator)

resolver = RefResolver.from_schema(schema)

default_reference = validator(
    schema, format_checker=draft202012_format_checker, resolver=resolver)

failed = False
for error in sorted(default_reference.iter_errors(design), key=str):
    # print(error)
    error_path = " → ".join([str(e) for e in error.path])
    print(f"[ERROR]\n    {error_path}: \n    {error.message}\n")
    failed = True

if args.verbose:
    dump_data(design)

if failed:
    print("Design file is INVALID")
    exit(1)


# add missing properties from other properties
# defaults = {
#     'lwc.ports.sdi.bit_width': 'lwc.ports.pdi.bit_width',
#     'lwc.ports.sdi.num_shares': 'lwc.ports.pdi.num_shares',
# }

# if args.with_defaults:
#     for k, default_reference in defaults.items():
#         if get_path(design, k) is None:
#             default_value = get_path(design, default_reference)
#             print(f"missing {k} set to {default_reference} = {default_value}")
#             set_path(design, k, default_value)

if args.check_paths:
    for p in ['rtl', 'tb']:
        x = design.get(p, {})
        for files in [x.get('sources', []), x.get('includes', [])]:
            for f in files:
                path = Path(f)
                assert path.exists(), f"file {path} does not exist."
                assert path.is_file(), f"{path} is not a regular file."

for p in ['rtl', 'tb']:
    x = design.get(p, {})
    params = x.get('parameters', {})
    if params and args.verbose:
        print(f"design.{p}.parameters:")
        dump_data(params)
    for p_name, p_data in params.items():
        if p_data and isinstance(p_data, dict):
            assert all(isinstance(k, str) and isinstance(v, str) and k == 'file'
                       for k, v in p_data.items()), f"Unsupported dict format in design.{p}.parameters.{p_name}"

assert (get_path(design, 'lwc.sca_protection.order') > 0) == (
    get_path(design, 'lwc.ports.pdi.num_shares') > 1) == (get_path(design, 'lwc.ports.pdi.num_shares') > 1)


print("\nDesign file is VALID    \n")

if args.write_toml:
    with open(args.write_toml, "w") as tf:
        toml.dump(design, tf, encoder=toml.TomlEncoder(
            _dict=OrderedDict, preserve=True)
        )

if args.write_yaml:
    with open(args.write_yaml, "w") as tf:
        yaml.dump(design, tf, sort_keys=False)

if args.write_json:
    with open(args.write_json, "w") as tf:
        json.dump(design, tf, sort_keys=False, indent=4)
