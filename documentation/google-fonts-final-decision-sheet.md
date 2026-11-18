# Google Fonts Final Decision Sheet

This is the short maintainer-facing sheet for the values and review decisions
that remain before the Blocksync Google Fonts submission can be treated as
final. Fill this once, apply the answers to the listed files, then rerun
`make release-check`.

## Required Final Values

| Decision | Current value | Final answer | Apply to |
| --- | --- | --- | --- |
| Google Fonts `date_added` | `PENDING-YYYY-MM-DD` | TBD | `documentation/google-fonts-downstream-metadata-draft.md` |
| Final source commit | `PENDING_FINAL_40_CHARACTER_COMMIT` | TBD | `documentation/google-fonts-downstream-metadata-draft.md`, Add Font issue/PR text |
| Public upstream URL | `https://github.com/eliheuer/blocksyncer` | Confirm or replace | metadata draft, `OFL.txt`, generated name ID 0 policy, Add Font issue |
| Public default branch | `main` | Confirm or replace | metadata draft |
| Package source strategy | preferred `source.config_yaml: "sources/config.yaml"` | Confirm or switch to release/archive | metadata draft, package preview, release archive manifest |
| Family name uniqueness | `namecheck.fontdata.com` API clear on 2026-05-30 | namecheck.fontdata.com API clear on 2026-05-30: zero matches at confidence 0.3-1.0 and trademark=false | Add Font issue, handoff docs |
| Designer string | `Eli Heuer` | Confirm or replace | metadata draft, issue, profile text |
| AI-use disclosure | pending maintainer answer | Confirm wording | Add Font issue, maintainer notes |
| Authorship/CLA/RFN status | local OFL/no-RFN drafts exist | Confirm | Add Font issue, downstream PR |

## Review Decisions

| Review item | Current evidence | Final answer |
| --- | --- | --- |
| Fontspector warning floor | `make release-check` passes with 3 WARN: metadata reachability, `uni01F5` contour count, outline alignment | Accept for first review or schedule source cleanup |
| Visual proof | `make proof` writes `out/proof/index.html` with 73 proof pages and 19 fonts | Maintainer review required |
| Generated Latin Extended and Vietnamese composites | Added to clear coverage/subset gates; documented as review glyphs | Accept, revise, or defer |
| Static TTFs | Generated for local proofing, not listed as downstream package files | Keep proof-only unless Google Fonts asks |
| Release/archive fallback | `dist/Blocksync-GF-review.zip` is built by `make release-check` and tracked in `documentation/release-archive-manifest.md` | Use only if Google Fonts rejects `source.config_yaml` path |

## Apply Flow

1. Copy `documentation/google-fonts-final-values.template.json` to a scratch
   values file and fill every value.
   Use a simple git branch name for `branch` such as `main`; branch values with
   spaces, traversal, or git ref metacharacters are rejected.
2. Run `make final-values-packet` and use
   `documentation/google-fonts-final-values-packet.md` to confirm every
   decision row maps to a JSON key.
3. Run `make final-values-check VALUES=/path/to/final-values.json`.
4. Run `make apply-final-values VALUES=/path/to/final-values.json` to update
   this sheet, `documentation/google-fonts-downstream-metadata-draft.md`,
   `documentation/google-fonts-add-font-issue-draft.md`, and
   `documentation/google-fonts-submission-handoff.md`. The helper also keeps
   `OFL.txt` and active UFO `fontinfo.plist` copyright URLs aligned with the
   final public upstream URL so generated name ID 0 stays consistent.
5. If release/archive packaging is selected, provide the final
   `archive_url` in the values file and rebuild the archive with
   `make release-archive-build`.
6. If any answer needs custom wording after the automated application, edit the
   affected draft directly.
   If the Google Fonts Add Font issue already exists, include its URL as
   `google_fonts_issue_url` in the values file so downstream PR readiness can
   verify the issue-first rule.
7. Run:

   ```bash
   make release-check
   make proof
   make packager-dry-run-record
   make downstream-pr-readiness
   make final-readiness-check
   ```

8. Run `make package-dry-run-readiness`, then `make package-dry-run` for a
   guarded no-PR Packager dry run in a local `google/fonts` checkout before
   opening a downstream PR. The wrapper records the dry-run evidence; rerun
   `make packager-dry-run-record` if the metadata draft changes.
