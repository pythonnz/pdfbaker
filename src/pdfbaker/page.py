"""PDFBakerPage class.

Individual page rendering and PDF conversion.

Renders its SVG template with a fully merged configuration,
converts the result to PDF and returns the path of the new PDF file.
"""

from pathlib import Path
from typing import Any

from jinja2.exceptions import TemplateError, TemplateNotFound

from .config import PDFBakerConfiguration
from .errors import ConfigurationError, SVGConversionError, SVGTemplateError
from .logging import TRACE, LoggingMixin
from .pdf import convert_svg_to_pdf
from .render import create_env, prepare_template_context

__all__ = ["PDFBakerPage"]


# pylint: disable=too-few-public-methods
class PDFBakerPage(LoggingMixin):
    """A single page of a document."""

    class Configuration(PDFBakerConfiguration):
        """PDFBakerPage configuration."""

        def __init__(
            self,
            page: "PDFBakerPage",
            base_config: dict[str, Any],
            config_path: Path,
        ) -> None:
            """Initialize page configuration (needs a template)."""
            self.page = page

            self.name = config_path.stem

            self.page.log_trace_section("Loading page configuration: %s", config_path)
            super().__init__(base_config, config_path)
            self.page.log_trace(self.pretty())

            self.templates_dir = self["directories"]["templates"]
            self.images_dir = self["directories"]["images"]
            self.build_dir = page.document.config.build_dir
            self.dist_dir = page.document.config.dist_dir

            if "template" not in self:
                raise ConfigurationError(
                    f'Page "{self.name}" in document '
                    f'"{self.page.document.config.name}" has no template'
                )
            if isinstance(self["template"], dict) and "path" in self["template"]:
                # Path was specified: relative to the config file
                self.template = self.resolve_path(
                    self["template"]["path"], directory=self["directories"]["config"]
                ).resolve()
            else:
                # Only name was specified: relative to the templates directory
                self.template = self.resolve_path(
                    self["template"], directory=self.templates_dir
                ).resolve()

    def __init__(
        self,
        document: "PDFBakerDocument",  # type: ignore # noqa: F821
        page_number: int,
        base_config: dict[str, Any],
        config_path: Path | dict[str, Any],
    ) -> None:
        """Initialize a page."""
        super().__init__()
        self.document = document
        self.number = page_number
        self.config = self.Configuration(
            page=self,
            base_config=base_config,
            config_path=config_path,
        )

    def process(self) -> Path:
        """Render SVG template and convert to PDF."""
        self.log_debug_subsection(
            "Processing page %d: %s", self.number, self.config.name
        )

        self.log_debug("Loading template: %s", self.config.template)
        if self.logger.isEnabledFor(TRACE):
            with open(self.config.template, encoding="utf-8") as f:
                self.log_trace_preview(f.read())

        try:
            jinja_env = create_env(self.config.template.parent)
            template = jinja_env.get_template(self.config.template.name)
        except TemplateNotFound as exc:
            raise SVGTemplateError(
                "Failed to load template for page "
                f"{self.number} ({self.config.name}): {exc}"
            ) from exc

        template_context = prepare_template_context(
            self.config,
            self.config.images_dir,
        )

        self.config.build_dir.mkdir(parents=True, exist_ok=True)
        output_svg = self.config.build_dir / f"{self.config.name}_{self.number:03}.svg"
        output_pdf = self.config.build_dir / f"{self.config.name}_{self.number:03}.pdf"

        self.log_debug("Rendering template...")
        try:
            rendered_template = template.render(**template_context)
            with open(output_svg, "w", encoding="utf-8") as f:
                f.write(rendered_template)
        except TemplateError as exc:
            raise SVGTemplateError(
                f"Failed to render page {self.number} ({self.config.name}): {exc}"
            ) from exc
        self.log_trace_preview(rendered_template)

        self.log_debug("Converting SVG to PDF: %s", output_svg)
        svg2pdf_backend = self.config.get("svg2pdf_backend", "cairosvg")
        try:
            return convert_svg_to_pdf(
                output_svg,
                output_pdf,
                backend=svg2pdf_backend,
            )
        except SVGConversionError as exc:
            self.log_error(
                "Failed to convert page %d (%s): %s",
                self.number,
                self.config.name,
                exc,
            )
            raise
