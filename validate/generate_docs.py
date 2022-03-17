#!/usr/bin/env python3
#
# Install dependencies before running this script:
#  python3 -m pip install -U -r requirements.txt
#
import json
import re
from typing import Dict, Optional, List, Any, Union
import io
from functools import reduce
import json
from typing import Any, Dict, Mapping, OrderedDict, Type
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
import io


def get_path(dct: Dict[str, Any], path, sep='/'):
    if isinstance(path, str):
        path = path.split(sep)
    try:
        return reduce(dict.__getitem__, path, dct)
    except:
        return None

# Following borrowed from jsonschema2md.py
# Original author: Ralf Gabriels (ralfg@hotmail.be)
# License: Apache-2.0"
# Modified by Kamyar Mohajerani. All modifications are under Apache-2.0 license.


name_monospace: bool = True


class Parser:
    def __init__(self, schema_object, tab_size=4) -> None:
        self.schema_object = schema_object
        self.tab_size = tab_size

    def _construct_description_line(
        self,
        obj: Dict,
        add_type: bool = False
    ) -> List[str]:
        """Construct description line of property, definition, or item."""
        description_line = []

        if "description" in obj:
            ending = "" if re.search(r"[.?!;]$", obj["description"]) else "."
            description_line.append(f"{obj['description']}{ending} ")
        if add_type:
            if "type" in obj:
                description_line.append(f"Must be of type *{obj['type']}*")
        if "minimum" in obj:
            description_line.append(f"  _Minimum:_ `{obj['minimum']}` ")
        if "maximum" in obj:
            description_line.append(f"  _Maximum:_ `{obj['maximum']}` ")
        if "enum" in obj:
            description_line.append(
                f"  _Supported values:_ `{'`, `'.join(obj['enum'])}` ")
        # if "additionalProperties" in obj:
        #     if obj["additionalProperties"]:
        #         description_line.append("Can contain additional properties.")
        #     else:
        #         description_line.append(
        #             "Cannot contain additional properties.")
        if "default" in obj:
            default_value = obj['default']
            if isinstance(default_value, bool):
                default_value = str(default_value).lower()
            description_line.append(f"  _Default:_ `{default_value}` ")

        return description_line

    def _construct_examples(
        self,
        obj: Dict,
        indent_level: int = 0,
        add_header: bool = True
    ) -> Sequence[str]:
        def dump_json_with_line_head(obj, line_head, **kwargs):
            f = io.StringIO(json.dumps(obj, **kwargs))
            result = [line_head + line for line in f.readlines()]
            return ''.join(result)

        example_lines = []
        if "examples" in obj:
            example_indentation = " " * self.tab_size * (indent_level + 1)
            if add_header:
                example_lines.append(
                    f'{example_indentation}_Examples:_\n{example_indentation}')
            all_examples = []
            for example in obj["examples"]:
                example_str = dump_json_with_line_head(
                    example,
                    line_head="",
                    # indent=4
                )
                all_examples.append(f"`{example_str}`")
            example_lines.append(
                f"{example_indentation}{', '.join(all_examples)}\n")
        return example_lines

    def _parse_object(
        self,
        obj: Dict[str, Union[str, int, bool, Dict[str, Any], List]],
        name: str,
        output_lines: Optional[List[str]] = None,
        level: int = -1,
        required: bool = True
    ) -> Sequence[str]:
        """Parse JSON object and its items, definitions, and properties recursively."""
        if not isinstance(obj, dict):
            raise TypeError(
                f"Non-object type found in properties list: `{name}: {obj}`."
            )

        if not output_lines:
            output_lines = []

        indentation = " " * self.tab_size * level if level > 0 else ""
        indentation_items = " " * self.tab_size * (level+1)

        ref = obj.get('$ref')
        if ref:
            assert isinstance(ref, str)
            ref_path = ref.removeprefix('#/')
            defi = get_path(self.schema_object, ref_path)
            if ref_path:
                obj = {**obj, **defi}

        # Construct full description line
        description_line_base = self._construct_description_line(obj)
        if description_line_base:
            description_line_base.insert(0, ":")

        description_line = list(
            map(
                lambda line: line.replace("\n\n", "<br>" + indentation_items),
                description_line_base
            )
        )

        def proc_type(typ, parent_is_array=False):
            if typ:
                if isinstance(typ, list):
                    typ = [proc_type(t, parent_is_array) for t in typ]
                    typ = " or ".join(typ)
                elif typ == "array" and "items" in obj:
                    items_type = obj["items"].get("type")
                    if items_type:
                        t = "array"
                        if parent_is_array:
                            t += "s"
                        typ = f"{t} of {proc_type(items_type, True)}"
            elif parent_is_array:
                return typ + "s"
            return typ

        typ = proc_type(obj.get('type'))

        obj_type = f" *({typ})*" if typ and typ != "object" else ""

        if name:
            # name = name.replace('_', '\\_')
            name_formatted = f"**`{name}`**" if name_monospace else f"**{name}**"
            if required:
                name_formatted = f"***`{name}`***" if name_monospace else f"**{name}**"
            pre = indentation + "- " if level >= 0 else ""
            output_lines.append(
                f"{pre}{name_formatted}{obj_type}{' '.join(description_line)}\n"
            )

        # Recursively add items and definitions:
        # for name, key in [("Items", "items")]:
        #     if key in obj:
        #         output_lines = self._parse_object(
        #             obj[key],
        #             name,
        #             name_monospace=False,
        #             output_lines=output_lines,
        #             indent_level=indent_level + 1
        #         )

        # Recursively add child properties
        required_fields: List = obj.get("required", [])
        assert isinstance(required_fields, list)
        if "properties" in obj:
            for property_name, property_obj in obj.get("properties", {}).items():
                output_lines = self._parse_object(
                    property_obj,
                    property_name,
                    output_lines=output_lines,
                    level=level + 1,
                    required=required and (property_name in required_fields)
                )

        # Add examples
        output_lines.extend(
            self._construct_examples(obj, indent_level=level)
        )

        return output_lines

    def generate_md(self) -> Sequence[str]:
        """Parse JSON Schema object to markdown text."""
        schema_object = self.schema_object
        output_lines: List[str] = []

        # Add title and description
        # if "title" in schema_object:
        #     output_lines.append(f"# {schema_object['title']}\n\n")
        # else:
        #     output_lines.append("# JSON Schema\n\n")
        # if "description" in schema_object:
        #     output_lines.append(f"{schema_object['description']}\n\n")

        # Add properties and definitions
        # for name, key in [("Properties", "properties")]:
        #     if key in schema_object:
        #         output_lines.append(f"## {name}:\n")
        #         for obj_name, obj in schema_object[key].items():
        #             output_lines.extend(self._parse_object(obj, obj_name))
        output_lines.extend(self._parse_object(
            schema_object, schema_object.get('title', "Schema"), required=True))

        # Add examples
        # if "examples" in schema_object:
        #     output_lines.append("## Examples\n")
        #     output_lines.extend(self._construct_examples(
        #         schema_object, indent_level=0, add_header=False
        #     ))

        return output_lines


#############################################
# end of code based on jsonschema2md.py
#############################################


arg_parser = argparse.ArgumentParser(description='Validate LWC design files.')
arg_parser.add_argument('--schema-file', default="lwc.schema.json")
arg_parser.add_argument('--html', action='store_true')
arg_parser.add_argument('--markdown', action='store_true', default=True)
args = arg_parser.parse_args()

with open(args.schema_file) as sf:
    schema = json.load(sf)

html_filename = "doc/lwc_design_doc.html"
md_filename = "doc/lwc_design_doc.md"
pdf_file_path = "doc/lwc_design_doc.pdf"

if args.markdown:

    # schema_doc_config = GenerationConfiguration(
    #     # expand_buttons=True,
    #     description_is_markdown=True,
    #     with_footer=False,
    #     # link_to_reused_ref = False,
    #     show_toc = False,
    #     template_name='md', # or "md_nested"
    # )
    # generate_from_filename(args.schema_file, filename, config=schema_doc_config)
    parser = Parser(schema)
    md_lines = parser.generate_md()
    md_content = "".join(md_lines)
    with open(md_filename, "w") as output_markdown:
        output_markdown.write(md_content)

    from markdown2 import markdown
    md = markdown(md_content, extras=None)

    # with open(html_filename, "w") as output_markdown:
    #     output_markdown.write(md)

    # from weasyprint import HTML, CSS
    # html = HTML(string=md)
    # css = []
    # css.append(CSS(filename='validate/md.css'))
    # html.write_pdf(pdf_file_path, stylesheets=css)

if args.html:
    from json_schema_for_humans.generate import generate_from_filename
    from json_schema_for_humans.generation_configuration import GenerationConfiguration

    schema_doc_config = GenerationConfiguration(
        # expand_buttons=True,
        description_is_markdown=True,
        with_footer=False,
        link_to_reused_ref=False,
        template_name='js',  # or flat
    )
    generate_from_filename(args.schema_file, html_filename,
                           config=schema_doc_config)
