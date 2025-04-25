"""Page class.

Individual page rendering and PDF conversion.

Renders its SVG template with a fully merged configuration,
converts the result to PDF and returns the path of the new PDF file.
"""

from pathlib import Path

from jinja2.exceptions import TemplateError, TemplateNotFound

from .config import PageConfig, PathSpec
from .errors import SVGConversionError, SVGTemplateError
from .logging import TRACE, LoggingMixin
from .pdf import convert_svg_to_pdf
from .render import create_env, prepare_template_context

__all__ = ["Page"]


class Page(LoggingMixin):
    """Page class."""

    def __init__(self, config_path: PathSpec, number: int, **kwargs):
        self.log_trace_section("Loading page configuration: %s", config_path.name)
        self.config = PageConfig(config_path=config_path, **kwargs)
        self.number = number
        self.log_trace(self.config.readable())

    def process(self) -> Path:
        """Render SVG template and convert to PDF."""
        self.log_debug_subsection(
            "Processing page %d: %s", self.number, self.config.name
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
                template_filters=self.config.template_filters,
            )
            template = jinja_env.get_template(self.config.template.path.name)
        except TemplateNotFound as exc:
            raise SVGTemplateError(
                "Failed to load template for page "
                f"{self.number} ({self.config.name}): {exc}"
            ) from exc
        except TemplateError as exc:
            raise SVGTemplateError(
                f"Template error for page {self.number} ({self.config.name}): {exc}"
            ) from exc

        template_context = prepare_template_context(
            config=self.config,
            images_dir=self.config.directories.images,
        )
        # FIXME: should just be in PageConfig
        template_context["page_number"] = self.number

        build_dir = self.config.directories.build
        build_dir.mkdir(parents=True, exist_ok=True)
        output_svg = build_dir / f"{self.config.name}_{self.number:03}.svg"
        output_pdf = build_dir / f"{self.config.name}_{self.number:03}.pdf"

        self.log_debug("Rendering template...")
        try:
            rendered_template = template.render(
                **template_context,
                renderers=self.config.template_renderers,
            )
            with open(output_svg, "w", encoding="utf-8") as f:
                f.write(rendered_template)
        except TemplateError as exc:
            raise SVGTemplateError(
                f"Failed to render page {self.number} ({self.config.name}): {exc}"
            ) from exc
        self.log_trace_preview(rendered_template)

        self.log_debug("Converting SVG to PDF: %s", output_svg)
        try:
            return convert_svg_to_pdf(
                output_svg,
                output_pdf,
                backend=self.config.svg2pdf_backend.value,
            )
        except SVGConversionError as exc:
            self.log_error(
                "Failed to convert page %d (%s): %s",
                self.number,
                self.config.name,
                exc,
            )
            raise
