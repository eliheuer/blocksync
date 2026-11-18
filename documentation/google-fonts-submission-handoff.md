# Google Fonts Submission Handoff

This is the current handoff note for opening the Google Fonts Add Font issue
and preparing the downstream package.

## Current Status

- Upstream repo: `https://github.com/eliheuer/blocksyncer`
- Google Fonts issue: pending
- Family name: Blocksync
- Namecheck: `documentation/namecheck-fontdata-result.json` records a
  2026-05-30 `namecheck.fontdata.com` API clear result
- License: SIL Open Font License v1.1, no Reserved Font Names declared
- Source format: UFO masters plus `sources/Blocksync.designspace`
- Archived sources: historical `.glyphs` files in `sources/archive/`
- Build command: `make build`
- Release gate: `make release-check`
- Proof command: `make proof`
- Variable font: `fonts/variable/Blocksync[wdth,wght].ttf`
- Downstream subset draft: `latin`, `latin-ext`, `menu`, `vietnamese`
- Current Fontspector status: 0 FAIL, 0 ERROR, 0 FATAL, 3 WARN in both
  release variable and package-context checks
- Current metadata blockers: `date_added` is `PENDING-YYYY-MM-DD` and
  `source.commit` is `PENDING_FINAL_40_CHARACTER_COMMIT`
- Final readiness gate: `make final-readiness-check` currently reports
  blockers: 10
- Final decision sheet:
  `documentation/google-fonts-final-decision-sheet.md`
- Final values packet:
  `documentation/google-fonts-final-values-packet.md`
- Downstream package preview:
  `documentation/google-fonts-downstream-package-preview.md`
- Downstream PR readiness:
  `documentation/downstream-pr-readiness.md`
- Package dry-run readiness:
  `documentation/package-dry-run-readiness.md`
- Current next-actions queue:
  `documentation/next-actions.md`
- Final submission blocker snapshot:
  `documentation/final-submission-blockers.md`
- Fallback release/archive manifest:
  `documentation/release-archive-manifest.md`
- Google Fonts live-reference refresh:
  `documentation/google-fonts-reference-refresh.md`

## Draft Add Font Issue

Use `documentation/google-fonts-add-font-issue-draft.md` as the source of truth
for the issue body. Before pasting it, replace draft status notes that still
need maintainer confirmation:

- final public upstream URL and default branch;
- AI-use disclosure;
- namecheck result refresh if the Add Font issue is opened later;
- package strategy if Google Fonts asks for release/archive packaging instead
  of `sources/config.yaml`;
- final `date_added` and source commit.

## Local QA Commands

```bash
make release-check
make proof
make release-metadata-readiness
make qa
make reports
make source-readiness
make family-name-readiness
make authorship-disclosure-readiness
make packager-source-strategy
make proof-review-readiness
make proof-review-packet
make warning-worklist
make release-archive-build
make prepare-gf-clean-checkout
make final-values-packet
make final-values-proposal
make final-values-check VALUES=/path/to/final-values.json
make apply-final-values VALUES=/path/to/final-values.json
make package-dry-run-readiness
make packager-dry-run-record
make downstream-pr-draft
make downstream-pr-readiness
make submission-handoff-readiness
make google-fonts-reference-refresh
make agent-reuse-readiness
make next-actions
make blockers
make script-gate-tests
make final-readiness-check
```

`make qa` matches the Virtua Grotesk command surface and runs the release
variable Fontspector profile after building. `make test` aliases `make qa`.

`make reports` regenerates the release/readiness report bundle through the
same report path used by `make agent-reuse-readiness`.

`make release-check` builds once, then runs the release variable Fontspector
profile, downstream metadata checker, package-context Fontspector probe, and
release-structure preflight.

`make proof` regenerates `out/proof/index.html`; review it before treating the
generated Vietnamese and Latin Extended component glyphs as final drawings.

`make release-metadata-readiness` regenerates
`documentation/release-metadata-readiness.md`, which records the current source
version, built font version, git HEAD, dirty state, and final
`date_added`/`source.commit` placeholder status.

`make family-name-readiness` and `make authorship-disclosure-readiness`
regenerate local evidence reports for built family names, RFN status,
authorship files, CLA/disclosure decisions, and Add Font issue checklist
coverage.

`make packager-source-strategy` regenerates
`documentation/packager-source-strategy.md`, which keeps the preferred
`source.config_yaml` build-from-source path and release/archive fallback
evidence in one place.

`make proof-review-readiness` regenerates
`documentation/proof-review-readiness.md`, which verifies the current proof
index and summarizes open visual proof, generated composite, warning-floor,
and static-output decisions.

`make proof-review-packet` regenerates
`documentation/proof-review-packet.md`, which groups proof pages, remaining
Fontspector WARN items, and final-values keys for maintainer review.

`make warning-worklist` regenerates
`documentation/fontspector-zero-warning-worklist.md` from the current built
font and Fontspector reports.

`make release-archive-build` builds `dist/Blocksync-GF-review.zip` and updates
`documentation/release-archive-manifest.md`. Use this only if Google Fonts asks
for release/archive packaging instead of the preferred designspace/UFO
`sources/config.yaml` build path.

`make final-values-check VALUES=/path/to/final-values.json` validates a filled
copy of `documentation/google-fonts-final-values.template.json`, or a reviewed
copy of `documentation/google-fonts-final-values.proposal.json` after removing
proposal-only `_...` keys.
`make final-values-packet` regenerates
`documentation/google-fonts-final-values-packet.md`, which maps each
maintainer decision row to the JSON key that will apply it.
`make final-values-proposal` regenerates
`documentation/google-fonts-final-values.proposal.json`, a non-final starting
point with evidence-backed values prefilled and blank strings where a real
maintainer answer is still needed.
`make apply-final-values VALUES=/path/to/final-values.json` applies those
answers to the metadata draft, final decision sheet, Add Font issue draft,
submission handoff, `OFL.txt`, and active UFO `fontinfo.plist` copyright URLs.
When the Google Fonts Add Font issue exists, include it as
`google_fonts_issue_url` so the handoff line changes from pending to the final
issue URL.

`make final-readiness-check` is stricter than `make release-check`; it should
fail until final metadata values, maintainer decisions, proof review,
namecheck, Packager dry run, and WARN acceptance are resolved.

`make package-dry-run-readiness` reports whether the local `google/fonts`
checkout and metadata draft are ready for a guarded no-PR Packager dry run.
`make package-dry-run` refuses to run while final metadata placeholders remain.
If the shared checkout has unrelated dirty work, run
`make prepare-gf-clean-checkout` and rerun the readiness and dry-run commands
with `GF_REPO_PATH=/private/tmp/blocksync-google-fonts`.
For a rehearsal using a reviewed metadata copy, set
`PACKAGE_METADATA_PATH=/path/to/metadata-draft.md` on both
`make package-dry-run-readiness` and `make package-dry-run`; set
`PACKAGER_WORK_DIR`, `PACKAGER_DRY_RUN_RECORD_PATH`, and
`PACKAGER_DRY_RUN_RECORD_OUTPUT` when the rehearsal record should not replace
the repo-local final record.
After a successful no-PR run, the wrapper records
`documentation/google-fonts-packager-dry-run-record.json` and regenerates
`documentation/packager-dry-run-record.md`; `make packager-dry-run-record`
rechecks that record against the current metadata draft. The wrapper performs
that record check in strict mode after Packager so stale or mismatched dry-run
evidence fails the run instead of only writing a negative report.

`make downstream-pr-readiness` records whether the eventual downstream
`google/fonts` PR is ready to open. It is read-only and checks the local
`google/fonts` fork, package path, issue-first rule, expected branch/title/body,
Packager readiness, and the clean-checkout escape hatch.

`make downstream-pr-draft` generates
`documentation/google-fonts-downstream-pr-draft.md`, including the final PR
title, provenance body line, Google Fonts issue URL, and expected branch.

`make google-fonts-reference-refresh` verifies that the repo-local reference
map records the current Add Font issue template and the recent merged
`google/fonts` PR examples used for this setup pass. Refresh those live
references again before opening the issue or PR.

`make next-actions` regenerates `documentation/next-actions.md`, a compact
owner-grouped queue for resuming the remaining maintainer, proof, packaging,
and downstream blockers.

`make blockers` regenerates `documentation/final-submission-blockers.md`, the
full final-submission blocker snapshot used for handoff and later resumption.

## Expected Downstream PR Shape

- Branch name: `gftools_packager_ofl_blocksync`
- Family directory: `ofl/blocksync`
- PR title: `Blocksync : 1.000 added`
- PR body provenance line:
  `Taken from the upstream repo <repo-url> at commit <commit-url>.`
  Replace the placeholders with the line generated by
  `make downstream-pr-draft` from the final source metadata.
- Open or link the Google Fonts Add Font issue before creating the PR.
- Keep the PR scoped to one family directory.
- Match recent merged PR checklist expectations: Fontspector review, OFL URL
  review, subset/primary-script review where applicable, designer profile
  status, and tags for new fonts.

## Packaging Notes

The downstream metadata draft currently uses:

```textproto
source {
  repository_url: "https://github.com/eliheuer/blocksyncer"
  commit: "PENDING_FINAL_40_CHARACTER_COMMIT"
  config_yaml: "sources/config.yaml"
  branch: "main"
}
```

Keep the `config_yaml` path if Google Fonts accepts the reproducible
designspace/UFO build. If review asks for binary release packaging instead,
create a release/archive package containing:

- `OFL.txt`
- `fonts/variable/Blocksync[wdth,wght].ttf`
- `documentation/DESCRIPTION.en_us.html`

Then update the metadata draft with the final archive URL and rerun
`make release-check`.

## Known Review Items

- Review or accept the remaining Fontspector warning floor documented in
  `documentation/fontspector-zero-warning-worklist.md`.
- Review generated Vietnamese and Latin Extended composites in proof output.
- Confirm that static TTFs remain proof-only outputs unless Google Fonts asks
  for downstream static files.
- Confirm designer profile, authorship, AI-use disclosure, and ongoing
  maintenance statement before opening the issue.
