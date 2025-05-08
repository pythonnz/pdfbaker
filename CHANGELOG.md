# CHANGELOG


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

### Bug Fixes

- Always inject "page_number" into the config/template context
  ([`f6b38a0`](https://github.com/pythonnz/pdfbaker/commit/f6b38a090d0df1adc20444c6ff8098ec08803e92))

- Config directory may already be rendered string
  ([`1d05a3a`](https://github.com/pythonnz/pdfbaker/commit/1d05a3a891b9873c91871f6d8342bfeaf15976ca))

We determine variant pages late in the game when the variant config was merged into the document
  config

- Nested f-string
  ([`8f357bb`](https://github.com/pythonnz/pdfbaker/commit/8f357bbb4ab4b10a04615b54cc1bb984115b4e38))

- Nested quotes
  ([`6645491`](https://github.com/pythonnz/pdfbaker/commit/664549108b18ffea2f24e1b3bd5d4ef682204ddc))

- Pages may only be defined in variants, not document itself
  ([`75cae8e`](https://github.com/pythonnz/pdfbaker/commit/75cae8e30376c9a9501167d7ad59b41b0b6d25c5))

- Typo
  ([`b79cbbb`](https://github.com/pythonnz/pdfbaker/commit/b79cbbb0d55ba1fa399d1705041be34c759f9f10))
