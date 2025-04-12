"""Custom processing example - fetches latest XKCD comic."""

import base64
import json
import urllib.request
from datetime import datetime

from pdfbaker.document import PDFBakerDocument
from pdfbaker.errors import PDFBakeError


def process_document(document: PDFBakerDocument) -> None:
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

        # Update config with XKCD info
        document.config["xkcd"] = {
            "title": data["title"],
            "alt_text": data["alt"],
            "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "image_data": image_data,
        }

        # Process as usual
        document.process()
    except Exception as exc:
        raise PDFBakeError(f"Failed to process XKCD example: {exc}") from exc
