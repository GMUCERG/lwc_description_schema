#!/usr/bin/env python3
#
# Install dependencies before running this script:
#  python3 -m pip install -U -r requirements.txt
#
import json
from typing import Any, Dict, Mapping, OrderedDict, Type
import jsonschema
from jsonschema import Draft202012Validator, draft202012_format_checker, validators, RefResolver
from enum import Enum, auto
from pathlib import Path
import toml
from toml import ordered as toml_ordered
import yaml
import argparse
from functools import reduce
import json
import re
from typing import Dict, Optional, Sequence, Any


def get_path(dct: Dict[str, Any], path, sep='/'):
    if isinstance(path, str):
        path = path.split(sep)
    try:
        return reduce(dict.__getitem__, path, dct)
    except:
        return None


parser = argparse.ArgumentParser(description='Validate LWC design files.')

parser.add_argument('design_file')

parser.add_argument('--schema-file', default="lwc.schema.json")
parser.add_argument(
    '--write-toml', type=str, default=None)
parser.add_argument(
    '--write-json', type=str, default=None)
parser.add_argument(
    '--write-yaml', type=str, default=None)
# parser.add_argument(
#     '--with-defaults', action='store_true', default=False)

parser.add_argument(
    '--check-paths', action='store_true')

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
    for files in [design['rtl']['sources'], design.get('rtl', {}).get('includes', []), design.get('tb', {}).get('sources', []), design.get('tb', {}).get('includes', []), ]:
        for f in files:
            path = Path(f)
            assert path.exists(), f"file {path} does not exist."
            assert path.is_file(), f"{path} is not a regular file."

if failed:
    print("Design file is INVALID")
    exit(1)


assert (get_path(design, 'lwc.sca_protection.order') > 0) == (
    get_path(design, 'lwc.ports.pdi.num_shares') > 1) == (get_path(design, 'lwc.ports.pdi.num_shares') > 1)


print("\nDesign file is VALID    \n")

if args.write_toml:
    with open(args.write_toml, "w") as tf:
        # toml.dump(design, tf, encoder=toml_ordered.TomlOrderedEncoder())
        toml.dump(design, tf, encoder=toml.TomlEncoder(
            _dict=OrderedDict, preserve=True))

if args.write_yaml:
    with open(args.write_yaml, "w") as tf:
        yaml.dump(design, tf, sort_keys=False)

if args.write_json:
    with open(args.write_json, "w") as tf:
        json.dump(design, tf, sort_keys=False, indent=4)

#
# \emph{\textbf{\texttt{ -> \uline{\textbf{\texttt{
# \setlist[itemize]{label={\tiny$\bullet$}, leftmargin = *}
# \begin{itemize}[
#   labelsep=1pt,
#   labelindent=0pt,%0.5\parindent,
#   itemindent=0pt,
#   leftmargin=1pt,
#   before=\setlength{\listparindent}{-\leftmargin},
#   label=\textbullet
# ]
