"""Tests for PDF processing functionality."""

import logging
from pathlib import Path
from unittest.mock import patch

import pytest

from pdfbaker.pdf import (
    PDFCombineError,
    PDFCompressionError,
    SVGConversionError,
    combine_pdfs,
    compress_pdf,
    convert_svg_to_pdf,
)


def test_combine_pdfs_empty_list(tmp_path: Path) -> None:
    """Test combining empty list of PDFs."""
    output_file = tmp_path / "output.pdf"
    with pytest.raises(PDFCombineError, match="No PDF files provided to combine"):
        combine_pdfs([], output_file)


def test_combine_pdfs_single_file(tmp_path: Path) -> None:
    """Test combining a single PDF file."""
    # Create a valid PDF file
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

    output_file = tmp_path / "output.pdf"
    combine_pdfs([pdf_file], output_file)
    assert output_file.exists()


def test_combine_pdfs_multiple_files(tmp_path: Path) -> None:
    """Test combining multiple PDF files."""
    # Create two valid PDF files
    pdf1 = tmp_path / "test1.pdf"
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

    pdf2 = tmp_path / "test2.pdf"
    pdf2.write_bytes(
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

    output_file = tmp_path / "output.pdf"
    combine_pdfs([pdf1, pdf2], output_file)
    assert output_file.exists()


def test_combine_pdfs_broken_annotations(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """Test combining PDFs with broken annotations."""
    # Create PDF with annotation missing a required /Subtype field
    # This will trigger the specific KeyError("'/Subtype'") exception
    pdf_file = tmp_path / "test.pdf"

    # The key part is creating an annotation without a Subtype
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
        b"<< /Type /Annot /Rect [0 0 0 0] >>\n"  # Missing /Subtype field
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
        # Manually reinstall caplog handler to the root logger
        logging.getLogger().addHandler(caplog.handler)
        combine_pdfs([pdf_file], output_file)

    # Check for our specific broken annotations warning
    assert "Broken annotations in PDF" in caplog.text
    assert "Falling back to page-by-page method" in caplog.text
    assert output_file.exists()


def test_combine_pdfs_invalid_file(tmp_path: Path) -> None:
    """Test combining invalid PDF files."""
    pdf_file = tmp_path / "test.pdf"
    pdf_file.write_bytes(b"Not a PDF file")

    output_file = tmp_path / "output.pdf"
    with pytest.raises(PDFCombineError, match="Failed to combine PDFs"):
        combine_pdfs([pdf_file], output_file)


def test_convert_svg_to_pdf_cairosvg(tmp_path: Path) -> None:
    """Test SVG to PDF conversion using cairosvg."""
    # Create a valid SVG file
    svg_file = tmp_path / "test.svg"
    svg_file.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">'
        '<rect width="100" height="100" fill="red"/></svg>'
    )

    output_file = tmp_path / "output.pdf"
    convert_svg_to_pdf(svg_file, output_file, backend="cairosvg")
    assert output_file.exists()


def test_convert_svg_to_pdf_unknown_backend(tmp_path: Path) -> None:
    """Test SVG to PDF conversion with unknown backend."""
    svg_file = tmp_path / "test.svg"
    svg_file.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">'
        '<rect width="100" height="100" fill="red"/></svg>'
    )
    output_file = tmp_path / "output.pdf"
    with pytest.raises(SVGConversionError) as exc_info:
        convert_svg_to_pdf(svg_file, output_file, backend="unknown")
    assert "Unknown svg2pdf backend" in str(exc_info.value)


def test_convert_svg_to_pdf_invalid_svg(tmp_path: Path) -> None:
    """Test SVG to PDF conversion with invalid SVG."""
    svg_file = tmp_path / "test.svg"
    svg_file.write_text("Not an SVG file")
    output_file = tmp_path / "output.pdf"
    with pytest.raises(SVGConversionError) as exc_info:
        convert_svg_to_pdf(svg_file, output_file)
    assert "syntax error: line 1, column 0" in str(exc_info.value)


def test_compress_pdf_missing_ghostscript(tmp_path: Path) -> None:
    """Test PDF compression with missing Ghostscript."""
    pdf_file = tmp_path / "test.pdf"
    pdf_file.write_bytes(b"%PDF-1.4\n%%EOF\n")

    output_file = tmp_path / "output.pdf"
    # Use a realistic error message that would occur when gs is not found
    with patch(
        "pdfbaker.pdf._run_subprocess_logged",
        side_effect=FileNotFoundError("gs: command not found"),
    ):
        with pytest.raises(PDFCompressionError) as exc_info:
            compress_pdf(pdf_file, output_file)

    # Check that our error message is included in the PDFCompressionError
    assert "Ghostscript not found" in str(exc_info.value)
