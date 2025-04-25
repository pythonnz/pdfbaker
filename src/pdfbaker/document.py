"""Document class.

Document-level processing, variants, custom bake modules.

Delegates the jobs of rendering and converting to its pages,
combines and compresses the result and reports back to its baker.
"""

import importlib
import os
from pathlib import Path

from .config import (
    DocumentConfig,
    DocumentVariantConfig,
    PathSpec,
    render_config,
)
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
            FIXME: could have created SOME PDF files
            - error_message is a string describing the error, or None if successful
        """
        self.log_info_section('Processing document "%s"...', self.config.name)

        self.config.directories.build.mkdir(parents=True, exist_ok=True)
        self.config.directories.dist.mkdir(parents=True, exist_ok=True)

        bake_path = self.config.bake_path.path
        try:
            if bake_path.exists():
                return self._process_with_custom_bake(bake_path), None
            return self.process(), None
        except PDFBakerError as exc:
            return None, str(exc)

    # ##############################################################

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
        if self.config.variants:
            # Multiple PDF documents
            pdf_files = []
            for variant_config in self.config.variants:
                self.log_info_subsection(
                    'Processing variant "%s"...', variant_config.name
                )
                _ = """
                # variant_config = deep_merge(self.config, variant)
                # self.log_trace(variant_config)
                self.config.update(variant_config)
                # variant_config = render_config(variant_config)
                page_pdfs = self._process_pages(self.config)
                pdf_files.append(self._finalize(page_pdfs, self.config))
                """

                # FIXME: Too much logic here, should be in DocumentVariantConfig

                # Create a document config with the variant info
                merged_config = self.config.model_dump()
                variant_data = variant_config.model_dump()
                merged_config["variant"] = variant_data

                # Update other config values from the variant
                # FIXME: should use deep_merge?
                # FIXME: pages could be defined in page but not variant or vice versa
                for key, value in variant_data.items():
                    if key not in ["directories", "pages"]:
                        merged_config[key] = value
                # if variant_data.get("pages"):
                #    merged_config["pages"] = variant_data["pages"]

                variant_settings = self.config.variant_settings
                merged_config.update(variant_settings)
                merged_config = render_config(merged_config)

                doc_with_variant = DocumentVariantConfig(**merged_config)

                # Process with the variant-enhanced config
                page_pdfs = self._process_pages(doc_with_variant)
                pdf_files.append(self._finalize(page_pdfs, doc_with_variant))

            return pdf_files

        # Single PDF document
        # doc_config = render_config(self.config)
        page_pdfs = self._process_pages(self.config)
        return self._finalize(page_pdfs, self.config)

    def _process_pages(
        self, config: DocumentConfig | DocumentVariantConfig
    ) -> list[Path]:
        """Process pages with given configuration."""
        self.log_debug_subsection("Pages to process:")
        self.log_debug(config.pages)
        pdf_files = []

        # FIXME: Too much logic here, should be in DocumentVariantConfig

        for page_num, page_config_path in enumerate(config.pages, start=1):
            # if "variant" in config:
            #    base_config = DocumentVariantConfig(
            #        variant=config["variant"],
            #        directories=config.directories,
            #        pages=config.pages,
            #    )
            # else:
            #    base_config = config

            # Get the settings (includes variant if present)
            base_config = config.page_settings
            if "config_path" in base_config:
                # Fix for variant
                del base_config["config_path"]

            page = Page(
                config_path=page_config_path,
                number=page_num,
                **base_config,
            )
            pdf_files.append(page.process())

            _ = """
            page_name = page_config_path.stem
            base_config = config.copy()

            # If the document/variant has page-specific configuration
            # (a section with the same name as the page), include it
            if page_name in config:
                if "variant" in config:
                    source_desc = f'Variant "{config["variant"]["name"]}"'
                else:
                    source_desc = f'Document "{self.config.name}"'
                self.log_debug_subsection(
                    f'{source_desc} provides settings for page "{page_name}"'
                )
                self.log_trace(config[page_name])
                base_config.update(config[page_name])

            page = PDFBakerPage(
                document=self,
                page_number=page_num,
                base_config=base_config,
                config_path=page_config_path,
            )
            pdf_files.append(page.process())
            """

        return pdf_files

    def _finalize(
        self, pdf_files: list[Path], doc_config: DocumentConfig | DocumentVariantConfig
    ) -> Path:
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

    # ##############################################################

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
