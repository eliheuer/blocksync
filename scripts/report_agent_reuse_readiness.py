#!/usr/bin/env python3
"""Generate a reusable-agent Google Fonts readiness report for Blocksync."""

from __future__ import annotations

from pathlib import Path

from report_google_fonts_reference_refresh import EXPECTED_LAST_CHECKED, RECENT_PR_MARKERS
import re


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "documentation" / "google-fonts-agent-reuse-readiness.md"

AGENT_FILES = [
    ".agents/README.md",
    ".agents/google-fonts-onboarding-checklists.md",
    ".agents/google-fonts-official-reference-map.md",
    ".agents/skills/google-fonts-onboarding/SKILL.md",
    ".agents/skills/google-fonts-qa/SKILL.md",
    ".agents/skills/google-fonts-coverage-drawing/SKILL.md",
    ".agents/skills/google-fonts-packaging/SKILL.md",
    ".agents/skills/google-fonts-finalize/SKILL.md",
]

REFERENCE_URLS = [
    "https://googlefonts.github.io/gf-guide/onboarding.html",
    "https://googlefonts.github.io/gf-guide/upstream.html",
    "https://googlefonts.github.io/gf-guide/requirements.html",
    "https://googlefonts.github.io/gf-guide/variable.html",
    "https://googlefonts.github.io/gf-guide/metadata.html",
    "https://googlefonts.github.io/gf-guide/package.html",
    "https://googlefonts.github.io/gf-guide/article.html",
    "https://googlefonts.github.io/gf-guide/making-pr.html",
    "https://github.com/google/fonts/blob/main/.github/ISSUE_TEMPLATE/1_add-font.md",
    *RECENT_PR_MARKERS,
    "https://github.com/googlefonts/googlefonts-project-template",
    "https://github.com/googlefonts/glyphsets",
]

REPORT_DOCS = [
    "documentation/release-metadata-readiness.md",
    "documentation/source-readiness.md",
    "documentation/google-fonts-glyphset-coverage.md",
    "documentation/google-fonts-downstream-metadata-draft.md",
    "documentation/google-fonts-downstream-package-preview.md",
    "documentation/google-fonts-package-checklist.md",
    "documentation/google-fonts-submission-handoff.md",
    "documentation/google-fonts-final-decision-sheet.md",
    "documentation/google-fonts-final-values.proposal.json",
    "documentation/google-fonts-final-values-packet.md",
    "documentation/google-fonts-maintainer-decision-request.md",
    "documentation/google-fonts-name-audit.md",
    "documentation/namecheck-fontdata-result.json",
    "documentation/family-name-readiness.md",
    "documentation/authorship-disclosure-readiness.md",
    "documentation/packager-source-strategy.md",
    "documentation/proof-review-readiness.md",
    "documentation/proof-review-packet.md",
    "documentation/open-placeholder-audit.md",
    "documentation/decision-application-blockers.md",
    "documentation/fontspector-zero-warning-worklist.md",
    "documentation/package-dry-run-readiness.md",
    "documentation/packager-dry-run-record.md",
    "documentation/google-fonts-downstream-pr-draft.md",
    "documentation/downstream-pr-readiness.md",
    "documentation/release-archive-manifest.md",
    "documentation/next-actions.md",
    "documentation/final-submission-blockers.md",
    "documentation/submission-handoff-readiness.md",
    "documentation/google-fonts-reference-refresh.md",
    "documentation/final-readiness-report.md",
    "documentation/google-fonts-agent-porting-manifest.md",
]

HELPER_FILES = [
    "documentation/google-fonts-final-values.template.json",
    "scripts/report_agent_porting_manifest.py",
    "scripts/report_final_values_packet.py",
    "scripts/report_final_values_proposal.py",
    "scripts/report_maintainer_decision_request.py",
    "scripts/apply_final_values.py",
    "scripts/test_apply_final_values.py",
    "scripts/test_agent_porting_manifest.py",
    "scripts/test_maintainer_decision_request.py",
    "scripts/prepare_clean_gf_checkout.sh",
    "scripts/report_packager_dry_run_record.py",
    "scripts/test_packager_dry_run_record.py",
    "scripts/report_downstream_pr_draft.py",
    "scripts/test_downstream_pr_draft.py",
    "scripts/report_final_submission_blockers.py",
    "scripts/report_submission_handoff_readiness.py",
    "scripts/report_proof_review_packet.py",
    "scripts/report_google_fonts_reference_refresh.py",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def main() -> int:
    readme = read(ROOT / "README.md")
    agents = read(ROOT / "AGENTS.md")
    agent_readme = read(ROOT / ".agents" / "README.md")
    checklist = read(ROOT / ".agents" / "google-fonts-onboarding-checklists.md")
    refs = read(ROOT / ".agents" / "google-fonts-official-reference-map.md")
    font_qa = read(ROOT / ".agents" / "skills" / "font-qa" / "SKILL.md")
    google_fonts_qa = read(ROOT / ".agents" / "skills" / "google-fonts-qa" / "SKILL.md")

    present_agent_files = [path for path in AGENT_FILES if (ROOT / path).exists()]
    present_report_docs = [path for path in REPORT_DOCS if (ROOT / path).exists()]
    present_helper_files = [path for path in HELPER_FILES if (ROOT / path).exists()]
    linked_from_readme = [path for path in AGENT_FILES[:3] if path in readme]
    linked_from_agents = [path for path in AGENT_FILES if path in agents]
    linked_from_agent_readme = [path for path in AGENT_FILES[3:] if path.removeprefix(".agents/") in agent_readme]
    present_refs = [url for url in REFERENCE_URLS if url in refs]
    checklist_sections = re.findall(r"^## ", checklist, flags=re.MULTILINE)
    copy_guidance = all(
        phrase in checklist
        for phrase in [
            "future font repos",
            "Active build path uses designspace/UFO",
            "Historical `.glyphs` files live in `sources/archive/`",
        ]
    )
    reference_refresh_guidance = all(
        phrase in refs
        for phrase in [
            EXPECTED_LAST_CHECKED,
            "Recent Merged Downstream PR Examples",
            "Taken from the upstream repo",
            "Fontspector checks are reviewed",
        ]
    )
    fontspector_gate_guidance = all(
        phrase in f"{font_qa}\n{google_fonts_qa}"
        for phrase in [
            "make test",
            "make package-context-check",
            "make warning-worklist",
            "documentation/fontspector-zero-warning-worklist.md",
        ]
    )
    ready = (
        len(present_agent_files) == len(AGENT_FILES)
        and len(present_report_docs) == len(REPORT_DOCS)
        and len(present_helper_files) == len(HELPER_FILES)
        and len(linked_from_readme) == len(AGENT_FILES[:3])
        and len(linked_from_agents) == len(AGENT_FILES)
        and len(linked_from_agent_readme) == len(AGENT_FILES[3:])
        and len(present_refs) == len(REFERENCE_URLS)
        and len(checklist_sections) >= 5
        and copy_guidance
        and fontspector_gate_guidance
        and reference_refresh_guidance
    )

    lines = [
        "# Google Fonts Agent Reuse Readiness",
        "",
        "This generated report checks whether Blocksync's agent-facing Google",
        "Fonts workflow is discoverable, repeatable, and ready to copy into the",
        "next font repository with family-specific edits.",
        "",
        "## Summary",
        "",
        f"- Reusable agent bundle ready: {yes_no(ready)}",
        f"- Required agent files present: {len(present_agent_files)} / {len(AGENT_FILES)}",
        f"- Generated release reports present: {len(present_report_docs)} / {len(REPORT_DOCS)}",
        f"- Reusable helper files present: {len(present_helper_files)} / {len(HELPER_FILES)}",
        f"- Core agent files linked from README: {len(linked_from_readme)} / {len(AGENT_FILES[:3])}",
        f"- Agent files linked from AGENTS.md: {len(linked_from_agents)} / {len(AGENT_FILES)}",
        f"- Google Fonts skills linked from .agents/README.md: {len(linked_from_agent_readme)} / {len(AGENT_FILES[3:])}",
        f"- Official reference URLs mapped: {len(present_refs)} / {len(REFERENCE_URLS)}",
        f"- Checklist sections present: {len(checklist_sections)}",
        f"- Copy guidance present: {yes_no(copy_guidance)}",
        f"- Fontspector gate guidance present: {yes_no(fontspector_gate_guidance)}",
        f"- Live reference refresh guidance present: {yes_no(reference_refresh_guidance)}",
        "",
        "## Required Agent Files",
        "",
    ]
    lines.extend(f"- `{path}`: {yes_no(path in present_agent_files)}" for path in AGENT_FILES)
    lines.extend(["", "## Generated Release Reports", ""])
    lines.extend(f"- `{path}`: {yes_no(path in present_report_docs)}" for path in REPORT_DOCS)
    lines.extend(["", "## Reusable Helper Files", ""])
    lines.extend(f"- `{path}`: {yes_no(path in present_helper_files)}" for path in HELPER_FILES)
    lines.extend(["", "## Official References", ""])
    lines.extend(f"- {url}: {yes_no(url in present_refs)}" for url in REFERENCE_URLS)
    lines.extend(
        [
            "",
            "## Copy Guidance",
            "",
            "- Copy `.agents/`, `AGENTS.md`, `GF_READINESS.md`, and the release",
            "  report scripts before starting the next family.",
            "- Replace family name, upstream URL, source paths, downstream package",
            "  directory, axis data, designer identity, and first-submission scope.",
            "- Keep the active build path on designspace/UFO and archive historical",
            "  `.glyphs` sources unless the next family has a different confirmed",
            "  source strategy.",
            "- Refresh official Google Fonts docs and templates before final issue",
            "  or PR work.",
            "",
        ]
    )

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
