# Blocksync

Blocksync is a block-like Latin display face by Eli Heuer. The archived Knowledge Triumphant and DIE GNU TYPOGRAFIE posters show it in short, tightly set lines. Capitals supply the construction of many lowercase forms. The designspace has width and weight axes.

## Contents

- [Construction](#construction)
- [Spacing and accents](#spacing-and-accents)
- [Grades](#grades)
- [Baseline QA](#baseline-qa)

## Construction

**R1.** Work in the original 1000-unit em. For example, the Regular O has long vertical sides, cubic shoulders and extrema at −11 and 812 around the 800-unit cap height. Preserve fractional coordinates, optical overshoot and contour correspondence.

**R2.** Read each master at its own width and weight. The normal-width Regular is the designspace default. The six remaining sources cover Regular, Bold and Black at each width extreme. Match the existing weight map (400–900) and width range (75–125). A display test needs both axes, including their intersections. At width 100 the weight must progress from Regular to Black. The compiler interpolates its normal-width Bold and Black supports halfway between the corresponding original width masters. Eli approved the heavier Black after comparing the two proofs.

**R3.** Preserve the distinction between contours and component-built forms. For example, Regular n takes its shape from N. A request to change a lowercase composite requires inspection of its uppercase donor and all other users of that donor.

## Spacing and accents

**R4.** Retain each master's advance, sidebearings, kerning groups and pairs. Compare the widths and rhythm of the two poster titles across both axes before proposing a spacing change.

**R5.** Use the existing base and mark recipes, anchor names and offsets as evidence. Check accented forms beside their decomposed sequences, especially stacked Vietnamese marks, and inspect the condensed Black counters at text size. The inherited composites include placements still awaiting designer review.

## Grades

Both existing green swatches are protected. This mapping preserves the historical colors. A component's green mark alone does not approve the drawings it uses. Treat unmarked glyphs and every component donor as read-only until the designer assigns an appropriate task. The existing blue swatches retain their original values. A new agent draft uses purple.

```toml
[colors.green]
rgba = [[0.04,0.57,0.04,1], [0.67,0.95,0.38,1], [0,1,0,1], [0.09,0.72,0.44,1]]
policy = "Protected. Only the designer approves or regrades."
[colors.blue]
rgba = [[0,0.67,0.91,1], [0.18,0.16,0.78,1]]
policy = "Existing blue grade. Inspect construction before assignment."
[colors.orange]
rgba = [[1,0.6,0.2,1], [0.85,0.26,0.06,1]]
policy = "Preserve the existing drawing as the starting point."
[colors.yellow]
rgba = [[1,0.867,0.2,1]]
policy = "Revise only within the named assignment."
[colors.red]
rgba = [[1,0.251,0.251,1]]
policy = "May be redrawn on assignment."
[colors.purple]
rgba = [[0.54,0.44,0.88,1], [0.5,0,1,1]]
policy = "Agent draft awaiting designer review."
```

## Baseline QA

The pinned profile ran on the seven-master baseline and its 18 static proofs before migration. These checks had existing failures. The normal gate uses the Blocksync-specific exclusions below. The full profile remains relevant for glyph and release review.

```toml
[qa.exclude]
"fontgarden/unitsperem" = "The original em is 1000."
"fontgarden/grid" = "The sources retain fractional coordinates and optical corrections."
"fontgarden/marks_attach" = "Existing combining marks fail attachment tests including the lowercase x."
"fontgarden/precomposed_match" = "When a subset drops precomposed letters, anchor-built fallback differs from existing drawings, including cedilla and ogonek forms."
"googlefonts/font_names" = "The proof-only static fonts carry Condensed and Expanded style names."
# Family-wide online check. Its service rejected repeated identical requests
# across the static proofs. Run it once on the release VF with make namecheck-live.
"fontdata_namecheck" = "Separate live family-name gate before submission."
"googlefonts/repo/dirname_matches_nameid_1" = "The local fonts/ttf and fonts/variable folders are build outputs. Check the downstream package separately."
```
