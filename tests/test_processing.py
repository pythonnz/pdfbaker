"""Tests for processing functions."""

from pdfbaker.processing import wordwrap


def test_wordwrap_empty_input():
    """wordwrap: returns empty list for empty or whitespace input."""
    assert not wordwrap("")
    assert not wordwrap(" ")
    assert not wordwrap("   ")


def test_wordwrap_normal_text():
    """wordwrap: wraps text at max_chars boundary."""
    text = "This is a simple test for word wrapping functionality."
    # Max width 20 chars
    expected = ["This is a simple", "test for word", "wrapping", "functionality."]
    assert wordwrap(text, max_chars=20) == expected

    # Default max width (60 chars)
    assert wordwrap(text) == [text]  # Should fit on one line with default width


def test_wordwrap_long_words():
    """wordwrap: handles words longer than max_chars."""
    text = "Supercalifragilisticexpialidocious"
    assert wordwrap(text, max_chars=10) == [text]


def test_wordwrap_edge_cases():
    """wordwrap: handles edge cases with punctuation and short lines."""
    text = "Hello, world!"
    assert wordwrap(text, max_chars=5) == ["Hello,", "world!"]
    text = "A B C D E F G"
    assert wordwrap(text, max_chars=3) == ["A B", "C D", "E F", "G"]


def test_wordwrap_newlines():
    """wordwrap: newlines are whitespace, only wraps at word boundaries."""
    text = "Line1\nLine2 Line3"
    assert wordwrap(text, max_chars=10) == ["Line1", "Line2", "Line3"]


def test_wordwrap_long_word_with_following_words():
    """wordwrap: long word at start followed by short words."""
    text = "Supercalifragilisticexpialidocious is fun"
    assert wordwrap(text, max_chars=10) == [
        "Supercalifragilisticexpialidocious",
        "is fun",
    ]
