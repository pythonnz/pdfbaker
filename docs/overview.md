# pdfbaker Overview

pdfbaker creates PDF documents from SVG templates and YAML configuration. Quick and easy
out of the box, it's flexible enough to allow for heavy customisation.

- **SVG**: Full control over document layout and design
- **Jinja2**: Replace static content in your SVG with variables, conditions, loops
- **YAML**: Configure your content in plain text
- **PDF**: Your end result, optionally compressed

## Use cases

Use SVG to create documents that need precise positioning, complex layouts with
overlapping elements, specific fonts or custom shapes:

- Posters and flyers
- Marketing materials (brochures, prospectuses)
- Fancy reports and certificates
- Any document requiring precise design control

Configuring and editing content in plaintext YAML files is great if you create the same
types of documents again and again.

Use pdfbaker as a command line tool or Python libary.

## When not to use pdfbaker

- When you need something other than PDF
- When flexible document flow is more important than precise positioning

You may want to consider using an Office Suite, HTML/CSS, Markdown or a text-first tool
like LaTex, even if your end result is exported to PDF.

## Advanced features

- [Configuration Reference](configuration.md) - All available settings
- [Document Variants](variants.md) - Create multiple versions of the same document
- [Custom Processing](custom_processing.md) - Provide page content from anywhere

## Workflow

1. Create your document in an SVG editor or convert to SVG
2. Replace text with variables, add conditions and loops using Jinja2
3. Configure your content and settings in YAML
4. Generate PDFs with `pdfbaker bake`

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

## Examples

See the [examples](examples) directory:

- [minimal](examples/minimal) - Basic usage
- [regular](examples/regular) - Standard features
- [variants](examples/variants) - Document variants
- [custom_locations](examples/custom_locations) - Custom file/directory locations
- [custom_processing](examples/custom_processing) - Custom processing with Python

## Getting Help

If something doesn't work as advertised or is not clearly enough documented, please
[open an issue](https://github.com/pythonnz/pdfbaker/issues) on GitHub.
