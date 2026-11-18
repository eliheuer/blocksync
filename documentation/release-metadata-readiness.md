# Release Metadata Readiness

This generated report ties the Google Fonts metadata placeholders to
the current source version, built font version, and git state. It
documents why `date_added` and `source.commit` cannot be final while
the release tree is still under review.

## Summary

- Release metadata local evidence ready: yes
- Release metadata final-ready for submission: no
- Current git HEAD: `eadeb6a445d79cd79e5d6365dc782744db11a75f`
- Working tree clean: no
- Dirty paths total: 2230
- Dirty modified paths: 554
- Dirty untracked paths: 1676
- Metadata repository_url: `https://github.com/eliheuer/blocksyncer`
- Metadata branch: `main`
- Metadata date_added final-looking: no
- Metadata source.commit final-looking: no
- Metadata source.commit equals current HEAD: no
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
