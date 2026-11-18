## FontSpector report

fontspector version: 1.9.0






## Check results




<details><summary>[2] fonts/variable/Blocksync[wdth,wght].ttf</summary>
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
* - uni0218 (U+0218): X=180,Y=2.5 (should be at baseline 0?)
* - ccedilla (U+00E7): X=387.5,Y=2.5 (should be at baseline 0?)
* - g (U+0067): X=349,Y=-2.5 (should be at baseline 0?)
* - gbreve (U+011F): X=349,Y=-2.5 (should be at baseline 0?)
* - uni0123 (U+0123): X=349,Y=-2.5 (should be at baseline 0?)
* - gdotaccent (U+0121): X=349,Y=-2.5 (should be at baseline 0?)
* - s (U+0073): X=180,Y=2.5 (should be at baseline 0?)
* - sacute (U+015B): X=180,Y=2.5 (should be at baseline 0?)
* - scaron (U+0161): X=180,Y=2.5 (should be at baseline 0?)
* - uni0219 (U+0219): X=180,Y=2.5 (should be at baseline 0?)
* - section (U+00A7): X=801.5,Y=-1 (should be at baseline 0?)
* - section (U+00A7): X=625.5,Y=-2 (should be at baseline 0?)
* - Gcaron (U+01E6): X=349,Y=-2.5 (should be at baseline 0?)
* - Gstroke (U+01E4): X=349,Y=-2.5 (should be at baseline 0?)
* - gcaron (U+01E7): X=349,Y=-2.5 (should be at baseline 0?)
* - gstroke (U+01E5): X=349,Y=-2.5 (should be at baseline 0?)
* - scircumflex (U+015D): X=180,Y=2.5 (should be at baseline 0?)
* - uni01F4 (U+01F4): X=349,Y=-2.5 (should be at baseline 0?)
* - uni01F5 (U+01F5): X=349,Y=-2.5 (should be at baseline 0?)
* - uni1E08 (U+1E08): X=387.5,Y=2.5 (should be at baseline 0?)
* - uni1E09 (U+1E09): X=387.5,Y=2.5 (should be at baseline 0?)
* - uni1E20 (U+1E20): X=349,Y=-2.5 (should be at baseline 0?)
* - uni1E21 (U+1E21): X=349,Y=-2.5 (should be at baseline 0?)
* - uni1E60 (U+1E60): X=180,Y=2.5 (should be at baseline 0?)
* - uni1E61 (U+1E61): X=180,Y=2.5 (should be at baseline 0?)
* - uni1E64 (U+1E64): X=180,Y=2.5 (should be at baseline 0?)
* - uni1E65 (U+1E65): X=180,Y=2.5 (should be at baseline 0?)
* - uni1E66 (U+1E66): X=180,Y=2.5 (should be at baseline 0?)
* - uni1E67 (U+1E67): X=180,Y=2.5 (should be at baseline 0?) [code: found-misalignments]
  
  

</div>
</details>


</div>
</details>


<details><summary>[1] fonts/variable</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> Check for codepoints not covered by METADATA subsets. (googlefonts/metadata/unreachable_subsetting)</summary>
    <div>








- ⚠️ **WARN** fonts/variable/Blocksync[wdth,wght].ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+02D8 BREVE: try adding one of: yi, canadian-aboriginal
* U+02D9 DOT ABOVE: try adding one of: yi, canadian-aboriginal
* U+02DB OGONEK: try adding one of: canadian-aboriginal, yi
* U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: cherokee, tifinagh, coptic, math
* U+0306 COMBINING BREVE: try adding one of: old-permic, tifinagh
* U+0307 COMBINING DOT ABOVE: try adding one of: canadian-aboriginal, coptic, tai-le, todhri, malayalam, tifinagh, duployan, math, syriac, old-permic, hebrew
* U+030A COMBINING RING ABOVE: try adding one of: syriac, duployan
* U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: osage, cherokee
* U+030C COMBINING CARON: try adding one of: cherokee, tai-le
* U+0312 COMBINING TURNED COMMA ABOVE: try adding math
* U+0315 COMBINING COMMA ABOVE RIGHT: try adding math
* U+0326 COMBINING COMMA BELOW: try adding math
* U+0327 COMBINING CEDILLA: try adding math
* U+0331 COMBINING MACRON BELOW: try adding one of: tifinagh, caucasian-albanian, syriac, thai, cherokee, gothic, sunuwar
* U+25CC DOTTED CIRCLE: try adding one of: mahajani, khmer, tamil, thai, hanifi-rohingya, masaram-gondi, wancho, tirhuta, buginese, mongolian, sinhala, symbols, kayah-li, syloti-nagri, kaithi, modi, tifinagh, malayalam, gurmukhi, sundanese, armenian, kharoshthi, balinese, brahmi, sogdian, tagbanwa, gunjala-gondi, mende-kikakui, dogra, siddham, tai-tham, duployan, math, bengali, music, kannada, meetei-mayek, coptic, grantha, hanunoo, mandaic, oriya, osage, sharada, soyombo, tai-le, devanagari, elbasan, nko, phags-pa, telugu, thaana, javanese, takri, cham, canadian-aboriginal, yi, tibetan, adlam, lao, miao, hebrew, ahom, lepcha, batak, caucasian-albanian, gujarati, myanmar, new-tai-lue, old-permic, pahawh-hmong, limbu, syriac, tai-viet, khojki, psalter-pahlavi, rejang, bhaiksuki, chakma, tagalog, saurashtra, buhid, bassa-vah, marchen, warang-citi, zanabazar-square, khudawadi, newa, manichaean

Or you can add the above codepoints to one of the subsets supported by the font: latin-ext, latin, vietnamese [code: unreachable-subsetting]
  
  

</div>
</details>


</div>
</details>






### Summary

| ⚠️ WARN | ℹ️ INFO | ✅ PASS | ⏩ SKIP | 
| ---|---|---|---|
| 3 | 8 | 131 | 60 | 
| 1% | 4% | 65% | 30% | 



