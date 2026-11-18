#!/usr/bin/env python3
"""Generate a concise final Google Fonts submission blocker report."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "documentation" / "final-submission-blockers.md"

FINAL_READINESS = ROOT / "documentation" / "final-readiness-report.md"
RELEASE_METADATA = ROOT / "documentation" / "release-metadata-readiness.md"
SOURCE_READINESS = ROOT / "documentation" / "source-readiness.md"
WARNINGS = ROOT / "documentation" / "fontspector-zero-warning-worklist.md"
METADATA_DRAFT = ROOT / "documentation" / "google-fonts-downstream-metadata-draft.md"
FAMILY_NAME = ROOT / "documentation" / "family-name-readiness.md"
AUTHORSHIP = ROOT / "documentation" / "authorship-disclosure-readiness.md"
PACKAGER_STRATEGY = ROOT / "documentation" / "packager-source-strategy.md"
PROOF_REVIEW = ROOT / "documentation" / "proof-review-readiness.md"
PROOF_REVIEW_PACKET = ROOT / "documentation" / "proof-review-packet.md"
PACKAGE_DRY_RUN = ROOT / "documentation" / "package-dry-run-readiness.md"
PACKAGER_RECORD = ROOT / "documentation" / "packager-dry-run-record.md"
DOWNSTREAM_PR = ROOT / "documentation" / "downstream-pr-readiness.md"
AGENT_REUSE = ROOT / "documentation" / "google-fonts-agent-reuse-readiness.md"
ARCHIVE = ROOT / "documentation" / "release-archive-manifest.md"
DECISIONS = ROOT / "documentation" / "google-fonts-final-decision-sheet.md"
SUBMISSION_HANDOFF = ROOT / "documentation" / "submission-handoff-readiness.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def summary_value(label: str, text: str, default: str = "unknown") -> str:
    match = re.search(rf"^- {re.escape(label)}: (.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else default


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def strip_code(value: str) -> str:
    return value.strip().strip("`")


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


def decision_rows(decision_text: str) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for line in decision_text.splitlines():
        if not line.startswith("| ") or line.startswith("| ---"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) >= 3 and cells[0] not in {"Decision", "Review item"}:
            rows.append((cells[0], cells[1], cells[2]))
    return rows


def current_metadata_value(key: str, text: str, default: str = "missing") -> str:
    match = re.search(rf'^\s*{re.escape(key)}:\s+"([^"]*)"', text, flags=re.MULTILINE)
    return match.group(1) if match else default


def source_summary(source_text: str) -> str:
    if "Source-ready for Google Fonts build path: yes" not in source_text:
        return "not ready"
    source_count = summary_value("Designspace source UFOs", source_text)
    archived_count = summary_value("Archived `.glyphs` snapshots", source_text)
    default_layers = summary_value("Active build uses default UFO layers only", source_text)
    return f"ready; {source_count} UFO sources, {archived_count} archived Glyphs snapshots, default layers only: {default_layers}"


def fontspector_summary(warning_text: str) -> str:
    warning_floor = summary_value("Package-context warning checks", warning_text)
    honest_zero = summary_value("Honest zero-warning state possible with current scope", warning_text)
    return f"{warning_floor}; honest zero-warning state possible: {honest_zero}"


def final_decision_table(rows: list[tuple[str, str, str]]) -> list[str]:
    lines = [
        "| Decision | Current evidence | Final answer |",
        "| --- | --- | --- |",
    ]
    lines.extend(f"| {name} | {evidence} | {answer} |" for name, evidence, answer in rows)
    return lines


def markdown() -> str:
    final_text = read(FINAL_READINESS)
    release_metadata_text = read(RELEASE_METADATA)
    source_text = read(SOURCE_READINESS)
    warning_text = read(WARNINGS)
    metadata_text = read(METADATA_DRAFT)
    family_text = read(FAMILY_NAME)
    authorship_text = read(AUTHORSHIP)
    strategy_text = read(PACKAGER_STRATEGY)
    proof_text = read(PROOF_REVIEW)
    proof_packet_text = read(PROOF_REVIEW_PACKET)
    dry_run_text = read(PACKAGE_DRY_RUN)
    record_text = read(PACKAGER_RECORD)
    downstream_text = read(DOWNSTREAM_PR)
    agent_text = read(AGENT_REUSE)
    archive_text = read(ARCHIVE)
    decision_text = read(DECISIONS)
    handoff_text = read(SUBMISSION_HANDOFF)
    blockers = final_blockers(final_text)
    decisions = decision_rows(decision_text)
    current_head = strip_code(summary_value("Current git HEAD", release_metadata_text))

    lines = [
        "# Final Submission Blockers",
        "",
        "This generated snapshot separates local release readiness from values",
        "or review decisions that cannot be finalized by automation alone.",
        "",
        "## Summary",
        "",
        "| Area | Current state | Final-submission requirement |",
        "| --- | --- | --- |",
        f"| Source format | {source_summary(source_text)} | Keep `sources/config.yaml` pointed at `sources/Blocksync.designspace` unless Google Fonts requests the release/archive fallback |",
        f"| Archived Glyphs sources | top-level `.glyphs` files remain out of `sources/`; archived snapshots: {summary_value('Archived `.glyphs` snapshots', source_text)} | Keep `.glyphs` files archived and out of package inputs |",
        f"| Release gate | `make release-check` currently has local evidence ready: {yes_no('Reusable agent bundle ready: yes' in agent_text and 'Source-ready for Google Fonts build path: yes' in source_text)} | Rerun after every source, metadata, package, or workflow change |",
        f"| Final readiness gate | {summary_value('Final-ready for Google Fonts submission', final_text)}; blockers: {summary_value('Blocking items', final_text, str(len(blockers)))} | Pass `make final-readiness-check` before submission |",
        f"| Release metadata | date_added: `{current_metadata_value('date_added', metadata_text)}`; commit: `{current_metadata_value('commit', metadata_text)}`; current HEAD: `{current_head}`; working tree clean: {summary_value('Working tree clean', release_metadata_text)} | Commit the reviewed release tree and apply final package date/source commit |",
        f"| Fontspector release/package context | {fontspector_summary(warning_text)} | Fix or explicitly accept remaining warning floor before opening the Add Font issue |",
        f"| Family name readiness | local evidence ready: {summary_value('Family name local evidence ready', family_text)} | Record final `namecheck.fontdata.com` clearance |",
        f"| Authorship/disclosure | local evidence ready: {summary_value('Local authorship/disclosure evidence ready', authorship_text)} | Confirm designer, authorship/CLA/RFN, and AI-use disclosure answers |",
        f"| Package source strategy | local evidence ready: {summary_value('Package source strategy local evidence ready', strategy_text)}; final-ready: {summary_value('Package source strategy final-ready for submission', strategy_text)} | Confirm `source.config_yaml` or release/archive strategy before final metadata |",
        f"| Visual proofing | local evidence ready: {summary_value('Proof review local evidence ready', proof_text)}; packet ready: {summary_value('Proof review packet ready', proof_packet_text)}; final-ready: {summary_value('Proof review final-ready for submission', proof_text)} | Human-review proof pages and generated composite glyphs |",
        f"| No-PR Packager dry run | ready: {summary_value('Ready to run final no-PR Packager dry run', dry_run_text)}; recorded: {summary_value('Final no-PR Packager dry run recorded', record_text)} | Run and record the guarded dry run after final metadata clears |",
        f"| Downstream PR | ready: {summary_value('Ready to open downstream PR', downstream_text)} | Open Google Fonts issue first, then prepare one-family downstream PR |",
        f"| Submission handoff | local evidence ready: {summary_value('Submission handoff local evidence ready', handoff_text)} | Keep the Add Font issue draft and handoff synchronized before opening the issue |",
        f"| Fallback archive | local hashes match: {summary_value('Local release archive hashes match source files', archive_text)}; final URL: {summary_value('Final GitHub release archive URL recorded', archive_text)} | Publish and record archive URL only if release/archive fallback is selected |",
        f"| Reusable workflow | reusable `.agents` bundle ready: {yes_no('Reusable agent bundle ready: yes' in agent_text)} | Copy `.agents`, scripts, and reports into future font repos with family-specific replacements |",
        "",
        "## Current Final Readiness Blockers",
        "",
    ]
    if blockers:
        lines.extend(f"- {blocker}" for blocker in blockers)
    else:
        lines.append("- none")

    lines.extend(["", "## Maintainer Decision Sheet", ""])
    lines.extend(final_decision_table(decisions))

    lines.extend(
        [
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
            "- `documentation/google-fonts-final-values.proposal.json`",
            "- `documentation/fontspector-zero-warning-worklist.md`",
            "- `documentation/package-dry-run-readiness.md`",
            "- `documentation/packager-dry-run-record.md`",
            "- `documentation/downstream-pr-readiness.md`",
            "- `documentation/submission-handoff-readiness.md`",
            "- `documentation/google-fonts-agent-reuse-readiness.md`",
            "- `documentation/release-archive-manifest.md`",
            "- `out/fontspector/fontspector-report.html`",
            "- `out/fontspector/fontspector-package-context-report.html`",
            "- `out/proof/index.html`",
            "",
            "Regenerate this snapshot with `make blockers` after release checks,",
            "metadata changes, source edits, proof review, or Google Fonts reviewer",
            "feedback.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    OUTPUT.write_text(markdown(), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
