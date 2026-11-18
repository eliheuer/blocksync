# Proof Review Packet

This generated packet turns the proof output and remaining Fontspector
warnings into a short maintainer review queue. It does not accept or
reject any review item on the maintainer's behalf.

## Summary

- Proof review packet ready: yes
- Proof index: `out/proof/index.html`
- Proof HTML pages linked: 73
- Proof fonts linked: 19
- Proof review local evidence ready: yes
- Proof review final-ready for submission: no
- Final values packet ready: yes
- Remaining warning floor: `googlefonts/metadata/unreachable_subsetting`: 1, `contour_count`: 1, `outline_alignment_miss`: 1

## Review Decisions To Record

| Decision row | Current final answer | Final values key |
| --- | --- | --- |
| Visual proof | Maintainer review required | `visual_proof_decision` |
| Generated Latin Extended and Vietnamese composites | Accept, revise, or defer | `generated_composites_decision` |
| Fontspector warning floor | Accept for first review or schedule source cleanup | `fontspector_warning_decision` |
| Static TTFs | Keep proof-only unless Google Fonts asks | `static_ttf_decision` |

## Proof Pages By Kind

| Kind | Count | First pages |
| --- | ---: | --- |
| diffenator2-report.html | 1 | `out/proof/diffenator2-report.html` |
| glyphs | 18 | `out/proof/Black-diffbrowsers_glyphs.html`, `out/proof/Bold-diffbrowsers_glyphs.html`, `out/proof/Condensed Black-diffbrowsers_glyphs.html` |
| proofer | 18 | `out/proof/Black-diffbrowsers_proofer.html`, `out/proof/Bold-diffbrowsers_proofer.html`, `out/proof/Condensed Black-diffbrowsers_proofer.html` |
| text | 18 | `out/proof/Black-diffbrowsers_text.html`, `out/proof/Bold-diffbrowsers_text.html`, `out/proof/Condensed Black-diffbrowsers_text.html` |
| waterfall | 18 | `out/proof/Black-diffbrowsers_waterfall.html`, `out/proof/Bold-diffbrowsers_waterfall.html`, `out/proof/Condensed Black-diffbrowsers_waterfall.html` |

## Warning Review Items

### Metadata Reachability

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
- `U+25CC DOTTED CIRCLE`

### Contour Count

- `uni01F5` (U+01F5 LATIN SMALL LETTER G WITH ACUTE) is component-based

### Outline Alignment

- Remaining alignment warnings are G/S/Ccedilla-derived implied curve
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
- ... 20 more item(s) in `documentation/fontspector-zero-warning-worklist.md`

## Suggested Review Flow

1. Open `out/proof/index.html` and scan glyphs, text, proofer, and
   waterfall pages across normal, condensed, and expanded instances.
2. Compare generated Latin Extended and Vietnamese composites against
   base glyph rhythm and mark placement.
3. Inspect `uni01F5`, G/S/Ccedilla families, and section-sign pages
   while reviewing the remaining contour/alignment WARNs.
4. Record final decisions in a filled copy of
   `documentation/google-fonts-final-values.template.json`.
5. Validate with `make final-values-check VALUES=/path/to/final-values.json`
   before applying.
