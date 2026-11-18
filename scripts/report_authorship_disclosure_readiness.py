#!/usr/bin/env python3
"""Generate an authorship and disclosure readiness report for Blocksync."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "documentation" / "authorship-disclosure-readiness.md"
DECISIONS = ROOT / "documentation" / "google-fonts-final-decision-sheet.md"
ISSUE_DRAFT = ROOT / "documentation" / "google-fonts-add-font-issue-draft.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def entries(path: Path) -> list[str]:
    return [
        line.strip()
        for line in read(path).splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def row_final_answer(decision_name: str, decisions: str) -> str:
    for line in decisions.splitlines():
        if not line.startswith(f"| {decision_name} |"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        return cells[2] if len(cells) >= 3 else "unknown"
    return "unknown"


def issue_checkbox_status(issue_text: str, phrase: str) -> bool:
    return phrase in issue_text


def has_ofl_source_requirement(issue_text: str) -> bool:
    normalized = re.sub(r"\s+", " ", issue_text)
    return "available in a Github repository" in normalized and "under the OFL" in normalized


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def main() -> int:
    decisions = read(DECISIONS)
    issue = read(ISSUE_DRAFT)
    authors = entries(ROOT / "AUTHORS.txt")
    contributors = entries(ROOT / "CONTRIBUTORS.txt")
    ai_answer = row_final_answer("AI-use disclosure", decisions)
    designer_answer = row_final_answer("Designer string", decisions)
    authorship_answer = row_final_answer("Authorship/CLA/RFN status", decisions)
    ai_final = ai_answer not in {"Confirm wording", "unknown"}
    designer_final = designer_answer not in {"Confirm or replace", "unknown"}
    authorship_final = authorship_answer not in {"Confirm", "unknown"}
    local_ready = (
        authors == ["Eli Heuer"]
        and contributors == ["Eli Heuer"]
        and issue_checkbox_status(issue, "clearly disclosing if AI tools were used")
        and issue_checkbox_status(issue, "no Reserved Font Names")
        and issue_checkbox_status(issue, "maintain the repository")
    )
    final_ready = local_ready and ai_final and designer_final and authorship_final

    lines = [
        "# Authorship And Disclosure Readiness",
        "",
        "This generated report tracks Google Fonts authorship, maintainer,",
        "AI-use disclosure, RFN, and designer-string readiness for Blocksync.",
        "",
        "## Summary",
        "",
        f"- Local authorship/disclosure evidence ready: {yes_no(local_ready)}",
        f"- Authorship/disclosure final-ready for submission: {yes_no(final_ready)}",
        f"- AUTHORS.txt entries: `{', '.join(authors) if authors else 'none'}`",
        f"- CONTRIBUTORS.txt entries: `{', '.join(contributors) if contributors else 'none'}`",
        f"- Designer string final confirmation recorded: {yes_no(designer_final)}",
        f"- AI-use disclosure final wording recorded: {yes_no(ai_final)}",
        f"- Authorship/CLA/RFN final confirmation recorded: {yes_no(authorship_final)}",
        "",
        "## Issue Draft Coverage",
        "",
        "| Requirement surface | Present in draft |",
        "| --- | --- |",
        f"| OFL source availability | {yes_no(has_ofl_source_requirement(issue))} |",
        f"| Copyright authorship and AI-use disclosure checkbox | {yes_no('clearly disclosing if AI tools were used' in issue)} |",
        f"| RFN checkbox | {yes_no('no Reserved Font Names' in issue)} |",
        f"| Maintenance commitment checkbox | {yes_no('maintain the repository' in issue)} |",
        "",
        "## Open Final Decisions",
        "",
        f"- Designer string: {designer_answer}",
        f"- AI-use disclosure: {ai_answer}",
        f"- Authorship/CLA/RFN status: {authorship_answer}",
        "",
        "## Finalization",
        "",
        "- Replace draft AI-use language with maintainer-approved wording before",
        "  opening the Add Font issue.",
        "- Confirm the Google CLA identity matches the downstream PR author.",
        "- Keep AUTHORS.txt, CONTRIBUTORS.txt, OFL.txt, metadata designer field,",
        "  and issue text aligned after any authorship change.",
        "",
    ]

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {display_path(OUTPUT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
