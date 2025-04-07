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
    "combine_pdfs",
    "compress_pdf",
    "convert_svg_to_pdf",
    "deep_merge",
    "load_pages",
    # Render functions
    "create_env",
    "encode_image",
    "encode_images",
    "highlight",
    "process_list_item_texts",
    "process_list_items",
    "process_style",
    "process_template_data",
    "process_text_with_jinja",
    "space_bullets",
]
