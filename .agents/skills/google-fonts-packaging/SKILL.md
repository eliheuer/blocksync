# /google-fonts-packaging

Prepare upstream release, downstream metadata, Google Fonts Packager dry run,
Add Font issue, and downstream PR handoff.

## Usage

`/google-fonts-packaging [metadata|release|packager|issue|pr|all]`

Default: `all`

## Preconditions

- Maintainer decisions are recorded in `GF_READINESS.md`.
- Drawing/source blockers are fixed or explicitly accepted for review.
- QA and visual proof evidence is current.
- Public upstream URL is final.
- Local `google/fonts` fork is synced, or
  `make prepare-gf-clean-checkout` has prepared an isolated
  `GF_REPO_PATH=/private/tmp/blocksync-google-fonts` checkout.
- Git identity and Google CLA identity are aligned.

## Source Strategy

Choose exactly one source strategy and document it:

- default branch,
- latest release/archive,
- build from source.

For each strategy, verify every `source.files` path exists, generated/ignored
files are handled intentionally, and `source.config_yaml` is present only for
build-from-source mode or reviewer request.

## Downstream Metadata

Check family name, designer strings, category, date, font filenames, axes,
subsets, source repository URL, source commit, and archive URL when used. Do
not apply metadata into `google/fonts` until final values are available.
When final maintainer values are available, copy
`documentation/google-fonts-final-values.template.json`, fill it, regenerate
the answer packet with `make final-values-packet`, validate it with
`make final-values-check VALUES=/path/to/final-values.json`, then apply it with
`make apply-final-values VALUES=/path/to/final-values.json`. This also aligns
`OFL.txt` and active UFO `fontinfo.plist` copyright URLs with the final public
upstream URL. After the Add Font issue is opened, include its URL as
`google_fonts_issue_url`.

Use:

```bash
make metadata-check
```

This validates the draft against the built font and reports the expected
`date_added`/`source.commit` blockers without failing. Use
`make metadata-final-check` only after final package values are filled in.

## Packager And PR

Run Packager without PR mode first. If the shared `google/fonts` fork has
unrelated dirty paths, use:

```bash
make prepare-gf-clean-checkout
GF_REPO_PATH=/private/tmp/blocksync-google-fonts make package-dry-run-readiness
GF_REPO_PATH=/private/tmp/blocksync-google-fonts make package-dry-run
make packager-dry-run-record
make downstream-pr-draft
GF_REPO_PATH=/private/tmp/blocksync-google-fonts make downstream-pr-readiness
```

For rehearsals against a reviewed metadata copy, both the readiness report and
wrapper accept `PACKAGE_METADATA_PATH=/path/to/metadata-draft.md`. The wrapper
also accepts `PACKAGER_WORK_DIR`, `PACKAGER_DRY_RUN_RECORD_PATH`, and
`PACKAGER_DRY_RUN_RECORD_OUTPUT` so temporary dry-run evidence can be isolated
from the repo docs. The report command is non-strict for normal readiness
generation, but `make package-dry-run` records with strict validation and fails
if the generated record does not match the metadata/package evidence.

Review that changed paths are limited to one family directory and that fonts,
article/description, images, license, and source metadata are present. Open the
Add Font issue before any PR-mode run.
