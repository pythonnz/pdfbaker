"""PDFBakerPage class.

Individual page rendering and PDF conversion.

Renders its SVG template with a fully merged configuration,
converts the result to PDF and returns the path of the new PDF file.
"""

from pathlib import Path
from typing import Any

from jinja2.exceptions import TemplateError

from .config import PDFBakerConfiguration
from .errors import ConfigurationError, SVGConversionError
from .pdf import convert_svg_to_pdf
from .render import create_env, prepare_template_context

__all__ = ["PDFBakerPage"]


class PDFBakerPage:
    """A single page of a document."""

    class Configuration(PDFBakerConfiguration):
        """PDFBakerPage configuration."""
        def __init__(
                self,
                base_config: dict[str, Any],
                config: Path,
                page: "PDFBakerPage",
            ) -> None:
            """Initialize page configuration (needs a template)."""
            self.page = page
            # FIXME: config is usually pages/mypage.yaml
            self.name = "TBC"
            super().__init__(base_config, config)
            self.page.document.baker.debug("Page config for %s:", self.name)
            self.page.document.baker.debug(self.pprint())
            if "template" not in self:
                raise ConfigurationError(
                    f'Page "{self.name}" in document '
                    f'"{self.page.document.config.name}" has no template'
                )
            self.templates_dir = self.resolve_path(
                self["templates_dir"],
                directory=self.page.document.config.directory,
            )
            self.template = self.resolve_path(
                self["template"],
                directory=self.templates_dir,
            )
            self.images_dir = self.resolve_path(
                self["images_dir"],
                directory=self.page.document.config.directory,
            )
            self.build_dir = self.resolve_path(self["build_dir"])

    def __init__(
        self,
        document: "PDFBakerDocument",  # type: ignore # noqa: F821
        page_number: int,
        base_config: dict[str, Any],
        config: Path | dict[str, Any],
    ) -> None:
        """Initialize a page."""
        self.document = document
        self.number = page_number
        self.config = self.Configuration(
            base_config=base_config,
            config=config,
            page=self,
        )

    def process(self) -> Path:
        """Render SVG template and convert to PDF."""
        self.config.build_dir.mkdir(parents=True, exist_ok=True)
        output_svg = self.config.build_dir / f"{self.config.name}_{self.number:03}.svg"
        output_pdf = self.config.build_dir / f"{self.config.name}_{self.number:03}.pdf"

        jinja_env = create_env(self.config.template.parent)
        template = jinja_env.get_template(self.config["template"])
        template_context = prepare_template_context(
            self.config,
            self.config.images_dir,
        )

        try:
            with open(output_svg, "w", encoding="utf-8") as f:
                f.write(template.render(**template_context))
        except TemplateError as exc:
            self.document.baker.error(
                "Failed to render page %d (%s): %s",
                self.number,
                self.config.name,
                exc,
            )
            raise

        svg2pdf_backend = self.config.get("svg2pdf_backend", "cairosvg")
        try:
            return convert_svg_to_pdf(
                output_svg,
                output_pdf,
                backend=svg2pdf_backend,
            )
        except SVGConversionError as exc:
            self.document.baker.error(
                "Failed to convert page %d (%s): %s",
                self.number,
                self.config.name,
                exc,
            )
            raise
