#!/usr/bin/env python3
"""Generate the portable Google Fonts workflow manifest for future repos."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "documentation" / "google-fonts-agent-porting-manifest.md"

COPY_FIRST = [
    ".agents/",
    "AGENTS.md",
    "GF_READINESS.md",
    "Makefile",
    "requirements.in",
    "build.sh",
    "scripts/check_gf_fonts.sh",
    "scripts/check_downstream_metadata.py",
    "scripts/check_package_context.py",
    "scripts/gf_preflight.py",
]

REUSABLE_HELPERS = [
    "scripts/apply_final_values.py",
    "scripts/build_proof_index.py",
    "scripts/build_release_archive.py",
    "scripts/package_gf_dry_run.sh",
    "scripts/prepare_clean_gf_checkout.sh",
    "scripts/remove_unreachable_support_mark_unicodes.py",
    "scripts/report_agent_porting_manifest.py",
    "scripts/report_agent_reuse_readiness.py",
    "scripts/report_authorship_disclosure_readiness.py",
    "scripts/report_decision_application_blockers.py",
    "scripts/report_downstream_pr_draft.py",
    "scripts/report_downstream_pr_readiness.py",
    "scripts/report_family_name_readiness.py",
    "scripts/report_final_submission_blockers.py",
    "scripts/report_final_values_packet.py",
    "scripts/report_final_values_proposal.py",
    "scripts/report_google_fonts_reference_refresh.py",
    "scripts/report_maintainer_decision_request.py",
    "scripts/report_next_actions.py",
    "scripts/report_open_placeholders.py",
    "scripts/report_package_dry_run_readiness.py",
    "scripts/report_packager_dry_run_record.py",
    "scripts/report_packager_source_strategy.py",
    "scripts/report_proof_review_packet.py",
    "scripts/report_proof_review_readiness.py",
    "scripts/report_release_metadata_readiness.py",
    "scripts/report_source_readiness.py",
    "scripts/report_submission_handoff_readiness.py",
    "scripts/report_zero_warning_worklist.py",
]

TEST_HELPERS = [
    "scripts/test_apply_final_values.py",
    "scripts/test_agent_porting_manifest.py",
    "scripts/test_downstream_pr_draft.py",
    "scripts/test_final_values_packet.py",
    "scripts/test_maintainer_decision_request.py",
    "scripts/test_package_gf_dry_run_gates.sh",
    "scripts/test_packager_dry_run_record.py",
    "scripts/test_release_archive_gates.sh",
]

FAMILY_SPECIFIC_REPLACEMENTS = [
    "Family name, package directory, and downstream metadata `name`.",
    "Public upstream URL, branch, source commit, and optional archive URL.",
    "Designer string, authorship files, CLA identity, RFN status, and AI-use disclosure.",
    "Active source paths, designspace filename, UFO master list, and build config.",
    "Variable axes, default instance, static instance list, and STAT expectations.",
    "First-submission subset/script scope, glyphset coverage targets, and sample text.",
    "Vendor ID, copyright year/project name, DESCRIPTION links, and Add Font issue text.",
    "Fontspector warning disposition, proof review decisions, and generated glyph review scope.",
]

REGENERATE_IN_NEW_REPO = [
    "make preflight-only",
    "make source-readiness",
    "make release-metadata-readiness",
    "make family-name-readiness",
    "make authorship-disclosure-readiness",
    "make packager-source-strategy",
    "make proof-review-readiness",
    "make proof-review-packet",
    "make placeholder-audit",
    "make decision-application-check",
    "make final-values-packet",
    "make final-values-proposal",
    "make maintainer-decision-request",
    "make google-fonts-reference-refresh",
    "make agent-porting-manifest",
    "make agent-reuse-readiness",
    "make release-check",
]


def exists(relpath: str) -> bool:
    path = ROOT / relpath.rstrip("/")
    return path.exists()


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def checklist(paths: list[str]) -> list[str]:
    return [f"- `{path}`: {yes_no(exists(path))}" for path in paths]


def display_path(path: Path) -> Path:
    return path.relative_to(ROOT) if path.is_relative_to(ROOT) else path


def main() -> int:
    all_files = COPY_FIRST + REUSABLE_HELPERS + TEST_HELPERS
    present = [path for path in all_files if exists(path)]
    ready = len(present) == len(all_files)

    lines = [
        "# Google Fonts Agent Porting Manifest",
        "",
        "This generated manifest is the low-token copy plan for moving the",
        "Blocksync Google Fonts workflow into another font repository. It does",
        "not make the next family release-ready by itself; it identifies the",
        "portable files and the family-specific facts that must be replaced.",
        "",
        "## Summary",
        "",
        f"- Porting manifest ready: {yes_no(ready)}",
        f"- Portable files present: {len(present)} / {len(all_files)}",
        "- Active source policy to preserve: designspace/UFO active sources, archived `.glyphs` snapshots.",
        "",
        "## Copy First",
        "",
    ]
    lines.extend(checklist(COPY_FIRST))
    lines.extend(["", "## Reusable Report And Gate Helpers", ""])
    lines.extend(checklist(REUSABLE_HELPERS))
    lines.extend(["", "## Reusable Script Tests", ""])
    lines.extend(checklist(TEST_HELPERS))
    lines.extend(["", "## Replace In The Next Family", ""])
    lines.extend(f"- {item}" for item in FAMILY_SPECIFIC_REPLACEMENTS)
    lines.extend(["", "## Regenerate In The Next Family", "", "```bash"])
    lines.extend(REGENERATE_IN_NEW_REPO)
    lines.extend(
        [
            "```",
            "",
            "## Final Porting Rule",
            "",
            "Do not carry over Blocksync-generated release reports as evidence for",
            "another family. Copy the workflow, replace family facts, regenerate",
            "reports from that repo's current sources, then trust only the new",
            "reports and command output.",
            "",
        ]
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {display_path(OUTPUT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
