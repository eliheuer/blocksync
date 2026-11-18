# Final Submission Blockers

This generated snapshot separates local release readiness from values
or review decisions that cannot be finalized by automation alone.

## Summary

| Area | Current state | Final-submission requirement |
| --- | --- | --- |
| Source format | ready; 7 UFO sources, 6 archived Glyphs snapshots, default layers only: yes | Keep `sources/config.yaml` pointed at `sources/Blocksync.designspace` unless Google Fonts requests the release/archive fallback |
| Archived Glyphs sources | top-level `.glyphs` files remain out of `sources/`; archived snapshots: 6 | Keep `.glyphs` files archived and out of package inputs |
| Release gate | `make release-check` currently has local evidence ready: yes | Rerun after every source, metadata, package, or workflow change |
| Final readiness gate | no; blockers: 6 | Pass `make final-readiness-check` before submission |
| Release metadata | date_added: `2026-11-18`; commit: `46cd53e51744630b4f92e2a2e5957b41e6bd9294`; current HEAD: `46cd53e51744630b4f92e2a2e5957b41e6bd9294`; working tree clean: no | Commit the reviewed release tree and apply final package date/source commit |
| Fontspector release/package context | `googlefonts/metadata/unreachable_subsetting`: 1, `contour_count`: 1, `outline_alignment_miss`: 1; honest zero-warning state possible: no | Fix or explicitly accept remaining warning floor before opening the Add Font issue |
| Family name readiness | local evidence ready: yes | Record final `namecheck.fontdata.com` clearance |
| Authorship/disclosure | local evidence ready: yes | Confirm designer, authorship/CLA/RFN, and AI-use disclosure answers |
| Package source strategy | local evidence ready: yes; final-ready: yes | Confirm `source.config_yaml` or release/archive strategy before final metadata |
| Visual proofing | local evidence ready: yes; packet ready: yes; final-ready: no | Human-review proof pages and generated composite glyphs |
| No-PR Packager dry run | ready: no; recorded: yes | Run and record the guarded dry run after final metadata clears |
| Downstream PR | ready: no | Open Google Fonts issue first, then prepare one-family downstream PR |
| Submission handoff | local evidence ready: yes | Keep the Add Font issue draft and handoff synchronized before opening the issue |
| Fallback archive | local hashes match: yes; final URL: pending | Publish and record archive URL only if release/archive fallback is selected |
| Reusable workflow | reusable `.agents` bundle ready: yes | Copy `.agents`, scripts, and reports into future font repos with family-specific replacements |

## Current Final Readiness Blockers

- final decision sheet still has unresolved answer cells: 3
- package-context Fontspector report has FAIL/FATAL/ERROR results
- Fontspector warning floor is not resolved or accepted: release 3 WARN, package 3 WARN
- zero-warning worklist says true zero is not currently achieved
- generated composite review glyphs are not finally accepted/revised/deferred
- downstream Google Fonts PR readiness is not complete

## Maintainer Decision Sheet

| Decision | Current evidence | Final answer |
| --- | --- | --- |
| Google Fonts `date_added` | Candidate package date | 2026-11-18 |
| Final source commit | Packaged source revision | 46cd53e51744630b4f92e2a2e5957b41e6bd9294 |
| Public upstream URL | Public GitHub repository | https://github.com/eliheuer/blocksync |
| Public default branch | GitHub default branch | main |
| Package source strategy | preferred `source.config_yaml: "sources/config.yaml"` | Build from source with `source.config_yaml` pointing to `sources/config.yaml` |
| Family name uniqueness | `namecheck.fontdata.com` API clear on 2026-11-18 | namecheck.fontdata.com API clear on 2026-11-18: zero matches at confidence 0.3-1.0 and trademark=false |
| Designer string | AUTHORS.txt and OFL | Eli Heuer |
| AI-use disclosure | AI-assisted engineering, component work, QA and independent proof review documented in the issue draft | Eli confirmed the issue disclosure covers earlier work, engineering, components, mark positioning, QA and proof review. |
| Authorship/CLA/RFN status | Eli confirmed rights to all styles, the OFL, continued maintenance, the absence of an applicable upstream RFN, and agreement to the contribution requirements. | Pending confirmation of the downstream contributor’s CLA identity |
| Fontspector warning floor | Release VF has three warnings. Package-context QA reports the missing web-subset mark. | Accept for first review or schedule source cleanup |
| Visual proof | 18-page print proof, two-axis HTML specimen and separate legacy proof bundle | Eli approved the heavier normal-width Black after a side-by-side proof. Independent checks cover weight, width, fractions, mark stacks and the complete language specimens. |
| Generated Latin Extended and Vietnamese composites | Added to clear coverage/subset gates; documented as review glyphs | Pending design review. Hold the submission until the placeholder identities and accent constructions have been reviewed. |
| Static TTFs | Generated for local proofing, not listed as downstream package files | Ship the variable TTF. Keep all 18 static instances for proofs. |
| Release/archive fallback | `dist/Blocksync-GF-review.zip` is built by `make release-check` and tracked in `documentation/release-archive-manifest.md` | Use source.config_yaml. Keep the verified ZIP for a requested fallback. |

## Evidence Reports

- `documentation/final-readiness-report.md`
- `documentation/release-metadata-readiness.md`
- `documentation/source-readiness.md`
- `documentation/family-name-readiness.md`
- `documentation/authorship-disclosure-readiness.md`
- `documentation/packager-source-strategy.md`
- `documentation/proof-review-readiness.md`
- `documentation/proof-review-packet.md`
- `documentation/google-fonts-final-values.proposal.json`
- `documentation/fontspector-zero-warning-worklist.md`
- `documentation/package-dry-run-readiness.md`
- `documentation/packager-dry-run-record.md`
- `documentation/downstream-pr-readiness.md`
- `documentation/submission-handoff-readiness.md`
- `documentation/google-fonts-agent-reuse-readiness.md`
- `documentation/release-archive-manifest.md`
- `out/fontspector/fontspector-report.html`
- `out/fontspector/fontspector-package-context-report.html`
- `out/proof/index.html`

Regenerate this snapshot with `make blockers` after release checks,
metadata changes, source edits, proof review, or Google Fonts reviewer
feedback.
