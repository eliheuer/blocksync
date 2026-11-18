#!/usr/bin/env python3
"""Generate the maintainer final-values answer packet."""

from __future__ import annotations

import json
from pathlib import Path
import re

import apply_final_values


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "documentation" / "google-fonts-final-values-packet.md"
TEMPLATE = ROOT / "documentation" / "google-fonts-final-values.template.json"
DECISIONS = ROOT / "documentation" / "google-fonts-final-decision-sheet.md"
NEXT_ACTIONS = ROOT / "documentation" / "next-actions.md"

OPTIONAL_KEYS = {"archive_url", "google_fonts_issue_url"}
KEY_NOTES = {
    "date_added": "Use the final Google Fonts package date in YYYY-MM-DD form.",
    "source_commit": "Use the reviewed final public upstream commit hash.",
    "repository_url": "Use the final public GitHub upstream URL.",
    "branch": "Use a simple git branch name, usually main.",
    "designer": "Use the final metadata designer string.",
    "package_source_strategy": "Use config_yaml unless release/archive packaging is selected.",
    "archive_url": "Required only when package_source_strategy is archive.",
    "namecheck_result": "Record final namecheck.fontdata.com clearance.",
    "ai_use_disclosure": "Record maintainer-approved AI-use wording.",
    "authorship_cla_rfn_status": "Record final authorship, CLA identity, and no-RFN status.",
    "fontspector_warning_decision": "Accept remaining warnings or describe scheduled cleanup.",
    "visual_proof_decision": "Record proof review status.",
    "generated_composites_decision": "Accept, revise, or defer generated composites.",
    "static_ttf_decision": "Confirm whether statics are proof-only.",
    "release_archive_fallback_decision": "Confirm fallback policy.",
    "google_fonts_issue_url": "Fill after the Add Font issue exists.",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def decision_rows(text: str) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for line in text.splitlines():
        if not line.startswith("| ") or line.startswith("| ---"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) >= 3 and cells[0] not in {"Decision", "Review item"}:
            rows.append((cells[0], cells[1], cells[2]))
    return rows


def final_blockers(text: str) -> list[str]:
    match = re.search(
        r"^## Maintainer Decisions\n(?P<body>.*?)(?=^## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if not match:
        return []
    return [
        line.split("|", 2)[1].strip()
        for line in match.group("body").splitlines()
        if line.startswith("| ") and not line.startswith("| ---") and "Blocker" not in line
    ]


def template_values() -> dict[str, str]:
    data = json.loads(read(TEMPLATE))
    if not isinstance(data, dict):
        raise ValueError("final values template must be a JSON object")
    return {
        key: value if isinstance(value, str) else ""
        for key, value in data.items()
    }


def decision_key(label: str) -> str:
    if label == "Package source strategy":
        return "package_source_strategy"
    return apply_final_values.DECISION_LABELS.get(label, "")


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def markdown() -> str:
    decisions = decision_rows(read(DECISIONS))
    template = template_values()
    required = set(apply_final_values.REQUIRED_KEYS)
    expected = required | OPTIONAL_KEYS
    template_keys = set(template)
    missing_required = sorted(required - template_keys)
    extra = sorted(template_keys - expected)
    mapped_row_count = sum(1 for label, _current, _answer in decisions if decision_key(label))
    mapped_labels = {label for label, _current, _answer in decisions if decision_key(label)}
    unmapped_labels = [label for label, _current, _answer in decisions if not decision_key(label)]
    missing_decision_labels = sorted(set(apply_final_values.DECISION_LABELS) - mapped_labels)
    package_strategy_mapped = any(label == "Package source strategy" for label, _current, _answer in decisions)
    ready = (
        not missing_required
        and not extra
        and not unmapped_labels
        and not missing_decision_labels
        and package_strategy_mapped
    )

    lines = [
        "# Google Fonts Final Values Packet",
        "",
        "This generated packet maps the maintainer decision sheet to the JSON",
        "values file consumed by `scripts/apply_final_values.py`.",
        "",
        "## Summary",
        "",
        f"- Final values packet ready: {yes_no(ready)}",
        f"- Decision rows mapped to JSON keys: {mapped_row_count} / {len(decisions)}",
        f"- Required JSON keys present in template: {len(required - set(missing_required))} / {len(required)}",
        f"- Optional JSON keys present in template: {len(OPTIONAL_KEYS & template_keys)} / {len(OPTIONAL_KEYS)}",
        f"- Unknown template keys: {len(extra)}",
        f"- Unmapped decision rows: {len(unmapped_labels)}",
        "",
        "## Fill This File",
        "",
        "1. Copy `documentation/google-fonts-final-values.template.json` to a",
        "   scratch path outside the repo or to a private working file.",
        "2. Replace every placeholder value.",
        "3. Run `make final-values-check VALUES=/path/to/final-values.json`.",
        "4. Run `make apply-final-values VALUES=/path/to/final-values.json` only",
        "   after the dry-run validation passes.",
        "",
        "## Decision To JSON Map",
        "",
        "| Decision | Current evidence | Current final answer | JSON key | Template value | Note |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for label, current, answer in decisions:
        key = decision_key(label)
        value = template.get(key, "missing") if key else "unmapped"
        note = KEY_NOTES.get(key, "Add a mapping before finalization.")
        lines.append(f"| {label} | {current} | {answer} | `{key or 'unmapped'}` | `{value}` | {note} |")

    lines.extend(["", "## Optional Values", "", "| JSON key | Template value | When needed |", "| --- | --- | --- |"])
    for key in sorted(OPTIONAL_KEYS):
        lines.append(f"| `{key}` | `{template.get(key, 'missing')}` | {KEY_NOTES[key]} |")

    lines.extend(["", "## Validation Rules", ""])
    lines.extend(
        [
            "- `date_added` must be `YYYY-MM-DD`.",
            "- `source_commit` must be a lowercase 40-character git hash.",
            "- `repository_url` must be a public GitHub HTTPS URL.",
            "- `branch` must be a simple git branch name with no spaces, traversal, or ref metacharacters.",
            "- `package_source_strategy` must be `config_yaml` or `archive`.",
            "- `archive_url` is required when `package_source_strategy` is `archive`.",
            "- `google_fonts_issue_url`, when present, must be a `google/fonts` issue URL.",
            "- Values must not contain Markdown table pipe characters.",
            "",
            "## Template Coverage Issues",
            "",
        ]
    )
    issues = []
    issues.extend(f"missing required key: `{key}`" for key in missing_required)
    issues.extend(f"unknown template key: `{key}`" for key in extra)
    issues.extend(f"unmapped decision row: {label}" for label in unmapped_labels)
    issues.extend(f"decision label not present in sheet: {label}" for label in missing_decision_labels)
    if not package_strategy_mapped:
        issues.append("Package source strategy row is missing")
    if issues:
        lines.extend(f"- {issue}" for issue in issues)
    else:
        lines.append("- none")

    blockers = final_blockers(read(NEXT_ACTIONS))
    lines.extend(["", "## Current Maintainer Blockers", ""])
    if blockers:
        lines.extend(f"- {blocker}" for blocker in blockers)
    else:
        lines.append("- none")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    OUTPUT.write_text(markdown(), encoding="utf-8")
    print(f"Wrote {display_path(OUTPUT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
