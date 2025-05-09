# Custom Processing

For advanced use cases, you can create a `bake.py` file in your document directory to
customize the document generation process. This allows you to modify existing and inject
additional settings and content.

## Basic Structure

As a naming convention, your `bake.py` needs to define a `process_document` function:

```python
from pdfbaker.document import Document

def process_document(document: Document) -> None:
    """Get settings from other places."""
    # Inject additional data into document.config
    document.config.profit_and_loss = query_xero_api()
    # Continue with regular processing
    return document.process()
```

You will usually just manipulate the data for your templates, and then call `.process()`
on the document to continue with the built-in stages of rendering and combining pages as
configured.

If you need to fully customise the processing, make sure that your function returns a
single `pathlib.Path` or list of such `Path` objects (the PDF files that were created)
as that is the expected type of return value for logging.

## Example

See [the custom_processing example](../examples/custom_processing) for an implementation
that insert the latest XKCD comic into your PDF.
