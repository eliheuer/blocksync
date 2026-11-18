# Google Fonts Add Font Issue Draft

This draft is not ready to paste until the final source commit, metadata date,
and remaining QA warnings are reviewed.

## Issue Title

```text
Add Blocksync
```

## Labels

```text
I New Font, II Submission
```

## Draft Body

**Font Project Git Repo URL:**

https://github.com/eliheuer/blocksyncer

**Super short description of the Font Family:**

Blocksync is a block-like variable display typeface with Width and Weight axes.

**Requirements:**

By opening this issue, I confirm the project meets the following requirements:

- [ ] The entire font project is available in a Github repository and licensed
  under the OFL.
  - Draft status: local OFL and source path are in place; public upstream URL
    still needs final confirmation.
- [ ] The source files are available in the repo.
  - Draft status: active designspace/UFO sources are present; historical
    `.glyphs` files are archived.
- [ ] I am the sole copyright author of the entire project, or all other
  copyright authors have licensed their work to me under the OFL, and I commit
  to clearly disclosing if AI tools were used in the creation of this project.
  - Draft status: `AUTHORS.txt` and `CONTRIBUTORS.txt` list Eli Heuer; final
    AI-use disclosure still needs maintainer confirmation.
- [ ] There are no Reserved Font Names, or RFNs are not used in whole or in
  part in this family name.
  - Draft status: no RFN is declared in `OFL.txt`.
- [ ] The family name is unique according to `namecheck.fontdata.com`.
  - Draft status: `namecheck.fontdata.com` API clear on 2026-05-30; refresh
    if this issue is opened later.
- [ ] The app-menu family name is clearly communicated and definitive.
  - Draft status: built default names resolve to `Blocksync Regular`.
- [ ] The font supports at least Google Fonts Latin Core.
  - Draft status: Fontspector has no FAIL results, and local glyphsets coverage
    reports `GF_Latin_Core 100%`.
- [ ] The repo has the Google Fonts preferred upstream repo structure.
  - Draft status: source/build structure is in place; downstream package
    strategy still needs final confirmation.
- [ ] I have read, agree with, and comply with the Google Fonts contributing
  requirements.
  - Draft status: remaining WARNs and package metadata placeholders must be
    reviewed before opening.
- [ ] I will maintain the repository and participate in onboarding.
  - Draft status: maintainer confirmation required.

## Current QA Evidence

- Build command: `make build`
- QA command: `make test`
- Current Fontspector report:
  `out/fontspector/fontspector-report.html`
- Current release variable status: 0 FAIL, 0 ERROR, 0 FATAL.
- Remaining WARN groups: metadata reachability/subsetting, `uni01F5`
  contour-count review, and outline alignment review.
- Downstream metadata draft currently includes `latin`, `latin-ext`, `menu`,
  and `vietnamese`. Remaining subsetting WARNs are mainly encoded combining
  marks, spacing modifier marks, and dotted circle. Package-context probing
  now shows both `latin-ext` and `vietnamese` clear the local Google Fonts
  support thresholds.

## Finalize Before Opening

- Replace pending values in
  `documentation/google-fonts-downstream-metadata-draft.md`.
- Decide whether generated TTFs are supplied from a release/archive or via the
  `sources/config.yaml` build path.
- Review `documentation/google-fonts-package-checklist.md`.
- Rerun `make release-check`.
