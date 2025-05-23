"""Main entry point for pdfbaker (CLI)."""

import logging
import sys
from pathlib import Path

import rich_click as click

from pdfbaker import __version__
from pdfbaker.baker import Baker, BakerOptions
from pdfbaker.console import HELP_CONFIG
from pdfbaker.errors import (
    DocumentNotFoundError,
    DryRunCreateFromCompleted,
    PDFBakerError,
)

logger = logging.getLogger(__name__)


@click.command()
@click.version_option(version=__version__, prog_name="pdfbaker")
@click.argument(
    "config_file",
    type=click.Path(exists=False, dir_okay=False, path_type=Path),
)
@click.argument("document_names", nargs=-1)
@click.option("-q", "--quiet", is_flag=True, help="Show errors only.")
@click.option("-v", "--verbose", is_flag=True, help="Show debug information.")
@click.option(
    "-t",
    "--trace",
    is_flag=True,
    help="Show trace information (maximum details).",
)
@click.option(
    "--keep-build", is_flag=True, help="Keep rendered SVGs and single-page PDFs."
)
@click.option(
    "--debug", is_flag=True, help="Debug mode (implies --verbose and --keep-build)."
)
@click.option(
    "--fail-if-exists",
    is_flag=True,
    help="Abort if a target PDF already exists.",
)
@click.option("--dry-run", is_flag=True, help="Do not write any files.")
@click.option(
    "--create-from",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    metavar="SVG_FILE",
    help="Scaffold CONFIG_FILE and supporting files for your existing SVG.",
)
@click.rich_config(help_config=HELP_CONFIG)
# pylint: disable=too-many-arguments,too-many-positional-arguments
def cli(
    config_file: Path,
    document_names: tuple[str, ...],
    quiet: bool,
    verbose: bool,
    trace: bool,
    keep_build: bool,
    debug: bool,
    fail_if_exists: bool,
    dry_run: bool,
    create_from: Path | None,
) -> None:
    """Generate PDF documents from YAML-configured SVG templates.

    Specify one or more document names to only process those.
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
            fail_if_exists=fail_if_exists,
            dry_run=dry_run,
            create_from=create_from,
        )
        baker = Baker(config_file, options=options)
        success = baker.bake(document_names=document_names)
        sys.exit(0 if success else 1)
    except DryRunCreateFromCompleted:
        sys.exit(0)
    except FileExistsError as exc:
        logger.error("❌ %s", str(exc))
        sys.exit(2)
    except FileNotFoundError as exc:
        logger.error("❌ %s", str(exc))
        sys.exit(2)
    except DocumentNotFoundError as exc:
        logger.error("❌ %s", str(exc))
        sys.exit(2)
    except PDFBakerError as exc:
        logger.error("❌ %s", str(exc))
        sys.exit(1)


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
