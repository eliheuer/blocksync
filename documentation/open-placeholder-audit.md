# Open Placeholder Audit

This generated report tracks unresolved Google Fonts handoff strings
that still need a maintainer answer, final metadata value, or external
confirmation. Generated reports are separated from public application
surfaces so echoed blockers do not look like new work.

## Summary

- Public placeholder blocker count: 17
- Pending date_added occurrences: 14
- Pending source commit occurrences: 10
- TBD markers: 0
- PR template placeholders: 3
- Pending maintainer-answer markers: 9
- Pending confirmation markers: 18
- Pending proof-review markers: 7
- Pending review-decision markers: 9
- Internal metadata guard markers: 1
- Generated evidence echoes: 58

## Public Blockers

| Kind | File | Line | Text |
| --- | --- | ---: | --- |
| pending date_added | `documentation/google-fonts-downstream-metadata-draft.md` | 11 | `date_added: "PENDING-YYYY-MM-DD"` |
| pending source commit | `documentation/google-fonts-downstream-metadata-draft.md` | 37 | `commit: "PENDING_FINAL_40_CHARACTER_COMMIT"` |
| pending source commit | `documentation/google-fonts-downstream-pr-draft.md` | 14 | `- Upstream source commit: `PENDING_FINAL_40_CHARACTER_COMMIT`` |
| PR template placeholder | `documentation/google-fonts-downstream-pr-draft.md` | 32 | `Taken from the upstream repo <repo-url> at commit <commit-url>.` |
| pending date_added | `documentation/google-fonts-final-decision-sheet.md` | 12 | `\| Google Fonts `date_added` \| `PENDING-YYYY-MM-DD` \| TBD \| `documentation/google-fonts-downstream-metadata-draft.md` \|` |
| pending source commit | `documentation/google-fonts-final-decision-sheet.md` | 13 | `\| Final source commit \| `PENDING_FINAL_40_CHARACTER_COMMIT` \| TBD \| `documentation/google-fonts-downstream-metadata-draft.md`, Add Font issue/PR text \|` |
| pending confirmation | `documentation/google-fonts-final-decision-sheet.md` | 14 | `\| Public upstream URL \| `https://github.com/eliheuer/blocksyncer` \| Confirm or replace \| metadata draft, `OFL.txt`, generated name ID 0 policy, Add Font issue \|` |
| pending confirmation | `documentation/google-fonts-final-decision-sheet.md` | 15 | `\| Public default branch \| `main` \| Confirm or replace \| metadata draft \|` |
| pending confirmation | `documentation/google-fonts-final-decision-sheet.md` | 18 | `\| Designer string \| `Eli Heuer` \| Confirm or replace \| metadata draft, issue, profile text \|` |
| pending maintainer answer | `documentation/google-fonts-final-decision-sheet.md` | 19 | `\| AI-use disclosure \| pending maintainer answer \| Confirm wording \| Add Font issue, maintainer notes \|` |
| pending proof review | `documentation/google-fonts-final-decision-sheet.md` | 27 | `\| Visual proof \| `make proof` writes `out/proof/index.html` with 73 proof pages and 19 fonts \| Maintainer review required \|` |
| pending review decision | `documentation/google-fonts-final-decision-sheet.md` | 28 | `\| Generated Latin Extended and Vietnamese composites \| Added to clear coverage/subset gates; documented as review glyphs \| Accept, revise, or defer \|` |
| pending packaging fallback decision | `documentation/google-fonts-final-decision-sheet.md` | 30 | `\| Release/archive fallback \| `dist/Blocksync-GF-review.zip` is built by `make release-check` and tracked in `documentation/release-archive-manifest.md` \| Use only if Google Fonts rejects `source.config_yaml` path \|` |
| pending date_added | `documentation/google-fonts-submission-handoff.md` | 23 | `- Current metadata blockers: `date_added` is `PENDING-YYYY-MM-DD` and` |
| pending source commit | `documentation/google-fonts-submission-handoff.md` | 24 | ``source.commit` is `PENDING_FINAL_40_CHARACTER_COMMIT`` |
| PR template placeholder | `documentation/google-fonts-submission-handoff.md` | 207 | ``Taken from the upstream repo <repo-url> at commit <commit-url>.`` |
| pending source commit | `documentation/google-fonts-submission-handoff.md` | 223 | `commit: "PENDING_FINAL_40_CHARACTER_COMMIT"` |

## Public Blockers By Kind

- PR template placeholder: 2
- pending confirmation: 3
- pending date_added: 3
- pending maintainer answer: 1
- pending packaging fallback decision: 1
- pending proof review: 1
- pending review decision: 1
- pending source commit: 5

## Internal Guards

These strings intentionally remain in guard scripts so stale or
incomplete metadata cannot reach Packager.

| Kind | File | Line | Text |
| --- | --- | ---: | --- |
| internal metadata guard | `scripts/package_gf_dry_run.sh` | 32 | `if grep -q 'PENDING-YYYY-MM-DD\\|PENDING_FINAL_40_CHARACTER_COMMIT' "$METADATA_DRAFT"; then` |

## Generated Evidence Echoes

| Kind | File | Line | Text |
| --- | --- | ---: | --- |
| pending confirmation | `documentation/authorship-disclosure-readiness.md` | 27 | `- Designer string: Confirm or replace` |
| pending confirmation | `documentation/authorship-disclosure-readiness.md` | 28 | `- AI-use disclosure: Confirm wording` |
| pending date_added | `documentation/decision-application-blockers.md` | 29 | `\| Google Fonts `date_added` \| TBD \| blocks \| blocks \| blocks \| `PENDING-YYYY-MM-DD` still present \| `documentation/google-fonts-downstream-metadata-draft.md` \|` |
| pending source commit | `documentation/decision-application-blockers.md` | 30 | `\| Final source commit \| TBD \| blocks \| blocks \| blocks \| `PENDING_FINAL_40_CHARACTER_COMMIT` still present \| `documentation/google-fonts-downstream-metadata-draft.md`, Add Font issue/PR text \|` |
| pending confirmation | `documentation/decision-application-blockers.md` | 31 | `\| Public upstream URL \| Confirm or replace \| blocks until confirmed \| blocks if changed \| blocks issue/PR text if changed \| unresolved final answer \| metadata draft, `OFL.txt`, generated name ID 0 policy, Add Font issue \|` |
| pending confirmation | `documentation/decision-application-blockers.md` | 32 | `\| Public default branch \| Confirm or replace \| blocks until confirmed \| blocks if changed \| blocks issue/PR text if changed \| unresolved final answer \| metadata draft \|` |
| pending confirmation | `documentation/decision-application-blockers.md` | 35 | `\| Designer string \| Confirm or replace \| blocks if changed \| does not block directly \| blocks Add Font issue \| unresolved final answer \| metadata draft, issue, profile text \|` |
| pending confirmation | `documentation/decision-application-blockers.md` | 36 | `\| AI-use disclosure \| Confirm wording \| does not block \| does not block directly \| blocks Add Font issue \| unresolved final answer \| Add Font issue, maintainer notes \|` |
| pending proof review | `documentation/decision-application-blockers.md` | 39 | `\| Visual proof \| Maintainer review required \| does not block \| does not block directly \| blocks review confidence \| maintainer proof review not recorded \| review log / handoff docs \|` |
| pending review decision | `documentation/decision-application-blockers.md` | 40 | `\| Generated Latin Extended and Vietnamese composites \| Accept, revise, or defer \| does not block \| blocks if source cleanup chosen \| blocks if review glyphs are not accepted/deferred \| unresolved final answer \| review log / handoff docs \|` |
| pending packaging fallback decision | `documentation/decision-application-blockers.md` | 42 | `\| Release/archive fallback \| Use only if Google Fonts rejects `source.config_yaml` path \| does not block \| blocks only if release/archive strategy is selected \| blocks only if release/archive strategy is selected \| pending \| review log / handoff docs \|` |
| PR template placeholder | `documentation/downstream-pr-readiness.md` | 14 | `- Expected PR body provenance line: `Taken from the upstream repo <repo-url> at commit <commit-url>.`` |
| pending date_added | `documentation/final-readiness-report.md` | 15 | `- metadata `date_added` is still `PENDING-YYYY-MM-DD`` |
| pending maintainer answer | `documentation/final-readiness-report.md` | 17 | `- AI-use disclosure is still pending maintainer answer` |
| pending date_added | `documentation/final-submission-blockers.md` | 14 | `\| Release metadata \| date_added: `PENDING-YYYY-MM-DD`; commit: `PENDING_FINAL_40_CHARACTER_COMMIT`; current HEAD: `eadeb6a445d79cd79e5d6365dc782744db11a75f`; working tree clean: no \| Commit the reviewed release tree and apply final package date/source commit \|` |
| pending date_added | `documentation/final-submission-blockers.md` | 28 | `- metadata `date_added` is still `PENDING-YYYY-MM-DD`` |
| pending maintainer answer | `documentation/final-submission-blockers.md` | 30 | `- AI-use disclosure is still pending maintainer answer` |
| pending date_added | `documentation/final-submission-blockers.md` | 43 | `\| Google Fonts `date_added` \| `PENDING-YYYY-MM-DD` \| TBD \|` |
| pending source commit | `documentation/final-submission-blockers.md` | 44 | `\| Final source commit \| `PENDING_FINAL_40_CHARACTER_COMMIT` \| TBD \|` |
| pending confirmation | `documentation/final-submission-blockers.md` | 45 | `\| Public upstream URL \| `https://github.com/eliheuer/blocksyncer` \| Confirm or replace \|` |
| pending confirmation | `documentation/final-submission-blockers.md` | 46 | `\| Public default branch \| `main` \| Confirm or replace \|` |
| pending confirmation | `documentation/final-submission-blockers.md` | 49 | `\| Designer string \| `Eli Heuer` \| Confirm or replace \|` |
| pending maintainer answer | `documentation/final-submission-blockers.md` | 50 | `\| AI-use disclosure \| pending maintainer answer \| Confirm wording \|` |
| pending proof review | `documentation/final-submission-blockers.md` | 53 | `\| Visual proof \| `make proof` writes `out/proof/index.html` with 73 proof pages and 19 fonts \| Maintainer review required \|` |
| pending review decision | `documentation/final-submission-blockers.md` | 54 | `\| Generated Latin Extended and Vietnamese composites \| Added to clear coverage/subset gates; documented as review glyphs \| Accept, revise, or defer \|` |
| pending packaging fallback decision | `documentation/final-submission-blockers.md` | 56 | `\| Release/archive fallback \| `dist/Blocksync-GF-review.zip` is built by `make release-check` and tracked in `documentation/release-archive-manifest.md` \| Use only if Google Fonts rejects `source.config_yaml` path \|` |
| pending date_added | `documentation/google-fonts-final-values-packet.md` | 28 | `\| Google Fonts `date_added` \| `PENDING-YYYY-MM-DD` \| TBD \| `date_added` \| `YYYY-MM-DD` \| Use the final Google Fonts package date in YYYY-MM-DD form. \|` |
| pending source commit | `documentation/google-fonts-final-values-packet.md` | 29 | `\| Final source commit \| `PENDING_FINAL_40_CHARACTER_COMMIT` \| TBD \| `source_commit` \| `40_CHARACTER_FINAL_COMMIT_HASH` \| Use the reviewed final public upstream commit hash. \|` |
| pending confirmation | `documentation/google-fonts-final-values-packet.md` | 30 | `\| Public upstream URL \| `https://github.com/eliheuer/blocksyncer` \| Confirm or replace \| `repository_url` \| `https://github.com/eliheuer/blocksyncer` \| Use the final public GitHub upstream URL. \|` |
| pending confirmation | `documentation/google-fonts-final-values-packet.md` | 31 | `\| Public default branch \| `main` \| Confirm or replace \| `branch` \| `main` \| Use a simple git branch name, usually main. \|` |
| pending confirmation | `documentation/google-fonts-final-values-packet.md` | 34 | `\| Designer string \| `Eli Heuer` \| Confirm or replace \| `designer` \| `Eli Heuer` \| Use the final metadata designer string. \|` |
| pending maintainer answer | `documentation/google-fonts-final-values-packet.md` | 35 | `\| AI-use disclosure \| pending maintainer answer \| Confirm wording \| `ai_use_disclosure` \| `FINAL_AI_USE_DISCLOSURE` \| Record maintainer-approved AI-use wording. \|` |
| pending proof review | `documentation/google-fonts-final-values-packet.md` | 38 | `\| Visual proof \| `make proof` writes `out/proof/index.html` with 73 proof pages and 19 fonts \| Maintainer review required \| `visual_proof_decision` \| `FINAL_VISUAL_PROOF_DECISION` \| Record proof review status. \|` |
| pending review decision | `documentation/google-fonts-final-values-packet.md` | 39 | `\| Generated Latin Extended and Vietnamese composites \| Added to clear coverage/subset gates; documented as review glyphs \| Accept, revise, or defer \| `generated_composites_decision` \| `FINAL_GENERATED_COMPOSITES_DECISION` \| Accept, revise, or defer generated composites. \|` |
| pending packaging fallback decision | `documentation/google-fonts-final-values-packet.md` | 41 | `\| Release/archive fallback \| `dist/Blocksync-GF-review.zip` is built by `make release-check` and tracked in `documentation/release-archive-manifest.md` \| Use only if Google Fonts rejects `source.config_yaml` path \| `release_archive_fallback_decision` \| `FINAL_RELEASE_ARCHIVE_FALLBACK_DECISION` \| Confirm fallback policy. \|` |
| pending date_added | `documentation/google-fonts-final-values-packet.md` | 67 | `- metadata `date_added` is still `PENDING-YYYY-MM-DD`` |
| pending maintainer answer | `documentation/google-fonts-final-values-packet.md` | 69 | `- AI-use disclosure is still pending maintainer answer` |
| pending review decision | `documentation/google-fonts-maintainer-decision-request.md` | 31 | `\| `generated_composites_decision` \|  \| yes \| Accept, revise, or defer generated composites. \|` |
| pending date_added | `documentation/google-fonts-maintainer-decision-request.md` | 80 | `- metadata `date_added` is still `PENDING-YYYY-MM-DD`` |
| pending maintainer answer | `documentation/google-fonts-maintainer-decision-request.md` | 82 | `- AI-use disclosure is still pending maintainer answer` |
| pending date_added | `documentation/next-actions.md` | 33 | `\| Google Fonts `date_added` \| `PENDING-YYYY-MM-DD` \| TBD \|` |
| pending source commit | `documentation/next-actions.md` | 34 | `\| Final source commit \| `PENDING_FINAL_40_CHARACTER_COMMIT` \| TBD \|` |
| pending confirmation | `documentation/next-actions.md` | 35 | `\| Public upstream URL \| `https://github.com/eliheuer/blocksyncer` \| Confirm or replace \|` |
| pending confirmation | `documentation/next-actions.md` | 36 | `\| Public default branch \| `main` \| Confirm or replace \|` |
| pending confirmation | `documentation/next-actions.md` | 38 | `\| Designer string \| `Eli Heuer` \| Confirm or replace \|` |
| pending maintainer answer | `documentation/next-actions.md` | 39 | `\| AI-use disclosure \| pending maintainer answer \| Confirm wording \|` |
| pending proof review | `documentation/next-actions.md` | 42 | `\| Visual proof \| `make proof` writes `out/proof/index.html` with 73 proof pages and 19 fonts \| Maintainer review required \|` |
| pending review decision | `documentation/next-actions.md` | 43 | `\| Generated Latin Extended and Vietnamese composites \| Added to clear coverage/subset gates; documented as review glyphs \| Accept, revise, or defer \|` |
| pending packaging fallback decision | `documentation/next-actions.md` | 45 | `\| Release/archive fallback \| `dist/Blocksync-GF-review.zip` is built by `make release-check` and tracked in `documentation/release-archive-manifest.md` \| Use only if Google Fonts rejects `source.config_yaml` path \|` |
| pending date_added | `documentation/next-actions.md` | 51 | `\| metadata `date_added` is still `PENDING-YYYY-MM-DD` \| Choose the final Google Fonts package date, then update the metadata draft. \|` |
| pending maintainer answer | `documentation/next-actions.md` | 53 | `\| AI-use disclosure is still pending maintainer answer \| Record the maintainer-approved AI-use disclosure wording. \|` |
| pending review decision | `documentation/next-actions.md` | 62 | `\| generated composite review glyphs are not finally accepted/revised/deferred \| Accept, revise, or defer the generated Latin Extended and Vietnamese review glyphs. \|` |
| pending proof review | `documentation/proof-review-packet.md` | 22 | `\| Visual proof \| Maintainer review required \| `visual_proof_decision` \|` |
| pending review decision | `documentation/proof-review-packet.md` | 23 | `\| Generated Latin Extended and Vietnamese composites \| Accept, revise, or defer \| `generated_composites_decision` \|` |
| pending proof review | `documentation/proof-review-readiness.md` | 36 | `- Visual proof: Maintainer review required` |
| pending review decision | `documentation/proof-review-readiness.md` | 37 | `- Generated Latin Extended and Vietnamese composites: Accept, revise, or defer` |
| pending date_added | `documentation/submission-handoff-readiness.md` | 15 | `- Current `date_added`: `PENDING-YYYY-MM-DD`` |
| pending source commit | `documentation/submission-handoff-readiness.md` | 16 | `- Current source commit: `PENDING_FINAL_40_CHARACTER_COMMIT`` |

## Apply Before Final Packaging

- Replace `date_added` and `source.commit` placeholders after the final
  source state is reviewed.
- Replace PR provenance placeholders after the Google Fonts issue and
  final upstream commit URL are known.
- Resolve maintainer answer markers in the final decision sheet, issue
  draft, metadata draft, and handoff document.
- Regenerate this report with `make placeholder-audit` after applying
  decisions.
