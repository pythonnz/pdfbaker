"""Tests for CLI functionality."""

from pathlib import Path

from click.testing import CliRunner

import pdfbaker
from pdfbaker.__main__ import cli


def test_cli_version():
    """CLI: --version outputs version string."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.output.lower()
    assert pdfbaker.__version__ in result.output


def test_cli_help():
    """CLI: --help outputs usage and commands."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "bake" in result.output
    assert "version" in result.output


def test_cli_bake_help():
    """CLI: bake --help outputs bake options."""
    runner = CliRunner()
    result = runner.invoke(cli, ["bake", "--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "--quiet" in result.output
    assert "--verbose" in result.output
    assert "--keep-build" in result.output


def test_cli_bake_missing_config(tmp_path: Path):
    """CLI: bake with missing config file reports error."""
    runner = CliRunner()
    result = runner.invoke(cli, ["bake", str(tmp_path / "missing.yaml")])
    assert result.exit_code == 2
    assert "does not exist" in result.output


def test_cli_bake_invalid_config(tmp_path: Path):
    """CLI: bake with invalid config file reports YAML and validation errors."""
    config_file = tmp_path / "invalid.yaml"
    config_file.write_text("invalid: yaml: content")
    runner = CliRunner()
    result = runner.invoke(cli, ["bake", str(config_file)])
    assert result.exit_code == 1
    assert result.exception is not None
    assert "mapping values are not allowed here" in str(result.exception)
    config_file.write_text("""
directories:
  base: /tmp
""")
    result = runner.invoke(cli, ["bake", str(config_file)])
    assert result.exit_code == 1
    assert result.exception is not None
    exception_str = str(result.exception)
    assert "BakerConfig" in exception_str
    assert "documents" in exception_str
    assert (
        'Value error, Key "documents" missing' in exception_str
        or "Field required" in exception_str
    )
    abs_config = Path("/tmp/test_config.yaml")
    abs_config.write_text("""
documents: []
directories:
  base: /tmp
""")
    result = runner.invoke(cli, ["bake", str(abs_config)])
    assert result.exit_code == 0


def test_cli_bake_verbosity_flags(tmp_path: Path):
    """
    CLI: --quiet suppresses output on success, errors are still reported;
    --verbose enables debug output.
    """
    failing_config = tmp_path / "failing.yaml"
    failing_config.write_text("pages: [page1.yaml]\ndirectories:\n  build: build\n")
    runner = CliRunner()
    result = runner.invoke(cli, ["bake", "--quiet", str(failing_config)])
    assert result.exit_code == 1
    assert result.output == ""
    success_config = tmp_path / "success.yaml"
    success_config.write_text("documents: []\ndirectories:\n  base: /tmp\n")
    result = runner.invoke(cli, ["bake", "--quiet", str(success_config)])
    assert result.exit_code == 0
    assert result.output == ""
    result = runner.invoke(cli, ["bake", "--verbose", str(success_config)])
    assert result.exit_code == 0
    assert "DEBUG" in result.output
    assert "Loading main configuration" in result.output
