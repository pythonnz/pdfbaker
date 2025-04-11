"""Main PDF baker class."""

import logging
from pathlib import Path
from typing import Any

import yaml

from . import errors
from .document import PDFBakerDocument

__all__ = ["PDFBaker"]


class PDFBaker:
    """Main class for PDF document generation."""

    def __init__(self, config_file: Path) -> None:
        """Initialize PDFBaker with config file path.

        Args:
            config_file: Path to config file, document directory is its parent
        """
        self.logger = logging.getLogger(__name__)
        self.base_dir = config_file.parent
        self.build_dir = self.base_dir / "build"
        self.dist_dir = self.base_dir / "dist"
        self.config = self._load_config(config_file)

    # Add convenience methods for logging
    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a debug message."""
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log an info message."""
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a warning message."""
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log an error message."""
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a critical message."""
        self.logger.critical(msg, *args, **kwargs)

    def bake(self, debug: bool = False) -> None:
        """Generate PDFs from configuration.

        Args:
            debug: If True, keep build files for debugging
        """
        document_paths = self._get_document_paths(self.config.get("documents", []))

        for doc_name, doc_path in document_paths.items():
            doc = PDFBakerDocument(
                name=doc_name,
                doc_dir=doc_path,
                baker=self,
            )
            doc.setup_directories()
            doc.process_document()

        if not debug:
            self._teardown_build_directories(list(document_paths.keys()))

    def _load_config(self, config_file: Path) -> dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(config_file, encoding="utf-8") as f:
                config = yaml.safe_load(f)
                if "documents" not in config:
                    raise errors.PDFBakeError(
                        'Not a main configuration file - "documents" key missing'
                    )
                return config
        except Exception as exc:
            raise errors.PDFBakeError(f"Failed to load config file: {exc}") from exc

    def _get_document_paths(
        self, documents: list[dict[str, str] | str]
    ) -> dict[str, Path]:
        """Resolve document paths to absolute paths."""
        document_paths: dict[str, Path] = {}

        for doc_name in documents:
            if isinstance(doc_name, dict):
                # Format: {"name": "doc_name", "path": "/absolute/path/to/doc"}
                doc_path = Path(doc_name["path"])
                doc_name = doc_name["name"]
            else:
                # Default: document in subdirectory with same name as doc_name
                doc_path = self.base_dir / doc_name

            document_paths[doc_name] = doc_path.resolve()

        return document_paths

    def _teardown_build_directories(self, doc_names: list[str]) -> None:
        """Clean up build directories after successful processing."""
        for doc_name in doc_names:
            doc_build_dir = self.build_dir / doc_name
            if doc_build_dir.exists():
                # Remove all files in the document's build directory
                for file_path in doc_build_dir.iterdir():
                    if file_path.is_file():
                        file_path.unlink()

                # Try to remove the document's build directory if empty
                try:
                    doc_build_dir.rmdir()
                except OSError:
                    # Directory not empty (might contain subdirectories)
                    self.logger.warning(
                        "Build directory of document not empty, keeping: %s",
                        doc_build_dir,
                    )

        # Try to remove the base build directory if it exists and is empty
        if self.build_dir.exists():
            try:
                self.build_dir.rmdir()
            except OSError:
                # Directory not empty
                self.logger.warning(
                    "Build directory not empty, keeping: %s", self.build_dir
                )
