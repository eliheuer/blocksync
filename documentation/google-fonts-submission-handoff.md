# Google Fonts submission handoff

**Submission is on hold pending Eli’s design review.** The maintainer requested preparation only. Keep the issue and pull request as drafts until he gives the go-ahead.

## Release candidate

- Upstream repo: https://github.com/eliheuer/blocksync
- Public branch: main
- Google Fonts issue: pending
- Source commit: 46cd53e51744630b4f92e2a2e5957b41e6bd9294
- Candidate package date: 2026-11-18
- Source: seven UFO masters and `sources/Blocksync.designspace`. Earlier Glyphs sources are in `sources/archive/`.
- Packager builds `sources/config.yaml` and ships the variable TTF, OFL, description and METADATA.pb in `ofl/blocksync`. The 18 static fonts are proof outputs.
- FontData returned zero matches for Blocksync at all six reported confidence levels on 2026-11-18. The trademark flag was false. See `documentation/namecheck-fontdata-result.json`.

## Draft Add Font Issue

The issue text and maintainer confirmations are in `documentation/google-fonts-add-font-issue-draft.md` and `documentation/google-fonts-final-decision-sheet.md`. Google Fonts reviews the issue before requesting a downstream PR. The expected branch is `gftools_packager_ofl_blocksync` and the title is `Blocksync : 1.000 added`. The PR template uses `Taken from the upstream repo <repo-url> at commit <commit-url>.`

## QA and visual review

The [design review](design-review.md) identifies inconsistent capital weights, protected placeholder glyphs, fragile Black counters and verified letter collisions. The [live comparison](https://eliheuer.github.io/blocksync/proof/design.html) highlights intersecting outlines in red.

The baseline and first migration build have identical outlines, metrics, axes and shaping. The release adds the heavier normal-width Black selected by Eli, two component-built fractions and zero-width U+0331 for Amarakaeri, Mezquital Otomi and Secoya. The printed and interactive proofs include both axes. Existing green glyphs, component donors and their anchors are protected. The inherited Font.Garden findings are documented in CONTEXT.md.

Fontspector 1.9.0 reports **3 WARN, 0 FAIL, 0 FATAL, 0 ERROR** on the release variable font and **3 WARN, 6 FAIL, 0 FATAL, 0 ERROR** in the local package-context check. All six failures identify one absent serving codepoint. Besides the three specimen texts, the web subset check flags additional samples for Chickasaw, Siona and Ticuna. A controlled test with the same font and U+0331 added only to the validator’s Latin serving data passed. The published check still runs against Google's original data.

The official no-PR Packager produced four files against google/fonts revision `5bd87dfc525c8a0d1d8529d3684716e00c3fc59a`. The packaged TTF and a clean build with the source commit timestamp were byte-identical (SHA-256 `401f5adf26abeff20caef3a4dcfa9570d5ef1f3624bb6d9464421e17bae0cb60`). The final font has 630 glyphs and 617 encoded codepoints. The full online Google Fonts profile on those four files returned 160 PASS, 10 INFO, 44 SKIP, 4 WARN and 6 FAIL. The fourth warning is the missing Google Fonts designer profile for Eli Heuer.

The full font renders the three language samples. Google's web subset definitions omit U+0331 from the declared Latin subsets. Fontspector flags the resulting missing character in the simulated web fonts. The onboarding team tracks split-font mark attachment. [Subset tracking](https://github.com/googlefonts/nam-files/issues/6) · [Fontspector tracking](https://github.com/fonttools/fontspector/issues/946)

[Print proof](https://eliheuer.github.io/blocksync/proof/proof.pdf) · [Two-axis specimen](https://eliheuer.github.io/blocksync/proof/widths.html)

## Reproducing the handoff

Run `make setup build test proof` and `make release-check`. Use a clean downstream checkout and `gftools packager` for a source-build rehearsal. Run the unexcluded Google Fonts profile over the resulting four-file family. Record the Packager source revision because it resolves the upstream branch at build time.

The workflow also maintains the following records.

- Final values and package preview: `documentation/google-fonts-final-values-packet.md`, `documentation/google-fonts-downstream-package-preview.md`.
- Packager and archive verification: `documentation/package-dry-run-readiness.md`, `documentation/packager-dry-run-record.md`, `documentation/release-archive-manifest.md`.
- Downstream review: `documentation/downstream-pr-readiness.md`, `documentation/next-actions.md`, `documentation/final-submission-blockers.md`, `documentation/final-readiness-report.md`.
