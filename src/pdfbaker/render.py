"""Helper functions for rendering with Jinja"""

import base64
import re
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import jinja2

from .types import ImageSpec, StyleDict, ThemeDict

__all__ = [
    "create_env",
    "process_template_data",
]


def process_style(style: StyleDict, theme: ThemeDict) -> StyleDict:
    """Convert style references to actual color values from theme."""
    return_dict: StyleDict = {}
    for key, value in style.items():
        return_dict[key] = theme[value]
    return return_dict


def process_template_data(
    template_data: dict[str, Any],
    defaults: dict[str, Any],
    images_dir: Path | None = None,
) -> dict[str, Any]:
    """Process and enhance template data with styling and images."""
    # Process style first
    if template_data.get("style") is not None:
        default_style = dict(defaults["style"])
        default_style.update(template_data["style"])
        template_data["style"] = default_style
    else:
        template_data["style"] = defaults["style"]

    template_data["style"] = process_style(template_data["style"], defaults["theme"])

    # Process images
    if template_data.get("images") is not None:
        template_data["images"] = encode_images(template_data["images"], images_dir)

    return template_data


class HighlightingTemplate(jinja2.Template):  # pylint: disable=too-few-public-methods
    """A Jinja template that automatically applies highlighting to text.

    This template class extends the base Jinja template to automatically
    process <highlight> tags in the rendered output, converting them to
    styled <tspan> elements with the highlight color.
    """

    def render(self, *args: Any, **kwargs: Any) -> str:
        """Render the template and apply highlighting to the result."""
        rendered = super().render(*args, **kwargs)

        if "style" in kwargs and "highlight_colour" in kwargs["style"]:
            highlight_colour = kwargs["style"]["highlight_colour"]

            def replacer(match: re.Match[str]) -> str:
                content = match.group(1)
                return f'<tspan style="fill:{highlight_colour}">{content}</tspan>'

            rendered = re.sub(r"<highlight>(.*?)</highlight>", replacer, rendered)

        return rendered


def create_env(templates_dir: Path | None = None) -> jinja2.Environment:
    """Create and configure the Jinja environment."""
    if templates_dir is None:
        raise ValueError("templates_dir is required")

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(templates_dir)),
        autoescape=jinja2.select_autoescape(),
        extensions=["jinja2.ext.do"],
    )
    env.template_class = HighlightingTemplate
    return env


def encode_image(filename: str, images_dir: Path) -> str:
    """Encode an image file to a base64 data URI."""
    image_path = images_dir / filename
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    with open(image_path, "rb") as f:
        binary_fc = f.read()
        base64_utf8_str = base64.b64encode(binary_fc).decode("utf-8")
        ext = filename.split(".")[-1]
        return f"data:image/{ext};base64,{base64_utf8_str}"


def encode_images(
    images: Sequence[ImageSpec], images_dir: Path | None
) -> list[ImageSpec]:
    """Encode a list of image specifications to include base64 data."""
    if images_dir is None:
        raise ValueError("images_dir is required when processing images")

    result = []
    for image in images:
        img: ImageSpec = image.copy()
        if img.get("type") is None:
            img["type"] = "default"
        img["data"] = encode_image(img["name"], images_dir)
        result.append(img)
    return result
