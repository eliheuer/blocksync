# /google-fonts-onboarding

Prepare a font repository for Google Fonts onboarding from first audit through
handoff. This skill is portable: replace family-specific names, paths, scripts,
and source strategy values before copying it to another family.

## Usage

`/google-fonts-onboarding [audit|decisions|handoff|all]`

Default: `all`

## Flow

1. Read `AGENTS.md`, `GF_READINESS.md`, `sources/README.md`, and
   `sources/config.yaml`.
2. Confirm active sources are designspace/UFO and historical `.glyphs` files
   are archived.
3. Confirm license, authorship, RFN, public upstream URL, and CLA identity.
4. Build fonts from `sources/config.yaml`.
5. Run Google Fonts QA and save reports.
6. Audit glyphset coverage for the intended first-submission scope.
7. Audit variable-font metadata: axes, `fvar`, `STAT`, `avar`, name table,
   version, license, embedding, and vendor ID.
8. Generate visual proof output and record review status.
9. Record open maintainer decisions in `GF_READINESS.md`.
10. Prepare downstream metadata/package evidence only after source and QA
    blockers are either fixed or explicitly accepted for review.

## Principles

- Treat current Google Fonts docs and the `google/fonts` repo as source of
  truth before final issue or PR work.
- Keep one canonical decision log.
- Separate drawing/source blockers from onboarding mechanics.
- Prefer generated, repeatable reports for state that can drift.
- Do not open or update a downstream PR until a no-PR Packager run has been
  reviewed and the Google Fonts Add Font issue exists.
