"""Common functionality for document generation."""

import logging
import subprocess

import pypdf
import yaml
from cairosvg import svg2pdf

logger = logging.getLogger(__name__)


def deep_merge(base, update):
    """Recursively merge two dictionaries.

    Values in update will override those in base, except for dictionaries
    which will be merged recursively.
    """
    merged = base.copy()
    for key, value in update.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_pages(pages_dir):
    """Load page configurations from a specific subdirectory."""
    pages = {}

    if pages_dir.exists():
        for page in pages_dir.iterdir():
            if not page.name.endswith(".yml"):
                continue
            with open(page, encoding="utf-8") as f:
                yaml_config = yaml.safe_load(f)
                pages[yaml_config["name"]] = yaml_config["config"]

    return pages


def compress_pdf(input_pdf, output_pdf, dpi=300):
    """Compress a PDF file using Ghostscript."""
    subprocess.run(
        [
            "gs",
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.7",
            "-dPDFSETTINGS=/printer",
            f"-r{dpi}",
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            f"-sOutputFile={output_pdf}",
            input_pdf,
        ],
        check=True,
    )


def combine_pdfs(pdf_files, output_file):
    """Combine multiple PDF files into a single PDF."""
    pdf_writer = pypdf.PdfWriter()

    with open(output_file, "wb") as output_stream:
        for pdf_file in pdf_files:
            with open(pdf_file, "rb") as file_obj:
                pdf_reader = pypdf.PdfReader(file_obj)
                try:
                    # The proper method to assemble PDFs
                    pdf_writer.append(pdf_reader)
                except KeyError as exc:
                    # PDF has broken annotations with missing /Subtype
                    if str(exc) == "'/Subtype'":
                        logger.warning(
                            "PDF %s has broken annotations. "
                            "Falling back to page-by-page method.",
                            pdf_file,
                        )
                        for page in pdf_reader.pages:
                            pdf_writer.add_page(page)
                    else:
                        # Re-raise unexpected KeyError
                        raise
        pdf_writer.write(output_stream)


def convert_svg_to_pdf(svg_path, pdf_path, backend="cairosvg"):
    """Convert an SVG file to PDF.

    Args:
        svg_path: Path to input SVG file
        pdf_path: Path to output PDF file
        backend: Conversion backend to use (cairosvg or inkscape)

    Returns:
        Path to the generated PDF file
    """
    if backend == "inkscape":
        try:
            subprocess.run(
                [
                    "inkscape",
                    f"--export-filename={pdf_path}",
                    svg_path,
                ],
                check=True,
            )
        except (subprocess.SubprocessError, FileNotFoundError) as exc:
            raise RuntimeError(
                "Inkscape command failed. Please ensure Inkscape is installed "
                'and in your PATH or set svg2pdf_backend to "cairosvg" in your config.'
            ) from exc
    else:
        with open(svg_path, "rb") as svg_file:
            svg2pdf(file_obj=svg_file, write_to=pdf_path)

    return pdf_path
