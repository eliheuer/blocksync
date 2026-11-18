# Google Fonts Readiness

This repo is being prepared for Google Fonts onboarding.

## Current Scope

- Family: Blocksync
- License: SIL Open Font License v1.1
- Sources: UFO masters plus `sources/Blocksync.designspace`
- Axes: `wght` 400-900, `wdth` 75-125
- Build entrypoint: `make build`
- Fast structure gate: `make preflight-only`
- Release metadata evidence gate: `make release-metadata-readiness`
- Source-readiness gate: `make source-readiness`
- Metadata draft gate: `make metadata-check`
- Package-context QA gate: `make package-context-check`
- Family-name evidence gate: `make family-name-readiness`
- Authorship/disclosure evidence gate: `make authorship-disclosure-readiness`
- Packager source-strategy gate: `make packager-source-strategy`
- Proof review evidence gate: `make proof-review-readiness`
- Placeholder audit gate: `make placeholder-audit`
- Decision application gate: `make decision-application-check`
- Isolated `google/fonts` checkout prep: `make prepare-gf-clean-checkout`
- Final values helper:
  `make final-values-check VALUES=/path/to/final-values.json`, then
  `make apply-final-values VALUES=/path/to/final-values.json`
  Include `google_fonts_issue_url` after opening the Add Font issue.
- Packager readiness gate: `make package-dry-run-readiness`
- Packager dry-run evidence gate: `make packager-dry-run-record`
- Downstream PR draft gate: `make downstream-pr-draft`
- Consolidated handoff gate: `make release-check`
- Final submission gate: `make final-readiness-check`
- Preferred GF build config: `sources/config.yaml`

## Source Policy

- Active release sources are designspace/UFO only.
- `.glyphs` files are archived in `sources/archive/` and are not package inputs.
- `sources/Blocksync-Regular.ufo` is the generated normal-width default source
  used to keep the variable font default at Regular width/weight.
- Generated fonts, build outputs, instance UFOs, and local venvs are ignored.

## Open Release Work

- Confirm final public upstream URL, version/tag strategy, RFN status,
  designer profile, AI-use disclosure, and package source strategy.
- Review glyphset coverage for the intended first Google Fonts submission.
- Generate and review proof output for spacing, kerning, outlines, and
  interpolation behavior.
- Replace pending values in the downstream metadata draft and run a Packager
  dry run after source/QA blockers are resolved or explicitly accepted.

## Current Verification

Checked 2026-05-30 with the repo-local `venv` built from `requirements.in`:

- `make preflight-only` passes.
- `make release-metadata-readiness` reports source UFO versions and built
  variable-font version metadata match locally, while final `date_added`,
  final `source.commit`, and a clean release commit remain pending.
- `make source-readiness` validates that `sources/config.yaml` points to
  `sources/Blocksync.designspace`, no `.glyphs` files remain as top-level
  package inputs, and all seven active UFO masters load with matching glyph
  inventories.
- `make family-name-readiness` reports local built-name and RFN evidence is
  ready, while final `namecheck.fontdata.com` and authorship/CLA/RFN answers
  are still pending.
- `make authorship-disclosure-readiness` reports local AUTHORS,
  CONTRIBUTORS, OFL, and Add Font issue checklist coverage is ready, while
  final designer, AI-use, and authorship/CLA answers are still pending.
- `make packager-source-strategy` reports the preferred `source.config_yaml`
  build-from-source path and release/archive fallback evidence are locally
  ready, while the final package-strategy answer and source commit remain
  pending.
- `make proof-review-readiness` reports the existing proof bundle is locally
  ready, while proof review, generated composite, warning-floor, and static
  output decisions remain pending.
- `make placeholder-audit` reports public placeholder strings that still need
  final metadata values, maintainer answers, proof review, or PR provenance
  before package handoff.
- `make decision-application-check` maps all final decision sheet rows to the
  metadata, Packager dry-run, and downstream PR gates they block.
- `make release-check` builds once, then runs the release variable
  Fontspector gate, metadata draft gate, package-context gate, and
  release-structure preflight.
- `make test` builds `fonts/variable/Blocksync[wdth,wght].ttf` and 18 static
  TTFs, then runs Fontspector on the release variable font.
- `make metadata-check` passes structurally and reports expected blockers only
  for `date_added` and `source.commit`.
- `make package-context-check` creates a temporary `ofl/blocksync` package
  from the metadata draft and generated variable font, then runs Fontspector
  with network-only axes matching excluded. Fontspector 1.6's
  `googlefonts/metadata/consistent_repo_urls` check is also excluded there
  because it mis-parses standard Google Fonts DESCRIPTION links; the repo URL
  is checked directly by `scripts/check_downstream_metadata.py`.
- Variable default names now resolve to `Blocksync Regular`.
- `OFL.txt`, `AUTHORS.txt`, and `CONTRIBUTORS.txt` have release-ready local
  project credits. Generated name ID 0 now uses the Blocksyncer upstream URL.
- Fontspector 1.6.0 Google Fonts profile writes:
  - `out/fontspector/fontspector-report.html`
  - `out/fontspector/fontspector-report.md`
  - `out/badges/`
- Latest release variable QA summary: 0 ERROR, 0 FATAL, 0 FAIL, 3 WARN,
  59 SKIP, 8 INFO, 129 PASS.
- Latest package-context QA summary: 0 ERROR, 0 FATAL, 0 FAIL, 3 WARN,
  46 SKIP, 10 INFO, 155 PASS.
- `make test` now exits cleanly for the release variable font. Use
  `CHECK_STATIC=1 ./scripts/check_gf_fonts.sh` for local static TTF proofing
  output checks. Static proofing writes separate reports:
  - `out/fontspector/fontspector-static-report.html`
  - `out/fontspector/fontspector-static-report.md`
- Current metadata subset draft keeps `latin`, `latin-ext`, `menu`, and
  `vietnamese` so already-encoded Latin Extended codepoints are not stranded.
  Local `glyphsets coverage` reports `GF_Latin_Core 100%` and
  `GF_Latin_Vietnamese 100%` and `GF_TransLatin_Pinyin`/`GF_Latin_PriAfrican`
  remain below 80%, while package probing shows the `latin-ext` and
  `vietnamese` subset thresholds clear locally.
- Current static proofing status: 12 FAIL, all from Condensed/Expanded static
  `googlefonts/font_names` unsupported-style checks. Treat generated static
  TTFs as proof outputs until static package naming is deliberately resolved.
- `make proof` generates a current diffenator2 proof bundle in `out/proof/`;
  the latest index contains 73 proof pages and 19 fonts for human spacing,
  outline, and interpolation review.
- `scripts/build_proof_index.py` writes `out/proof/index.html`, and
  `scripts/index.html` links the release Fontspector report, static proofing
  report, and proof index.
- `scripts/fix_gf_metadata.py` patches generated TTFs with GF-required
  metadata that does not survive instance generation: installable embedding,
  OFL copyright name records, identity `avar`, and Latin `meta` script tags.
- `scripts/check_downstream_metadata.py` verifies the downstream metadata draft
  against the designspace axes, package file mapping, generated variable font
  name records, `fvar`, `avar`, vendor ID, installable embedding, and Latin
  script metadata.
- `scripts/check_package_context.py` catches package-context warnings/failures
  that loose-font Fontspector runs do not see, including description URL,
  sample-text tofu, and subset-threshold behavior.
- `nbspace` widths now match `space` widths in the active UFOs.
- `dcaron` and `tcaron` now use the existing `caroncomb.alt` source glyph
  instead of resolving through the regular caron component.
- Case-mapping gaps were filled for `ccircumflex`, `scircumflex`, `itilde`,
  `Ibreve`, `Lj`, and `LJ`.
- Latin mark positioning is active under the `latn` script via UFO
  `features.fea` language-system declarations.
- Placeholder contour failures were resolved for `onehalf`, `section`,
  `currency`, `cedillacomb`, and `ogonekcomb`.
- Added source glyphs for U+2028, U+2029, U+25CC, and U+20B9.
- Math sign advances now match for `less` and `greater`; `caroncomb.alt` is
  encoded as U+0315.
- `dollar` now has compatible contours and a consistent advance across the
  condensed weight masters.
- Lithuanian mark-attachment WARNs were cleared by adding top anchors to
  ogonek composites and L/M glyphs across the active UFO masters.
- Safe auxiliary coverage composites were added for `Gcaron`, `gcaron`,
  `Hcaron`, `hcaron`, `Kcaron`, `kcaron`, `Ucaron`, `ucaron`, `Etilde`,
  `etilde`, `Oslashacute`, `oslashacute`, `Ldot`, `ldot`, and U+02BB.
  Additional component-based review glyphs were added for `Tbar`, `tbar`,
  `Gstroke`, `gstroke`, `Ezh`, `ezh`, `Ezhcaron`, `ezhcaron`, and `longs`,
  clearing the release Fontspector auxiliary shape-language WARN. These still
  need visual proof review before treating them as final drawings.
- Component-based Vietnamese review glyphs were added across the active UFO
  masters via `scripts/add_vietnamese_components.py`, raising
  `GF_Latin_Vietnamese` coverage to 100% and clearing the package-context
  `vietnamese` unsupported-subset WARN. These glyphs need human proof review
  before final submission.
- Component-based Latin Extended review glyphs were added across the active UFO
  masters via `scripts/add_decomposable_latin_ext_components.py`, raising the
  broad Google Fonts `latin-ext` subset probe to 308/1144 codepoints, above
  the local threshold requirement of 229. The script intentionally skips a
  small set of decomposable composites that would otherwise trigger unrelated
  Pinyin, PriAfrican, or Aleut package-context obligations.
- Baseline/cap-height outline warnings were cleared for `K`/`k` derivatives
  and `caroncomb.alt` derivatives. Remaining outline-alignment WARNs are
  limited to G/S/Ccedilla-derived implied curve points and scaled `section`
  components; treat those as visual-review items before changing curves.
- Heavy extreme spacing-mark and trademark metric inconsistencies were cleaned
  up in the UFO sources, clearing the package-context
  `suspicious_sidebearings` WARN.
- Google Fonts package drafts now exist:
  - `documentation/DESCRIPTION.en_us.html`
  - `documentation/google-fonts-downstream-metadata-draft.md`
  - `documentation/google-fonts-downstream-package-preview.md`
  - `documentation/google-fonts-final-decision-sheet.md`
  - `documentation/google-fonts-package-checklist.md`
  - `documentation/google-fonts-add-font-issue-draft.md`
  - `documentation/google-fonts-source-strategy.md`
  - `documentation/google-fonts-glyphset-coverage.md`
  - `documentation/google-fonts-name-audit.md`
  - `documentation/google-fonts-submission-handoff.md`
  - `documentation/open-placeholder-audit.md`
  - `documentation/decision-application-blockers.md`
  - `documentation/fontspector-zero-warning-worklist.md`
  - `documentation/final-submission-blockers.md`
  - `documentation/final-readiness-report.md`
  - `documentation/package-dry-run-readiness.md`
  - `documentation/release-archive-manifest.md`

Largest remaining blocker groups:

- final downstream metadata values: `date_added`, source commit, branch, and
  package source strategy;
- maintainer answers in `documentation/google-fonts-final-decision-sheet.md`;
- current Fontspector WARN review: metadata reachability, `uni01F5`
  contour-count review, and outline alignment;
- visual proof review of generated Vietnamese and Latin Extended review
  composites before treating them as final drawings;
- static TTF naming if Google Fonts asks for downstream static files;
- human review of the generated `out/proof/` artifacts and final package
  specimen quality.

## Reusable Workflow

Portable Google Fonts onboarding guidance lives in `.agents/`. Copy that
directory into future font repos, then replace family names, active source
paths, axes, build outputs, and package strategy values.
