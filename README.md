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

## Quickstart

### Installation

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

### Basic Usage

1. Create your document design in an SVG editor
2. Replace text with variables using Jinja2 (e.g., `{{ title }}`)
3. Configure your content in YAML
4. Generate PDFs with:

```bash
pdfbaker bake <config_file>
```

This will produce your PDF files in a `dist/` directory where your configuration file
lives. It will also create a `build/` directory with intermediate files, which is only
kept if you specify `--keep-build-files` (or `--debug`).

## Examples

For working examples, see the [examples](examples) directory:

- [minimal](examples/minimal) - Basic usage
- [regular](examples/regular) - Standard features
- [variants](examples/variants) - Document variants
- [custom_locations](examples/custom_locations) - Custom file/directory locations
- [custom_processing](examples/custom_processing) - Custom processing with Python

Create all PDFs with:

```bash
pdfbaker bake examples/examples.yaml
```

## Documentation

- [Overview](docs/overview.md) - Start here
- [Configuration Reference](docs/configuration.md) - All available settings
- [Document Variants](docs/variants.md) - Create multiple versions of the same document
- [Custom Processing](docs/custom_processing.md) - Provide page content from anywhere

( [on GitHub](https://github.com/pythonnz/pdfbaker/tree/main/docs) )

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

If you want to commit changes, install [pre-commit](https://pre-commit.com) and run

```bash
pre-commit install
```

This ensures the same checks run locally as in GitHub CI.
