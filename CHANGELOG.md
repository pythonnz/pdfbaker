# CHANGELOG


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
