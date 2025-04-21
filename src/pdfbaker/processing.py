"""Helper functions for custom processing."""


def wordwrap(text: str, max_chars: int = 60) -> list[str]:
    """Split text into lines with a maximum width, breaking at word boundaries.

    Args:
        text: The text to wrap
        max_chars: Maximum number of characters per line

    Returns:
        List of strings, one for each line
    """
    if not text:
        return []

    words = text.split()
    lines = []
    current_line = []
    current_width = 0

    for word in words:
        if current_width + len(word) + int(current_width > 0) <= max_chars:
            # Word still fits in current line
            current_line.append(word)
            current_width += len(word) + int(current_width > 0)
        else:
            # Word is too long, start a new line
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
            current_width = len(word)

    if current_line:
        lines.append(" ".join(current_line))

    return lines
