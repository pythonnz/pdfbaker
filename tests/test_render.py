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
    """Test creating Jinja environment."""
    env = create_env(tmp_path)
    assert isinstance(env, jinja2.Environment)
    assert env.template_class == PDFBakerTemplate
    assert isinstance(env.loader, jinja2.FileSystemLoader)


def test_create_env_no_directory() -> None:
    """Test create_env with no directory."""
    with pytest.raises(ValueError, match="templates_dir is required"):
        create_env(None)


# Template rendering tests
def test_highlighting_template() -> None:
    """Test highlighting template functionality."""
    template = PDFBakerTemplate("<highlight>test</highlight>")
    result = template.render(
        renderers=["render_highlight"], style={"highlight_color": "red"}
    )
    assert result == '<tspan style="fill:red">test</tspan>'


def test_highlighting_template_no_style() -> None:
    """Test highlighting template with no highlight color."""
    template = PDFBakerTemplate("<highlight>test</highlight>")
    result = template.render(
        renderers=["render_highlight"],
        # No style provided
    )
    assert result == "<highlight>test</highlight>"


# Context preparation tests
def test_prepare_template_context_styles() -> None:
    """Test style resolution in template context."""
    config = {
        "style": {"color": "primary"},
        "theme": {"primary": "#ff0000"},
    }
    context = prepare_template_context(config)
    assert context["style"]["color"] == "#ff0000"


def test_prepare_template_context_images(tmp_path: Path) -> None:
    """Test image processing in template context."""
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
    """Test encoding a single image to base64."""
    # Create test image file
    image_path = tmp_path / "test.png"
    image_path.write_bytes(b"fake image data")

    # Encode the image
    result = encode_image("test.png", tmp_path)

    # Verify the result
    assert result.startswith("data:image/png;base64,")
    encoded_data = result.split(",")[1]
    decoded_data = base64.b64decode(encoded_data)
    assert decoded_data == b"fake image data"


def test_encode_image_not_found(tmp_path: Path) -> None:
    """Test handling of missing image file."""
    with pytest.raises(FileNotFoundError):
        encode_image("missing.png", tmp_path)


def test_encode_images(tmp_path: Path) -> None:
    """Test encoding multiple images."""
    # Create test images
    images_dir = tmp_path / "images"
    images_dir.mkdir()
    (images_dir / "test1.png").write_bytes(b"image1")
    (images_dir / "test2.png").write_bytes(b"image2")

    images = [
        {"name": "test1.png"},
        {"name": "test2.png", "type": "custom"},
    ]

    result = encode_images(images, images_dir)
    assert len(result) == 2
    assert result[0]["type"] == "default"  # Default type added
    assert result[1]["type"] == "custom"  # Existing type preserved
    assert all(img["data"].startswith("data:image/png;base64,") for img in result)


def test_encode_images_no_directory() -> None:
    """Test encode_images with no directory."""
    with pytest.raises(ValueError, match="images_dir is required"):
        encode_images([{"name": "test.png"}], None)
