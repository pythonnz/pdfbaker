"""Document processing classes."""

import importlib
import os
from pathlib import Path
from typing import Any

import yaml

from .common import (
    combine_pdfs,
    compress_pdf,
    convert_svg_to_pdf,
    deep_merge,
    resolve_config,
)
from .errors import (
    PDFBakeError,
    PDFCombineError,
    PDFCompressionError,
    SVGConversionError,
)
from .render import create_env, prepare_template_context

__all__ = [
    "PDFBakerDocument",
    "PDFBakerPage",
]


class PDFBakerPage:  # pylint: disable=too-few-public-methods
    """A single page of a document."""

    def __init__(
        self,
        document: "PDFBakerDocument",
        name: str,
        number: int,
        config: dict[str, Any] | None = None,
    ) -> None:
        """Initialize a page.

        Args:
            document: Parent PDFBakerDocument instance
            name: Name of the page
            number: Page number (for output filename)
            config: Optional variant-specific config to use instead of document config
        """
        self.document = document
        self.name = name
        self.number = number
        base_config = config or document.config
        config_path = document.doc_dir / "pages" / f"{name}.yml"
        self.config = self._load_config(config_path, base_config)

    def _load_config(
        self, config_path: Path, base_config: dict[str, Any]
    ) -> dict[str, Any]:
        """Load and merge page configuration with document configuration."""
        try:
            with open(config_path, encoding="utf-8") as f:
                page_config = yaml.safe_load(f)
                return deep_merge(base_config, page_config)
        except Exception as exc:
            raise PDFBakeError(f"Failed to load page config file: {exc}") from exc

    def process(self) -> Path:
        """Process the page from SVG template to PDF."""
        if "template" not in self.config:
            raise PDFBakeError(
                f'Page "{self.name}" in document "{self.document.name}" has no template'
            )

        # Resolve any templates in the config
        self.config = resolve_config(self.config)

        output_filename = f"{self.config['filename']}_{self.number:03}"
        svg_path = self.document.build_dir / f"{output_filename}.svg"
        pdf_path = self.document.build_dir / f"{output_filename}.pdf"

        template = self.document.jinja_env.get_template(self.config["template"])
        template_context = prepare_template_context(
            self.config, images_dir=self.document.doc_dir / "images"
        )
        template_context["page_number"] = self.number

        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(template.render(**template_context))

        svg2pdf_backend = self.config.get("svg2pdf_backend", "cairosvg")
        try:
            return convert_svg_to_pdf(
                svg_path,
                pdf_path,
                backend=svg2pdf_backend,
            )
        except SVGConversionError as exc:
            self.document.baker.error(
                "Failed to convert page %d (%s): %s",
                self.number,
                self.name,
                exc,
            )
            raise


class PDFBakerDocument:
    """A document being processed."""

    def __init__(
        self,
        name: str,
        doc_dir: Path,
        baker: "PDFBaker",  # noqa: F821
    ) -> None:
        """Initialize a document.

        Args:
            name: Document name
            doc_dir: Path to document directory
            baker: PDFBaker instance that owns this document
        """
        self.name = name
        self.doc_dir = doc_dir
        self.baker = baker
        self.config = self._load_config()
        self.jinja_env = create_env(doc_dir / "templates")
        self.build_dir = baker.build_dir / name
        self.dist_dir = baker.dist_dir / name

    def _load_config(self) -> dict[str, Any]:
        """Load and merge document configuration."""
        config_path = self.doc_dir / "config.yml"
        try:
            with open(config_path, encoding="utf-8") as f:
                doc_config = yaml.safe_load(f)
            return deep_merge(self.baker.config, doc_config)
        except Exception as exc:
            raise PDFBakeError(f"Failed to load config file: {exc}") from exc

    def setup_directories(self) -> None:
        """Set up output directories."""
        self.build_dir.mkdir(parents=True, exist_ok=True)
        self.dist_dir.mkdir(parents=True, exist_ok=True)

        # Clean existing files
        for dir_path in [self.build_dir, self.dist_dir]:
            for file in os.listdir(dir_path):
                file_path = dir_path / file
                if os.path.isfile(file_path):
                    os.remove(file_path)

    def process_document(self) -> None:
        """Process the document - use custom bake module if it exists."""
        self.baker.info('Processing document "%s" from %s...', self.name, self.doc_dir)

        # Try to load custom bake module
        bake_path = self.doc_dir / "bake.py"
        if bake_path.exists():
            self._process_with_custom_bake(bake_path)
        else:
            self.process()

    def process(self) -> None:
        """Process document using standard processing."""
        doc_config = self.config.copy()

        if "variants" in self.config:
            # Multiple PDF documents
            for variant in self.config["variants"]:
                self.baker.info("Processing variant: %s", variant["name"])
                variant_config = deep_merge(doc_config, variant)
                variant_config["variant"] = variant
                variant_config = resolve_config(variant_config)
                self._process_pages(variant_config)
        else:
            # Single PDF document
            doc_config = resolve_config(doc_config)
            self._process_pages(doc_config)

    def _process_pages(self, config: dict[str, Any]) -> None:
        """Process pages with given configuration."""
        pages = config.get("pages", [])
        if not pages:
            raise PDFBakeError("No pages defined in config")

        pdf_files = []
        for page_num, page_name in enumerate(pages, start=1):
            page = PDFBakerPage(
                document=self,
                name=page_name,
                number=page_num,
                config=config,
            )
            pdf_files.append(page.process())

        self._finalize(pdf_files, config)

    def _process_with_custom_bake(self, bake_path: Path) -> None:
        """Process document using custom bake module."""
        try:
            spec = importlib.util.spec_from_file_location(
                f"documents.{self.name}.bake", bake_path
            )
            if spec is None or spec.loader is None:
                raise PDFBakeError(
                    f"Failed to load bake module for document {self.name}"
                )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.process_document(document=self)
        except Exception as exc:
            raise PDFBakeError(
                f"Failed to process document with custom bake: {exc}"
            ) from exc

    def _finalize(self, pdf_files: list[Path], config: dict[str, Any]) -> None:
        """Combine pages and handle compression."""
        try:
            combined_pdf = combine_pdfs(
                pdf_files,
                self.build_dir / f"{config['filename']}.pdf",
            )
        except PDFCombineError as exc:
            raise PDFBakeError(f"Failed to combine PDFs: {exc}") from exc

        output_path = self.dist_dir / f"{config['filename']}.pdf"

        if config.get("compress_pdf", False):
            try:
                compress_pdf(combined_pdf, output_path)
                self.baker.info("PDF compressed successfully")
            except PDFCompressionError as exc:
                self.baker.warning(
                    "Compression failed, using uncompressed version: %s",
                    exc,
                )
                os.rename(combined_pdf, output_path)
        else:
            os.rename(combined_pdf, output_path)
