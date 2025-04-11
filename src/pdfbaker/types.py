"""Type definitions for pdfbaker."""

from typing import NotRequired, TypedDict

__all__ = [
    "ImageSpec",
    "StyleDict",
]


class ImageSpec(TypedDict):
    """Image specification."""

    name: str
    type: NotRequired[str]
    data: NotRequired[str]


class StyleDict(TypedDict):
    """Style configuration."""

    highlight_color: NotRequired[str]
