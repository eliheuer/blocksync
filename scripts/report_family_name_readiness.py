#!/usr/bin/env python3
"""Generate a family-name readiness report for Blocksync."""

from __future__ import annotations

import json
from pathlib import Path
import re

from fontTools.ttLib import TTFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "documentation" / "family-name-readiness.md"
DEFAULT_FONT = ROOT / "fonts" / "variable" / "Blocksync[wdth,wght].ttf"
DECISIONS = ROOT / "documentation" / "google-fonts-final-decision-sheet.md"
NAME_AUDIT = ROOT / "documentation" / "google-fonts-name-audit.md"
NAMECHECK_RESULT = ROOT / "documentation" / "namecheck-fontdata-result.json"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def entries(path: Path) -> list[str]:
    return [
        line.strip()
        for line in read(path).splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def name_values(font_path: Path) -> dict[int, list[str]]:
    values: dict[int, list[str]] = {1: [], 2: [], 4: [], 6: [], 16: [], 17: []}
    if not font_path.exists():
        return values
    font = TTFont(font_path)
    try:
        for record in font["name"].names:
            if record.nameID not in values:
                continue
            value = record.toUnicode()
            if value not in values[record.nameID]:
                values[record.nameID].append(value)
    finally:
        font.close()
    return values


def row_final_answer(decision_name: str, decisions: str) -> str:
    for line in decisions.splitlines():
        if not line.startswith(f"| {decision_name} |"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        return cells[2] if len(cells) >= 3 else "unknown"
    return "unknown"


def ofl_rfn_status() -> tuple[bool, list[str]]:
    lines = read(ROOT / "OFL.txt").splitlines()
    header_lines: list[str] = []
    for line in lines[1:12]:
        if line.startswith("This Font Software is licensed"):
            break
        header_lines.append(line.strip())
    rfn_lines = [line for line in header_lines if "reserved font name" in line.lower()]
    return not rfn_lines, rfn_lines


def ascii_safe(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9 ]+", value))


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def namecheck_result() -> dict[str, object]:
    if not NAMECHECK_RESULT.exists():
        return {}
    data = json.loads(NAMECHECK_RESULT.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def main() -> int:
    decisions = read(DECISIONS)
    name_audit = read(NAME_AUDIT)
    namecheck = namecheck_result()
    names = name_values(DEFAULT_FONT)
    family_names = sorted(set(names[16] or names[1]))
    subfamily_names = sorted(set(names[17] or names[2]))
    authors = entries(ROOT / "AUTHORS.txt")
    contributors = entries(ROOT / "CONTRIBUTORS.txt")
    no_rfn, rfn_lines = ofl_rfn_status()
    family_answer = row_final_answer("Family name uniqueness", decisions)
    authorship_answer = row_final_answer("Authorship/CLA/RFN status", decisions)
    confidence = namecheck.get("confidence", {})
    confidence_clear = (
        isinstance(confidence, dict)
        and bool(confidence)
        and all(value == 0 for value in confidence.values())
    )
    namecheck_clear = (
        namecheck.get("query") == "Blocksync"
        and namecheck.get("result") == "clear"
        and confidence_clear
        and namecheck.get("trademark") is False
    )
    final_namecheck = namecheck_clear or family_answer not in {
        "Confirm `namecheck.fontdata.com` result",
        "unknown",
    }
    final_authorship = authorship_answer not in {"Confirm", "unknown"} and not authorship_answer.lower().startswith("pending")
    app_menu_ready = family_names == ["Blocksync"] and "Regular" in subfamily_names
    local_ready = (
        DEFAULT_FONT.exists()
        and app_menu_ready
        and all(ascii_safe(name) for name in family_names)
        and no_rfn
        and bool(authors)
        and bool(contributors)
    )
    final_ready = local_ready and final_namecheck and final_authorship

    lines = [
        "# Family Name Readiness",
        "",
        "This generated report separates objective local family-name evidence",
        "from maintainer-only final clearance for Google Fonts onboarding.",
        "",
        "## Summary",
        "",
        f"- Built font inspected: {yes_no(DEFAULT_FONT.exists())}",
        f"- Family name local evidence ready: {yes_no(local_ready)}",
        f"- Family name final-ready for submission: {yes_no(final_ready)}",
        f"- Built family names: `{', '.join(family_names) if family_names else 'unknown'}`",
        f"- Built subfamily names include Regular: {yes_no('Regular' in subfamily_names)}",
        f"- Family names are ASCII letters/digits/spaces only: {yes_no(bool(family_names) and all(ascii_safe(name) for name in family_names))}",
        f"- OFL declares no project-specific Reserved Font Names: {yes_no(no_rfn)}",
        f"- Namecheck final confirmation recorded: {yes_no(final_namecheck)}",
        f"- namecheck.fontdata.com API result clear: {yes_no(namecheck_clear)}",
        f"- namecheck.fontdata.com checked at: `{namecheck.get('checked_at', 'missing')}`",
        f"- Authorship/CLA/RFN final confirmation recorded: {yes_no(final_authorship)}",
        "",
        "## Built Name Records",
        "",
        "| name ID | Values |",
        "| --- | --- |",
    ]
    for name_id in [1, 2, 4, 6, 16, 17]:
        values = names[name_id]
        lines.append(f"| {name_id} | {', '.join(f'`{value}`' for value in values) if values else '`unset`'} |")

    lines.extend(
        [
            "",
            "## Local Evidence",
            "",
            f"- AUTHORS.txt entries: `{', '.join(authors) if authors else 'none'}`",
            f"- CONTRIBUTORS.txt entries: `{', '.join(contributors) if contributors else 'none'}`",
            f"- Current name audit says final `namecheck.fontdata.com` check is still required: {yes_no('still needs a direct final check' in name_audit)}",
            f"- Recorded namecheck source: `{namecheck.get('source', 'missing')}`",
            f"- Recorded namecheck confidence buckets: `{confidence if confidence else 'missing'}`",
            f"- Recorded trademark flag: `{namecheck.get('trademark', 'missing')}`",
        ]
    )
    if rfn_lines:
        lines.extend(f"- Potential RFN header line: `{line}`" for line in rfn_lines)
    else:
        lines.append("- No project-specific RFN declaration found before the OFL body.")

    lines.extend(
        [
            "",
            "## Finalization",
            "",
            "- Keep `documentation/namecheck-fontdata-result.json` fresh before",
            "  opening the Add Font issue.",
            "- Confirm authorship, CLA identity, and RFN status in the decision",
            "  sheet before running final downstream package checks.",
            "",
        ]
    )

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
