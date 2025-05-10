"""Tests for rendering functionality."""

import base64
from pathlib import Path

import jinja2
import pytest

from pdfbaker.render import (
    PDFBakerTemplate,
    create_env,
    encode_image,
    encode_images,
    prepare_template_context,
)


# Template environment tests
def test_create_env(tmp_path: Path) -> None:
    """Jinja environment is created with correct loader and template class."""
    env = create_env(tmp_path)
    assert isinstance(env, jinja2.Environment)
    assert env.template_class == PDFBakerTemplate
    assert isinstance(env.loader, jinja2.FileSystemLoader)
    assert str(tmp_path) in env.loader.searchpath
    assert env.trim_blocks is False
    assert env.lstrip_blocks is False


def test_create_env_no_directory() -> None:
    """create_env raises ValueError if no directory is given."""
    with pytest.raises(ValueError, match="templates_dir is required"):
        create_env(None)


# Template rendering tests
def test_highlighting_template() -> None:
    """PDFBakerTemplate: highlight tags are rendered as <tspan> with color."""
    # Test case 1: Basic highlighting
    template = PDFBakerTemplate("<highlight>test</highlight>")
    result = template.render(
        renderers=["render_highlight"], style={"highlight_color": "red"}
    )
    assert result == '<tspan style="fill:red">test</tspan>'

    # Test case 2: Nested highlighting (pointless but supported)
    template = PDFBakerTemplate(
        "<highlight>outer <highlight>inner</highlight> text</highlight>"
    )
    result = template.render(
        renderers=["render_highlight"], style={"highlight_color": "blue"}
    )
    expected = (
        '<tspan style="fill:blue">outer <tspan style="fill:blue">inner</tspan> '
        "text</tspan>"
    )
    assert result == expected

    # Test case 3: No highlighting
    template = PDFBakerTemplate("plain text")
    result = template.render(renderers=["render_highlight"])
    assert result == "plain text"


def test_highlighting_template_no_style() -> None:
    """PDFBakerTemplate: highlight tags are not replaced if no color is given."""
    template = PDFBakerTemplate("<highlight>test</highlight>")
    result = template.render(
        renderers=["render_highlight"],
        # No style provided
    )
    assert result == "<highlight>test</highlight>"


# Context preparation tests
def test_prepare_template_context_images(tmp_path: Path) -> None:
    """prepare_template_context encodes images in context."""
    # Create test image
    images_dir = tmp_path / "images"
    images_dir.mkdir()
    image_path = images_dir / "test.png"
    image_path.write_bytes(b"fake image data")

    config = {
        "images": [
            {"name": "test.png"},
        ]
    }
    context = prepare_template_context(config, images_dir)
    assert context["images"][0]["type"] == "default"  # Default type added
    assert context["images"][0]["data"].startswith("data:image/png;base64,")


# Image encoding tests
def test_encode_image(tmp_path: Path) -> None:
    """encode_image encodes PNG and JPG images to base64 data URIs."""
    # Test case 1: PNG image
    image_path = tmp_path / "test.png"
    image_data = b"fake image data"
    image_path.write_bytes(image_data)

    result = encode_image("test.png", tmp_path)
    assert result.startswith("data:image/png;base64,")
    encoded_data = result.split(",")[1]
    decoded_data = base64.b64decode(encoded_data)
    assert decoded_data == image_data

    # Test case 2: JPEG image
    image_path = tmp_path / "test.jpg"
    image_path.write_bytes(image_data)
    result = encode_image("test.jpg", tmp_path)
    assert result.startswith("data:image/jpg;base64,")


def test_encode_image_not_found(tmp_path: Path) -> None:
    """encode_image raises FileNotFoundError for missing file."""
    with pytest.raises(FileNotFoundError):
        encode_image("missing.png", tmp_path)


def test_encode_images(tmp_path: Path) -> None:
    """encode_images encodes multiple images and preserves types."""
    # Create test images
    images_dir = tmp_path / "images"
    images_dir.mkdir()
    (images_dir / "test1.png").write_bytes(b"image1")
    (images_dir / "test2.png").write_bytes(b"image2")
    (images_dir / "test3.jpg").write_bytes(b"image3")

    # Test case 1: Basic image list
    images = [
        {"name": "test1.png"},
        {"name": "test2.png", "type": "custom"},
    ]

    result = encode_images(images, images_dir)
    assert len(result) == 2
    assert result[0]["type"] == "default"  # Default type added
    assert result[1]["type"] == "custom"  # Existing type preserved
    assert result[0]["data"].startswith("data:image/png;base64,")
    assert result[1]["data"].startswith("data:image/png;base64,")

    # Verify image data
    assert base64.b64decode(result[0]["data"].split(",")[1]) == b"image1"
    assert base64.b64decode(result[1]["data"].split(",")[1]) == b"image2"

    # Test case 2: Mixed image types
    images = [
        {"name": "test1.png"},
        {"name": "test3.jpg", "type": "photo"},
    ]

    result = encode_images(images, images_dir)
    assert len(result) == 2
    assert result[0]["data"].startswith("data:image/png;base64,")
    assert result[1]["data"].startswith("data:image/jpg;base64,")


def test_encode_images_no_directory() -> None:
    """encode_images raises ValueError if images_dir is None."""
    with pytest.raises(ValueError, match="images_dir is required"):
        encode_images([{"name": "test.png"}], None)


def test_prepare_template_context(tmp_path: Path) -> None:
    """prepare_template_context encodes images and preserves other fields."""
    # Create test images directory and image
    images_dir = tmp_path / "images"
    images_dir.mkdir()
    test_image = images_dir / "test.png"
    test_image.write_bytes(b"fake image data")

    # Test case 1: Context with images
    context = {
        "title": "Test Document",
        "images": [
            {"name": "test.png"},
            {"name": "test.png", "type": "custom"},
        ],
    }
    result = prepare_template_context(context, images_dir)

    # Verify images were encoded
    assert len(result["images"]) == 2
    assert result["images"][0]["type"] == "default"  # Default type added
    assert result["images"][1]["type"] == "custom"  # Existing type preserved
    assert all(
        img["data"].startswith("data:image/png;base64,") for img in result["images"]
    )

    # Verify original context is preserved
    assert result["title"] == "Test Document"

    # Test case 2: Context without images
    context = {"title": "Test Document"}
    result = prepare_template_context(context, images_dir)
    assert result == context  # Context unchanged when no images

    # Test case 3: Missing images_dir
    context = {"images": [{"name": "test.png"}]}
    with pytest.raises(
        ValueError, match="images_dir is required when processing images"
    ):
        prepare_template_context(context, None)
