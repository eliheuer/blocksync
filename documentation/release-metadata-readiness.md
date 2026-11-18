# Release Metadata Readiness

The candidate revision identifies the reviewed font and package inputs. Later handoff documentation can refer to that revision.

## Summary

- Release metadata local evidence ready: yes
- Release metadata final-ready for submission: yes
- Current git HEAD: `46cd53e51744630b4f92e2a2e5957b41e6bd9294`
- Working tree clean: no
- Dirty paths total: 60
- Dirty modified paths: 58
- Dirty untracked paths: 2
- Metadata repository_url: `https://github.com/eliheuer/blocksync`
- Metadata branch: `main`
- Metadata date_added final-looking: yes
- Metadata source.commit final-looking: yes
- Packaged revision matches current build and package inputs: yes
- Metadata source.commit equals current HEAD: yes
- Source UFO version: `1.000`
- Built variable font matches source version: yes

## Source UFO Versions

| Source | versionMajor | versionMinor | Version string |
| --- | ---: | ---: | --- |
| `sources/Blocksync-CondensedBlack.ufo/fontinfo.plist` | 1 | 0 | `1.000` |
| `sources/Blocksync-CondensedBold.ufo/fontinfo.plist` | 1 | 0 | `1.000` |
| `sources/Blocksync-CondensedRegular.ufo/fontinfo.plist` | 1 | 0 | `1.000` |
| `sources/Blocksync-ExpandedBlack.ufo/fontinfo.plist` | 1 | 0 | `1.000` |
| `sources/Blocksync-ExpandedBold.ufo/fontinfo.plist` | 1 | 0 | `1.000` |
| `sources/Blocksync-ExpandedRegular.ufo/fontinfo.plist` | 1 | 0 | `1.000` |
| `sources/Blocksync-Regular.ufo/fontinfo.plist` | 1 | 0 | `1.000` |

## Built Font Versions

| Font | name ID 5 | Matches source version |
| --- | --- | --- |
| `fonts/variable/Blocksync[wdth,wght].ttf` | `Version 1.000` | yes |

## Finalization

- Do not replace `source.commit` until the reviewed release tree has
  been committed and `make release-check` passes on that commit.
- Do not replace `date_added` until the downstream Google Fonts package
  date is known.
- After replacing either value, run `make metadata-final-check`,
  `make release-check`, and `make final-readiness-check`.
