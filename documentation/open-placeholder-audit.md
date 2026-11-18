# Open Placeholder Audit

This generated report tracks unresolved Google Fonts handoff strings
that still need a maintainer answer, final metadata value, or external
confirmation. Generated reports are separated from public application
surfaces so echoed blockers do not look like new work.

## Summary

- Public placeholder blocker count: 1
- Pending date_added occurrences: 0
- Pending source commit occurrences: 0
- TBD markers: 0
- PR template placeholders: 2
- Pending maintainer-answer markers: 3
- Pending confirmation markers: 0
- Pending proof-review markers: 0
- Pending review-decision markers: 3
- Internal metadata guard markers: 1
- Generated evidence echoes: 7

## Public Blockers

| Kind | File | Line | Text |
| --- | --- | ---: | --- |
| PR template placeholder | `documentation/google-fonts-submission-handoff.md` | 18 | `The issue text and maintainer confirmations are in `documentation/google-fonts-add-font-issue-draft.md` and `documentation/google-fonts-final-decision-sheet.md`. Google Fonts reviews the issue before requesting a downstream PR. The expected branch is `gftools_packager_ofl_blocksync` and the title is `Blocksync : 1.000 added`. The PR template uses `Taken from the upstream repo <repo-url> at commit <commit-url>.`` |

## Public Blockers By Kind

- PR template placeholder: 1

## Internal Guards

These strings intentionally remain in guard scripts so stale or
incomplete metadata cannot reach Packager.

| Kind | File | Line | Text |
| --- | --- | ---: | --- |
| internal metadata guard | `scripts/package_gf_dry_run.sh` | 32 | `if grep -q 'PENDING-YYYY-MM-DD\\|PENDING_FINAL_40_CHARACTER_COMMIT' "$METADATA_DRAFT"; then` |

## Generated Evidence Echoes

| Kind | File | Line | Text |
| --- | --- | ---: | --- |
| PR template placeholder | `documentation/downstream-pr-readiness.md` | 14 | `- Expected PR body provenance line: `Taken from the upstream repo <repo-url> at commit <commit-url>.`` |
| pending maintainer answer | `documentation/final-submission-blockers.md` | 28 | `- AI-use disclosure is still pending maintainer answer` |
| pending review decision | `documentation/google-fonts-final-values-packet.md` | 39 | `\| Generated Latin Extended and Vietnamese composites \| Added to clear coverage/subset gates; documented as review glyphs \| Pending design review. Hold the submission until the placeholder identities and accent constructions have been reviewed. \| `generated_composites_decision` \| `FINAL_GENERATED_COMPOSITES_DECISION` \| Accept, revise, or defer generated composites. \|` |
| pending maintainer answer | `documentation/google-fonts-final-values-packet.md` | 67 | `- AI-use disclosure is still pending maintainer answer` |
| pending review decision | `documentation/google-fonts-maintainer-decision-request.md` | 31 | `\| `generated_composites_decision` \|  \| yes \| Accept, revise, or defer generated composites. \|` |
| pending maintainer answer | `documentation/next-actions.md` | 41 | `\| AI-use disclosure is still pending maintainer answer \| Record the maintainer-approved AI-use disclosure wording. \|` |
| pending review decision | `documentation/next-actions.md` | 49 | `\| generated composite review glyphs are not finally accepted/revised/deferred \| Accept, revise, or defer the generated Latin Extended and Vietnamese review glyphs. \|` |

## Apply Before Final Packaging

- Replace `date_added` and `source.commit` placeholders after the final
  source state is reviewed.
- Replace PR provenance placeholders after the Google Fonts issue and
  final upstream commit URL are known.
- Resolve maintainer answer markers in the final decision sheet, issue
  draft, metadata draft, and handoff document.
- Regenerate this report with `make placeholder-audit` after applying
  decisions.
