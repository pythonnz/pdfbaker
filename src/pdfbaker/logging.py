"""Logging mixin for pdfbaker classes."""

import logging
import sys
from typing import Any

TRACE = 5
logging.addLevelName(TRACE, "TRACE")

__all__ = ["LoggingMixin", "setup_logging"]


class LoggingMixin:
    """Mixin providing consistent logging functionality across pdfbaker classes."""

    @property
    def logger(self) -> logging.Logger:
        """Return the named logger for this instance."""
        return logging.getLogger(self.__class__.__module__)

    def log_trace(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a trace message (more detailed than debug)."""
        self.logger.log(TRACE, f"🔍 {msg}", *args, **kwargs)

    def log_trace_preview(
        self, msg: str, *args: Any, max_chars: int = 500, **kwargs: Any
    ) -> None:
        """Log a trace preview of a potentially large message, truncating if needed."""
        if len(msg) > max_chars:
            msg = msg[:max_chars] + "(...)"
        self.logger.log(TRACE, f"🔍 \n{msg}", *args, **kwargs)

    def log_trace_section(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a trace message as a main section header."""
        self.logger.log(TRACE, f"🔍 ──── {msg} ────", *args, **kwargs)

    def log_trace_subsection(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a trace message as a subsection header."""
        self.logger.log(TRACE, f"🔍   ── {msg} ──", *args, **kwargs)

    def log_debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a debug message."""
        self.logger.debug(f"🔧 {msg}", *args, **kwargs)

    def log_debug_section(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a debug message as a main section header."""
        self.logger.debug(f"🔧 ──── {msg} ────", *args, **kwargs)

    def log_debug_subsection(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a debug message as a subsection header."""
        self.logger.debug(f"🔧   ── {msg} ──", *args, **kwargs)

    def log_info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log an info message."""
        self.logger.info(msg, *args, **kwargs)

    def log_info_section(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log an info message as a main section header."""
        self.logger.info(f"──── {msg} ────", *args, **kwargs)

    def log_info_subsection(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log an info message as a subsection header."""
        self.logger.info(f"  ── {msg} ──", *args, **kwargs)

    def log_warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a warning message."""
        self.logger.warning(f"⚠️ {msg}", *args, **kwargs)

    def log_error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log an error message."""
        self.logger.error(f"**** ❌ {msg} ****", *args, **kwargs)

    def log_critical(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a critical message."""
        self.logger.critical(f"**** 🚨 {msg} ****", *args, **kwargs)


def setup_logging(quiet=False, trace=False, verbose=False) -> None:
    """Set up logging for the application."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s: %(message)s")

    # stdout handler for TRACE/DEBUG/INFO
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    stdout_handler.setLevel(TRACE)
    stdout_handler.addFilter(lambda record: record.levelno < logging.WARNING)

    # stderr handler for WARNING and above
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(formatter)
    stderr_handler.setLevel(logging.WARNING)

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
