"""Test the new Pydantic config models."""

import sys
from pathlib import Path

import ruamel.yaml
from pydantic import ValidationError

from pdfbaker import config

CONFIG_FILE = Path("/home/danny/src/pdfbaker/examples/examples.yaml")


def simple_representer(tag):
    """Represent object as a string."""
    return lambda representer, data: representer.represent_scalar(tag, str(data))


def register_representers(yaml_instance, class_tag_map, use_multi_for=()):
    """Register representer..

    If a class is in use_multi_for, subclasses will also be covered.
    (like PosixPath is a subclass of Path)
    """
    for cls, tag in class_tag_map.items():
        func = simple_representer(tag)
        if cls in use_multi_for:
            # Add a representer for the class and all subclasses.
            yaml_instance.representer.add_multi_representer(cls, func)
        else:
            # Add a representer for this exact class only.
            yaml_instance.representer.add_representer(cls, func)


yaml = ruamel.yaml.YAML()
yaml.indent(offset=4)
yaml.default_flow_style = False
register_representers(
    yaml,
    {
        Path: "!path",
        config.SVG2PDFBackend: "!svg2pdf_backend",
        config.TemplateRenderer: "!template_renderer",
        config.TemplateFilter: "!template_filter",
    },
    use_multi_for=(Path,),
)

try:
    baker_config = config.BakerConfig(config_file=CONFIG_FILE)
    baker_config_dict = baker_config.model_dump()
    print("*** Full config after parsing: ***")
    yaml.dump(baker_config_dict, sys.stdout)
    print()
    print("*** Custom config values only: ***")
    yaml.dump(baker_config.custom_config, sys.stdout)
except ValidationError as e:
    print(e)
