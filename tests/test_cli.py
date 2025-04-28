"""Tests for CLI functionality."""

from pathlib import Path

from click.testing import CliRunner

from pdfbaker.__main__ import cli


def test_cli_version() -> None:
    """Test CLI version command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.output.lower()


def test_cli_help() -> None:
    """Test CLI help command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_cli_bake_help() -> None:
    """Test CLI bake help command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["bake", "--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_cli_bake_missing_config(tmp_path: Path) -> None:
    """Test CLI bake command with missing config file."""
    runner = CliRunner()
    result = runner.invoke(cli, ["bake", str(tmp_path / "missing.yaml")])
    assert result.exit_code == 2
    assert "does not exist" in result.output


def test_cli_bake_invalid_config(tmp_path: Path) -> None:
    """Test CLI bake command with invalid config file."""
    config_file = tmp_path / "invalid.yaml"
    config_file.write_text("invalid: yaml: content")

    runner = CliRunner()
    result = runner.invoke(cli, ["bake", str(config_file)])
    assert result.exit_code == 1


def test_cli_bake_quiet_mode(tmp_path: Path) -> None:
    """Test CLI bake command in quiet mode."""
    # Test case 1: Failure - should show errors
    failing_config = tmp_path / "failing.yaml"
    failing_config.write_text("""
pages: [page1.yaml]
directories:
  build: build
""")

    runner = CliRunner()
    result_obj = runner.invoke(cli, ["bake", "--quiet", str(failing_config)])

    # We just need to verify the exit code is 1, indicating an error
    assert result_obj.exit_code == 1  # Will fail because document is invalid

    # Success test
    success_config = tmp_path / "success.yaml"
    success_config.write_text("""
documents: []  # Empty list of documents is valid
""")

    result = runner.invoke(cli, ["bake", "--quiet", str(success_config)])
    assert result.exit_code == 0
    assert not result.output  # Should be completely quiet on success
