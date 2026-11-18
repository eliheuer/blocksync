#!/usr/bin/env python3
"""Map Blocksync final decisions to the Google Fonts gates they block."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/decision-application-blockers.md")
DECISION_SHEET = ROOT / "documentation" / "google-fonts-final-decision-sheet.md"
METADATA_DRAFT = ROOT / "documentation" / "google-fonts-downstream-metadata-draft.md"
PACKAGE_DRY_RUN = ROOT / "documentation" / "package-dry-run-readiness.md"
DOWNSTREAM_PR = ROOT / "documentation" / "downstream-pr-readiness.md"
ARCHIVE_MANIFEST = ROOT / "documentation" / "release-archive-manifest.md"
OPEN_PLACEHOLDERS = ROOT / "documentation" / "open-placeholder-audit.md"
WARNINGS = ROOT / "documentation" / "fontspector-zero-warning-worklist.md"
PROOF_REVIEW = ROOT / "documentation" / "proof-review-readiness.md"


UNRESOLVED_VALUES = {
    "TBD",
    "Confirm",
    "Confirm or replace",
    "Confirm wording",
    "Confirm `namecheck.fontdata.com` result",
    "Keep proof-only unless Google Fonts asks",
    "Accept for first review or schedule source cleanup",
    "Accept, revise, or defer",
    "Use only if Google Fonts rejects `source.config_yaml` path",
}


@dataclass(frozen=True)
class DecisionRow:
    section: str
    item: str
    current_value: str
    final_answer: str
    apply_to: str


@dataclass(frozen=True)
class GateRow:
    item: str
    final_answer: str
    downstream_metadata: str
    package_dry_run: str
    downstream_pr: str
    current_blocker: str
    apply_surfaces: str


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def summary_value(label: str, text: str, default: str = "unknown") -> str:
    match = re.search(rf"^- {re.escape(label)}: (.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else default


def parse_decision_rows(text: str) -> list[DecisionRow]:
    rows: list[DecisionRow] = []
    section = ""
    for line in text.splitlines():
        if line.startswith("## "):
            section = line.removeprefix("## ").strip()
            continue
        if not line.startswith("| ") or line.startswith("| ---"):
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if parts[0] in {"Decision", "Review item"}:
            continue
        if section == "Required Final Values" and len(parts) >= 4:
            rows.append(DecisionRow(section, parts[0], parts[1], parts[2], parts[3]))
        elif section == "Review Decisions" and len(parts) >= 3:
            rows.append(DecisionRow(section, parts[0], parts[1], parts[2], "review log / handoff docs"))
    return rows


def is_unresolved(answer: str) -> bool:
    return (
        not answer
        or answer in UNRESOLVED_VALUES
        or answer.startswith("Confirm ")
        or answer.startswith("Maintainer review")
        or answer.lower().startswith("pending")
    )


def gate_for_row(row: DecisionRow, metadata: str, package: str, downstream: str, archive: str) -> GateRow:
    item_key = row.item.lower()
    unresolved = is_unresolved(row.final_answer)
    current_blocker = "unresolved final answer" if unresolved else "answer recorded"
    downstream_metadata = "does not block"
    package_dry_run = "does not block directly"
    downstream_pr = "does not block directly"

    if "date_added" in item_key:
        current_blocker = (
            "`PENDING-YYYY-MM-DD` still present"
            if "PENDING-YYYY-MM-DD" in metadata
            else current_blocker
        )
        downstream_metadata = "blocks"
        package_dry_run = "blocks"
        downstream_pr = "blocks"
    elif "source commit" in item_key:
        current_blocker = (
            "`PENDING_FINAL_40_CHARACTER_COMMIT` still present"
            if "PENDING_FINAL_40_CHARACTER_COMMIT" in metadata
            else current_blocker
        )
        downstream_metadata = "blocks"
        package_dry_run = "blocks"
        downstream_pr = "blocks"
    elif "public upstream" in item_key or "default branch" in item_key:
        downstream_metadata = "blocks until confirmed"
        package_dry_run = "blocks if changed"
        downstream_pr = "blocks issue/PR text if changed"
    elif "package source strategy" in item_key:
        downstream_metadata = "blocks source block finalization"
        package_dry_run = "blocks source mode"
        downstream_pr = "blocks package provenance"
        if "Final GitHub release archive URL recorded: pending" in archive:
            current_blocker = "release/archive fallback URL pending if selected"
    elif "family name" in item_key:
        downstream_pr = "blocks Add Font issue"
        current_blocker = "namecheck result not recorded" if unresolved else current_blocker
    elif "designer" in item_key or "authorship" in item_key:
        downstream_metadata = "blocks if changed"
        downstream_pr = "blocks Add Font issue"
    elif "ai-use" in item_key:
        downstream_pr = "blocks Add Font issue"
    elif "fontspector" in item_key:
        package_dry_run = "blocks only if not accepted or fixed"
        downstream_pr = "blocks warning rationale"
        current_blocker = summary_value("Remaining Fontspector warning floor", read(ROOT / "documentation" / "next-actions.md"), "warning floor unresolved")
    elif "visual proof" in item_key:
        downstream_pr = "blocks review confidence"
        current_blocker = "maintainer proof review not recorded"
    elif "composites" in item_key:
        package_dry_run = "blocks if source cleanup chosen"
        downstream_pr = "blocks if review glyphs are not accepted/deferred"
    elif "static ttfs" in item_key:
        package_dry_run = "blocks only if Google Fonts asks for static files"
        downstream_pr = "blocks only if package file list changes"
    elif "release/archive fallback" in item_key:
        package_dry_run = "blocks only if release/archive strategy is selected"
        downstream_pr = "blocks only if release/archive strategy is selected"
        current_blocker = summary_value("Final GitHub release archive URL recorded", archive)

    return GateRow(
        item=row.item,
        final_answer=row.final_answer,
        downstream_metadata=downstream_metadata,
        package_dry_run=package_dry_run,
        downstream_pr=downstream_pr,
        current_blocker=current_blocker,
        apply_surfaces=row.apply_to,
    )


def markdown_report() -> str:
    decisions = read(DECISION_SHEET)
    metadata = read(METADATA_DRAFT)
    package = read(PACKAGE_DRY_RUN)
    downstream = read(DOWNSTREAM_PR)
    archive = read(ARCHIVE_MANIFEST)
    placeholders = read(OPEN_PLACEHOLDERS)
    warnings = read(WARNINGS)
    proof_review = read(PROOF_REVIEW)

    rows = parse_decision_rows(decisions)
    unresolved_rows = [row for row in rows if is_unresolved(row.final_answer)]
    gate_rows = [
        gate_for_row(row, metadata, package, downstream, archive)
        for row in rows
    ]
    metadata_blockers = [
        row for row in gate_rows if row.downstream_metadata.startswith("blocks")
    ]
    package_blockers = [
        row for row in gate_rows if row.package_dry_run.startswith("blocks")
    ]
    pr_blockers = [row for row in gate_rows if row.downstream_pr.startswith("blocks")]

    lines = [
        "# Decision Application Blockers",
        "",
        "This generated report maps each remaining maintainer decision or",
        "finalization item to the exact Google Fonts packaging gate it affects.",
        "It is the apply surface after `documentation/google-fonts-final-decision-sheet.md`",
        "is filled in.",
        "",
        "## Summary",
        "",
        f"- Decision rows tracked: {len(rows)}",
        f"- Unresolved final-answer rows: {len(unresolved_rows)}",
        f"- Unresolved row names: {', '.join(row.item for row in unresolved_rows) if unresolved_rows else 'none'}",
        f"- Public placeholder blocker count: {summary_value('Public placeholder blocker count', placeholders)}",
        f"- Metadata has pending date_added: {'yes' if 'PENDING-YYYY-MM-DD' in metadata else 'no'}",
        f"- Metadata has pending source.commit: {'yes' if 'PENDING_FINAL_40_CHARACTER_COMMIT' in metadata else 'no'}",
        f"- Downstream metadata blocking decision rows: {len(metadata_blockers)}",
        f"- Package dry-run blocking decision rows: {len(package_blockers)}",
        f"- Downstream PR blocking decision rows: {len(pr_blockers)}",
        f"- Package dry-run first blocker: {summary_value('First blocker', package)}",
        f"- Downstream PR first blocker: {summary_value('First blocker', downstream)}",
        f"- Final GitHub release archive URL recorded: {summary_value('Final GitHub release archive URL recorded', archive)}",
        f"- Zero-warning possible with current scope: {summary_value('Honest zero-warning state possible with current scope', warnings)}",
        f"- Proof review local evidence ready: {summary_value('Proof review local evidence ready', proof_review)}",
        "",
        "## Blocker Map",
        "",
        "| Item | Final answer | Downstream metadata | Package dry run | Downstream PR | Current blocker marker | Apply surfaces |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in gate_rows:
        lines.append(
            f"| {row.item} | {row.final_answer} | {row.downstream_metadata} | "
            f"{row.package_dry_run} | {row.downstream_pr} | {row.current_blocker} | {row.apply_surfaces} |"
        )

    lines.extend(
        [
            "",
            "## Apply Order",
            "",
            "1. Fill every unresolved final-answer cell in `documentation/google-fonts-final-decision-sheet.md`.",
            "2. Apply final `date_added`, `source.commit`, branch, designer, and package source decisions to `documentation/google-fonts-downstream-metadata-draft.md`.",
            "3. Apply namecheck, authorship, AI-use, warning-floor, proof, and composite-review decisions to the Add Font issue draft and handoff docs.",
            "4. If release/archive packaging is selected, publish the archive and record the final `source.archive_url`.",
            "5. Rerun `make release-check`, `make placeholder-audit`, `make decision-application-check`, and `make final-readiness-check`.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    output = ROOT / (Path(sys.argv[1]) if len(sys.argv) > 1 else OUTPUT_DEFAULT)
    output.write_text(markdown_report(), encoding="utf-8")
    print(f"Wrote {output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
