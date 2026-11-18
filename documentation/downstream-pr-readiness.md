# Downstream PR Readiness

This generated report records local evidence for the eventual downstream
`google/fonts` pull request. It does not open an issue, create a branch,
push commits, or write to the local `google/fonts` checkout.

## Summary

- Ready to open downstream PR: no
- First blocker: google/fonts checkout has dirty paths outside ofl/blocksync
- Expected downstream family path: `ofl/blocksync`
- Expected Packager branch: `gftools_packager_ofl_blocksync`
- Expected PR title: `Blocksync : 1.000 added`
- Expected PR body provenance line: `Taken from the upstream repo <repo-url> at commit <commit-url>.`
- Downstream PR draft ready: no
- Google Fonts issue pending: yes
- Metadata has final-value placeholders: yes
- Guarded no-PR Packager dry run ready: no
- Final no-PR Packager dry run recorded: no
- Local google/fonts checkout exists: yes
- Current google/fonts branch: `main`
- google/fonts tracking branch: `origin/main`
- google/fonts origin: `git@github.com:eliheuer/fonts.git`
- google/fonts upstream: `https://github.com/google/fonts.git`
- google/fonts main vs origin/main: 0 ahead, 0 behind
- google/fonts main vs upstream/main: 0 ahead, 0 behind
- google/fonts fork base ready for branch: no
- Effective clean fork base ready for branch: no
- Dirty google/fonts paths inside family dir: 0
- Dirty google/fonts paths outside family dir: 1
- Suggested clean GF_REPO_PATH: `/private/tmp/blocksync-google-fonts`
- Suggested clean checkout exists: no
- Suggested clean checkout branch: `missing`
- Suggested clean checkout base ready: no
- Suggested clean checkout dirty paths outside family dir: 0
- Current downstream family file count: 0

## Blocking Items

- google/fonts checkout has dirty paths outside ofl/blocksync
- downstream metadata still has final-value placeholders
- Google Fonts Add Font issue has not been recorded
- guarded no-PR Packager dry run is not ready
- final no-PR Packager dry run has not been recorded
- downstream PR draft is not final

## Handoff Coverage

- Handoff names expected Packager branch: yes
- Handoff includes expected PR title: yes
- Handoff includes expected PR provenance body line: yes
- Downstream PR draft includes final title: yes
- Downstream PR draft includes final provenance: no
- Handoff records issue-first rule: yes
- Handoff records one-family-directory rule: yes

## google/fonts Fork Evidence

Dirty paths inside family dir:

- None

Dirty paths outside family dir:

- `?? ofl/virtuagrotesk/`

Clean checkout escape hatch:

Use `make prepare-gf-clean-checkout` and rerun readiness with `GF_REPO_PATH=/private/tmp/blocksync-google-fonts` when the shared checkout has unrelated dirty work.

Current files inside downstream family dir:

- None

## Safe Local Sequence

Use this only after final metadata, final proof review, issue creation,
and no-PR Packager review are complete:

```bash
make release-check
GF_REPO_PATH=/Users/eli/GH/forks/fonts make package-dry-run-readiness
GF_REPO_PATH=/Users/eli/GH/forks/fonts make package-dry-run
git -C /Users/eli/GH/forks/fonts checkout -b gftools_packager_ofl_blocksync
```

Only after reviewing the no-PR package and recording the Google Fonts
issue number should any final Packager run use PR-opening flags.
