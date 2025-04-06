# pdfbaker

Creates PDF documents from YAML-configured SVG templates.

## Requirements

For the conversion from SVG to PDF you need to install either

- [CairoSVG](https://cairosvg.org/)<br>
  ```
  sudo apt install python3-cairosvg
  ```

or

- [Inkscape](https://inkscape.org/)<br>
  ```
  sudo apt install inkscape
  ```

If you want to compress your PDFs, you will also need to install

- [Ghostscript](https://www.ghostscript.com/)
  ```
  sudo apt install ghostscript
  ```

## Installation

pdfbaker is on [PyPI](https://pypi.org/project/pdfbaker/) and we reommend installing it
using [pipx](https://github.com/pypa/pipx):

```
pipx install pdfbaker
```

If you don't yet have pipx,
[install it first](https://pipx.pypa.io/latest/installation/):

```
sudo apt install pipx
pipx ensurepath
```

## Usage

Generate your documents with:

```
pdfbaker <path_to_config_file>
```

This will create a `build/` directory and a `dist/` directory where your configuration
file lives.<br> It will produce your PDF files in the `dist/` directory (and leave some
artifacts in the `build/` directory to aid debugging).

## Configuration

**FIXME: This is hard to find useful without seeing an example or the required settings
to e.g. enable compression.**

A **document** is made up of **pages**.<br> Pages take their layout from **templates**,
and their specific content from your **configuration**. They may also include
**images**.

Your configuration file can describe multiple documents, each having further
configuration and files in their own directory next to the configuration.

Each document directory consists of:

- `templates/`<br> contains `.svg.j2` files describing the layout of a page. These are
  Jinja2 templates which are used to render pages in SVG format, which then gets
  transformed into PDF.<br> They contain placeholders for text and images.<br> You only
  need to work with these files if you want to make fundamental layout or branding
  changes.

- `pages/`<br> contains one `.yml` file for each page of a document. These files
  describe which template to use, which image files (if any) should be used in its
  template, and they also define content which generally doesn't need to be
  configurable.<br> You only need to work with these files if you want to change text
  that is usually fixed, or if you want to change which images are used.

- `images/`<br> contains the actual image files referenced in the `.yml` files for
  pages.

- `config.yml`<br> contains the configuration of the document (and possibly its
  variants). It describes which pages make up the document and in which order, and what
  specific content to insert. When your templates are processed, this document-specific
  configuration will be merged with your main configuration file, so you can keep
  settings in the latter to share between different documents.

- `bake.py`<br> Contains the code for generating your documents.<br> It will create
  individual `.svg` files for each page, convert them to `.pdf` files, and then combine
  them into a single `.pdf` file for each document and place those in the `dist/`
  directory. Where configured to do so, your PDF will also be compressed.

While you have to write the document generation yourself in `bake.py`, it is little code
and gives you full control - for example, one document may create just one PDF file but
another might creates half a dozen variations of itself. All that logic is in your
`bake.py`.

## Development

The source code of pdfbaker lives [on github](https://github.com/pythonnz/pdfbaker).

Your changes will be rejected by github if the linters throw warnings. You should
install [pre-commmit](https://pre-commit.com) and run

```
pre-commit install
```

inside your repo. This will ensure you run the same checks as github every time you
commit.

## Known Issues

See [Github Issues](https://github.com/pythonnz/pdfbaker/issues) for known issues.
