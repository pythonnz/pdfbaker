"""Base configuration for pdfbaker classes."""

import io
import logging
from collections.abc import Mapping, Sequence
from enum import Enum
from pathlib import Path
from typing import Any

import ruamel.yaml
from jinja2 import Template
from jinja2.exceptions import TemplateError as JinjaTemplateError
from pydantic import (
    BaseModel,
    ConfigDict,
    PrivateAttr,
    ValidationError,
    model_validator,
)
from ruamel.yaml import YAML

from .errors import ConfigurationError
from .logging import LoggingMixin

__all__ = [
    "BakerConfig",
    "deep_merge",
    "DocumentConfig",
    "DocumentVariantConfig",
    "PageConfig",
    "render_config",
]

logger = logging.getLogger(__name__)

# FIXME: need to achieve the same effect as the old render_config()
# variables within variables resolved, e.g. {{ variant.name }} in "filename"
# TODO: change examples from images_dir to use directories.images (breaking change)
# TODO: allow directories.images to be either a PathSpec or a list of Pathspecs

DEFAULT_DIRECTORIES = {
    "build": "build",
    "dist": "dist",
    "documents": ".",
    "pages": "pages",
    "templates": "templates",
    "images": "images",
}
DEFAULT_DOCUMENT_CONFIG_FILE = "config.yaml"


class PathSpec(BaseModel):
    """File/Directory location (relative or absolute) in YAML config."""

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


class StyleDict(BaseModel):
    """Style configuration."""

    highlight_color: str | None = None


class DirectoriesConfig(BaseModel):
    """Directories configuration."""

    root: Path
    build: Path
    dist: Path
    documents: Path
    pages: Path
    templates: Path
    images: Path

    def resolved(self) -> "DirectoriesConfig":
        """Resolve relative paths relative to the root directory."""
        root = self.root.resolve()
        resolved = {}
        for field in self.__class__.model_fields.keys():
            path = getattr(self, field)
            resolved[field] = path if path.is_absolute() else (root / path).resolve()
        return DirectoriesConfig(**resolved)


class BaseConfig(BaseModel, LoggingMixin):
    """Base configuration class for pages, documents/variants, baker."""

    model_config = ConfigDict(
        strict=True,  # don't try to coerce values
        extra="allow",  # will go in __pydantic_extra__ dict
    )

    def readable(self, max_chars: int = 60) -> str:
        """Return YAML representation with truncated strings for readability."""
        yaml_instance = get_readable_yaml(max_chars=max_chars)
        stream = io.StringIO()
        yaml_instance.dump(self.model_dump(), stream)
        return f"\n{stream.getvalue()}"


class PageConfig(BaseConfig):
    """Page configuration."""

    config_path: PathSpec
    directories: DirectoriesConfig
    _resolved_directories: DirectoriesConfig = PrivateAttr()
    template: PathSpec

    @model_validator(mode="before")
    @classmethod
    def load_config(cls, data: Any) -> Any:
        """Load document configuration from YAML file."""
        if isinstance(data, dict) and "config_path" in data:
            config_data = YAML().load(data["config_path"].path.read_text())
            config_data.update(data)  # kwargs override YAML values
            data = config_data

            data["directories"]["root"] = data["config_path"].path.parent

        return data

    @model_validator(mode="after")
    def resolve_paths(self) -> "PageConfig":
        """Resolve relative paths relative to the root directory."""
        self._resolved_directories = self.directories.resolved()

        # Resolve template path
        templates_dir = self._resolved_directories.templates
        page_root = self._resolved_directories.root
        if len(self.template.path.parts) > 1:
            # Relative to document root or absolute path
            self.template.path = (page_root / self.template.path).resolve()
        else:
            # Simple string - relative to templates directory
            self.template.path = self.template.resolve_relative_to(templates_dir).path
        self.template.name = self.template.path.name  # not just stem

        return self

    @property
    def name(self) -> str:
        """Page name is the 'name' of its config file."""
        return self.config_path.name

    @property
    def settings(self) -> dict[str, Any]:
        """All configuration settings in a dictionary."""
        return self.model_dump()

    @property
    def user_defined(self) -> dict[str, Any]:
        """Dictionary of all custom user-defined settings."""
        # FIXME: remove if not neeeded (at least for debugging)
        return getattr(self, "__pydantic_extra__", {}) or {}


class DocumentVariantConfig(BaseConfig):
    """Document variant configuration.

    Like a document without a config file or own variants
    """

    name: str
    directories: DirectoriesConfig
    pages: list[PathSpec]

    @model_validator(mode="after")
    def resolve_paths(self) -> "DocumentConfig":
        """Resolve relative paths relative to the root directory."""
        # Resolve page paths
        pages_dir = self.directories.pages
        document_root = self.directories.root
        for page in self.pages:
            if not page.path.suffix:
                page.path = page.path.with_suffix(".yaml")

            if len(page.path.parts) > 1:
                # Relative to document root or absolute path
                page.path = (document_root / page.path).resolve()
            else:
                # Simple string - relative to pages directory
                page.path = page.resolve_relative_to(pages_dir).path

        return self

    @property
    def page_settings(self) -> dict[str, Any]:
        """All configuration settings in a dictionary. Given to pages."""
        return self.model_dump(
            exclude={
                "pages",
            }
        )


class DocumentConfig(BaseConfig):
    """Document configuration.

    Lazy-loads page configs.
    """

    config_path: PathSpec
    directories: DirectoriesConfig
    _resolved_directories: DirectoriesConfig = PrivateAttr()
    variants: list[DocumentVariantConfig] = []
    pages: list[PathSpec] = []
    bake_path: PathSpec | None = None

    @model_validator(mode="before")
    @classmethod
    def load_config(cls, data: Any) -> Any:
        """Load document configuration from YAML file."""
        if isinstance(data, dict) and "config_path" in data:
            if data["config_path"].path.is_dir():
                # Keep name but change path
                data["config_path"].path /= DEFAULT_DOCUMENT_CONFIG_FILE

            config_data = YAML().load(data["config_path"].path.read_text())
            config_data.update(data)  # kwargs override YAML values
            data = config_data

            data["directories"]["root"] = data["config_path"].path.parent

            variants_data = data.get("variants", [])
            valid_variants = []
            for vdata in variants_data:
                try:
                    # FIXME: doc without pages
                    if "pages" in data:
                        variant = DocumentVariantConfig(
                            directories=data["directories"],
                            pages=data["pages"],
                            **vdata,
                        )
                    else:
                        # This should fail if no pages in doc and also not in variant
                        variant = DocumentVariantConfig(
                            directories=data["directories"],
                            **vdata,
                        )
                    valid_variants.append(variant)
                except ValidationError as e:
                    print(f"⚠️ Skipping invalid variant '{vdata.get('name')}': {e}")

            data["variants"] = valid_variants

        return data

    @model_validator(mode="after")
    def resolve_paths(self) -> "DocumentConfig":
        """Resolve relative paths relative to the root directory."""
        self.directories.build = self.directories.build / self.name
        self.directories.dist = self.directories.dist / self.name
        self._resolved_directories = self.directories.resolved()

        # Resolve page paths
        pages_dir = self._resolved_directories.pages
        document_root = self._resolved_directories.root
        for page in self.pages:
            if not page.path.suffix:
                page.path = page.path.with_suffix(".yaml")

            if len(page.path.parts) > 1:
                # Relative to document root or absolute path
                page.path = (document_root / page.path).resolve()
            else:
                # Simple string - relative to pages directory
                page.path = page.resolve_relative_to(pages_dir).path

        if not self.bake_path:
            self.bake_path = PathSpec(
                path=self._resolved_directories.root / "bake.py",
                name="bake.py",
            )

        return self

    @model_validator(mode="after")
    def check_pages_or_variants(self) -> "DocumentConfig":
        """Check if pages or variants are defined."""
        # The "pages" may be defined in the variants rather than
        # the document itself (when different variants have different pages)
        if not self.pages:
            if self.variants:
                # A variant not defining pages will fail to process
                self.log_debug(
                    'Pages of document "%s" will be determined per variant',
                    self.name,
                )
            else:
                self.log_warning(
                    'Document "%s" has neither pages nor variants', self.name
                )
                raise ConfigurationError(
                    f'Cannot determine pages of document "{self.name}"'
                )
        return self

    @property
    def name(self) -> str:
        """Document name is the 'name' of its config file."""
        return self.config_path.name

    @property
    def variant_settings(self) -> dict[str, Any]:
        """Variant settings."""
        # FIXME: see document.py variant processing - need elegance
        settings = {"directories": {}}
        for directory in self.directories.__class__.model_fields.keys():
            settings["directories"][directory] = getattr(
                self._resolved_directories, directory
            )
        return settings

    @property
    def page_settings(self) -> dict[str, Any]:
        """All configuration settings in a dictionary. Given to pages."""
        settings = self.model_dump(exclude={"config_path", "variants", "pages"})
        settings["directories"]["pages"] = self._resolved_directories.pages
        settings["directories"]["templates"] = self._resolved_directories.templates
        settings["directories"]["images"] = self._resolved_directories.images
        return settings


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


class BakerConfig(BaseConfig):
    """Baker configuration.

    Lazy-loads document configs.
    """

    config_file: Path
    directories: DirectoriesConfig
    _resolved_directories: DirectoriesConfig = PrivateAttr()
    documents: list[PathSpec]
    # FIXME: jinja2_extensions set for just a page not picked up
    jinja2_extensions: list[str] = []
    template_renderers: list[TemplateRenderer] = [TemplateRenderer.RENDER_HIGHLIGHT]
    template_filters: list[TemplateFilter] = [TemplateFilter.WORDWRAP]
    svg2pdf_backend: SVG2PDFBackend | None = SVG2PDFBackend.CAIROSVG
    compress_pdf: bool = False
    keep_build: bool = False

    @model_validator(mode="before")
    @classmethod
    def load_config(cls, data: Any) -> Any:
        """Load main configuration from YAML file."""
        if isinstance(data, dict) and "config_file" in data:
            if isinstance(data["config_file"], str):
                data["config_file"] = Path(data["config_file"])
            if isinstance(data["config_file"], Path):
                data["config_file"] = data["config_file"].resolve()

            config_data = YAML().load(data["config_file"].read_text())
            config_data.update(data)  # kwargs override YAML values
            data = config_data

            # Set default directories
            if "directories" not in data:
                data["directories"] = {}
            directories = data["directories"]
            directories.setdefault("root", data["config_file"].parent)
            for key, default in DEFAULT_DIRECTORIES.items():
                directories.setdefault(key, default)

            if "documents" not in data:
                raise ValueError(
                    'Key "documents" missing - is this the main configuration file?'
                )

        return data

    @model_validator(mode="after")
    def resolve_paths(self) -> "BakerConfig":
        """Resolve relative paths relative to the root directory."""
        self._resolved_directories = self.directories.resolved()

        # Resolve build/dist, they are fixed unless re-defined
        self.directories.build = self._resolved_directories.build
        self.directories.dist = self._resolved_directories.dist

        # Resolve document paths
        root = self.directories.root.resolve()
        self.documents = [doc.resolve_relative_to(root) for doc in self.documents]

        return self

    @property
    def document_settings(self) -> dict[str, Any]:
        """All configuration settings relevant for a document."""
        return self.model_dump(exclude={"config_file", "documents"})


def register_representers(yaml_instance, class_tag_map, use_multi_for=()):
    """Register representer..

    If a class is in use_multi_for, subclasses will also be covered.
    (like PosixPath is a subclass of Path)
    """

    def simple_representer(tag):
        """Represent object as a string."""
        return lambda representer, data: representer.represent_scalar(tag, str(data))

    for cls, tag in class_tag_map.items():
        func = simple_representer(tag)
        if cls in use_multi_for:
            # Add a representer for the class and all subclasses.
            yaml_instance.representer.add_multi_representer(cls, func)
        else:
            # Add a representer for this exact class only.
            yaml_instance.representer.add_representer(cls, func)


def get_readable_yaml(max_chars: int = 60) -> ruamel.yaml.YAML:
    """Get a YAML instance with string truncation for readable output."""
    yaml = ruamel.yaml.YAML()
    yaml.indent(offset=4)
    yaml.default_flow_style = False

    register_representers(
        yaml,
        {
            Path: "!path",
            SVG2PDFBackend: "!svg2pdf_backend",
            TemplateRenderer: "!template_renderer",
            TemplateFilter: "!template_filter",
        },
        use_multi_for=(Path,),
    )

    # Add string truncation representer
    def truncating_representer(representer, data):
        if len(data) > max_chars:
            data = data[:max_chars] + "..."
        return representer.represent_scalar("tag:yaml.org,2002:str", data)

    yaml.representer.add_representer(str, truncating_representer)

    return yaml


def deep_merge(base: dict[str, Any], update: dict[str, Any]) -> dict[str, Any]:
    """Deep merge two dictionaries."""
    result = base.copy()
    for key, value in update.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def render_config(config: dict[str, Any], max_iterations: int = 10) -> dict[str, Any]:
    """Render config with its own values."""
    current = dict(config)
    for _ in range(max_iterations):
        new = _render_object(current, context=current)
        if new == current:
            return new
        current = new
    raise ConfigurationError(
        "Maximum number of iterations reached — possible circular reference"
    )


def _render_object(obj, context, seen_keys=None):
    if seen_keys is None:
        seen_keys = set()

    if isinstance(obj, str):
        for key in seen_keys:
            if f"{{{{ {key} }}}}" in obj:
                raise ConfigurationError(
                    f"Circular/self reference detected: '{key}' in '{obj}'"
                )
        try:
            return Template(obj).render(**context)
        except JinjaTemplateError as e:
            raise ConfigurationError(f"Error rendering template '{obj}': {e}") from e

    elif isinstance(obj, Mapping):
        return {k: _render_object(v, context, seen_keys | {k}) for k, v in obj.items()}

    elif isinstance(obj, Sequence) and not isinstance(obj, str):
        return [_render_object(i, context, seen_keys) for i in obj]

    return obj
