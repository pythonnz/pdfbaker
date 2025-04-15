# Custom Processing

For advanced use cases, you can create a `bake.py` file in your document directory to
customize the document generation process. This allows you to:

- Add custom preprocessing steps
- Modify content dynamically
- Generate content programmatically
- Handle complex document structures

## Basic Structure

As a naming convention, your `bake.py` needs to define a `process_document` function:

```python
from pdfbaker.document import PDFBakerDocument

def process_document(document: PDFBakerDocument) -> None:
    # Custom processing logic here
    document.process()
```

You will usually just manipulate the data for your templates, and then call `.process()`
on the document to continue with the built-in stages of combining pages and compressing
the PDF as configured.

See `examples/custom_processing/bake.py` for a simple example of how to do this.

If you need to fully customise the processing, make sure that your function returns a
Path or list of Path objects (the PDF files that were created) as that is the expected
type of return value for logging.
