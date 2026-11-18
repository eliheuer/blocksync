# Scoped glyph drafts

Record the starting Git SHA, glyph names, comma-separated master names and intended change. Run each batch on a separate worktree and branch. Give each writer disjoint glyphs and component families. Keep donors read-only. If a donor lacks a designer-approved example of the construction, return the glyph for a design decision.

Read CONTEXT.md. Inspect the base and mark recipes and dependent glyphs in all seven masters. In a matching live editor session, use a proposal layer and review the preview before applying it. For on-disk edits, edit only the assigned GLIF files. Mark the result purple. Keep the original encoding, advance, anchors, kerning and all historical layers.

Run the assignment gate with the original SHA, e.g. `make check-changes BASE=HEAD GLYPHS="threequarters" MASTERS="Condensed Black"` before the first commit. Keep using that original SHA after commits. Check interpolation structure and run fgtools lint-glifs on the named glyphs. Run make build, make test and make proof. Give the independent reviewer the images, names, masters and CONTEXT.md. Return faults for correction, and keep unresolved design choices for Eli. Commit each tested batch with its scope. Only Eli assigns green and approves publication of drawings.
