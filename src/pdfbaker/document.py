"""PDFBakerDocument class.

Document-level processing, variants, custom bake modules.

Delegates the jobs of rendering and converting to its pages,
combines and compresses the result and reports back to its baker.
"""

import importlib
import os
from pathlib import Path
from typing import Any

import jinja2

from .config import (
    PDFBakerConfiguration,
    deep_merge,
)
from .errors import (
    ConfigurationError,
    PDFBakerError,
    PDFCombineError,
    PDFCompressionError,
)
from .logging import LoggingMixin
from .page import PDFBakerPage
from .pdf import (
    combine_pdfs,
    compress_pdf,
)

DEFAULT_DOCUMENT_CONFIG_FILE = "config.yaml"

__all__ = ["PDFBakerDocument"]


class PDFBakerDocument(LoggingMixin):
    """A document being processed."""

    class Configuration(PDFBakerConfiguration):
        """PDFBaker document-specific configuration."""

        def __init__(
            self,
            base_config: "PDFBakerConfiguration",  # type: ignore # noqa: F821
            config: Path,
            document: "PDFBakerDocument",
        ) -> None:
            """Initialize document configuration.

            Args:
                base_config: The PDFBaker configuration to merge with
                config_file: The document configuration (YAML file)
            """
            self.document = document
            self.document.log_debug_subsection("Parsing document config: %s", config)
            if config.is_dir():
                self.name = config.name
                config = config / DEFAULT_DOCUMENT_CONFIG_FILE
            else:
                self.name = config.stem
            self.directory = config.parent
            self.document.log_trace(self.pretty())
            self.document.log_debug_section(
                'Merging document config for "%s"...', self.name
            )
            super().__init__(base_config, config)
            self.document.log_trace(self.pretty())
            self.document.log_debug_subsection("Document config for %s:", self.name)
            if "pages" not in self:
                raise ConfigurationError(
                    'Document "{document.name}" is missing key "pages"'
                )
            self.pages_dir = self.resolve_path(self["pages_dir"])
            self.pages = []
            for page_spec in self["pages"]:
                page = self.resolve_path(page_spec, directory=self.pages_dir)
                if not page.suffix:
                    page = page.with_suffix(".yaml")
                self.pages.append(page)
            self.build_dir = self.resolve_path(self["build_dir"])
            self.dist_dir = self.resolve_path(self["dist_dir"])
            self.document.log_trace(self.pretty())

    def __init__(
        self,
        baker: "PDFBaker",  # type: ignore # noqa: F821
        base_config: dict[str, Any],
        config: Path,
    ):
        """Initialize a document."""
        super().__init__()
        self.baker = baker
        self.config = self.Configuration(base_config, config, document=self)

    def process_document(self) -> tuple[Path | list[Path] | None, str | None]:
        """Process the document - use custom bake module if it exists.

        Returns:
            Tuple of (pdf_files, error_message) where:
            - pdf_files is a Path or list of Paths to the created PDF
              files, or None if creation failed
            FIXME: could have created SOME PDF files
            - error_message is a string describing the error, or None if successful
        """
        self.log_info_section('Processing document "%s"...', self.config.directory.name)

        self.config.build_dir.mkdir(parents=True, exist_ok=True)
        self.config.dist_dir.mkdir(parents=True, exist_ok=True)

        bake_path = self.config.directory / "bake.py"
        if bake_path.exists():
            # Custom (pre-)processing
            try:
                return self._process_with_custom_bake(bake_path), None
            except PDFBakerError as exc:
                return None, str(exc)
        else:
            # Standard processing
            try:
                return self.process(), None
            except (PDFBakerError, jinja2.exceptions.TemplateError) as exc:
                return None, str(exc)

    def _process_with_custom_bake(self, bake_path: Path) -> Path | list[Path]:
        """Process document using custom bake module."""
        try:
            spec = importlib.util.spec_from_file_location(
                f"documents.{self.config.name}.bake", bake_path
            )
            if spec is None or spec.loader is None:
                raise PDFBakerError(
                    f"Failed to load bake module for document {self.config.name}"
                )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module.process_document(document=self)
        except Exception as exc:
            raise PDFBakerError(
                f"Failed to process document with custom bake: {exc}"
            ) from exc

    def process(self) -> Path | list[Path]:
        """Process document using standard processing.

        FIXME: don't mix up who gets what - there's still a page config
        PDFBaker and PDFBakerDocument load and merge their config
        file upong initialization, but a PDFBakerPage is initialized with
        an already merged config, so that we can provide different
        configs for different variants.
        """
        doc_config = self.config.copy()

        if "variants" in self.config:
            # Multiple PDF documents
            pdf_files = []
            for variant in self.config["variants"]:
                self.log_info_subsection('Processing variant "%s"...', variant["name"])
                variant_config = deep_merge(doc_config, variant)
                variant_config["variant"] = variant
                # variant_config = deep_merge(variant_config, self.config)
                page_pdfs = self._process_pages(variant_config)
                pdf_files.append(self._combine_and_compress(page_pdfs, variant_config))
            return pdf_files

        # Single PDF document
        page_pdfs = self._process_pages(doc_config)
        # doc_config = doc_config.render()
        return self._combine_and_compress(page_pdfs, doc_config)

    def _process_pages(self, config: dict[str, Any]) -> list[Path]:
        """Process pages with given configuration."""
        pdf_files = []
        for page_num, page in enumerate(self.config.pages, start=1):
            # FIXME: just call with config - already merged
            page = PDFBakerPage(
                document=self,
                page_number=page_num,
                base_config=config,
                config=page,
            )
            pdf_files.append(page.process())

        return pdf_files

    def _combine_and_compress(
        self, pdf_files: list[Path], doc_config: dict[str, Any]
    ) -> Path:
        """Combine PDF pages and optionally compress."""
        try:
            combined_pdf = combine_pdfs(
                pdf_files,
                self.config.build_dir / f"{doc_config['filename']}.pdf",
            )
        except PDFCombineError as exc:
            raise PDFBakerError(f"Failed to combine PDFs: {exc}") from exc

        output_path = self.config.dist_dir / f"{doc_config['filename']}.pdf"

        if doc_config.get("compress_pdf", False):
            try:
                compress_pdf(combined_pdf, output_path)
                self.log_info("PDF compressed successfully")
            except PDFCompressionError as exc:
                self.log_warning(
                    "Compression failed, using uncompressed version: %s",
                    exc,
                )
                os.rename(combined_pdf, output_path)
        else:
            os.rename(combined_pdf, output_path)

        self.log_info("Created PDF: %s", output_path)
        return output_path

    def teardown(self) -> None:
        """Clean up build directory after successful processing."""
        if self.config.build_dir.exists():
            # Remove all files in the build directory
            for file_path in self.config.build_dir.iterdir():
                if file_path.is_file():
                    file_path.unlink()

            # Try to remove the build directory
            try:
                self.config.build_dir.rmdir()
            except OSError:
                # Directory not empty - this is expected if we have subdirectories
                pass
