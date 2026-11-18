# /proof

Generate and review Blocksync proof artifacts.

## Usage

`/proof [build|review|all]`

Default: `all`

## Build

Run:

```bash
make proof
```

This builds the Font.Garden print PDF and the two-axis specimen in output/proof/. The older Google Fonts handoff uses `make proof-legacy` for its HTML bundle.

## Review

Check the proof output after any source, spacing, kerning, component, glyphset,
or metadata change that affects rendered fonts. Review:

- regular default instance;
- condensed and expanded width extremes;
- weight extremes;
- diacritic placement;
- component-derived symbols and punctuation;
- interpolation behavior across width and weight;
- spacing and kerning strings.

Document unresolved visual decisions in `GF_READINESS.md` or a focused
`documentation/` note before handing off to Google Fonts.
