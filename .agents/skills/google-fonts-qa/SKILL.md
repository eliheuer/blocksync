# /google-fonts-qa

Run and document Google Fonts QA for a font family.

## Usage

`/google-fonts-qa [fontspector|glyphsets|proof|kerning|metadata|all]`

Default: `all`

## Checks

1. Build from the active source config:

   ```bash
   make build
   ```

2. Run the Fontspector Google Fonts QA profile on the release font package:

   ```bash
   make test
   ```

   Use `CHECK_STATIC=1 ./scripts/check_gf_fonts.sh` only when static TTF
   proofing outputs need to be checked too.

3. Run the downstream-like package-context Fontspector check:

   ```bash
   make package-context-check
   ```

   This catches metadata/package interactions that may not appear when checking
   only `fonts/variable/Blocksync[wdth,wght].ttf`.

4. Regenerate the current warning floor:

   ```bash
   make warning-worklist
   ```

   Use `documentation/fontspector-zero-warning-worklist.md` to decide whether
   each remaining WARN is a source fix, maintainer decision, or reviewer
   acceptance item.

5. Run the lightweight source/release structure check:

   ```bash
   make preflight-only
   ```

6. Run the source-readiness gate when validating release sources:

   ```bash
   make source-readiness
   ```

7. Run the consolidated handoff gate before returning release status:

   ```bash
   make release-check
   ```

8. Generate proof output when spacing, kerning, glyphs, source metadata, or
   build outputs change:

   ```bash
   make proof
   ```

9. Classify every QA FAIL/WARN as one of:
   - fix now,
   - drawing/source blocker,
   - maintainer decision,
   - reviewer-approved exception,
   - false positive or tool limitation with evidence.

## Visual QA

- Review proof output for every expected instance.
- Review spacing, kerning, diacritics, outlines, and interpolation behavior.
- Rerun proofs after source, spacing, kerning, or scope changes.
- Do not mark kerning final until both source data and proof review agree.
