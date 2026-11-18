# /draw-outline

Draw or redraw a glyph outline in the Blocksync UFO sources.

## Usage

`/draw-outline <glyph-name> [--masters all|regular|condensed|expanded|path] [--from-sketch <image-path>]`

Default master set: `all`.

## Instructions

### Step 0: Gather Context

1. Parse `sources/Blocksync.designspace` and identify the active UFO masters.
2. Read each selected UFO's `glyphs/contents.plist`.
3. If the glyph already exists, inspect its current GLIF:
   - advance width;
   - components;
   - contour count and point counts;
   - anchors;
   - unicode value and lib color.
4. If `--from-sketch` is provided, inspect the image before planning.
5. Read related glyphs for consistency. Examples:
   - for accented glyphs, inspect the base glyph and mark source;
   - for new capitals, inspect nearby construction families such as `O`, `C`,
     `G`, `H`, `N`, or `S`;
   - for lowercase glyphs, inspect `n`, `o`, `c`, `s`, and existing accented
     composites as applicable.

### Step 1: Plan The Outline

Before writing XML, state:

- whether the glyph should be a component composite or a drawn outline;
- expected advance width and sidebearings;
- contour count and point-count compatibility strategy;
- anchors to preserve or add;
- which source glyphs are being used as construction references;
- whether the edit affects interpolation compatibility.

Prefer components for decomposable accented glyphs and support glyphs when the
base and marks already exist. Prefer drawn outlines only when components would
misrepresent the design or fail QA.

### Step 2: Draw Or Edit

Use UFO GLIF format 2. Keep edits as small as the drawing allows.

For new glyphs:

1. create the GLIF in every selected active UFO;
2. add it to each selected `contents.plist`;
3. include unicode values only for encoded glyphs;
4. copy appropriate anchors from the base glyph when the composite should keep
   mark attachment behavior.

For existing interpolating outlines:

1. preserve contour count, point count, point order, and point types across
   compatible masters unless deliberately redrawing the whole compatible set;
2. keep component structure compatible when possible;
3. avoid changing unrelated glyphs or generated proof outputs.

### Step 3: Vector Rules

- Place on-curve points at important extrema.
- Keep handles smooth and avoid crossed handles.
- Avoid zero-length handles and coincident points.
- Keep paths closed.
- Avoid tiny stray contours or off-canvas debris.
- Preserve intended overshoots unless a QA warning has been visually reviewed
  and deliberately corrected.
- Use integer coordinates; prefer existing Blocksync coordinate rhythms from
  nearby glyphs over inventing a new grid.

### Step 4: Validate

After editing:

1. re-read the edited glyphs and confirm contents mappings;
2. verify interpolation compatibility for changed outlines;
3. run:

   ```bash
   make preflight-only
   ```

4. run `make test` or `make release-check` after encoded glyph, glyphset,
   metadata, or interpolation-risk changes;
5. run `make proof` after visible drawing changes that require human review.
