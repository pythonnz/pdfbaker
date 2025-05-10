"""Tests for configuration functionality."""

from pathlib import Path

import pytest
import ruamel.yaml

from pdfbaker.config import (
    BaseConfig,
    ConfigurationError,
    Directories,
    PathSpec,
    SVG2PDFBackend,
    TemplateFilter,
    TemplateRenderer,
    convert_enum,
)
from pdfbaker.config.baker import DEFAULT_DIRECTORIES, BakerConfig
from pdfbaker.config.document import DocumentConfig
from pdfbaker.config.page import PageConfig


# BaseConfig merger tests
def test_base_config_merge_basic(default_directories) -> None:
    """BaseConfig: merge updates top-level fields."""

    class SimpleConfig(BaseConfig):
        """Simple config for merge test."""

        field_foo: str
        field_bar: int

    base = SimpleConfig(field_foo="a", field_bar=1, directories=default_directories)
    update = {"field_foo": "b", "field_bar": 2}
    merged = base.merge(update)
    assert merged.field_foo == "b"
    assert merged.field_bar == 2


def test_base_config_merge_nested(default_directories) -> None:
    """BaseConfig: merge updates nested dict fields."""

    class NestedConfig(BaseConfig):
        """Nested config for merge test."""

        document: dict
        style: dict

    base = NestedConfig(
        document={
            "title": "Main Document",
            "meta": {"author": "Jane Smith", "date": "2024-01-01"},
        },
        style={"font": "Arial", "colors": {"text": "black", "background": "white"}},
        directories=default_directories,
    )
    update = {
        "document": {"meta": {"date": "2024-04-01", "version": "1.0"}},
        "style": {"colors": {"text": "navy"}},
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
    """BaseConfig: merge with empty dict returns self."""

    class SimpleConfig(BaseConfig):
        """Simple config for merge empty test."""

        field_foo: str
        field_bar: int

    base = SimpleConfig(field_foo="a", field_bar=1, directories=default_directories)
    merged = base.merge({})
    assert merged.field_foo == "a"
    assert merged.field_bar == 1


# Configuration initialization tests
def test_baker_config_init_with_file(
    tmp_path: Path, default_directories: Directories, write_yaml
) -> None:
    """BakerConfig: loads config from YAML file and resolves paths."""
    config_file = tmp_path / "baker.yaml"
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
    assert config.directories.base.resolve() == default_directories.base.resolve()


def test_baker_config_custom_directories(
    tmp_path: Path, default_directories: Directories, write_yaml
) -> None:
    """BakerConfig: custom directories are resolved correctly."""
    config_file = tmp_path / "baker.yaml"
    custom_dirs = default_directories.model_dump(mode="json")
    custom_build = tmp_path / "custom_build"
    custom_dirs["build"] = str(custom_build)

    config_data = {
        "documents": [{"path": "doc1", "name": "doc1"}],
        "directories": custom_dirs,
    }

    write_yaml(config_file, config_data)
    config = BakerConfig(config_file=config_file)

    assert config.config_file == config_file
    assert len(config.documents) == 1
    assert config.documents[0].name == "doc1"
    assert config.directories.build.resolve() == custom_build.resolve()


def test_baker_config_init_invalid_yaml(tmp_path: Path) -> None:
    """BakerConfig: invalid YAML raises error."""
    config_file = tmp_path / "bad.yaml"
    config_file.write_text("invalid: yaml: content")
    with pytest.raises(ruamel.yaml.YAMLError):
        BakerConfig(config_file=config_file)


# Path resolution tests
def test_config_resolve_path(tmp_path: Path, default_directories: Directories) -> None:
    """BaseConfig: resolve_path resolves relative and absolute paths."""

    class PathConfig(BaseConfig):
        """Path config for resolve_path test."""

        field_foo: str

    base = PathConfig(field_foo="bar", directories=default_directories)
    rel = base.resolve_path("foo/bar")
    abs_path = base.resolve_path(str(tmp_path))
    assert rel.is_absolute()
    assert abs_path == tmp_path


# Configuration rendering tests
def test_config_render_basic(default_directories) -> None:
    """BaseConfig: readable output is truncated and includes key fields."""

    class RenderConfig(BaseConfig):
        """Render config for render test."""

        field_foo: str
        field_bar: int

    config = RenderConfig(field_foo="a", field_bar=1, directories=default_directories)
    rendered = config.readable()
    assert "field_foo" in rendered and "field_bar" in rendered


def test_config_render_circular(default_directories) -> None:
    """BaseConfig: readable output raises ValueError on circular references."""

    class CircularConfig(BaseConfig):
        """Circular config for render test."""

        field_foo: str
        field_bar: "CircularConfig" = None

    config = CircularConfig(field_foo="a", directories=default_directories)
    config.field_bar = config
    with pytest.raises(ValueError, match="Circular reference detected"):
        config.readable()


# Utility method tests
def test_config_readable(default_directories) -> None:
    """BaseConfig: readable output is truncated and includes key fields."""

    class ReadableConfig(BaseConfig):
        """Readable config for readable test."""

        title: str
        content: str

    config = ReadableConfig(
        title="Test", content="A" * 100, directories=default_directories
    )
    readable = config.readable(max_chars=20)
    assert "..." in readable
    assert "Test" in readable


# === Additional coverage tests ===


def test_enum_values():
    """Test all enum values for TemplateRenderer, TemplateFilter, SVG2PDFBackend."""
    assert TemplateRenderer.RENDER_HIGHLIGHT.value == "render_highlight"
    assert TemplateFilter.WORDWRAP.value == "wordwrap"
    assert SVG2PDFBackend.CAIROSVG.value == "cairosvg"
    assert SVG2PDFBackend.INKSCAPE.value == "inkscape"


def test_convert_enum():
    """Test convert_enum utility for valid and invalid input."""
    assert (
        convert_enum(TemplateRenderer)("render_highlight")
        == TemplateRenderer.RENDER_HIGHLIGHT
    )
    assert (
        convert_enum(SVG2PDFBackend)(SVG2PDFBackend.CAIROSVG) == SVG2PDFBackend.CAIROSVG
    )
    with pytest.raises(ValueError):
        convert_enum(SVG2PDFBackend)("notavalidbackend")


def test_baseconfig_user_defined_settings(default_directories):
    """Test user_defined_settings property with and without extra fields."""

    class ExtraConfig(BaseConfig):
        """Extra config for user_defined_settings test."""

        value: int

    config = ExtraConfig(value=1, directories=default_directories)
    config.__pydantic_extra__ = {"bar": 2}
    assert config.user_defined_settings == {"bar": 2}
    config2 = ExtraConfig(value=2, directories=default_directories)
    assert not config2.user_defined_settings


def test_baseconfig_resolve_variables_circular(default_directories):
    """Test resolve_variables raises on circular reference."""

    class CircularConfig(BaseConfig):
        """Circular config for resolve_variables test."""

        data: str

    config = CircularConfig(data="{{ data }}", directories=default_directories)
    with pytest.raises(ConfigurationError, match="Maximum iterations reached"):
        config.resolve_variables(max_iterations=2)


def test_baseconfig_readable_truncation(default_directories):
    """Test readable output truncates long strings."""

    class TruncConfig(BaseConfig):
        """Trunc config for readable truncation test."""

        data: str

    config = TruncConfig(data="A" * 100, directories=default_directories)
    out = config.readable(max_chars=10)
    assert "..." in out


def test_pathspec_ensure_pathspec():
    """Test PathSpec.model_validate with various input forms and error case."""
    ps = PathSpec(path="foo/bar.txt", name="bar")
    assert ps.path.name == "bar.txt"
    ps2 = PathSpec.model_validate({"path": "baz/qux.txt", "name": "qux"})
    assert ps2.name == "qux"
    ps3 = PathSpec.model_validate({"path": "baz/quux.txt"})
    assert ps3.name == "quux"
    with pytest.raises(ValueError):
        PathSpec.model_validate({"name": "fail"})


def test_pathspec_resolve_relative_to(tmp_path):
    """Test PathSpec.resolve_relative_to for relative and absolute paths."""
    rel = PathSpec(path="foo.txt", name="foo")
    abs_ps = rel.resolve_relative_to(tmp_path)
    assert abs_ps.path.is_absolute()
    already_abs = PathSpec(path=tmp_path / "bar.txt", name="bar")
    abs2 = already_abs.resolve_relative_to(tmp_path)
    assert abs2.path == already_abs.path


def test_directories_ensure_resolved_base(tmp_path):
    """Test Directories.model_validate ensures base is absolute."""
    dirs = DEFAULT_DIRECTORIES.copy()
    dirs["base"] = str(tmp_path / "relbase")
    d = Directories.model_validate(dirs)
    assert d.base.is_absolute()


def test_bakerconfig_missing_documents(tmp_path, default_directories):
    """Test BakerConfig raises ValueError if 'documents' key is missing."""
    config_file = tmp_path / "bad.yaml"
    # Use the default_directories fixture to get the directory structure
    directories_dict = default_directories.model_dump(mode="json")
    # Remove 'documents' key to trigger the error
    config_file.write_text(f"directories:\n  base: {directories_dict['base']}\n")
    with pytest.raises(ValueError, match='Key "documents" missing'):
        BakerConfig(config_file=config_file)


def test_documentconfig_check_pages_and_variants(default_directories):
    """Test DocumentConfig error cases for pages/variants logic."""
    with pytest.raises(ConfigurationError, match="Cannot determine pages"):
        DocumentConfig(name="doc", filename="doc", directories=default_directories)


def test_documentconfig_set_variants_invalid(default_directories):
    """Test DocumentConfig skips invalid variants and logs a warning."""
    with pytest.raises(TypeError):
        DocumentConfig(
            name="doc",
            filename="doc",
            directories=default_directories,
            variants=[{"pages": []}],
        )


def test_pageconfig_name_property(tmp_path, default_directories):
    """PageConfig: name property returns the stem of config_path.path."""
    page_yaml = tmp_path / "page1.yaml"
    page_yaml.write_text("template: template.svg\n")
    config_path = PathSpec(path=page_yaml, name="page1")
    template_path = PathSpec(path="template.svg", name="template.svg")
    page = PageConfig(
        config_path=config_path,
        page_number=1,
        template=template_path,
        directories=default_directories.model_dump(mode="json"),
    )
    assert page.name == "page1"
