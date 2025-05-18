"""Classes and functions used for rendering with Jinja"""

import base64
import re
from collections.abc import Sequence
from enum import Enum
from pathlib import Path
from typing import Any

import jinja2

from . import processing
from .config import ImageSpec

__all__ = [
    "create_env",
    "PDFBakerTemplate",
    "prepare_template_context",
]


class PDFBakerTemplate(jinja2.Template):  # pylint: disable=too-few-public-methods
    """A Jinja template with custom rendering capabilities for pdfbaker.

    This template class extends the base Jinja template to apply
    additional rendering transformations to the template output.
    """

    def render(self, *args: Any, **kwargs: Any) -> str:
        """Render the template and apply custom transformations.

        Args:
            *args: Positional arguments for template rendering
            **kwargs: Keyword arguments for template rendering
                renderers: Optional list of renderer function names to apply

        Returns:
            Rendered template with transformations applied
        """
        rendered = super().render(*args, **kwargs)

        for renderer_name in kwargs.get("renderers", []):
            renderer_func = globals().get(renderer_name)
            if callable(renderer_func):
                rendered = renderer_func(rendered, **kwargs)

        return rendered


def render_highlight(rendered: str, **kwargs: Any) -> str:
    """
    Apply highlight tags to the rendered template content.

    Recursively convert all <highlight> tags to styled <tspan> elements
    with the highlight color from the `style.highlight_color` setting.
    """
    if "style" in kwargs and "highlight_color" in kwargs["style"]:
        highlight_color = kwargs["style"]["highlight_color"]

        pattern = re.compile(r"<highlight>(.*?)</highlight>", re.DOTALL)

        def replacer(match: re.Match[str]) -> str:
            # Recursively process the content for nested highlights
            content = render_highlight(match.group(1), **kwargs)
            return f'<tspan style="fill:{highlight_color}">{content}</tspan>'

        # Keep replacing until no more <highlight> tags are found
        while pattern.search(rendered):
            rendered = pattern.sub(replacer, rendered)

    return rendered


class PDFBakerUndefined(jinja2.Undefined):
    """Custom Undefined that collects undefined variable names and template file."""

    def __init__(self, *args, undefined_vars=None, template_file=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._undefined_vars = undefined_vars
        self._template_file = template_file
        if self._undefined_vars is not None and self._undefined_name is not None:
            self._undefined_vars.add((self._undefined_name, self._template_file))

    def _fail_with_undefined_error(self, *args, **kwargs):
        if self._undefined_vars is not None and self._undefined_name is not None:
            self._undefined_vars.add((self._undefined_name, self._template_file))
        return ""

    def __str__(self):
        return self._fail_with_undefined_error()

    def __getattr__(self, name):
        return self._fail_with_undefined_error()

    def __call__(self, *args, **kwargs):
        return self._fail_with_undefined_error()

    def __iter__(self):
        # Allows {% for ... in ... %} to not fail
        self._fail_with_undefined_error()
        return iter([])

    def __bool__(self):
        # Allows {% if ... %} to not fail
        self._fail_with_undefined_error()
        return False

    def __len__(self):
        self._fail_with_undefined_error()
        return 0

    def __getitem__(self, key):
        # Allows {{ ...[0].something }} to not fail
        return self._fail_with_undefined_error()


def create_env(
    templates_dir: Path | None = None,
    extensions: list[str] | None = None,
    template_filters: list[str] | None = None,
    undefined_vars: set | None = None,
    template_file: str | None = None,
) -> jinja2.Environment:
    """Create and configure the Jinja environment.

    Args:
        templates_dir: Directory containing templates
        extensions: List of Jinja2 extensions
        template_filters: List of template filter names
        undefined_vars: Set to collect (var, template_file) tuples for undefined vars
        template_file: Name of the template file being rendered (for error reporting)
    """
    if templates_dir is None:
        raise ValueError("templates_dir is required")

    # pylint: disable=too-few-public-methods
    class CustomUndefined(PDFBakerUndefined):
        """Undefined class that collects undefined variables per template."""

        def __init__(self, *args, **kwargs):
            super().__init__(
                *args,
                undefined_vars=undefined_vars,
                template_file=template_file,
                **kwargs,
            )

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(templates_dir)),
        autoescape=jinja2.select_autoescape(),
        extensions=extensions or [],
        undefined=CustomUndefined,
    )
    env.template_class = PDFBakerTemplate

    if template_filters:
        for filter_spec in template_filters:
            filter_name = (
                filter_spec.value if isinstance(filter_spec, Enum) else filter_spec
            )
            if hasattr(processing, filter_name):
                env.filters[filter_name] = getattr(processing, filter_name)

    return env


def prepare_template_context(
    context: dict[str], images_dir: Path | None = None
) -> dict[str]:
    """Encode images for template context

    Args:
        config: Configuration with optional images
        images_dir: Directory containing images to encode
    """
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
