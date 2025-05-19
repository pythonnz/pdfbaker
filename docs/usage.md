# Usage - CLI or Library

How to use **pdfbaker** both from the command line and as a Python library.

---

## Command-Line Interface

```bash
$ pdfbaker --help
Usage: pdfbaker [OPTIONS] CONFIG_FILE [DOCUMENT_NAMES]...

  Generate PDF documents from YAML-configured SVG templates.

  Specify one or more document names to only process those.

Options:
  --version               Show the version and exit.
  -q, --quiet             Show errors only.
  -v, --verbose           Show debug information.
  -t, --trace             Show trace information (maximum details).
  --keep-build            Keep rendered SVGs and single-page PDFs.
  --debug                 Debug mode (implies --verbose and --keep-build).
  --fail-if-exists        Abort if a target PDF already exists.
  --dry-run               Do not write any files.
  --create-from SVG_FILE  Scaffold CONFIG_FILE and supporting files for your
                          existing SVG.
  --help                  Show this message and exit.
```

### Logging verbosity

Use `--quiet` if you only want to see errors, `--verbose` to see the details of what's
getting done, and `--trace` to even see parsed configurations and templates - helpful if
the end result doesn't look right.

### Debugging

If you run into errors or the output doesn't look right, increase log verbosity to see
what's happening and keep intermediary files so you can see how individual page
templates rendered.

Use `--keep-build` to keep the rendered SVGs and PDFs of each page, `--debug` as a
shortcut for "`--verbose` and `--keep-build`".

### Create config from existing SVG

Quickstart! Pass an existing SVG file to `--create-from` and the specified configuration
file and supporting project structure will be created and then processed.

If the path to the (new) config file contains directories that don't exist yet, they
will be created.

For example,

```bash
pdfbaker --create-from poster.svg kiwipycon/kiwipycon.yaml
```

will create a directory `kiwipycon` with a document `poster` that uses a copy of
`poster.svg` as its template:

```bash
kiwipycon
├── kiwipycon.yaml
└── poster
    ├── config.yaml
    ├── pages
    │   └── main.yaml
    └── templates
        └── main.svg.j2
```

After this scaffolding, your new document configuration will be processed immediately,
so you'll get a PDF document right away:

```bash
kiwipycon
├── dist
│   └── poster
│       └── poster.pdf
├── kiwipycon.yaml
└── poster
    └── ...
```

Next, edit the template and the YAML configuration to replace static content with
variables and set their values. See the [Configuration Reference](configuration.md) for
details.

### Miscellaneous

Use `--dry-run` to parse and process - and therefore validate - your configuration but
not actually write any files. If used in conjunction with `--create-from` this will show
the files that _would_ be created (and will not attempt to process them).

Use `--fail-if-exists` to abort if a target PDF already exists in the "dist" output
folder. This may help you avoid race conditions in automated environments.

Use `--version` to show the installed version of pdfbaker and exit, `--help` to show the
above help text and exit.

---

## Python Library

You can use pdfbaker as a Python library by importing the `Baker` class and configuring
it with `BakerOptions`.

### Example

```python
from pathlib import Path
from pdfbaker.baker import Baker, BakerOptions

options = BakerOptions(
    # quiet=False,
    # verbose=False,
    # trace=False,
    # keep_build=True,
    # fail_if_exists=False,
    # dry_run=False,
    # create_from=None,
)

baker = Baker(Path("kiwipycon/kiwipycon.yaml"), options=options)
baker.bake()
```
