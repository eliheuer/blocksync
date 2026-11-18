#!/usr/bin/env python3
"""Generate a Google Fonts live-reference refresh report.

This report is intentionally offline. Agents should refresh the source map
from live Google Fonts docs/PRs before final issue or PR work, then this script
checks that the repo-local map captures the current template and PR patterns.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / ".agents" / "google-fonts-official-reference-map.md"
OUTPUT = ROOT / "documentation" / "google-fonts-reference-refresh.md"

EXPECTED_LAST_CHECKED = "Last checked: 2026-06-13."

TEMPLATE_MARKERS = [
    "labels: `I New Font, II Submission`",
    "AI tools were used",
    "no Reserved Font Names",
    "namecheck.fontdata.com",
    "GF_Latin_Core.txt",
    "preferred upstream repo structure",
    "maintain the repository",
]

RECENT_PR_MARKERS = [
    "https://github.com/google/fonts/pull/10596",
    "https://github.com/google/fonts/pull/10591",
    "https://github.com/google/fonts/pull/10613",
]

DOWNSTREAM_MARKERS = [
    "Taken from the upstream repo",
    "PR Checklist",
    "Fontspector checks are reviewed",
    "The PR is linked to the corresponding issue",
    "`tags` are added for NEW FONTS",
    "Designers bio info",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def missing(markers: list[str], text: str) -> list[str]:
    return [marker for marker in markers if marker not in text]


def main() -> int:
    text = read(MAP)
    missing_template = missing(TEMPLATE_MARKERS, text)
    missing_prs = missing(RECENT_PR_MARKERS, text)
    missing_downstream = missing(DOWNSTREAM_MARKERS, text)
    last_checked_current = EXPECTED_LAST_CHECKED in text

    ready = (
        last_checked_current
        and not missing_template
        and not missing_prs
        and not missing_downstream
    )

    lines = [
        "# Google Fonts Reference Refresh",
        "",
        "This generated report checks that Blocksync's repo-local Google Fonts",
        "reference map records the current Add Font issue template and recent",
        "merged downstream PR conventions used for this release setup pass.",
        "",
        "## Summary",
        "",
        f"- Reference refresh ready: {yes_no(ready)}",
        f"- Expected live-check date recorded: {yes_no(last_checked_current)}",
        f"- Add Font template markers present: {len(TEMPLATE_MARKERS) - len(missing_template)} / {len(TEMPLATE_MARKERS)}",
        f"- Recent merged PR references present: {len(RECENT_PR_MARKERS) - len(missing_prs)} / {len(RECENT_PR_MARKERS)}",
        f"- Downstream PR convention markers present: {len(DOWNSTREAM_MARKERS) - len(missing_downstream)} / {len(DOWNSTREAM_MARKERS)}",
        f"- First blocker: {(missing_template + missing_prs + missing_downstream)[0] if not ready and (missing_template + missing_prs + missing_downstream) else ('missing current live-check date' if not last_checked_current else 'none')}",
        "",
        "## Checked References",
        "",
        "- Current Add Font issue template:",
        "  https://github.com/google/fonts/blob/main/.github/ISSUE_TEMPLATE/1_add-font.md",
        "- Current Google Fonts contributing entrypoint:",
        "  https://github.com/google/fonts/blob/main/CONTRIBUTING.md",
        "- Recent merged new-font/package PR examples:",
    ]
    lines.extend(f"  - {url}" for url in RECENT_PR_MARKERS)
    lines.extend(["", "## Missing Template Markers", ""])
    lines.extend(f"- `{marker}`" for marker in missing_template) if missing_template else lines.append("- none")
    lines.extend(["", "## Missing Recent PR References", ""])
    lines.extend(f"- {marker}" for marker in missing_prs) if missing_prs else lines.append("- none")
    lines.extend(["", "## Missing Downstream PR Convention Markers", ""])
    lines.extend(f"- `{marker}`" for marker in missing_downstream) if missing_downstream else lines.append("- none")
    lines.extend(
        [
            "",
            "## Handoff Notes",
            "",
            "- Refresh the live links again before opening the Google Fonts issue",
            "  or downstream PR; this report records the 2026-06-13 check only.",
            "- Keep the issue draft aligned with the current Add Font checklist:",
            "  source availability, OFL/RFN/authorship/AI disclosure, unique",
            "  family name, Latin Core support, preferred upstream structure,",
            "  contribution requirements, and maintenance commitment.",
            "- Keep the downstream PR body aligned with recent merged PRs: upstream",
            "  repo and commit provenance, linked Add Font issue, Fontspector",
            "  review, OFL URL review, subset/primary-script review, designer",
            "  profile status, and tags for new fonts.",
            "",
        ]
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
