#!/usr/bin/env python3
"""Generate the concise maintainer decision request for final GF values."""

from __future__ import annotations

import json
from pathlib import Path
import re

from check_final_readiness import blocker_lines


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "documentation" / "google-fonts-maintainer-decision-request.md"
PROPOSAL = ROOT / "documentation" / "google-fonts-final-values.proposal.json"
PACKET = ROOT / "documentation" / "google-fonts-final-values-packet.md"
FINAL_READINESS = ROOT / "documentation" / "final-readiness-report.md"
PLACEHOLDERS = ROOT / "documentation" / "open-placeholder-audit.md"
WARNINGS = ROOT / "documentation" / "fontspector-zero-warning-worklist.md"

REQUIRED_KEYS = [
    "date_added",
    "source_commit",
    "repository_url",
    "branch",
    "designer",
    "package_source_strategy",
    "namecheck_result",
    "ai_use_disclosure",
    "authorship_cla_rfn_status",
    "fontspector_warning_decision",
    "visual_proof_decision",
    "generated_composites_decision",
    "static_ttf_decision",
    "release_archive_fallback_decision",
]
OPTIONAL_KEYS = ["archive_url", "google_fonts_issue_url"]

KEY_PROMPTS = {
    "date_added": "Final Google Fonts package date, YYYY-MM-DD.",
    "source_commit": "Final reviewed public upstream commit hash.",
    "repository_url": "Final public GitHub upstream URL.",
    "branch": "Final public source branch.",
    "designer": "Final metadata designer string.",
    "package_source_strategy": "Use config_yaml unless archive packaging is chosen.",
    "namecheck_result": "Final namecheck.fontdata.com clearance statement.",
    "ai_use_disclosure": "Maintainer-approved AI-use disclosure wording.",
    "authorship_cla_rfn_status": "Final authorship, CLA identity, and RFN status.",
    "fontspector_warning_decision": "Accept current WARN floor or require source cleanup.",
    "visual_proof_decision": "Final proof review disposition.",
    "generated_composites_decision": "Accept, revise, or defer generated composites.",
    "static_ttf_decision": "Confirm statics are proof-only unless requested.",
    "release_archive_fallback_decision": "Confirm archive fallback policy.",
    "archive_url": "Required only when package_source_strategy is archive.",
    "google_fonts_issue_url": "Fill after the Add Font issue exists.",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def load_proposal() -> dict[str, str]:
    if not PROPOSAL.exists():
        return {}
    data = json.loads(PROPOSAL.read_text(encoding="utf-8"))
    return {
        key: value.strip() if isinstance(value, str) else ""
        for key, value in data.items()
    }


def final_blockers(text: str) -> list[str]:
    match = re.search(
        r"^## Blocking Items\n(?P<body>.*?)(?=^## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if not match:
        return []
    return [
        line[2:].strip()
        for line in match.group("body").splitlines()
        if line.startswith("- ") and line != "- none"
    ]


def summary_value(label: str, text: str, default: str = "unknown") -> str:
    match = re.search(rf"^- {re.escape(label)}: (.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else default


def needs_answer(value: str, *, optional: bool = False) -> str:
    if value:
        return "review"
    return "conditional" if optional else "yes"


def escape_table(value: str) -> str:
    if not value:
        return ""
    return value.replace("|", "\\|").replace("\n", " ")


def key_rows(values: dict[str, str], keys: list[str], *, optional: bool = False) -> list[str]:
    rows: list[str] = []
    for key in keys:
        value = values.get(key, "")
        rows.append(
            f"| `{key}` | {escape_table(value)} | {needs_answer(value, optional=optional)} | {KEY_PROMPTS[key]} |"
        )
    return rows


def values_without_proposal_keys(values: dict[str, str]) -> str:
    clean = {key: values.get(key, "") for key in REQUIRED_KEYS + OPTIONAL_KEYS}
    return json.dumps(clean, indent=2, ensure_ascii=True)


def display_path(path: Path) -> Path:
    return path.relative_to(ROOT) if path.is_relative_to(ROOT) else path


def main() -> int:
    values = load_proposal()
    try:
        blockers = blocker_lines()
    except Exception:
        blockers = final_blockers(read(FINAL_READINESS))
    placeholders = read(PLACEHOLDERS)
    warnings = read(WARNINGS)
    packet = read(PACKET)
    packet_ready = "Final values packet ready: yes" in packet

    lines = [
        "# Google Fonts Maintainer Decision Request",
        "",
        "This generated request is the shortest handoff surface for the final",
        "human decisions that automation cannot invent. Fill the blank values,",
        "review the proposed values, then validate a private JSON copy before",
        "applying anything to release drafts.",
        "",
        "## Summary",
        "",
        f"- Maintainer decision request ready: {'yes' if values and packet_ready else 'no'}",
        f"- Final values packet ready: {'yes' if packet_ready else 'no'}",
        f"- Current final-readiness blockers: {len(blockers)}",
        f"- Public placeholder blocker count: {summary_value('Public placeholder blocker count', placeholders)}",
        f"- Remaining Fontspector warning floor: {summary_value('Package-context warning checks', warnings)}",
        "",
        "## Required Answers",
        "",
        "| JSON key | Proposed value from local evidence | Needs maintainer answer | Prompt |",
        "| --- | --- | --- | --- |",
    ]
    lines.extend(key_rows(values, REQUIRED_KEYS))
    lines.extend(
        [
            "",
            "## Optional Answers",
            "",
            "| JSON key | Proposed value from local evidence | Needs maintainer answer | Prompt |",
            "| --- | --- | --- | --- |",
        ]
    )
    lines.extend(key_rows(values, OPTIONAL_KEYS, optional=True))

    lines.extend(
        [
            "",
            "## Copyable JSON Starting Point",
            "",
            "This block intentionally omits proposal-only `_...` keys. Save it as a",
            "private values file, replace blanks and any non-final wording, then run",
            "the validation command below.",
            "",
            "```json",
            values_without_proposal_keys(values),
            "```",
            "",
            "## Validation Commands",
            "",
            "```bash",
            "make final-values-check VALUES=/path/to/final-values.json",
            "make apply-final-values VALUES=/path/to/final-values.json",
            "make release-check",
            "make final-readiness-check",
            "```",
            "",
            "## Current Final Blockers",
            "",
        ]
    )
    if blockers:
        lines.extend(f"- {blocker}" for blocker in blockers)
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "Regenerate this request with `make maintainer-decision-request` after",
            "running `make release-check`, proof review, or final-value changes.",
            "",
        ]
    )

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {display_path(OUTPUT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
