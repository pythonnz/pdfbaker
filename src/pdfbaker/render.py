"""Helper functions for rendering with Jinja"""

import base64
import re
from collections.abc import Sequence
from pathlib import Path
from typing import Any, TypeVar

import jinja2

from .types import ImageSpec, StyleDict, ThemeDict

__all__ = [
    "create_env",
    "process_template_data",
]

# Fields that need line counting for positioning
LINE_COUNT_FIELDS: set[str] = {"text", "title"}

T = TypeVar("T")


def process_style(style: StyleDict, theme: ThemeDict) -> StyleDict:
    """Convert style references to actual color values from theme."""
    return_dict: StyleDict = {}
    for key in style:
        return_dict[key] = theme[style[key]]
    return return_dict


def process_text_with_jinja(
    env: jinja2.Environment, text: str | None, template_data: dict[str, Any]
) -> str | None:
    """Process text through Jinja templating and apply highlighting."""
    if text is None:
        return None

    template = env.from_string(text)
    processed = template.render(**template_data)

    if "style" in template_data and "highlight_colour" in template_data["style"]:

        def replacer(match: re.Match[str]) -> str:
            return (
                f'<tspan style="fill:{template_data["style"]["highlight_colour"]}">'
                f"{match.group(1)}</tspan>"
            )

        processed = re.sub(r"<highlight>(.*?)</highlight>", replacer, processed)

    return processed


def process_list_items(
    list_items: list[dict[str, Any]], template_data: dict[str, Any]
) -> list[dict[str, Any]]:
    """Process a list of text items.

    Applies Jinja templating and calculates positions for SVG layout.
    """
    env = jinja2.Environment()
    previous_lines = 0

    for i, item in enumerate(list_items):
        # Process text fields
        if "text" in item:
            item["text"] = process_text_with_jinja(env, item["text"], template_data)
        if "title" in item:
            item["title"] = process_text_with_jinja(env, item["title"], template_data)

        # Calculate positions for SVG layout
        item["lines"] = previous_lines
        item["position"] = i
        # Count lines from both text and title fields
        for field in LINE_COUNT_FIELDS:
            if item.get(field) is not None:
                previous_lines = item[field].count("\n") + previous_lines + 1

    return list_items


def process_nested_text(template: T, data: dict[str, Any] | None = None) -> T:
    """Process text fields in any nested dictionary or list structure.

    Args:
        template: The template structure to process
        data: Optional data to use for rendering. If None, uses template as data.
    """
    env = jinja2.Environment()
    render_data = data if data is not None else template

    if isinstance(template, dict):
        return {
            key: process_nested_text(value, render_data)
            if isinstance(value, dict | list)
            else process_text_with_jinja(env, value, render_data)
            if isinstance(value, str)
            else value
            for key, value in template.items()
        }  # type: ignore
    if isinstance(template, list):
        return [
            process_nested_text(item, render_data)
            if isinstance(item, dict | list)
            else process_text_with_jinja(env, item, render_data)
            if isinstance(item, str)
            else item
            for item in template
        ]  # type: ignore

    return template


def process_nested_lists(
    data: dict[str, Any] | list[Any], template_data: dict[str, Any]
) -> None:
    """Process any nested lists of items that have text fields."""
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list) and value and isinstance(value[0], dict):
                # Check if any item in the list has text or title fields
                if any("text" in item or "title" in item for item in value):
                    data[key] = process_list_items(value, template_data)
            elif isinstance(value, dict | list):
                process_nested_lists(value, template_data)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict | list):
                process_nested_lists(item, template_data)


def process_template_data(
    template_data: dict[str, Any],
    defaults: dict[str, Any],
    images_dir: Path | None = None,
) -> dict[str, Any]:
    """Process and enhance template data with images, list items, and styling."""
    # Process style first
    if template_data.get("style") is not None:
        default_style = dict(defaults["style"])
        default_style.update(template_data["style"])
        template_data["style"] = default_style
    else:
        template_data["style"] = defaults["style"]

    template_data["style"] = process_style(template_data["style"], defaults["theme"])

    # Process all text fields through Jinja
    template_data = process_nested_text(template_data)

    # Process any nested lists of items that have text fields
    process_nested_lists(template_data, template_data)

    # Process images
    if template_data.get("images") is not None:
        template_data["images"] = encode_images(template_data["images"], images_dir)

    return template_data


def create_env(templates_dir: Path | None = None) -> jinja2.Environment:
    """Create and configure the Jinja environment."""
    if templates_dir is None:
        raise ValueError("templates_dir is required")

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(templates_dir)),
        autoescape=jinja2.select_autoescape(),
    )
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
