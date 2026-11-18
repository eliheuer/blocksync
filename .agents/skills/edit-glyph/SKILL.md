# /edit-glyph

Read, inspect, and edit glyphs in the Blocksync UFO sources.

## Usage

`/edit-glyph <glyph-name> [--masters all|regular|condensed|expanded|path]`

Default: `all`

## Instructions

1. Parse `sources/Blocksync.designspace` to get the active UFO list.
2. For each selected UFO, read `glyphs/contents.plist` and map the glyph name
   to its `.glif` filename.
3. Before editing, report:
   - advance width;
   - component list;
   - contour count and point counts;
   - bounding box;
   - left and right sidebearings when outlines have points;
   - anchors.
4. Apply edits with the smallest source change that satisfies the request.
5. If adding a glyph, add it to every active UFO and to every selected
   `contents.plist`.
6. If changing an interpolating outline, keep compatible point order, contour
   count, component structure, and point types unless the whole compatible
   family is intentionally redrawn.
7. Re-read the edited glyphs and run at least:

   ```bash
   make preflight-only
   ```

   Run `make test` after encoding, glyphset, metadata, or interpolation-risk
   changes.

## Active Masters

- `sources/Blocksync-Regular.ufo`
- `sources/Blocksync-CondensedRegular.ufo`
- `sources/Blocksync-CondensedBold.ufo`
- `sources/Blocksync-CondensedBlack.ufo`
- `sources/Blocksync-ExpandedRegular.ufo`
- `sources/Blocksync-ExpandedBold.ufo`
- `sources/Blocksync-ExpandedBlack.ufo`
