"""PDFBaker class.

Overall orchestration and logging.

Is given a configuration file and sets up logging.
bake() delegates to its documents and reports back the end result.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .config import PDFBakerConfiguration, deep_merge
from .document import PDFBakerDocument
from .errors import ConfigurationError, DocumentNotFoundError
from .logging import LoggingMixin, setup_logging

__all__ = ["PDFBaker", "PDFBakerOptions"]


DEFAULT_BAKER_CONFIG = {
    # Default to directories relative to the config file
    "directories": {
        "documents": ".",
        "build": "build",
        "dist": "dist",
    },
    # Highlighting support enabled by default
    "template_renderers": ["render_highlight"],
    # Make all filters available by default
    "template_filters": ["wordwrap"],
}


@dataclass
class PDFBakerOptions:
    """Options for controlling PDFBaker behavior.

    Attributes:
        quiet: Show errors only
        verbose: Show debug information
        trace: Show trace information (even more detailed than debug)
        keep_build: Keep build artifacts after processing
        default_config_overrides: Dictionary of values to override the built-in defaults
            before loading the main configuration
    """

    quiet: bool = False
    verbose: bool = False
    trace: bool = False
    keep_build: bool = False
    default_config_overrides: dict[str, Any] | None = None


class PDFBaker(LoggingMixin):
    """Main class for PDF document generation."""

    class Configuration(PDFBakerConfiguration):
        """PDFBaker configuration."""

        def __init__(
            self, baker: "PDFBaker", base_config: dict[str, Any], config_file: Path
        ) -> None:
            """Initialize baker configuration (needs documents)."""
            self.baker = baker
            self.name = config_file.name
            self.baker.log_debug_section("Loading main configuration: %s", config_file)
            super().__init__(base_config, config_file)
            self.baker.log_trace(self.pretty())
            if "documents" not in self:
                raise ConfigurationError(
                    'Key "documents" missing - is this the main configuration file?'
                )
            self.build_dir = self["directories"]["build"]
            self.documents = []
            for doc_spec in self["documents"]:
                doc_path = self.resolve_path(
                    doc_spec, directory=self["directories"]["documents"]
                )
                self.documents.append({"name": doc_path.name, "path": doc_path})

    def __init__(
        self,
        config_file: Path,
        options: PDFBakerOptions | None = None,
    ) -> None:
        """Initialize PDFBaker with config file path. Set logging level.

        Args:
            config_file: Path to config file
            options: Optional options for logging and build behavior
        """
        super().__init__()
        options = options or PDFBakerOptions()
        setup_logging(quiet=options.quiet, trace=options.trace, verbose=options.verbose)
        self.keep_build = options.keep_build

        base_config = DEFAULT_BAKER_CONFIG.copy()
        if options and options.default_config_overrides:
            base_config = deep_merge(base_config, options.default_config_overrides)
        base_config["directories"]["config"] = config_file.parent.resolve()

        self.config = self.Configuration(
            baker=self,
            base_config=base_config,
            config_file=config_file,
        )

    def _get_documents_to_process(
        self, selected_document_names: tuple[str, ...] | None = None
    ) -> list[Path]:
        """Get the document paths to process based on optional filtering.

        Args:
            document_names: Optional tuple of document names to process

        Returns:
            List of document paths to process
        """
        if not selected_document_names:
            return self.config.documents

        available_doc_names = [doc["name"] for doc in self.config.documents]
        missing_docs = [
            name for name in selected_document_names if name not in available_doc_names
        ]
        if missing_docs:
            available_str = ", ".join([f'"{name}"' for name in available_doc_names])
            self.log_info(f"Documents in {self.config.name}: {available_str}")
            missing_str = ", ".join([f'"{name}"' for name in missing_docs])
            raise DocumentNotFoundError(
                f"Document{'s' if len(missing_docs) != 1 else ''} not found "
                f"in configuration: {missing_str}."
            )

        return [
            doc
            for doc in self.config.documents
            if doc["name"] in selected_document_names
        ]

    def bake(self, document_names: tuple[str, ...] | None = None) -> bool:
        """Create PDFs for all documents or only the specified ones.

        Args:
            document_names: Optional tuple of document names to process

        Returns:
        bool: True if all documents were processed successfully, False if any failed
        """
        pdfs_created: list[Path] = []
        failed_docs: list[tuple[str, str]] = []

        documents = self._get_documents_to_process(document_names)

        self.log_debug_subsection("Documents to process:")
        self.log_debug(documents)
        for doc_config in documents:
            doc = PDFBakerDocument(
                baker=self,
                base_config=self.config,
                config_path=doc_config["path"],
            )
            pdf_files, error_message = doc.process_document()
            if error_message:
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
            self.log_info("Successfully created PDFs:")
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

        if not self.keep_build:
            self.teardown()

        return not failed_docs

    def teardown(self) -> None:
        """Clean up (top-level) build directory after processing."""
        self.log_debug_subsection(
            "Tearing down top-level build directory: %s", self.config.build_dir
        )
        if self.config.build_dir.exists():
            try:
                self.log_debug("Removing top-level build directory...")
                self.config.build_dir.rmdir()
            except OSError:
                self.log_warning("Top-level build directory not empty - not removing")
