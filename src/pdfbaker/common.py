"""Common functionality for document generation."""

import logging
import os
import select
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


def _run_subprocess_logged(cmd, check=True, env=None):
    """Run a subprocess with output redirected to logging.

    Args:
        cmd: Command and arguments to run
        check: If True, raise CalledProcessError on non-zero exit
        env: Optional environment variables to set

    Returns:
        Return code from process
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

    if ret_code != 0 and check:
        raise subprocess.CalledProcessError(ret_code, cmd)

    return ret_code


def compress_pdf(input_pdf, output_pdf, dpi=300):
    """Compress a PDF file using Ghostscript."""
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
            input_pdf,
        ]
    )
    return output_pdf


def combine_pdfs(pdf_files, output_file):
    """Combine multiple PDF files into a single PDF."""
    pdf_writer = pypdf.PdfWriter()

    with open(output_file, "wb") as output_stream:
        for pdf_file in pdf_files:
            with open(pdf_file, "rb") as file_obj:
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
        pdf_writer.write(output_stream)

    return output_file


def convert_svg_to_pdf(svg_path, pdf_path, backend="cairosvg"):
    """Convert an SVG file to PDF."""
    if backend == "inkscape":
        try:
            _run_subprocess_logged(
                [
                    "inkscape",
                    f"--export-filename={pdf_path}",
                    svg_path,
                ]
            )
        except subprocess.SubprocessError as exc:
            raise RuntimeError(
                "Inkscape command failed. Please ensure Inkscape is installed "
                'and in your PATH or set svg2pdf_backend to "cairosvg" in your config.'
            ) from exc
    else:
        with open(svg_path, "rb") as svg_file:
            svg2pdf(file_obj=svg_file, write_to=pdf_path)

    return pdf_path
