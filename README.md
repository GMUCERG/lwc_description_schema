# Variant description file for Protected LWC Hardware Implementations
A _variant description file_ is a [TOML](https://toml.io/en/) file describing the details of an LWC protected hardware implementation. As suggested in the "Call for Protected Hardware Implementation", a _variant description file_ serves as an organized container of information and meta-data required for automated evaluation of an LWC hardware implementation.

## Schema
The structure of a LWC _variant description file_ is described as a [JSON Schema](https://json-schema.org/draft/2020-12/json-schema-core.html) in the file `lwc.schema.json`. 
The schema provides a precise specification of the hierarchy as well as type, format, and description of the data fields. 

## Examples
Example variant description files are provided in the [examples](./examples) subfolder.

`examples/TinyJAMBU_DOM/tinyjambu-dom1-v1.toml`

## Validation
A Python script is provided to assist validation of a _variant description file_.
Requires: Python 3.7+

Install dependencies:
```
$ python3 -m pip install -U -r validate/requirements.txt
```

Usage:
```
$ python3 ./validate/validate.py --help 
```

Validating a variant description file:
```
$ python3 ./validate/validate.py <path-to-variant-description-file>
```

for example:
```
$ python3 ./validate/validate.py examples/TinyJAMBU_DOM/tinyjambu-dom1-v1.toml
```

## Documentation
Human-readable documentation in Markdown and HTML format is availale in the [doc](./doc) subfolder.
