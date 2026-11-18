# /google-fonts-coverage-drawing

Finish coverage-related drawing, composite, mark, and warning cleanup for a
Google Fonts submission while keeping the designspace/UFO sources compatible.
This skill adapts the reusable drawing-review workflow from Virtua Grotesk for
Blocksync's Latin, Latin-ext, and Vietnamese first-submission scope.

## Usage

`/google-fonts-coverage-drawing [audit|composites|warnings|proof|all]`

Default: `all`

## Inputs

Read these first:

- `sources/Blocksync.designspace`
- `sources/config.yaml`
- `documentation/google-fonts-glyphset-coverage.md`
- `documentation/fontspector-zero-warning-worklist.md`
- `out/fontspector/fontspector-report.md`
- `out/fontspector/fontspector-package-context-report.md`

## Principles

- Treat generated composites and mechanical outline changes as review
  candidates, not final design decisions.
- Keep the active build path on `sources/Blocksync.designspace` and UFO
  masters. Do not revive `.glyphs` files as active sources.
- Prefer family-native components, anchors, widths, and mark placement over
  copied external outlines.
- Keep component and contour structures compatible across all seven active UFO
  masters unless a deliberate design decision says otherwise.
- Do not delete supported marks or compatibility codepoints only to silence
  `unreachable_subsetting`; record the tradeoff and ask Google Fonts review if
  needed.
- Preserve intentional overshoots unless proof review says the shape should be
  snapped.

## Audit Flow

1. Parse the designspace and list every active UFO master.
2. Compare the current glyphset coverage report against the built font cmap.
3. Inspect the current Fontspector warning worklist:
   - unreachable serving subset codepoints,
   - contour-count warnings,
   - outline-alignment warnings.
4. For each warning, classify it as:
   - safe mechanical source fix,
   - source drawing review,
   - metadata/package strategy decision,
   - reviewer-accepted exception candidate.
5. Record the classification in `documentation/fontspector-zero-warning-worklist.md`
   or the final decision sheet before changing sources.

## Composite Cleanup

For accented Latin, Latin-ext, and Vietnamese glyphs:

1. Inspect the encoded glyph, base glyph, mark glyph, and matching lowercase or
   uppercase pattern.
2. Keep composites component-based when the base and mark already match the
   design.
3. Preserve anchors from the base glyph when the composite should remain mark
   attachable.
4. If a generated composite is visually wrong, fix component offsets in every
   active UFO master rather than decomposing only one master.
5. If a contour-count warning exists only because Blocksync intentionally uses a
   single-storey or uppercase-derived construction, document the evidence and
   leave it for maintainer/reviewer acceptance.

## Warning Cleanup

For `contour_count`:

- Confirm the glyph maps to the correct Unicode.
- Compare the glyph's design construction to adjacent encoded glyphs.
- Redraw only if the current construction is a genuine source error.
- Do not add dummy contours to satisfy the statistical expectation.

For `outline_alignment_miss`:

- Identify whether the coordinate is an explicit on-curve point, an implied
  curve extremum, or a transformed component artifact.
- Snap explicit accidental coordinates only after visual proof review.
- For implied curve extrema, inspect the parent contour before editing handles.
- For transformed components such as `section`, prefer a deliberate redraw or
  accepted warning over silent decomposition.

For `googlefonts/metadata/unreachable_subsetting`:

- Keep marks and dotted circle if they are needed for composition, proofing, or
  shaping sanity.
- Do not add unrelated non-Latin subsets just to silence the warning.
- If final review wants zero warnings, decide whether to move the codepoints
  into a supported subset, change encoding, or accept the warning with evidence.

## Verification Loop

After source edits:

```bash
make preflight-only
make release-check
make proof
```

After metadata-only warning work:

```bash
make metadata-check
make package-context-check
make warning-worklist
make preflight-only
```

Before saying the coverage/drawing pass is done:

- `make release-check` passes.
- `documentation/fontspector-zero-warning-worklist.md` matches the latest
  Fontspector reports.
- Every remaining warning has a clear final action: fixed, accepted for first
  review, or blocked on maintainer/Google Fonts decision.
- Proof output has been regenerated after the latest visible source change.
