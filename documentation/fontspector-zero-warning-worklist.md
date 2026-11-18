# Fontspector Zero-Warning Worklist

Font: `fonts/variable/Blocksync[wdth,wght].ttf`

This report records the remaining warning floor in both checked profiles.
It is a worklist for real cleanup and reviewer decisions, not
a recommendation to hide supported codepoints or narrow the package
scope just to reduce warning count.

## Current Warning Floor

- Honest zero-warning state possible with current scope: no
- Release variable Fontspector summary: 0 FAIL, 3 WARN, 8 INFO, 131 PASS, 60 SKIP
- Package-context Fontspector summary: 6 FAIL, 3 WARN, 10 INFO, 157 PASS, 46 SKIP
- Package-context warning checks: `googlefonts/metadata/unreachable_subsetting`: 1, `contour_count`: 1, `outline_alignment_miss`: 1

## Zero-Warning Verdict

True zero is not a final-polish toggle. It requires either source
drawing cleanup or Google Fonts reviewer acceptance for the remaining
metadata reachability, contour-count, and outline warnings. The
current package scope is honest: `latin`, `latin-ext`, `menu`, and
`vietnamese` all pass the local release gate, and the broad
`latin-ext`/`vietnamese` subset
thresholds clear locally.

## Subset Threshold Math

| Subset | Threshold | Subset codepoints | Present | Present needed | Coverage | Threshold met |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `latin-ext` | 20% | 1144 | 308 | 229 | 26.92% | yes |
| `vietnamese` | 50% | 115 | 109 | 58 | 94.78% | yes |

## Remaining Warning Buckets

### Metadata Reachability

The font intentionally keeps support marks and compatibility codepoints
that are useful for composition and proofing, but Google Fonts serving
subsets do not cover all of them. Do not delete these codepoints only
to silence `unreachable_subsetting`; review the final metadata strategy
with Google Fonts if needed.

A source-unencoding probe of these support marks was rejected: it
caused Google Fonts `glyph_coverage`, `dotted_circle`,
`shape_languages`, and `unreachable_glyphs` regressions. Keep the
codepoints unless Google Fonts explicitly asks for a different
package strategy.

Current package-context list:

- `U+02D8 BREVE`
- `U+02D9 DOT ABOVE`
- `U+02DB OGONEK`
- `U+0302 COMBINING CIRCUMFLEX ACCENT`
- `U+0306 COMBINING BREVE`
- `U+0307 COMBINING DOT ABOVE`
- `U+030A COMBINING RING ABOVE`
- `U+030B COMBINING DOUBLE ACUTE ACCENT`
- `U+030C COMBINING CARON`
- `U+0312 COMBINING TURNED COMMA ABOVE`
- `U+0315 COMBINING COMMA ABOVE RIGHT`
- `U+0326 COMBINING COMMA BELOW`
- `U+0327 COMBINING CEDILLA`
- `U+0331 COMBINING MACRON BELOW`
- `U+25CC DOTTED CIRCLE`

### Contour Count

- `uni01F5` (U+01F5 LATIN SMALL LETTER G WITH ACUTE) is component-based
  and currently has 2 contours where Fontspector expects 3-5. Review
  whether this should be accepted for Blocksync's construction or redrawn.

### Outline Alignment

- Remaining alignment warnings are G/S/Ccedilla-derived implied curve
  points and scaled `section` components. Treat them as visual-review
  items before snapping overshoots to the grid.

Current package-context list:

- Ccedilla (U+00C7): X=387.5,Y=2.5 (should be at baseline 0?)
- G (U+0047): X=349,Y=-2.5 (should be at baseline 0?)
- Gbreve (U+011E): X=349,Y=-2.5 (should be at baseline 0?)
- uni0122 (U+0122): X=349,Y=-2.5 (should be at baseline 0?)
- Gdotaccent (U+0120): X=349,Y=-2.5 (should be at baseline 0?)
- S (U+0053): X=180,Y=2.5 (should be at baseline 0?)
- Sacute (U+015A): X=180,Y=2.5 (should be at baseline 0?)
- Scaron (U+0160): X=180,Y=2.5 (should be at baseline 0?)
- Scircumflex (U+015C): X=180,Y=2.5 (should be at baseline 0?)
- uni0218 (U+0218): X=180,Y=2.5 (should be at baseline 0?)
- ccedilla (U+00E7): X=387.5,Y=2.5 (should be at baseline 0?)
- g (U+0067): X=349,Y=-2.5 (should be at baseline 0?)
- gbreve (U+011F): X=349,Y=-2.5 (should be at baseline 0?)
- uni0123 (U+0123): X=349,Y=-2.5 (should be at baseline 0?)
- gdotaccent (U+0121): X=349,Y=-2.5 (should be at baseline 0?)
- s (U+0073): X=180,Y=2.5 (should be at baseline 0?)
- sacute (U+015B): X=180,Y=2.5 (should be at baseline 0?)
- scaron (U+0161): X=180,Y=2.5 (should be at baseline 0?)
- uni0219 (U+0219): X=180,Y=2.5 (should be at baseline 0?)
- section (U+00A7): X=801.5,Y=-1 (should be at baseline 0?)
- section (U+00A7): X=625.5,Y=-2 (should be at baseline 0?)
- Gcaron (U+01E6): X=349,Y=-2.5 (should be at baseline 0?)
- Gstroke (U+01E4): X=349,Y=-2.5 (should be at baseline 0?)
- gcaron (U+01E7): X=349,Y=-2.5 (should be at baseline 0?)
- gstroke (U+01E5): X=349,Y=-2.5 (should be at baseline 0?)
- scircumflex (U+015D): X=180,Y=2.5 (should be at baseline 0?)
- uni01F4 (U+01F4): X=349,Y=-2.5 (should be at baseline 0?)
- uni01F5 (U+01F5): X=349,Y=-2.5 (should be at baseline 0?)
- uni1E08 (U+1E08): X=387.5,Y=2.5 (should be at baseline 0?)
- uni1E09 (U+1E09): X=387.5,Y=2.5 (should be at baseline 0?)
- uni1E20 (U+1E20): X=349,Y=-2.5 (should be at baseline 0?)
- uni1E21 (U+1E21): X=349,Y=-2.5 (should be at baseline 0?)
- uni1E60 (U+1E60): X=180,Y=2.5 (should be at baseline 0?)
- uni1E61 (U+1E61): X=180,Y=2.5 (should be at baseline 0?)
- uni1E64 (U+1E64): X=180,Y=2.5 (should be at baseline 0?)
- uni1E65 (U+1E65): X=180,Y=2.5 (should be at baseline 0?)
- uni1E66 (U+1E66): X=180,Y=2.5 (should be at baseline 0?)
- uni1E67 (U+1E67): X=180,Y=2.5 (should be at baseline 0?)

## Cleared Warning Buckets

- `suspicious_sidebearings` is no longer present in the package-context
  Fontspector report after spacing mark and trademark metric cleanup.

## Fastest Honest Next Step

Review `out/proof/index.html`, then either accept the current warning
floor for first Google Fonts review or make deliberate source edits for
`uni01F5`, metadata reachability, and the remaining implied-curve
alignment warnings. Rerun `make release-check` and this report after
any source or metadata change.
