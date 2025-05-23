"""Constants and functions for the console UI."""

from collections.abc import Generator
from pathlib import Path
from typing import TYPE_CHECKING

import rich_click as click
from rich.console import Console, Group, group
from rich.markup import escape
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.theme import Theme
from rich.tree import Tree

if TYPE_CHECKING:
    from .baker import ProcessedDoc

__all__ = [
    "build_create_from_panel",
    "build_outcome_panel",
    "HELP_CONFIG",
    "RICH_THEME",
    "stdout_console",
    "stderr_console",
    "SYNTAX_THEME",
]


HELP_CONFIG = click.RichHelpConfiguration(
    style_option="bold cyan",
    style_argument="bold cyan",
    style_command="bold cyan",
    style_switch="bold green",
    style_metavar="bold yellow",
    style_metavar_separator="dim",
    style_usage="bold yellow",
    style_usage_command="bold",
    style_helptext_first_line="",
    style_helptext="dim",
    style_option_default="dim",
    style_required_short="red",
    style_required_long="dim red",
    style_options_panel_border="dim",
    style_commands_panel_border="dim",
)
RICH_THEME = Theme(
    {
        "logging.level.info": "cyan",
        "logging.level.warning": "bold yellow",
        "logging.level.error": "bold red",
        "logging.level.success": "green",
        "logging.level.debug": "dim",
        "logging.level.trace": "dim",
        "repr.ellipsis": "",  # don't highlight
        "repr.indent": "dim green",
        "repr.error": "bold red",
        "repr.str": "green",
        "repr.brace": "",  # don't highlight
        "repr.comma": "bold",
        "repr.ipv4": "bold bright_green",
        "repr.ipv6": "bold bright_green",
        "repr.eui48": "bold bright_green",
        "repr.eui64": "bold bright_green",
        "repr.tag_start": "bold",
        "repr.tag_name": "bold bright_magenta",
        "repr.tag_contents": "default",
        "repr.tag_end": "bold",
        "repr.attrib_name": "yellow",
        "repr.attrib_equal": "bold",
        "repr.attrib_value": "magenta",
        "repr.number": "bold cyan",
        "repr.number_complex": "bold cyan",
        "repr.bool_true": "italic bright_green",
        "repr.bool_false": "italic bright_red",
        "repr.none": "italic magenta",
        "repr.url": "underline bright_blue",
        "repr.uuid": "bright_yellow",
        "repr.call": "bold magenta",
        "repr.path": "magenta",
        "repr.filename": "bright_magenta",
    }
)
SYNTAX_THEME = "ansi_light"

stdout_console = Console(theme=RICH_THEME)
stderr_console = Console(stderr=True, theme=RICH_THEME)


def _build_directory_tree(root: Path) -> Tree:
    """Return a Rich Tree representing the directory structure starting from `root`."""

    def walk_directory(directory: Path, tree: Tree) -> None:
        paths = sorted(
            directory.iterdir(),
            key=lambda path: (path.is_file(), path.name.lower()),
        )
        for path in paths:
            if path.is_dir():
                branch = tree.add(
                    f"[bold magenta]:open_file_folder: [link file://{path}]{escape(path.name)}"
                )
                walk_directory(path, branch)
            else:
                suffix = path.suffix
                if path.suffix == ".j2":
                    suffix = path.with_suffix("").suffix
                icon = {
                    ".yaml": "page_facing_up",
                    ".svg": "framed_picture",
                }.get(suffix, "page_facing_up")
                tree.add(
                    Text.from_markup(
                        f":{icon}: [link file://{path}]{escape(path.name)}"
                    )
                )

    tree = Tree(f":open_file_folder: [link file://{root}]{root.resolve()}")
    walk_directory(root, tree)
    return tree


def build_create_from_panel(create_from, project_dir):
    """Return a Rich Panel for showing --create-from results."""
    return Panel(
        Group(
            f"[green]Created from {create_from}:[/green]",
            _build_directory_tree(project_dir),
        ),
        title=":white_check_mark: Success",
        title_align="left",
        border_style="green",
    )


@group()
def _get_outcome_items(
    processed_docs: list["ProcessedDoc"],
    dry_run: bool,
    keep_build: bool,
    build_dir: Path,
) -> Generator:
    """Yield the items making up the outcome panel."""
    total_pdfs = sum(len(d.pdf_files) for d in processed_docs if d.pdf_files)
    total_failures = sum(1 for d in processed_docs if d.error_message)
    summary = Text()
    if dry_run:
        summary.append(
            f"Would have created {total_pdfs} PDF{'s' if total_pdfs != 1 else ''}.",
            style="yellow",
        )
    else:
        if total_pdfs:
            summary.append(
                f"Created {total_pdfs} PDF{'s' if total_pdfs != 1 else ''}.",
                style="green",
            )
        else:
            summary.append(
                "No PDFs were created.",
                style="yellow",
            )
    if total_failures:
        summary.append(
            f" Failed to process {total_failures} document"
            f"{'s' if total_failures != 1 else ''}",
            style="red",
        )
    yield summary

    table = Table.grid(padding=(0, 1))
    table.add_column(justify="left", style="bold")
    table.add_column(justify="left")

    for doc in processed_docs:
        name = (
            doc.document.config.name
            if hasattr(doc.document, "config")
            else str(doc.document)
        )
        if hasattr(doc.document, "config") and getattr(
            doc.document.config, "is_variant", False
        ):
            name += f' variant "{doc.document.config.variant["name"]}"'

        if doc.pdf_files:
            emoji = "no_entry_sign" if dry_run else "white_check_mark"
            for i, pdf in enumerate(doc.pdf_files):
                left = name if i == 0 else ""
                table.add_row(
                    left,
                    Text.from_markup(
                        f":{emoji}: [link=file://{pdf}]{pdf}[/link]",
                        style="yellow" if dry_run else "green",
                    ),
                )

        if doc.error_message:
            table.add_row(
                name,
                Text.from_markup(f":cross_mark: [red]{doc.error_message}[/red]"),
            )
            if hasattr(doc.document, "config") and doc.document.config.keep_build:
                table.add_row(
                    "",
                    Text(
                        f"Build files kept in: {doc.document.config.directories.build}",
                        style="cyan",
                    ),
                )
    yield table

    if keep_build and not dry_run:
        yield Text(f"Build files kept in: {build_dir}", style="cyan")


def build_outcome_panel(
    processed_docs: list["ProcessedDoc"],
    dry_run: bool,
    keep_build: bool,
    build_dir: Path,
) -> Panel:
    """Return a Rich Panel summarizing the outcome of processing documents."""
    total_pdfs = sum(len(d.pdf_files) for d in processed_docs if d.pdf_files)
    total_failures = sum(1 for d in processed_docs if d.error_message)

    if total_pdfs and not total_failures:
        outcome_emoji = "white_check_mark"
        outcome_title = "Success"
        border_style = "green"
    elif total_failures and not total_pdfs:
        outcome_emoji = "cross_mark"
        outcome_title = "Failure"
        border_style = "bold red"
    else:
        outcome_emoji = "yellow_square"
        outcome_title = "There were errors" if total_failures else "Warning"
        border_style = "bold yellow"
    if dry_run:
        outcome_title = f"[DRY RUN] {outcome_title}"

    return Panel(
        _get_outcome_items(
            processed_docs=processed_docs,
            dry_run=dry_run,
            keep_build=keep_build,
            build_dir=build_dir,
        ),
        title=f":{outcome_emoji}: {outcome_title}",
        title_align="left",
        border_style=border_style,
    )
