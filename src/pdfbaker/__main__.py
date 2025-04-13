"""Main entry point for pdfbaker (CLI)."""

import logging
import sys
from pathlib import Path

import click

from pdfbaker import __version__
from pdfbaker.baker import PDFBaker
from pdfbaker.errors import PDFBakeError

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
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
@click.option(
    "--debug", is_flag=True, help="Debug mode (implies --verbose, keeps build files)"
)
@click.option("-v", "--verbose", is_flag=True, help="Show debug information")
@click.option("-q", "--quiet", is_flag=True, help="Show errors only")
def bake(config_file: Path, debug: bool, verbose: bool, quiet: bool) -> int:
    """Parse config file and bake PDFs."""
    if debug:
        verbose = True
    if quiet:
        logging.getLogger().setLevel(logging.ERROR)
    elif verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    try:
        baker = PDFBaker(config_file)
        baker.bake(debug=debug)
        return 0
    except PDFBakeError as exc:
        logger.error(str(exc))
        return 1


if __name__ == "__main__":
    sys.exit(cli())
