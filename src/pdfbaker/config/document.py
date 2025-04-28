"""Document configuration for pdfbaker."""

import logging
from typing import Any

from pydantic import ValidationError, model_validator
from ruamel.yaml import YAML

from . import (
    BaseConfig,
    ConfigurationError,
    PathSpec,
)

logger = logging.getLogger(__name__)
DEFAULT_DOCUMENT_CONFIG_FILE = "config.yaml"


class DocumentConfig(BaseConfig):
    """Document configuration.

    Lazy-loads page configs.
    """

    config_path: PathSpec | None = None
    name: str
    filename: str
    variants: list["DocumentConfig"] | list[dict[str, Any]] = []
    is_variant: bool = False
    pages: list[PathSpec] = []
    # TODO: "exclude if None" make sense here
    # https://github.com/pydantic/pydantic-core/pull/1535
    custom_bake: PathSpec | None = None

    @model_validator(mode="before")
    @classmethod
    def load_config(cls, data: Any) -> Any:
        """Load document configuration from YAML file."""
        if isinstance(data, dict) and data.get("config_path", None) is not None:
            if isinstance(data["config_path"], dict):
                data["config_path"] = PathSpec(**data["config_path"])
            data["name"] = data.get("name", data["config_path"].name)
            if data["config_path"].path.is_dir():
                # Change path but not name
                data["config_path"].path /= DEFAULT_DOCUMENT_CONFIG_FILE

            config_path = data["config_path"]
            config_data = YAML().load(config_path.path.read_text())
            data.update(config_data)  # YAML values override kwargs
            data["directories"]["base"] = config_path.path.parent

        return data

    @model_validator(mode="after")
    def resolve_paths(self) -> "DocumentConfig":
        """Resolve relative paths."""
        self.directories.pages = self.resolve_path(self.directories.pages)

        # Resolve page paths
        for page in self.pages:
            if not page.path.suffix:
                page.path = page.path.with_suffix(".yaml")

            if len(page.path.parts) > 1:
                # Relative to document root or absolute path
                page.path = (self.directories.base / page.path).resolve()
            else:
                # Simple string - relative to pages directory
                page.path = page.resolve_relative_to(self.directories.pages).path

        if not self.custom_bake:
            custom_bake_path = self.directories.base / "bake.py"
            if custom_bake_path.is_file():
                self.custom_bake = PathSpec(
                    path=custom_bake_path,
                    name="bake.py",
                )

        return self

    @model_validator(mode="after")
    def check_pages_and_variants(self) -> "DocumentConfig":
        """Check if pages or variants are defined; a variant can't have variants."""
        if self.variants:
            if not self.pages:
                self.log_debug(
                    'Pages of document "%s" will be determined per variant',
                    self.name,
                )
        elif not self.pages:
            if self.is_variant:
                self.log_warning(
                    '"%s" variant "%s" does not define any pages',
                    self.name,
                    self.variant.name,
                )
                raise ConfigurationError(
                    "Cannot determine pages of "
                    f'"{self.name}" variant "{self.variant.name}"'
                )
            self.log_warning('Document "%s" has neither pages nor variants', self.name)
            raise ConfigurationError(
                f'Cannot determine pages of document "{self.name}"'
            )
        if self.is_variant and self.variants:
            raise ConfigurationError(
                f'{self.name} variant "{self.variant.name}" '
                "may not contain variants itself"
            )
        return self

    @model_validator(mode="after")
    def set_variants(self) -> "DocumentConfig":
        """Set variants."""
        valid_variants = []
        for variant_data in self.variants:
            if isinstance(variant_data, dict):
                try:
                    if "name" not in variant_data:
                        raise ValidationError("A document variant needs a name")
                    variant_only_data = variant_data.copy()
                    doc_data = self.variant_settings.copy()
                    if variant_data.get("pages", None):
                        doc_data["pages"] = variant_data["pages"]
                    doc_data["variant"] = variant_data
                    doc_data["variant"]["directories"] = doc_data["directories"]
                    variant = DocumentConfig(**doc_data)
                    # Merge variant data but don't overwrite the document name
                    del variant_only_data["name"]
                    variant = variant.merge(variant_only_data)
                    valid_variants.append(variant)
                except ValidationError as e:
                    logger.warning(
                        "⚠️ Skipping invalid variant '%s': %s",
                        variant_data.get("name"),
                        e,
                    )
            self.variants = valid_variants
        return self

    @property
    def variant_settings(self) -> dict[str, Any]:
        """All configuration settings relevant for a variant."""
        settings = self.model_dump(
            exclude={
                "config_path",
                "variants",
            }
        )
        settings["is_variant"] = True
        return settings

    @property
    def page_settings(self) -> dict[str, Any]:
        """All configuration settings relevant for a page."""
        settings = self.model_dump(
            exclude={
                "config_path",
                "variants",
                "pages",
            }
        )
        settings["directories"]["templates"] = self.resolve_path(
            self.directories.templates
        )
        settings["directories"]["images"] = self.resolve_path(self.directories.images)
        return settings
