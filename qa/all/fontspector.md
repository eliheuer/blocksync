## FontSpector report

fontspector version: 1.9.0






## Check results




<details><summary>[1] /home/runner/work/blocksync/blocksync/fonts/variable</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> Check for codepoints not covered by METADATA subsets. (googlefonts/metadata/unreachable_subsetting)</summary>
    <div>








- ⚠️ **WARN** /home/runner/work/blocksync/blocksync/fonts/variable/Blocksync[wdth,wght].ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+02D8 BREVE: try adding one of: canadian-aboriginal, yi
* U+02D9 DOT ABOVE: try adding one of: yi, canadian-aboriginal
* U+02DB OGONEK: try adding one of: yi, canadian-aboriginal
* U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: math, tifinagh, cherokee, coptic
* U+0306 COMBINING BREVE: try adding one of: tifinagh, old-permic
* U+0307 COMBINING DOT ABOVE: try adding one of: todhri, syriac, hebrew, tifinagh, malayalam, coptic, canadian-aboriginal, tai-le, old-permic, duployan, math
* U+030A COMBINING RING ABOVE: try adding one of: duployan, syriac
* U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: cherokee, osage
* U+030C COMBINING CARON: try adding one of: cherokee, tai-le
... and 6 others

Or you can add the above codepoints to one of the subsets supported by the font: latin-ext, latin, vietnamese [code: unreachable-subsetting]
  
  

</div>
</details>


</div>
</details>


<details><summary>[3] /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-ExpandedSemiBold.ttf</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>








- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* currency (U+00A4): found 4, expected one of: [2, 6]
* uni01F5 (U+01F5): found 2, expected one of: [3, 4, 5] [code: contour-count]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Are there any misaligned on-curve points? (outline_alignment_miss)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have on-curve points which have potentially incorrect y coordinates:

* - Ccedilla (U+00C7): X=387.5,Y=2.5 (should be at baseline 0?)
* - G (U+0047): X=384.5,Y=-1.5 (should be at baseline 0?)
* - Gbreve (U+011E): X=384.5,Y=-1.5 (should be at baseline 0?)
* - uni0122 (U+0122): X=384.5,Y=-1.5 (should be at baseline 0?)
* - Gdotaccent (U+0120): X=384.5,Y=-1.5 (should be at baseline 0?)
* - ccedilla (U+00E7): X=387.5,Y=2.5 (should be at baseline 0?)
* - g (U+0067): X=384.5,Y=-1.5 (should be at baseline 0?)
* - gbreve (U+011F): X=384.5,Y=-1.5 (should be at baseline 0?)
* - uni0123 (U+0123): X=384.5,Y=-1.5 (should be at baseline 0?)
... and 12 others [code: found-misalignments]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do any segments have colinear vectors? (outline_colinear_vectors)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have colinear vectors:

* trademark (U+2122): from (296.0, 800.0) to (302.0, 800.0) is colinear with segment from (302.0, 800.0) to (392.0, 800.0) [code: found-colinear-vectors]
  
  

</div>
</details>


</div>
</details>


<details><summary>[2] /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-CondensedSemiBold.ttf</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>








- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* currency (U+00A4): found 4, expected one of: [2, 6]
* uni01F5 (U+01F5): found 2, expected one of: [3, 4, 5] [code: contour-count]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Are there any misaligned on-curve points? (outline_alignment_miss)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have on-curve points which have potentially incorrect y coordinates:

* - Ccedilla (U+00C7): X=387.5,Y=2.5 (should be at baseline 0?)
* - ccedilla (U+00E7): X=387.5,Y=2.5 (should be at baseline 0?)
* - at (U+0040): X=85.5,Y=-1.5 (should be at baseline 0?)
* - uni1E08 (U+1E08): X=387.5,Y=2.5 (should be at baseline 0?)
* - uni1E09 (U+1E09): X=387.5,Y=2.5 (should be at baseline 0?) [code: found-misalignments]
  
  

</div>
</details>


</div>
</details>


<details><summary>[2] /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-Medium.ttf</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>








- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* currency (U+00A4): found 4, expected one of: [2, 6]
* uni01F5 (U+01F5): found 2, expected one of: [3, 4, 5] [code: contour-count]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Are there any misaligned on-curve points? (outline_alignment_miss)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have on-curve points which have potentially incorrect y coordinates:

* - Ccedilla (U+00C7): X=387.5,Y=2.5 (should be at baseline 0?)
* - G (U+0047): X=349,Y=-2.5 (should be at baseline 0?)
* - Gbreve (U+011E): X=349,Y=-2.5 (should be at baseline 0?)
* - uni0122 (U+0122): X=349,Y=-2.5 (should be at baseline 0?)
* - Gdotaccent (U+0120): X=349,Y=-2.5 (should be at baseline 0?)
* - ccedilla (U+00E7): X=387.5,Y=2.5 (should be at baseline 0?)
* - g (U+0067): X=349,Y=-2.5 (should be at baseline 0?)
* - gbreve (U+011F): X=349,Y=-2.5 (should be at baseline 0?)
* - uni0123 (U+0123): X=349,Y=-2.5 (should be at baseline 0?)
... and 11 others [code: found-misalignments]
  
  

</div>
</details>


</div>
</details>


<details><summary>[2] /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-CondensedBold.ttf</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>








- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* currency (U+00A4): found 4, expected one of: [2, 6]
* uni01F5 (U+01F5): found 2, expected one of: [3, 4, 5] [code: contour-count]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Are there any misaligned on-curve points? (outline_alignment_miss)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have on-curve points which have potentially incorrect y coordinates:

* - Ccedilla (U+00C7): X=387.5,Y=2.5 (should be at baseline 0?)
* - ccedilla (U+00E7): X=387.5,Y=2.5 (should be at baseline 0?)
* - at (U+0040): X=85.5,Y=-1.5 (should be at baseline 0?)
* - uni1E08 (U+1E08): X=387.5,Y=2.5 (should be at baseline 0?)
* - uni1E09 (U+1E09): X=387.5,Y=2.5 (should be at baseline 0?) [code: found-misalignments]
  
  

</div>
</details>


</div>
</details>


<details><summary>[2] /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-CondensedRegular.ttf</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>








- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* currency (U+00A4): found 4, expected one of: [2, 6]
* uni01F5 (U+01F5): found 2, expected one of: [3, 4, 5] [code: contour-count]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Are there any misaligned on-curve points? (outline_alignment_miss)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have on-curve points which have potentially incorrect y coordinates:

* - Ccedilla (U+00C7): X=387.5,Y=2.5 (should be at baseline 0?)
* - ccedilla (U+00E7): X=387.5,Y=2.5 (should be at baseline 0?)
* - at (U+0040): X=85.5,Y=-1.5 (should be at baseline 0?)
* - uni1E08 (U+1E08): X=387.5,Y=2.5 (should be at baseline 0?)
* - uni1E09 (U+1E09): X=387.5,Y=2.5 (should be at baseline 0?) [code: found-misalignments]
  
  

</div>
</details>


</div>
</details>


<details><summary>[2] /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-SemiBold.ttf</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>








- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* currency (U+00A4): found 4, expected one of: [2, 6]
* uni01F5 (U+01F5): found 2, expected one of: [3, 4, 5] [code: contour-count]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Are there any misaligned on-curve points? (outline_alignment_miss)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have on-curve points which have potentially incorrect y coordinates:

* - Ccedilla (U+00C7): X=387.5,Y=2.5 (should be at baseline 0?)
* - G (U+0047): X=349,Y=-2.5 (should be at baseline 0?)
* - Gbreve (U+011E): X=349,Y=-2.5 (should be at baseline 0?)
* - uni0122 (U+0122): X=349,Y=-2.5 (should be at baseline 0?)
* - Gdotaccent (U+0120): X=349,Y=-2.5 (should be at baseline 0?)
* - ccedilla (U+00E7): X=387.5,Y=2.5 (should be at baseline 0?)
* - g (U+0067): X=349,Y=-2.5 (should be at baseline 0?)
* - gbreve (U+011F): X=349,Y=-2.5 (should be at baseline 0?)
* - uni0123 (U+0123): X=349,Y=-2.5 (should be at baseline 0?)
... and 11 others [code: found-misalignments]
  
  

</div>
</details>


</div>
</details>


<details><summary>[4] /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-ExpandedBlack.ttf</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>








- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* currency (U+00A4): found 4, expected one of: [2, 6]
* uni01F5 (U+01F5): found 2, expected one of: [3, 4, 5] [code: contour-count]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Are there any misaligned on-curve points? (outline_alignment_miss)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have on-curve points which have potentially incorrect y coordinates:

* - Ccedilla (U+00C7): X=387.5,Y=2.5 (should be at baseline 0?)
* - G (U+0047): X=193.5,Y=2 (should be at baseline 0?)
* - G (U+0047): X=389,Y=2 (should be at baseline 0?)
* - Gbreve (U+011E): X=193.5,Y=2 (should be at baseline 0?)
* - Gbreve (U+011E): X=389,Y=2 (should be at baseline 0?)
* - uni0122 (U+0122): X=193.5,Y=2 (should be at baseline 0?)
* - uni0122 (U+0122): X=389,Y=2 (should be at baseline 0?)
* - Gdotaccent (U+0120): X=193.5,Y=2 (should be at baseline 0?)
* - Gdotaccent (U+0120): X=389,Y=2 (should be at baseline 0?)
... and 43 others [code: found-misalignments]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check there are no overlapping path segments (overlapping_path_segments)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have overlapping path segments:

* tcaron (U+0165): Quad(QuadBez { p0: (423.0, 800.0), p1: (449.0, 800.0), p2: (459.0, 790.0) }) has the same coordinates as a previous segment.
* tcaron (U+0165): Quad(QuadBez { p0: (459.0, 790.0), p1: (469.0, 780.0), p2: (469.0, 754.0) }) has the same coordinates as a previous segment. [code: overlapping-path-segments]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do outlines contain any semi-vertical or semi-horizontal lines? (outline_semi_vertical)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have semi-vertical/semi-horizontal lines:

* M (U+004D): Line(Line { p0: (381.0, 754.0), p1: (384.0, 387.0) }) (angle: -89.53 degrees, expected: -90.00 degrees)
* M (U+004D): Line(Line { p0: (503.0, 406.0), p1: (504.0, 46.0) }) (angle: -89.84 degrees, expected: -90.00 degrees)
* W (U+0057): Line(Line { p0: (417.0, 425.0), p1: (414.0, 46.0) }) (angle: -90.45 degrees, expected: -90.00 degrees)
* Wacute (U+1E82): Line(Line { p0: (417.0, 425.0), p1: (414.0, 46.0) }) (angle: -90.45 degrees, expected: -90.00 degrees)
* Wcircumflex (U+0174): Line(Line { p0: (417.0, 425.0), p1: (414.0, 46.0) }) (angle: -90.45 degrees, expected: -90.00 degrees)
* Wdieresis (U+1E84): Line(Line { p0: (417.0, 425.0), p1: (414.0, 46.0) }) (angle: -90.45 degrees, expected: -90.00 degrees)
* Wgrave (U+1E80): Line(Line { p0: (417.0, 425.0), p1: (414.0, 46.0) }) (angle: -90.45 degrees, expected: -90.00 degrees)
* Y (U+0059): Line(Line { p0: (303.0, 606.0), p1: (304.0, 766.0) }) (angle: 89.64 degrees, expected: 90.00 degrees)
* Yacute (U+00DD): Line(Line { p0: (303.0, 606.0), p1: (304.0, 766.0) }) (angle: 89.64 degrees, expected: 90.00 degrees)
... and 39 others [code: found-semi-vertical]
  
  

</div>
</details>


</div>
</details>


<details><summary>[2] /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-CondensedMedium.ttf</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>








- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* currency (U+00A4): found 4, expected one of: [2, 6]
* uni01F5 (U+01F5): found 2, expected one of: [3, 4, 5] [code: contour-count]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Are there any misaligned on-curve points? (outline_alignment_miss)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have on-curve points which have potentially incorrect y coordinates:

* - Ccedilla (U+00C7): X=387.5,Y=2.5 (should be at baseline 0?)
* - ccedilla (U+00E7): X=387.5,Y=2.5 (should be at baseline 0?)
* - at (U+0040): X=85.5,Y=-1.5 (should be at baseline 0?)
* - uni1E08 (U+1E08): X=387.5,Y=2.5 (should be at baseline 0?)
* - uni1E09 (U+1E09): X=387.5,Y=2.5 (should be at baseline 0?) [code: found-misalignments]
  
  

</div>
</details>


</div>
</details>


<details><summary>[2] /home/runner/work/blocksync/blocksync/fonts/ttf</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> Ensure Fonts have 'ital' STAT axis. (opentype/STAT/ital_axis)</summary>
    <div>








- ⚠️ **WARN** Static font is missing the 'STAT' table. [code: no-stat-table]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check for codepoints not covered by METADATA subsets. (googlefonts/metadata/unreachable_subsetting)</summary>
    <div>








- ⚠️ **WARN** /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-Black.ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+02D8 BREVE: try adding one of: canadian-aboriginal, yi
* U+02D9 DOT ABOVE: try adding one of: yi, canadian-aboriginal
* U+02DB OGONEK: try adding one of: yi, canadian-aboriginal
* U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: math, tifinagh, cherokee, coptic
* U+0306 COMBINING BREVE: try adding one of: tifinagh, old-permic
* U+0307 COMBINING DOT ABOVE: try adding one of: todhri, syriac, hebrew, tifinagh, malayalam, coptic, canadian-aboriginal, tai-le, old-permic, duployan, math
* U+030A COMBINING RING ABOVE: try adding one of: duployan, syriac
* U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: cherokee, osage
* U+030C COMBINING CARON: try adding one of: cherokee, tai-le
... and 6 others

Or you can add the above codepoints to one of the subsets supported by the font: latin-ext, latin, vietnamese [code: unreachable-subsetting]
  
  


- ⚠️ **WARN** /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-Bold.ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+02D8 BREVE: try adding one of: canadian-aboriginal, yi
* U+02D9 DOT ABOVE: try adding one of: yi, canadian-aboriginal
* U+02DB OGONEK: try adding one of: yi, canadian-aboriginal
* U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: math, tifinagh, cherokee, coptic
* U+0306 COMBINING BREVE: try adding one of: tifinagh, old-permic
* U+0307 COMBINING DOT ABOVE: try adding one of: todhri, syriac, hebrew, tifinagh, malayalam, coptic, canadian-aboriginal, tai-le, old-permic, duployan, math
* U+030A COMBINING RING ABOVE: try adding one of: duployan, syriac
* U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: cherokee, osage
* U+030C COMBINING CARON: try adding one of: cherokee, tai-le
... and 6 others

Or you can add the above codepoints to one of the subsets supported by the font: latin-ext, latin, vietnamese [code: unreachable-subsetting]
  
  


- ⚠️ **WARN** /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-CondensedBlack.ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+02D8 BREVE: try adding one of: canadian-aboriginal, yi
* U+02D9 DOT ABOVE: try adding one of: yi, canadian-aboriginal
* U+02DB OGONEK: try adding one of: yi, canadian-aboriginal
* U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: math, tifinagh, cherokee, coptic
* U+0306 COMBINING BREVE: try adding one of: tifinagh, old-permic
* U+0307 COMBINING DOT ABOVE: try adding one of: todhri, syriac, hebrew, tifinagh, malayalam, coptic, canadian-aboriginal, tai-le, old-permic, duployan, math
* U+030A COMBINING RING ABOVE: try adding one of: duployan, syriac
* U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: cherokee, osage
* U+030C COMBINING CARON: try adding one of: cherokee, tai-le
... and 6 others

Or you can add the above codepoints to one of the subsets supported by the font: latin-ext, latin, vietnamese [code: unreachable-subsetting]
  
  


- ⚠️ **WARN** /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-CondensedBold.ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+02D8 BREVE: try adding one of: canadian-aboriginal, yi
* U+02D9 DOT ABOVE: try adding one of: yi, canadian-aboriginal
* U+02DB OGONEK: try adding one of: yi, canadian-aboriginal
* U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: math, tifinagh, cherokee, coptic
* U+0306 COMBINING BREVE: try adding one of: tifinagh, old-permic
* U+0307 COMBINING DOT ABOVE: try adding one of: todhri, syriac, hebrew, tifinagh, malayalam, coptic, canadian-aboriginal, tai-le, old-permic, duployan, math
* U+030A COMBINING RING ABOVE: try adding one of: duployan, syriac
* U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: cherokee, osage
* U+030C COMBINING CARON: try adding one of: cherokee, tai-le
... and 6 others

Or you can add the above codepoints to one of the subsets supported by the font: latin-ext, latin, vietnamese [code: unreachable-subsetting]
  
  


- ⚠️ **WARN** /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-CondensedExtraBold.ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+02D8 BREVE: try adding one of: canadian-aboriginal, yi
* U+02D9 DOT ABOVE: try adding one of: yi, canadian-aboriginal
* U+02DB OGONEK: try adding one of: yi, canadian-aboriginal
* U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: math, tifinagh, cherokee, coptic
* U+0306 COMBINING BREVE: try adding one of: tifinagh, old-permic
* U+0307 COMBINING DOT ABOVE: try adding one of: todhri, syriac, hebrew, tifinagh, malayalam, coptic, canadian-aboriginal, tai-le, old-permic, duployan, math
* U+030A COMBINING RING ABOVE: try adding one of: duployan, syriac
* U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: cherokee, osage
* U+030C COMBINING CARON: try adding one of: cherokee, tai-le
... and 6 others

Or you can add the above codepoints to one of the subsets supported by the font: latin-ext, latin, vietnamese [code: unreachable-subsetting]
  
  


- ⚠️ **WARN** /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-CondensedMedium.ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+02D8 BREVE: try adding one of: canadian-aboriginal, yi
* U+02D9 DOT ABOVE: try adding one of: yi, canadian-aboriginal
* U+02DB OGONEK: try adding one of: yi, canadian-aboriginal
* U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: math, tifinagh, cherokee, coptic
* U+0306 COMBINING BREVE: try adding one of: tifinagh, old-permic
* U+0307 COMBINING DOT ABOVE: try adding one of: todhri, syriac, hebrew, tifinagh, malayalam, coptic, canadian-aboriginal, tai-le, old-permic, duployan, math
* U+030A COMBINING RING ABOVE: try adding one of: duployan, syriac
* U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: cherokee, osage
* U+030C COMBINING CARON: try adding one of: cherokee, tai-le
... and 6 others

Or you can add the above codepoints to one of the subsets supported by the font: latin-ext, latin, vietnamese [code: unreachable-subsetting]
  
  


- ⚠️ **WARN** /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-CondensedRegular.ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+02D8 BREVE: try adding one of: canadian-aboriginal, yi
* U+02D9 DOT ABOVE: try adding one of: yi, canadian-aboriginal
* U+02DB OGONEK: try adding one of: yi, canadian-aboriginal
* U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: math, tifinagh, cherokee, coptic
* U+0306 COMBINING BREVE: try adding one of: tifinagh, old-permic
* U+0307 COMBINING DOT ABOVE: try adding one of: todhri, syriac, hebrew, tifinagh, malayalam, coptic, canadian-aboriginal, tai-le, old-permic, duployan, math
* U+030A COMBINING RING ABOVE: try adding one of: duployan, syriac
* U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: cherokee, osage
* U+030C COMBINING CARON: try adding one of: cherokee, tai-le
... and 6 others

Or you can add the above codepoints to one of the subsets supported by the font: latin-ext, latin, vietnamese [code: unreachable-subsetting]
  
  


- ⚠️ **WARN** /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-CondensedSemiBold.ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+02D8 BREVE: try adding one of: canadian-aboriginal, yi
* U+02D9 DOT ABOVE: try adding one of: yi, canadian-aboriginal
* U+02DB OGONEK: try adding one of: yi, canadian-aboriginal
* U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: math, tifinagh, cherokee, coptic
* U+0306 COMBINING BREVE: try adding one of: tifinagh, old-permic
* U+0307 COMBINING DOT ABOVE: try adding one of: todhri, syriac, hebrew, tifinagh, malayalam, coptic, canadian-aboriginal, tai-le, old-permic, duployan, math
* U+030A COMBINING RING ABOVE: try adding one of: duployan, syriac
* U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: cherokee, osage
* U+030C COMBINING CARON: try adding one of: cherokee, tai-le
... and 6 others

Or you can add the above codepoints to one of the subsets supported by the font: latin-ext, latin, vietnamese [code: unreachable-subsetting]
  
  


- ⚠️ **WARN** /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-ExpandedBlack.ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+02D8 BREVE: try adding one of: canadian-aboriginal, yi
* U+02D9 DOT ABOVE: try adding one of: yi, canadian-aboriginal
* U+02DB OGONEK: try adding one of: yi, canadian-aboriginal
* U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: math, tifinagh, cherokee, coptic
* U+0306 COMBINING BREVE: try adding one of: tifinagh, old-permic
* U+0307 COMBINING DOT ABOVE: try adding one of: todhri, syriac, hebrew, tifinagh, malayalam, coptic, canadian-aboriginal, tai-le, old-permic, duployan, math
* U+030A COMBINING RING ABOVE: try adding one of: duployan, syriac
* U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: cherokee, osage
* U+030C COMBINING CARON: try adding one of: cherokee, tai-le
... and 6 others

Or you can add the above codepoints to one of the subsets supported by the font: latin-ext, latin, vietnamese [code: unreachable-subsetting]
  
  


- ⚠️ **WARN** /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-ExpandedBold.ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+02D8 BREVE: try adding one of: canadian-aboriginal, yi
* U+02D9 DOT ABOVE: try adding one of: yi, canadian-aboriginal
* U+02DB OGONEK: try adding one of: yi, canadian-aboriginal
* U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: math, tifinagh, cherokee, coptic
* U+0306 COMBINING BREVE: try adding one of: tifinagh, old-permic
* U+0307 COMBINING DOT ABOVE: try adding one of: todhri, syriac, hebrew, tifinagh, malayalam, coptic, canadian-aboriginal, tai-le, old-permic, duployan, math
* U+030A COMBINING RING ABOVE: try adding one of: duployan, syriac
* U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: cherokee, osage
* U+030C COMBINING CARON: try adding one of: cherokee, tai-le
... and 6 others

Or you can add the above codepoints to one of the subsets supported by the font: latin-ext, latin, vietnamese [code: unreachable-subsetting]
  
  


- ⚠️ **WARN** /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-ExpandedExtraBold.ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+02D8 BREVE: try adding one of: canadian-aboriginal, yi
* U+02D9 DOT ABOVE: try adding one of: yi, canadian-aboriginal
* U+02DB OGONEK: try adding one of: yi, canadian-aboriginal
* U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: math, tifinagh, cherokee, coptic
* U+0306 COMBINING BREVE: try adding one of: tifinagh, old-permic
* U+0307 COMBINING DOT ABOVE: try adding one of: todhri, syriac, hebrew, tifinagh, malayalam, coptic, canadian-aboriginal, tai-le, old-permic, duployan, math
* U+030A COMBINING RING ABOVE: try adding one of: duployan, syriac
* U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: cherokee, osage
* U+030C COMBINING CARON: try adding one of: cherokee, tai-le
... and 6 others

Or you can add the above codepoints to one of the subsets supported by the font: latin-ext, latin, vietnamese [code: unreachable-subsetting]
  
  


- ⚠️ **WARN** /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-ExpandedMedium.ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+02D8 BREVE: try adding one of: canadian-aboriginal, yi
* U+02D9 DOT ABOVE: try adding one of: yi, canadian-aboriginal
* U+02DB OGONEK: try adding one of: yi, canadian-aboriginal
* U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: math, tifinagh, cherokee, coptic
* U+0306 COMBINING BREVE: try adding one of: tifinagh, old-permic
* U+0307 COMBINING DOT ABOVE: try adding one of: todhri, syriac, hebrew, tifinagh, malayalam, coptic, canadian-aboriginal, tai-le, old-permic, duployan, math
* U+030A COMBINING RING ABOVE: try adding one of: duployan, syriac
* U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: cherokee, osage
* U+030C COMBINING CARON: try adding one of: cherokee, tai-le
... and 6 others

Or you can add the above codepoints to one of the subsets supported by the font: latin-ext, latin, vietnamese [code: unreachable-subsetting]
  
  


- ⚠️ **WARN** /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-ExpandedRegular.ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+02D8 BREVE: try adding one of: canadian-aboriginal, yi
* U+02D9 DOT ABOVE: try adding one of: yi, canadian-aboriginal
* U+02DB OGONEK: try adding one of: yi, canadian-aboriginal
* U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: math, tifinagh, cherokee, coptic
* U+0306 COMBINING BREVE: try adding one of: tifinagh, old-permic
* U+0307 COMBINING DOT ABOVE: try adding one of: todhri, syriac, hebrew, tifinagh, malayalam, coptic, canadian-aboriginal, tai-le, old-permic, duployan, math
* U+030A COMBINING RING ABOVE: try adding one of: duployan, syriac
* U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: cherokee, osage
* U+030C COMBINING CARON: try adding one of: cherokee, tai-le
... and 6 others

Or you can add the above codepoints to one of the subsets supported by the font: latin-ext, latin, vietnamese [code: unreachable-subsetting]
  
  


- ⚠️ **WARN** /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-ExpandedSemiBold.ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+02D8 BREVE: try adding one of: canadian-aboriginal, yi
* U+02D9 DOT ABOVE: try adding one of: yi, canadian-aboriginal
* U+02DB OGONEK: try adding one of: yi, canadian-aboriginal
* U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: math, tifinagh, cherokee, coptic
* U+0306 COMBINING BREVE: try adding one of: tifinagh, old-permic
* U+0307 COMBINING DOT ABOVE: try adding one of: todhri, syriac, hebrew, tifinagh, malayalam, coptic, canadian-aboriginal, tai-le, old-permic, duployan, math
* U+030A COMBINING RING ABOVE: try adding one of: duployan, syriac
* U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: cherokee, osage
* U+030C COMBINING CARON: try adding one of: cherokee, tai-le
... and 6 others

Or you can add the above codepoints to one of the subsets supported by the font: latin-ext, latin, vietnamese [code: unreachable-subsetting]
  
  


- ⚠️ **WARN** /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-ExtraBold.ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+02D8 BREVE: try adding one of: canadian-aboriginal, yi
* U+02D9 DOT ABOVE: try adding one of: yi, canadian-aboriginal
* U+02DB OGONEK: try adding one of: yi, canadian-aboriginal
* U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: math, tifinagh, cherokee, coptic
* U+0306 COMBINING BREVE: try adding one of: tifinagh, old-permic
* U+0307 COMBINING DOT ABOVE: try adding one of: todhri, syriac, hebrew, tifinagh, malayalam, coptic, canadian-aboriginal, tai-le, old-permic, duployan, math
* U+030A COMBINING RING ABOVE: try adding one of: duployan, syriac
* U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: cherokee, osage
* U+030C COMBINING CARON: try adding one of: cherokee, tai-le
... and 6 others

Or you can add the above codepoints to one of the subsets supported by the font: latin-ext, latin, vietnamese [code: unreachable-subsetting]
  
  


- ⚠️ **WARN** /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-Medium.ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+02D8 BREVE: try adding one of: canadian-aboriginal, yi
* U+02D9 DOT ABOVE: try adding one of: yi, canadian-aboriginal
* U+02DB OGONEK: try adding one of: yi, canadian-aboriginal
* U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: math, tifinagh, cherokee, coptic
* U+0306 COMBINING BREVE: try adding one of: tifinagh, old-permic
* U+0307 COMBINING DOT ABOVE: try adding one of: todhri, syriac, hebrew, tifinagh, malayalam, coptic, canadian-aboriginal, tai-le, old-permic, duployan, math
* U+030A COMBINING RING ABOVE: try adding one of: duployan, syriac
* U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: cherokee, osage
* U+030C COMBINING CARON: try adding one of: cherokee, tai-le
... and 6 others

Or you can add the above codepoints to one of the subsets supported by the font: latin-ext, latin, vietnamese [code: unreachable-subsetting]
  
  


- ⚠️ **WARN** /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-Regular.ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+02D8 BREVE: try adding one of: canadian-aboriginal, yi
* U+02D9 DOT ABOVE: try adding one of: yi, canadian-aboriginal
* U+02DB OGONEK: try adding one of: yi, canadian-aboriginal
* U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: math, tifinagh, cherokee, coptic
* U+0306 COMBINING BREVE: try adding one of: tifinagh, old-permic
* U+0307 COMBINING DOT ABOVE: try adding one of: todhri, syriac, hebrew, tifinagh, malayalam, coptic, canadian-aboriginal, tai-le, old-permic, duployan, math
* U+030A COMBINING RING ABOVE: try adding one of: duployan, syriac
* U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: cherokee, osage
* U+030C COMBINING CARON: try adding one of: cherokee, tai-le
... and 6 others

Or you can add the above codepoints to one of the subsets supported by the font: latin-ext, latin, vietnamese [code: unreachable-subsetting]
  
  


- ⚠️ **WARN** /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-SemiBold.ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+02D8 BREVE: try adding one of: canadian-aboriginal, yi
* U+02D9 DOT ABOVE: try adding one of: yi, canadian-aboriginal
* U+02DB OGONEK: try adding one of: yi, canadian-aboriginal
* U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: math, tifinagh, cherokee, coptic
* U+0306 COMBINING BREVE: try adding one of: tifinagh, old-permic
* U+0307 COMBINING DOT ABOVE: try adding one of: todhri, syriac, hebrew, tifinagh, malayalam, coptic, canadian-aboriginal, tai-le, old-permic, duployan, math
* U+030A COMBINING RING ABOVE: try adding one of: duployan, syriac
* U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: cherokee, osage
* U+030C COMBINING CARON: try adding one of: cherokee, tai-le
... and 6 others

Or you can add the above codepoints to one of the subsets supported by the font: latin-ext, latin, vietnamese [code: unreachable-subsetting]
  
  

</div>
</details>


</div>
</details>


<details><summary>[4] /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-CondensedBlack.ttf</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>








- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* currency (U+00A4): found 4, expected one of: [2, 6]
* uni01F5 (U+01F5): found 2, expected one of: [3, 4, 5] [code: contour-count]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Are there any misaligned on-curve points? (outline_alignment_miss)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have on-curve points which have potentially incorrect y coordinates:

* - Ccedilla (U+00C7): X=387.5,Y=2.5 (should be at baseline 0?)
* - ccedilla (U+00E7): X=387.5,Y=2.5 (should be at baseline 0?)
* - uni1E08 (U+1E08): X=387.5,Y=2.5 (should be at baseline 0?)
* - uni1E09 (U+1E09): X=387.5,Y=2.5 (should be at baseline 0?) [code: found-misalignments]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check there are no overlapping path segments (overlapping_path_segments)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have overlapping path segments:

* ellipsis (U+2026): Line(Line { p0: (263.0, 46.0), p1: (263.0, 194.0) }) has the same coordinates as a previous segment.
* ellipsis (U+2026): Line(Line { p0: (503.0, 46.0), p1: (503.0, 194.0) }) has the same coordinates as a previous segment. [code: overlapping-path-segments]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do outlines contain any semi-vertical or semi-horizontal lines? (outline_semi_vertical)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have semi-vertical/semi-horizontal lines:

* M (U+004D): Line(Line { p0: (400.0, 406.0), p1: (401.0, 46.0) }) (angle: -89.84 degrees, expected: -90.00 degrees)
* W (U+0057): Line(Line { p0: (360.0, 425.0), p1: (357.0, 46.0) }) (angle: -90.45 degrees, expected: -90.00 degrees)
* Wacute (U+1E82): Line(Line { p0: (360.0, 425.0), p1: (357.0, 46.0) }) (angle: -90.45 degrees, expected: -90.00 degrees)
* Wcircumflex (U+0174): Line(Line { p0: (360.0, 425.0), p1: (357.0, 46.0) }) (angle: -90.45 degrees, expected: -90.00 degrees)
* Wdieresis (U+1E84): Line(Line { p0: (360.0, 425.0), p1: (357.0, 46.0) }) (angle: -90.45 degrees, expected: -90.00 degrees)
* Wgrave (U+1E80): Line(Line { p0: (360.0, 425.0), p1: (357.0, 46.0) }) (angle: -90.45 degrees, expected: -90.00 degrees)
* m (U+006D): Line(Line { p0: (400.0, 406.0), p1: (401.0, 46.0) }) (angle: -89.84 degrees, expected: -90.00 degrees)
* w (U+0077): Line(Line { p0: (360.0, 425.0), p1: (357.0, 46.0) }) (angle: -90.45 degrees, expected: -90.00 degrees)
* wacute (U+1E83): Line(Line { p0: (360.0, 425.0), p1: (357.0, 46.0) }) (angle: -90.45 degrees, expected: -90.00 degrees)
... and 13 others [code: found-semi-vertical]
  
  

</div>
</details>


</div>
</details>


<details><summary>[4] /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-CondensedExtraBold.ttf</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>








- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* currency (U+00A4): found 4, expected one of: [2, 6]
* uni01F5 (U+01F5): found 2, expected one of: [3, 4, 5] [code: contour-count]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Combined length of family and style must not exceed 32 characters. (name/family_and_style_max_length)</summary>
    <div>








- ⚠️ **WARN** Name ID 6 'PostScript Name' exceeds 27 characters (1 characters too long). This has been found to cause problems with PostScript printers, especially on Mac platforms. [code: nameid6-too-long]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Are there any misaligned on-curve points? (outline_alignment_miss)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have on-curve points which have potentially incorrect y coordinates:

* - Ccedilla (U+00C7): X=387.5,Y=2.5 (should be at baseline 0?)
* - ccedilla (U+00E7): X=387.5,Y=2.5 (should be at baseline 0?)
* - uni1E08 (U+1E08): X=387.5,Y=2.5 (should be at baseline 0?)
* - uni1E09 (U+1E09): X=387.5,Y=2.5 (should be at baseline 0?) [code: found-misalignments]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do outlines contain any semi-vertical or semi-horizontal lines? (outline_semi_vertical)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have semi-vertical/semi-horizontal lines:

* K (U+004B): Line(Line { p0: (242.0, 326.0), p1: (243.0, 46.0) }) (angle: -89.80 degrees, expected: -90.00 degrees)
* uni0136 (U+0136): Line(Line { p0: (242.0, 326.0), p1: (243.0, 46.0) }) (angle: -89.80 degrees, expected: -90.00 degrees)
* k (U+006B): Line(Line { p0: (242.0, 326.0), p1: (243.0, 46.0) }) (angle: -89.80 degrees, expected: -90.00 degrees)
* uni0137 (U+0137): Line(Line { p0: (242.0, 326.0), p1: (243.0, 46.0) }) (angle: -89.80 degrees, expected: -90.00 degrees)
* Kcaron (U+01E8): Line(Line { p0: (242.0, 326.0), p1: (243.0, 46.0) }) (angle: -89.80 degrees, expected: -90.00 degrees)
* kcaron (U+01E9): Line(Line { p0: (242.0, 326.0), p1: (243.0, 46.0) }) (angle: -89.80 degrees, expected: -90.00 degrees)
* uni1E30 (U+1E30): Line(Line { p0: (242.0, 326.0), p1: (243.0, 46.0) }) (angle: -89.80 degrees, expected: -90.00 degrees)
* uni1E31 (U+1E31): Line(Line { p0: (242.0, 326.0), p1: (243.0, 46.0) }) (angle: -89.80 degrees, expected: -90.00 degrees)
* uni1E32 (U+1E32): Line(Line { p0: (242.0, 326.0), p1: (243.0, 46.0) }) (angle: -89.80 degrees, expected: -90.00 degrees)
... and 1 others [code: found-semi-vertical]
  
  

</div>
</details>


</div>
</details>


<details><summary>[2] /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-Regular.ttf</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>








- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* currency (U+00A4): found 4, expected one of: [2, 6]
* uni01F5 (U+01F5): found 2, expected one of: [3, 4, 5] [code: contour-count]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Are there any misaligned on-curve points? (outline_alignment_miss)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have on-curve points which have potentially incorrect y coordinates:

* - Ccedilla (U+00C7): X=387.5,Y=2.5 (should be at baseline 0?)
* - G (U+0047): X=349,Y=-2.5 (should be at baseline 0?)
* - Gbreve (U+011E): X=349,Y=-2.5 (should be at baseline 0?)
* - uni0122 (U+0122): X=349,Y=-2.5 (should be at baseline 0?)
* - Gdotaccent (U+0120): X=349,Y=-2.5 (should be at baseline 0?)
* - ccedilla (U+00E7): X=387.5,Y=2.5 (should be at baseline 0?)
* - g (U+0067): X=349,Y=-2.5 (should be at baseline 0?)
* - gbreve (U+011F): X=349,Y=-2.5 (should be at baseline 0?)
* - uni0123 (U+0123): X=349,Y=-2.5 (should be at baseline 0?)
... and 11 others [code: found-misalignments]
  
  

</div>
</details>


</div>
</details>


<details><summary>[3] /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-ExpandedBold.ttf</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>








- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* currency (U+00A4): found 4, expected one of: [2, 6]
* uni01F5 (U+01F5): found 2, expected one of: [3, 4, 5] [code: contour-count]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Are there any misaligned on-curve points? (outline_alignment_miss)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have on-curve points which have potentially incorrect y coordinates:

* - Ccedilla (U+00C7): X=387.5,Y=2.5 (should be at baseline 0?)
* - G (U+0047): X=384.5,Y=-1.5 (should be at baseline 0?)
* - Gbreve (U+011E): X=384.5,Y=-1.5 (should be at baseline 0?)
* - uni0122 (U+0122): X=384.5,Y=-1.5 (should be at baseline 0?)
* - Gdotaccent (U+0120): X=384.5,Y=-1.5 (should be at baseline 0?)
* - ccedilla (U+00E7): X=387.5,Y=2.5 (should be at baseline 0?)
* - g (U+0067): X=384.5,Y=-1.5 (should be at baseline 0?)
* - gbreve (U+011F): X=384.5,Y=-1.5 (should be at baseline 0?)
* - uni0123 (U+0123): X=384.5,Y=-1.5 (should be at baseline 0?)
... and 12 others [code: found-misalignments]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do any segments have colinear vectors? (outline_colinear_vectors)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have colinear vectors:

* trademark (U+2122): from (296.0, 800.0) to (302.0, 800.0) is colinear with segment from (302.0, 800.0) to (392.0, 800.0) [code: found-colinear-vectors]
  
  

</div>
</details>


</div>
</details>


<details><summary>[2] /home/runner/work/blocksync/blocksync/fonts/variable/Blocksync[wdth,wght].ttf</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>








- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* uni01F5 (U+01F5): found 2, expected one of: [3, 4, 5] [code: contour-count]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Are there any misaligned on-curve points? (outline_alignment_miss)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have on-curve points which have potentially incorrect y coordinates:

* - Ccedilla (U+00C7): X=387.5,Y=2.5 (should be at baseline 0?)
* - G (U+0047): X=349,Y=-2.5 (should be at baseline 0?)
* - Gbreve (U+011E): X=349,Y=-2.5 (should be at baseline 0?)
* - uni0122 (U+0122): X=349,Y=-2.5 (should be at baseline 0?)
* - Gdotaccent (U+0120): X=349,Y=-2.5 (should be at baseline 0?)
* - S (U+0053): X=180,Y=2.5 (should be at baseline 0?)
* - Sacute (U+015A): X=180,Y=2.5 (should be at baseline 0?)
* - Scaron (U+0160): X=180,Y=2.5 (should be at baseline 0?)
* - Scircumflex (U+015C): X=180,Y=2.5 (should be at baseline 0?)
... and 29 others [code: found-misalignments]
  
  

</div>
</details>


</div>
</details>


<details><summary>[3] /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-ExpandedMedium.ttf</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>








- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* currency (U+00A4): found 4, expected one of: [2, 6]
* uni01F5 (U+01F5): found 2, expected one of: [3, 4, 5] [code: contour-count]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Are there any misaligned on-curve points? (outline_alignment_miss)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have on-curve points which have potentially incorrect y coordinates:

* - Ccedilla (U+00C7): X=387.5,Y=2.5 (should be at baseline 0?)
* - G (U+0047): X=384.5,Y=-1.5 (should be at baseline 0?)
* - Gbreve (U+011E): X=384.5,Y=-1.5 (should be at baseline 0?)
* - uni0122 (U+0122): X=384.5,Y=-1.5 (should be at baseline 0?)
* - Gdotaccent (U+0120): X=384.5,Y=-1.5 (should be at baseline 0?)
* - ccedilla (U+00E7): X=387.5,Y=2.5 (should be at baseline 0?)
* - g (U+0067): X=384.5,Y=-1.5 (should be at baseline 0?)
* - gbreve (U+011F): X=384.5,Y=-1.5 (should be at baseline 0?)
* - uni0123 (U+0123): X=384.5,Y=-1.5 (should be at baseline 0?)
... and 12 others [code: found-misalignments]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do any segments have colinear vectors? (outline_colinear_vectors)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have colinear vectors:

* trademark (U+2122): from (296.0, 800.0) to (302.0, 800.0) is colinear with segment from (302.0, 800.0) to (392.0, 800.0) [code: found-colinear-vectors]
  
  

</div>
</details>


</div>
</details>


<details><summary>[3] /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-ExpandedRegular.ttf</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>








- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* currency (U+00A4): found 4, expected one of: [2, 6]
* uni01F5 (U+01F5): found 2, expected one of: [3, 4, 5] [code: contour-count]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Are there any misaligned on-curve points? (outline_alignment_miss)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have on-curve points which have potentially incorrect y coordinates:

* - Ccedilla (U+00C7): X=387.5,Y=2.5 (should be at baseline 0?)
* - G (U+0047): X=384.5,Y=-1.5 (should be at baseline 0?)
* - Gbreve (U+011E): X=384.5,Y=-1.5 (should be at baseline 0?)
* - uni0122 (U+0122): X=384.5,Y=-1.5 (should be at baseline 0?)
* - Gdotaccent (U+0120): X=384.5,Y=-1.5 (should be at baseline 0?)
* - ccedilla (U+00E7): X=387.5,Y=2.5 (should be at baseline 0?)
* - g (U+0067): X=384.5,Y=-1.5 (should be at baseline 0?)
* - gbreve (U+011F): X=384.5,Y=-1.5 (should be at baseline 0?)
* - uni0123 (U+0123): X=384.5,Y=-1.5 (should be at baseline 0?)
... and 12 others [code: found-misalignments]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do any segments have colinear vectors? (outline_colinear_vectors)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have colinear vectors:

* trademark (U+2122): from (296.0, 800.0) to (302.0, 800.0) is colinear with segment from (302.0, 800.0) to (392.0, 800.0) [code: found-colinear-vectors]
  
  

</div>
</details>


</div>
</details>


<details><summary>[3] /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-ExpandedExtraBold.ttf</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>








- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* currency (U+00A4): found 4, expected one of: [2, 6]
* uni01F5 (U+01F5): found 2, expected one of: [3, 4, 5] [code: contour-count]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Are there any misaligned on-curve points? (outline_alignment_miss)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have on-curve points which have potentially incorrect y coordinates:

* - Ccedilla (U+00C7): X=387.5,Y=2.5 (should be at baseline 0?)
* - ccedilla (U+00E7): X=387.5,Y=2.5 (should be at baseline 0?)
* - uni1E08 (U+1E08): X=387.5,Y=2.5 (should be at baseline 0?)
* - uni1E09 (U+1E09): X=387.5,Y=2.5 (should be at baseline 0?) [code: found-misalignments]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do outlines contain any semi-vertical or semi-horizontal lines? (outline_semi_vertical)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have semi-vertical/semi-horizontal lines:

* K (U+004B): Line(Line { p0: (276.0, 337.0), p1: (277.0, 46.0) }) (angle: -89.80 degrees, expected: -90.00 degrees)
* uni0136 (U+0136): Line(Line { p0: (276.0, 337.0), p1: (277.0, 46.0) }) (angle: -89.80 degrees, expected: -90.00 degrees)
* k (U+006B): Line(Line { p0: (276.0, 337.0), p1: (277.0, 46.0) }) (angle: -89.80 degrees, expected: -90.00 degrees)
* uni0137 (U+0137): Line(Line { p0: (276.0, 337.0), p1: (277.0, 46.0) }) (angle: -89.80 degrees, expected: -90.00 degrees)
* Kcaron (U+01E8): Line(Line { p0: (276.0, 337.0), p1: (277.0, 46.0) }) (angle: -89.80 degrees, expected: -90.00 degrees)
* kcaron (U+01E9): Line(Line { p0: (276.0, 337.0), p1: (277.0, 46.0) }) (angle: -89.80 degrees, expected: -90.00 degrees)
* uni1E30 (U+1E30): Line(Line { p0: (276.0, 337.0), p1: (277.0, 46.0) }) (angle: -89.80 degrees, expected: -90.00 degrees)
* uni1E31 (U+1E31): Line(Line { p0: (276.0, 337.0), p1: (277.0, 46.0) }) (angle: -89.80 degrees, expected: -90.00 degrees)
* uni1E32 (U+1E32): Line(Line { p0: (276.0, 337.0), p1: (277.0, 46.0) }) (angle: -89.80 degrees, expected: -90.00 degrees)
... and 1 others [code: found-semi-vertical]
  
  

</div>
</details>


</div>
</details>


<details><summary>[3] /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-ExtraBold.ttf</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>








- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* currency (U+00A4): found 4, expected one of: [2, 6]
* uni01F5 (U+01F5): found 2, expected one of: [3, 4, 5] [code: contour-count]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Are there any misaligned on-curve points? (outline_alignment_miss)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have on-curve points which have potentially incorrect y coordinates:

* - Ccedilla (U+00C7): X=387.5,Y=2.5 (should be at baseline 0?)
* - G (U+0047): X=362,Y=2.5 (should be at baseline 0?)
* - Gbreve (U+011E): X=362,Y=2.5 (should be at baseline 0?)
* - uni0122 (U+0122): X=362,Y=2.5 (should be at baseline 0?)
* - Gdotaccent (U+0120): X=362,Y=2.5 (should be at baseline 0?)
* - ccedilla (U+00E7): X=387.5,Y=2.5 (should be at baseline 0?)
* - g (U+0067): X=362,Y=2.5 (should be at baseline 0?)
* - gbreve (U+011F): X=362,Y=2.5 (should be at baseline 0?)
* - uni0123 (U+0123): X=362,Y=2.5 (should be at baseline 0?)
... and 15 others [code: found-misalignments]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do outlines contain any semi-vertical or semi-horizontal lines? (outline_semi_vertical)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have semi-vertical/semi-horizontal lines:

* K (U+004B): Line(Line { p0: (259.0, 331.0), p1: (260.0, 46.0) }) (angle: -89.80 degrees, expected: -90.00 degrees)
* uni0136 (U+0136): Line(Line { p0: (259.0, 331.0), p1: (260.0, 46.0) }) (angle: -89.80 degrees, expected: -90.00 degrees)
* k (U+006B): Line(Line { p0: (259.0, 331.0), p1: (260.0, 46.0) }) (angle: -89.80 degrees, expected: -90.00 degrees)
* uni0137 (U+0137): Line(Line { p0: (259.0, 331.0), p1: (260.0, 46.0) }) (angle: -89.80 degrees, expected: -90.00 degrees)
* Kcaron (U+01E8): Line(Line { p0: (259.0, 331.0), p1: (260.0, 46.0) }) (angle: -89.80 degrees, expected: -90.00 degrees)
* kcaron (U+01E9): Line(Line { p0: (259.0, 331.0), p1: (260.0, 46.0) }) (angle: -89.80 degrees, expected: -90.00 degrees)
* uni1E30 (U+1E30): Line(Line { p0: (259.0, 331.0), p1: (260.0, 46.0) }) (angle: -89.80 degrees, expected: -90.00 degrees)
* uni1E31 (U+1E31): Line(Line { p0: (259.0, 331.0), p1: (260.0, 46.0) }) (angle: -89.80 degrees, expected: -90.00 degrees)
* uni1E32 (U+1E32): Line(Line { p0: (259.0, 331.0), p1: (260.0, 46.0) }) (angle: -89.80 degrees, expected: -90.00 degrees)
... and 1 others [code: found-semi-vertical]
  
  

</div>
</details>


</div>
</details>


<details><summary>[2] /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-Bold.ttf</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>








- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* currency (U+00A4): found 4, expected one of: [2, 6]
* uni01F5 (U+01F5): found 2, expected one of: [3, 4, 5] [code: contour-count]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Are there any misaligned on-curve points? (outline_alignment_miss)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have on-curve points which have potentially incorrect y coordinates:

* - Ccedilla (U+00C7): X=387.5,Y=2.5 (should be at baseline 0?)
* - G (U+0047): X=349,Y=-2.5 (should be at baseline 0?)
* - Gbreve (U+011E): X=349,Y=-2.5 (should be at baseline 0?)
* - uni0122 (U+0122): X=349,Y=-2.5 (should be at baseline 0?)
* - Gdotaccent (U+0120): X=349,Y=-2.5 (should be at baseline 0?)
* - ccedilla (U+00E7): X=387.5,Y=2.5 (should be at baseline 0?)
* - g (U+0067): X=349,Y=-2.5 (should be at baseline 0?)
* - gbreve (U+011F): X=349,Y=-2.5 (should be at baseline 0?)
* - uni0123 (U+0123): X=349,Y=-2.5 (should be at baseline 0?)
... and 11 others [code: found-misalignments]
  
  

</div>
</details>


</div>
</details>


<details><summary>[3] /home/runner/work/blocksync/blocksync/fonts/ttf/Blocksync-Black.ttf</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>








- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* currency (U+00A4): found 4, expected one of: [2, 6]
* uni01F5 (U+01F5): found 2, expected one of: [3, 4, 5] [code: contour-count]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Are there any misaligned on-curve points? (outline_alignment_miss)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have on-curve points which have potentially incorrect y coordinates:

* - Ccedilla (U+00C7): X=387.5,Y=2.5 (should be at baseline 0?)
* - G (U+0047): X=357.5,Y=2 (should be at baseline 0?)
* - Gbreve (U+011E): X=357.5,Y=2 (should be at baseline 0?)
* - uni0122 (U+0122): X=357.5,Y=2 (should be at baseline 0?)
* - Gdotaccent (U+0120): X=357.5,Y=2 (should be at baseline 0?)
* - ccedilla (U+00E7): X=387.5,Y=2.5 (should be at baseline 0?)
* - g (U+0067): X=357.5,Y=2 (should be at baseline 0?)
* - gbreve (U+011F): X=357.5,Y=2 (should be at baseline 0?)
* - uni0123 (U+0123): X=357.5,Y=2 (should be at baseline 0?)
... and 11 others [code: found-misalignments]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do outlines contain any semi-vertical or semi-horizontal lines? (outline_semi_vertical)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have semi-vertical/semi-horizontal lines:

* M (U+004D): Line(Line { p0: (452.0, 406.0), p1: (453.0, 46.0) }) (angle: -89.84 degrees, expected: -90.00 degrees)
* W (U+0057): Line(Line { p0: (389.0, 425.0), p1: (386.0, 46.0) }) (angle: -90.45 degrees, expected: -90.00 degrees)
* Wacute (U+1E82): Line(Line { p0: (389.0, 425.0), p1: (386.0, 46.0) }) (angle: -90.45 degrees, expected: -90.00 degrees)
* Wcircumflex (U+0174): Line(Line { p0: (389.0, 425.0), p1: (386.0, 46.0) }) (angle: -90.45 degrees, expected: -90.00 degrees)
* Wdieresis (U+1E84): Line(Line { p0: (389.0, 425.0), p1: (386.0, 46.0) }) (angle: -90.45 degrees, expected: -90.00 degrees)
* Wgrave (U+1E80): Line(Line { p0: (389.0, 425.0), p1: (386.0, 46.0) }) (angle: -90.45 degrees, expected: -90.00 degrees)
* Y (U+0059): Line(Line { p0: (300.0, 542.0), p1: (301.0, 766.0) }) (angle: 89.74 degrees, expected: 90.00 degrees)
* Yacute (U+00DD): Line(Line { p0: (300.0, 542.0), p1: (301.0, 766.0) }) (angle: 89.74 degrees, expected: 90.00 degrees)
* Ycircumflex (U+0176): Line(Line { p0: (300.0, 542.0), p1: (301.0, 766.0) }) (angle: 89.74 degrees, expected: 90.00 degrees)
... and 34 others [code: found-semi-vertical]
  
  

</div>
</details>


</div>
</details>






### Summary

| ⚠️ WARN | ℹ️ INFO | ✅ PASS | ⏩ SKIP | 
| ---|---|---|---|
| 71 | 126 | 1914 | 1181 | 
| 2% | 4% | 58% | 36% | 



