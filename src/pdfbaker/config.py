"""Base configuration for pdfbaker classes."""

import logging
import pprint
from enum import Enum
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Template
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)
from ruamel.yaml import YAML

from .errors import ConfigurationError
from .logging import LoggingMixin, truncate_strings
from .types import PathSpec

__all__ = ["PDFBakerConfiguration", "deep_merge", "render_config"]

logger = logging.getLogger(__name__)


# #####################################################################
# New Pydantic models
# #####################################################################

# TODO: show names instead of index numbers for error locations
#       https://docs.pydantic.dev/latest/errors/errors/#customize-error-messages


class NewPathSpec(BaseModel):
    """File/Directory location in YAML config."""

    # Relative paths may not exist until resolved against root,
    # so we have to check existence later
    # path: FilePath | DirectoryPath
    path: Path
    name: str = Field(default_factory=lambda data: data["path"].stem)

    @model_validator(mode="before")
    @classmethod
    def ensure_pathspec(cls, data: Any) -> Any:
        """Coerce what was given"""
        if isinstance(data, str):
            data = {"name": data}
        if isinstance(data, dict) and "path" not in data:
            data["path"] = Path(data["name"])
        return data


class ImageSpec(NewPathSpec):
    """Image specification."""

    type: str | None = None
    data: str | None = None


class StyleDict(BaseModel):
    """Style configuration."""

    highlight_color: str | None = None


class DirectoriesConfig(BaseModel):
    """Directories configuration."""

    root: NewPathSpec
    build: NewPathSpec
    dist: NewPathSpec
    documents: NewPathSpec
    pages: NewPathSpec
    templates: NewPathSpec
    images: NewPathSpec

    @model_validator(mode="after")
    def resolve_paths(self) -> Any:
        """Resolve all paths relative to the root directory."""
        self.root.path = self.root.path.resolve()
        for field_name, value in self.__dict__.items():
            if field_name != "root" and isinstance(value, NewPathSpec):
                value.path = (self.root.path / value.path).resolve()
        return self


class PageConfig(BaseModel, LoggingMixin):
    """Page configuration."""

    directories: DirectoriesConfig
    template: NewPathSpec
    model_config = ConfigDict(
        strict=True,  # don't try to coerce values
        extra="allow",  # will go in __pydantic_extra__ dict
    )


class DocumentConfig(BaseModel, LoggingMixin):
    """Document configuration.

    Lazy-loads page configs.
    """

    directories: DirectoriesConfig
    pages: list[Path | PageConfig]
    model_config = ConfigDict(
        strict=True,  # don't try to coerce values
        extra="allow",  # will go in __pydantic_extra__ dict
    )


class DocumentVariantConfig(DocumentConfig):
    """Document variant configuration."""


class TemplateRenderer(Enum):
    """Possible values for template_renderers."""

    RENDER_HIGHLIGHT = "render_highlight"


class TemplateFilter(Enum):
    """Possible values for template_filters."""

    WORDWRAP = "wordwrap"


class SVG2PDFBackend(Enum):
    """Possible values for svg2pdf_backend."""

    CAIROSVG = "cairosvg"
    INKSCAPE = "inkscape"


class BakerConfig(BaseModel, LoggingMixin):
    """Baker configuration.

    Lazy-loads document configs.
    """

    directories: DirectoriesConfig
    # TODO: lazy/forgiving documents parsing
    # documents: list[Path | DocumentConfig]
    documents: list[str]
    template_renderers: list[TemplateRenderer] = [TemplateRenderer.RENDER_HIGHLIGHT]
    template_filters: list[TemplateFilter] = [TemplateFilter.WORDWRAP]
    svg2pdf_backend: SVG2PDFBackend | None = SVG2PDFBackend.CAIROSVG
    compress_pdf: bool = False
    model_config = ConfigDict(
        strict=True,  # don't try to coerce values
        extra="allow",  # will go in __pydantic_extra__ dict
    )

    @model_validator(mode="before")
    @classmethod
    def load_config(cls, data: Any) -> Any:
        """Load main configuration from YAML file."""
        if isinstance(data, dict) and "config_file" in data:
            # FIXME: save config_file path in model
            # then load in "after" validator
            # nice side effect: just change config_file to reload
            config_file = data.pop("config_file")
            config_data = YAML().load(config_file.read_text())
            config_data.update(data)  # let kwargs override values from YAML
            return config_data
        return data

    @model_validator(mode="before")
    @classmethod
    def set_default_directories(cls, data: Any) -> Any:
        """Set default directories."""
        if isinstance(data, dict):
            directories = data.setdefault("directories", {})
            directories.setdefault("root", ".")  # FIXME: should be config parent
            directories.setdefault("build", "build")
            directories.setdefault("dist", "dist")
            directories.setdefault("documents", ".")
            directories.setdefault("pages", "pages")
            directories.setdefault("templates", "templates")
            directories.setdefault("images", "images")
        return data

    @property
    def custom_config(self) -> dict[str, Any]:
        """Dictionary of all custom user-defined configuration."""
        return self.__pydantic_extra__


class BakerOptions(BaseModel):
    """Options for controlling PDFBaker behavior.

    Attributes:
        quiet: Show errors only
        verbose: Show debug information
        trace: Show trace information (even more detailed than debug)
        keep_build: Keep build artifacts after processing
        default_config_overrides: Dictionary of values to override the built-in defaults
            before loading the main configuration
    """

    quiet: bool = False
    verbose: bool = False
    trace: bool = False
    keep_build: bool = False
    default_config_overrides: dict[str, Any] | None = None


# #####################################################################


def deep_merge(base: dict[str, Any], update: dict[str, Any]) -> dict[str, Any]:
    """Deep merge two dictionaries."""
    result = base.copy()
    for key, value in update.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


class PDFBakerConfiguration(dict):
    """Base  class for handling config loading/merging/parsing."""

    def __init__(
        self,
        base_config: dict[str, Any],
        config_file: Path,
    ) -> None:
        """Initialize configuration from a file.

        Args:
            base_config: Existing base configuration
            config: Path to YAML file to merge with base_config
        """
        try:
            with open(config_file, encoding="utf-8") as f:
                config = yaml.safe_load(f)
        except yaml.scanner.ScannerError as exc:
            raise ConfigurationError(
                f"Invalid YAML syntax in config file {config_file}: {exc}"
            ) from exc
        except Exception as exc:
            raise ConfigurationError(f"Failed to load config file: {exc}") from exc

        # Determine all relevant directories
        self["directories"] = directories = {"config": config_file.parent.resolve()}
        for directory in (
            "documents",
            "pages",
            "templates",
            "images",
            "build",
            "dist",
        ):
            if directory in config.get("directories", {}):
                # Set in this config file, relative to this config file
                directories[directory] = self.resolve_path(
                    config["directories"][directory]
                )
            elif directory in base_config.get("directories", {}):
                # Inherited (absolute) or default (relative to _this_ config)
                directories[directory] = self.resolve_path(
                    str(base_config["directories"][directory])
                )
        super().__init__(deep_merge(base_config, config))
        self["directories"] = directories

    def resolve_path(self, spec: PathSpec, directory: Path | None = None) -> Path:
        """Resolve a possibly relative path specification.

        Args:
            spec: Path specification (string or dict with path/name)
            directory: Optional directory to use for resolving paths
        Returns:
            Resolved Path object
        """
        directory = directory or self["directories"]["config"]
        if isinstance(directory, str):
            directory = Path(directory)

        if isinstance(spec, str):
            return directory / spec

        if "path" not in spec and "name" not in spec:
            raise ConfigurationError("Invalid path specification: needs path or name")

        if "path" in spec:
            return Path(spec["path"])

        return directory / spec["name"]

    def pretty(self, max_chars: int = 60) -> str:
        """Return readable presentation (for debugging)."""
        truncated = truncate_strings(self, max_chars=max_chars)
        return pprint.pformat(truncated, indent=2)


def _convert_paths_to_strings(config: dict[str, Any]) -> dict[str, Any]:
    """Convert all Path objects in config to strings."""
    result = {}
    for key, value in config.items():
        if isinstance(value, Path):
            result[key] = str(value)
        elif isinstance(value, dict):
            result[key] = _convert_paths_to_strings(value)
        elif isinstance(value, list):
            result[key] = [
                _convert_paths_to_strings(item)
                if isinstance(item, dict)
                else str(item)
                if isinstance(item, Path)
                else item
                for item in value
            ]
        else:
            result[key] = value
    return result


def render_config(config: dict[str, Any]) -> dict[str, Any]:
    """Resolve all template strings in config using its own values.

    This allows the use of "{{ variant }}" in the "filename" etc.

    Args:
        config: Configuration dictionary to render

    Returns:
        Resolved configuration dictionary

    Raises:
        ConfigurationError: If maximum number of iterations is reached
            (circular references)
    """
    max_iterations = 10
    current_config = dict(config)
    current_config = _convert_paths_to_strings(current_config)

    for _ in range(max_iterations):
        config_yaml = Template(yaml.dump(current_config))
        resolved_yaml = config_yaml.render(**current_config)
        new_config = yaml.safe_load(resolved_yaml)

        # Check for direct self-references
        for key, value in new_config.items():
            if isinstance(value, str) and f"{{{{ {key} }}}}" in value:
                raise ConfigurationError(
                    f"Circular reference detected: {key} references itself"
                )

        if new_config == current_config:  # No more changes
            return new_config
        current_config = new_config

    raise ConfigurationError(
        "Maximum number of iterations reached. "
        "Check for circular references in your configuration."
    )
