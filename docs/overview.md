# pdfbaker Overview

pdfbaker is a tool for generating PDF documents from SVG templates and YAML
configuration. It's designed to be flexible and powerful, allowing you to create complex
documents with minimal effort.

## Key Features

- **SVG Layout Control**: Full control over document layout and design
- **Simple Configuration**: YAML for easy content management
- **Dynamic Content**: Jinja2 templating for variable text, conditions, and loops
- **Document Variants**: Create multiple versions of the same document
- **Custom Processing**: Extend the processing workflow with Python
- **PDF Compression**: Optional compression of final PDFs

## Quickstart

For a quick introduction, see the [README](../README.md).

## Workflow

### From configuration to PDF documents

Your main configuration defines which documents to create.<br>Each document
configuration defines which pages make up the document.

```mermaid
flowchart TD
    Main[YAML Main Config] -->|document 1| Doc1[Document Processing]
    Main -->|document 2| Doc2[Document Processing]

    subgraph Document[YAML Document Config]
        Doc1 -->|page 1| Page1[Page Processing]
        Doc1 -->|page 2| Page2[Page Processing]
        Doc1 -->|page ...| PageN[Page Processing]

        Page1 --> PDF1[PDF File Page 1]
        Page2 --> PDF2[PDF File Page 2]
        PageN --> PDFN[PDF File Page ...]

        PDF1 --> PDF[PDF Pages]
        PDF2 --> PDF[PDF Pages]
        PDFN --> PDF[PDF Pages]

        PDF -->|combine| PDFDocument[PDF Document]
    end

    Doc2 -->|pages| Doc2PageProcessing[...]
    Doc2PageProcessing --> Doc2PageFile[...]
    Doc2PageFile --> Doc2Pages[...]
    Doc2Pages -->|combine| Doc2PDFDocument[PDF Document]
```

### Inheriting common values

Settings in the main configuration are available to all documents.<br>Settings in a
document configuration are available to all of its pages.<br>Each page configuration can
hold page-specific settings/content, so that the template of the page is only
responsible for layout/design.

```mermaid
flowchart TD
    subgraph Configuration
        Main[YAML Main Config] -->|inherits| Doc[YAML Document Config]
        Doc -->|inherits| Page[YAML Page Config]
    end

    subgraph Page Processing
        Template[SVG Template]
        Page -->|context| Render[Template Rendering]
        Template -->|jinja2| Render
        Render -->|output| SVG[SVG File]
        SVG -->|cairosvg| PDF[PDF File]
    end
```

### Pages make up a document

After each page template was rendered and the resulting SVG file converted to PDF, these
page PDFs are combined to create the document.<br>This PDF document may optionally get
compressed for a nice end result.

```mermaid
flowchart LR
    subgraph Document Creation
        Page1[PDF File Page 1] -->|combine| Document[PDF Document]
        Page2[PDF File Page 2] -->|combine| Document
        PageN[PDF File Page ...] -->|combine| Document
        Document -.->|ghostscript| Compressed[PDF Document compressed]
        linkStyle 3 stroke-dasharray: 5 5
    end
```

## Documentation

- [Configuration](configuration.md) - How to set up your documents
- [Document Variants](variants.md) - Create multiple versions of a document
- [Custom Processing](custom_processing.md) - Extend the processing workflow

## Examples

See the [examples](examples) directory:

- [minimal](examples/minimal) - Basic usage
- [regular](examples/regular) - Standard features
- [variants](examples/variants) - Document variants
- [custom_locations](examples/custom_locations) - Custom file/directory locations
- [custom_processing](examples/custom_processing) - Custom processing with Python

## Example Project Structure

```
project/
├── kiwipycon.yaml        # Main configuration
├── material_specs/       # A document
│   ├── config.yaml       # Document configuration
│   ├── images/           # Images
│   ├── pages/            # Page configurations
│   └── templates/        # SVG templates
└── prospectus/           # Another document
    ├── config.yaml
    ├── images/
    ├── pages/
    └── templates/
```

## Workflow

1. Create your document design in an SVG editor
2. Replace text with variables, add conditions and loops using Jinja2
3. Configure your content and settings in YAML
4. Generate PDFs with `pdfbaker bake`

## Use Cases

pdfbaker is ideal for any document that needs precise layout control. Unlike HTML-based
solutions, SVG gives you:

- Exact positioning of every element
- Full control over typography
- Complex layouts with overlapping elements
- Precise image placement
- Custom shapes and paths

## Getting Help

- [Open an issue](https://github.com/pythonnz/pdfbaker/issues) on GitHub
