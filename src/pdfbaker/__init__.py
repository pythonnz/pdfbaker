"""Core functionality for document generation."""

from .common import (
    load_pages,
    compress_pdf,
    combine_pdfs,
    convert_svg_to_pdf,
)

from .render import (
    process_template_data,
    create_env,
    highlight,
    process_style,
    process_text_with_jinja,
    process_list_item_texts,
    process_list_items,
    space_bullets,
    encode_image,
    encode_images,
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
