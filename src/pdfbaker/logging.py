"""Logging mixin for pdfbaker classes."""

import logging
from typing import Any

from rich.logging import RichHandler
from rich.syntax import Syntax
from rich.text import Text

from .console import SYNTAX_THEME, stderr_console, stdout_console

TRACE = 5
logging.addLevelName(TRACE, "TRACE")
TRACE_PREVIEW_MAX_CHARS = 500

__all__ = ["LoggingMixin", "setup_logging"]


class LoggingMixin:
    """Mixin providing consistent logging functionality across pdfbaker classes."""

    @property
    def logger(self) -> logging.Logger:
        """Return the named logger for this instance."""
        return logging.getLogger(self.__class__.__module__)

    def _log(
        self,
        level: int,
        msg: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Internal log method to handle highlighting and markup."""
        markup = kwargs.pop("markup", True)
        extra = {"markup": markup}
        if not kwargs.pop("highlight", True):
            extra["highlighter"] = None
        syntax = kwargs.pop("syntax", None)
        if syntax:
            msg = Syntax(msg, syntax, theme=SYNTAX_THEME)
        elif markup:
            msg = Text.from_markup(msg)
        self.logger.log(level, msg, *args, stacklevel=3, extra=extra, **kwargs)

    def log_trace(
        self,
        msg: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Log a trace message (more detailed than debug)."""
        self._log(
            TRACE,
            f":magnifying_glass_tilted_left: {msg}",
            *args,
            **kwargs,
        )

    def log_trace_preview(
        self,
        msg: str,
        *args: Any,
        syntax: str | None = None,
        max_chars: int = TRACE_PREVIEW_MAX_CHARS,
        **kwargs: Any,
    ) -> None:
        """Log a trace preview of a potentially large message, truncating if needed."""
        if max_chars is not None and len(msg) > max_chars:
            msg = msg[:max_chars] + "(...)"
        self._log(
            TRACE,
            msg,
            *args,
            highlight=False,
            markup=False,
            syntax=syntax,
            **kwargs,
        )

    def log_trace_section(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a trace message as a main section header."""
        self._log(
            TRACE, f":magnifying_glass_tilted_left: ──── {msg} ────", *args, **kwargs
        )

    def log_trace_subsection(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a trace message as a subsection header."""
        self._log(
            TRACE,
            f":magnifying_glass_tilted_left:   ── {msg} ──",
            *args,
            **kwargs,
        )

    def log_debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a debug message."""
        self._log(logging.DEBUG, f":wrench: {msg}", *args, **kwargs)

    def log_debug_section(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a debug message as a main section header."""
        self._log(logging.DEBUG, f":wrench: ──── {msg} ────", *args, **kwargs)

    def log_debug_subsection(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a debug message as a subsection header."""
        self._log(logging.DEBUG, f":wrench:   ── {msg} ──", *args, **kwargs)

    def log_info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log an info message."""
        self._log(logging.INFO, msg, *args, **kwargs)

    def log_info_section(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log an info message as a main section header."""
        self._log(logging.INFO, f"──── {msg} ────", *args, **kwargs)

    def log_info_subsection(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log an info message as a subsection header."""
        self._log(logging.INFO, f"  ── {msg} ──", *args, **kwargs)

    def log_warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a warning message."""
        self._log(logging.WARNING, f":fire: {msg}", *args, **kwargs)

    def log_error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log an error message."""
        self._log(
            logging.ERROR,
            f"**** :cross_mark: {msg} ****",
            *args,
            **kwargs,
        )


class RichHandlerWithSyntax(RichHandler):
    """Rich handler that prints Syntax objects as given."""

    def emit(self, record: logging.LogRecord) -> None:
        if isinstance(record.msg, Syntax):
            self.console.print(record.msg)
        else:
            super().emit(record)


def setup_logging(quiet=False, trace=False, verbose=False) -> None:
    """Set up rich logging for the application."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Handler for TRACE/DEBUG/INFO to stdout
    stdout_handler = RichHandlerWithSyntax(
        level=TRACE,
        console=stdout_console,
        omit_repeated_times=False,
        rich_tracebacks=True,
    )
    stdout_handler.addFilter(lambda record: record.levelno <= logging.INFO)

    # Handler for WARNING and above to stderr
    stderr_handler = RichHandlerWithSyntax(
        level=logging.WARNING,
        console=stderr_console,
        omit_repeated_times=False,
        show_path=True,
        rich_tracebacks=True,
    )

    # Remove existing console handlers, add ours
    for handler in logger.handlers[:]:
        if isinstance(handler, logging.StreamHandler) and not isinstance(
            handler, logging.FileHandler
        ):
            logger.removeHandler(handler)
    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)

    if quiet:
        logger.setLevel(logging.ERROR)
    elif trace:
        logger.setLevel(TRACE)
    elif verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
