"""Baker class.

Overall orchestration and logging.

Is given a configuration file and sets up logging.
bake() delegates to its documents and reports back the end result.
"""

from pathlib import Path

from pydantic import BaseModel, ValidationError

from .config import PathSpec
from .config.baker import BakerConfig
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
        dry_run: Do not write any files, just log actions
        fail_if_exists: Abort if a file already exists in the dist directory
        create_from: Path to SVG file for populating a (new) project
    """

    quiet: bool = False
    verbose: bool = False
    trace: bool = False
    keep_build: bool = False
    fail_if_exists: bool = False
    dry_run: bool = False
    create_from: Path | None = None


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
        self.create_from = options.create_from
        # FIXME: use create_from to create a new config file
        self.log_debug_section("Loading main configuration: %s", config_file)
        self.config = BakerConfig(
            config_file=config_file,
            keep_build=options.keep_build,
            fail_if_exists=options.fail_if_exists,
            dry_run=options.dry_run,
            **kwargs,
        )
        self.log_trace(self.config.readable())
        self.log_debug("Build directory: %s", self.config.directories.build)

    def bake(self, document_names: tuple[str, ...] | None = None) -> None:
        """Bake the documents."""
        docs = self._get_selected_documents(document_names)
        self.log_debug_subsection("Documents to process:")
        self.log_debug(docs)

        pdfs_created, failed_docs = self._process_documents(docs)

        self.log_info("─" * 80)
        if pdfs_created:
            if self.config.dry_run:
                self.log_info("👀 [DRY RUN] Would have created PDFs:")
            else:
                self.log_info("Successfully created PDFs:")
            for pdf in pdfs_created:
                self.log_info("  %s %s", "🟨" if self.config.dry_run else "✅", pdf)
        else:
            self.log_warning("No PDFs were created.")

        if failed_docs:
            self.log_warning(
                "Failed to process %d document%s:",
                len(failed_docs),
                "" if len(failed_docs) == 1 else "s",
            )
            for failed_doc, error_message in failed_docs:
                name = failed_doc.config.name
                if isinstance(failed_doc, Document) and failed_doc.config.is_variant:
                    name += f' variant "{failed_doc.config.variant["name"]}"'
                self.log_error("  %s: %s", name, error_message)
                if hasattr(failed_doc, "config"):
                    self.log_debug(
                        'Build directory for "%s": %s',
                        name,
                        failed_doc.config.directories.build,
                    )

        if self.config.keep_build:
            self.log_info("Build files kept in: %s", self.config.directories.build)
        else:
            self.teardown()

        return not failed_docs

    def _get_selected_documents(
        self, selected_names: tuple[str, ...] | None = None
    ) -> list[PathSpec]:
        """Return the document paths to actually process as selected."""
        if not selected_names:
            return self.config.documents

        available = [doc.name for doc in self.config.documents]
        missing = [name for name in selected_names if name not in available]
        if missing:
            available_str = ", ".join([f'"{name}"' for name in available])
            self.log_info(
                f"Documents in {self.config.config_file.name}: {available_str}"
            )
            missing_str = ", ".join([f'"{name}"' for name in missing])
            raise DocumentNotFoundError(
                f"Document{'s' if len(missing) != 1 else ''} not found "
                f"in configuration file: {missing_str}."
            )

        return [doc for doc in self.config.documents if doc.name in selected_names]

    def _process_documents(
        self, docs: list[PathSpec]
    ) -> tuple[list[Path], list[tuple[PathSpec, str]]]:
        pdfs_created: list[Path] = []
        failed_docs: list[tuple[PathSpec, str]] = []

        for config_path in docs:
            try:
                document = Document(
                    config_path=config_path, **self.config.document_settings
                )
            except ValidationError as e:
                error_message = f'Invalid config for document "{config_path.name}": {e}'
                self.log_error(error_message)
                failed_docs.append((config_path, error_message))
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

        return pdfs_created, failed_docs

    def teardown(self) -> None:
        """Clean up (top-level) build directory after processing."""
        build_dir = self.config.directories.build
        self.log_debug_subsection(
            "Tearing down top-level build directory: %s", build_dir
        )
        if build_dir.exists():
            try:
                self.log_debug("Removing top-level build directory...")
                if self.config.dry_run:
                    self.log_debug(
                        "👀 [DRY RUN] Not removing top-level build directory"
                    )
                else:
                    build_dir.rmdir()
            except OSError:
                self.log_warning("Top-level build directory not empty - not removing")
        else:
            self.log_debug("Top-level build directory does not exist")
