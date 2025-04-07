"""Core functionality for document generation."""

from .common import (
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

__all__ = [
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
