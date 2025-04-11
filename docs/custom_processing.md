# Custom Processing

For advanced use cases, you can create a `bake.py` file in your document directory to
customize the document generation process. This allows you to:

- Add custom preprocessing steps
- Modify content dynamically
- Generate content programmatically
- Handle complex document structures

## Basic Structure

Your `bake.py` should define a `process_document` function:

```python
from pdfbaker.document import PDFBakerDocument

def process_document(document: PDFBakerDocument) -> None:
    # Custom processing logic here
    pass
```

## Document Object

The `document` parameter provides access to:

- Document configuration
- Variant processing
- Page rendering
- File management

### Key Methods and Properties

```python
# Access configuration
config = document.config

# Process variants
for variant in document.config.get('variants', []):
    # Process variant...

# Process pages
for page in document.config.get('pages', []):
    # Process page...

# File management
build_dir = document.build_dir
dist_dir = document.dist_dir
```

## Example: Dynamic Pricing

Here's an example that calculates dynamic pricing based on features:

```python
def process_document(document):
    # Load pricing data
    with open('content/pricing_data.yaml') as f:
        pricing_data = yaml.safe_load(f)

    # Calculate pricing for each variant
    for variant in document.config.get('variants', []):
        base_price = document.config['content']['base_price']
        features = len(variant['content']['features'])

        # Adjust price based on features
        adjusted_price = base_price * (1 + (features - 1) * 0.1)
        final_price = adjusted_price * (1 - variant['content']['discount'])

        # Update variant content
        variant['content']['final_price'] = round(final_price, 2)

    # Process as usual
    document.process()
```

## Example: Content Generation

Generate content dynamically based on external data:

```python
def process_document(document):
    # Fetch data from API
    response = requests.get('https://api.example.com/data')
    data = response.json()

    # Update document content
    document.config['content'].update({
        'latest_data': data,
        'generated_at': datetime.now().isoformat()
    })

    # Process as usual
    document.process()
```
