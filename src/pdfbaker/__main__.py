"""Main entry point for pdfbaker (CLI)."""

import logging
import sys
from pathlib import Path

import click

from pdfbaker import __version__
from pdfbaker.baker import PDFBaker, PDFBakerOptions
from pdfbaker.errors import PDFBakerError

logger = logging.getLogger(__name__)


@click.group()
@click.version_option(version=__version__, prog_name="pdfbaker")
def cli() -> None:
    """Generate PDF documents from YAML-configured SVG templates."""


@cli.command()
@click.argument(
    "config_file",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option("-q", "--quiet", is_flag=True, help="Show errors only")
@click.option("-v", "--verbose", is_flag=True, help="Show debug information")
@click.option(
    "-t",
    "--trace",
    is_flag=True,
    help="Show trace information (even more detailed than --verbose)",
)
@click.option("--keep-build", is_flag=True, help="Keep build artifacts")
@click.option("--debug", is_flag=True, help="Debug mode (--verbose and --keep-build)")
# pylint: disable=too-many-arguments,too-many-positional-arguments
def bake(
    config_file: Path,
    quiet: bool,
    verbose: bool,
    trace: bool,
    keep_build: bool,
    debug: bool,
) -> int:
    """Parse config file and bake PDFs."""
    if debug:
        verbose = True
        keep_build = True

    try:
        options = PDFBakerOptions(
            quiet=quiet,
            verbose=verbose,
            trace=trace,
            keep_build=keep_build,
        )
        baker = PDFBaker(config_file, options=options)
        success = baker.bake()
        sys.exit(0 if success else 1)
    except PDFBakerError as exc:
        logger.error(str(exc))
        sys.exit(1)


if __name__ == "__main__":
    cli()
