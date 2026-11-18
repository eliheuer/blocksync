# Package Dry-Run Readiness

This report checks whether a no-PR Google Fonts Packager dry run can be
started safely. It does not write to the local `google/fonts` checkout.

## Summary

- GF_REPO_PATH: `/Users/eli/GH/forks/fonts`
- Local google/fonts checkout exists: yes
- Current google/fonts branch: `main`
- google/fonts origin: `git@github.com:eliheuer/fonts.git`
- google/fonts upstream: `https://github.com/google/fonts.git`
- Expected package path: `ofl/blocksync`
- Downstream family directory exists locally: no
- Dirty google/fonts paths outside package: 1
- Suggested clean GF_REPO_PATH: `/private/tmp/blocksync-google-fonts`
- Suggested clean checkout exists: no
- Suggested clean checkout branch: `missing`
- Suggested clean checkout dirty paths outside package: 0
- Clean checkout avoids shared dirty paths: no
- Effective checkout path for final dry run: `/Users/eli/GH/forks/fonts`
- Ready to run final no-PR Packager dry run: no
- First blocker: google/fonts checkout has dirty paths outside ofl/blocksync

## Blocking Items

- google/fonts checkout has dirty paths outside ofl/blocksync

## Dirty google/fonts Paths Outside Package

- `?? ofl/virtuagrotesk/`

## Clean Checkout Escape Hatch

Use this when the shared `google/fonts` checkout has unrelated dirty work.

```bash
make prepare-gf-clean-checkout
GF_REPO_PATH="/private/tmp/blocksync-google-fonts" make package-dry-run-readiness
GF_REPO_PATH="/private/tmp/blocksync-google-fonts" make package-dry-run
```


## Command

After final metadata values and maintainer decisions are applied, run:

```bash
make package-dry-run
```

The wrapper is intentionally guarded and refuses to run while metadata
placeholders remain.
