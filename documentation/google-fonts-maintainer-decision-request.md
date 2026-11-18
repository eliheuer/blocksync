# Google Fonts Maintainer Decision Request

This generated request is the shortest handoff surface for the final
human decisions that automation cannot invent. Fill the blank values,
review the proposed values, then validate a private JSON copy before
applying anything to release drafts.

## Summary

- Maintainer decision request ready: yes
- Final values packet ready: yes
- Current final-readiness blockers: 10
- Public placeholder blocker count: 17
- Remaining Fontspector warning floor: `googlefonts/metadata/unreachable_subsetting`: 1, `contour_count`: 1, `outline_alignment_miss`: 1

## Required Answers

| JSON key | Proposed value from local evidence | Needs maintainer answer | Prompt |
| --- | --- | --- | --- |
| `date_added` |  | yes | Final Google Fonts package date, YYYY-MM-DD. |
| `source_commit` |  | yes | Final reviewed public upstream commit hash. |
| `repository_url` | https://github.com/eliheuer/blocksyncer | review | Final public GitHub upstream URL. |
| `branch` | main | review | Final public source branch. |
| `designer` | Eli Heuer | review | Final metadata designer string. |
| `package_source_strategy` | config_yaml | review | Use config_yaml unless archive packaging is chosen. |
| `namecheck_result` | namecheck.fontdata.com API clear on 2026-05-30: zero matches at confidence 0.3-1.0 and trademark=false | review | Final namecheck.fontdata.com clearance statement. |
| `ai_use_disclosure` |  | yes | Maintainer-approved AI-use disclosure wording. |
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
  "date_added": "",
  "source_commit": "",
  "repository_url": "https://github.com/eliheuer/blocksyncer",
  "branch": "main",
  "designer": "Eli Heuer",
  "package_source_strategy": "config_yaml",
  "namecheck_result": "namecheck.fontdata.com API clear on 2026-05-30: zero matches at confidence 0.3-1.0 and trademark=false",
  "ai_use_disclosure": "",
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

Regenerate this request with `make maintainer-decision-request` after
running `make release-check`, proof review, or final-value changes.
