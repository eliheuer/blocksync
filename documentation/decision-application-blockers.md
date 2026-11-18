# Decision Application Blockers

This generated report maps each remaining maintainer decision or
finalization item to the exact Google Fonts packaging gate it affects.
It is the apply surface after `documentation/google-fonts-final-decision-sheet.md`
is filled in.

## Summary

- Decision rows tracked: 14
- Unresolved final-answer rows: 3
- Unresolved row names: Authorship/CLA/RFN status, Fontspector warning floor, Generated Latin Extended and Vietnamese composites
- Public placeholder blocker count: 1
- Metadata has pending date_added: no
- Metadata has pending source.commit: no
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
| Google Fonts `date_added` | 2026-11-18 | blocks | blocks | blocks | answer recorded | `documentation/google-fonts-downstream-metadata-draft.md` |
| Final source commit | 46cd53e51744630b4f92e2a2e5957b41e6bd9294 | blocks | blocks | blocks | answer recorded | `documentation/google-fonts-downstream-metadata-draft.md`, Add Font issue/PR text |
| Public upstream URL | https://github.com/eliheuer/blocksync | blocks until confirmed | blocks if changed | blocks issue/PR text if changed | answer recorded | metadata draft, `OFL.txt`, generated name ID 0 policy, Add Font issue |
| Public default branch | main | blocks until confirmed | blocks if changed | blocks issue/PR text if changed | answer recorded | metadata draft |
| Package source strategy | Build from source with `source.config_yaml` pointing to `sources/config.yaml` | blocks source block finalization | blocks source mode | blocks package provenance | release/archive fallback URL pending if selected | metadata draft, package preview, release archive manifest |
| Family name uniqueness | namecheck.fontdata.com API clear on 2026-11-18: zero matches at confidence 0.3-1.0 and trademark=false | does not block | does not block directly | blocks Add Font issue | answer recorded | Add Font issue, handoff docs |
| Designer string | Eli Heuer | blocks if changed | does not block directly | blocks Add Font issue | answer recorded | metadata draft, issue, profile text |
| AI-use disclosure | Eli confirmed the issue disclosure covers earlier work, engineering, components, mark positioning, QA and proof review. | does not block | does not block directly | blocks Add Font issue | answer recorded | Add Font issue, maintainer notes |
| Authorship/CLA/RFN status | Pending confirmation of the downstream contributor’s CLA identity | blocks if changed | does not block directly | blocks Add Font issue | unresolved final answer | Add Font issue, downstream PR |
| Fontspector warning floor | Accept for first review or schedule source cleanup | does not block | blocks only if not accepted or fixed | blocks warning rationale | `googlefonts/metadata/unreachable_subsetting`: 1, `contour_count`: 1, `outline_alignment_miss`: 1 | review log / handoff docs |
| Visual proof | Eli approved the heavier normal-width Black after a side-by-side proof. Independent checks cover weight, width, fractions, mark stacks and the complete language specimens. | does not block | does not block directly | blocks review confidence | maintainer proof review not recorded | review log / handoff docs |
| Generated Latin Extended and Vietnamese composites | Pending design review. Hold the submission until the placeholder identities and accent constructions have been reviewed. | does not block | blocks if source cleanup chosen | blocks if review glyphs are not accepted/deferred | unresolved final answer | review log / handoff docs |
| Static TTFs | Ship the variable TTF. Keep all 18 static instances for proofs. | does not block | blocks only if Google Fonts asks for static files | blocks only if package file list changes | answer recorded | review log / handoff docs |
| Release/archive fallback | Use source.config_yaml. Keep the verified ZIP for a requested fallback. | does not block | blocks only if release/archive strategy is selected | blocks only if release/archive strategy is selected | pending | review log / handoff docs |

## Apply Order

1. Fill every unresolved final-answer cell in `documentation/google-fonts-final-decision-sheet.md`.
2. Apply final `date_added`, `source.commit`, branch, designer, and package source decisions to `documentation/google-fonts-downstream-metadata-draft.md`.
3. Apply namecheck, authorship, AI-use, warning-floor, proof, and composite-review decisions to the Add Font issue draft and handoff docs.
4. If release/archive packaging is selected, publish the archive and record the final `source.archive_url`.
5. Rerun `make release-check`, `make placeholder-audit`, `make decision-application-check`, and `make final-readiness-check`.
