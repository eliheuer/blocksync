# Google Fonts Maintainer Decision Request

This generated request is the shortest handoff surface for the final
human decisions that automation cannot invent. Fill the blank values,
review the proposed values, then validate a private JSON copy before
applying anything to release drafts.

## Summary

- Maintainer decision request ready: yes
- Final values packet ready: yes
- Current final-readiness blockers: 6
- Public placeholder blocker count: 1
- Remaining Fontspector warning floor: `googlefonts/metadata/unreachable_subsetting`: 1, `contour_count`: 1, `outline_alignment_miss`: 1

## Required Answers

| JSON key | Proposed value from local evidence | Needs maintainer answer | Prompt |
| --- | --- | --- | --- |
| `date_added` | 2026-11-18 | review | Final Google Fonts package date, YYYY-MM-DD. |
| `source_commit` | 46cd53e51744630b4f92e2a2e5957b41e6bd9294 | review | Final reviewed public upstream commit hash. |
| `repository_url` | https://github.com/eliheuer/blocksync | review | Final public GitHub upstream URL. |
| `branch` | main | review | Final public source branch. |
| `designer` | Eli Heuer | review | Final metadata designer string. |
| `package_source_strategy` | config_yaml | review | Use config_yaml unless archive packaging is chosen. |
| `namecheck_result` | namecheck.fontdata.com API clear on 2026-11-18: zero matches at confidence 0.3-1.0 and trademark=false | review | Final namecheck.fontdata.com clearance statement. |
| `ai_use_disclosure` | AI tools assisted with build and CI configuration, documentation, QA, proof comparison and draft component construction. In this release, the quarter and three-quarter fractions use Blocksync’s existing numeral and slash drawings. Eli selected the heavier normal-width Black from rendered alternatives. The build interpolates the heavier styles from existing masters. New OpenType positioning and a combining macron below support accent sequences. The sources include Latin Extended and Vietnamese composites assembled by project scripts. The maintainer confirmed that this disclosure also covers earlier work. | review | Maintainer-approved AI-use disclosure wording. |
| `authorship_cla_rfn_status` | AUTHORS.txt: Eli Heuer; CONTRIBUTORS.txt: Eli Heuer; OFL declares no project-specific Reserved Font Names. CLA identity remains a maintainer-only final check before submission. | review | Final authorship, CLA identity, and RFN status. |
| `fontspector_warning_decision` |  | yes | Accept current WARN floor or require source cleanup. |
| `visual_proof_decision` |  | yes | Final proof review disposition. |
| `generated_composites_decision` |  | yes | Accept, revise, or defer generated composites. |
| `static_ttf_decision` | Keep static TTFs as local proof outputs only unless Google Fonts asks for downstream static files. | review | Confirm statics are proof-only unless requested. |
| `release_archive_fallback_decision` | Use source.config_yaml with sources/config.yaml for first submission; release/archive fallback remains available with local archive hashes match: yes. | review | Confirm archive fallback policy. |

## Optional Answers

| JSON key | Proposed value from local evidence | Needs maintainer answer | Prompt |
| --- | --- | --- | --- |
| `archive_url` |  | conditional | Required only when package_source_strategy is archive. |
| `google_fonts_issue_url` |  | conditional | Fill after the Add Font issue exists. |

## Copyable JSON Starting Point

This block intentionally omits proposal-only `_...` keys. Save it as a
private values file, replace blanks and any non-final wording, then run
the validation command below.

```json
{
  "date_added": "2026-11-18",
  "source_commit": "46cd53e51744630b4f92e2a2e5957b41e6bd9294",
  "repository_url": "https://github.com/eliheuer/blocksync",
  "branch": "main",
  "designer": "Eli Heuer",
  "package_source_strategy": "config_yaml",
  "namecheck_result": "namecheck.fontdata.com API clear on 2026-11-18: zero matches at confidence 0.3-1.0 and trademark=false",
  "ai_use_disclosure": "AI tools assisted with build and CI configuration, documentation, QA, proof comparison and draft component construction. In this release, the quarter and three-quarter fractions use Blocksync\u2019s existing numeral and slash drawings. Eli selected the heavier normal-width Black from rendered alternatives. The build interpolates the heavier styles from existing masters. New OpenType positioning and a combining macron below support accent sequences. The sources include Latin Extended and Vietnamese composites assembled by project scripts. The maintainer confirmed that this disclosure also covers earlier work.",
  "authorship_cla_rfn_status": "AUTHORS.txt: Eli Heuer; CONTRIBUTORS.txt: Eli Heuer; OFL declares no project-specific Reserved Font Names. CLA identity remains a maintainer-only final check before submission.",
  "fontspector_warning_decision": "",
  "visual_proof_decision": "",
  "generated_composites_decision": "",
  "static_ttf_decision": "Keep static TTFs as local proof outputs only unless Google Fonts asks for downstream static files.",
  "release_archive_fallback_decision": "Use source.config_yaml with sources/config.yaml for first submission; release/archive fallback remains available with local archive hashes match: yes.",
  "archive_url": "",
  "google_fonts_issue_url": ""
}
```

## Validation Commands

```bash
make final-values-check VALUES=/path/to/final-values.json
make apply-final-values VALUES=/path/to/final-values.json
make release-check
make final-readiness-check
```

## Current Final Blockers

- final decision sheet still has unresolved answer cells: 3
- package-context Fontspector report has FAIL/FATAL/ERROR results
- Fontspector warning floor is not resolved or accepted: release 3 WARN, package 3 WARN
- zero-warning worklist says true zero is not currently achieved
- generated composite review glyphs are not finally accepted/revised/deferred
- downstream Google Fonts PR readiness is not complete

Regenerate this request with `make maintainer-decision-request` after
running `make release-check`, proof review, or final-value changes.
