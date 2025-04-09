"""Core functionality for document generation."""

import logging

from .common import (
    PDFBakeError,
    PDFCombineError,
    PDFCompressionError,
    SVGConversionError,
    combine_pdfs,
    compress_pdf,
    convert_svg_to_pdf,
    deep_merge,
    load_pages,
)
from .render import (
    create_env,
    process_template_data,
)

logger = logging.getLogger(__name__)

__all__ = [
    "logger",
    # common
    "PDFBakeError",
    "PDFCombineError",
    "PDFCompressionError",
    "SVGConversionError",
    "combine_pdfs",
    "compress_pdf",
    "convert_svg_to_pdf",
    "deep_merge",
    "load_pages",
    # render
    "create_env",
    "process_template_data",
]
