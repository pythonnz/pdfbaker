"""Page configuration for pdfbaker."""

from typing import Any

from pydantic import computed_field, model_validator
from ruamel.yaml import YAML

from . import (
    BaseConfig,
    PathSpec,
)


class PageConfig(BaseConfig):
    """Page configuration."""

    config_path: PathSpec
    page_number: int
    template: PathSpec

    @model_validator(mode="before")
    @classmethod
    def load_config(cls, data: Any) -> Any:
        """Load page configuration from YAML file."""
        if isinstance(data, dict) and "config_path" in data:
            if isinstance(data["config_path"], dict):
                data["config_path"] = PathSpec(**data["config_path"])
            config_data = YAML().load(data["config_path"].path.read_text())
            data.update(config_data)  # YAML values override kwargs
            data["directories"]["base"] = data["config_path"].path.parent
        return data

    @model_validator(mode="after")
    def resolve_paths(self) -> "PageConfig":
        """Resolve relative paths."""
        if len(self.template.path.parts) > 1:
            # Relative to pages root or absolute path
            self.template.path = (self.directories.base / self.template.path).resolve()
        else:
            # Simple string - relative to templates directory
            templates_dir = self.resolve_path(self.directories.templates)
            self.template.path = self.template.resolve_relative_to(templates_dir).path
        self.template.name = self.template.path.name  # not just stem
        return self

    @computed_field
    @property
    def name(self) -> str:
        """Return the name of this page."""
        return self.config_path.path.stem
