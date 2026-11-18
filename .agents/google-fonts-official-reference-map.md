# Google Fonts Official Reference Map

Last checked: 2026-11-18.

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

The checked google/fonts main revision is `5bd87dfc525c8a0d1d8529d3684716e00c3fc59a`. The template permits opening with pending checkboxes, then completing them on the issue page. [Checked revision](https://github.com/google/fonts/blob/5bd87dfc525c8a0d1d8529d3684716e00c3fc59a/.github/ISSUE_TEMPLATE/1_add-font.md)

Current checked template details:

- issue title pattern: `Add [Font Name]`;
- labels: `I New Font, II Submission`;
- Font Project Git Repo URL field;
- super short description field;
- checkbox for entire project availability in a GitHub repository and OFL
  licensing;
- separate confirmation that no larger retail Plus, Pro or other edition of the project exists;
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

The GitHub API confirmed that each PR added a family directory and merged.

| PR | Merged | Relevant evidence |
| --- | --- | --- |
| https://github.com/google/fonts/pull/11222 | 2026-11-06 | Geist Serif linked the source commit and preparation PR, described verified QA and requested specific custom-axis waivers. |
| https://github.com/google/fonts/pull/11179 | 2026-10-29 | Madhuban shipped a variable TTF, metadata, OFL and illustrated article. Its source record gives the upstream commit, branch, config and file mappings. |
| https://github.com/google/fonts/pull/11123 | 2026-10-15 | Firjar shipped a variable TTF with width and weight, alongside metadata, OFL and article. The source record maps the VF, OFL and article and identifies the build config. |

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

## Blocksync evidence

The public source repo is `eliheuer/blocksync` and its default branch is `main`. Full-text GitHub searches across issue and PR titles, bodies and comments for both Blocksync and its historical spelling Blocksyncer returned zero matches on November 18. Search again before creating an issue. [Upstream](https://github.com/eliheuer/blocksync) · [Blocksync search](https://github.com/google/fonts/issues?q=Blocksync) · [Blocksyncer search](https://github.com/google/fonts/issues?q=Blocksyncer)

FontData returned zero matches in all six confidence groups and a false trademark flag for Blocksync. The local evidence captures the API response. [Name search](https://namecheck.fontdata.com/api/?q=Blocksync)

A previous Google Fonts PR submitted by eliheuer was merged. Its currently visible checks provide no explicit CLA result. Confirm the agreement for the identity used by the downstream commit through Google's agreement manager. [Prior PR](https://github.com/google/fonts/pull/6850) · [Google Fonts PR guide](https://googlefonts.github.io/gf-guide/making-pr.html) · [Google CLA](https://cla.developers.google.com/)

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
