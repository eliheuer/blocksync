# AGENTS.md

Guidance for Codex and other agents working in this repository.

## Project Overview

Blocksync is an open-source variable font licensed under the SIL Open Font
License v1.1. The Google Fonts-ready build path uses UFO masters plus
`sources/Blocksync.designspace`; `.glyphs` files are archived reference
snapshots only.

## Font.Garden drafting workflow

Read [CONTEXT.md](CONTEXT.md) for the family design and historical grades. The designer assigns glyphs and masters. Start every writer from the same tested commit in a separate worktree. Split by component family, record the read-only donors, and keep assignments disjoint. Both green swatches and every glyph used as a component are frozen for drafting. A donor edit requires a separate design task and review of its dependents.

Use [.agents/tasks/glyph-drafts.md](.agents/tasks/glyph-drafts.md) or [.agents/tasks/accented-letters.md](.agents/tasks/accented-letters.md), then [.agents/tasks/visual-review.md](.agents/tasks/visual-review.md). Give the reviewer clean before/after images and the rules. Only Eli approves a grade. Commit tested batches individually before integration.

Run `make setup` to install the template pins in .venv. The assignment gate compares the starting revision with the working tree and checks the allowed master/glyph pairs, green glyphs, donors and purple drafts. Pass the master names as a comma-separated list. The shared check-design tool also reports its own two-unit-grid findings. Refer those to R1 before editing any point.

Use `make runebender` to open Blocksync in the native editor from the current local Runebender checkout. Both project MCP commands use this checkout as well. Set RUNEBENDER_REPO to override its location. Select the session matching the absolute Blocksync designspace path and verify its document epoch and master before each live assignment. The runebender-blocksync endpoint also provides a disk view of the designspace. Preserve editors already open for other families.

## Quick Start

```bash
make help
make setup
make preflight-only
make release-metadata-readiness
make source-readiness
make family-name-readiness
make authorship-disclosure-readiness
make packager-source-strategy
make proof-review-readiness
make proof-review-packet
make placeholder-audit
make decision-application-check
make submission-handoff-readiness
make google-fonts-reference-refresh
make build
make qa
make test
make reports
make metadata-check
make package-context-check
make release-check
make final-values-packet
make final-values-proposal
make maintainer-decision-request
make agent-porting-manifest
make next-actions
make blockers
make proof
```

## Active Sources

- `sources/Blocksync.designspace`
- `sources/Blocksync-Regular.ufo`
- `sources/Blocksync-CondensedRegular.ufo`
- `sources/Blocksync-CondensedBold.ufo`
- `sources/Blocksync-CondensedBlack.ufo`
- `sources/Blocksync-ExpandedRegular.ufo`
- `sources/Blocksync-ExpandedBold.ufo`
- `sources/Blocksync-ExpandedBlack.ufo`

The active source config is `sources/config.yaml`. It must point to
`Blocksync.designspace`, not a `.glyphs` file. Historical `.glyphs` files live
in `sources/archive/`. `Blocksync-Regular.ufo` is the normal-width default
source generated from the corner masters.

## Build And QA

Built fonts go to `fonts/` and are ignored. Use `make build` for the pinned fgtools fontmake build and Blocksync metadata step. Use `make preflight-only` for the fast structure check that does not
need the Python font toolchain. Use `make source-readiness` for the fuller
designspace/UFO source validation pass. Use `make test` for the pinned Font.Garden suite across the family, and `make qa` for
Fontspector Google Fonts QA on the release variable font; use
`CHECK_STATIC=1 ./scripts/check_gf_fonts.sh`
when static TTF proofing outputs also need to be checked. Use
`make release-metadata-readiness` to refresh source version, built version,
current git HEAD, dirty-state, and `date_added`/`source.commit` placeholder
evidence. Use
`make family-name-readiness` and `make authorship-disclosure-readiness` to
refresh local evidence for namecheck, RFN, authorship, CLA, and AI-use
disclosure decisions. Use `make packager-source-strategy` to refresh the
preferred `source.config_yaml` path and release/archive fallback evidence. Use
`make proof-review-readiness` to verify the existing visual proof bundle and
summarize open proof/composite review decisions. Use `make proof-review-packet`
to generate a maintainer-facing proof and remaining-WARN review packet. Use
`make placeholder-audit` and `make decision-application-check` to map pending
maintainer answers to public placeholder strings and the exact metadata,
Packager, and downstream PR surfaces they block. Use
`make metadata-check` to verify the downstream metadata draft against the
current built font while allowing the documented final-date/final-commit
placeholders. Use `make package-context-check` to run Fontspector with a
temporary downstream-like package directory. Use `make metadata-final-check`
only for the final package pass. When final maintainer values are available,
run `make final-values-packet` and `make final-values-proposal`. Use
`documentation/google-fonts-final-values.proposal.json` as a non-final
starting point where useful, or copy
`documentation/google-fonts-final-values.template.json`; fill every final
value, remove proposal-only `_...` keys, and run
`make final-values-check VALUES=/path/to/final-values.json` before
`make apply-final-values VALUES=/path/to/final-values.json`. Use
`make maintainer-decision-request` when you need the shortest answer request
for the remaining human-only final values and review decisions. If the shared
local `google/fonts` fork has
unrelated dirty work, use `make prepare-gf-clean-checkout`, then pass
`GF_REPO_PATH=/private/tmp/blocksync-google-fonts` to package dry-run and
downstream readiness commands. `make package-dry-run` writes the final no-PR
Packager evidence record after a successful run; use
`make packager-dry-run-record` to refresh that report. Use
`make release-check` before handoff; it builds once, then runs release
Fontspector, metadata, package-context, and structure gates. Use
`make submission-handoff-readiness` to check the Add Font issue draft and
handoff text against the current generated reports before opening the issue.
Use `make google-fonts-reference-refresh` to verify the repo-local record of
the current Google Fonts Add Font template and recent merged downstream PR
patterns used for this setup pass. It is an offline gate; refresh the live
GitHub/docs references before final issue or PR work, then update
`.agents/google-fonts-official-reference-map.md`.
Use `make next-actions` to regenerate the compact owner-grouped blocker queue
for handoff or later resumption, and `make blockers` to regenerate the fuller
final submission blocker snapshot. Use `make agent-porting-manifest` when
copying this workflow into another font repository; it lists portable files,
family-specific replacements, and the commands to regenerate in the new repo.

## Reusable Google Fonts Knowledge

Start in `.agents/` for low-token repeat work:

- `.agents/README.md`
- `.agents/skills/build-font/SKILL.md`
- `.agents/skills/font-qa/SKILL.md`
- `.agents/skills/edit-glyph/SKILL.md`
- `.agents/skills/kerning/SKILL.md`
- `.agents/skills/proof/SKILL.md`
- `.agents/google-fonts-onboarding-checklists.md`
- `.agents/google-fonts-official-reference-map.md`
- `.agents/skills/google-fonts-onboarding/SKILL.md`
- `.agents/skills/google-fonts-qa/SKILL.md`
- `.agents/skills/google-fonts-coverage-drawing/SKILL.md`
- `.agents/skills/google-fonts-packaging/SKILL.md`
- `.agents/skills/google-fonts-finalize/SKILL.md`

Before final Google Fonts issue or PR work, refresh official docs and the
current `google/fonts` templates and recent merged new-font PR examples because
those can change.
