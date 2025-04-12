"""Tests for rendering functionality."""

import base64

import pytest

from pdfbaker.render import encode_image


def test_encode_image(tmp_path):
    """Test encoding an image to base64."""
    # Create a test image file
    image_path = tmp_path / "test.png"
    image_path.write_bytes(b"fake image data")

    # Encode the image
    result = encode_image("test.png", tmp_path)

    # Verify the result
    assert result.startswith("data:image/png;base64,")
    encoded_data = result.split(",")[1]
    decoded_data = base64.b64decode(encoded_data)
    assert decoded_data == b"fake image data"


def test_encode_image_not_found(tmp_path):
    """Test handling of missing image file."""
    with pytest.raises(FileNotFoundError):
        encode_image("missing.png", tmp_path)
