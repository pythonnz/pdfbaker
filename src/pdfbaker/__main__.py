"""Main entry point for pdfbaker (CLI)."""

import logging
import sys
from pathlib import Path

import click

from pdfbaker import __version__
from pdfbaker.baker import Baker, BakerOptions
from pdfbaker.errors import DocumentNotFoundError, PDFBakerError

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
@click.argument("documents", nargs=-1)
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
    documents: tuple[str, ...],
    quiet: bool,
    verbose: bool,
    trace: bool,
    keep_build: bool,
    debug: bool,
) -> int:
    """Parse config file and bake PDFs.

    Optionally specify one or more document names to only process those documents.
    """
    if debug:
        verbose = True
        keep_build = True

    try:
        options = BakerOptions(
            quiet=quiet,
            verbose=verbose,
            trace=trace,
            keep_build=keep_build,
        )
        baker = Baker(config_file, options=options)
        success = baker.bake(document_names=documents if documents else None)
        sys.exit(0 if success else 1)
    except DocumentNotFoundError as exc:
        logger.error("❌ %s", str(exc))
        sys.exit(2)
    except PDFBakerError as exc:
        logger.error("❌ %s", str(exc))
        sys.exit(1)


if __name__ == "__main__":
    cli()
