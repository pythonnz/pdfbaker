"""Base configuration for pdfbaker classes."""

import logging
import pprint
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Template

from .errors import ConfigurationError
from .logging import truncate_strings
from .types import PathSpec

__all__ = ["PDFBakerConfiguration", "deep_merge", "render_config"]

logger = logging.getLogger(__name__)


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
