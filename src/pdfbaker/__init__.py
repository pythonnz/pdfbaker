"""Core functionality for document generation."""

from .common import (
    combine_pdfs,
    compress_pdf,
    convert_svg_to_pdf,
    load_pages,
)
from .render import (
    create_env,
    encode_image,
    encode_images,
    highlight,
    process_list_item_texts,
    process_list_items,
    process_style,
    process_template_data,
    process_text_with_jinja,
    space_bullets,
)

__all__ = [
    # Common functions
    "load_pages",
    "compress_pdf",
    "combine_pdfs",
    "convert_svg_to_pdf",
    # Render functions
    "process_template_data",
    "create_env",
    "highlight",
    "process_style",
    "process_text_with_jinja",
    "process_list_item_texts",
    "process_list_items",
    "space_bullets",
    "encode_image",
    "encode_images",
]
