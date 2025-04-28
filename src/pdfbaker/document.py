"""Document class.

Document-level processing, variants, custom bake modules.

Delegates the jobs of rendering and converting to its pages,
combines and compresses the result and reports back to its baker.
"""

import importlib
import os
from pathlib import Path

from .config import PathSpec
from .config.document import DocumentConfig
from .errors import (
    PDFBakerError,
    PDFCombineError,
    PDFCompressionError,
)
from .logging import LoggingMixin
from .page import Page
from .pdf import (
    combine_pdfs,
    compress_pdf,
)

__all__ = ["Document"]


class Document(LoggingMixin):
    """Document class."""

    def __init__(self, config_path: PathSpec, **kwargs):
        self.log_trace_section("Loading document configuration: %s", config_path.name)
        self.config = DocumentConfig(config_path=config_path, **kwargs)
        self.log_trace(self.config.readable())

    def process_document(self) -> tuple[Path | list[Path] | None, str | None]:
        """Process the document - use custom bake module if it exists.

        Returns:
            Tuple of (pdf_files, error_message) where:
            - pdf_files is a Path or list of Paths to the created PDF
              files, or None if creation failed
            - error_message is a string describing the error, or None if successful
            FIXME: could have created SOME PDF files but also error
        """
        self.config.directories.build /= self.config.name
        self.config.directories.dist /= self.config.name

        self.log_info_section('Processing document "%s"...', self.config.name)
        self.log_debug(
            "Ensuring build directory exists: %s", self.config.directories.build
        )
        self.config.directories.build.mkdir(parents=True, exist_ok=True)
        self.log_debug(
            "Ensuring dist directory exists: %s", self.config.directories.dist
        )
        self.config.directories.dist.mkdir(parents=True, exist_ok=True)

        try:
            if self.config.custom_bake:
                return self._process_with_custom_bake(), None
            return self.process(), None
        except PDFBakerError as exc:
            return None, str(exc)

    def _process_with_custom_bake(self) -> Path | list[Path]:
        """Process document using custom bake module."""
        self.log_debug_subsection(
            'Custom processing document "%s"...', self.config.name
        )
        try:
            spec = importlib.util.spec_from_file_location(
                f"documents.{self.config.name}.bake",
                self.config.custom_bake.path,
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
        """Process document using standard processing."""
        self.log_debug_subsection(
            'Standard processing document "%s"...', self.config.name
        )
        if self.config.variants:
            # Multiple PDF documents
            pdf_files = []
            for variant_config in self.config.variants:
                self.log_info_subsection(
                    'Processing variant "%s"...', variant_config.variant["name"]
                )
                variant_config.directories.build = self.config.directories.build
                variant_config.directories.dist = self.config.directories.dist
                variant_config = variant_config.resolve_variables()
                self.log_trace(variant_config.readable())
                page_pdfs = self._process_pages(variant_config)
                pdf_files.append(self._finalize(page_pdfs, variant_config))

            return pdf_files

        # Single PDF document
        document_config = self.config.resolve_variables()
        page_pdfs = self._process_pages(document_config)
        return self._finalize(page_pdfs, document_config)

    def _process_pages(self, config: DocumentConfig) -> list[Path]:
        """Process pages with given configuration.

        If the document/variant has page-specific configuration
        (a section with the same name as the page), include it.
        """
        self.log_debug_subsection("Pages to process:")
        self.log_debug(config.pages)
        pdf_files = []

        for page_number, config_path in enumerate(config.pages, start=1):
            page_data = config.page_settings
            page_name = config_path.name

            page = Page(
                config_path=config_path,
                page_number=page_number,
                **page_data,
            )

            specific_config = getattr(config, page_name, None)
            if specific_config:
                source = "Variant" if config.is_variant else "Document"
                self.log_debug_subsection(
                    f'{source} "{config.name}" provides settings for page "{page_name}"'
                )
                self.log_trace(specific_config)
                page.config = page.config.merge(specific_config)

            pdf_files.append(page.process())

        return pdf_files

    def _finalize(self, pdf_files: list[Path], doc_config: DocumentConfig) -> Path:
        """Combine PDF pages and optionally compress."""
        self.log_debug_subsection("Finalizing document...")
        self.log_debug("Combining PDF pages...")
        try:
            combined_pdf = combine_pdfs(
                pdf_files,
                self.config.directories.build / f"{doc_config.filename}.pdf",
            )
        except PDFCombineError as exc:
            raise PDFBakerError(f"Failed to combine PDFs: {exc}") from exc

        output_path = self.config.directories.dist / f"{doc_config.filename}.pdf"

        if doc_config.compress_pdf:
            self.log_debug("Compressing PDF document...")
            try:
                compress_pdf(combined_pdf, output_path)
                self.log_info("PDF compressed successfully")
            except PDFCompressionError as exc:
                self.log_warning(
                    "Compression failed, using uncompressed PDF: %s",
                    exc,
                )
                os.rename(combined_pdf, output_path)
        else:
            os.rename(combined_pdf, output_path)

        self.log_info("Created %s", output_path.name)
        return output_path

    def teardown(self) -> None:
        """Clean up build directory after processing."""
        build_dir = self.config.directories.build
        self.log_debug_subsection("Tearing down build directory: %s", build_dir)
        if build_dir.exists():
            self.log_debug("Removing files in build directory...")
            for file_path in build_dir.iterdir():
                if file_path.is_file():
                    file_path.unlink()

            try:
                self.log_debug("Removing build directory...")
                build_dir.rmdir()
            except OSError:
                self.log_warning("Build directory not empty - not removing")
