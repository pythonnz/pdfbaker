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

__all__ = ["PDFBaker"]


DEFAULT_CONFIG = {
    "documents_dir": ".",
    "pages_dir": "pages",
    "templates_dir": "templates",
    "images_dir": "images",
    "build_dir": "build",
    "dist_dir": "dist",
}


class PDFBaker:
    """Main class for PDF document generation."""

    class Configuration(PDFBakerConfiguration):
        """PDFBaker configuration."""

        def __init__(self, base_config: dict[str, Any], config_file: Path) -> None:
            """Initialize baker configuration (needs documents)."""
            super().__init__(base_config, config_file)
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
        keep_build: bool = False,
    ) -> None:
        """Initialize PDFBaker with config file path.

        Args:
            config_file: Path to config file, document directory is its parent
        """
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
        self.logger = logging.getLogger(__name__)
        if quiet:
            logging.getLogger().setLevel(logging.ERROR)
        elif verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)
        self.keep_build = keep_build
        self.config = self.Configuration(
            base_config=DEFAULT_CONFIG,
            config_file=config_file,
        )

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a debug message."""
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log an info message."""
        self.logger.info(msg, *args, **kwargs)

    def info_section(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log an info message as a main section header."""
        self.logger.info(f"──── {msg} ────", *args, **kwargs)

    def info_subsection(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log an info message as a subsection header."""
        self.logger.info(f"  ── {msg} ──", *args, **kwargs)

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a warning message."""
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log an error message."""
        self.logger.error(f"**** {msg} ****", *args, **kwargs)

    def critical(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a critical message."""
        self.logger.critical(msg, *args, **kwargs)

    def bake(self) -> None:
        """Generate PDFs from documents."""
        pdfs_created: list[Path] = []
        failed_docs: list[tuple[str, str]] = []

        self.debug("Main configuration:")
        self.debug(self.config.pprint())
        self.debug("Documents to process:")
        self.debug(self.config.documents)
        for doc_config in self.config.documents:
            doc = PDFBakerDocument(
                baker=self,
                base_config=self.config,
                config=doc_config,
            )
            pdf_files, error_message = doc.process_document()
            if pdf_files is None:
                self.error(
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
            self.info("Created PDFs:")
            for pdf in pdfs_created:
                self.info("  %s", pdf)
        else:
            self.warning("No PDFs were created.")

        if failed_docs:
            self.warning(
                "Failed to process %d document%s:",
                len(failed_docs),
                "" if len(failed_docs) == 1 else "s",
            )
            for doc_name, error in failed_docs:
                self.error("  %s: %s", doc_name, error)
