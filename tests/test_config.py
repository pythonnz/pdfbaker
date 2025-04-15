"""Tests for common functionality."""

from pathlib import Path

import pytest

from pdfbaker.config import PDFBakerConfiguration, deep_merge


def test_deep_merge_basic():
    """Test basic dictionary merging."""
    base = {
        "title": "Document",
        "style": {
            "font": "Helvetica",
            "size": 12,
        },
    }
    update = {
        "title": "Updated Document",
        "style": {
            "size": 14,
        },
        "author": "John Doe",
    }
    expected = {
        "title": "Updated Document",
        "style": {
            "font": "Helvetica",
            "size": 14,
        },
        "author": "John Doe",
    }
    assert deep_merge(base, update) == expected


def test_deep_merge_nested():
    """Test merging of nested dictionaries."""
    base = {
        "document": {
            "title": "Main Document",
            "meta": {
                "author": "Jane Smith",
                "date": "2024-01-01",
            },
        },
        "style": {
            "font": "Arial",
            "colors": {
                "text": "black",
                "background": "white",
            },
        },
    }
    update = {
        "document": {
            "meta": {
                "date": "2024-04-01",
                "version": "1.0",
            },
        },
        "style": {
            "colors": {
                "text": "navy",
            },
        },
    }
    expected = {
        "document": {
            "title": "Main Document",
            "meta": {
                "author": "Jane Smith",
                "date": "2024-04-01",
                "version": "1.0",
            },
        },
        "style": {
            "font": "Arial",
            "colors": {
                "text": "navy",
                "background": "white",
            },
        },
    }
    assert deep_merge(base, update) == expected


def test_deep_merge_empty():
    """Test merging with empty dictionaries."""
    base = {
        "title": "Document",
        "style": {
            "font": "Helvetica",
        },
    }
    update = {}
    # Merging empty into non-empty should return non-empty
    assert deep_merge(base, update) == base
    # Merging non-empty into empty should return non-empty
    # pylint: disable=arguments-out-of-order
    assert deep_merge(update, base) == base


def test_configuration_init_with_dict():
    """Test initializing Configuration with a dictionary."""
    config = PDFBakerConfiguration({}, {"title": "Document"})
    assert config["title"] == "Document"


def test_configuration_init_with_path(tmp_path):
    """Test initializing Configuration with a file path."""
    config_file = tmp_path / "test.yaml"
    config_file.write_text("title: Document")

    config = PDFBakerConfiguration({}, config_file)
    assert config["title"] == "Document"
    assert config.directory == tmp_path


def test_configuration_init_with_directory(tmp_path):
    """Test initializing Configuration with custom directory."""
    config_file = tmp_path / "test.yaml"
    config_file.write_text('{"title": "Document"}')
    config = PDFBakerConfiguration({}, config_file)
    assert config["title"] == "Document"
    assert config.directory == tmp_path


def test_configuration_resolve_path():
    """Test path resolution."""
    config = PDFBakerConfiguration({}, {"template": "test.yaml"})
    config.directory = Path("/base")  # Set directory explicitly for testing
    assert config.resolve_path("test.yaml") == Path("/base/test.yaml")
    assert config.resolve_path({"path": "/absolute/path.yaml"}) == Path(
        "/absolute/path.yaml"
    )
    assert config.resolve_path({"name": "test.yaml"}) == Path("/base/test.yaml")


def test_configuration_resolve_path_invalid():
    """Test invalid path specification."""
    config = PDFBakerConfiguration({}, {})
    with pytest.raises(ValueError, match="Invalid path specification"):
        config.resolve_path({})
