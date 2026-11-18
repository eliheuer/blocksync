#!/usr/bin/env python3
"""Generate an owner-grouped Google Fonts next-actions report for Blocksync."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "documentation" / "next-actions.md"

FINAL_READINESS = ROOT / "documentation" / "final-readiness-report.md"
RELEASE_METADATA = ROOT / "documentation" / "release-metadata-readiness.md"
SOURCE_READINESS = ROOT / "documentation" / "source-readiness.md"
WARNINGS = ROOT / "documentation" / "fontspector-zero-warning-worklist.md"
PACKAGE_DRY_RUN = ROOT / "documentation" / "package-dry-run-readiness.md"
DOWNSTREAM_PR = ROOT / "documentation" / "downstream-pr-readiness.md"
PACKAGER_RECORD = ROOT / "documentation" / "packager-dry-run-record.md"
AGENT_REUSE = ROOT / "documentation" / "google-fonts-agent-reuse-readiness.md"
ARCHIVE = ROOT / "documentation" / "release-archive-manifest.md"
DECISIONS = ROOT / "documentation" / "google-fonts-final-decision-sheet.md"
FAMILY_NAME = ROOT / "documentation" / "family-name-readiness.md"
AUTHORSHIP = ROOT / "documentation" / "authorship-disclosure-readiness.md"
PACKAGER_STRATEGY = ROOT / "documentation" / "packager-source-strategy.md"
PROOF_REVIEW = ROOT / "documentation" / "proof-review-readiness.md"
PROOF_REVIEW_PACKET = ROOT / "documentation" / "proof-review-packet.md"
PLACEHOLDERS = ROOT / "documentation" / "open-placeholder-audit.md"
DECISION_APPLICATION = ROOT / "documentation" / "decision-application-blockers.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def summary_value(label: str, text: str, default: str = "unknown") -> str:
    match = re.search(rf"^- {re.escape(label)}: (.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else default


def final_blockers(text: str) -> list[str]:
    section = re.search(
        r"^## Blocking Items\n(?P<body>.*?)(?=^## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if not section:
        return []
    return [
        line[2:].strip()
        for line in section.group("body").splitlines()
        if line.startswith("- ") and line != "- none"
    ]


def unresolved_decision_rows(decision_text: str) -> list[tuple[str, str, str]]:
    unresolved_values = {
        "TBD",
        "Confirm or replace",
        "Confirm wording",
        "Confirm",
        "Accept for first review or schedule source cleanup",
        "Accept, revise, or defer",
        "Keep proof-only unless Google Fonts asks",
        "Use only if Google Fonts rejects `source.config_yaml` path",
    }
    rows: list[tuple[str, str, str]] = []
    for line in decision_text.splitlines():
        if not line.startswith("| ") or line.startswith("| ---"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 3 or cells[0] in {"Decision", "Review item"}:
            continue
        final_answer = cells[2]
        if final_answer in unresolved_values:
            rows.append((cells[0], cells[1], final_answer))
        elif final_answer.startswith(("Confirm ", "Maintainer review", "Pending")):
            rows.append((cells[0], cells[1], final_answer))
    return rows


def blocker_action(blocker: str) -> str:
    if "date_added" in blocker:
        return "Choose the final Google Fonts package date, then update the metadata draft."
    if "source.commit" in blocker:
        return "Use the reviewed final upstream commit hash in metadata and issue/PR text."
    if "namecheck" in blocker or "family name" in blocker:
        return "Run the final `namecheck.fontdata.com` check and record the result."
    if "AI-use" in blocker:
        return "Record the maintainer-approved AI-use disclosure wording."
    if "decision sheet" in blocker:
        return "Fill every final-answer cell in the maintainer decision sheet."
    if "zero-warning" in blocker:
        return "Either fix the remaining warning buckets or explicitly accept them for first review."
    if "visual proof" in blocker:
        return "Review `out/proof/index.html` and record the proof decision."
    if "generated composite" in blocker:
        return "Accept, revise, or defer the generated Latin Extended and Vietnamese review glyphs."
    if "archive URL" in blocker:
        return "Only if release/archive packaging is selected, publish the archive and add the final URL."
    if "Packager" in blocker or "dry run" in blocker:
        return "Clear final metadata and review blockers, then run the guarded no-PR Packager dry run; use the clean checkout path if the shared fork is dirty."
    if "downstream" in blocker or "PR" in blocker:
        return "Open the Google Fonts issue first, then prepare the one-family downstream PR."
    return "Resolve the blocker and rerun `make final-readiness-check`."


def classify(blockers: list[str]) -> dict[str, list[str]]:
    groups = {
        "Maintainer Decisions": [],
        "Source And Proof Review": [],
        "Packaging And Downstream": [],
    }
    for blocker in blockers:
        if any(key in blocker for key in ["date_added", "source.commit", "namecheck", "AI-use", "decision sheet"]):
            groups["Maintainer Decisions"].append(blocker)
        elif any(key in blocker for key in ["zero-warning", "visual proof", "generated composite"]):
            groups["Source And Proof Review"].append(blocker)
        else:
            groups["Packaging And Downstream"].append(blocker)
    return groups


def main() -> int:
    final_text = read(FINAL_READINESS)
    release_metadata_text = read(RELEASE_METADATA)
    source_text = read(SOURCE_READINESS)
    warning_text = read(WARNINGS)
    package_text = read(PACKAGE_DRY_RUN)
    downstream_text = read(DOWNSTREAM_PR)
    packager_record_text = read(PACKAGER_RECORD)
    agent_text = read(AGENT_REUSE)
    archive_text = read(ARCHIVE)
    decision_text = read(DECISIONS)
    family_text = read(FAMILY_NAME)
    authorship_text = read(AUTHORSHIP)
    packager_strategy_text = read(PACKAGER_STRATEGY)
    proof_review_text = read(PROOF_REVIEW)
    proof_review_packet_text = read(PROOF_REVIEW_PACKET)
    placeholder_text = read(PLACEHOLDERS)
    decision_application_text = read(DECISION_APPLICATION)

    blockers = final_blockers(final_text)
    groups = classify(blockers)
    decision_rows = unresolved_decision_rows(decision_text)

    lines = [
        "# Google Fonts Next Actions",
        "",
        "This generated report condenses the current Blocksync release blockers",
        "into an owner-grouped queue. It is intentionally short so future agents",
        "can resume Google Fonts release work without rediscovering the same",
        "state from the full documentation set.",
        "",
        "## Snapshot",
        "",
        f"- Release metadata local evidence ready: {summary_value('Release metadata local evidence ready', release_metadata_text)}",
        f"- Source-ready for designspace/UFO build path: {yes_no('Source-ready for Google Fonts build path: yes' in source_text)}",
        f"- Family-name local evidence ready: {summary_value('Family name local evidence ready', family_text)}",
        f"- Authorship/disclosure local evidence ready: {summary_value('Local authorship/disclosure evidence ready', authorship_text)}",
        f"- Package source strategy local evidence ready: {summary_value('Package source strategy local evidence ready', packager_strategy_text)}",
        f"- Proof review local evidence ready: {summary_value('Proof review local evidence ready', proof_review_text)}",
        f"- Proof review packet ready: {summary_value('Proof review packet ready', proof_review_packet_text)}",
        f"- Reusable `.agents` workflow ready: {yes_no('Reusable agent bundle ready: yes' in agent_text)}",
        f"- Final-ready for Google Fonts submission: {summary_value('Final-ready for Google Fonts submission', final_text)}",
        f"- Final readiness blockers: {summary_value('Blocking items', final_text, str(len(blockers)))}",
        f"- Remaining Fontspector warning floor: {summary_value('Package-context warning checks', warning_text)}",
        f"- No-PR Packager dry-run ready: {summary_value('Ready to run final no-PR Packager dry run', package_text)}",
        f"- No-PR Packager dry-run recorded: {summary_value('Final no-PR Packager dry run recorded', packager_record_text)}",
        f"- Downstream PR ready: {summary_value('Ready to open downstream PR', downstream_text)}",
        f"- Fallback archive URL status: {summary_value('Final GitHub release archive URL recorded', archive_text)}",
        f"- Public placeholder blocker count: {summary_value('Public placeholder blocker count', placeholder_text)}",
        f"- Decision rows tracked: {summary_value('Decision rows tracked', decision_application_text)}",
        f"- Unresolved final-answer rows: {summary_value('Unresolved final-answer rows', decision_application_text)}",
        "",
        "## Maintainer Decision Rows",
        "",
        "| Decision | Current evidence | Needed answer |",
        "| --- | --- | --- |",
    ]
    if decision_rows:
        lines.extend(f"| {name} | {evidence} | {answer} |" for name, evidence, answer in decision_rows)
    else:
        lines.append("| none | all final answers recorded | none |")

    for heading, group_blockers in groups.items():
        lines.extend(["", f"## {heading}", "", "| Blocker | Next action |", "| --- | --- |"])
        if group_blockers:
            lines.extend(f"| {blocker} | {blocker_action(blocker)} |" for blocker in group_blockers)
        else:
            lines.append("| none | none |")

    lines.extend(
        [
            "",
            "## Fast Resume Sequence",
            "",
            "1. Fill a copy of `documentation/google-fonts-final-values.template.json` with maintainer answers.",
            "2. Use `documentation/google-fonts-final-values.proposal.json` as a non-final starting point where useful; remove proposal-only `_...` keys before validation.",
            "3. Run `make final-values-check VALUES=/path/to/final-values.json`, then `make apply-final-values VALUES=/path/to/final-values.json`.",
            "4. Review `out/proof/index.html` and update the proof/composite-glyph decisions.",
            "5. Rerun `make release-check`.",
            "6. Rerun `make final-readiness-check`; if it passes, run the guarded no-PR Packager dry run, using `GF_REPO_PATH=/private/tmp/blocksync-google-fonts` if the shared fork is dirty.",
            "7. Open the Google Fonts issue, add its URL to `google_fonts_issue_url`, rerun the values helper, then prepare the scoped downstream PR after the no-PR package is reviewed.",
            "",
            "## Evidence Reports",
            "",
            "- `documentation/final-readiness-report.md`",
            "- `documentation/release-metadata-readiness.md`",
            "- `documentation/source-readiness.md`",
            "- `documentation/family-name-readiness.md`",
            "- `documentation/authorship-disclosure-readiness.md`",
            "- `documentation/packager-source-strategy.md`",
            "- `documentation/proof-review-readiness.md`",
            "- `documentation/proof-review-packet.md`",
            "- `documentation/open-placeholder-audit.md`",
            "- `documentation/decision-application-blockers.md`",
            "- `documentation/fontspector-zero-warning-worklist.md`",
            "- `documentation/package-dry-run-readiness.md`",
            "- `documentation/packager-dry-run-record.md`",
            "- `documentation/downstream-pr-readiness.md`",
            "- `documentation/google-fonts-agent-reuse-readiness.md`",
            "- `documentation/release-archive-manifest.md`",
            "- `documentation/google-fonts-submission-handoff.md`",
            "- `documentation/google-fonts-final-values.proposal.json`",
            "",
        ]
    )

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
