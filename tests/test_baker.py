"""Tests for the PDFBaker class and related functionality."""

import logging
import shutil
from pathlib import Path

import pytest

from pdfbaker.baker import Baker, BakerOptions
from pdfbaker.errors import ConfigurationError
from pdfbaker.logging import TRACE

# FIXME: default_config_overrides no longer needed, just throw kwargs at Baker init


# BakerOptions tests
def test_baker_options_defaults() -> None:
    """Test BakerOptions default values."""
    options = BakerOptions()
    assert not options.quiet
    assert not options.verbose
    assert not options.trace
    assert not options.keep_build
    assert options.default_config_overrides is None


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


def test_baker_options_default_config_overrides(tmp_path: Path) -> None:
    """Test BakerOptions with default_config_overrides."""
    # Create a minimal valid config
    config_file = tmp_path / "test.yaml"
    config_file.write_text("documents: [test]")

    custom_dir = tmp_path / "custom"
    options = BakerOptions(
        default_config_overrides={
            "directories": {
                "documents": str(custom_dir),
            }
        }
    )

    baker = Baker(config_file, options=options)
    assert str(baker.config["directories"]["documents"]) == str(custom_dir)


# PDFBaker initialization tests
def test_baker_init_invalid_config(tmp_path: Path) -> None:
    """Test PDFBaker initialization with invalid configuration."""
    # Create an invalid config file (missing 'documents' key)
    config_file = tmp_path / "invalid.yaml"
    config_file.write_text("title: test")

    with pytest.raises(ConfigurationError, match=".*documents.*missing.*"):
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
        default_config_overrides={
            "directories": {
                "build": str(build_dir),
                "dist": str(dist_dir),
            }
        },
    )

    try:
        baker = Baker(examples_config, options=options)
        baker.bake()
    finally:
        # Clean up test directories
        if build_dir.exists():
            shutil.rmtree(build_dir)
        if dist_dir.exists():
            shutil.rmtree(dist_dir)
