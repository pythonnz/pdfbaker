"""Tests for configuration functionality."""

from pathlib import Path

import pytest
import yaml

from pdfbaker.config import PDFBakerConfiguration, deep_merge, render_config
from pdfbaker.errors import ConfigurationError


# Dictionary merging tests
def test_deep_merge_basic() -> None:
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


def test_deep_merge_nested() -> None:
    """Test nested dictionary merging."""
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


def test_deep_merge_empty() -> None:
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


# Configuration initialization tests
def test_configuration_init_with_dict(tmp_path: Path) -> None:
    """Test initializing Configuration with a dictionary."""
    config_file = tmp_path / "test.yaml"
    config_file.write_text(yaml.dump({"title": "Document"}))

    config = PDFBakerConfiguration({}, config_file)
    assert config["title"] == "Document"


def test_configuration_init_with_path(tmp_path: Path) -> None:
    """Test initializing Configuration with a file path."""
    config_file = tmp_path / "test.yaml"
    config_file.write_text(yaml.dump({"title": "Document"}))

    config = PDFBakerConfiguration({}, config_file)
    assert config["title"] == "Document"
    assert config["directories"]["config"] == tmp_path


def test_configuration_init_with_directory(tmp_path: Path) -> None:
    """Test initializing Configuration with custom directory."""
    config_file = tmp_path / "test.yaml"
    config_file.write_text(yaml.dump({"title": "Document"}))

    config = PDFBakerConfiguration({}, config_file)
    assert config["title"] == "Document"
    assert config["directories"]["config"] == tmp_path


def test_configuration_init_invalid_yaml(tmp_path: Path) -> None:
    """Test configuration with invalid YAML."""
    config_file = tmp_path / "invalid.yaml"
    config_file.write_text("invalid: [yaml: content")

    with pytest.raises(ConfigurationError, match="Failed to load config file"):
        PDFBakerConfiguration({}, config_file)


# Path resolution tests
def test_configuration_resolve_path(tmp_path: Path) -> None:
    """Test path resolution."""
    config_file = tmp_path / "test.yaml"
    config_file.write_text(yaml.dump({"template": "test.yaml"}))

    config = PDFBakerConfiguration({}, config_file)

    # Test relative path
    assert config.resolve_path("test.yaml") == tmp_path / "test.yaml"

    # Test absolute path
    assert config.resolve_path({"path": "/absolute/path.yaml"}) == Path(
        "/absolute/path.yaml"
    )

    # Test named path
    assert config.resolve_path({"name": "test.yaml"}) == tmp_path / "test.yaml"


def test_configuration_resolve_path_invalid(tmp_path: Path) -> None:
    """Test invalid path specification."""
    config_file = tmp_path / "test.yaml"
    config_file.write_text(yaml.dump({}))

    config = PDFBakerConfiguration({}, config_file)
    with pytest.raises(ConfigurationError, match="Invalid path specification"):
        config.resolve_path({})


# Configuration rendering tests
def test_render_config_basic() -> None:
    """Test basic template rendering in configuration."""
    config = {
        "name": "test",
        "title": "{{ name }} document",
        "nested": {
            "value": "{{ title }}",
        },
    }

    rendered = render_config(config)
    assert rendered["title"] == "test document"
    assert rendered["nested"]["value"] == "test document"


def test_render_config_circular() -> None:
    """Test detection of circular references in config rendering."""
    config = {
        "a": "{{ b }}",
        "b": "{{ a }}",
    }

    with pytest.raises(ConfigurationError, match="(?i).*circular.*"):
        render_config(config)


# Utility method tests
def test_configuration_pretty(tmp_path: Path) -> None:
    """Test configuration pretty printing."""
    config_file = tmp_path / "test.yaml"
    config_file.write_text(
        yaml.dump(
            {
                "title": "Test",
                "content": "A" * 100,  # Long string that should be truncated
            }
        )
    )

    config = PDFBakerConfiguration({}, config_file)
    pretty = config.pretty(max_chars=20)
    assert "…" in pretty  # Should show truncation
    assert "Test" in pretty
