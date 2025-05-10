"""Tests for the PDFBaker class and related functionality."""

import logging
import shutil
from pathlib import Path

import pytest
from pydantic import ValidationError

from pdfbaker.baker import Baker, BakerOptions
from pdfbaker.errors import ConfigurationError, DocumentNotFoundError
from pdfbaker.logging import TRACE


def test_baker_options_defaults():
    """BakerOptions: defaults are all False."""
    options = BakerOptions()
    assert not options.quiet
    assert not options.verbose
    assert not options.trace
    assert not options.keep_build


def test_baker_options_logging_levels():
    """BakerOptions: logging level is set as expected."""
    test_cases = [
        (BakerOptions(quiet=True), logging.ERROR),
        (BakerOptions(verbose=True), logging.DEBUG),
        (BakerOptions(trace=True), TRACE),
        (BakerOptions(), logging.INFO),
    ]
    examples_config = Path(__file__).parent.parent / "examples" / "examples.yaml"
    for options, expected_level in test_cases:
        Baker(examples_config, options=options)
        assert logging.getLogger().level == expected_level


def test_baker_init_invalid_config(tmp_path: Path, write_yaml):
    """Baker: raises ValidationError for missing or invalid config fields."""
    config_file = tmp_path / "invalid.yaml"
    write_yaml(config_file, {"title": "test", "directories": {"base": str(tmp_path)}})
    with pytest.raises(ValidationError) as exc_info:
        Baker(config_file)
    assert "documents" in str(exc_info.value)
    write_yaml(
        config_file, {"documents": "not_a_list", "directories": {"base": str(tmp_path)}}
    )
    with pytest.raises(ValidationError) as exc_info:
        Baker(config_file)
    assert "documents" in str(exc_info.value)
    abs_config = Path("/tmp/test_config.yaml")
    write_yaml(abs_config, {"documents": [], "directories": {"base": "/tmp"}})
    baker = Baker(abs_config)
    assert baker.config.directories.base == Path("/tmp")


def test_baker_examples():
    """Baker: bakes all examples and verifies output files."""
    test_dir = Path(__file__).parent
    examples_config_path = test_dir.parent / "examples" / "examples.yaml"
    examples_base_dir = examples_config_path.parent
    build_dir = examples_base_dir / "build"
    dist_dir = examples_base_dir / "dist"
    if build_dir.exists():
        shutil.rmtree(build_dir)
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    options = BakerOptions(quiet=False, keep_build=True)
    try:
        baker = Baker(examples_config_path, options=options)
        success = baker.bake()
        assert success, "baker.bake() reported failure"
        assert build_dir.exists() and any(build_dir.iterdir())
        assert dist_dir.exists() and any(dist_dir.iterdir())
        expected_filenames = {
            "minimal": "minimal_example.pdf",
            "regular": "regular_example.pdf",
            "custom_locations": "custom_locations_custom.pdf",
            "custom_processing": "xkcd_example.pdf",
        }
        for doc_spec in baker.config.documents:
            doc_name = doc_spec.name
            doc_output_dir = dist_dir / doc_name
            if doc_name == "variants":
                for vp in [
                    doc_output_dir / "basic_variant.pdf",
                    doc_output_dir / "premium_variant.pdf",
                    doc_output_dir / "enterprise_variant.pdf",
                ]:
                    assert vp.exists() and vp.stat().st_size > 0
            elif doc_name in expected_filenames:
                filename = expected_filenames[doc_name]
                expected_pdf = doc_output_dir / filename
                assert expected_pdf.exists() and expected_pdf.stat().st_size > 0
    finally:
        if build_dir.exists():
            shutil.rmtree(build_dir)
        if dist_dir.exists():
            shutil.rmtree(dist_dir)
        assert not build_dir.exists()
        assert not dist_dir.exists()


def test_baker_get_selected_documents_missing(
    tmp_path, write_yaml, default_directories
):
    """Baker: _get_selected_documents raises DocumentNotFoundError for missing doc."""
    config_file = tmp_path / "baker.yaml"
    write_yaml(
        config_file,
        {
            "documents": [{"path": "doc1", "name": "doc1"}],
            "directories": default_directories.model_dump(mode="json"),
        },
    )
    baker = Baker(config_file=config_file, options=BakerOptions())
    with pytest.raises(DocumentNotFoundError):
        baker._get_selected_documents(("not_a_doc",))  # pylint: disable=protected-access


def test_baker_teardown_no_build_dir(tmp_path, write_yaml, default_directories):
    """Baker: teardown does nothing if build dir does not exist."""
    config_file = tmp_path / "baker.yaml"
    dirs = default_directories.model_dump(mode="json")
    write_yaml(
        config_file,
        {
            "documents": [{"path": "doc1", "name": "doc1"}],
            "directories": dirs,
        },
    )
    baker = Baker(config_file=config_file, options=BakerOptions())
    # build dir does not exist
    baker.teardown()  # Should not raise


def test_baker_bake_success_and_failure(tmp_path, write_yaml, default_directories):
    """Baker: bake() returns True if all succeed, False if any fail."""
    # Success case
    config_file = tmp_path / "baker.yaml"
    write_yaml(
        config_file,
        {
            "documents": [
                {"path": "doc1.yaml", "name": "doc1"},
                {"path": "doc2.yaml", "name": "doc2"},
            ],
            "directories": default_directories.model_dump(mode="json"),
        },
    )
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir(exist_ok=True)
    for doc in ("doc1.yaml", "doc2.yaml"):
        pages_dir = docs_dir / "pages"
        pages_dir.mkdir(exist_ok=True)
        write_yaml(pages_dir / "page1.yaml", {"template": "template.svg"})
        templates_dir = docs_dir / "templates"
        templates_dir.mkdir(exist_ok=True)
        (templates_dir / "template.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"></svg>'
        )
        doc_dirs = default_directories.model_dump(mode="json")
        doc_dirs["templates"] = str(templates_dir)
        doc_dirs["pages"] = str(pages_dir)
        write_yaml(
            docs_dir / doc,
            {
                "pages": [{"path": "page1.yaml", "name": "page1"}],
                "directories": doc_dirs,
                "filename": doc,
            },
        )
    baker = Baker(config_file=config_file, options=BakerOptions(keep_build=True))
    assert baker.bake(("doc1", "doc2")) is True

    # Failure case: one doc missing
    with pytest.raises(DocumentNotFoundError):
        baker.bake(("doc1", "not_a_doc"))


def test_baker_process_documents_handles_validation_error(
    tmp_path, write_yaml, default_directories
):
    """Baker: _process_documents handles ValidationError and logs error."""
    config_file = tmp_path / "baker.yaml"
    write_yaml(
        config_file,
        {
            "documents": [
                {"path": "doc1.yaml", "name": "doc1"},
            ],
            "directories": default_directories.model_dump(mode="json"),
        },
    )
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir(exist_ok=True)
    pages_dir = docs_dir / "pages"
    pages_dir.mkdir(exist_ok=True)
    write_yaml(pages_dir / "page1.yaml", {"template": "template.svg"})
    templates_dir = docs_dir / "templates"
    templates_dir.mkdir(exist_ok=True)
    (templates_dir / "template.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"></svg>'
    )
    doc_dirs = default_directories.model_dump(mode="json")
    doc_dirs["templates"] = str(templates_dir)
    doc_dirs["pages"] = str(pages_dir)
    # Write a minimal valid YAML to doc1.yaml
    write_yaml(
        docs_dir / "doc1.yaml",
        {"pages": [], "directories": doc_dirs, "filename": "doc1"},
    )
    baker = Baker(config_file=config_file, options=BakerOptions(keep_build=True))
    with pytest.raises(
        ConfigurationError, match='Cannot determine pages of document "doc1"'
    ):
        baker._process_documents(baker.config.documents)  # pylint: disable=protected-access


def test_baker_teardown_build_dir_not_empty(tmp_path, write_yaml, default_directories):
    """Baker: teardown logs warning if build dir is not empty and does not remove it."""
    config_file = tmp_path / "baker.yaml"
    dirs = default_directories.model_dump(mode="json")
    build_dir = tmp_path / "build"
    build_dir.mkdir()
    (build_dir / "dummy.txt").write_text("not empty")
    dirs["build"] = str(build_dir)
    write_yaml(
        config_file,
        {
            "documents": [{"path": "doc1", "name": "doc1"}],
            "directories": dirs,
        },
    )
    baker = Baker(config_file=config_file, options=BakerOptions())
    baker.teardown()  # Should log a warning and not remove the dir
    assert build_dir.exists()
