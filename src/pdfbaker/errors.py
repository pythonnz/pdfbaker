"""pdfbaker exceptions."""

from pathlib import Path

__all__ = [
    "ConfigurationError",
    "DocumentNotFoundError",
    "PDFBakerError",
    "PDFCombineError",
    "PDFCompressionError",
    "SVGConversionError",
    "SVGTemplateError",
]


class PDFBakerError(Exception):
    """Base exception for PDF baking errors."""


class DocumentNotFoundError(PDFBakerError):
    """Document not found in main configuration."""


class ConfigurationError(PDFBakerError):
    """Failed to load or parse configuration."""


class PDFCombineError(PDFBakerError):
    """Failed to combine PDFs."""


class PDFCompressionError(PDFBakerError):
    """Failed to compress PDF."""


class SVGConversionError(PDFBakerError):
    """Failed to convert SVG to PDF."""

    def __init__(
        self, svg_path: str | Path, backend: str, cause: str | None = None
    ) -> None:
        self.svg_path = svg_path
        self.backend = backend
        self.cause = cause
        super().__init__(f"Failed to convert {svg_path} using {backend}: {cause}")


class SVGTemplateError(PDFBakerError):
    """Failed to load or render an SVG template."""
