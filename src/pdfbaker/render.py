"""Helper functions for rendering with Jinja"""

import base64
import os
import re

import jinja2

__all__ = [
    "process_template_data",
    "create_env",
]


def highlight(text, style=None):
    """Replaces <highlight>text</highlight> with highlighted tspan elements."""
    if not text:
        return text

    if not style or "highlight_colour" not in style:
        raise ValueError(
            "highlight_colour must be configured in style to use <highlight> tags"
        )

    def replacer(match):
        return (
            f'<tspan style="fill:{style["highlight_colour"]}">{match.group(1)}</tspan>'
        )

    return re.sub(r"<highlight>(.*?)</highlight>", replacer, text)


def process_style(style, theme):
    """Convert style references to actual color values from theme."""
    return_dict = {}
    for key in style:
        return_dict[key] = theme[style[key]]
    return return_dict


def process_text_with_jinja(env, text, template_data):
    """Process text through Jinja templating."""
    if text is None:
        return None

    template = env.from_string(text)
    processed = template.render(**template_data)
    if "style" in template_data:
        processed = highlight(processed, template_data["style"])
    return processed


def process_list_item_texts(env, items, template_data):
    """Process text fields in list items through Jinja."""
    for item in items:
        if "text" in item:
            item["text"] = process_text_with_jinja(env, item["text"], template_data)
        if "title" in item:
            item["title"] = process_text_with_jinja(env, item["title"], template_data)
    return items


def process_list_items(list_items):
    """Process a list of text items to calculate line positions."""
    previous_lines = 0
    for i, item in enumerate(list_items):
        item["lines"] = previous_lines
        item["position"] = i
        if item.get("text") is not None:
            previous_lines = item["text"].count("\n") + previous_lines + 1
    return list_items


def process_template_data(template_data, defaults, images_dir=None):
    """Process and enhance template data with images, list items, and styling."""
    # Process style first
    if template_data.get("style") is not None:
        default_style = dict(defaults["style"])
        default_style.update(template_data["style"])
        template_data["style"] = default_style
    else:
        template_data["style"] = defaults["style"]

    template_data["style"] = process_style(template_data["style"], defaults["theme"])

    # Create single Jinja environment for all text processing
    env = jinja2.Environment()

    # Process all text fields through Jinja
    for key in template_data:
        if (key == "text" or key.startswith("text_")) and template_data[
            key
        ] is not None:
            template_data[key] = process_text_with_jinja(
                env, template_data[key], template_data
            )

    # Process list items
    if template_data.get("list_items") is not None:
        template_data["list_items"] = process_list_item_texts(
            env, template_data["list_items"], template_data
        )
        template_data["list_items"] = process_list_items(template_data["list_items"])

    if template_data.get("specs_items") is not None:
        template_data["specs_items"] = process_list_item_texts(
            env, template_data["specs_items"], template_data
        )
        template_data["specs_items"] = process_list_items(template_data["specs_items"])

    # Process images
    if template_data.get("images") is not None:
        template_data["images"] = encode_images(template_data["images"], images_dir)

    return template_data


def create_env(templates_dir=None):
    """Create and configure the Jinja environment."""
    if templates_dir is None:
        raise ValueError("templates_dir is required")

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(templates_dir)),
        autoescape=jinja2.select_autoescape(),
    )
    env.filters["space_bullets"] = space_bullets
    return env


def space_bullets(text):
    """Add spacing after each bullet point while preserving line formatting."""
    if not text:
        return text

    lines = text.split("\n")
    result = []

    for i, line in enumerate(lines):
        if line.strip().startswith("•"):
            if i > 0 and not lines[i - 1].strip() == "":
                result.append("")
            result.append(line)
        else:
            result.append(line)

    return "\n".join(result)


def encode_image(filename, images_dir):
    """Encode an image file to a base64 data URI."""
    image_path = os.path.join(images_dir, filename)
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    with open(image_path, "rb") as f:
        binary_fc = f.read()
        base64_utf8_str = base64.b64encode(binary_fc).decode("utf-8")
        ext = filename.split(".")[-1]
        return f"data:image/{ext};base64,{base64_utf8_str}"


def encode_images(images, images_dir):
    """Encode a list of image specifications to include base64 data."""
    for image in images:
        if image.get("type") is None:
            image["type"] = "default"
        image["data"] = encode_image(image["name"], images_dir)
    return images
