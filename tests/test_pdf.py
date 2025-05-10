"""Tests for PDF processing functionality."""

import logging
from pathlib import Path

import pypdf
import pytest

from pdfbaker.pdf import (
    PDFCombineError,
    SVGConversionError,
    combine_pdfs,
    convert_svg_to_pdf,
)


def test_combine_pdfs_empty_list(tmp_path: Path) -> None:
    """combine_pdfs: raises error for empty input list."""
    output_file = tmp_path / "output.pdf"
    with pytest.raises(PDFCombineError) as exc_info:
        combine_pdfs([], output_file)
    assert "No PDF files provided to combine" in str(exc_info.value)
    assert not output_file.exists()


def test_combine_pdfs_single_file(tmp_path: Path) -> None:
    """combine_pdfs: single PDF file is copied to output."""
    pdf_file = tmp_path / "test.pdf"
    pdf_content = (
        b"%PDF-1.4\n"
        b"1 0 obj\n"
        b"<< /Type /Catalog /Pages 2 0 R >>\n"
        b"endobj\n"
        b"2 0 obj\n"
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>\n"
        b"endobj\n"
        b"3 0 obj\n"
        b"<< /Type /Page /Parent 2 0 R /Resources <<>> /MediaBox [0 0 612 792] >>\n"
        b"endobj\n"
        b"xref\n"
        b"0 4\n"
        b"0000000000 65535 f\n"
        b"0000000010 00000 n\n"
        b"0000000056 00000 n\n"
        b"0000000112 00000 n\n"
        b"trailer\n"
        b"<< /Size 4 /Root 1 0 R >>\n"
        b"startxref\n"
        b"164\n"
        b"%%EOF\n"
    )
    pdf_file.write_bytes(pdf_content)
    output_file = tmp_path / "output.pdf"
    combine_pdfs([pdf_file], output_file)
    assert output_file.exists() and output_file.stat().st_size > 0
    reader = pypdf.PdfReader(output_file)
    assert len(reader.pages) == 1
    assert reader.metadata is not None


def test_combine_pdfs_multiple_files(tmp_path: Path) -> None:
    """combine_pdfs: multiple PDF files are combined into one."""
    pdf1 = tmp_path / "test1.pdf"
    pdf2 = tmp_path / "test2.pdf"
    pdf1.write_bytes(
        b"%PDF-1.4\n"
        b"1 0 obj\n"
        b"<< /Type /Catalog /Pages 2 0 R >>\n"
        b"endobj\n"
        b"2 0 obj\n"
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>\n"
        b"endobj\n"
        b"3 0 obj\n"
        b"<< /Type /Page /Parent 2 0 R /Resources <<>> /MediaBox [0 0 612 792] >>\n"
        b"endobj\n"
        b"xref\n"
        b"0 4\n"
        b"0000000000 65535 f\n"
        b"0000000010 00000 n\n"
        b"0000000056 00000 n\n"
        b"0000000112 00000 n\n"
        b"trailer\n"
        b"<< /Size 4 /Root 1 0 R >>\n"
        b"startxref\n"
        b"164\n"
        b"%%EOF\n"
    )
    pdf2.write_bytes(pdf1.read_bytes())
    output_file = tmp_path / "output.pdf"
    combine_pdfs([pdf1, pdf2], output_file)
    assert output_file.exists() and output_file.stat().st_size > 0
    reader = pypdf.PdfReader(output_file)
    assert len(reader.pages) == 2


def test_combine_pdfs_broken_annotations(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """combine_pdfs: logs warning and falls back for broken annotations."""
    pdf_file = tmp_path / "test.pdf"
    pdf_file.write_bytes(
        b"%PDF-1.4\n"
        b"1 0 obj\n"
        b"<< /Type /Catalog /Pages 2 0 R >>\n"
        b"endobj\n"
        b"2 0 obj\n"
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>\n"
        b"endobj\n"
        b"3 0 obj\n"
        b"<< /Type /Page /Parent 2 0 R /Resources <<>> /MediaBox [0 0 612 792] "
        b"/Annots [4 0 R]>>\n"
        b"endobj\n"
        b"4 0 obj\n"
        b"<< /Type /Annot /Rect [0 0 0 0] >>\n"
        b"endobj\n"
        b"xref\n"
        b"0 5\n"
        b"0000000000 65535 f\n"
        b"0000000010 00000 n\n"
        b"0000000056 00000 n\n"
        b"0000000112 00000 n\n"
        b"0000000168 00000 n\n"
        b"trailer\n"
        b"<< /Size 5 /Root 1 0 R >>\n"
        b"startxref\n"
        b"220\n"
        b"%%EOF\n"
    )
    output_file = tmp_path / "output.pdf"
    with caplog.at_level(logging.WARNING):
        combine_pdfs([pdf_file], output_file)
    assert "Broken annotations in PDF" in caplog.text
    assert "Falling back to page-by-page method" in caplog.text
    assert output_file.exists() and output_file.stat().st_size > 0


def test_combine_pdfs_invalid_file(tmp_path: Path) -> None:
    """combine_pdfs: raises error for invalid PDF files."""
    pdf_file = tmp_path / "test.pdf"
    pdf_file.write_bytes(b"Not a PDF file")
    output_file = tmp_path / "output.pdf"
    with pytest.raises(PDFCombineError) as exc_info:
        combine_pdfs([pdf_file], output_file)
    assert "Failed to combine PDFs" in str(exc_info.value)
    pdf_file.write_bytes(
        b"%PDF-1.4\n"
        b"1 0 obj\n"
        b"<< /Type /Catalog /Pages 2 0 R >>\n"
        b"endobj\n"
        b"%%EOF\n"
    )
    with pytest.raises(PDFCombineError) as exc_info:
        combine_pdfs([pdf_file], output_file)
    assert "Failed to combine PDFs" in str(exc_info.value)
    abs_pdf = Path("/tmp/test.pdf")
    abs_pdf.write_bytes(
        b"%PDF-1.4\n"
        b"1 0 obj\n"
        b"<< /Type /Catalog /Pages 2 0 R >>\n"
        b"endobj\n"
        b"2 0 obj\n"
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>\n"
        b"endobj\n"
        b"3 0 obj\n"
        b"<< /Type /Page /Parent 2 0 R /Resources <<>> /MediaBox [0 0 612 792] >>\n"
        b"endobj\n"
        b"xref\n"
        b"0 4\n"
        b"0000000000 65535 f\n"
        b"0000000010 00000 n\n"
        b"0000000056 00000 n\n"
        b"0000000112 00000 n\n"
        b"trailer\n"
        b"<< /Size 4 /Root 1 0 R >>\n"
        b"startxref\n"
        b"164\n"
        b"%%EOF\n"
    )
    abs_output = Path("/tmp/output.pdf")
    combine_pdfs([abs_pdf], abs_output)
    assert abs_output.exists() and abs_output.stat().st_size > 0


def test_convert_svg_to_pdf_cairosvg(tmp_path: Path) -> None:
    """convert_svg_to_pdf: valid SVG is converted to PDF."""
    svg_file = tmp_path / "test.svg"
    svg_content = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">'
        '<rect width="100" height="100" fill="red"/>'
        '<text x="50" y="50" text-anchor="middle">Test</text>'
        "</svg>"
    )
    svg_file.write_text(svg_content)
    output_file = tmp_path / "output.pdf"
    convert_svg_to_pdf(svg_file, output_file, backend="cairosvg")
    assert output_file.exists() and output_file.stat().st_size > 0
    reader = pypdf.PdfReader(output_file)
    assert len(reader.pages) == 1
    assert reader.metadata is not None


def test_convert_svg_to_pdf_unknown_backend(tmp_path: Path) -> None:
    """convert_svg_to_pdf: raises error for unknown backend."""
    svg_file = tmp_path / "test.svg"
    svg_file.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">'
        '<rect width="100" height="100" fill="red"/></svg>'
    )
    output_file = tmp_path / "output.pdf"
    with pytest.raises(SVGConversionError) as exc_info:
        convert_svg_to_pdf(svg_file, output_file, backend="unknown")
    assert "Unknown svg2pdf backend" in str(exc_info.value)
    assert not output_file.exists()


def test_convert_svg_to_pdf_invalid_svg(tmp_path: Path) -> None:
    """convert_svg_to_pdf: raises error for invalid SVG content."""
    svg_file = tmp_path / "test.svg"
    svg_file.write_text("Not an SVG file", encoding="utf-8")
    output_file = tmp_path / "output.pdf"
    with pytest.raises(SVGConversionError) as exc_info:
        convert_svg_to_pdf(svg_file, output_file)
    assert "syntax error" in str(exc_info.value)
    assert not output_file.exists()
    svg_file.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">'
        '<rect width="100" height="100" fill="red">',
        encoding="utf-8",
    )
    with pytest.raises(SVGConversionError) as exc_info:
        convert_svg_to_pdf(svg_file, output_file)
    assert "no element found" in str(exc_info.value)
    assert not output_file.exists()
    abs_svg = Path("/tmp/test.svg")
    abs_svg.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">'
        '<rect width="100" height="100" fill="red"/></svg>',
        encoding="utf-8",
    )
    abs_output = Path("/tmp/output.pdf")
    convert_svg_to_pdf(abs_svg, abs_output)
    assert abs_output.exists() and abs_output.stat().st_size > 0
