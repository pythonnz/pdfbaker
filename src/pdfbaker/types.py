"""Type definitions for pdfbaker."""

from typing import NotRequired, TypedDict

__all__ = [
    "ImageSpec",
    "StyleDict",
]


class ImageDict(TypedDict):
    """Image specification."""

    name: str
    type: NotRequired[str]
    data: NotRequired[str]


ImageSpec = str | ImageDict


class StyleDict(TypedDict):
    """Style configuration."""

    highlight_color: NotRequired[str]
