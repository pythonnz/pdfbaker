"""Common configuration of tests."""

from pathlib import Path

import pytest

from pdfbaker.config import Directories


@pytest.fixture
def default_directories(tmp_path: Path) -> Directories:
    """Fixture providing default Directories for tests."""
    return Directories(
        base=tmp_path,
        build=tmp_path / "build",
        dist=tmp_path / "dist",
        documents=tmp_path / "documents",
        pages=tmp_path / "pages",
        templates=tmp_path / "templates",
        images=tmp_path / "images",
    )
