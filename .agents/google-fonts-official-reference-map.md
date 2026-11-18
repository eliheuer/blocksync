# Google Fonts Official Reference Map

Last checked: 2026-06-13.

Refresh these before final issue or PR work because Google Fonts requirements,
templates, and downstream PR conventions can change.

## Core Google Fonts Docs

| Reference | Use it for | Reusable agent surface |
| --- | --- | --- |
| https://googlefonts.github.io/gf-guide/ | Guide index and current navigation | onboarding skills |
| https://googlefonts.github.io/gf-guide/onboarding.html | New-family acceptance criteria, OFL/RFN/CLA/name/source/build/TTF/glyphset/QA expectations, issue-first entrypoint | `.agents/google-fonts-onboarding-checklists.md`; `.agents/skills/google-fonts-onboarding/SKILL.md` |
| https://googlefonts.github.io/gf-guide/upstream.html | Preferred upstream repository shape and public source expectations | repo baseline checklist; release/source strategy |
| https://googlefonts.github.io/gf-guide/requirements.html | Overall production requirements and exception handling | QA and final blocker reports |
| https://googlefonts.github.io/gf-guide/variable.html | Variable font axis, instance, `STAT`, and variable-specific review | QA skill; metadata checklist |
| https://googlefonts.github.io/gf-guide/metadata.html | Downstream `METADATA.pb` fields and source linkage | packaging skill; downstream metadata checklist |
| https://googlefonts.github.io/gf-guide/package.html | Packager behavior, package branch naming, `source.files`, release archive `archive_url`, no-PR review before PR mode | packaging skill; package dry-run checklist |
| https://googlefonts.github.io/gf-guide/article.html | `ARTICLE.en_us.html`, image, and provenance expectations | article/image checklist |
| https://googlefonts.github.io/gf-guide/making-pr.html | Issue-first rule, CLA/git identity, local fork setup, downstream PR expectations | PR identity and downstream PR checklists |
| https://googlefonts.github.io/gf-guide/onboarder-workflow.html | Onboarder review workflow, proof review expectations, handoff expectations | visual QA and handoff checklists |

## Current Add Font Template

Reference: https://github.com/google/fonts/blob/main/.github/ISSUE_TEMPLATE/1_add-font.md

Current checked template details:

- issue title pattern: `Add [Font Name]`;
- labels: `I New Font, II Submission`;
- Font Project Git Repo URL field;
- super short description field;
- checkbox for entire project availability in a GitHub repository and OFL
  licensing;
- checkbox that source files are available in the repo;
- checkbox for copyright authorship/licensing plus clear disclosure if
  AI tools were used;
- checkbox for no Reserved Font Names, or RFNs not conflicting with the family
  name;
- checkbox that the family name is unique according to
  `namecheck.fontdata.com`;
- checkbox that the app-menu family name is definitive and does not include a
  copyright holder full name or acronym;
- checkbox for at least Google Fonts Latin Core support via
  `GF_Latin_Core.txt`;
- checkbox that the repo follows the Google Fonts preferred upstream repo
  structure; exact template phrase: preferred upstream repo structure.
- checkbox that the submitter has read and complies with full contributing
  requirements;
- checkbox that the maintainer will maintain the repository and participate in
  onboarding;
- one image/screenshot is expected in the issue.

## Current Google Fonts Contributing Entrypoint

Reference: https://github.com/google/fonts/blob/main/CONTRIBUTING.md

- New OFL family submissions start by creating a `google/fonts` issue with a
  source repository link.
- Special circumstances can request exceptions on the issue.
- Google CLA status matters for downstream contributions.
- `CONTRIBUTORS.txt` tracks contributors; `AUTHORS.txt` tracks copyright
  holders.

## Recent Merged Downstream PR Examples

These were checked on 2026-06-13 as recent merged examples in
`google/fonts`:

| PR | Merged | Pattern used |
| --- | --- | --- |
| https://github.com/google/fonts/pull/10596 | 2026-06-08 | New font package for Yuyu Short; `METADATA.pb`, `OFL.txt`, TTF, and article; source block maps upstream repo, commit, files, and branch. |
| https://github.com/google/fonts/pull/10591 | 2026-06-05 | New family submission for Geist Pixel; PR body records upstream repo, commit/config, GF Latin Core coverage, namecheck, copyright, designers, and category. |
| https://github.com/google/fonts/pull/10613 | 2026-06-10 | Follow-up metadata update for Geist Pixel; adds final `date_added` and metadata ordering cleanup. |
| https://github.com/google/fonts/pull/10546 | 2026-05-22 | New font package for Pliant; PR checklist includes designer profile, minisite, and tags review items. |

Recent downstream PR body conventions to keep in Blocksync handoff:

- `Taken from the upstream repo <repo-url> at commit <commit-url>.`
- `PR Checklist` with PR placement/labels and linked issue; exact checklist
  item: The PR is linked to the corresponding issue.
- `Fontspector checks are reviewed and failing checks are resolved` before
  merge.
- `OFL.txt` URL review uses https://openfontlicense.org.
- subset definitions and `primary_script` are reviewed where applicable.
- Designers bio info/profile status and designer ordering are reviewed.
- `tags` are added for NEW FONTS.
- PRs are scoped to the affected family directory and linked Add Font issue.

## GitHub References

| Reference | Use it for | Reusable agent surface |
| --- | --- | --- |
| https://github.com/google/fonts | Downstream package layout, recent family directories, current PR conventions | downstream PR readiness |
| https://github.com/googlefonts/googlefonts-project-template | Optional automation and baseline upstream project conventions | project-template automation decision |
| https://github.com/googlefonts/glyphsets | GF Latin Core and script-specific glyphset coverage targets | glyphset/script QA |

## Reusable Evidence Set

For a new font repo, keep the evidence categories visible without recreating a
large generated report farm by default:

- official reference links and local decisions,
- source metadata and generated font metadata,
- master/source compatibility,
- glyphset and language coverage,
- Fontspector output,
- visual proof output,
- package source strategy,
- downstream metadata and Add Font issue draft,
- release/archive evidence if that source strategy is selected,
- current blockers and next actions.

## Portable Gate Shape

Every copied onboarding setup should have one synchronized command that:

1. builds or verifies current build output,
2. regenerates generated reports,
3. checks official-reference coverage,
4. checks decision-log coverage,
5. checks Fontspector and proof evidence,
6. checks package source and metadata readiness,
7. checks downstream fork/PR readiness,
8. fails only for known and documented blockers.

For Blocksync this command is:

```bash
make release-check
```

Use `make final-readiness-check` only after final values, issue URL,
maintainer/proof decisions, and Packager evidence are applied.
