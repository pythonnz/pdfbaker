"""Classes and functions used for rendering with Jinja"""

import base64
import re
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import jinja2

from .types import ImageSpec, StyleDict

__all__ = [
    "create_env",
    "prepare_template_context",
]


class HighlightingTemplate(jinja2.Template):  # pylint: disable=too-few-public-methods
    """A Jinja template that automatically applies highlighting to text.

    This template class extends the base Jinja template to automatically
    convert <highlight> tags to styled <tspan> elements with the highlight color.
    """

    def render(self, *args: Any, **kwargs: Any) -> str:
        """Render the template and apply highlighting to the result."""
        rendered = super().render(*args, **kwargs)

        if "style" in kwargs and "highlight_color" in kwargs["style"]:
            highlight_color = kwargs["style"]["highlight_color"]

            def replacer(match: re.Match[str]) -> str:
                content = match.group(1)
                return f'<tspan style="fill:{highlight_color}">{content}</tspan>'

            rendered = re.sub(r"<highlight>(.*?)</highlight>", replacer, rendered)

        return rendered


def create_env(templates_dir: Path | None = None) -> jinja2.Environment:
    """Create and configure the Jinja environment."""
    if templates_dir is None:
        raise ValueError("templates_dir is required")

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(templates_dir)),
        autoescape=jinja2.select_autoescape(),
        # FIXME: extensions configurable
        extensions=["jinja2.ext.do"],
    )
    env.template_class = HighlightingTemplate
    return env


def prepare_template_context(
    config: dict[str], images_dir: Path | None = None
) -> dict[str]:
    """Prepare config for template rendering by resolving styles and encoding images.

    Args:
        config: Configuration with optional styles and images
        images_dir: Directory containing images to encode
    """
    context = config.copy()

    # Resolve style references to actual theme colors
    if "style" in context and "theme" in context:
        style = context["style"]
        theme = context["theme"]
        resolved_style: StyleDict = {}
        for key, value in style.items():
            resolved_style[key] = theme[value]
        context["style"] = resolved_style

    # Process image references
    if context.get("images") is not None:
        context["images"] = encode_images(context["images"], images_dir)

    return context


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
