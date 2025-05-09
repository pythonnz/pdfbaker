"""Base configuration for pdfbaker classes."""

import io
from enum import Enum
from pathlib import Path
from typing import Any

from jinja2 import Template
from jinja2 import TemplateError as JinjaTemplateError
from pydantic import BaseModel, ConfigDict, field_validator, model_validator
from ruamel.yaml import YAML

from ..errors import ConfigurationError
from ..logging import LoggingMixin

__all__ = [
    "BaseConfig",
    "Directories",
    "ImageSpec",
    "PathSpec",
    "SVG2PDFBackend",
    "TemplateFilter",
    "TemplateRenderer",
]


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


def convert_enum(enum_class):
    """Convert a string to an enum value."""

    def _convert(value):
        if isinstance(value, str):
            return enum_class(value)
        return value

    return _convert


class PathSpec(BaseModel):
    """File/Directory location (relative or absolute) in a YAML config."""

    path: Path
    name: str

    @model_validator(mode="before")
    @classmethod
    def ensure_pathspec(cls, data: Any) -> Any:
        """Coerce string/Path or partial dict into full dict with 'path' and 'name'."""
        if isinstance(data, str | Path):
            path = Path(data)
            data = {"path": path, "name": path.stem}
        elif isinstance(data, dict):
            if "path" not in data:
                raise ValueError("path is required")
            path = Path(data["path"])
            data = {"path": path, "name": data.get("name", path.stem)}
        return data

    def resolve_relative_to(self, base: Path) -> "PathSpec":
        """Resolve relative paths relative to a base directory."""
        path = self.path
        if not path.is_absolute():
            path = (base / path).resolve()
        return PathSpec(path=path, name=self.name)


class ImageSpec(PathSpec):
    """Image specification."""

    type: str | None = None
    data: str | None = None


class Directories(BaseModel):
    """Directories configuration."""

    base: Path
    build: Path
    dist: Path
    documents: Path
    pages: Path
    templates: Path
    images: Path

    @model_validator(mode="before")
    @classmethod
    def ensure_resolved_base(cls, data: Any) -> Any:
        """Ensure base path is absolute."""
        if isinstance(data, dict):
            data["base"] = Path(data["base"]).resolve()
        return data


class BaseConfig(BaseModel, LoggingMixin):
    """Base configuration class for BakerConfig, DocumentConfig and PageConfig."""

    directories: Directories
    jinja2_extensions: list[str] = []
    template_renderers: list[TemplateRenderer] = [TemplateRenderer.RENDER_HIGHLIGHT]
    template_filters: list[TemplateFilter] = [TemplateFilter.WORDWRAP]
    svg2pdf_backend: SVG2PDFBackend | None = SVG2PDFBackend.CAIROSVG
    compress_pdf: bool = False
    keep_build: bool = False

    model_config = ConfigDict(
        strict=True,  # don't try to coerce values
        extra="allow",  # extra kwargs will go in __pydantic_extra__
    )

    @field_validator("template_renderers", mode="before")
    @classmethod
    def validate_template_renderers(cls, value: list[str]) -> list[TemplateRenderer]:
        """Convert strings to TemplateRenderer enum values."""
        return [convert_enum(TemplateRenderer)(item) for item in value]

    @field_validator("template_filters", mode="before")
    @classmethod
    def validate_template_filters(cls, value: list[str]) -> list[TemplateFilter]:
        """Convert strings to TemplateFilter enum values."""
        return [convert_enum(TemplateFilter)(item) for item in value]

    @field_validator("svg2pdf_backend", mode="before")
    @classmethod
    def validate_svg2pdf_backend(cls, value: str) -> SVG2PDFBackend:
        """Convert string to SVG2PDFBackend enum value."""
        return convert_enum(SVG2PDFBackend)(value)

    def readable(self, max_chars: int = 60) -> str:
        """Return readable YAML representation with truncated strings."""
        yaml = YAML()
        yaml.indent(offset=4)
        yaml.default_flow_style = False
        yaml.representer.ignore_aliases = lambda *args: True

        def add_simple_representer(cls, tag, use_multi=False):
            """Add a representer that converts objects to string with a tag."""

            def representer(r, data):
                return r.represent_scalar(tag, str(data))

            if use_multi:
                yaml.representer.add_multi_representer(cls, representer)
            else:
                yaml.representer.add_representer(cls, representer)

        add_simple_representer(Path, "!path", use_multi=True)
        add_simple_representer(SVG2PDFBackend, "!svg2pdf_backend")
        add_simple_representer(TemplateRenderer, "!template_renderer")
        add_simple_representer(TemplateFilter, "!template_filter")

        def truncating_representer(representer, data):
            if len(data) > max_chars:
                data = data[:max_chars] + "..."
            return representer.represent_scalar("tag:yaml.org,2002:str", data)

        yaml.representer.add_representer(str, truncating_representer)

        stream = io.StringIO()
        yaml.dump(self.model_dump(), stream)
        return f"\n{stream.getvalue()}"

    def resolve_path(self, path: Path) -> Path:
        """Resolve relative paths relative to the base directory."""
        return (self.directories.base.resolve() / path).resolve()

    @property
    def user_defined_settings(self) -> dict[str, Any]:
        """Return dictionary of user-defined settings."""
        return getattr(self, "__pydantic_extra__", {}) or {}

    def merge(self, update: dict[str, Any]) -> "BaseConfig":
        """Deep merge a dictionary into a config, returning a new config instance."""

        def _deep_merge(
            base_dict: dict[str, Any], update_dict: dict[str, Any]
        ) -> dict[str, Any]:
            """Deep merge two dictionaries."""
            result = base_dict.copy()
            for key, value in update_dict.items():
                if (
                    key in result
                    and isinstance(result[key], dict)
                    and isinstance(value, dict)
                ):
                    result[key] = _deep_merge(result[key], value)
                else:
                    result[key] = value
            return result

        base_dict = self.model_dump()
        merged = _deep_merge(base_dict, update)
        return self.__class__(**merged)

    # ruff: noqa: C901
    def resolve_variables(self, max_iterations: int = 10) -> "BaseConfig":
        """Resolve template variables in config values, modifying in place.

        For example this allows:
        ```yaml
        filename: "{{ variant.name | lower }}_variant"
        ```

        Args:
            max_iterations: Maximum number of iterations to avoid circular references
        """

        def render_template_string(value: str, context: dict[str, Any]) -> str:
            try:
                return Template(value).render(**context)
            except JinjaTemplateError as e:
                raise ConfigurationError(f'Error rendering value "{value}": {e}') from e

        def walk_and_resolve(obj: Any, context: dict[str, Any]) -> Any:
            if isinstance(obj, str) and "{{" in obj:
                return render_template_string(obj, context)
            if isinstance(obj, dict):
                return {k: walk_and_resolve(v, context) for k, v in obj.items()}
            if isinstance(obj, list):
                return [walk_and_resolve(v, context) for v in obj]
            if isinstance(obj, BaseModel):
                for field_name, field_value in obj.model_dump().items():
                    field = getattr(obj.__class__, field_name, None)
                    if isinstance(field, property) and field.fset is None:
                        continue
                    resolved = walk_and_resolve(field_value, context)
                    if resolved != field_value:
                        setattr(obj, field_name, resolved)
            return obj

        def has_unresolved_templates(obj: Any) -> bool:
            if isinstance(obj, str):
                return "{{" in obj
            if isinstance(obj, dict):
                return any(has_unresolved_templates(v) for v in obj.values())
            if isinstance(obj, list):
                return any(has_unresolved_templates(v) for v in obj)
            if isinstance(obj, BaseModel):
                return any(
                    has_unresolved_templates(v) for v in obj.model_dump().values()
                )
            return False

        context = self.model_dump()
        for _ in range(max_iterations):
            walk_and_resolve(self, context)
            if not has_unresolved_templates(self):
                return self

        raise ConfigurationError(
            "Maximum iterations reached, possible circular reference"
        )
