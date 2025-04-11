"""pdfbaker exceptions."""

from pathlib import Path

__all__ = [
    "PDFBakeError",
    "PDFCombineError",
    "PDFCompressionError",
    "SVGConversionError",
]


class PDFBakeError(Exception):
    """Base exception for PDF baking errors."""


class PDFCombineError(PDFBakeError):
    """Failed to combine PDFs."""


class PDFCompressionError(PDFBakeError):
    """Failed to compress PDF."""


class SVGConversionError(PDFBakeError):
    """Failed to convert SVG to PDF."""

    def __init__(
        self, svg_path: str | Path, backend: str, cause: str | None = None
    ) -> None:
        self.svg_path = svg_path
        self.backend = backend
        self.cause = cause
        super().__init__(f"Failed to convert {svg_path} using {backend}: {cause}")
