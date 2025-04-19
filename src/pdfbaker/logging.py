"""Logging mixin for pdfbaker classes."""

import logging
from typing import Any

TRACE = 5
logging.addLevelName(TRACE, "TRACE")


class LoggingMixin:
    """Mixin providing consistent logging functionality across pdfbaker classes."""

    def __init__(self) -> None:
        """Initialize logger for the class."""
        self.logger = logging.getLogger(self.__class__.__module__)

    def log_trace(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a trace message (more detailed than debug)."""
        self.logger.log(TRACE, msg, *args, **kwargs)

    def log_trace_preview(
        self, msg: str, *args: Any, max_chars: int = 500, **kwargs: Any
    ) -> None:
        """Log a trace preview of a potentially large message, truncating if needed."""
        self.logger.log(
            TRACE, truncate_strings(msg, max_chars=max_chars), *args, **kwargs
        )

    def log_trace_section(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a trace message as a main section header."""
        self.logger.log(TRACE, f"──── {msg} ────", *args, **kwargs)

    def log_trace_subsection(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a trace message as a subsection header."""
        self.logger.log(TRACE, f"  ── {msg} ──", *args, **kwargs)

    def log_debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a debug message."""
        self.logger.debug(msg, *args, **kwargs)

    def log_debug_section(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a debug message as a main section header."""
        self.logger.debug(f"──── {msg} ────", *args, **kwargs)

    def log_debug_subsection(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a debug message as a subsection header."""
        self.logger.debug(f"  ── {msg} ──", *args, **kwargs)

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
        self.logger.warning(msg, *args, **kwargs)

    def log_error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log an error message."""
        self.logger.error(f"**** {msg} ****", *args, **kwargs)

    def log_critical(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a critical message."""
        self.logger.critical(msg, *args, **kwargs)


def truncate_strings(obj, max_chars: int) -> Any:
    """Recursively truncate strings in nested structures."""
    if isinstance(obj, str):
        return obj if len(obj) <= max_chars else obj[:max_chars] + "…"
    if isinstance(obj, dict):
        return {
            truncate_strings(k, max_chars): truncate_strings(v, max_chars)
            for k, v in obj.items()
        }
    if isinstance(obj, list):
        return [truncate_strings(item, max_chars) for item in obj]
    if isinstance(obj, tuple):
        return tuple(truncate_strings(item, max_chars) for item in obj)
    if isinstance(obj, set):
        return {truncate_strings(item, max_chars) for item in obj}
    return obj
