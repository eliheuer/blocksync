# Google Fonts Agent Porting Manifest

This generated manifest is the low-token copy plan for moving the
Blocksync Google Fonts workflow into another font repository. It does
not make the next family release-ready by itself; it identifies the
portable files and the family-specific facts that must be replaced.

## Summary

- Porting manifest ready: yes
- Portable files present: 47 / 47
- Active source policy to preserve: designspace/UFO active sources, archived `.glyphs` snapshots.

## Copy First

- `.agents/`: yes
- `AGENTS.md`: yes
- `GF_READINESS.md`: yes
- `Makefile`: yes
- `requirements.in`: yes
- `build.sh`: yes
- `scripts/check_gf_fonts.sh`: yes
- `scripts/check_downstream_metadata.py`: yes
- `scripts/check_package_context.py`: yes
- `scripts/gf_preflight.py`: yes

## Reusable Report And Gate Helpers

- `scripts/apply_final_values.py`: yes
- `scripts/build_proof_index.py`: yes
- `scripts/build_release_archive.py`: yes
- `scripts/package_gf_dry_run.sh`: yes
- `scripts/prepare_clean_gf_checkout.sh`: yes
- `scripts/remove_unreachable_support_mark_unicodes.py`: yes
- `scripts/report_agent_porting_manifest.py`: yes
- `scripts/report_agent_reuse_readiness.py`: yes
- `scripts/report_authorship_disclosure_readiness.py`: yes
- `scripts/report_decision_application_blockers.py`: yes
- `scripts/report_downstream_pr_draft.py`: yes
- `scripts/report_downstream_pr_readiness.py`: yes
- `scripts/report_family_name_readiness.py`: yes
- `scripts/report_final_submission_blockers.py`: yes
- `scripts/report_final_values_packet.py`: yes
- `scripts/report_final_values_proposal.py`: yes
- `scripts/report_google_fonts_reference_refresh.py`: yes
- `scripts/report_maintainer_decision_request.py`: yes
- `scripts/report_next_actions.py`: yes
- `scripts/report_open_placeholders.py`: yes
- `scripts/report_package_dry_run_readiness.py`: yes
- `scripts/report_packager_dry_run_record.py`: yes
- `scripts/report_packager_source_strategy.py`: yes
- `scripts/report_proof_review_packet.py`: yes
- `scripts/report_proof_review_readiness.py`: yes
- `scripts/report_release_metadata_readiness.py`: yes
- `scripts/report_source_readiness.py`: yes
- `scripts/report_submission_handoff_readiness.py`: yes
- `scripts/report_zero_warning_worklist.py`: yes

## Reusable Script Tests

- `scripts/test_apply_final_values.py`: yes
- `scripts/test_agent_porting_manifest.py`: yes
- `scripts/test_downstream_pr_draft.py`: yes
- `scripts/test_final_values_packet.py`: yes
- `scripts/test_maintainer_decision_request.py`: yes
- `scripts/test_package_gf_dry_run_gates.sh`: yes
- `scripts/test_packager_dry_run_record.py`: yes
- `scripts/test_release_archive_gates.sh`: yes

## Replace In The Next Family

- Family name, package directory, and downstream metadata `name`.
- Public upstream URL, branch, source commit, and optional archive URL.
- Designer string, authorship files, CLA identity, RFN status, and AI-use disclosure.
- Active source paths, designspace filename, UFO master list, and build config.
- Variable axes, default instance, static instance list, and STAT expectations.
- First-submission subset/script scope, glyphset coverage targets, and sample text.
- Vendor ID, copyright year/project name, DESCRIPTION links, and Add Font issue text.
- Fontspector warning disposition, proof review decisions, and generated glyph review scope.

## Regenerate In The Next Family

```bash
make preflight-only
make source-readiness
make release-metadata-readiness
make family-name-readiness
make authorship-disclosure-readiness
make packager-source-strategy
make proof-review-readiness
make proof-review-packet
make placeholder-audit
make decision-application-check
make final-values-packet
make final-values-proposal
make maintainer-decision-request
make google-fonts-reference-refresh
make agent-porting-manifest
make agent-reuse-readiness
make release-check
```

## Final Porting Rule

Do not carry over Blocksync-generated release reports as evidence for
another family. Copy the workflow, replace family facts, regenerate
reports from that repo's current sources, then trust only the new
reports and command output.
