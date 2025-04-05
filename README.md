# kpc-sponsorship

Creates a [Kiwi PyCon](https://kiwipycon.nz/) sponsorship prospectus and material specs
documents for different sponsorship tiers in PDF format.

The main branch has a year tag for the version that is/was used for that particular
year's conference, like
"[2025](https://github.com/pythonnz/kpc-sponsorship/releases/tag/2025)".

## Requirements

- [Roboto fonts](https://fonts.google.com/specimen/Roboto) - the font we use
- [Jinja2](https://jinja.palletsprojects.com/en/stable/) (>=3.1.3) - to render the SVG
  templates
- [Inkscape](https://inkscape.org/) - to convert SVG to PDF
- [pypdf](https://pypdf.readthedocs.io/en/stable/index.html) (>=4.3.1) - to assemble PDF
  pages to a document
- [Ghostscript](https://www.ghostscript.com/) - for PDF compression

```
sudo apt install fonts-roboto
sudo apt install python3-jinja2
sudo apt install inkscape
sudo apt install python3-pypdf
sudo apt install ghostscript
```

The two Python dependencies can also be installed with pip:

```
pip install -r requirements.txt
```

The requirements file installs at least the versions that currently get installed by the
above system packages on Ubuntu 24.10.

## Usage

Generate all documents with:

```
python3 -m generate
```

This will create a `build/` directory and a `dist/` directory (both ignored by git).<br>
It will produce your PDF files in the `dist/` directory (and leave some artifacts in the
`build/` directory, mainly for debugging).

## Structure and Workflow

A total of 6 documents are generated:

- Sponsorship Prospectus
- Material Specs - Diamond
- Material Specs - Platinum
- Material Specs - Gold
- Material Specs - Silver
- Material Specs - Bronze

A **document** is made up of **pages**.<br> Pages take their layout from **templates**,
and their specific content from your **configuration**. They may also include
**images**.

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

- `config/`<br> contains the configuration of all documents. It describes which pages
  make up a document and in which order, and what specific content to insert. Common
  configuration is in `common.yml`, document-specific configuration in their respective
  files.<br> You will at the very least need to to adjust the year for your next
  conference in `common.yml`.

- `generate/`<br> Contains the code for generating documents.<br> The main entry point
  for invoking the generator is in `__main__.py`. Common functionality is in
  `common.py`. Helper functions for rendering the SVGs with Jinja are in `render.py`.
  Each document gets its own separate module under `documents/`.<br> Documents are
  generated using the above framework. A top-level `build/` working directory and a
  `dist/` directory for the final results will be created. If they already exist they
  will be wiped clean.<br> In the `build/` directory, it will create individual `.svg`
  files for each page, convert them to `.pdf` files, and then combine them into a single
  `.pdf` file for each document and place them in the `dist/` directory. The prospectus
  PDF will also be compressed.

Note: You need to follow a consistent naming convention.
`generate/documents/prospectus.py` will be given the combined configuration of
`config/common.yml` and `config/prospectus.yml`. It will take its pages from
`pages/prospectus/`. Do the same for any new documents you may add.

## Development

Your changes will be rejected by github if the linters throw warnings. You should
install [pre-commmit](https://pre-commit.com) and run

```
pre-commit install
```

inside your repo. This will ensure you run the same checks as github every time you
commit.

## Known Issues

See [Github Issues](https://github.com/pythonnz/kpc-sponsorship/issues) for known
issues.
