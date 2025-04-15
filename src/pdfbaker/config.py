"""Base configuration for pdfbaker classes."""

import logging
import pprint
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Template

from .errors import ConfigurationError
from .types import PathSpec

__all__ = ["PDFBakerConfiguration"]

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


def _truncate_strings(obj, max_length: int) -> Any:
    """Recursively truncate strings in nested structures."""
    if isinstance(obj, str):
        return obj if len(obj) <= max_length else obj[:max_length] + "…"
    if isinstance(obj, dict):
        return {
            _truncate_strings(k, max_length): _truncate_strings(v, max_length)
            for k, v in obj.items()
        }
    if isinstance(obj, list):
        return [_truncate_strings(item, max_length) for item in obj]
    if isinstance(obj, tuple):
        return tuple(_truncate_strings(item, max_length) for item in obj)
    if isinstance(obj, set):
        return {_truncate_strings(item, max_length) for item in obj}
    return obj


class PDFBakerConfiguration(dict):
    """Base  class for handling config loading/merging/parsing."""

    def __init__(
        self,
        base_config: dict[str, Any],
        config: Path,
    ) -> None:
        """Initialize configuration from a file.

        Args:
            base_config: Existing base configuration
            config: Path to YAML file to merge with base_config
        """
        self.directory = config.parent
        super().__init__(deep_merge(base_config, self._load_config(config)))

    def _load_config(self, config_file: Path) -> dict[str, Any]:
        """Load configuration from a file."""
        try:
            with open(config_file, encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception as exc:
            raise ConfigurationError(f"Failed to load config file: {exc}") from exc

    def resolve_path(self, spec: PathSpec, directory: Path | None = None) -> Path:
        """Resolve a possibly relative path specification.

        Args:
            spec: Path specification (string or dict with path/name)
            directory: Optional directory to use for resolving paths
        Returns:
            Resolved Path object
        """
        directory = directory or self.directory
        if isinstance(spec, str):
            return directory / spec

        if "path" not in spec and "name" not in spec:
            raise ConfigurationError("Invalid path specification: needs path or name")

        if "path" in spec:
            return Path(spec["path"])

        return directory / spec["name"]

    def render(self) -> dict[str, Any]:
        """Resolve all template strings in config using its own values.

        This allows the use of "{{ variant }}" in the "filename" etc.

        Returns:
            Resolved configuration dictionary

        Raises:
            ConfigurationError: If maximum number of iterations is reached
                (circular references)
        """
        max_iterations = 10
        config = self
        for _ in range(max_iterations):
            config_yaml = Template(yaml.dump(config))
            resolved_yaml = config_yaml.render(**config)
            new_config = yaml.safe_load(resolved_yaml)

            if new_config == config:  # No more changes
                return new_config
            config = new_config

        raise ConfigurationError(
            "Maximum number of iterations reached. "
            "Check for circular references in your configuration."
        )

    def pprint(self, max_string=60) -> str:
        """Pretty print a configuration dictionary (for debugging)."""
        truncated = _truncate_strings(self, max_string)
        return pprint.pformat(truncated, indent=2)
