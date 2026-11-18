# Google Fonts Next Actions

This generated report condenses the current Blocksync release blockers
into an owner-grouped queue. It is intentionally short so future agents
can resume Google Fonts release work without rediscovering the same
state from the full documentation set.

## Snapshot

- Release metadata local evidence ready: yes
- Source-ready for designspace/UFO build path: yes
- Family-name local evidence ready: yes
- Authorship/disclosure local evidence ready: yes
- Package source strategy local evidence ready: yes
- Proof review local evidence ready: yes
- Proof review packet ready: yes
- Reusable `.agents` workflow ready: yes
- Final-ready for Google Fonts submission: no
- Final readiness blockers: 6
- Remaining Fontspector warning floor: `googlefonts/metadata/unreachable_subsetting`: 1, `contour_count`: 1, `outline_alignment_miss`: 1
- No-PR Packager dry-run ready: no
- No-PR Packager dry-run recorded: yes
- Downstream PR ready: no
- Fallback archive URL status: pending
- Public placeholder blocker count: 1
- Decision rows tracked: 14
- Unresolved final-answer rows: 3

## Maintainer Decision Rows

| Decision | Current evidence | Needed answer |
| --- | --- | --- |
| Authorship/CLA/RFN status | Eli confirmed rights to all styles, the OFL, continued maintenance, the absence of an applicable upstream RFN, and agreement to the contribution requirements. | Pending confirmation of the downstream contributor’s CLA identity |
| Fontspector warning floor | Release VF has three warnings. Package-context QA reports the missing web-subset mark. | Accept for first review or schedule source cleanup |
| Generated Latin Extended and Vietnamese composites | Added to clear coverage/subset gates; documented as review glyphs | Pending design review. Hold the submission until the placeholder identities and accent constructions have been reviewed. |

## Maintainer Decisions

| Blocker | Next action |
| --- | --- |
| final decision sheet still has unresolved answer cells: 3 | Fill every final-answer cell in the maintainer decision sheet. |

## Source And Proof Review

| Blocker | Next action |
| --- | --- |
| zero-warning worklist says true zero is not currently achieved | Either fix the remaining warning buckets or explicitly accept them for first review. |
| generated composite review glyphs are not finally accepted/revised/deferred | Accept, revise, or defer the generated Latin Extended and Vietnamese review glyphs. |

## Packaging And Downstream

| Blocker | Next action |
| --- | --- |
| package-context Fontspector report has FAIL/FATAL/ERROR results | Resolve the blocker and rerun `make final-readiness-check`. |
| Fontspector warning floor is not resolved or accepted: release 3 WARN, package 3 WARN | Resolve the blocker and rerun `make final-readiness-check`. |
| downstream Google Fonts PR readiness is not complete | Open the Google Fonts issue first, then prepare the one-family downstream PR. |

## Fast Resume Sequence

1. Fill a copy of `documentation/google-fonts-final-values.template.json` with maintainer answers.
2. Use `documentation/google-fonts-final-values.proposal.json` as a non-final starting point where useful; remove proposal-only `_...` keys before validation.
3. Run `make final-values-check VALUES=/path/to/final-values.json`, then `make apply-final-values VALUES=/path/to/final-values.json`.
4. Review `out/proof/index.html` and update the proof/composite-glyph decisions.
5. Rerun `make release-check`.
6. Rerun `make final-readiness-check`; if it passes, run the guarded no-PR Packager dry run, using `GF_REPO_PATH=/private/tmp/blocksync-google-fonts` if the shared fork is dirty.
7. Open the Google Fonts issue, add its URL to `google_fonts_issue_url`, rerun the values helper, then prepare the scoped downstream PR after the no-PR package is reviewed.

## Evidence Reports

- `documentation/final-readiness-report.md`
- `documentation/release-metadata-readiness.md`
- `documentation/source-readiness.md`
- `documentation/family-name-readiness.md`
- `documentation/authorship-disclosure-readiness.md`
- `documentation/packager-source-strategy.md`
- `documentation/proof-review-readiness.md`
- `documentation/proof-review-packet.md`
- `documentation/open-placeholder-audit.md`
- `documentation/decision-application-blockers.md`
- `documentation/fontspector-zero-warning-worklist.md`
- `documentation/package-dry-run-readiness.md`
- `documentation/packager-dry-run-record.md`
- `documentation/downstream-pr-readiness.md`
- `documentation/google-fonts-agent-reuse-readiness.md`
- `documentation/release-archive-manifest.md`
- `documentation/google-fonts-submission-handoff.md`
- `documentation/google-fonts-final-values.proposal.json`
