"""Tests for configuration functionality."""

from pathlib import Path

import pytest
from ruamel.yaml import YAML
from ruamel.yaml.parser import ParserError

from pdfbaker.config import BaseConfig, Directories
from pdfbaker.config.baker import BakerConfig
from pdfbaker.errors import ConfigurationError


# Function to help with creating YAML content for tests
def write_yaml(path, data):
    """Write data to a YAML file using ruamel.yaml."""
    yaml = YAML()
    with open(path, "w", encoding="utf-8") as file:
        yaml.dump(data, file)


# BaseConfig merger tests
def test_base_config_merge_basic(default_directories) -> None:
    """Test basic config merging with BaseConfig."""

    class TestConfig(BaseConfig):
        """Test configuration class for basic merging."""

        title: str
        style: dict

    base = TestConfig(
        title="Document",
        style={
            "font": "Helvetica",
            "size": 12,
        },
        directories=default_directories,
    )

    update = {
        "title": "Updated Document",
        "style": {
            "size": 14,
        },
        "author": "John Doe",
    }

    merged = base.merge(update)
    assert merged.title == "Updated Document"
    assert merged.style == {"font": "Helvetica", "size": 14}
    assert merged.user_defined_settings.get("author") == "John Doe"


def test_base_config_merge_nested(default_directories) -> None:
    """Test nested config merging with BaseConfig."""

    class NestedConfig(BaseConfig):
        """Test configuration class for nested merging."""

        document: dict
        style: dict

    base = NestedConfig(
        document={
            "title": "Main Document",
            "meta": {
                "author": "Jane Smith",
                "date": "2024-01-01",
            },
        },
        style={
            "font": "Arial",
            "colors": {
                "text": "black",
                "background": "white",
            },
        },
        directories=default_directories,
    )

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

    merged = base.merge(update)
    assert merged.document["title"] == "Main Document"
    assert merged.document["meta"]["author"] == "Jane Smith"
    assert merged.document["meta"]["date"] == "2024-04-01"
    assert merged.document["meta"]["version"] == "1.0"
    assert merged.style["font"] == "Arial"
    assert merged.style["colors"]["text"] == "navy"
    assert merged.style["colors"]["background"] == "white"


def test_base_config_merge_empty(default_directories) -> None:
    """Test merging with empty dictionary."""

    class SimpleConfig(BaseConfig):
        """Test configuration class for empty dict merging."""

        title: str
        style: dict

    base = SimpleConfig(
        title="Document",
        style={
            "font": "Helvetica",
        },
        directories=default_directories,
    )

    update = {}
    # Merging empty into non-empty should return equivalent of non-empty
    merged = base.merge(update)
    assert merged.title == base.title
    assert merged.style == base.style


# Configuration initialization tests
def test_baker_config_init_with_file(
    tmp_path: Path, default_directories: Directories
) -> None:
    """Test initializing BakerConfig with a file."""
    config_file = tmp_path / "test.yaml"
    write_yaml(
        config_file,
        {
            "documents": [
                {"path": "doc1", "name": "doc1"},
                {"path": "doc2", "name": "doc2"},
            ],
            "directories": default_directories.model_dump(mode="json"),
        },
    )

    config = BakerConfig(config_file=config_file)
    assert len(config.documents) == 2
    assert config.config_file == config_file


def test_baker_config_custom_directories(
    tmp_path: Path, default_directories: Directories
) -> None:
    """Test initializing BakerConfig with custom directories."""
    config_file = tmp_path / "test.yaml"
    custom_dirs = default_directories.model_dump(mode="json")
    custom_dirs["build"] = str(tmp_path / "custom_build")

    config_data = {
        "documents": [{"path": "doc1", "name": "doc1"}],
        "directories": custom_dirs,
    }

    write_yaml(config_file, config_data)
    config = BakerConfig(config_file=config_file)

    assert config.config_file == config_file
    assert len(config.documents) == 1
    assert config.documents[0].name == "doc1"


def test_baker_config_init_invalid_yaml(tmp_path: Path) -> None:
    """Test configuration with invalid YAML."""
    config_file = tmp_path / "invalid.yaml"
    with open(config_file, "w", encoding="utf-8") as f:
        f.write("invalid: [yaml: content")

    # Use ruamel.yaml's specific exception
    with pytest.raises(ParserError):
        BakerConfig(config_file=config_file)


# Path resolution tests
def test_config_resolve_path(tmp_path: Path, default_directories: Directories) -> None:
    """Test path resolution."""

    # Create a basic config for testing path resolution
    class TestConfig(BaseConfig):
        """Test configuration class for path resolution."""

        directories: Directories

    config = TestConfig(
        directories=default_directories,
    )

    # Test relative path
    path = Path("test.yaml")
    resolved = config.resolve_path(path)
    assert resolved == tmp_path / "test.yaml"

    # Test subdirectory path
    path = Path("subdir/test.yaml")
    resolved = config.resolve_path(path)
    assert resolved == tmp_path / "subdir/test.yaml"


# Configuration rendering tests
def test_config_render_basic(default_directories) -> None:
    """Test basic template rendering in configuration."""

    class RenderConfig(BaseConfig):
        """Test configuration class for rendering templates."""

        name: str
        title: str
        nested: dict

    config = RenderConfig(
        name="test",
        title="{{ name }} document",
        nested={
            "value": "{{ title }}",
        },
        directories=default_directories,
    )

    rendered = config.resolve_variables()
    assert rendered.title == "test document"
    assert rendered.nested["value"] == "test document"


def test_config_render_circular(default_directories) -> None:
    """Test detection of circular references in config rendering."""

    class CircularConfig(BaseConfig):
        """Test configuration class for circular reference detection."""

        a: str
        b: str

    config = CircularConfig(
        a="{{ b }}",
        b="{{ a }}",
        directories=default_directories,
    )

    with pytest.raises(ConfigurationError, match="(?i).*circular.*"):
        config.resolve_variables()


# Utility method tests
def test_config_readable(default_directories) -> None:
    """Test configuration readable printing."""

    class ReadableConfig(BaseConfig):
        """Test configuration class for readable output."""

        title: str
        content: str

    config = ReadableConfig(
        title="Test",
        content="A" * 100,  # Long string that should be truncated
        directories=default_directories,
    )

    readable = config.readable(max_chars=20)
    assert "..." in readable  # Should show truncation
    assert "Test" in readable
