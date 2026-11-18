# /build-font

Build Blocksync from the active designspace/UFO sources.

## Usage

`/build-font [all|variable|static|proof]`

Default: `all`

## Instructions

1. Read `AGENTS.md`, `sources/README.md`, and `sources/config.yaml`.
2. Confirm `sources/config.yaml` points to `Blocksync.designspace`, not a
   `.glyphs` file.
3. Run `make source-readiness` when validating source state before a release
   handoff.
3. Use the repo-local workflow:

   ```bash
   make build
   ```

   This creates the pinned environment if needed, runs fgtools with fontmake
   through `build.sh`, and applies `scripts/fix_gf_metadata.py`.

4. For release QA, run:

   ```bash
   make test
   ```

5. For print and two-axis proofs, run:

   ```bash
   make proof
   ```

6. Report built files and the Fontspector summary. If the build fails, classify
   the failure as source compatibility, invalid UFO/XML, missing dependency, or
   post-build metadata patching.

## Active Source Policy

- Active sources are `sources/Blocksync.designspace` and the UFO masters it
  references.
- Historical `.glyphs` files must stay in `sources/archive/`.
- Do not add `.glyphs` files back to `sources/config.yaml`.
- Generated `fonts/`, `out/`, `build/`, `dist/`, and `venv/` outputs are local
  artifacts unless a release/archive packaging strategy explicitly includes
  them.
