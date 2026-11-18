# Release Archive Manifest

This is a local review archive for fallback Google Fonts release/archive
packaging. The preferred package path remains `sources/config.yaml` ->
`sources/Blocksync.designspace` unless Google Fonts asks for prebuilt
release files.

## Summary

- Mapping source: `documentation/google-fonts-downstream-metadata-draft.md`
- Local release archive: `dist/Blocksync-GF-review.zip`
- Archive inputs expected: 3
- Archive inputs present locally: 3 / 3
- Missing archive inputs: 0
- Validation issues: 0
- Local release archive exists: yes
- Local release archive contains expected files: yes
- Local release archive has extra files: no
- Local release archive hashes match source files: yes
- Local release archive metadata deterministic: yes
- Local release archive SHA-256: `1ea3cce3b125b5fa315120f7c6e641d1030e361f7043b9cedcd9a57a239ecfad`
- Final GitHub release archive URL recorded: pending

## Archive Inputs

| Source file | Destination in package | Exists | Size bytes | SHA-256 |
| --- | --- | --- | ---: | --- |
| `OFL.txt` | `OFL.txt` | yes | 4393 | `4b6ed05e5d8eae7161df728438a0ea114ae735552e969df5099c5785b91aa219` |
| `fonts/variable/Blocksync[wdth,wght].ttf` | `Blocksync[wdth,wght].ttf` | yes | 81160 | `5a31cc7b62823ea28ec241d27ccb376d70afa77e82e101979aa2953589694025` |
| `documentation/DESCRIPTION.en_us.html` | `DESCRIPTION.en_us.html` | yes | 528 | `2e5e902626af170dc9e61fcda21036c13bb05ea28fcb58a2c4689069dce31a97` |

## Archive Entries

| Archive entry | Present | Size matches source | SHA-256 matches source | Deterministic metadata |
| --- | --- | --- | --- | --- |
| `OFL.txt` | yes | yes | yes | yes |
| `fonts/variable/Blocksync[wdth,wght].ttf` | yes | yes | yes | yes |
| `documentation/DESCRIPTION.en_us.html` | yes | yes | yes | yes |

## Final Release Gate

1. Finish source and proof review.
2. Replace final `date_added` and `source.commit` values.
3. If using release/archive packaging, publish this archive or an
   equivalent GitHub release asset and add the final `source.archive_url`.
4. Rerun `make release-check` after any source, metadata, or archive
   mapping change.
