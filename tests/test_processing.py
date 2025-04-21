"""Tests for processing functions."""

from pdfbaker.processing import wordwrap


def test_wordwrap_empty_input():
    """Test wordwrap with empty inputs."""
    assert not wordwrap("")
    assert not wordwrap(" ")
    assert not wordwrap("   ")


def test_wordwrap_normal_text():
    """Test wordwrap with normal text."""
    text = "This is a simple test for word wrapping functionality."
    # Max width 20 chars
    expected = ["This is a simple", "test for word", "wrapping", "functionality."]
    assert wordwrap(text, max_chars=20) == expected

    # Default max width (60 chars)
    assert wordwrap(text) == [text]  # Should fit on one line with default width


def test_wordwrap_long_words():
    """Test wordwrap with words longer than the max width."""
    # Single word longer than max width
    assert wordwrap("supercalifragilisticexpialidocious", max_chars=10) == [
        "supercalifragilisticexpialidocious"
    ]

    # Mixed text with one long word
    text = "This has a supercalifragilisticexpialidocious word in it."
    expected = ["This has a", "supercalifragilisticexpialidocious", "word in it."]
    assert wordwrap(text, max_chars=15) == expected


def test_wordwrap_edge_cases():
    """Test wordwrap with various edge cases."""
    # Text with exactly max width
    assert wordwrap("1234567890", max_chars=10) == ["1234567890"]

    # Text with multiple spaces
    assert wordwrap("word1    word2", max_chars=20) == ["word1 word2"]

    # Line just at the boundary
    text = "one two three four"
    assert wordwrap(text, max_chars=13) == ["one two three", "four"]

    # Really large max_chars
    assert wordwrap("short text", max_chars=1000) == ["short text"]


def test_wordwrap_newlines():
    """Test that newlines in the input are treated as spaces."""
    text = "Line one\nLine two\nLine three"
    expected = ["Line one Line two", "Line three"]
    assert wordwrap(text, max_chars=20) == expected


def test_wordwrap_long_word_with_following_words():
    """Test that processing continues after a long word."""
    text = "supercalifragilisticexpialidocious is followed by more words"
    result = wordwrap(text, 10)

    assert result == [
        "supercalifragilisticexpialidocious",
        "is",
        "followed",
        "by more",
        "words",
    ]
