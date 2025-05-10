"""Tests for document processing functionality."""

import shutil
from pathlib import Path

import pytest
from pydantic import ValidationError

from pdfbaker.baker import Baker, BakerOptions
from pdfbaker.config import Directories, PathSpec
from pdfbaker.document import Document


@pytest.fixture(name="baker_config")
def fixture_baker_config(
    tmp_path: Path, default_directories: Directories, write_yaml
) -> Path:
    """Create a baker configuration file."""
    config_file = tmp_path / "config.yaml"
    dirs = default_directories.model_dump(mode="json")
    write_yaml(
        config_file,
        {
            "documents": [{"path": "test_doc", "name": "test_doc"}],
            "directories": dirs,
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
def fixture_doc_dir(
    tmp_path: Path, default_directories: Directories, write_yaml
) -> Path:
    """Create a document directory with necessary files."""
    doc_path = tmp_path / "test_doc"
    doc_path.mkdir()

    config_file = doc_path / "config.yaml"
    dirs = default_directories.model_dump(mode="json")
    dirs["base"] = str(doc_path)
    dirs["build"] = str(doc_path / "build")
    dirs["dist"] = str(doc_path / "dist")
    write_yaml(
        config_file,
        {
            "pages": [{"path": "page1.yaml", "name": "page1"}],
            "directories": dirs,
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
    """Document: initializes from directory and loads config."""
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
    write_yaml,
) -> None:
    """Document: initializes from file and loads config."""
    config_file = tmp_path / "test_doc.yaml"
    dirs = default_directories.model_dump(mode="json")
    dirs["base"] = str(tmp_path)
    write_yaml(
        config_file,
        {
            "pages": [{"path": "page1.yaml", "name": "page1"}],
            "directories": dirs,
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
    baker_options: BakerOptions, tmp_path: Path
) -> None:
    """Document: raises error if pages are missing."""
    config_file = tmp_path / "missing_pages.yaml"
    config_file.write_text("""
name: missing_pages
directories:
  base: .
pages: []
""")
    doc_config_path = PathSpec(path=config_file, name="missing_pages")
    with pytest.raises(ValidationError):
        Document(config_path=doc_config_path, **baker_options.model_dump())


def test_document_custom_bake(
    baker_config: Path, baker_options: BakerOptions, doc_dir: Path
) -> None:
    """Document: custom bake module is used if present."""
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
    """Document: error in custom bake module is reported."""
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
    write_yaml,
) -> None:
    """Document: processes all variants and produces PDFs."""
    config_file = doc_dir / "config.yaml"
    dirs = default_directories.model_dump(mode="json")
    dirs["base"] = str(doc_dir)
    dirs["build"] = str(doc_dir / "build")
    dirs["dist"] = str(doc_dir / "dist")
    write_yaml(
        config_file,
        {
            "pages": [{"path": "page1.yaml", "name": "page1"}],
            "directories": dirs,
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
    write_yaml,
) -> None:
    """Document: variants with different pages are processed correctly."""
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
