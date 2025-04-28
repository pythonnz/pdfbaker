"""Tests for document processing functionality."""

import shutil
from pathlib import Path

import pytest
from ruamel.yaml import YAML

from pdfbaker.baker import Baker, BakerOptions
from pdfbaker.config import Directories, PathSpec
from pdfbaker.document import Document
from pdfbaker.errors import ConfigurationError


def write_yaml(path: Path, data: dict) -> None:
    """Write data to a YAML file using ruamel.yaml."""
    yaml = YAML()
    with open(path, "w", encoding="utf-8") as file:
        yaml.dump(data, file)


@pytest.fixture(name="baker_config")
def fixture_baker_config(tmp_path: Path, default_directories: Directories) -> Path:
    """Create a baker configuration file."""
    config_file = tmp_path / "config.yaml"
    write_yaml(
        config_file,
        {
            "documents": [{"path": "test_doc", "name": "test_doc"}],
            "directories": {
                "base": str(default_directories.base),
                "build": str(default_directories.build),
                "dist": str(default_directories.dist),
                "documents": str(default_directories.documents),
                "pages": str(default_directories.pages),
                "templates": str(default_directories.templates),
                "images": str(default_directories.images),
            },
        },
    )
    return config_file


@pytest.fixture(name="baker_options")
def fixture_baker_options(tmp_path: Path) -> BakerOptions:
    """Create baker options with test-specific build/dist directories."""
    return BakerOptions(
        default_config_overrides={
            "directories": {
                "build": str(tmp_path / "build"),
                "dist": str(tmp_path / "dist"),
            }
        }
    )


@pytest.fixture(name="doc_dir")
def fixture_doc_dir(tmp_path: Path, default_directories: Directories) -> Path:
    """Create a document directory with necessary files."""
    doc_path = tmp_path / "test_doc"
    doc_path.mkdir()

    config_file = doc_path / "config.yaml"
    write_yaml(
        config_file,
        {
            "pages": [{"path": "page1.yaml", "name": "page1"}],
            "directories": {
                "base": str(doc_path),
                "build": str(doc_path / "build"),
                "dist": str(doc_path / "dist"),
                "documents": str(default_directories.documents),
                "pages": str(default_directories.pages),
                "templates": str(default_directories.templates),
                "images": str(default_directories.images),
            },
            "filename": "test_doc",
        },
    )

    pages_dir = doc_path / "pages"
    pages_dir.mkdir()
    write_yaml(pages_dir / "page1.yaml", {"template": "template.svg"})

    templates_dir = doc_path / "templates"
    templates_dir.mkdir()
    (templates_dir / "template.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"></svg>'
    )

    yield doc_path

    shutil.rmtree(doc_path, ignore_errors=True)


def test_document_init_with_dir(
    baker_config: Path, baker_options: BakerOptions, doc_dir: Path
) -> None:
    """Test document initialization with a directory."""
    baker = Baker(config_file=baker_config, options=baker_options)
    doc_config_path = PathSpec(path=doc_dir, name="test_doc")
    doc = Document(config_path=doc_config_path, **baker.config.document_settings)
    assert doc.config.name == "test_doc"
    assert len(doc.config.pages) == 1
    assert doc.config.pages[0].name == "page1"


def test_document_init_with_file(
    tmp_path: Path,
    baker_config: Path,
    baker_options: BakerOptions,
    default_directories: Directories,
) -> None:
    """Test document initialization with a config file."""
    config_file = tmp_path / "test_doc.yaml"
    write_yaml(
        config_file,
        {
            "pages": [{"path": "page1.yaml", "name": "page1"}],
            "directories": {
                "base": str(default_directories.base),
                "build": str(default_directories.build),
                "dist": str(default_directories.dist),
                "documents": str(default_directories.documents),
                "pages": str(default_directories.pages),
                "templates": str(default_directories.templates),
                "images": str(default_directories.images),
            },
            "filename": "test_doc",
        },
    )

    pages_dir = tmp_path / "pages"
    pages_dir.mkdir()
    write_yaml(pages_dir / "page1.yaml", {"template": "template.svg"})

    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    (templates_dir / "template.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"></svg>'
    )

    baker = Baker(config_file=baker_config, options=baker_options)
    doc_config_path = PathSpec(path=config_file, name="test_doc")
    doc = Document(config_path=doc_config_path, **baker.config.document_settings)
    assert doc.config.name == "test_doc"
    assert len(doc.config.pages) == 1
    assert doc.config.pages[0].name == "page1"


def test_document_init_missing_pages(
    tmp_path: Path, baker_config: Path, default_directories: Directories
) -> None:
    """Test document initialization with missing pages key."""
    config_file = tmp_path / "test_doc.yaml"
    write_yaml(
        config_file,
        {
            "title": "Test Document",
            "directories": {
                "base": str(default_directories.base),
                "build": str(default_directories.build),
                "dist": str(default_directories.dist),
                "documents": str(default_directories.documents),
                "pages": str(default_directories.pages),
                "templates": str(default_directories.templates),
                "images": str(default_directories.images),
            },
            "filename": "test_doc",
        },
    )

    baker = Baker(baker_config)
    doc_config_path = PathSpec(path=config_file, name="test_doc")
    with pytest.raises(ConfigurationError, match="Cannot determine pages"):
        Document(config_path=doc_config_path, **baker.config.document_settings)


def test_document_custom_bake(
    baker_config: Path, baker_options: BakerOptions, doc_dir: Path
) -> None:
    """Test document processing with a custom bake module."""
    (doc_dir / "bake.py").write_text(
        "def process_document(document):\n"
        "    return document.config.directories.build / 'custom.pdf'\n"
    )

    baker = Baker(config_file=baker_config, options=baker_options)
    doc_config_path = PathSpec(path=doc_dir, name="test_doc")
    doc = Document(config_path=doc_config_path, **baker.config.document_settings)
    assert doc.config.name == "test_doc"
    assert len(doc.config.pages) == 1


def test_document_custom_bake_error(
    baker_config: Path, baker_options: BakerOptions, doc_dir: Path
) -> None:
    """Test document processing with an invalid custom bake module."""
    (doc_dir / "bake.py").write_text("raise Exception('Test error')")

    baker = Baker(config_file=baker_config, options=baker_options)
    doc_config_path = PathSpec(path=doc_dir, name="test_doc")
    doc = Document(config_path=doc_config_path, **baker.config.document_settings)
    assert doc.config.name == "test_doc"
    assert len(doc.config.pages) == 1


def test_document_variants(
    baker_config: Path,
    baker_options: BakerOptions,
    doc_dir: Path,
    default_directories: Directories,
) -> None:
    """Test document processing with variants."""
    config_file = doc_dir / "config.yaml"
    write_yaml(
        config_file,
        {
            "pages": [{"path": "page1.yaml", "name": "page1"}],
            "directories": {
                "base": str(doc_dir),
                "build": str(doc_dir / "build"),
                "dist": str(doc_dir / "dist"),
                "documents": str(default_directories.documents),
                "pages": str(default_directories.pages),
                "templates": str(default_directories.templates),
                "images": str(default_directories.images),
            },
            "filename": "test_doc",
            "variants": [
                {"name": "variant1", "filename": "variant1"},
                {"name": "variant2", "filename": "variant2"},
            ],
        },
    )

    baker = Baker(config_file=baker_config, options=baker_options)
    doc_config_path = PathSpec(path=doc_dir, name="test_doc")
    doc = Document(config_path=doc_config_path, **baker.config.document_settings)
    assert doc.config.name == "test_doc"
    assert len(doc.config.pages) == 1
    assert len(doc.config.variants) == 2


def test_document_variants_with_different_pages(
    tmp_path: Path,
    baker_config: Path,
    baker_options: BakerOptions,
    default_directories: Directories,
) -> None:
    """Test document with variants where each variant has different pages."""
    config_file = tmp_path / "test_doc.yaml"
    write_yaml(
        config_file,
        {
            "filename": "{{ variant.name }}_doc",
            "directories": default_directories.model_dump(mode="json"),
            "variants": [
                {
                    "name": "variant1",
                    "filename": "variant1",
                    "pages": [{"path": "page1.yaml", "name": "page1"}],
                },
                {
                    "name": "variant2",
                    "filename": "variant2",
                    "pages": [{"path": "page2.yaml", "name": "page2"}],
                },
            ],
        },
    )

    pages_dir = tmp_path / "pages"
    pages_dir.mkdir()
    write_yaml(
        pages_dir / "page1.yaml",
        {"template": "template.svg", "content": "Variant 1 content"},
    )
    write_yaml(
        pages_dir / "page2.yaml",
        {"template": "template.svg", "content": "Variant 2 content"},
    )

    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    (templates_dir / "template.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"></svg>'
    )

    baker = Baker(config_file=baker_config, options=baker_options)
    doc_config_path = PathSpec(path=config_file, name="test_doc")
    doc = Document(config_path=doc_config_path, **baker.config.document_settings)

    assert doc.config.name == "test_doc"
    assert not doc.config.pages
    assert len(doc.config.variants) == 2
