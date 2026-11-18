# Final Submission Blockers

This generated snapshot separates local release readiness from values
or review decisions that cannot be finalized by automation alone.

## Summary

| Area | Current state | Final-submission requirement |
| --- | --- | --- |
| Source format | ready; 7 UFO sources, 6 archived Glyphs snapshots, default layers only: yes | Keep `sources/config.yaml` pointed at `sources/Blocksync.designspace` unless Google Fonts requests the release/archive fallback |
| Archived Glyphs sources | top-level `.glyphs` files remain out of `sources/`; archived snapshots: 6 | Keep `.glyphs` files archived and out of package inputs |
| Release gate | `make release-check` currently has local evidence ready: yes | Rerun after every source, metadata, package, or workflow change |
| Final readiness gate | no; blockers: 10 | Pass `make final-readiness-check` before submission |
| Release metadata | date_added: `PENDING-YYYY-MM-DD`; commit: `PENDING_FINAL_40_CHARACTER_COMMIT`; current HEAD: `eadeb6a445d79cd79e5d6365dc782744db11a75f`; working tree clean: no | Commit the reviewed release tree and apply final package date/source commit |
| Fontspector release/package context | `googlefonts/metadata/unreachable_subsetting`: 1, `contour_count`: 1, `outline_alignment_miss`: 1; honest zero-warning state possible: no | Fix or explicitly accept remaining warning floor before opening the Add Font issue |
| Family name readiness | local evidence ready: yes | Record final `namecheck.fontdata.com` clearance |
| Authorship/disclosure | local evidence ready: yes | Confirm designer, authorship/CLA/RFN, and AI-use disclosure answers |
| Package source strategy | local evidence ready: yes; final-ready: no | Confirm `source.config_yaml` or release/archive strategy before final metadata |
| Visual proofing | local evidence ready: yes; packet ready: yes; final-ready: no | Human-review proof pages and generated composite glyphs |
| No-PR Packager dry run | ready: no; recorded: no | Run and record the guarded dry run after final metadata clears |
| Downstream PR | ready: no | Open Google Fonts issue first, then prepare one-family downstream PR |
| Submission handoff | local evidence ready: yes | Keep the Add Font issue draft and handoff synchronized before opening the issue |
| Fallback archive | local hashes match: yes; final URL: pending | Publish and record archive URL only if release/archive fallback is selected |
| Reusable workflow | reusable `.agents` bundle ready: yes | Copy `.agents`, scripts, and reports into future font repos with family-specific replacements |

## Current Final Readiness Blockers

- metadata `date_added` is still `PENDING-YYYY-MM-DD`
- metadata `source.commit` is still pending
- AI-use disclosure is still pending maintainer answer
- final decision sheet still has unresolved answer cells: 13
- zero-warning worklist says true zero is not currently achieved
- visual proof review is still marked maintainer-required
- generated composite review glyphs are not finally accepted/revised/deferred
- no-PR Packager dry run is not ready to start
- final no-PR Packager dry run has not been recorded
- downstream Google Fonts PR readiness is not complete

## Maintainer Decision Sheet

| Decision | Current evidence | Final answer |
| --- | --- | --- |
| Google Fonts `date_added` | `PENDING-YYYY-MM-DD` | TBD |
| Final source commit | `PENDING_FINAL_40_CHARACTER_COMMIT` | TBD |
| Public upstream URL | `https://github.com/eliheuer/blocksyncer` | Confirm or replace |
| Public default branch | `main` | Confirm or replace |
| Package source strategy | preferred `source.config_yaml: "sources/config.yaml"` | Confirm or switch to release/archive |
| Family name uniqueness | `namecheck.fontdata.com` API clear on 2026-05-30 | namecheck.fontdata.com API clear on 2026-05-30: zero matches at confidence 0.3-1.0 and trademark=false |
| Designer string | `Eli Heuer` | Confirm or replace |
| AI-use disclosure | pending maintainer answer | Confirm wording |
| Authorship/CLA/RFN status | local OFL/no-RFN drafts exist | Confirm |
| Fontspector warning floor | `make release-check` passes with 3 WARN: metadata reachability, `uni01F5` contour count, outline alignment | Accept for first review or schedule source cleanup |
| Visual proof | `make proof` writes `out/proof/index.html` with 73 proof pages and 19 fonts | Maintainer review required |
| Generated Latin Extended and Vietnamese composites | Added to clear coverage/subset gates; documented as review glyphs | Accept, revise, or defer |
| Static TTFs | Generated for local proofing, not listed as downstream package files | Keep proof-only unless Google Fonts asks |
| Release/archive fallback | `dist/Blocksync-GF-review.zip` is built by `make release-check` and tracked in `documentation/release-archive-manifest.md` | Use only if Google Fonts rejects `source.config_yaml` path |

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
