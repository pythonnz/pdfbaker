"""PDF document generator."""

import logging

from .common import (
    # Exceptions
    PDFBakeError,
    PDFCombineError,
    PDFCompressionError,
    SVGConversionError,
    # Functions
    combine_pdfs,
    compress_pdf,
    convert_svg_to_pdf,
    deep_merge,
    load_pages,
)
from .render import create_env, process_template_data

logger = logging.getLogger(__name__)

__all__ = [
    # Logger
    "logger",
    # Exceptions
    "PDFBakeError",
    "PDFCombineError",
    "PDFCompressionError",
    "SVGConversionError",
    # Common functions
    "combine_pdfs",
    "compress_pdf",
    "convert_svg_to_pdf",
    "deep_merge",
    "load_pages",
    # Render functions
    "create_env",
    "process_template_data",
]
