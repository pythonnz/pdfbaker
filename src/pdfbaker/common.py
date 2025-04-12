"""Common functionality for document generation."""

import logging
import os
import select
import subprocess
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import pypdf
import yaml
from cairosvg import svg2pdf
from jinja2 import Template

from . import errors

__all__ = [
    "combine_pdfs",
    "compress_pdf",
    "convert_svg_to_pdf",
    "deep_merge",
    "resolve_config",
]

logger = logging.getLogger(__name__)


def deep_merge(base: dict[str, Any], update: dict[str, Any]) -> dict[str, Any]:
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


def resolve_config(config: dict) -> dict:
    """Resolve all template strings in config using its own values.

    Args:
        config: Configuration dictionary with template strings

    Returns:
        Resolved configuration dictionary

    Raises:
        ValueError: If maximum number of iterations is reached
            (likely due to circular references)
    """
    max_iterations = 10
    for _ in range(max_iterations):
        config_yaml = Template(yaml.dump(config))
        resolved_yaml = config_yaml.render(**config)
        new_config = yaml.safe_load(resolved_yaml)

        if new_config == config:  # No more changes
            return new_config
        config = new_config

    raise ValueError(
        "Maximum number of iterations reached. "
        "Check for circular references in your configuration."
    )


def combine_pdfs(
    pdf_files: Sequence[Path], output_file: Path
) -> Path | errors.PDFCombineError:
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
        raise errors.PDFCombineError("No PDF files provided to combine")

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
                                "PDF %s has broken annotations. "
                                "Falling back to page-by-page method.",
                                pdf_file,
                            )
                            for page in pdf_reader.pages:
                                pdf_writer.add_page(page)
                        else:
                            raise
                except Exception as exc:
                    raise errors.PDFCombineError(
                        f"Failed to combine PDFs: {exc}"
                    ) from exc
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

    with subprocess.Popen(
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
) -> Path | errors.PDFCompressionError:
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
    except subprocess.SubprocessError as exc:
        raise errors.PDFCompressionError(
            f"Ghostscript compression failed: {exc}"
        ) from exc


def convert_svg_to_pdf(
    svg_path: Path,
    pdf_path: Path,
    backend: str = "cairosvg",
) -> Path | errors.SVGConversionError:
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
    try:
        if backend == "inkscape":
            try:
                _run_subprocess_logged(
                    [
                        "inkscape",
                        f"--export-filename={pdf_path}",
                        str(svg_path),
                    ]
                )
            except subprocess.SubprocessError as exc:
                raise errors.SVGConversionError(svg_path, backend, str(exc)) from exc
        else:
            try:
                with open(svg_path, "rb") as svg_file:
                    svg2pdf(file_obj=svg_file, write_to=str(pdf_path))
            except Exception as exc:
                raise errors.SVGConversionError(svg_path, backend, str(exc)) from exc

        return pdf_path
    except Exception as exc:
        raise errors.SVGConversionError(svg_path, backend, str(exc)) from exc
