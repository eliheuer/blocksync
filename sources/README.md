# Sources

Active Google Fonts build inputs:

- `Blocksync.designspace`
- `Blocksync-Regular.ufo`
- `Blocksync-CondensedRegular.ufo`
- `Blocksync-CondensedBold.ufo`
- `Blocksync-CondensedBlack.ufo`
- `Blocksync-ExpandedRegular.ufo`
- `Blocksync-ExpandedBold.ufo`
- `Blocksync-ExpandedBlack.ufo`

Older Glyphs source snapshots live in `archive/` and are not part of the active
Google Fonts build. `Blocksync-Regular.ufo` is the normal-width default source
generated from the corner masters so the variable font defaults to Regular.
Each active UFO has a minimal `features.fea` declaring `DFLT` and `latn` so
generated mark positioning is active for Latin shaping. Some active UFOs still
contain historical non-default layers from older Glyphs exports; the designspace
does not reference those layers, so the Google Fonts build uses only each UFO's
`public.default` layer. Keep the active build path in designspace/UFO form.
