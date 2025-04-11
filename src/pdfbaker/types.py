"""Type definitions for pdfbaker."""

from typing import NotRequired, TypedDict


class StyleDict(TypedDict):
    """Style configuration."""

    highlight_color: NotRequired[str]


class ImageSpec(TypedDict):
    """Image specification."""

    name: str
    type: NotRequired[str]
    data: NotRequired[str]
