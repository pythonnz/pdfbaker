"""Type definitions for pdfbaker."""

from typing import NotRequired, TypedDict

__all__ = [
    "ImageSpec",
    "PathSpec",
    "StyleDict",
]


class _ImageDict(TypedDict):
    """Image specification."""

    name: str
    type: NotRequired[str]
    data: NotRequired[str]


ImageSpec = str | _ImageDict


class StyleDict(TypedDict):
    """Style configuration."""

    highlight_color: NotRequired[str]


class _PathSpecDict(TypedDict):
    """File/Directory location in YAML config."""

    path: NotRequired[str]
    name: NotRequired[str]


PathSpec = str | _PathSpecDict
