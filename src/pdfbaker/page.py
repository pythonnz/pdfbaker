"""Page class.

Individual page rendering and PDF conversion.

Renders its SVG template with a fully merged configuration,
converts the result to PDF and returns the path of the new PDF file.
"""

from pathlib import Path

from jinja2.exceptions import TemplateError, TemplateNotFound

from .config import PathSpec
from .config.page import PageConfig
from .errors import SVGConversionError, SVGTemplateError
from .logging import TRACE, LoggingMixin
from .pdf import convert_svg_to_pdf
from .render import create_env, prepare_template_context

__all__ = ["Page"]


class Page(LoggingMixin):
    """Page class."""

    def __init__(self, config_path: PathSpec, page_number: int, **kwargs):
        self.log_trace_section("Loading page configuration: %s", config_path.name)
        self.config = PageConfig(
            config_path=config_path, page_number=page_number, **kwargs
        )
        self.log_trace(self.config.readable())

    def process(self) -> Path:
        """Render SVG template and convert to PDF."""
        self.log_debug_subsection(
            "Processing page %d: %s", self.config.page_number, self.config.name
        )

        self.log_debug("Loading template: %s", self.config.template.name)
        if self.logger.isEnabledFor(TRACE):
            with open(self.config.template.path, encoding="utf-8") as f:
                self.log_trace_preview(f.read())

        try:
            jinja_extensions = self.config.jinja2_extensions
            if jinja_extensions:
                self.log_debug("Using Jinja2 extensions: %s", jinja_extensions)
            jinja_env = create_env(
                templates_dir=self.config.template.path.parent,
                extensions=jinja_extensions,
                template_filters=[
                    filter.value for filter in self.config.template_filters
                ],
            )
            template = jinja_env.get_template(self.config.template.path.name)
        except TemplateNotFound as exc:
            raise SVGTemplateError(
                "Failed to load template for page "
                f"{self.config.page_number} ({self.config.name}): {exc}"
            ) from exc
        except TemplateError as exc:
            raise SVGTemplateError(
                "Template error for page "
                f"{self.config.page_number} ({self.config.name}): {exc}"
            ) from exc

        context = self.config.resolve_variables().model_dump()
        template_context = prepare_template_context(
            context=context,
            images_dir=self.config.directories.images,
        )

        build_dir = self.config.directories.build
        name = self.config.name
        if self.config.is_variant:
            name = f'{name}_{self.config.variant["name"]}'
        output_svg = build_dir / f"{self.config.page_number:03}_{name}.svg"
        output_pdf = build_dir / f"{self.config.page_number:03}_{name}.pdf"

        self.log_debug("Rendering template...")
        try:
            rendered_template = template.render(
                **template_context,
                renderers=[
                    renderer.value for renderer in self.config.template_renderers
                ],
            )
            with open(output_svg, "w", encoding="utf-8") as f:
                f.write(rendered_template)
        except TemplateError as exc:
            raise SVGTemplateError(
                "Failed to render page "
                f"{self.config.page_number} ({self.config.name}): {exc}"
            ) from exc
        self.log_trace_preview(rendered_template)

        self.log_debug("Converting SVG to PDF: %s", output_svg)
        try:
            return convert_svg_to_pdf(
                output_svg,
                output_pdf,
                backend=self.config.svg2pdf_backend,
            )
        except SVGConversionError as exc:
            self.log_error(
                "Failed to convert page %d (%s): %s",
                self.config.page_number,
                self.config.name,
                exc,
            )
            raise
