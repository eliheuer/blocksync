# Google Fonts Source Strategy

This note records the current Blocksync packaging direction so future agents do
not mix the designspace/UFO source policy with a binary-only package path.

## Current Direction

- Active upstream source path: `sources/config.yaml` ->
  `sources/Blocksync.designspace`.
- Active sources: seven UFO masters referenced by the designspace.
- Historical `.glyphs` files are archived in `sources/archive/` and are not
  package inputs.
- Release binary output: `fonts/variable/Blocksync[wdth,wght].ttf`.
- Current downstream metadata draft keeps `source.config_yaml:
  "sources/config.yaml"` because the repo is being prepared around the
  designspace/UFO build path.
- Current downstream subset draft includes `latin`, `latin-ext`, `menu`, and
  `vietnamese`. This prevents already-encoded Latin Extended codepoints from
  being stranded. Package-context probing now shows both declared broad subsets
  clear the local Google Fonts support thresholds.

The Google Fonts metadata guide describes `source` as the upstream repository
and version trace, and its variable-font example maps package files from
`source.files`. The package guide says Packager uses the `source` block in
`METADATA.pb` for packaging. Treat the draft as a Packager preview, not as a
final downstream file, until the public commit and package date are known.

## Source Files Preview

Current local package files:

| Source file | Downstream destination | Status |
| --- | --- | --- |
| `OFL.txt` | `OFL.txt` | tracked source file |
| `fonts/variable/Blocksync[wdth,wght].ttf` | `Blocksync[wdth,wght].ttf` | generated local build output |
| `documentation/DESCRIPTION.en_us.html` | `DESCRIPTION.en_us.html` | tracked package text |

If Google Fonts wants a release/archive package instead of build-from-source
review, create a release archive containing exactly the mapped files and update
the metadata draft with the final `archive_url`.

If Google Fonts accepts the reproducible build path, keep
`source.config_yaml: "sources/config.yaml"` and make sure the public commit
contains every build input required by `build.sh`.

## Current Blockers

- Final public source commit hash.
- Final package `date_added`.
- Maintainer confirmation of package strategy: build from source with
  designspace/UFO, or generated-font release/archive fallback.
- Human review of proof output and remaining Fontspector WARN groups.

## Verification Commands

```bash
make preflight-only
make test
make metadata-check
make package-context-check
make release-check
make proof
```
