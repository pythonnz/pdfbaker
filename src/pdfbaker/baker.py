"""Baker class.

Overall orchestration and logging.

Is given a configuration file and sets up logging.
bake() delegates to its documents and reports back the end result.
"""

import logging
import shutil
from pathlib import Path
from typing import NamedTuple

from pydantic import BaseModel, ValidationError
from ruamel.yaml import YAML

from .config import PathSpec
from .config.baker import BakerConfig
from .console import build_create_from_panel, build_outcome_panel, stdout_console
from .document import Document
from .errors import DocumentNotFoundError, DryRunCreateFromCompleted
from .logging import LoggingMixin, setup_logging

__all__ = ["Baker", "BakerOptions", "ProcessedDoc"]


class ProcessedDoc(NamedTuple):
    """The outcome of processing a document, for reporting back to the user."""

    document: Document
    pdf_files: list[Path] | None
    error_message: str | None


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

        if options.create_from:
            project_dir = self.create_from(
                svg_path=options.create_from,
                config_path=config_file,
                dry_run=options.dry_run,
            )
            if options.dry_run:
                # Dry run creations don't continue with dry run processing
                raise DryRunCreateFromCompleted()

            if self.logger.getEffectiveLevel() <= logging.INFO:
                panel = build_create_from_panel(options.create_from, project_dir)
                stdout_console.print(panel)

        self.log_debug_section("Loading main configuration: %s", config_file)
        self.config = BakerConfig(
            config_file=config_file,
            keep_build=options.keep_build,
            fail_if_exists=options.fail_if_exists,
            dry_run=options.dry_run,
            **kwargs,
        )
        self.log_trace_preview(self.config.readable(), syntax="yaml")
        self.log_debug("Build directory: %s", self.config.directories.build)

    def bake(self, document_names: tuple[str, ...] | None = None) -> None:
        """Bake the documents."""
        docs = self._get_selected_documents(document_names)

        if self.config.dry_run:
            self.log_info("[DRY RUN] No files will be created.")
        self.log_debug_subsection("Documents to process:")
        self.log_debug(docs)

        processed_docs = self._process_documents(docs)
        if not self.config.keep_build:
            self.teardown()

        if self.logger.getEffectiveLevel() <= logging.INFO:
            outcome_panel = build_outcome_panel(
                processed_docs,
                dry_run=self.config.dry_run,
                keep_build=self.config.keep_build,
                build_dir=self.config.directories.build,
            )
            stdout_console.print(outcome_panel)

        return all(not d.error_message for d in processed_docs)

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

    def _process_documents(self, docs: list[PathSpec]) -> list[ProcessedDoc]:
        processed_docs: list[ProcessedDoc] = []
        for config_path in docs:
            try:
                document = Document(
                    config_path=config_path, **self.config.document_settings
                )
            except ValidationError as e:
                error_message = f'Invalid config for document "{config_path.name}": {e}'
                self.log_error(error_message)
                processed_docs.append(ProcessedDoc(config_path, None, error_message))
                continue

            pdf_files, error_message = document.process_document()

            if error_message:
                self.log_error(
                    "Failed to process document '%s': %s",
                    document.config.name,
                    error_message,
                )
                processed_docs.append(ProcessedDoc(document, None, error_message))
            else:
                if isinstance(pdf_files, Path):
                    pdf_files = [pdf_files]
                processed_docs.append(ProcessedDoc(document, pdf_files, None))
            if not self.config.keep_build:
                document.teardown()
        return processed_docs

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
                        ":no_entry_sign:"
                        " [DRY RUN] Not removing top-level build directory"
                    )
                else:
                    build_dir.rmdir()
            except OSError:
                self.log_warning("Top-level build directory not empty - not removing")
        else:
            self.log_debug("Top-level build directory does not exist")

    def create_from(
        self, svg_path: Path, config_path: Path, dry_run: bool = False
    ) -> None:
        """Create a scaffold for templating from an SVG and config path."""
        project_dir = config_path.parent
        self.log_debug_section(
            "Creating from %s in: %s", svg_path.resolve(), project_dir.resolve()
        )
        doc_name = svg_path.stem
        doc_dir = project_dir / doc_name
        template_file = doc_dir / "templates" / "main.svg.j2"
        page_file = doc_dir / "pages" / "main.yaml"
        doc_config_file = doc_dir / "config.yaml"
        files_to_create = [config_path, doc_config_file, page_file, template_file]
        dirs_to_create = [
            d
            for d in [project_dir, doc_dir, doc_dir / "pages", doc_dir / "templates"]
            if not d.exists()
        ]

        for f in files_to_create:
            if f.exists():
                raise FileExistsError(f"File already exists: {f.resolve()}")

        if dry_run:
            for d in dirs_to_create:
                self.log_info(":no_entry_sign: [DRY RUN] Would create directory: %s", d)
            for f in files_to_create:
                self.log_info(":no_entry_sign: [DRY RUN] Would create file:      %s", f)
            self.log_info(":no_entry_sign: [DRY RUN] No files created.")
            raise DryRunCreateFromCompleted()

        for d in dirs_to_create:
            self.log_debug_subsection("Ensuring directory exists: %s", d.resolve())
            d.mkdir(parents=True, exist_ok=True)

        yaml = YAML()
        yaml.indent(mapping=2, sequence=4, offset=2)

        self.log_debug_subsection("Writing main config: %s", config_path.resolve())
        with open(config_path, "w", encoding="utf-8") as f:
            f.write("# PDFBaker main config\n\n")
            yaml.dump({"documents": [doc_name]}, f)
            f.write(
                "\n"
                "# directories:  # Override default directories below\n"
                "#   dist: dist  # Final PDF files are written here\n"
                "#   documents: .  # Location of document configurations\n"
                "#   images: images  # Location of image files\n"
                "#   pages: pages  # Location of page configurations\n"
                "#   templates: templates  # Location of SVG template files\n"
                "# jinja2_extensions: []"
                "  # Jinja2 extensions to load and use in templates\n"
                "# template_renderers:  # List of automatically applied renderers\n"
                "#   - render_highlight\n"
                "# template_filters:  # List of filters made available to templates\n"
                "#   - wordwrap\n"
                "# svg2pdf_backend: cairosvg"
                "  # Backend to use for SVG to PDF conversion\n"
                "# compress_pdf: false  # Whether to compress the final PDF\n"
                "# keep_build: false"
                "  # Whether to keep the build directory and its intermediary files\n"
                "\n"
                "# Example custom variables for all pages of all documents:\n"
                "# style:\n"
                "#   font: Arial\n"
                "#   color: black\n"
            )
        self.log_trace_preview(
            config_path.read_text(encoding="utf-8"),
            syntax="yaml",
        )
        self.log_info("Created main config: %s", config_path)

        self.log_debug_subsection(
            "Writing document config: %s", doc_config_file.resolve()
        )
        with open(doc_config_file, "w", encoding="utf-8") as f:
            f.write("# Document config\n\n")
            yaml.dump({"filename": doc_name, "pages": ["main"]}, f)
            f.write(
                "\n"
                "# compress_pdf: false"
                "  # Whether to compress the final PDF for this document\n"
                "# custom_bake: bake.py"
                "  # Python file used for custom processing (if found)\n"
                "# variants:  # List of document variants\n"
                "\n"
                "# Example custom variables for all pages of this document:\n"
                "# style:\n"
                "#   font: Arial\n"
                "#   color: black\n"
            )
        self.log_trace_preview(
            doc_config_file.read_text(encoding="utf-8"),
            syntax="yaml",
        )
        self.log_info("Created document config: %s", doc_config_file)

        self.log_debug_subsection("Writing page config: %s", page_file.resolve())
        with open(page_file, "w", encoding="utf-8") as f:
            f.write("# Page config\n\n")
            yaml.dump({"template": "main.svg.j2", "name": "main"}, f)
            f.write(
                "\n"
                "# images:  # List of images to use in the page\n"
                "\n"
                "# Example custom variables for this page:\n"
                "# title: My Document\n"
                "# date: 2025-05-19\n"
            )
        self.log_trace_preview(
            page_file.read_text(encoding="utf-8"),
            syntax="yaml",
        )
        self.log_info("Created page config: %s", page_file)

        self.log_debug_subsection(
            "Copying SVG to template: %s", template_file.resolve()
        )
        shutil.copy(svg_path, template_file)
        self.log_trace_preview(
            template_file.read_text(encoding="utf-8"),
            syntax="xml",
        )
        self.log_info("Created template: %s", template_file)

        return project_dir
