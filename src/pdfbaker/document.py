"""PDFBakerDocument class.

Document-level processing, variants, custom bake modules.

Delegates the jobs of rendering and converting to its pages,
combines and compresses the result and reports back to its baker.
"""

import importlib
import os
from pathlib import Path
from typing import Any

from .config import (
    PDFBakerConfiguration,
    deep_merge,
    render_config,
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

DEFAULT_DOCUMENT_CONFIG = {
    # Default to directories relative to the config file
    "directories": {
        "pages": "pages",
        "templates": "templates",
        "images": "images",
    },
}
DEFAULT_DOCUMENT_CONFIG_FILE = "config.yaml"

__all__ = ["PDFBakerDocument"]


class PDFBakerDocument(LoggingMixin):
    """A document being processed."""

    class Configuration(PDFBakerConfiguration):
        """PDFBaker document-specific configuration."""

        def __init__(
            self,
            document: "PDFBakerDocument",
            base_config: "PDFBakerConfiguration",  # type: ignore # noqa: F821
            config_path: Path,
        ) -> None:
            """Initialize document configuration.

            Args:
                base_config: The PDFBaker configuration to merge with
                config_file: The document configuration (YAML file)
            """
            self.document = document

            if config_path.is_dir():
                self.name = config_path.name
                config_path = config_path / DEFAULT_DOCUMENT_CONFIG_FILE
            else:
                self.name = config_path.stem

            base_config = deep_merge(base_config, DEFAULT_DOCUMENT_CONFIG)

            self.document.log_trace_section(
                "Loading document configuration: %s", config_path
            )
            super().__init__(base_config, config_path)
            self.document.log_trace(self.pretty())

            self.bake_path = self["directories"]["config"] / "bake.py"
            self.build_dir = self["directories"]["build"] / self.name
            self.dist_dir = self["directories"]["dist"] / self.name

            if "pages" not in self:
                raise ConfigurationError(
                    'Document "{document.name}" is missing key "pages"'
                )
            self.pages = []
            for page_spec in self["pages"]:
                if isinstance(page_spec, dict) and "path" in page_spec:
                    # Path was specified: relative to the config file
                    page = self.resolve_path(
                        page_spec["path"], directory=self["directories"]["config"]
                    )
                else:
                    # Only name was specified: relative to the pages directory
                    page = self.resolve_path(
                        page_spec, directory=self["directories"]["pages"]
                    )
                if not page.suffix:
                    page = page.with_suffix(".yaml")
                self.pages.append(page)

    def __init__(
        self,
        baker: "PDFBaker",  # type: ignore # noqa: F821
        base_config: dict[str, Any],
        config_path: Path,
    ):
        """Initialize a document."""
        super().__init__()
        self.baker = baker
        self.config = self.Configuration(
            document=self,
            base_config=base_config,
            config_path=config_path,
        )

    def process_document(self) -> tuple[Path | list[Path] | None, str | None]:
        """Process the document - use custom bake module if it exists.

        Returns:
            Tuple of (pdf_files, error_message) where:
            - pdf_files is a Path or list of Paths to the created PDF
              files, or None if creation failed
            FIXME: could have created SOME PDF files
            - error_message is a string describing the error, or None if successful
        """
        self.log_info_section('Processing document "%s"...', self.config.name)

        self.config.build_dir.mkdir(parents=True, exist_ok=True)
        self.config.dist_dir.mkdir(parents=True, exist_ok=True)

        try:
            if self.config.bake_path.exists():
                return self._process_with_custom_bake(self.config.bake_path), None
            return self.process(), None
        except PDFBakerError as exc:
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
        """Process document using standard processing."""
        if "variants" in self.config:
            # Multiple PDF documents
            pdf_files = []
            for variant in self.config["variants"]:
                self.log_info_subsection('Processing variant "%s"...', variant["name"])
                variant_config = deep_merge(self.config, variant)
                variant_config["variant"] = variant
                variant_config = render_config(variant_config)
                page_pdfs = self._process_pages(variant_config)
                pdf_files.append(self._finalize(page_pdfs, variant_config))
            return pdf_files

        # Single PDF document
        doc_config = render_config(self.config)
        page_pdfs = self._process_pages(doc_config)
        return self._finalize(page_pdfs, doc_config)

    def _process_pages(self, config: dict[str, Any]) -> list[Path]:
        """Process pages with given configuration."""
        pdf_files = []
        self.log_debug_subsection("Pages to process:")
        self.log_debug(self.config.pages)
        for page_num, page_config in enumerate(self.config.pages, start=1):
            page = PDFBakerPage(
                document=self,
                page_number=page_num,
                base_config=config,
                config_path=page_config,
            )
            pdf_files.append(page.process())

        return pdf_files

    def _finalize(self, pdf_files: list[Path], doc_config: dict[str, Any]) -> Path:
        """Combine PDF pages and optionally compress."""
        self.log_debug_subsection("Finalizing document...")
        self.log_debug("Combining PDF pages...")
        try:
            combined_pdf = combine_pdfs(
                pdf_files,
                self.config.build_dir / f"{doc_config['filename']}.pdf",
            )
        except PDFCombineError as exc:
            raise PDFBakerError(f"Failed to combine PDFs: {exc}") from exc

        output_path = self.config.dist_dir / f"{doc_config['filename']}.pdf"

        if doc_config.get("compress_pdf", False):
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
        self.log_debug_subsection(
            "Tearing down build directory: %s", self.config.build_dir
        )
        if self.config.build_dir.exists():
            self.log_debug("Removing files in build directory...")
            for file_path in self.config.build_dir.iterdir():
                if file_path.is_file():
                    file_path.unlink()

            try:
                self.log_debug("Removing build directory...")
                self.config.build_dir.rmdir()
            except OSError:
                self.log_warning("Build directory not empty - not removing")
