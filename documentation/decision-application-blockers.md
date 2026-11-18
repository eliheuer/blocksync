# Decision Application Blockers

This generated report maps each remaining maintainer decision or
finalization item to the exact Google Fonts packaging gate it affects.
It is the apply surface after `documentation/google-fonts-final-decision-sheet.md`
is filled in.

## Summary

- Decision rows tracked: 14
- Unresolved final-answer rows: 13
- Unresolved row names: Google Fonts `date_added`, Final source commit, Public upstream URL, Public default branch, Package source strategy, Designer string, AI-use disclosure, Authorship/CLA/RFN status, Fontspector warning floor, Visual proof, Generated Latin Extended and Vietnamese composites, Static TTFs, Release/archive fallback
- Public placeholder blocker count: 17
- Metadata has pending date_added: yes
- Metadata has pending source.commit: yes
- Downstream metadata blocking decision rows: 7
- Package dry-run blocking decision rows: 9
- Downstream PR blocking decision rows: 14
- Package dry-run first blocker: google/fonts checkout has dirty paths outside ofl/blocksync
- Downstream PR first blocker: google/fonts checkout has dirty paths outside ofl/blocksync
- Final GitHub release archive URL recorded: pending
- Zero-warning possible with current scope: no
- Proof review local evidence ready: yes

## Blocker Map

| Item | Final answer | Downstream metadata | Package dry run | Downstream PR | Current blocker marker | Apply surfaces |
| --- | --- | --- | --- | --- | --- | --- |
| Google Fonts `date_added` | TBD | blocks | blocks | blocks | `PENDING-YYYY-MM-DD` still present | `documentation/google-fonts-downstream-metadata-draft.md` |
| Final source commit | TBD | blocks | blocks | blocks | `PENDING_FINAL_40_CHARACTER_COMMIT` still present | `documentation/google-fonts-downstream-metadata-draft.md`, Add Font issue/PR text |
| Public upstream URL | Confirm or replace | blocks until confirmed | blocks if changed | blocks issue/PR text if changed | unresolved final answer | metadata draft, `OFL.txt`, generated name ID 0 policy, Add Font issue |
| Public default branch | Confirm or replace | blocks until confirmed | blocks if changed | blocks issue/PR text if changed | unresolved final answer | metadata draft |
| Package source strategy | Confirm or switch to release/archive | blocks source block finalization | blocks source mode | blocks package provenance | release/archive fallback URL pending if selected | metadata draft, package preview, release archive manifest |
| Family name uniqueness | namecheck.fontdata.com API clear on 2026-05-30: zero matches at confidence 0.3-1.0 and trademark=false | does not block | does not block directly | blocks Add Font issue | answer recorded | Add Font issue, handoff docs |
| Designer string | Confirm or replace | blocks if changed | does not block directly | blocks Add Font issue | unresolved final answer | metadata draft, issue, profile text |
| AI-use disclosure | Confirm wording | does not block | does not block directly | blocks Add Font issue | unresolved final answer | Add Font issue, maintainer notes |
| Authorship/CLA/RFN status | Confirm | blocks if changed | does not block directly | blocks Add Font issue | unresolved final answer | Add Font issue, downstream PR |
| Fontspector warning floor | Accept for first review or schedule source cleanup | does not block | blocks only if not accepted or fixed | blocks warning rationale | `googlefonts/metadata/unreachable_subsetting`: 1, `contour_count`: 1, `outline_alignment_miss`: 1 | review log / handoff docs |
| Visual proof | Maintainer review required | does not block | does not block directly | blocks review confidence | maintainer proof review not recorded | review log / handoff docs |
| Generated Latin Extended and Vietnamese composites | Accept, revise, or defer | does not block | blocks if source cleanup chosen | blocks if review glyphs are not accepted/deferred | unresolved final answer | review log / handoff docs |
| Static TTFs | Keep proof-only unless Google Fonts asks | does not block | blocks only if Google Fonts asks for static files | blocks only if package file list changes | unresolved final answer | review log / handoff docs |
| Release/archive fallback | Use only if Google Fonts rejects `source.config_yaml` path | does not block | blocks only if release/archive strategy is selected | blocks only if release/archive strategy is selected | pending | review log / handoff docs |

## Apply Order

1. Fill every unresolved final-answer cell in `documentation/google-fonts-final-decision-sheet.md`.
2. Apply final `date_added`, `source.commit`, branch, designer, and package source decisions to `documentation/google-fonts-downstream-metadata-draft.md`.
3. Apply namecheck, authorship, AI-use, warning-floor, proof, and composite-review decisions to the Add Font issue draft and handoff docs.
4. If release/archive packaging is selected, publish the archive and record the final `source.archive_url`.
5. Rerun `make release-check`, `make placeholder-audit`, `make decision-application-check`, and `make final-readiness-check`.
