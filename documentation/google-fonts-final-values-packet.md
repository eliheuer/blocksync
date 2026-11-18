# Google Fonts Final Values Packet

This generated packet maps the maintainer decision sheet to the JSON
values file consumed by `scripts/apply_final_values.py`.

## Summary

- Final values packet ready: yes
- Decision rows mapped to JSON keys: 14 / 14
- Required JSON keys present in template: 14 / 14
- Optional JSON keys present in template: 2 / 2
- Unknown template keys: 0
- Unmapped decision rows: 0

## Fill This File

1. Copy `documentation/google-fonts-final-values.template.json` to a
   scratch path outside the repo or to a private working file.
2. Replace every placeholder value.
3. Run `make final-values-check VALUES=/path/to/final-values.json`.
4. Run `make apply-final-values VALUES=/path/to/final-values.json` only
   after the dry-run validation passes.

## Decision To JSON Map

| Decision | Current evidence | Current final answer | JSON key | Template value | Note |
| --- | --- | --- | --- | --- | --- |
| Google Fonts `date_added` | Candidate package date | 2026-11-18 | `date_added` | `YYYY-MM-DD` | Use the final Google Fonts package date in YYYY-MM-DD form. |
| Final source commit | Packaged source revision | 46cd53e51744630b4f92e2a2e5957b41e6bd9294 | `source_commit` | `40_CHARACTER_FINAL_COMMIT_HASH` | Use the reviewed final public upstream commit hash. |
| Public upstream URL | Public GitHub repository | https://github.com/eliheuer/blocksync | `repository_url` | `https://github.com/eliheuer/blocksync` | Use the final public GitHub upstream URL. |
| Public default branch | GitHub default branch | main | `branch` | `main` | Use a simple git branch name, usually main. |
| Package source strategy | preferred `source.config_yaml: "sources/config.yaml"` | Build from source with `source.config_yaml` pointing to `sources/config.yaml` | `package_source_strategy` | `config_yaml` | Use config_yaml unless release/archive packaging is selected. |
| Family name uniqueness | `namecheck.fontdata.com` API clear on 2026-11-18 | namecheck.fontdata.com API clear on 2026-11-18: zero matches at confidence 0.3-1.0 and trademark=false | `namecheck_result` | `FINAL_NAMECHECK_RESULT` | Record final namecheck.fontdata.com clearance. |
| Designer string | AUTHORS.txt and OFL | Eli Heuer | `designer` | `Eli Heuer` | Use the final metadata designer string. |
| AI-use disclosure | AI-assisted engineering, component work, QA and independent proof review documented in the issue draft | Eli confirmed the issue disclosure covers earlier work, engineering, components, mark positioning, QA and proof review. | `ai_use_disclosure` | `FINAL_AI_USE_DISCLOSURE` | Record maintainer-approved AI-use wording. |
| Authorship/CLA/RFN status | Eli confirmed rights to all styles, the OFL, continued maintenance, the absence of an applicable upstream RFN, and agreement to the contribution requirements. | Pending confirmation of the downstream contributor’s CLA identity | `authorship_cla_rfn_status` | `FINAL_AUTHORSHIP_CLA_RFN_STATUS` | Record final authorship, CLA identity, and no-RFN status. |
| Fontspector warning floor | Release VF has three warnings. Package-context QA reports the missing web-subset mark. | Accept for first review or schedule source cleanup | `fontspector_warning_decision` | `FINAL_FONTSPECTOR_WARNING_DECISION` | Accept remaining warnings or describe scheduled cleanup. |
| Visual proof | 18-page print proof, two-axis HTML specimen and separate legacy proof bundle | Eli approved the heavier normal-width Black after a side-by-side proof. Independent checks cover weight, width, fractions, mark stacks and the complete language specimens. | `visual_proof_decision` | `FINAL_VISUAL_PROOF_DECISION` | Record proof review status. |
| Generated Latin Extended and Vietnamese composites | Added to clear coverage/subset gates; documented as review glyphs | Pending design review. Hold the submission until the placeholder identities and accent constructions have been reviewed. | `generated_composites_decision` | `FINAL_GENERATED_COMPOSITES_DECISION` | Accept, revise, or defer generated composites. |
| Static TTFs | Generated for local proofing, not listed as downstream package files | Ship the variable TTF. Keep all 18 static instances for proofs. | `static_ttf_decision` | `FINAL_STATIC_TTF_DECISION` | Confirm whether statics are proof-only. |
| Release/archive fallback | `dist/Blocksync-GF-review.zip` is built by `make release-check` and tracked in `documentation/release-archive-manifest.md` | Use source.config_yaml. Keep the verified ZIP for a requested fallback. | `release_archive_fallback_decision` | `FINAL_RELEASE_ARCHIVE_FALLBACK_DECISION` | Confirm fallback policy. |

## Optional Values

| JSON key | Template value | When needed |
| --- | --- | --- |
| `archive_url` | `` | Required only when package_source_strategy is archive. |
| `google_fonts_issue_url` | `` | Fill after the Add Font issue exists. |

## Validation Rules

- `date_added` must be `YYYY-MM-DD`.
- `source_commit` must be a lowercase 40-character git hash.
- `repository_url` must be a public GitHub HTTPS URL.
- `branch` must be a simple git branch name with no spaces, traversal, or ref metacharacters.
- `package_source_strategy` must be `config_yaml` or `archive`.
- `archive_url` is required when `package_source_strategy` is `archive`.
- `google_fonts_issue_url`, when present, must be a `google/fonts` issue URL.
- Values must not contain Markdown table pipe characters.

## Template Coverage Issues

- none

## Current Maintainer Blockers

- AI-use disclosure is still pending maintainer answer
- final decision sheet still has unresolved answer cells: 4
