"""Type definitions for pdfbaker."""

from pathlib import Path
from typing import Any, NotRequired, TypedDict


class StyleDict(TypedDict):
    """Style configuration."""

    highlight_colour: NotRequired[str]


class ThemeDict(TypedDict):
    """Theme configuration."""

    # Theme can have any color definitions


class ImageSpec(TypedDict):
    """Image specification."""

    name: str
    type: NotRequired[str]
    data: NotRequired[str]


class PageConfig(TypedDict):
    """Page configuration."""

    name: str
    config: dict[str, Any]


class PathsDict(TypedDict):
    """Common paths used throughout the application."""

    doc_dir: Path
    templates_dir: Path
    pages_dir: Path
    images_dir: Path
    build_dir: Path
    dist_dir: Path
