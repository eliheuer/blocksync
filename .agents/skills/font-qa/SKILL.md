# /font-qa

Run source and binary QA for Blocksync.

## Usage

`/font-qa [preflight|fontspector|static|sources|all]`

Default: `all`

## Commands

- Fast release-structure gate:

  ```bash
  make preflight-only
  ```

- Build plus release variable Fontspector gate:

  ```bash
  make test
  ```

- Downstream-like package-context Fontspector gate:

  ```bash
  make package-context-check
  ```

- Current Fontspector warning floor:

  ```bash
  make warning-worklist
  ```

- Optional static proofing report:

  ```bash
  CHECK_STATIC=1 ./scripts/check_gf_fonts.sh
  ```

- Visual proof output:

  ```bash
  make proof
  ```

## Source QA

For source edits, check all UFO masters referenced by
`sources/Blocksync.designspace`, not just one style. Verify:

- `make source-readiness` passes;
- every designspace source exists;
- glyph inventories match across active masters when adding or removing glyphs;
- compatible glyphs keep matching contour/component structure where
  interpolation depends on it;
- widths and anchors are updated consistently across width/weight masters;
- `contents.plist` is updated when adding new `.glif` files;
- encoded support glyphs required by Fontspector, such as dotted circle and
  spacing/combining marks, are not removed without a full `make test`.

## Report Policy

Classify every Fontspector FAIL/WARN as:

- fix now;
- drawing/source blocker;
- maintainer decision;
- reviewer-approved exception;
- tool limitation with evidence.

Keep the current summary in `GF_READINESS.md` and link any longer evidence from
`documentation/`. Use `documentation/fontspector-zero-warning-worklist.md` for
the current Google Fonts WARN floor and do not mark final readiness complete
until remaining WARNs are fixed or explicitly accepted for first review.
