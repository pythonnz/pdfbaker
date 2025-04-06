"""Common functionality for document generation."""

import subprocess

import pypdf
import yaml

try:
    from cairosvg import svg2pdf

    CAIROSVG_AVAILABLE = True
except ImportError:
    CAIROSVG_AVAILABLE = False


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
                        print(
                            f"Warning: PDF {pdf_file} has broken annotations. "
                            f"Falling back to page-by-page method."
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
        return _convert_with_inkscape(svg_path, pdf_path)
    return _convert_with_cairosvg(svg_path, pdf_path)


def _convert_with_cairosvg(svg_path, pdf_path):
    """Convert SVG to PDF using CairoSVG."""
    if not CAIROSVG_AVAILABLE:
        raise ImportError(
            "CairoSVG is not installed. Please install it with 'pip install cairosvg' "
            "or set svg2pdf_backend to 'inkscape' in your config."
        )

    with open(svg_path, "rb") as svg_file:
        svg2pdf(file_obj=svg_file, write_to=pdf_path)

    return pdf_path


def _convert_with_inkscape(svg_path, pdf_path):
    """Convert SVG to PDF using Inkscape."""
    try:
        subprocess.run(
            [
                "inkscape",
                f"--export-filename={pdf_path}",
                svg_path,
            ],
            check=True,
        )
        return pdf_path
    except (subprocess.SubprocessError, FileNotFoundError) as exc:
        raise RuntimeError(
            "Inkscape command failed. Please ensure Inkscape is installed "
            "and in your PATH or set svg2pdf_backend to 'cairosvg' in your config."
        ) from exc
