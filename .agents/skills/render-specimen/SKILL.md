# /render-specimen

Create quick Blocksync specimen renders for review.

## Usage

`/render-specimen [proof|custom]`

Default: `proof`

## Instructions

- Prefer the built-in proof workflow first:

  ```bash
  make proof
  ```

- Use `out/proof/index.html` as the stable entrypoint for generated proof
  pages.
- If a custom specimen image is needed, build fonts first with `make build`,
  then use the local drawing/rendering tool already present in the repo. Keep
  generated images under `out/` unless the asset is intentionally part of the
  Google Fonts package.
- Report the font file, text, axis location, and output path for every custom
  specimen.

Do not commit generated specimen assets unless they are explicitly selected for
documentation, article, README, or release packaging.
