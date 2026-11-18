# Google Fonts Readiness

This repo is being prepared for Google Fonts onboarding.

## Current Scope

- Family: Blocksync
- License: SIL Open Font License v1.1
- Sources: UFO masters plus `sources/Blocksync.designspace`
- Axes: `wght` 400-900, `wdth` 75-125
- Build entrypoint: `make build`
- Fast structure gate: `make preflight-only`
- Release metadata evidence gate: `make release-metadata-readiness`
- Source-readiness gate: `make source-readiness`
- Metadata draft gate: `make metadata-check`
- Package-context QA gate: `make package-context-check`
- Family-name evidence gate: `make family-name-readiness`
- Authorship/disclosure evidence gate: `make authorship-disclosure-readiness`
- Packager source-strategy gate: `make packager-source-strategy`
- Proof review evidence gate: `make proof-review-readiness`
- Placeholder audit gate: `make placeholder-audit`
- Decision application gate: `make decision-application-check`
- Isolated `google/fonts` checkout prep: `make prepare-gf-clean-checkout`
- Final values helper:
  `make final-values-check VALUES=/path/to/final-values.json`, then
  `make apply-final-values VALUES=/path/to/final-values.json`
  Include `google_fonts_issue_url` after opening the Add Font issue.
- Packager readiness gate: `make package-dry-run-readiness`
- Packager dry-run evidence gate: `make packager-dry-run-record`
- Downstream PR draft gate: `make downstream-pr-draft`
- Consolidated handoff gate: `make release-check`
- Final submission gate: `make final-readiness-check`
- Preferred GF build config: `sources/config.yaml`

## Source Policy

- Active release sources are designspace/UFO only.
- `.glyphs` files are archived in `sources/archive/` and are not package inputs.
- `sources/Blocksync-Regular.ufo` is the generated normal-width default source
  used to keep the variable font default at Regular width/weight.
- Generated fonts, build outputs, instance UFOs, and local venvs are ignored.

## November 2026 release candidate

Eli has placed the submission on hold. The [design review](documentation/design-review.md) gives the first drawing and spacing batches. The [submission handoff](documentation/google-fonts-submission-handoff.md) records the packaged source revision, independent visual checks, downstream validation and remaining onboarding decisions. The [issue draft](documentation/google-fonts-add-font-issue-draft.md) follows the current Add Font template.

The migration checkpoint reproduces all 19 baseline fonts. Subsequent release changes give Black its approved heavier drawing at normal width, restore the two quarter fractions, and improve combining accents. The seven original UFOs and the editable designspace remain the family sources. The Google Fonts package ships the variable font. The 18 static fonts serve as proofs.

Use `make setup build test proof` for Font.Garden. Use `make release-check` for downstream package QA. Fontspector reports results separately for an unpackaged variable font and for the family as Google Fonts would serve it. Some Indigenous-language specimens use U+0331, which is absent from Google's Latin web subsets. The handoff tracks the downstream result and links to the serving team's existing discussion.

- [Print proof](https://eliheuer.github.io/blocksync/proof/proof.pdf)
- [Interactive width and weight proof](https://eliheuer.github.io/blocksync/proof/widths.html)
- [Construction, protected glyphs and inherited findings](CONTEXT.md)

## Reusable Workflow

Portable Google Fonts onboarding guidance lives in `.agents/`. Copy that
directory into future font repos, then replace family names, active source
paths, axes, build outputs, and package strategy values.
