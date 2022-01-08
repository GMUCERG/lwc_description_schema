# LWC submission format

## Schema
The structure of LWC design file is described as a [JSON Schema](https://json-schema.org/draft/2020-12/json-schema-core.html) in the file `lwc.schema.json`. 

The schema contains the hierarchy of design properties and their types, format, etc. The schema can be used to validate design files in `TOML`, `JSON`, or `YAML` format (see Validation).
This schema also includes description of the data fields and is used to generate the human-readable documentation.

## Examples
Example design files are provided in the [examples](./examples) directory.

`examples/TinyJAMBU_DOM/tinyjambu-dom1-v1.toml`

## Validation
A Python script is provided to assist validation of design files.

Requires: Python 3.7+

Install dependencies:
```
$ python3 -m pip install -U -r validate/requirements.txt
```


Usage:
```
./validate/validate.py --help 
```

Validating a design file:
```
./validate/validate.py examples/TinyJAMBU_DOM/tinyjambu-dom1-v1.toml
```

## Documentation
Human-readable documentation in PDF, HTML, and Markdown format is availale in [schema_doc](./schema_doc) folder.
