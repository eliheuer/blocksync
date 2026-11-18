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
- Local release archive SHA-256: `9f27875f08342f384fec880e47d80d42978c5492d537558a4d6d495d7b80c6a4`
- Final GitHub release archive URL recorded: pending

## Archive Inputs

| Source file | Destination in package | Exists | Size bytes | SHA-256 |
| --- | --- | --- | ---: | --- |
| `OFL.txt` | `OFL.txt` | yes | 4391 | `63ca62a9ac81bb373fe70dd6730789d997a8d106004df6d54408a018299ade4b` |
| `fonts/variable/Blocksync[wdth,wght].ttf` | `Blocksync[wdth,wght].ttf` | yes | 94968 | `a88ba481b15a8ca6fe8c4a7a716c16a9094ec13ea3b19e57ffdc44414a65fb0e` |
| `documentation/DESCRIPTION.en_us.html` | `DESCRIPTION.en_us.html` | yes | 496 | `252b3b6428976dc9ff5882cda17a84eb97dd81792c69d6f342a10071b33f4e85` |

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
