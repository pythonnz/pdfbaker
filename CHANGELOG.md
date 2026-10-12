# CHANGELOG


## v1.0.1 (2026-10-12)

### Bug Fixes

- Pin semantic-release changelog mode to init
  ([`dfafc0b`](https://github.com/pythonnz/pdfbaker/commit/dfafc0bc6c69c230fa247a7d98f7c9fe33ff61b5))

PSR v10 (used by the release action) defaults changelog.mode to update, which no-ops without a
  version-list insertion flag. Pin it to init to restore the v9 full-regeneration behaviour so the
  changelog is rebuilt on every release (and backfills the missing 1.0.0 entry).


## v1.0.0 (2026-10-12)

### Bug Fixes

- Gate PyPI publish on tests and stop re-running on RELEASE commits
  ([`57855a4`](https://github.com/pythonnz/pdfbaker/commit/57855a4f5f38b3510db9ba1d78adaad5611b050a))

- split publishing into a separate job gated on the release action's structured 'released' output
  instead of grepping log text - skip every job on 'RELEASE:' commits to end the re-trigger waste -
  scope OIDC trusted publishing to the 'pypi' environment - drop the git reset --hard checkout hack

### Chores

- **deps**: Bump actions/cache from 5 to 6 ([#111](https://github.com/pythonnz/pdfbaker/pull/111),
  [`f030120`](https://github.com/pythonnz/pdfbaker/commit/f03012095c84fe7c0cbbeeda28841ace7aec57a3))

Bumps [actions/cache](https://github.com/actions/cache) from 5 to 6. - [Release
  notes](https://github.com/actions/cache/releases) -
  [Changelog](https://github.com/actions/cache/blob/main/RELEASES.md) -
  [Commits](https://github.com/actions/cache/compare/v5...v6)

--- updated-dependencies: - dependency-name: actions/cache dependency-version: '6'

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump actions/checkout from 5.0.1 to 6.0.2
  ([#78](https://github.com/pythonnz/pdfbaker/pull/78),
  [`d00c611`](https://github.com/pythonnz/pdfbaker/commit/d00c6118e211c48564eb86f7ee688e6e79151f99))

Bumps [actions/checkout](https://github.com/actions/checkout) from 5.0.1 to 6.0.2. - [Release
  notes](https://github.com/actions/checkout/releases) -
  [Commits](https://github.com/actions/checkout/compare/v5.0.1...v6.0.2)

--- updated-dependencies: - dependency-name: actions/checkout dependency-version: 6.0.2

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump actions/checkout from 6.0.2 to 6.0.3
  ([#105](https://github.com/pythonnz/pdfbaker/pull/105),
  [`af4c7af`](https://github.com/pythonnz/pdfbaker/commit/af4c7afca5f3c3b712ffcf440ae00f2c04379a6e))

Bumps [actions/checkout](https://github.com/actions/checkout) from 6.0.2 to 6.0.3. - [Release
  notes](https://github.com/actions/checkout/releases) -
  [Commits](https://github.com/actions/checkout/compare/v6.0.2...v6.0.3)

--- updated-dependencies: - dependency-name: actions/checkout dependency-version: 6.0.3

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump actions/checkout from 6.0.3 to 7.0.0
  ([#110](https://github.com/pythonnz/pdfbaker/pull/110),
  [`ad52664`](https://github.com/pythonnz/pdfbaker/commit/ad52664d83c8eb210ce21cd9146509191133eb99))

Bumps [actions/checkout](https://github.com/actions/checkout) from 6.0.3 to 7.0.0. - [Release
  notes](https://github.com/actions/checkout/releases) -
  [Commits](https://github.com/actions/checkout/compare/v6.0.3...v7)

--- updated-dependencies: - dependency-name: actions/checkout dependency-version: 7.0.0

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump actions/checkout from 7.0.0 to 7.0.1
  ([#117](https://github.com/pythonnz/pdfbaker/pull/117),
  [`a64541e`](https://github.com/pythonnz/pdfbaker/commit/a64541ebf0b0cee1c80f9b5bd6da3017a7e1e23f))

Bumps [actions/checkout](https://github.com/actions/checkout) from 7.0.0 to 7.0.1. - [Release
  notes](https://github.com/actions/checkout/releases) -
  [Commits](https://github.com/actions/checkout/compare/v7...v7.0.1)

--- updated-dependencies: - dependency-name: actions/checkout dependency-version: 7.0.1

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump actions/setup-python from 6 to 7
  ([#114](https://github.com/pythonnz/pdfbaker/pull/114),
  [`4860844`](https://github.com/pythonnz/pdfbaker/commit/486084424e983f4d6addbd8ef07321f4ff5fe321))

Bumps [actions/setup-python](https://github.com/actions/setup-python) from 6 to 7. - [Release
  notes](https://github.com/actions/setup-python/releases) -
  [Commits](https://github.com/actions/setup-python/compare/v6...v7)

--- updated-dependencies: - dependency-name: actions/setup-python dependency-version: '7'

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump actions/upload-artifact from 6.0.0 to 7.0.0
  ([#79](https://github.com/pythonnz/pdfbaker/pull/79),
  [`f11ffeb`](https://github.com/pythonnz/pdfbaker/commit/f11ffeb10adb84d0d992d62a3e782d5fa5ae9be6))

Bumps [actions/upload-artifact](https://github.com/actions/upload-artifact) from 6.0.0 to 7.0.0. -
  [Release notes](https://github.com/actions/upload-artifact/releases) -
  [Commits](https://github.com/actions/upload-artifact/compare/b7c566a772e6b6bfb58ed0dc250532a479d7789f...bbbca2ddaa5d8feaa63e36b76fdaad77386f024f)

--- updated-dependencies: - dependency-name: actions/upload-artifact dependency-version: 7.0.0

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump actions/upload-artifact from 7.0.0 to 7.0.1
  ([#89](https://github.com/pythonnz/pdfbaker/pull/89),
  [`014e9c2`](https://github.com/pythonnz/pdfbaker/commit/014e9c2ace6304550702121c1b3530b1c0ae074e))

Bumps [actions/upload-artifact](https://github.com/actions/upload-artifact) from 7.0.0 to 7.0.1. -
  [Release notes](https://github.com/actions/upload-artifact/releases) -
  [Commits](https://github.com/actions/upload-artifact/compare/bbbca2ddaa5d8feaa63e36b76fdaad77386f024f...043fb46d1a93c77aae656e7c1c64a875d1fc6a0a)

--- updated-dependencies: - dependency-name: actions/upload-artifact dependency-version: 7.0.1

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump cairosvg from 2.8.2 to 2.9.0 ([#82](https://github.com/pythonnz/pdfbaker/pull/82),
  [`e769635`](https://github.com/pythonnz/pdfbaker/commit/e7696356ee7ef868b365d23b18c36d03abf16148))

Bumps [cairosvg](https://github.com/Kozea/CairoSVG) from 2.8.2 to 2.9.0. - [Release
  notes](https://github.com/Kozea/CairoSVG/releases) -
  [Changelog](https://github.com/Kozea/CairoSVG/blob/main/NEWS.rst) -
  [Commits](https://github.com/Kozea/CairoSVG/compare/2.8.2...2.9.0)

--- updated-dependencies: - dependency-name: cairosvg dependency-version: 2.9.0

dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump cairosvg from 2.9.0 to 2.9.1
  ([#129](https://github.com/pythonnz/pdfbaker/pull/129),
  [`74491aa`](https://github.com/pythonnz/pdfbaker/commit/74491aa5e582bc1fcbe97049584486a165600b51))

Bumps [cairosvg](https://github.com/Kozea/CairoSVG) from 2.9.0 to 2.9.1. - [Release
  notes](https://github.com/Kozea/CairoSVG/releases) -
  [Changelog](https://github.com/Kozea/CairoSVG/blob/main/NEWS.rst) -
  [Commits](https://github.com/Kozea/CairoSVG/compare/2.9.0...2.9.1)

--- updated-dependencies: - dependency-name: cairosvg dependency-version: 2.9.1

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump codecov/codecov-action from 5 to 6
  ([#87](https://github.com/pythonnz/pdfbaker/pull/87),
  [`68f57f6`](https://github.com/pythonnz/pdfbaker/commit/68f57f6044b439daab2bcdb1460ae3c092e41835))

Bumps [codecov/codecov-action](https://github.com/codecov/codecov-action) from 5 to 6. - [Release
  notes](https://github.com/codecov/codecov-action/releases) -
  [Changelog](https://github.com/codecov/codecov-action/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/codecov/codecov-action/compare/v5...v6)

--- updated-dependencies: - dependency-name: codecov/codecov-action dependency-version: '6'

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump codecov/codecov-action from 6 to 7
  ([#104](https://github.com/pythonnz/pdfbaker/pull/104),
  [`e3de866`](https://github.com/pythonnz/pdfbaker/commit/e3de866f3250de54a50189b785b1c376bf2fe31b))

Bumps [codecov/codecov-action](https://github.com/codecov/codecov-action) from 6 to 7. - [Release
  notes](https://github.com/codecov/codecov-action/releases) -
  [Changelog](https://github.com/codecov/codecov-action/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/codecov/codecov-action/compare/v6...v7)

--- updated-dependencies: - dependency-name: codecov/codecov-action dependency-version: '7'

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump idna in the uv group across 1 directory
  ([#100](https://github.com/pythonnz/pdfbaker/pull/100),
  [`a420678`](https://github.com/pythonnz/pdfbaker/commit/a420678eb4593ed6954d25e72f436f89e967e89c))

Bumps the uv group with 1 update in the / directory: [idna](https://github.com/kjd/idna).

Updates `idna` from 3.10 to 3.15 - [Release notes](https://github.com/kjd/idna/releases) -
  [Changelog](https://github.com/kjd/idna/blob/master/HISTORY.md) -
  [Commits](https://github.com/kjd/idna/compare/v3.10...v3.15)

--- updated-dependencies: - dependency-name: idna dependency-version: '3.15'

dependency-type: indirect

dependency-group: uv ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump ossf/scorecard-action from 2.4.3 to 2.4.4
  ([#116](https://github.com/pythonnz/pdfbaker/pull/116),
  [`d5cf3f1`](https://github.com/pythonnz/pdfbaker/commit/d5cf3f108d3c531d49a03eca64f1e907043f9280))

Bumps [ossf/scorecard-action](https://github.com/ossf/scorecard-action) from 2.4.3 to 2.4.4. -
  [Release notes](https://github.com/ossf/scorecard-action/releases) -
  [Changelog](https://github.com/ossf/scorecard-action/blob/main/RELEASE.md) -
  [Commits](https://github.com/ossf/scorecard-action/compare/4eaacf0543bb3f2c246792bd56e8cdeffafb205a...2d1146689b8cda280b9bc96326124645441f03bc)

--- updated-dependencies: - dependency-name: ossf/scorecard-action dependency-version: 2.4.4

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pillow in the uv group across 1 directory
  ([#115](https://github.com/pythonnz/pdfbaker/pull/115),
  [`f0d043e`](https://github.com/pythonnz/pdfbaker/commit/f0d043edc0b9f77378ea54162ac120dbd1f4a72b))

Bumps the uv group with 1 update in the / directory:
  [pillow](https://github.com/python-pillow/Pillow).

Updates `pillow` from 12.2.0 to 12.3.0 - [Release
  notes](https://github.com/python-pillow/Pillow/releases) -
  [Changelog](https://github.com/python-pillow/Pillow/blob/main/CHANGES.rst) -
  [Commits](https://github.com/python-pillow/Pillow/compare/12.2.0...12.3.0)

--- updated-dependencies: - dependency-name: pillow dependency-version: 12.3.0

dependency-type: indirect

dependency-group: uv ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pillow in the uv group across 1 directory
  ([#90](https://github.com/pythonnz/pdfbaker/pull/90),
  [`5edc9b5`](https://github.com/pythonnz/pdfbaker/commit/5edc9b57831156bb9f829499d589c80dbe287905))

Bumps the uv group with 1 update in the / directory:
  [pillow](https://github.com/python-pillow/Pillow).

Updates `pillow` from 12.1.1 to 12.2.0 - [Release
  notes](https://github.com/python-pillow/Pillow/releases) -
  [Changelog](https://github.com/python-pillow/Pillow/blob/main/CHANGES.rst) -
  [Commits](https://github.com/python-pillow/Pillow/compare/12.1.1...12.2.0)

--- updated-dependencies: - dependency-name: pillow dependency-version: 12.2.0

dependency-type: indirect

dependency-group: uv ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pip in the uv group across 1 directory
  ([#124](https://github.com/pythonnz/pdfbaker/pull/124),
  [`5d1a55e`](https://github.com/pythonnz/pdfbaker/commit/5d1a55e3a67ccd71df6097a623322ae72f12c55a))

Bumps the uv group with 1 update in the / directory: [pip](https://github.com/pypa/pip).

Updates `pip` from 26.1.2 to 26.2 - [Changelog](https://github.com/pypa/pip/blob/main/NEWS.rst) -
  [Commits](https://github.com/pypa/pip/compare/26.1.2...26.2)

--- updated-dependencies: - dependency-name: pip dependency-version: '26.2'

dependency-type: indirect

dependency-group: uv ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pip in the uv group across 1 directory
  ([#96](https://github.com/pythonnz/pdfbaker/pull/96),
  [`1780040`](https://github.com/pythonnz/pdfbaker/commit/1780040930ed4d8dab5f9b76b80fe0cd5edcb379))

Bumps the uv group with 1 update in the / directory: [pip](https://github.com/pypa/pip).

Updates `pip` from 26.0 to 26.1 - [Changelog](https://github.com/pypa/pip/blob/main/NEWS.rst) -
  [Commits](https://github.com/pypa/pip/compare/26.0...26.1)

--- updated-dependencies: - dependency-name: pip dependency-version: '26.1'

dependency-type: indirect

dependency-group: uv ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pydantic from 2.12.5 to 2.13.2
  ([#94](https://github.com/pythonnz/pdfbaker/pull/94),
  [`5469a63`](https://github.com/pythonnz/pdfbaker/commit/5469a6353da5b493e64c8e9e0491060385591d18))

Bumps [pydantic](https://github.com/pydantic/pydantic) from 2.12.5 to 2.13.2. - [Release
  notes](https://github.com/pydantic/pydantic/releases) -
  [Changelog](https://github.com/pydantic/pydantic/blob/v2.13.2/HISTORY.md) -
  [Commits](https://github.com/pydantic/pydantic/compare/v2.12.5...v2.13.2)

--- updated-dependencies: - dependency-name: pydantic dependency-version: 2.13.2

dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pydantic from 2.13.2 to 2.13.3
  ([#95](https://github.com/pythonnz/pdfbaker/pull/95),
  [`5e4c201`](https://github.com/pythonnz/pdfbaker/commit/5e4c2010ba73560e0c068bed6cf0c57ac899ec06))

Bumps [pydantic](https://github.com/pydantic/pydantic) from 2.13.2 to 2.13.3. - [Release
  notes](https://github.com/pydantic/pydantic/releases) -
  [Changelog](https://github.com/pydantic/pydantic/blob/main/HISTORY.md) -
  [Commits](https://github.com/pydantic/pydantic/compare/v2.13.2...v2.13.3)

--- updated-dependencies: - dependency-name: pydantic dependency-version: 2.13.3

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pydantic from 2.13.3 to 2.13.4
  ([#98](https://github.com/pythonnz/pdfbaker/pull/98),
  [`26087cf`](https://github.com/pythonnz/pdfbaker/commit/26087cfdf75f038a5efd71dacf6b471e389cada0))

Bumps [pydantic](https://github.com/pydantic/pydantic) from 2.13.3 to 2.13.4. - [Release
  notes](https://github.com/pydantic/pydantic/releases) -
  [Changelog](https://github.com/pydantic/pydantic/blob/v2.13.4/HISTORY.md) -
  [Commits](https://github.com/pydantic/pydantic/compare/v2.13.3...v2.13.4)

--- updated-dependencies: - dependency-name: pydantic dependency-version: 2.13.4

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pydantic from 2.13.4 to 2.13.5
  ([#126](https://github.com/pythonnz/pdfbaker/pull/126),
  [`6cde413`](https://github.com/pythonnz/pdfbaker/commit/6cde41371b633d8f303975208e44b126a41112e4))

Bumps [pydantic](https://github.com/pydantic/pydantic) from 2.13.4 to 2.13.5. - [Release
  notes](https://github.com/pydantic/pydantic/releases) -
  [Changelog](https://github.com/pydantic/pydantic/blob/v2.13.5/HISTORY.md) -
  [Commits](https://github.com/pydantic/pydantic/compare/v2.13.4...v2.13.5)

--- updated-dependencies: - dependency-name: pydantic dependency-version: 2.13.5

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pygments from 2.20.0 to 2.21.0
  ([#121](https://github.com/pythonnz/pdfbaker/pull/121),
  [`393cee4`](https://github.com/pythonnz/pdfbaker/commit/393cee46e53766c12d8be8e6a60c7ac9be31d70c))

Bumps [pygments](https://github.com/pygments/pygments) from 2.20.0 to 2.21.0. - [Release
  notes](https://github.com/pygments/pygments/releases) -
  [Changelog](https://github.com/pygments/pygments/blob/master/CHANGES) -
  [Commits](https://github.com/pygments/pygments/compare/2.20.0...2.21.0)

--- updated-dependencies: - dependency-name: pygments dependency-version: 2.21.0

dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pypdf from 6.10.2 to 6.11.0 ([#97](https://github.com/pythonnz/pdfbaker/pull/97),
  [`3132648`](https://github.com/pythonnz/pdfbaker/commit/31326489765e88e29d76a8cc2c779f656d91adad))

Bumps [pypdf](https://github.com/py-pdf/pypdf) from 6.10.2 to 6.11.0. - [Release
  notes](https://github.com/py-pdf/pypdf/releases) -
  [Changelog](https://github.com/py-pdf/pypdf/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/py-pdf/pypdf/compare/6.10.2...6.11.0)

--- updated-dependencies: - dependency-name: pypdf dependency-version: 6.11.0

dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pypdf from 6.11.0 to 6.12.2 ([#102](https://github.com/pythonnz/pdfbaker/pull/102),
  [`a4f4646`](https://github.com/pythonnz/pdfbaker/commit/a4f4646074669b99e394e221698a26e8ac6c7d96))

Bumps [pypdf](https://github.com/py-pdf/pypdf) from 6.11.0 to 6.12.2. - [Release
  notes](https://github.com/py-pdf/pypdf/releases) -
  [Changelog](https://github.com/py-pdf/pypdf/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/py-pdf/pypdf/compare/6.11.0...6.12.2)

--- updated-dependencies: - dependency-name: pypdf dependency-version: 6.12.2

dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pypdf from 6.12.2 to 6.13.0 ([#106](https://github.com/pythonnz/pdfbaker/pull/106),
  [`d67be02`](https://github.com/pythonnz/pdfbaker/commit/d67be02fe397316e4e0ee842064cb1aa30573c5e))

Bumps [pypdf](https://github.com/py-pdf/pypdf) from 6.12.2 to 6.13.0. - [Release
  notes](https://github.com/py-pdf/pypdf/releases) -
  [Changelog](https://github.com/py-pdf/pypdf/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/py-pdf/pypdf/compare/6.12.2...6.13.0)

--- updated-dependencies: - dependency-name: pypdf dependency-version: 6.13.0

dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pypdf from 6.13.0 to 6.13.2 ([#107](https://github.com/pythonnz/pdfbaker/pull/107),
  [`27d74e9`](https://github.com/pythonnz/pdfbaker/commit/27d74e9f13a2834afbfff009c5875602a70d8196))

Bumps [pypdf](https://github.com/py-pdf/pypdf) from 6.13.0 to 6.13.2. - [Release
  notes](https://github.com/py-pdf/pypdf/releases) -
  [Changelog](https://github.com/py-pdf/pypdf/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/py-pdf/pypdf/compare/6.13.0...6.13.2)

--- updated-dependencies: - dependency-name: pypdf dependency-version: 6.13.2

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pypdf from 6.13.3 to 6.14.2 ([#112](https://github.com/pythonnz/pdfbaker/pull/112),
  [`086f079`](https://github.com/pythonnz/pdfbaker/commit/086f07974cd8a9f376e6de3f0b2bcee065f24592))

Bumps [pypdf](https://github.com/py-pdf/pypdf) from 6.13.3 to 6.14.2. - [Release
  notes](https://github.com/py-pdf/pypdf/releases) -
  [Changelog](https://github.com/py-pdf/pypdf/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/py-pdf/pypdf/compare/6.13.3...6.14.2)

--- updated-dependencies: - dependency-name: pypdf dependency-version: 6.14.2

dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pypdf from 6.15.0 to 6.16.1 ([#122](https://github.com/pythonnz/pdfbaker/pull/122),
  [`d1a22a7`](https://github.com/pythonnz/pdfbaker/commit/d1a22a75daabd3f245dca9e8eeaae1ad0a476ee7))

Bumps [pypdf](https://github.com/py-pdf/pypdf) from 6.15.0 to 6.16.1. - [Release
  notes](https://github.com/py-pdf/pypdf/releases) -
  [Changelog](https://github.com/py-pdf/pypdf/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/py-pdf/pypdf/compare/6.15.0...6.16.1)

--- updated-dependencies: - dependency-name: pypdf dependency-version: 6.16.1

dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pypdf from 6.16.1 to 6.16.2 ([#123](https://github.com/pythonnz/pdfbaker/pull/123),
  [`b0b59eb`](https://github.com/pythonnz/pdfbaker/commit/b0b59eb46fc6e4e46357a4117d96e5cf4e0f0976))

Bumps [pypdf](https://github.com/py-pdf/pypdf) from 6.16.1 to 6.16.2. - [Release
  notes](https://github.com/py-pdf/pypdf/releases) -
  [Changelog](https://github.com/py-pdf/pypdf/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/py-pdf/pypdf/compare/6.16.1...6.16.2)

--- updated-dependencies: - dependency-name: pypdf dependency-version: 6.16.2

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pypdf from 6.7.4 to 6.7.5 ([#80](https://github.com/pythonnz/pdfbaker/pull/80),
  [`483aba7`](https://github.com/pythonnz/pdfbaker/commit/483aba7bd76812cd54141e05ea983501c3119ebf))

Bumps [pypdf](https://github.com/py-pdf/pypdf) from 6.7.4 to 6.7.5. - [Release
  notes](https://github.com/py-pdf/pypdf/releases) -
  [Changelog](https://github.com/py-pdf/pypdf/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/py-pdf/pypdf/compare/6.7.4...6.7.5)

--- updated-dependencies: - dependency-name: pypdf dependency-version: 6.7.5

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pypdf from 6.8.0 to 6.9.0 ([#83](https://github.com/pythonnz/pdfbaker/pull/83),
  [`86e3c08`](https://github.com/pythonnz/pdfbaker/commit/86e3c085d065b9331463b94efd880df258a96398))

Bumps [pypdf](https://github.com/py-pdf/pypdf) from 6.8.0 to 6.9.0. - [Release
  notes](https://github.com/py-pdf/pypdf/releases) -
  [Changelog](https://github.com/py-pdf/pypdf/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/py-pdf/pypdf/compare/6.8.0...6.9.0)

--- updated-dependencies: - dependency-name: pypdf dependency-version: 6.9.0

dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pypdf in the uv group across 1 directory
  ([#119](https://github.com/pythonnz/pdfbaker/pull/119),
  [`32b853d`](https://github.com/pythonnz/pdfbaker/commit/32b853d57af2ed822d93d98cb06fdfbc2e9dd858))

Bumps the uv group with 1 update in the / directory: [pypdf](https://github.com/py-pdf/pypdf).

Updates `pypdf` from 6.14.2 to 6.15.0 - [Release notes](https://github.com/py-pdf/pypdf/releases) -
  [Changelog](https://github.com/py-pdf/pypdf/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/py-pdf/pypdf/compare/6.14.2...6.15.0)

--- updated-dependencies: - dependency-name: pypdf dependency-version: 6.15.0

dependency-type: direct:production

dependency-group: uv ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pypdf in the uv group across 1 directory
  ([#93](https://github.com/pythonnz/pdfbaker/pull/93),
  [`63376de`](https://github.com/pythonnz/pdfbaker/commit/63376de087e85a311f19159de84004360ade7013))

Bumps the uv group with 1 update in the / directory: [pypdf](https://github.com/py-pdf/pypdf).

Updates `pypdf` from 6.10.1 to 6.10.2 - [Release notes](https://github.com/py-pdf/pypdf/releases) -
  [Changelog](https://github.com/py-pdf/pypdf/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/py-pdf/pypdf/compare/6.10.1...6.10.2)

--- updated-dependencies: - dependency-name: pypdf dependency-version: 6.10.2

dependency-type: direct:production

dependency-group: uv ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pypdf in the uv group across 1 directory
  ([#92](https://github.com/pythonnz/pdfbaker/pull/92),
  [`a669ff3`](https://github.com/pythonnz/pdfbaker/commit/a669ff3e492f4727af0557c7ddea4db21e0a9a3d))

Bumps the uv group with 1 update in the / directory: [pypdf](https://github.com/py-pdf/pypdf).

Updates `pypdf` from 6.10.0 to 6.10.1 - [Release notes](https://github.com/py-pdf/pypdf/releases) -
  [Changelog](https://github.com/py-pdf/pypdf/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/py-pdf/pypdf/compare/6.10.0...6.10.1)

--- updated-dependencies: - dependency-name: pypdf dependency-version: 6.10.1

dependency-type: direct:production

dependency-group: uv ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pypdf in the uv group across 1 directory
  ([#88](https://github.com/pythonnz/pdfbaker/pull/88),
  [`cf180f2`](https://github.com/pythonnz/pdfbaker/commit/cf180f2879999fe6af032362a8617e417bbe2ec5))

Bumps the uv group with 1 update in the / directory: [pypdf](https://github.com/py-pdf/pypdf).

Updates `pypdf` from 6.9.2 to 6.10.0 - [Release notes](https://github.com/py-pdf/pypdf/releases) -
  [Changelog](https://github.com/py-pdf/pypdf/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/py-pdf/pypdf/compare/6.9.2...6.10.0)

--- updated-dependencies: - dependency-name: pypdf dependency-version: 6.10.0

dependency-type: direct:production

dependency-group: uv ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pypdf in the uv group across 1 directory
  ([#85](https://github.com/pythonnz/pdfbaker/pull/85),
  [`846a1d0`](https://github.com/pythonnz/pdfbaker/commit/846a1d009613a5309b40eaa7a2cfd06687fc76ef))

Bumps the uv group with 1 update in the / directory: [pypdf](https://github.com/py-pdf/pypdf).

Updates `pypdf` from 6.9.1 to 6.9.2 - [Release notes](https://github.com/py-pdf/pypdf/releases) -
  [Changelog](https://github.com/py-pdf/pypdf/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/py-pdf/pypdf/compare/6.9.1...6.9.2)

--- updated-dependencies: - dependency-name: pypdf dependency-version: 6.9.2

dependency-type: direct:production

dependency-group: uv ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pypdf in the uv group across 1 directory
  ([#84](https://github.com/pythonnz/pdfbaker/pull/84),
  [`993492a`](https://github.com/pythonnz/pdfbaker/commit/993492a4932e29b593108dc287eea9a804a9ba24))

Bumps the uv group with 1 update in the / directory: [pypdf](https://github.com/py-pdf/pypdf).

Updates `pypdf` from 6.9.0 to 6.9.1 - [Release notes](https://github.com/py-pdf/pypdf/releases) -
  [Changelog](https://github.com/py-pdf/pypdf/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/py-pdf/pypdf/compare/6.9.0...6.9.1)

--- updated-dependencies: - dependency-name: pypdf dependency-version: 6.9.1

dependency-type: direct:production

dependency-group: uv ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pypdf in the uv group across 1 directory
  ([#81](https://github.com/pythonnz/pdfbaker/pull/81),
  [`c7cadc1`](https://github.com/pythonnz/pdfbaker/commit/c7cadc1dfaffb2bd9312dc0baee3e2e9fb4077b2))

Bumps the uv group with 1 update in the / directory: [pypdf](https://github.com/py-pdf/pypdf).

Updates `pypdf` from 6.7.5 to 6.8.0 - [Release notes](https://github.com/py-pdf/pypdf/releases) -
  [Changelog](https://github.com/py-pdf/pypdf/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/py-pdf/pypdf/compare/6.7.5...6.8.0)

--- updated-dependencies: - dependency-name: pypdf dependency-version: 6.8.0

dependency-type: direct:production

dependency-group: uv ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pytest in the uv group across 1 directory
  ([#91](https://github.com/pythonnz/pdfbaker/pull/91),
  [`b76233f`](https://github.com/pythonnz/pdfbaker/commit/b76233f6871a6bf3e733dafb32786258922eafc7))

Bumps the uv group with 1 update in the / directory: [pytest](https://github.com/pytest-dev/pytest).

Updates `pytest` from 8.3.5 to 9.0.3 - [Release
  notes](https://github.com/pytest-dev/pytest/releases) -
  [Changelog](https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pytest-dev/pytest/compare/8.3.5...9.0.3)

--- updated-dependencies: - dependency-name: pytest dependency-version: 9.0.3

dependency-type: indirect

dependency-group: uv ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump python-semantic-release/publish-action
  ([#131](https://github.com/pythonnz/pdfbaker/pull/131),
  [`4a4391b`](https://github.com/pythonnz/pdfbaker/commit/4a4391b3fe4a2b4cf491ef058bb4fb91a1a335f7))

Bumps
  [python-semantic-release/publish-action](https://github.com/python-semantic-release/publish-action)
  from 10.6.2 to 10.7.0. - [Release
  notes](https://github.com/python-semantic-release/publish-action/releases) -
  [Changelog](https://github.com/python-semantic-release/publish-action/blob/main/releaserc.toml) -
  [Commits](https://github.com/python-semantic-release/publish-action/compare/v10.6.2...v10.7.0)

--- updated-dependencies: - dependency-name: python-semantic-release/publish-action
  dependency-version: 10.7.0

dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump python-semantic-release/publish-action
  ([#125](https://github.com/pythonnz/pdfbaker/pull/125),
  [`1720275`](https://github.com/pythonnz/pdfbaker/commit/17202753941df87542497409249676c33b71e18f))

Bumps
  [python-semantic-release/publish-action](https://github.com/python-semantic-release/publish-action)
  from 10.6.1 to 10.6.2. - [Release
  notes](https://github.com/python-semantic-release/publish-action/releases) -
  [Changelog](https://github.com/python-semantic-release/publish-action/blob/main/releaserc.toml) -
  [Commits](https://github.com/python-semantic-release/publish-action/compare/v10.6.1...v10.6.2)

--- updated-dependencies: - dependency-name: python-semantic-release/publish-action
  dependency-version: 10.6.2

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump python-semantic-release/publish-action
  ([#113](https://github.com/pythonnz/pdfbaker/pull/113),
  [`758b581`](https://github.com/pythonnz/pdfbaker/commit/758b58157387eab25eb1fc742e526a8d98199282))

Bumps
  [python-semantic-release/publish-action](https://github.com/python-semantic-release/publish-action)
  from 10.5.3 to 10.6.1. - [Release
  notes](https://github.com/python-semantic-release/publish-action/releases) -
  [Changelog](https://github.com/python-semantic-release/publish-action/blob/main/releaserc.toml) -
  [Commits](https://github.com/python-semantic-release/publish-action/compare/v10.5.3...v10.6.1)

--- updated-dependencies: - dependency-name: python-semantic-release/publish-action
  dependency-version: 10.6.1

dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump requests in the uv group across 1 directory
  ([#86](https://github.com/pythonnz/pdfbaker/pull/86),
  [`52a7156`](https://github.com/pythonnz/pdfbaker/commit/52a7156b21d89b96b53a5d5fa12acce981ba724a))

Bumps the uv group with 1 update in the / directory: [requests](https://github.com/psf/requests).

Updates `requests` from 2.32.5 to 2.33.0 - [Release notes](https://github.com/psf/requests/releases)
  - [Changelog](https://github.com/psf/requests/blob/main/HISTORY.md) -
  [Commits](https://github.com/psf/requests/compare/v2.32.5...v2.33.0)

--- updated-dependencies: - dependency-name: requests dependency-version: 2.33.0

dependency-type: indirect

dependency-group: uv ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump rich-click from 1.9.7 to 1.9.8
  ([#103](https://github.com/pythonnz/pdfbaker/pull/103),
  [`72690dc`](https://github.com/pythonnz/pdfbaker/commit/72690dc0b52fb3a1f18f8e5cf9f52727ab100e07))

Bumps [rich-click](https://github.com/ewels/rich-click) from 1.9.7 to 1.9.8. - [Release
  notes](https://github.com/ewels/rich-click/releases) -
  [Changelog](https://github.com/ewels/rich-click/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/ewels/rich-click/compare/v1.9.7...v1.9.8)

--- updated-dependencies: - dependency-name: rich-click dependency-version: 1.9.8

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump rich-click from 1.9.8 to 1.9.9
  ([#127](https://github.com/pythonnz/pdfbaker/pull/127),
  [`0d846f3`](https://github.com/pythonnz/pdfbaker/commit/0d846f3b2e643e6995fec3ee71a54df3b9c06cf7))

Bumps [rich-click](https://github.com/ewels/rich-click) from 1.9.8 to 1.9.9. - [Release
  notes](https://github.com/ewels/rich-click/releases) -
  [Changelog](https://github.com/ewels/rich-click/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/ewels/rich-click/compare/v1.9.8...v1.9.9)

--- updated-dependencies: - dependency-name: rich-click dependency-version: 1.9.9

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump the uv group across 1 directory with 2 updates
  ([#118](https://github.com/pythonnz/pdfbaker/pull/118),
  [`6ad2f6f`](https://github.com/pythonnz/pdfbaker/commit/6ad2f6fe7815d18ef3bacee69371814625a2e63f))

Bumps the uv group with 2 updates in the / directory:
  [gitpython](https://github.com/gitpython-developers/GitPython) and
  [setuptools](https://github.com/pypa/setuptools).

Updates `gitpython` from 3.1.50 to 3.1.58 - [Release
  notes](https://github.com/gitpython-developers/GitPython/releases) -
  [Changelog](https://github.com/gitpython-developers/GitPython/blob/main/CHANGES) -
  [Commits](https://github.com/gitpython-developers/GitPython/compare/3.1.50...3.1.58)

Updates `setuptools` from 80.0.0 to 83.0.0 - [Release
  notes](https://github.com/pypa/setuptools/releases) -
  [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst) -
  [Commits](https://github.com/pypa/setuptools/compare/v80.0.0...v83.0.0)

--- updated-dependencies: - dependency-name: gitpython dependency-version: 3.1.58

dependency-type: indirect

dependency-group: uv

- dependency-name: setuptools dependency-version: 83.0.0

dependency-group: uv ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump the uv group across 1 directory with 2 updates
  ([#109](https://github.com/pythonnz/pdfbaker/pull/109),
  [`ca43446`](https://github.com/pythonnz/pdfbaker/commit/ca434465e090be13fa22c98e3a1deedd1b1ed576))

Bumps the uv group with 2 updates in the / directory: [pypdf](https://github.com/py-pdf/pypdf) and
  [msgpack](https://github.com/msgpack/msgpack-python).

Updates `pypdf` from 6.13.2 to 6.13.3 - [Release notes](https://github.com/py-pdf/pypdf/releases) -
  [Changelog](https://github.com/py-pdf/pypdf/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/py-pdf/pypdf/compare/6.13.2...6.13.3)

Updates `msgpack` from 1.1.0 to 1.2.1 - [Release
  notes](https://github.com/msgpack/msgpack-python/releases) -
  [Changelog](https://github.com/msgpack/msgpack-python/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/msgpack/msgpack-python/compare/v1.1.0...v1.2.1)

--- updated-dependencies: - dependency-name: pypdf dependency-version: 6.13.3

dependency-type: direct:production

dependency-group: uv

- dependency-name: msgpack dependency-version: 1.2.1

dependency-type: indirect

dependency-group: uv ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump urllib3 in the uv group across 1 directory
  ([#99](https://github.com/pythonnz/pdfbaker/pull/99),
  [`da262a5`](https://github.com/pythonnz/pdfbaker/commit/da262a51133f158285fde89eb1b3fac139600e4a))

Bumps the uv group with 1 update in the / directory: [urllib3](https://github.com/urllib3/urllib3).

Updates `urllib3` from 2.6.3 to 2.7.0 - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst) -
  [Commits](https://github.com/urllib3/urllib3/compare/2.6.3...2.7.0)

--- updated-dependencies: - dependency-name: urllib3 dependency-version: 2.7.0

dependency-type: indirect

dependency-group: uv ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Fix CVE in gitpython by upgrading to >=3.1.50
  ([`fe5d0f9`](https://github.com/pythonnz/pdfbaker/commit/fe5d0f99a51206e1a413bfa0459cfe891fab7a6e))

- **deps**: Fix CVE in pygments by upgrading to >=2.20.0
  ([`743ad4b`](https://github.com/pythonnz/pdfbaker/commit/743ad4b9d0e247247cbe63e5640c2144e0a24452))

Bump transitive dependency to resolve GHSA-5239-wwwm-4pmq.

- **deps**: Update uv.lock to fix CVEs in gitpython (>=3.1.50) and pip (>=26.1.2)
  ([`371554f`](https://github.com/pythonnz/pdfbaker/commit/371554f631d26776893b0cb6c0798f043ed58a89))


## v0.11.4 (2026-03-01)

### Bug Fixes

- Security updates to dependencies
  ([`6833db1`](https://github.com/pythonnz/pdfbaker/commit/6833db165667a328a67a5601755940537da7eff3))

### Chores

- **deps**: Bump actions/cache from 4 to 5 ([#59](https://github.com/pythonnz/pdfbaker/pull/59),
  [`cc6c5ae`](https://github.com/pythonnz/pdfbaker/commit/cc6c5ae1340737507946fba601d9404c5f2890d4))

Bumps [actions/cache](https://github.com/actions/cache) from 4 to 5. - [Release
  notes](https://github.com/actions/cache/releases) -
  [Changelog](https://github.com/actions/cache/blob/main/RELEASES.md) -
  [Commits](https://github.com/actions/cache/compare/v4...v5)

--- updated-dependencies: - dependency-name: actions/cache dependency-version: '5'

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump actions/checkout from 5 to 6 ([#56](https://github.com/pythonnz/pdfbaker/pull/56),
  [`f4e57a2`](https://github.com/pythonnz/pdfbaker/commit/f4e57a25684cf58b5329743f8c98f12f2e788b1b))

Bumps [actions/checkout](https://github.com/actions/checkout) from 5 to 6. - [Release
  notes](https://github.com/actions/checkout/releases) -
  [Commits](https://github.com/actions/checkout/compare/v5...v6)

--- updated-dependencies: - dependency-name: actions/checkout dependency-version: '6'

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump actions/setup-python from 5 to 6
  ([#45](https://github.com/pythonnz/pdfbaker/pull/45),
  [`f52513b`](https://github.com/pythonnz/pdfbaker/commit/f52513b67589cd7a261278dc3a7aab8fb13feb38))

Bumps [actions/setup-python](https://github.com/actions/setup-python) from 5 to 6. - [Release
  notes](https://github.com/actions/setup-python/releases) -
  [Commits](https://github.com/actions/setup-python/compare/v5...v6)

--- updated-dependencies: - dependency-name: actions/setup-python dependency-version: '6'

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump actions/upload-artifact from 4.6.2 to 6.0.0
  ([#61](https://github.com/pythonnz/pdfbaker/pull/61),
  [`a443b00`](https://github.com/pythonnz/pdfbaker/commit/a443b00f3d9aefede9f3fddee3cef276cf0ac903))

Bumps [actions/upload-artifact](https://github.com/actions/upload-artifact) from 4.6.2 to 6.0.0. -
  [Release notes](https://github.com/actions/upload-artifact/releases) -
  [Commits](https://github.com/actions/upload-artifact/compare/ea165f8d65b6e75b540449e92b4886f43607fa02...b7c566a772e6b6bfb58ed0dc250532a479d7789f)

--- updated-dependencies: - dependency-name: actions/upload-artifact dependency-version: 6.0.0

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump filelock from 3.18.0 to 3.20.3
  ([#74](https://github.com/pythonnz/pdfbaker/pull/74),
  [`58d40b4`](https://github.com/pythonnz/pdfbaker/commit/58d40b45487f6a47b16b262238d5680e849d69a3))

Bumps [filelock](https://github.com/tox-dev/py-filelock) from 3.18.0 to 3.20.3. - [Release
  notes](https://github.com/tox-dev/py-filelock/releases) -
  [Changelog](https://github.com/tox-dev/filelock/blob/main/docs/changelog.rst) -
  [Commits](https://github.com/tox-dev/py-filelock/compare/3.18.0...3.20.3)

--- updated-dependencies: - dependency-name: filelock dependency-version: 3.20.3

dependency-type: indirect ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump github/codeql-action from 3 to 4
  ([#43](https://github.com/pythonnz/pdfbaker/pull/43),
  [`90104ac`](https://github.com/pythonnz/pdfbaker/commit/90104acd1d0434f5ac98ec678810e3931eef0980))

Bumps [github/codeql-action](https://github.com/github/codeql-action) from 3 to 4. - [Release
  notes](https://github.com/github/codeql-action/releases) -
  [Changelog](https://github.com/github/codeql-action/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/github/codeql-action/compare/v3...v4)

--- updated-dependencies: - dependency-name: github/codeql-action dependency-version: '4'

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pillow from 11.1.0 to 12.1.1 ([#76](https://github.com/pythonnz/pdfbaker/pull/76),
  [`803d4c1`](https://github.com/pythonnz/pdfbaker/commit/803d4c1113b72b9e97b1427e5ee872804180aec6))

Bumps [pillow](https://github.com/python-pillow/Pillow) from 11.1.0 to 12.1.1. - [Release
  notes](https://github.com/python-pillow/Pillow/releases) -
  [Changelog](https://github.com/python-pillow/Pillow/blob/main/CHANGES.rst) -
  [Commits](https://github.com/python-pillow/Pillow/compare/11.1.0...12.1.1)

--- updated-dependencies: - dependency-name: pillow dependency-version: 12.1.1

dependency-type: indirect ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pip from 25.2 to 26.0 ([#73](https://github.com/pythonnz/pdfbaker/pull/73),
  [`f998f60`](https://github.com/pythonnz/pdfbaker/commit/f998f60df500f3c38102f58456c1c485271ec7d6))

Bumps [pip](https://github.com/pypa/pip) from 25.2 to 26.0. -
  [Changelog](https://github.com/pypa/pip/blob/main/NEWS.rst) -
  [Commits](https://github.com/pypa/pip/compare/25.2...26.0)

--- updated-dependencies: - dependency-name: pip dependency-version: '26.0'

dependency-type: indirect ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pydantic from 2.12.3 to 2.12.4
  ([#50](https://github.com/pythonnz/pdfbaker/pull/50),
  [`c26e69d`](https://github.com/pythonnz/pdfbaker/commit/c26e69d1d98f4380c061637a7f52a8c356fd1485))

Bumps [pydantic](https://github.com/pydantic/pydantic) from 2.12.3 to 2.12.4. - [Release
  notes](https://github.com/pydantic/pydantic/releases) -
  [Changelog](https://github.com/pydantic/pydantic/blob/v2.12.4/HISTORY.md) -
  [Commits](https://github.com/pydantic/pydantic/compare/v2.12.3...v2.12.4)

--- updated-dependencies: - dependency-name: pydantic dependency-version: 2.12.4

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pydantic from 2.12.4 to 2.12.5
  ([#57](https://github.com/pythonnz/pdfbaker/pull/57),
  [`6ab264e`](https://github.com/pythonnz/pdfbaker/commit/6ab264e3ac3fb94a15c5210b1cdd3d8cde4655c6))

Bumps [pydantic](https://github.com/pydantic/pydantic) from 2.12.4 to 2.12.5. - [Release
  notes](https://github.com/pydantic/pydantic/releases) -
  [Changelog](https://github.com/pydantic/pydantic/blob/main/HISTORY.md) -
  [Commits](https://github.com/pydantic/pydantic/compare/v2.12.4...v2.12.5)

--- updated-dependencies: - dependency-name: pydantic dependency-version: 2.12.5

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pypdf from 6.1.1 to 6.1.2 ([#44](https://github.com/pythonnz/pdfbaker/pull/44),
  [`e70baaa`](https://github.com/pythonnz/pdfbaker/commit/e70baaa20f326cba4ba5b987334ba0ffbed98f32))

Bumps [pypdf](https://github.com/py-pdf/pypdf) from 6.1.1 to 6.1.2. - [Release
  notes](https://github.com/py-pdf/pypdf/releases) -
  [Changelog](https://github.com/py-pdf/pypdf/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/py-pdf/pypdf/compare/6.1.1...6.1.2)

--- updated-dependencies: - dependency-name: pypdf dependency-version: 6.1.2

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pypdf from 6.1.2 to 6.1.3 ([#46](https://github.com/pythonnz/pdfbaker/pull/46),
  [`d1898ea`](https://github.com/pythonnz/pdfbaker/commit/d1898eaa8bdd32a25f2f6f45718f51c619d0639a))

Bumps [pypdf](https://github.com/py-pdf/pypdf) from 6.1.2 to 6.1.3. - [Release
  notes](https://github.com/py-pdf/pypdf/releases) -
  [Changelog](https://github.com/py-pdf/pypdf/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/py-pdf/pypdf/compare/6.1.2...6.1.3)

--- updated-dependencies: - dependency-name: pypdf dependency-version: 6.1.3

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pypdf from 6.1.3 to 6.2.0 ([#51](https://github.com/pythonnz/pdfbaker/pull/51),
  [`c73a958`](https://github.com/pythonnz/pdfbaker/commit/c73a9584a0a915d8d449f26404ad87ff44083778))

Bumps [pypdf](https://github.com/py-pdf/pypdf) from 6.1.3 to 6.2.0. - [Release
  notes](https://github.com/py-pdf/pypdf/releases) -
  [Changelog](https://github.com/py-pdf/pypdf/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/py-pdf/pypdf/compare/6.1.3...6.2.0)

--- updated-dependencies: - dependency-name: pypdf dependency-version: 6.2.0

dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pypdf from 6.2.0 to 6.7.0 ([#72](https://github.com/pythonnz/pdfbaker/pull/72),
  [`17a0c1e`](https://github.com/pythonnz/pdfbaker/commit/17a0c1e137f9bb2cd970d1e6ab49514dc0d96451))

Bumps [pypdf](https://github.com/py-pdf/pypdf) from 6.2.0 to 6.7.0. - [Release
  notes](https://github.com/py-pdf/pypdf/releases) -
  [Changelog](https://github.com/py-pdf/pypdf/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/py-pdf/pypdf/compare/6.2.0...6.7.0)

--- updated-dependencies: - dependency-name: pypdf dependency-version: 6.7.0

dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pypdf from 6.2.0 to 6.7.4 ([#75](https://github.com/pythonnz/pdfbaker/pull/75),
  [`2c90a73`](https://github.com/pythonnz/pdfbaker/commit/2c90a739ccf7ed738d5873749e18a9d188621271))

Bumps [pypdf](https://github.com/py-pdf/pypdf) from 6.2.0 to 6.7.4. - [Release
  notes](https://github.com/py-pdf/pypdf/releases) -
  [Changelog](https://github.com/py-pdf/pypdf/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/py-pdf/pypdf/compare/6.2.0...6.7.4)

--- updated-dependencies: - dependency-name: pypdf dependency-version: 6.7.4

dependency-type: direct:production ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump python-semantic-release/publish-action
  ([#60](https://github.com/pythonnz/pdfbaker/pull/60),
  [`d1661a8`](https://github.com/pythonnz/pdfbaker/commit/d1661a8ae89daf883181c253925b9f7665f46dc5))

Bumps
  [python-semantic-release/publish-action](https://github.com/python-semantic-release/publish-action)
  from 10.5.1 to 10.5.3. - [Release
  notes](https://github.com/python-semantic-release/publish-action/releases) -
  [Changelog](https://github.com/python-semantic-release/publish-action/blob/main/releaserc.toml) -
  [Commits](https://github.com/python-semantic-release/publish-action/compare/v10.5.1...v10.5.3)

--- updated-dependencies: - dependency-name: python-semantic-release/publish-action
  dependency-version: 10.5.3

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump python-semantic-release/publish-action
  ([#52](https://github.com/pythonnz/pdfbaker/pull/52),
  [`4c1b000`](https://github.com/pythonnz/pdfbaker/commit/4c1b0000a708c5122e963a041981615fbfaefe57))

Bumps
  [python-semantic-release/publish-action](https://github.com/python-semantic-release/publish-action)
  from 10.4.1 to 10.5.1. - [Release
  notes](https://github.com/python-semantic-release/publish-action/releases) -
  [Changelog](https://github.com/python-semantic-release/publish-action/blob/main/releaserc.toml) -
  [Commits](https://github.com/python-semantic-release/publish-action/compare/v10.4.1...v10.5.1)

--- updated-dependencies: - dependency-name: python-semantic-release/publish-action
  dependency-version: 10.5.1

dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump rich-click from 1.9.3 to 1.9.7
  ([#70](https://github.com/pythonnz/pdfbaker/pull/70),
  [`6318960`](https://github.com/pythonnz/pdfbaker/commit/6318960f558592229a6c8b55fcf0afc829262b09))

Bumps [rich-click](https://github.com/ewels/rich-click) from 1.9.3 to 1.9.7. - [Release
  notes](https://github.com/ewels/rich-click/releases) -
  [Changelog](https://github.com/ewels/rich-click/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/ewels/rich-click/compare/v1.9.3...v1.9.7)

--- updated-dependencies: - dependency-name: rich-click dependency-version: 1.9.7

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump ruamel-yaml from 0.18.15 to 0.19.1
  ([#66](https://github.com/pythonnz/pdfbaker/pull/66),
  [`7c90d89`](https://github.com/pythonnz/pdfbaker/commit/7c90d89e89d7c21363378664d79de855687d9768))

Bumps ruamel-yaml from 0.18.15 to 0.19.1.

--- updated-dependencies: - dependency-name: ruamel-yaml dependency-version: 0.19.1

dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump urllib3 from 2.5.0 to 2.6.3 ([#77](https://github.com/pythonnz/pdfbaker/pull/77),
  [`c96129c`](https://github.com/pythonnz/pdfbaker/commit/c96129c8a3dba663a9ca87f245d80afaff39cc0f))

Bumps [urllib3](https://github.com/urllib3/urllib3) from 2.5.0 to 2.6.3. - [Release
  notes](https://github.com/urllib3/urllib3/releases) -
  [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst) -
  [Commits](https://github.com/urllib3/urllib3/compare/2.5.0...2.6.3)

--- updated-dependencies: - dependency-name: urllib3 dependency-version: 2.6.3

dependency-type: indirect ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>


## v0.11.3 (2025-10-19)

### Bug Fixes

- Ignore tarfile symlink vulnerability in pip-audit
  ([`01dad6b`](https://github.com/pythonnz/pdfbaker/commit/01dad6ba101f7569770260b08ab4cc457256714c))

https://github.com/advisories/GHSA-4xh5-x5gv-qwph https://github.com/pypa/pip/issues/13607

As we're not affected, this seems to be the most pragmatic approach for this curveball.

### Continuous Integration

- Bump Ubuntu version for pip-audit to use Python 3.12
  ([`0d38b57`](https://github.com/pythonnz/pdfbaker/commit/0d38b57e16eca75824ade45016687a27e00d4c27))

- Update pip
  ([`1dc2ecd`](https://github.com/pythonnz/pdfbaker/commit/1dc2ecdc755d430abf332403921dfbc447685dd7))

The current python action (as bumped by dependabot) seems to still be running pip 25.2 which
  pip-audit flagged for known vulnerability


## v0.11.2 (2025-10-19)

### Bug Fixes

- Update pip/requests/urllib3 to fix known vulnerabilities
  ([`9de1994`](https://github.com/pythonnz/pdfbaker/commit/9de199429d733e2810d3fe9877204b120181c292))

### Chores

- **deps**: Bump actions/checkout from 4 to 5 ([#35](https://github.com/pythonnz/pdfbaker/pull/35),
  [`5f50212`](https://github.com/pythonnz/pdfbaker/commit/5f5021217ca1f98a771158742e8fa59cfd431b6f))

Bumps [actions/checkout](https://github.com/actions/checkout) from 4 to 5. - [Release
  notes](https://github.com/actions/checkout/releases) -
  [Commits](https://github.com/actions/checkout/compare/v4...v5)

--- updated-dependencies: - dependency-name: actions/checkout dependency-version: '5'

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump actions/upload-artifact from 4.6.1 to 4.6.2
  ([#36](https://github.com/pythonnz/pdfbaker/pull/36),
  [`5438dd2`](https://github.com/pythonnz/pdfbaker/commit/5438dd2b983f48fa7671b371687176a2bc2d0963))

Bumps [actions/upload-artifact](https://github.com/actions/upload-artifact) from 4.6.1 to 4.6.2. -
  [Release notes](https://github.com/actions/upload-artifact/releases) -
  [Commits](https://github.com/actions/upload-artifact/compare/4cec3d8aa04e39d1a68397de0c4cd6fb9dce8ec1...ea165f8d65b6e75b540449e92b4886f43607fa02)

--- updated-dependencies: - dependency-name: actions/upload-artifact dependency-version: 4.6.2

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump cairosvg from 2.7.1 to 2.8.2 ([#40](https://github.com/pythonnz/pdfbaker/pull/40),
  [`de27263`](https://github.com/pythonnz/pdfbaker/commit/de27263770b161c09507b5102bdd07ea2155fa0c))

Bumps [cairosvg](https://github.com/Kozea/CairoSVG) from 2.7.1 to 2.8.2. - [Release
  notes](https://github.com/Kozea/CairoSVG/releases) -
  [Changelog](https://github.com/Kozea/CairoSVG/blob/main/NEWS.rst) -
  [Commits](https://github.com/Kozea/CairoSVG/compare/2.7.1...2.8.2)

--- updated-dependencies: - dependency-name: cairosvg dependency-version: 2.8.2

dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump ossf/scorecard-action from 2.4.1 to 2.4.3
  ([#37](https://github.com/pythonnz/pdfbaker/pull/37),
  [`8bea42c`](https://github.com/pythonnz/pdfbaker/commit/8bea42c8e2060a1c82e33d41b6b93e3a1f000835))

Bumps [ossf/scorecard-action](https://github.com/ossf/scorecard-action) from 2.4.1 to 2.4.3. -
  [Release notes](https://github.com/ossf/scorecard-action/releases) -
  [Changelog](https://github.com/ossf/scorecard-action/blob/main/RELEASE.md) -
  [Commits](https://github.com/ossf/scorecard-action/compare/f49aabe0b5af0936a0987cfb85d86b75731b0186...4eaacf0543bb3f2c246792bd56e8cdeffafb205a)

--- updated-dependencies: - dependency-name: ossf/scorecard-action dependency-version: 2.4.3

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pydantic from 2.11.3 to 2.12.3
  ([#41](https://github.com/pythonnz/pdfbaker/pull/41),
  [`88d8b4b`](https://github.com/pythonnz/pdfbaker/commit/88d8b4b8a184789b422628bb488958b7b9007b31))

Bumps [pydantic](https://github.com/pydantic/pydantic) from 2.11.3 to 2.12.3. - [Release
  notes](https://github.com/pydantic/pydantic/releases) -
  [Changelog](https://github.com/pydantic/pydantic/blob/main/HISTORY.md) -
  [Commits](https://github.com/pydantic/pydantic/compare/v2.11.3...v2.12.3)

--- updated-dependencies: - dependency-name: pydantic dependency-version: 2.12.3

dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pypdf from 5.4.0 to 6.1.1 ([#39](https://github.com/pythonnz/pdfbaker/pull/39),
  [`a3bfa23`](https://github.com/pythonnz/pdfbaker/commit/a3bfa23911c6be7c116134c002dbf0ffe4c99e1d))

Bumps [pypdf](https://github.com/py-pdf/pypdf) from 5.4.0 to 6.1.1. - [Release
  notes](https://github.com/py-pdf/pypdf/releases) -
  [Changelog](https://github.com/py-pdf/pypdf/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/py-pdf/pypdf/compare/5.4.0...6.1.1)

--- updated-dependencies: - dependency-name: pypdf dependency-version: 6.1.1

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump python-semantic-release/publish-action
  ([#34](https://github.com/pythonnz/pdfbaker/pull/34),
  [`dfa4e55`](https://github.com/pythonnz/pdfbaker/commit/dfa4e55bb2537c03de25f8024bf2f2c2878e4025))

Bumps
  [python-semantic-release/publish-action](https://github.com/python-semantic-release/publish-action)
  from 9.21.1 to 10.4.1. - [Release
  notes](https://github.com/python-semantic-release/publish-action/releases) -
  [Changelog](https://github.com/python-semantic-release/publish-action/blob/main/releaserc.toml) -
  [Commits](https://github.com/python-semantic-release/publish-action/compare/v9.21.1...v10.4.1)

--- updated-dependencies: - dependency-name: python-semantic-release/publish-action
  dependency-version: 10.4.1

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump rich-click from 1.8.8 to 1.9.3
  ([#38](https://github.com/pythonnz/pdfbaker/pull/38),
  [`0866d03`](https://github.com/pythonnz/pdfbaker/commit/0866d034b5c0c9108bc92257c8a64863342bee58))

Bumps [rich-click](https://github.com/ewels/rich-click) from 1.8.8 to 1.9.3. - [Release
  notes](https://github.com/ewels/rich-click/releases) -
  [Changelog](https://github.com/ewels/rich-click/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/ewels/rich-click/compare/v1.8.8...v1.9.3)

--- updated-dependencies: - dependency-name: rich-click dependency-version: 1.9.3

dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump ruamel-yaml from 0.18.10 to 0.18.15
  ([#42](https://github.com/pythonnz/pdfbaker/pull/42),
  [`46ee10d`](https://github.com/pythonnz/pdfbaker/commit/46ee10dc77d87078315755904458f6c7d88ad0c6))

Bumps ruamel-yaml from 0.18.10 to 0.18.15.

--- updated-dependencies: - dependency-name: ruamel-yaml dependency-version: 0.18.15

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>


## v0.11.1 (2025-10-16)

### Bug Fixes

- Remove comma to demo release
  ([`036151b`](https://github.com/pythonnz/pdfbaker/commit/036151bd5fe93b6ff3d96d4c2b56967db5efb899))

This is only for demonstration purposes. Marked as a fix to trigger a release.


## v0.11.0 (2025-05-23)

### Bug Fixes

- Escape XKCD title and alt text
  ([`8432a24`](https://github.com/pythonnz/pdfbaker/commit/8432a24eef9eb365149c9d3dbcff67eda8e12394))

Otherwise the SVG can be become invalid...

``` "Applying renormalization to bullies successfully transformed Pete & Pete's Endless Mike into
  Finite Mike." ``` needs to be escaped to ``` Pete &amp; Pete&#39;s Endless Mike into Finite Mike.
  ```

### Code Style

- Don't show location of build directory in a dry-run
  ([`cd4c675`](https://github.com/pythonnz/pdfbaker/commit/cd4c67529a9f690f272fd44a9c297e5fc8a39341))

It wouldn't have been created...

### Documentation

- Add "Usage" document, adjust README and overview, fix custom locations
  ([`2c390da`](https://github.com/pythonnz/pdfbaker/commit/2c390da73db7da6af718ecd9192bd021d1a81341))

- Fix config file path in library example (same as in CLI example)
  ([`6c3198a`](https://github.com/pythonnz/pdfbaker/commit/6c3198ac2969c54daee96ff839267c8dfc3e608b))

- Improve README
  ([`8a22464`](https://github.com/pythonnz/pdfbaker/commit/8a22464ca07e95e98a8ad4ce9145520a885145a5))

- add what you get from using SVG+YAML - add how quickly you can get started - Move "Documentation"
  to be before "Examples"

### Features

- Improve logging and console UI with rich formatting
  ([`fcf16ed`](https://github.com/pythonnz/pdfbaker/commit/fcf16ed2960fcba1155b8128857e5c9610edb379))

* Use rich and rich-click - colors, panels etc. * Proper syntax highlighting for SVG and YAML * Show
  directory tree after --create-from * Don't repeat identical subprocess log messages, count them


## v0.10.0 (2025-05-18)

### Code Style

- Remove `bake` action
  ([`1aff43f`](https://github.com/pythonnz/pdfbaker/commit/1aff43f06e1cd1400ab7c6c9f4878b8e27f372e8))

This is technically a breaking change but only for invoking.

### Documentation

- Add section on always quoting variables
  ([`7c0d13e`](https://github.com/pythonnz/pdfbaker/commit/7c0d13ef9baa759663a90b7cb4cb7e416e6a1f81))

Just got caught out by that myself :)

- Clarify that Jinja2 extensions to load are strings
  ([`3a921eb`](https://github.com/pythonnz/pdfbaker/commit/3a921eb15399add0b32cba0f2e8f29538106d1ba))

- Link to official Jinja2 extensions
  ([`264cb76`](https://github.com/pythonnz/pdfbaker/commit/264cb765658c71212a7e33ffd9824700edb50b24))

- Update README.md to include windows specific instructions
  ([#33](https://github.com/pythonnz/pdfbaker/pull/33),
  [`ef2d2f6`](https://github.com/pythonnz/pdfbaker/commit/ef2d2f6c296fd64eaf0e3b3aed78fba4b18c81df))

### Features

- Add `--dry-run`, `--fail-if-exists`, build in temp dir
  ([`70f956c`](https://github.com/pythonnz/pdfbaker/commit/70f956c0304636da2a519e5653e4850aab190e1c))

Also prep `--create-from` (coming up)

- Don't fail just warn about undefined Jinja variables
  ([`05cb2c1`](https://github.com/pythonnz/pdfbaker/commit/05cb2c1faed3d000b29124e72840d5bae397a9c9))

Stumbled over this when I used an existing template for --create-from. Maybe introduce a
  --fail-undefined-vars option later.

- Implement `--create-from`
  ([`ec24465`](https://github.com/pythonnz/pdfbaker/commit/ec244658dc0f38f88acdc6d3ab2c23d46e153849))

If used in conjunction with `--dry-run`, don't create any files. Otherwise, also process the new
  configs immediately.

### Testing

- Remove old absolute path test
  ([`f734b22`](https://github.com/pythonnz/pdfbaker/commit/f734b22f2b723555015a4cb1feee006c5ea772f9))

- Remove old absolute path tests
  ([`5553497`](https://github.com/pythonnz/pdfbaker/commit/55534974958075560bd92dc4dfc89bc70057a053))

This needs to work properly on Windows. Test to confirm relative and absolute paths lead to the same
  directories being used (maybe run all tests with both?)


## v0.9.4 (2025-05-11)

### Bug Fixes

- Actually deep-merge configs
  ([`1069a68`](https://github.com/pythonnz/pdfbaker/commit/1069a68121f126ef1ce6e628d738c28ab8903fec))

### Documentation

- Add link to pre-commit installation with uv
  ([`c834d30`](https://github.com/pythonnz/pdfbaker/commit/c834d30accdd23bffaad9443dbf60613d0c90c6d))

- Clarify directories, document/page names, variant config
  ([`c83f5c5`](https://github.com/pythonnz/pdfbaker/commit/c83f5c5eebd96940a68df1d7173c451098d6375f))

- Clarify page `template` setting
  ([`8de9fc8`](https://github.com/pythonnz/pdfbaker/commit/8de9fc886f916a70008cdf3107d8bbeb4153d2a5))


## v0.9.3 (2025-05-10)

### Bug Fixes

- Improved test suite, tests now also linted
  ([`11e8bb8`](https://github.com/pythonnz/pdfbaker/commit/11e8bb848114362c9c957351070f73ff084a4adc))

Reviewed all tests. Now 73 tests covering 91%.

### Continuous Integration

- Delete Sigstore signing - PyPI already doing that
  ([`1e4c7b6`](https://github.com/pythonnz/pdfbaker/commit/1e4c7b656040a2c4920571c83d0f72b35f87becf))

Only now I noticed the `.publish.attestation` files in the releases...

### Documentation

- Add sigstore badge
  ([`015fc47`](https://github.com/pythonnz/pdfbaker/commit/015fc47b271fb510e7c487805efee9750a4a52b6))


## v0.9.2 (2025-05-09)

### Bug Fixes

- Disable sigstore signing while waiting on PyPI issue
  ([`b850286`](https://github.com/pythonnz/pdfbaker/commit/b85028658f1e6c4ad316b35bfff681b01396142e))

https://github.com/pypa/gh-action-pypi-publish/issues/357


## v0.9.1 (2025-05-09)

### Bug Fixes

- Sign releases with Sigstore
  ([`e6b0f62`](https://github.com/pythonnz/pdfbaker/commit/e6b0f62f7c571c3c0e8b94ac9edb2782d03b51e5))

More of a `ci:` but I want to trigger a release to confirm

### Documentation

- Clarify that a page setting can override main or document
  ([`9b0c40f`](https://github.com/pythonnz/pdfbaker/commit/9b0c40f61235c5666eb02f804b0351038b283ee2))

- Fix default location of documents
  ([`228df2c`](https://github.com/pythonnz/pdfbaker/commit/228df2cea73defe7063d3534a1f2d80488188017))

(same directory as config file, not another subdirectory)

- Fix description - page overrides for page, not document
  ([`b43718a`](https://github.com/pythonnz/pdfbaker/commit/b43718a611f13965c1ed3f76174fc7e059aaa048))

- Improve configuration reference, add section on custom locations
  ([`aeee114`](https://github.com/pythonnz/pdfbaker/commit/aeee114a270eb4e078e89c58f5428fffc72f30b4))


## v0.9.0 (2025-05-09)

### Documentation

- Refactor documentation
  ([`8efced6`](https://github.com/pythonnz/pdfbaker/commit/8efced682753ad5e92c5a66c16766b04e2edd262))

A first stab at making the documentation up-to-date and useful.

### Features

- Up-to-date documentation
  ([`1a6ba58`](https://github.com/pythonnz/pdfbaker/commit/1a6ba58aae914f42438ede8c569d0c0e85f783f3))

Marking this as a feature to trigger a new release.


## v0.8.14 (2025-05-09)

### Bug Fixes

- Remove superfluous theme/color mechanism
  ([`bdf9fbe`](https://github.com/pythonnz/pdfbaker/commit/bdf9fbe3f3602241979ce29a40049126f24b6b29))

This is technically a breaking change but trivial to resolve in configs: No more special implicit
  treatment of "theme" to resolve a "style".

Just use regular variables like ``` style: primary_text_colour: {{ theme.off_black }}

secondary_text_colour: {{ theme.off_white }}

theme: off_black: "#2d2a2b"

off_white: "#f5f5f5" ```

### Code Style

- Show how you can add messages to the processing log
  ([`a2c2b62`](https://github.com/pythonnz/pdfbaker/commit/a2c2b62d0be5c3a9a119c80e0a5a5cb00b81e8ab))

### Continuous Integration

- Don't run pre-commit/tests twice on push to main
  ([`f721c24`](https://github.com/pythonnz/pdfbaker/commit/f721c24fc68e7ebe3f23e1c7fac255d93d4f26e8))

- Keep static `__version__` in `__init__.py`, update upon release
  ([`d240591`](https://github.com/pythonnz/pdfbaker/commit/d240591f374ad055838a0a4381ae2591ca74626e))


## v0.8.13 (2025-05-09)

### Bug Fixes

- -v option for main command
  ([`2d59fde`](https://github.com/pythonnz/pdfbaker/commit/2d59fdeb7153fc650a7999e603dca1176368fa06))

- Preserve exit code of PSR (also run verbose)
  ([`e86df6b`](https://github.com/pythonnz/pdfbaker/commit/e86df6bd44e0ac7047fa1a3f70dab866cfd0b26b))

The exit code of Python Semantic Release was shadowed by the exit code of the assignment of its
  output.


## v0.8.12 (2025-05-08)

### Bug Fixes

- Uv.lock was always a release behind
  ([`5ac00cc`](https://github.com/pythonnz/pdfbaker/commit/5ac00cca59f0931d3a09872d652513fe3bc50797))


## v0.8.11 (2025-05-08)

### Bug Fixes

- Ensure uv.lock gets updated by a release
  ([`6a074c8`](https://github.com/pythonnz/pdfbaker/commit/6a074c8ed270da3186eca196277090e2c4719b96))

### Chores

- Add DocumentNotFoundError to errors.__all__
  ([`02e95e8`](https://github.com/pythonnz/pdfbaker/commit/02e95e8c54d2e93e47f534fbb45a71a843ed5bd9))


## v0.8.10 (2025-05-08)

### Bug Fixes

- Add PSR default templates
  ([`b29b68c`](https://github.com/pythonnz/pdfbaker/commit/b29b68c896d486bdd3f004d25800d9bb63503e64))

It's not clever enough to only pick up custom templates, must copy their templates as a starting
  point for customisation.


## v0.8.9 (2025-05-08)

### Bug Fixes

- Show PSR output (was getting consumed for evaluation)
  ([`4cb4c85`](https://github.com/pythonnz/pdfbaker/commit/4cb4c85dc90cfdb7765443f0d0d4818ae4ed08e3))


## v0.8.8 (2025-05-08)

### Bug Fixes

- Remove version variable for CITATION.cff (now in template)
  ([`ee7bd69`](https://github.com/pythonnz/pdfbaker/commit/ee7bd69126abcc5802570e8270a21715c7cd89a4))

- Use PSR's templating mechanism instead of a script
  ([`2e608f9`](https://github.com/pythonnz/pdfbaker/commit/2e608f9131822e624b47f03cb36351b935990f17))

### Continuous Integration

- Remove unused version
  ([`4b21a43`](https://github.com/pythonnz/pdfbaker/commit/4b21a4376b9df7df2bcf5b9796cd252aff8c0d38))

The tag is already set correctly

### Documentation

- Add CITATION.cff and update its version and date during release
  ([`812b098`](https://github.com/pythonnz/pdfbaker/commit/812b098b24ed29def14d7e219f8b626523aa9f76))


## v0.8.7 (2025-05-08)

### Bug Fixes

- Remove debug logging
  ([`dbf2b88`](https://github.com/pythonnz/pdfbaker/commit/dbf2b8826e7dd607310fe28f71c341be8f4540e7))

Finally, this is working.


## v0.8.6 (2025-05-08)

### Bug Fixes

- Need to capture also stderr
  ([`cb6d2a9`](https://github.com/pythonnz/pdfbaker/commit/cb6d2a9c76f618274dacffbc884ce34a4a55fc83))


## v0.8.5 (2025-05-08)

### Bug Fixes

- Add some debug logging
  ([`83060f4`](https://github.com/pythonnz/pdfbaker/commit/83060f4d06425dd184f712795b3e94003003d32e))

Still not determining correctly whether a release is needed.


## v0.8.4 (2025-05-08)

### Bug Fixes

- Use grep to find string in multiline output
  ([`34e0575`](https://github.com/pythonnz/pdfbaker/commit/34e05755f267d1fe2e69a7a6eba62d46e77dac48))


## v0.8.3 (2025-05-08)

### Bug Fixes

- Don't re-trigger release, cater for some concurrency issues
  ([`be08d84`](https://github.com/pythonnz/pdfbaker/commit/be08d84b1ccfd5ffea1c213c44392ce6133dc6f7))


## v0.8.2 (2025-05-08)

### Bug Fixes

- Use new personal access token
  ([`788c60a`](https://github.com/pythonnz/pdfbaker/commit/788c60af19f535ae3211a9a8f5608b1ddc9bef64))

- Use same token for checkout
  ([`2deb5da`](https://github.com/pythonnz/pdfbaker/commit/2deb5da71207f0fef118e3e83339641123844d69))


## v0.8.1 (2025-05-08)

### Bug Fixes

- Checking where uv gets installed
  ([`966ffff`](https://github.com/pythonnz/pdfbaker/commit/966ffff0ff5cf04e93a944b0848d31a252d925ad))

- Specify path to uv
  ([`ed71ff7`](https://github.com/pythonnz/pdfbaker/commit/ed71ff7494504798af94db2c5ecef4b538cb86f3))

python-semantic-release runs `build_command` in a new shell...


## v0.8.0 (2025-05-08)

### Features

- Add names to stages
  ([`83db7fd`](https://github.com/pythonnz/pdfbaker/commit/83db7fd562153865d7bcc916b2d0c7fd79374ed0))

Not a real feature, want to trigger new release


## v0.7.1 (2025-05-08)

### Bug Fixes

- Add GH_TOKEN for creating release, remove invalid "version_source"
  ([`6e7e99d`](https://github.com/pythonnz/pdfbaker/commit/6e7e99d8f73000e1f7617cd2fe12b5b281c478ce))

- Can't use official release action (docker), it can't run `uv build`
  ([`c9d4e52`](https://github.com/pythonnz/pdfbaker/commit/c9d4e52d035912fb4a2706d80da9312e0024bac7))

Mimicking `released` output for the subsequent actions

- Correct PyPI action version
  ([`66801c5`](https://github.com/pythonnz/pdfbaker/commit/66801c52f581ba72c5dc21420c8db0488d27bcb4))

- Need to set up Python and uv for running `uv build`
  ([`0e353a1`](https://github.com/pythonnz/pdfbaker/commit/0e353a18bd9c9f540383eafb3901f3963ce5a9d1))

- Use official python-semantic-release actions
  ([`0c86b69`](https://github.com/pythonnz/pdfbaker/commit/0c86b694239b8f333e9dcd21da0886e9a314472d))


## v0.7.0 (2025-05-08)

### Features

- First proper release with python-semantic-release
  ([`f2996cb`](https://github.com/pythonnz/pdfbaker/commit/f2996cbbcfa24cf40996b002e60d828d1471d59d))

Not a real feature, just a minor rename to trigger the release.


## v0.6.3 (2025-05-08)

### Bug Fixes

- Need to double backslash escape in .toml
  ([`b9db84e`](https://github.com/pythonnz/pdfbaker/commit/b9db84e13e89d4a3a956c9a21e1e08b096d66bbd))

- Remove invalid "commit-parser" section (using default "angular" anyway)
  ([`cc4a985`](https://github.com/pythonnz/pdfbaker/commit/cc4a985be47df22a7c5f6da775b7969fdf6af3e8))

### Continuous Integration

- Delete .releaserc in favour of all settings in pyproject.toml
  ([`178cd75`](https://github.com/pythonnz/pdfbaker/commit/178cd7537f72d0e638572d927cf97038971d5840))


## v0.6.2 (2025-05-08)

### Bug Fixes

- Create github release before publishing
  ([`886e8dc`](https://github.com/pythonnz/pdfbaker/commit/886e8dc89804a272b2e5fc165ffd81cfb81de5cb))

- Remove GH_TOKEN
  ([`16b3aad`](https://github.com/pythonnz/pdfbaker/commit/16b3aad7017136cbf9c7552f59daa2f94afab2a1))

Using the deploy key now

- Use deploy key
  ([`a943ffc`](https://github.com/pythonnz/pdfbaker/commit/a943ffc9b628b08cf9c2c6fd318d3745136e1e18))

python-semantic-release needs to write (version number, changelog...) Github actions can not be
  allowed to bypass branch protection rules. Deploy keys can.
  https://github.com/orgs/community/discussions/25305#discussioncomment-10728028

### Code Style

- Add newline
  ([`73cd049`](https://github.com/pythonnz/pdfbaker/commit/73cd049895c1aa2ffed96466b8afe4bb90989275))

### Continuous Integration

- Add python-semantic-release
  ([`b1ec53c`](https://github.com/pythonnz/pdfbaker/commit/b1ec53c3ed869c48fc8fb14732e6330938f83e3f))

- Only release if pre-commit and tests were successful
  ([`9be16d7`](https://github.com/pythonnz/pdfbaker/commit/9be16d7480fbfad45862cc5df895344e0e3f516b))

- Use correct workflow file name
  ([`717d273`](https://github.com/pythonnz/pdfbaker/commit/717d2731c39e9fc82deef9b88184eca3153323bd))


## v0.6.1 (2025-04-29)

- Initial Release
