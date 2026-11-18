# Google Fonts Package Checklist

## Current Package Shape

- Upstream repo: `https://github.com/eliheuer/blocksyncer`
- Active source path: `sources/config.yaml` -> `sources/Blocksync.designspace`
- Active sources: seven UFO masters, including generated normal-width default
  `sources/Blocksync-Regular.ufo`
- Archived sources: historical `.glyphs` files in `sources/archive/`
- Release font: `fonts/variable/Blocksync[wdth,wght].ttf`
- Description draft: `documentation/DESCRIPTION.en_us.html`
- Metadata draft: `documentation/google-fonts-downstream-metadata-draft.md`
- Final decision sheet:
  `documentation/google-fonts-final-decision-sheet.md`
- Source strategy note: `documentation/google-fonts-source-strategy.md`
- Glyphset coverage note: `documentation/google-fonts-glyphset-coverage.md`
- Downstream package preview:
  `documentation/google-fonts-downstream-package-preview.md`
- Fallback release/archive manifest:
  `documentation/release-archive-manifest.md`
- Source-readiness report: `documentation/source-readiness.md`
- Release metadata readiness report:
  `documentation/release-metadata-readiness.md`
- Family-name readiness report: `documentation/family-name-readiness.md`
- Authorship/disclosure readiness report:
  `documentation/authorship-disclosure-readiness.md`
- Packager source strategy report:
  `documentation/packager-source-strategy.md`
- Proof review readiness report: `documentation/proof-review-readiness.md`

## Before Opening The Add Font Issue

- Run `make source-readiness`, then run `make release-check` and review all
  generated reports.
- Fill `documentation/google-fonts-final-decision-sheet.md`; do not replace
  metadata placeholders or issue draft notes without a maintainer answer.
- For a complete answer set, copy
  `documentation/google-fonts-final-values.template.json`, fill it, then run
  `make final-values-check VALUES=/path/to/final-values.json` before
  `make apply-final-values VALUES=/path/to/final-values.json`.
- Confirm the public upstream URL and default branch.
- Confirm the final source commit and version/tag strategy.
- Confirm `date_added` for downstream metadata.
- Review `documentation/release-metadata-readiness.md`; it should report local
  evidence ready, but final metadata should remain blocked until the reviewed
  release tree is committed and the Google Fonts package date is known.
- Confirm designer profile status for `Eli Heuer`.
- Confirm name uniqueness at `namecheck.fontdata.com`.
- Review `documentation/family-name-readiness.md` and
  `documentation/authorship-disclosure-readiness.md`; local evidence should
  be ready before final namecheck, CLA, designer, maintenance, and AI-use
  answers are applied.
- Confirm downstream subsets. Current draft keeps `latin`, `latin-ext`, `menu`,
  and `vietnamese` so existing encoded Latin Extended codepoints are not
  stranded. Package-context probing now shows both `latin-ext` and
  `vietnamese` clear the local Google Fonts support thresholds.
- Review current Fontspector WARNs and decide which are accepted for first
  submission.
- Review `documentation/google-fonts-glyphset-coverage.md` before changing
  subset scope.
- Run `make metadata-check` and confirm blockers are limited to final package
  values, not structural mismatches.
- Run `make package-dry-run-readiness` before attempting Packager. It should
  remain blocked while `date_added` and `source.commit` placeholders are
  present.
- If the shared `google/fonts` checkout has unrelated work, run
  `make prepare-gf-clean-checkout`, then use
  `GF_REPO_PATH=/private/tmp/blocksync-google-fonts` for
  `make package-dry-run-readiness`, `make package-dry-run`, and
  `make downstream-pr-readiness`.
- To rehearse against a reviewed metadata copy before applying it to the repo,
  set `PACKAGE_METADATA_PATH=/path/to/metadata-draft.md` for both
  `make package-dry-run-readiness` and `make package-dry-run`. For isolated
  rehearsal evidence, also set `PACKAGER_WORK_DIR`,
  `PACKAGER_DRY_RUN_RECORD_PATH`, and `PACKAGER_DRY_RUN_RECORD_OUTPUT`.
- Run `make package-context-check` and review
  `out/fontspector/fontspector-package-context-report.html`. The package probe
  excludes Fontspector 1.6's noisy `consistent_repo_urls` parsing check;
  `make metadata-check` verifies the canonical repository URL directly.
- Keep the preferred `source.config_yaml: "sources/config.yaml"` package path
  while Google Fonts accepts the designspace/UFO build. If review asks for
  release/archive packaging, run `make release-archive-build`, publish an
  equivalent GitHub release archive, add the final `source.archive_url`, and
  rerun `make release-check`.
- Review `documentation/packager-source-strategy.md` before changing source
  strategy; it should report local evidence ready before the strategy is
  confirmed in the final decision sheet.
- Generate visual proof output and review spacing, outlines, interpolation,
  and component-derived glyphs, especially the auxiliary review glyphs added
  to clear the shape-language warning: `Tbar`, `tbar`, `Gstroke`, `gstroke`,
  `Ezh`, `ezh`, `Ezhcaron`, `ezhcaron`, and `longs`, plus the Vietnamese
  horn, hook-above, dot-below, stacked-accent composites, and Latin Extended
  review composites generated by `scripts/add_vietnamese_components.py` and
  `scripts/add_decomposable_latin_ext_components.py`.
- Run `make proof-review-readiness` after `make proof`; it should report local
  proof evidence ready before final visual decisions are applied.

## Before Downstream PR

- Rerun `make release-check` after replacing final metadata values or changing
  glyph/source scope.
- Rerun `make source-readiness` after changing source config, designspace, UFO
  masters, or archived `.glyphs` files.
- Run `make final-readiness-check`; it must pass before treating the package as
  ready to submit.
- Apply final `METADATA.pb` values in the local `google/fonts` checkout.
- Prefer applying final local drafts through
  `make apply-final-values VALUES=/path/to/final-values.json` so the metadata,
  decision sheet, issue draft, handoff, `OFL.txt`, and active UFO copyright
  metadata stay aligned.
- Run `make metadata-final-check` after replacing `date_added` and
  `source.commit`.
- Run `make prepare-gf-clean-checkout` if the shared `google/fonts` fork is
  dirty for another family, and point the final dry run at
  `/private/tmp/blocksync-google-fonts`.
- Run `make package-dry-run` for the guarded no-PR Packager dry run first.
- Confirm `make packager-dry-run-record` reports the final no-PR run is
  recorded before opening any PR-mode Packager run. The wrapper uses strict
  record validation immediately after Packager, while the report command
  remains non-strict when it is only regenerating readiness docs.
- Run `make downstream-pr-draft` and review the generated PR title/body
  before opening the downstream branch.
- Keep `source.config_yaml: "sources/config.yaml"` if Google Fonts accepts the
  reproducible designspace/UFO build path.
- If Google Fonts asks for binary release packaging instead, create a release
  archive containing `OFL.txt`, `fonts/variable/Blocksync[wdth,wght].ttf`, and
  `documentation/DESCRIPTION.en_us.html`, then add the final `archive_url`.
