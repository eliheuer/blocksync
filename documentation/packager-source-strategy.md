# Packager Source Strategy

This generated report checks the preferred build-from-source path and
the release/archive fallback so agents do not mix the two packaging
strategies during Google Fonts handoff.

## Summary

- Preferred build-from-source path ready locally: yes
- Release/archive fallback ready locally: yes
- Package source strategy local evidence ready: yes
- Package source strategy final-ready for submission: yes
- Final strategy decision recorded: yes
- Metadata repository_url: `https://github.com/eliheuer/blocksync`
- Metadata branch: `main`
- Metadata commit final-looking: yes
- Metadata config_yaml: `sources/config.yaml`
- Metadata archive_url: `not set`
- Source files mapped: 3

## Source Files

| Source file | Destination | Exists | Tracked | Ignored |
| --- | --- | --- | --- | --- |
| `OFL.txt` | `OFL.txt` | yes | yes | no |
| `fonts/variable/Blocksync[wdth,wght].ttf` | `Blocksync[wdth,wght].ttf` | yes | no | yes |
| `documentation/DESCRIPTION.en_us.html` | `DESCRIPTION.en_us.html` | yes | yes | no |

## Preferred Strategy

- Keep `source.config_yaml: "sources/config.yaml"` for the first
  submission while Google Fonts accepts the reproducible
  designspace/UFO build path.
- Historical `.glyphs` files stay archived in `sources/archive/` and
  are not package inputs.

## Fallback Strategy

- Use release/archive packaging only if Google Fonts rejects the
  `source.config_yaml` path or explicitly asks for prebuilt files.
- If fallback is selected, publish an archive equivalent to
  `dist/Blocksync-GF-review.zip`, add final `source.archive_url`,
  and rerun `make release-check`.

## Finalization

- Current final decision sheet answer: Build from source with `source.config_yaml` pointing to `sources/config.yaml`
- Replace final `source.commit` before any Packager dry run.
- Confirm package strategy before opening the Add Font issue.
