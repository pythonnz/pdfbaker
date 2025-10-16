# pdfbaker

[![PyPI version](https://img.shields.io/pypi/v/pdfbaker?color=blue)](https://pypi.org/project/pdfbaker/)
[![Python](https://img.shields.io/python/required-version-toml?color=blue&tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fpythonnz%2Fpdfbaker%2Fmain%2Fpyproject.toml)](https://github.com/pythonnz/pdfbaker/blob/main/pyproject.toml)
[![Downloads](https://img.shields.io/pypi/dw/pdfbaker?color=blue)](https://pypistats.org/packages/pdfbaker)
[![sigstore](https://img.shields.io/badge/sigstore-signed-blue)](https://github.com/pythonnz/pdfbaker/releases)
[![tests](https://github.com/pythonnz/pdfbaker/actions/workflows/tests.yaml/badge.svg)](https://github.com/pythonnz/pdfbaker/actions/workflows/tests.yaml)
[![codecov](https://img.shields.io/codecov/c/github/pythonnz/pdfbaker)](https://codecov.io/gh/pythonnz/pdfbaker)
[![OSSF Scorecard](https://img.shields.io/ossf-scorecard/github.com/pythonnz/pdfbaker?label=OSSF%20Scorecard)](https://scorecard.dev/viewer/?uri=github.com/pythonnz/pdfbaker)
[![pip-audit](https://img.shields.io/github/actions/workflow/status/pythonnz/pdfbaker/pip-audit.yaml?label=pip-audit&logo=python)](https://github.com/pythonnz/pdfbaker/actions/workflows/pip-audit.yaml)
[![bandit](https://img.shields.io/github/actions/workflow/status/pythonnz/pdfbaker/bandit.yaml?label=bandit&logo=python)](https://github.com/pythonnz/pdfbaker/actions/workflows/bandit.yaml)
[![Last commit](https://img.shields.io/github/last-commit/pythonnz/pdfbaker?color=lightgrey)](https://github.com/pythonnz/pdfbaker/commits/main)
[![License](https://img.shields.io/github/license/pythonnz/pdfbaker?color=lightgrey)](https://github.com/pythonnz/pdfbaker/blob/main/LICENSE)

Create PDF documents from YAML-configured SVG templates.

- **Separation of design and content:** Design your layout visually in SVG while
  managing content and configuration in YAML.
- **Instant templating:** Turn any existing SVG into a configurable template with a
  single command.

## Installation

pdfbaker is available on [PyPI](https://pypi.org/project/pdfbaker/) and can be installed
using [pipx](https://github.com/pypa/pipx):

```bash
pipx install pdfbaker
```

If you don't have pipx yet,
[install it first](https://pipx.pypa.io/latest/installation/):

```bash
sudo apt install pipx
pipx ensurepath
```

### Windows Requirements

If you are using Windows, GTK needs to be installed:
[GTK for Windows Runtime Environment Installer](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases/download/2022-01-04/gtk3-runtime-3.24.31-2022-01-04-ts-win64.exe)

- Choose Install GTK+ libraries
- Tick to setup path (otherwise add the install DLL folder manually)
- Choose your installation location
- Complete the installation

### Optional Dependencies

- For SVG to PDF conversion, [CairoSVG](https://cairosvg.org/) is used by default. If
  you need [Inkscape](https://inkscape.org/) instead, install it:

  ```bash
  sudo apt install inkscape
  ```

- For PDF compression, install [Ghostscript](https://www.ghostscript.com/):

  ```bash
  sudo apt install ghostscript
  ```

- If your templates embed particular fonts, they need to be installed. For example for
  [Roboto fonts](https://fonts.google.com/specimen/Roboto):
  ```bash
  sudo apt install fonts-roboto
  ```

## Quickstart: Create templated PDF from an SVG

The fastest way to get started is with the `--create-from` option:

1. Design your document in an SVG editor or convert to SVG.
2. Run pdfbaker with `--create-from` to scaffold a new project and generate your first
   PDF:

   ```bash
   pdfbaker --create-from mydesign.svg myproject/myproject.yaml
   ```

   This will create a directory structure like:

   ```bash
   myproject
   ├── myproject.yaml
   └── mydesign
       ├── config.yaml
       ├── pages
       │   └── main.yaml
       └── templates
           └── main.svg.j2
   ```

   and produce your PDF in `myproject/dist/mydesign/mydesign.pdf`.

3. Edit the template and YAML files to customize your content and variables. This
   directory structure is just a starting point. Add more documents and customize as
   needed.

4. For future builds, just run:

   ```bash
   pdfbaker myproject/myproject.yaml
   ```

   to regenerate your PDFs.

## Documentation

- [Overview](https://github.com/pythonnz/pdfbaker/blob/main/docs/overview.md) - Start
  here
- [Usage](https://github.com/pythonnz/pdfbaker/blob/main/docs/usage.md) - From the CLI
  or as a library
- [Configuration Reference](https://github.com/pythonnz/pdfbaker/blob/main/docs/configuration.md) -
  All available settings
- [Document Variants](https://github.com/pythonnz/pdfbaker/blob/main/docs/variants.md) -
  Create multiple versions of the same document
- [Custom Processing](https://github.com/pythonnz/pdfbaker/blob/main/docs/custom_processing.md) -
  Provide page content from anywhere

## Examples

For working examples, see the
[examples](https://github.com/pythonnz/pdfbaker/tree/main/examples) directory:

- [minimal](https://github.com/pythonnz/pdfbaker/tree/main/examples/minimal) - Basic
  usage
- [regular](https://github.com/pythonnz/pdfbaker/tree/main/examples/regular) - Standard
  features
- [variants](https://github.com/pythonnz/pdfbaker/tree/main/examples/variants) -
  Document variants
- [custom_locations](https://github.com/pythonnz/pdfbaker/tree/main/examples/custom_locations) -
  Custom file/directory locations
- [custom_processing](https://github.com/pythonnz/pdfbaker/tree/main/examples/custom_processing) -
  Custom processing with Python

Create all PDFs with:

```bash
pdfbaker examples/examples.yaml
```

## Development

All source code is [on GitHub](https://github.com/pythonnz/pdfbaker).

This project uses [uv](https://github.com/astral-sh/uv) for dependency management. The
`uv.lock` file ensures reproducible builds.

Create and activate the virtual environment:

```bash
uv venv
source .venv/bin/activate
```

Install development dependencies:

```bash
uv sync --dev
```

### Tests

Run tests:

```bash
pytest
```

View test coverage:

```bash
pytest --cov=pdfbaker --cov-report=term-missing
```

### Pre-commit hook

If you want to commit changes, install [pre-commit](https://pre-commit.com) (maybe
[using uv](https://adamj.eu/tech/2025/05/07/pre-commit-install-uv/)) and run

```bash
pre-commit install
```

This ensures the same checks run locally as in GitHub CI.
