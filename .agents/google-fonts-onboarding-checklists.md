# Google Fonts Onboarding Checklists

Reusable checklist for bringing Blocksync and future font repos to a Google
Fonts handoff baseline.

## Repo Baseline

- Public upstream URL chosen and recorded.
- OFL or another accepted license present.
- `AUTHORS.txt` and `CONTRIBUTORS.txt` present.
- Reserved Font Name status explicit.
- Active sources live in `sources/`.
- Active build path uses designspace/UFO, not `.glyphs`.
- Historical `.glyphs` files live in `sources/archive/`.
- Generated build outputs are ignored.
- Build, QA, proof, and preflight commands are documented.
- Agent entrypoint points to the Google Fonts skills/checklists.

## Decisions To Record

- public upstream URL,
- source packaging strategy,
- version and tag,
- family name, trademarks, namecheck, and RFN status,
- copyright holder and CLA identity,
- AI-use disclosure,
- designer profile identity,
- first-submission script scope,
- custom sample text,
- Article versus legacy description,
- variable axes and `avar` decisions,
- vendor ID,
- kerning scope,
- private-use glyph scope,
- project-template automation.

## Build And Binary QA

- Build variable fonts and expected static instances from `sources/config.yaml`.
- Confirm generated file names and locations.
- Inspect name table, version, license, `OS/2.fsType`, vendor ID, `fvar`,
  `STAT`, and script metadata.
- Run the Google Fonts QA profile.
- Save the report under `out/` or `documentation/`.
- Classify every FAIL and WARN as fix-now, source blocker, decision, accepted
  exception, or tool limitation with evidence.

## Glyphset And Visual QA

- Identify intended first-submission script scope.
- Check Latin Core and any intended non-Latin core glyphsets.
- Track missing codepoints by source glyph work needed.
- Generate proof output after spacing, kerning, glyph, source, or scope changes.
- Review spacing, kerning, diacritics, and script-specific behavior.
- Keep accepted deferrals written down for the Add Font issue and PR handoff.

## Metadata And Packaging

- Generate downstream `METADATA.pb` from built fonts and recorded decisions.
- Check family, designer, category, `date_added`, axes, subsets, source URL,
  source commit, and optional release archive URL.
- Run Packager without PR mode first.
- Confirm changed downstream paths are limited to one family directory.
- Open the Add Font issue before any PR-mode Packager run.
