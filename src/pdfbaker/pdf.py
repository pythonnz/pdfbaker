"""PDF-related functions."""

import logging
import os
import select
import subprocess  # nosec B404
from collections.abc import Sequence
from pathlib import Path

import pypdf
from cairosvg import svg2pdf

from .config import SVG2PDFBackend
from .errors import (
    PDFCombineError,
    PDFCompressionError,
    SVGConversionError,
)

__all__ = [
    "combine_pdfs",
    "compress_pdf",
    "convert_svg_to_pdf",
]

logger = logging.getLogger(__name__)


def combine_pdfs(
    pdf_files: Sequence[Path], output_file: Path
) -> Path | PDFCombineError:
    """Combine multiple PDF files into a single PDF.

    Args:
        pdf_files: List of paths to PDF files to combine
        output_file: Path where the combined PDF will be written

    Returns:
        Path to the combined PDF file

    Raises:
        PDFCombineError: If no PDF files provided or if combining fails
    """
    if not pdf_files:
        raise PDFCombineError("No PDF files provided to combine")

    pdf_writer = pypdf.PdfWriter()

    with open(output_file, "wb") as output_stream:
        for pdf_file in pdf_files:
            with open(pdf_file, "rb") as file_obj:
                try:
                    pdf_reader = pypdf.PdfReader(file_obj)
                    try:
                        pdf_writer.append(pdf_reader)
                    except KeyError as exc:
                        if str(exc) == "'/Subtype'":
                            # PDF has broken annotations with missing /Subtype
                            logger.warning(
                                "Broken annotations in PDF: %s"
                                "Falling back to page-by-page method.",
                                pdf_file,
                            )
                            for page in pdf_reader.pages:
                                pdf_writer.add_page(page)
                        else:
                            raise
                except Exception as exc:
                    raise PDFCombineError(f"Failed to combine PDFs: {exc}") from exc
        pdf_writer.write(output_stream)

    return output_file


def _run_subprocess_logged(cmd: list[str], env: dict[str, str] | None = None) -> int:
    """Run a subprocess with output redirected to logging.

    Args:
        cmd: Command and arguments to run
        env: Optional environment variables to set

    Returns:
        0 if successful, otherwise raises CalledProcessError
    """
    env = env or os.environ.copy()
    env["PYTHONUNBUFFERED"] = "True"

    with subprocess.Popen(  # nosec B603
        cmd,
        bufsize=1,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    ) as proc:
        # Set up select for both pipes
        readable = {
            proc.stdout.fileno(): (proc.stdout, logger.info),
            proc.stderr.fileno(): (proc.stderr, logger.warning),
        }

        while (ret_code := proc.poll()) is None:
            # Wait for output on either pipe
            ready, _, _ = select.select(readable.keys(), [], [])

            for fd in ready:
                stream, log = readable[fd]
                line = stream.readline()
                if line:
                    log(line.rstrip())

        # Read any remaining output after process exits
        for stream, log in readable.values():
            for line in stream:
                if line.strip():
                    log(line.rstrip())

    if ret_code != 0:
        raise subprocess.CalledProcessError(ret_code, cmd)

    return 0


def compress_pdf(
    input_pdf: Path, output_pdf: Path, dpi: int = 300
) -> Path | PDFCompressionError:
    """Compress a PDF file using Ghostscript.

    Args:
        input_pdf: Path to the input PDF file
        output_pdf: Path where the compressed PDF will be written
        dpi: Resolution in dots per inch (default: 300)

    Returns:
        Path to the compressed PDF file

    Raises:
        PDFCompressionError: If Ghostscript compression fails
    """
    try:
        _run_subprocess_logged(
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
                str(input_pdf),
            ]
        )
        return output_pdf
    except FileNotFoundError as exc:
        raise PDFCompressionError(f"Ghostscript not found: {exc}") from exc
    except subprocess.SubprocessError as exc:
        raise PDFCompressionError(f"Ghostscript compression failed: {exc}") from exc


def convert_svg_to_pdf(
    svg_path: Path,
    pdf_path: Path,
    backend: SVG2PDFBackend | str = SVG2PDFBackend.CAIROSVG,
) -> Path | SVGConversionError:
    """Convert an SVG file to PDF.

    Args:
        svg_path: Path to the input SVG file
        pdf_path: Path where the PDF will be written
        backend: Conversion backend to use, either "cairosvg" or "inkscape"
            (default: "cairosvg")

    Returns:
        Path to the converted PDF file

    Raises:
        SVGConversionError: If SVG conversion fails, includes the backend used and cause
    """
    if isinstance(backend, str):
        try:
            backend = SVG2PDFBackend(backend)
        except ValueError as exc:
            raise SVGConversionError(
                svg_path, backend, f'Unknown svg2pdf backend: "{backend}"'
            ) from exc

    if backend == SVG2PDFBackend.INKSCAPE:
        try:
            _run_subprocess_logged(
                [
                    "inkscape",
                    f"--export-filename={pdf_path}",
                    str(svg_path),
                ]
            )
        except subprocess.SubprocessError as exc:
            raise SVGConversionError(svg_path, backend, str(exc)) from exc
    else:
        try:
            with open(svg_path, "rb") as svg_file:
                svg2pdf(file_obj=svg_file, write_to=str(pdf_path))
        except Exception as exc:
            raise SVGConversionError(svg_path, backend, str(exc)) from exc

    return pdf_path
