"""Tests for the PDFBaker class and related functionality."""

import logging
import shutil
from pathlib import Path

import pytest
from pydantic import ValidationError
from ruamel.yaml import YAML

from pdfbaker.baker import Baker, BakerOptions
from pdfbaker.logging import TRACE


def write_yaml(path, data):
    """Write data to a YAML file using ruamel.yaml."""
    yaml = YAML()
    with open(path, "w", encoding="utf-8") as file:
        yaml.dump(data, file)


# BakerOptions tests
def test_baker_options_defaults() -> None:
    """Test BakerOptions default values."""
    options = BakerOptions()
    assert not options.quiet
    assert not options.verbose
    assert not options.trace
    assert not options.keep_build


def test_baker_options_logging_levels() -> None:
    """Test different logging level configurations."""
    test_cases = [
        (BakerOptions(quiet=True), logging.ERROR),
        (BakerOptions(verbose=True), logging.DEBUG),
        (BakerOptions(trace=True), TRACE),
        (BakerOptions(), logging.INFO),  # default
    ]

    examples_config = Path(__file__).parent.parent / "examples" / "examples.yaml"
    for options, expected_level in test_cases:
        Baker(examples_config, options=options)
        assert logging.getLogger().level == expected_level


# PDFBaker initialization tests
def test_baker_init_invalid_config(tmp_path: Path) -> None:
    """Test PDFBaker initialization with invalid configuration."""
    # Create an invalid config file (missing 'documents' key)
    config_file = tmp_path / "invalid.yaml"
    write_yaml(config_file, {"title": "test", "directories": {"base": str(tmp_path)}})

    with pytest.raises(ValidationError, match=".*documents.*missing.*"):
        Baker(config_file)


# PDFBaker functionality tests
def test_baker_examples() -> None:
    """Test baking all examples."""
    test_dir = Path(__file__).parent
    examples_config = test_dir.parent / "examples" / "examples.yaml"

    # Create test output directories
    build_dir = test_dir / "build"
    dist_dir = test_dir / "dist"
    build_dir.mkdir(exist_ok=True)
    dist_dir.mkdir(exist_ok=True)

    options = BakerOptions(
        quiet=True,
        keep_build=True,
    )

    try:
        baker = Baker(
            examples_config,
            options=options,
            directories={
                "build": str(build_dir),
                "dist": str(dist_dir),
            },
        )
        baker.bake()
    finally:
        # Clean up test directories
        if build_dir.exists():
            shutil.rmtree(build_dir)
        if dist_dir.exists():
            shutil.rmtree(dist_dir)
