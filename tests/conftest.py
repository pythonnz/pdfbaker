"""Common configuration of tests."""

from pathlib import Path

import pytest
from ruamel.yaml import YAML

from pdfbaker.config import Directories


@pytest.fixture
def default_directories(tmp_path: Path) -> Directories:
    """Fixture providing default Directories for tests."""
    return Directories(
        base=tmp_path,
        build=tmp_path / "build",
        dist=tmp_path / "dist",
        documents=tmp_path / "docs",
        pages=tmp_path / "pages",
        templates=tmp_path / "templates",
        images=tmp_path / "images",
    )


@pytest.fixture
def write_yaml():
    """Reusable YAML writer for tests."""

    def _write_yaml(path, data):
        yaml = YAML(typ="full")
        with open(path, "w", encoding="utf-8") as file:
            yaml.dump(data, file)

    return _write_yaml
