# Google Fonts Downstream Package Preview

This preview describes the expected downstream `google/fonts` package for the
first Blocksync submission. It is a review target, not a substitute for a
Packager dry run in a local `google/fonts` checkout.

## Expected Downstream Path

```text
ofl/blocksync
```

## Expected Files

Variable-font-first package:

```text
ofl/blocksync/METADATA.pb
ofl/blocksync/OFL.txt
ofl/blocksync/Blocksync[wdth,wght].ttf
ofl/blocksync/DESCRIPTION.en_us.html
```

The generated static TTFs are proofing outputs for now. Include them only if
Google Fonts review asks for downstream static files.

## Source Strategy

Preferred first-submission strategy:

```text
source.config_yaml: "sources/config.yaml"
```

That path keeps the public package reproducible from the active
designspace/UFO sources. Historical `.glyphs` files remain archived in
`sources/archive/` and are not package inputs.

Fallback strategy:

If Google Fonts asks for release/archive packaging instead of a reproducible
builder config, run:

```bash
make release-archive-build
```

This creates `dist/Blocksync-GF-review.zip` and updates
`documentation/release-archive-manifest.md`. Publish an equivalent GitHub
release archive, add the final `source.archive_url` to the metadata draft, and
rerun `make release-check`.

## Expected METADATA.pb Shape

The canonical draft lives in
`documentation/google-fonts-downstream-metadata-draft.md`. Before applying it
downstream:

- replace `date_added`;
- replace `source.commit`;
- confirm `source.branch`;
- confirm final namecheck and maintainer disclosures;
- keep `latin`, `latin-ext`, `menu`, and `vietnamese` unless Google Fonts asks
  for different subset scope;
- keep `source.config_yaml` unless the submission switches to release/archive
  packaging.

## Review Checks

- `make release-check`
- `make proof`
- `make release-archive-build` if release/archive packaging is used
- final no-PR Packager dry run in a local `google/fonts` checkout
