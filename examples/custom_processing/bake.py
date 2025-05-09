"""Custom processing example - fetches latest XKCD comic."""

import base64
import json
import urllib.request
from datetime import datetime

from pdfbaker.document import Document
from pdfbaker.errors import PDFBakerError
from pdfbaker.processing import wordwrap


def process_document(document: Document) -> None:
    """Process document with live XKCD comic."""
    try:
        # Fetch latest XKCD
        with urllib.request.urlopen("https://xkcd.com/info.0.json") as response:
            data = json.loads(response.read())

        # Download and encode the image
        with urllib.request.urlopen(data["img"]) as img_response:
            img_data = img_response.read()
            image_data = (
                f"data:image/png;base64,{base64.b64encode(img_data).decode('utf-8')}"
            )

        # Get the alt text and split it into lines using the wordwrap function
        # Note: This is for demonstration. Could use the wordwrap filter in template.
        wrapped_alt_text = wordwrap(data["alt"], max_chars=60)

        # Log a message to show during document processing
        document.log_info("Setting XKCD data for template context 🙂")

        # Update config/template context with XKCD info
        document.config.xkcd = {
            "title": data["title"],
            "alt_text": data["alt"],
            "alt_text_lines": wrapped_alt_text,
            "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "image_data": image_data,
        }
    except Exception as exc:
        raise PDFBakerError(f"Failed to process XKCD example: {exc}") from exc

    return document.process()
