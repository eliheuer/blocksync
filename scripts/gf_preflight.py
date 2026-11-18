#!/usr/bin/env python3
"""Lightweight Google Fonts release-structure preflight for Blocksync.

This intentionally uses only the Python standard library so it can run before
the font build venv is installed.
"""

from __future__ import annotations

from pathlib import Path
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources"
CONFIG = SOURCES / "config.yaml"
DESIGNSPACE = SOURCES / "Blocksync.designspace"

REQUIRED_FILES = [
    "AGENTS.md",
    ".agents/README.md",
    ".agents/google-fonts-onboarding-checklists.md",
    ".agents/google-fonts-official-reference-map.md",
    ".agents/skills/build-font/SKILL.md",
    ".agents/skills/compare-reference/SKILL.md",
    ".agents/skills/draw-outline/SKILL.md",
    ".agents/skills/edit-glyph/SKILL.md",
    ".agents/skills/font-qa/SKILL.md",
    ".agents/skills/google-fonts-onboarding/SKILL.md",
    ".agents/skills/google-fonts-qa/SKILL.md",
    ".agents/skills/google-fonts-coverage-drawing/SKILL.md",
    ".agents/skills/google-fonts-packaging/SKILL.md",
    ".agents/skills/google-fonts-finalize/SKILL.md",
    ".agents/skills/kerning/SKILL.md",
    ".agents/skills/proof/SKILL.md",
    ".agents/skills/render-specimen/SKILL.md",
    "GF_READINESS.md",
    "OFL.txt",
    "AUTHORS.txt",
    "CONTRIBUTORS.txt",
    "build.sh",
    "scripts/fix_gf_metadata.py",
    "scripts/build_proof_index.py",
    "scripts/check_downstream_metadata.py",
    "scripts/check_gf_fonts.sh",
    "scripts/check_package_context.py",
    "scripts/check_final_readiness.py",
    "scripts/apply_final_values.py",
    "scripts/package_gf_dry_run.sh",
    "scripts/prepare_clean_gf_checkout.sh",
    "scripts/report_packager_dry_run_record.py",
    "scripts/report_package_dry_run_readiness.py",
    "scripts/report_downstream_pr_draft.py",
    "scripts/report_downstream_pr_readiness.py",
    "scripts/report_agent_reuse_readiness.py",
    "scripts/report_agent_porting_manifest.py",
    "scripts/report_release_metadata_readiness.py",
    "scripts/report_source_readiness.py",
    "scripts/report_family_name_readiness.py",
    "scripts/report_authorship_disclosure_readiness.py",
    "scripts/report_packager_source_strategy.py",
    "scripts/report_proof_review_readiness.py",
    "scripts/report_proof_review_packet.py",
    "scripts/report_open_placeholders.py",
    "scripts/report_decision_application_blockers.py",
    "scripts/report_final_values_packet.py",
    "scripts/report_final_values_proposal.py",
    "scripts/report_maintainer_decision_request.py",
    "scripts/report_final_submission_blockers.py",
    "scripts/report_submission_handoff_readiness.py",
    "scripts/report_google_fonts_reference_refresh.py",
    "scripts/remove_unreachable_support_mark_unicodes.py",
    "scripts/report_next_actions.py",
    "scripts/report_zero_warning_worklist.py",
    "scripts/test_release_archive_gates.sh",
    "scripts/test_package_gf_dry_run_gates.sh",
    "scripts/test_apply_final_values.py",
    "scripts/test_agent_porting_manifest.py",
    "scripts/test_final_values_packet.py",
    "scripts/test_maintainer_decision_request.py",
    "scripts/test_packager_dry_run_record.py",
    "scripts/test_downstream_pr_draft.py",
    "sources/README.md",
    "sources/archive/README.md",
    "documentation/DESCRIPTION.en_us.html",
    "documentation/google-fonts-add-font-issue-draft.md",
    "documentation/google-fonts-downstream-metadata-draft.md",
    "documentation/google-fonts-downstream-package-preview.md",
    "documentation/google-fonts-final-decision-sheet.md",
    "documentation/google-fonts-final-values.template.json",
    "documentation/google-fonts-final-values.proposal.json",
    "documentation/google-fonts-final-values-packet.md",
    "documentation/google-fonts-maintainer-decision-request.md",
    "documentation/google-fonts-glyphset-coverage.md",
    "documentation/google-fonts-name-audit.md",
    "documentation/namecheck-fontdata-result.json",
    "documentation/family-name-readiness.md",
    "documentation/authorship-disclosure-readiness.md",
    "documentation/packager-source-strategy.md",
    "documentation/proof-review-readiness.md",
    "documentation/proof-review-packet.md",
    "documentation/open-placeholder-audit.md",
    "documentation/decision-application-blockers.md",
    "documentation/google-fonts-package-checklist.md",
    "documentation/google-fonts-submission-handoff.md",
    "documentation/google-fonts-source-strategy.md",
    "documentation/release-metadata-readiness.md",
    "documentation/source-readiness.md",
    "documentation/fontspector-zero-warning-worklist.md",
    "documentation/final-submission-blockers.md",
    "documentation/submission-handoff-readiness.md",
    "documentation/google-fonts-reference-refresh.md",
    "documentation/final-readiness-report.md",
    "documentation/package-dry-run-readiness.md",
    "documentation/packager-dry-run-record.md",
    "documentation/google-fonts-downstream-pr-draft.md",
    "documentation/downstream-pr-readiness.md",
    "documentation/google-fonts-agent-reuse-readiness.md",
    "documentation/google-fonts-agent-porting-manifest.md",
    "documentation/release-archive-manifest.md",
    "documentation/next-actions.md",
    "sources/config.yaml",
    "sources/Blocksync.designspace",
    "sources/Blocksync-Regular.ufo",
    "scripts/build_release_archive.py",
]


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)
    print(f"FAIL: {message}")


def ok(message: str) -> None:
    print(f"OK: {message}")


def main() -> int:
    failures: list[str] = []

    for relpath in REQUIRED_FILES:
        path = ROOT / relpath
        if path.exists():
            ok(f"{relpath} exists")
        else:
            fail(f"{relpath} is missing", failures)

    config_text = CONFIG.read_text(encoding="utf-8") if CONFIG.exists() else ""
    if "Blocksync.designspace" in config_text and ".glyphs" not in config_text:
        ok("sources/config.yaml points to Blocksync.designspace and not .glyphs")
    else:
        fail("sources/config.yaml must use Blocksync.designspace and exclude .glyphs", failures)

    top_level_glyphs = sorted(path.name for path in SOURCES.glob("*.glyphs"))
    if top_level_glyphs:
        fail(f"top-level .glyphs files must be archived: {', '.join(top_level_glyphs)}", failures)
    else:
        ok("no top-level .glyphs files remain in sources/")

    archived_glyphs = sorted(path.name for path in (SOURCES / "archive").glob("*.glyphs"))
    if "Blocksync.glyphs" in archived_glyphs:
        ok("sources/archive/Blocksync.glyphs is archived")
    else:
        fail("sources/archive/Blocksync.glyphs is missing", failures)

    if DESIGNSPACE.exists():
        try:
            root = ET.parse(DESIGNSPACE).getroot()
            source_entries = [
                source.attrib
                for source in root.findall(".//source")
                if "filename" in source.attrib
            ]
            source_files = [source["filename"] for source in source_entries]
        except ET.ParseError as error:
            fail(f"Blocksync.designspace is not parseable XML: {error}", failures)
            source_files = []
            source_entries = []
        missing_ufos = [filename for filename in source_files if not (SOURCES / filename).exists()]
        if missing_ufos:
            fail(f"designspace references missing UFOs: {', '.join(missing_ufos)}", failures)
        elif source_files:
            ok(f"designspace references {len(source_files)} existing UFO masters")
        layer_overrides = [
            source["filename"]
            for source in source_entries
            if source.get("layer") or source.get("layername")
        ]
        if layer_overrides:
            fail(
                f"designspace source entries must use default UFO layers only: {', '.join(layer_overrides)}",
                failures,
            )
        elif source_entries:
            ok("designspace source entries use default UFO layers only")

    source_readiness = ROOT / "documentation/source-readiness.md"
    source_readiness_text = source_readiness.read_text(encoding="utf-8") if source_readiness.exists() else ""
    if "- Designspace source layer overrides: 0" in source_readiness_text:
        ok("source-readiness report records zero designspace layer overrides")
    else:
        fail("source-readiness report must record zero designspace layer overrides", failures)
    if "- Active build uses default UFO layers only: yes" in source_readiness_text:
        ok("source-readiness report confirms default UFO layers only")
    else:
        fail("source-readiness report must confirm default UFO layers only", failures)

    if failures:
        print("")
        print(f"{len(failures)} preflight issue(s) need attention.")
        return 1

    print("")
    print("Blocksync Google Fonts release-structure preflight passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
