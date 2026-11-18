# /compare-reference

Compare a reference image to the current Blocksync rendering and produce a
specific edit plan.

## Usage

`/compare-reference <image-path> [--text "..."]`

The image path should point to a reference image showing the intended text or
glyph appearance. If the text is not obvious, ask for it before drawing
conclusions.

## Instructions

Execute these phases in order:

### Phase 1: Read The Reference

Read the reference image and describe:

- characters or text shown;
- stroke weight, proportions, contrast, and overall texture;
- terminal and corner behavior;
- counter sizes and aperture openness;
- spacing density and any obvious tight or loose pairs.

### Phase 2: Build And Render A Matching Specimen

1. Determine the reference text.
2. Build the current font:

   ```bash
   make build
   ```

3. Render the same text using the repo's proof/specimen tooling where possible.
   Prefer an existing `make proof` or `render-specimen` path over creating a
   one-off renderer. If a one-off renderer is necessary, write it under a
   temporary output path and do not commit it unless requested.

### Phase 3: Read The Current Rendering

Inspect the current rendering and describe the same attributes as the
reference: proportions, stroke weight, counters, terminals, and spacing.

### Phase 4: Compare

Create a direct comparison covering:

- **Proportions:** width differences per character, cap-height and x-height
  relationships, descender/ascender fit.
- **Stroke weight:** stem thickness, overshoot impression, and heavy/light
  balance across width and weight extremes.
- **Counter shapes:** open versus closed, angular versus round, and whether
  counters match related glyphs.
- **Terminals and corners:** flat, angled, rounded, clipped, or block-like
  decisions.
- **Spacing:** overall density plus specific tight/loose pairs.
- **Specific glyphs:** the highest-impact glyphs to edit first.

### Phase 5: Produce An Edit Plan

Return a prioritized action list. For each item, specify:

1. glyphs to edit;
2. masters affected;
3. exact source file family if known;
4. specific change: advance width, sidebearing, component offset, anchor,
   contour coordinates, or point structure;
5. approximate values if the evidence supports them.

Structural changes to interpolating outlines must be made compatibly across
all active UFO masters. If compatibility cannot be preserved with a small edit,
stop and propose a redraw plan before writing GLIF changes.
