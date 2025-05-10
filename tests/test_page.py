"""Tests for the Page class and page rendering/conversion functionality."""

import pytest

import pdfbaker.page
from pdfbaker.config import PathSpec
from pdfbaker.errors import SVGConversionError, SVGTemplateError
from pdfbaker.page import Page


@pytest.fixture(name="template_svg")
def _template_svg(tmp_path):
    """Create a templates directory and a valid template.svg file."""
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    template_path = templates_dir / "template.svg"
    template_path.write_text(
        '<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">'
        "{{ foo }}</svg>"
    )
    return template_path


def test_page_process_success(tmp_path, default_directories, write_yaml, template_svg):
    """Page: process() renders SVG and converts to PDF successfully."""
    default_directories.build.mkdir()
    page_yaml = tmp_path / "page1.yaml"
    write_yaml(
        page_yaml, {"template": str(template_svg), "foo": "bar", "is_variant": False}
    )
    config_path = PathSpec(path=page_yaml, name="page1")
    page = Page(
        config_path=config_path,
        page_number=1,
        directories=default_directories.model_dump(mode="json"),
    )
    pdf_path = page.process()
    assert pdf_path.exists()
    assert pdf_path.suffix == ".pdf"


def test_page_process_template_not_found(tmp_path, default_directories, write_yaml):
    """Page: process() raises SVGTemplateError if template is missing."""
    default_directories.build.mkdir()
    page_yaml = tmp_path / "page1.yaml"
    write_yaml(page_yaml, {"template": "missing.svg", "is_variant": False})
    config_path = PathSpec(path=page_yaml, name="page1")
    page = Page(
        config_path=config_path,
        page_number=1,
        directories=default_directories.model_dump(mode="json"),
    )
    with pytest.raises(SVGTemplateError):
        page.process()


def test_page_process_template_error(
    tmp_path, default_directories, write_yaml, template_svg
):
    """Page: process() raises SVGTemplateError on Jinja2 TemplateError."""
    # Overwrite the template with an invalid filter
    template_svg.write_text('<svg width="100" height="100">{{ foo|notafilter }}</svg>')
    default_directories.build.mkdir()
    page_yaml = tmp_path / "page1.yaml"
    write_yaml(page_yaml, {"template": str(template_svg), "is_variant": False})
    config_path = PathSpec(path=page_yaml, name="page1")
    page = Page(
        config_path=config_path,
        page_number=1,
        directories=default_directories.model_dump(mode="json"),
    )
    with pytest.raises(SVGTemplateError):
        page.process()


def test_page_process_svg_conversion_error(
    tmp_path, default_directories, write_yaml, monkeypatch, template_svg
):
    """Page: process() raises SVGConversionError if SVG to PDF fails."""
    # Overwrite the template with a minimal valid SVG
    template_svg.write_text(
        '<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"></svg>'
    )
    default_directories.build.mkdir()
    page_yaml = tmp_path / "page1.yaml"
    write_yaml(
        page_yaml,
        {
            "template": str(template_svg),
            "is_variant": False,
            "template_filters": ["wordwrap"],
            "template_renderers": ["render_highlight"],
            "svg2pdf_backend": "cairosvg",
        },
    )
    config_path = PathSpec(path=page_yaml, name="page1")

    def raise_svg_conversion_error(output_svg, output_pdf, backend=None):
        raise SVGConversionError(output_svg, backend or "test-backend", "fail")

    monkeypatch.setattr(pdfbaker.page, "convert_svg_to_pdf", raise_svg_conversion_error)
    page = Page(
        config_path=config_path,
        page_number=1,
        directories=default_directories.model_dump(mode="json"),
    )
    with pytest.raises(SVGConversionError):
        page.process()


def test_page_process_variant_naming(
    tmp_path, default_directories, write_yaml, template_svg
):
    """Page: process() uses variant name in output file if is_variant is True."""
    # Overwrite the template with a minimal valid SVG
    template_svg.write_text(
        '<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"></svg>'
    )
    default_directories.build.mkdir()
    page_yaml = tmp_path / "page1.yaml"
    write_yaml(page_yaml, {"template": str(template_svg)})
    config_path = PathSpec(path=page_yaml, name="page1")
    page = Page(
        config_path=config_path,
        page_number=1,
        directories=default_directories.model_dump(mode="json"),
        is_variant=True,
        variant={"name": "special"},
    )
    pdf_path = page.process()
    assert "special" in pdf_path.name
