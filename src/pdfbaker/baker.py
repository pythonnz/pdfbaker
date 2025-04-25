"""Baker class.

Overall orchestration and logging.

Is given a configuration file and sets up logging.
bake() delegates to its documents and reports back the end result.
"""

from pathlib import Path

from pydantic import BaseModel, ValidationError

from .config import (
    BakerConfig,
    PathSpec,
)
from .document import Document
from .errors import DocumentNotFoundError
from .logging import LoggingMixin, setup_logging

__all__ = ["Baker", "BakerOptions"]


class BakerOptions(BaseModel):
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


class Baker(LoggingMixin):
    """Baker class."""

    def __init__(
        self,
        config_file: Path,
        options: BakerOptions | None = None,
        **kwargs,
    ) -> None:
        """Set up logging and load configuration."""
        options = options or BakerOptions()
        setup_logging(quiet=options.quiet, trace=options.trace, verbose=options.verbose)
        self.log_debug_section("Loading main configuration: %s", config_file)
        self.config = BakerConfig(
            config_file=config_file,
            keep_build=options and options.keep_build or False,
            **kwargs,
        )
        self.log_trace(self.config.readable())

    def _get_documents_to_process(
        self, selected_document_names: tuple[str, ...] | None = None
    ) -> list[PathSpec]:
        """Get the document paths to process based on optional filtering.

        Args:
            document_names: Optional tuple of document names to process

        Returns:
            List of document paths to process
        """
        if not selected_document_names:
            return self.config.documents

        available_doc_names = [doc.name for doc in self.config.documents]
        missing_docs = [
            name for name in selected_document_names if name not in available_doc_names
        ]
        if missing_docs:
            available_str = ", ".join([f'"{name}"' for name in available_doc_names])
            self.log_info(
                f"Documents in {self.config.config_file.name}: {available_str}"
            )
            missing_str = ", ".join([f'"{name}"' for name in missing_docs])
            raise DocumentNotFoundError(
                f"Document{'s' if len(missing_docs) != 1 else ''} not found "
                f"in configuration: {missing_str}."
            )

        return [
            doc for doc in self.config.documents if doc.name in selected_document_names
        ]

    def bake(self, document_names: tuple[str, ...] | None = None) -> None:
        """Bake the documents."""
        pdfs_created: list[Path] = []
        failed_docs: list[tuple[PathSpec, str]] = []

        doc_configs = self._get_documents_to_process(document_names)

        self.log_debug_subsection("Documents to process:")
        self.log_debug(doc_configs)
        for doc_config in doc_configs:
            try:
                document = Document(
                    config_path=doc_config, **self.config.document_settings
                )
            except ValidationError as e:
                self.log_error(f'Invalid config for document "{doc_config.name}": {e}')
                continue

            pdf_files, error_message = document.process_document()
            if error_message:
                self.log_error(
                    "Failed to process document '%s': %s",
                    document.config.name,
                    error_message,
                )
                failed_docs.append((document, error_message))
            else:
                if isinstance(pdf_files, Path):
                    pdf_files = [pdf_files]
                pdfs_created.extend(pdf_files)
            if not self.config.keep_build:
                document.teardown()

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

        if not self.config.keep_build:
            self.teardown()

        return not failed_docs

    def teardown(self) -> None:
        """Clean up (top-level) build directory after processing."""
        build_dir = self.config.directories.build
        self.log_debug_subsection(
            "Tearing down top-level build directory: %s", build_dir
        )
        if build_dir.exists():
            try:
                self.log_debug("Removing top-level build directory...")
                build_dir.rmdir()
            except OSError:
                self.log_warning("Top-level build directory not empty - not removing")
