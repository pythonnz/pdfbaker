"""PDFBaker class.

Overall orchestration and logging.

Is given a configuration file and sets up logging.
bake() delegates to its documents and reports back the end result.
"""

import logging
from pathlib import Path
from typing import Any

from .config import PDFBakerConfiguration
from .document import PDFBakerDocument
from .errors import ConfigurationError
from .logging import TRACE, LoggingMixin

__all__ = ["PDFBaker"]


DEFAULT_CONFIG = {
    "documents_dir": ".",
    "pages_dir": "pages",
    "templates_dir": "templates",
    "images_dir": "images",
    "build_dir": "build",
    "dist_dir": "dist",
}


class PDFBaker(LoggingMixin):
    """Main class for PDF document generation."""

    class Configuration(PDFBakerConfiguration):
        """PDFBaker configuration."""

        def __init__(
            self, baker: "PDFBaker", base_config: dict[str, Any], config_file: Path
        ) -> None:
            """Initialize baker configuration (needs documents)."""
            self.baker = baker
            self.baker.log_debug_section("Loading main configuration: %s", config_file)
            super().__init__(base_config, config_file)
            self.baker.log_trace(self.pprint())
            if "documents" not in self:
                raise ConfigurationError(
                    'Key "documents" missing - is this the main configuration file?'
                )
            self.documents = [
                self.resolve_path(doc_spec) for doc_spec in self["documents"]
            ]

    def __init__(
        self,
        config_file: Path,
        quiet: bool = False,
        verbose: bool = False,
        trace: bool = False,
        keep_build: bool = False,
    ) -> None:
        """Initialize PDFBaker with config file path. Set logging level.

        Args:
            config_file: Path to config file, document directory is its parent
            quiet: Show errors only
            verbose: Show debug information
            trace: Show trace information (even more detailed than debug)
            keep_build: Keep build artifacts
        """
        super().__init__()
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
        if quiet:
            logging.getLogger().setLevel(logging.ERROR)
        elif trace:
            logging.getLogger().setLevel(TRACE)
        elif verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)
        self.keep_build = keep_build
        self.config = self.Configuration(
            baker=self,
            base_config=DEFAULT_CONFIG,
            config_file=config_file,
        )

    def bake(self) -> None:
        """Generate PDFs from documents."""
        pdfs_created: list[Path] = []
        failed_docs: list[tuple[str, str]] = []

        self.log_debug_subsection("Documents to process:")
        self.log_debug(self.config.documents)
        for doc_config in self.config.documents:
            doc = PDFBakerDocument(
                baker=self,
                base_config=self.config,
                config=doc_config,
            )
            pdf_files, error_message = doc.process_document()
            if pdf_files is None:
                self.log_error(
                    "Failed to process document '%s': %s",
                    doc.config.name,
                    error_message,
                )
                failed_docs.append((doc.config.name, error_message))
            else:
                if isinstance(pdf_files, Path):
                    pdf_files = [pdf_files]
                pdfs_created.extend(pdf_files)
                if not self.keep_build:
                    doc.teardown()

        if pdfs_created:
            self.log_info("Created PDFs:")
            for pdf in pdfs_created:
                self.log_info("  %s", pdf)
        else:
            self.log_warning("No PDFs were created.")

        if failed_docs:
            self.log_warning(
                "Failed to process %d document%s:",
                len(failed_docs),
                "" if len(failed_docs) == 1 else "s",
            )
            for doc_name, error in failed_docs:
                self.log_error("  %s: %s", doc_name, error)
