# /google-fonts-finalize

Apply final maintainer decisions and verify a Google Fonts submission handoff.

## Usage

`/google-fonts-finalize [decisions|metadata|issue|verify|all]`

Default: `all`

## Inputs

Read these first:

- `documentation/google-fonts-final-decision-sheet.md`
- `documentation/google-fonts-final-values-packet.md`
- `documentation/google-fonts-final-values.proposal.json`
- `documentation/google-fonts-maintainer-decision-request.md`
- `documentation/google-fonts-downstream-metadata-draft.md`
- `documentation/google-fonts-add-font-issue-draft.md`
- `documentation/google-fonts-submission-handoff.md`
- `documentation/submission-handoff-readiness.md`
- `documentation/final-submission-blockers.md`
- `documentation/source-readiness.md`
- `documentation/release-metadata-readiness.md`
- `documentation/family-name-readiness.md`
- `documentation/authorship-disclosure-readiness.md`
- `documentation/packager-source-strategy.md`
- `documentation/proof-review-readiness.md`
- `documentation/proof-review-packet.md`
- `documentation/open-placeholder-audit.md`
- `documentation/decision-application-blockers.md`

## Instructions

1. Confirm every row in the final decision sheet has a maintainer answer.
2. Apply final values to downstream metadata:
   - `date_added`
   - `source.commit`
   - public branch and repository URL if changed
   - `source.archive_url` only if release/archive packaging is selected
3. Prefer using the final values helper:

   ```bash
   make final-values-packet
   make final-values-proposal
   make maintainer-decision-request
   make final-values-check VALUES=/path/to/final-values.json
   make apply-final-values VALUES=/path/to/final-values.json
   ```

   The values file should be a filled copy of
   `documentation/google-fonts-final-values.template.json`, or a reviewed copy
   of `documentation/google-fonts-final-values.proposal.json` with
   proposal-only `_...` keys removed; use
   `documentation/google-fonts-final-values-packet.md` to verify every
   decision row maps to a JSON key before applying. If the Add Font issue
   already exists, include `google_fonts_issue_url` so downstream PR readiness
   can verify the issue-first rule. The helper also aligns `OFL.txt` and
   active UFO `fontinfo.plist` copyright URLs with the final public upstream
   URL so generated name ID 0 stays consistent.
4. Update the Add Font issue draft so draft-status notes are replaced with
   final confirmed statements.
5. Update the submission handoff and blockers snapshot.
6. Run:

   ```bash
   make release-metadata-readiness
   make source-readiness
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
   make release-check
   make proof
   make prepare-gf-clean-checkout
   make package-dry-run-readiness
   make packager-dry-run-record
   make downstream-pr-draft
   make downstream-pr-readiness
   make submission-handoff-readiness
   make final-readiness-check
   ```

7. If packaging is release/archive based, verify
   `documentation/release-archive-manifest.md` reports matching source hashes
   and deterministic metadata.
8. Do not mark release complete while metadata placeholders, unresolved
   maintainer disclosures, unreviewed proof output, or unaccepted Fontspector
   WARNs remain.

## Completion Criteria

The family is locally final only when:

- `make release-check` passes;
- `make source-readiness` confirms the active build path is designspace/UFO
  and historical `.glyphs` snapshots are archived;
- `make proof` has been regenerated after the latest source/build change;
- `make proof-review-packet` reports the maintainer proof/WARN review packet
  is ready;
- `make final-readiness-check` passes;
- downstream metadata has no placeholders;
- namecheck, authorship, AI-use disclosure, RFN/CLA status, and package source
  strategy are confirmed;
- `make package-dry-run-readiness` reports ready and the guarded no-PR
  Packager run has been reviewed, using
  `GF_REPO_PATH=/private/tmp/blocksync-google-fonts` if the shared
  `google/fonts` fork has unrelated dirty work;
- `make packager-dry-run-record` reports that the final no-PR Packager run is
  recorded against the current metadata draft;
- `make downstream-pr-draft` contains a final provenance line with the upstream
  repo and commit URL;
- `make submission-handoff-readiness` reports the Add Font issue draft and
  handoff are synchronized with the current generated reports;
- `make downstream-pr-readiness` reports ready before a downstream PR is
  opened;
- remaining Fontspector WARNs are either fixed or explicitly accepted for
  first Google Fonts review.
