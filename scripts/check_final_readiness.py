#!/usr/bin/env python3
"""Check whether Blocksync is final-ready for Google Fonts submission."""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "documentation" / "final-readiness-report.md"
METADATA = ROOT / "documentation" / "google-fonts-downstream-metadata-draft.md"
DECISIONS = ROOT / "documentation" / "google-fonts-final-decision-sheet.md"
WARNINGS = ROOT / "documentation" / "fontspector-zero-warning-worklist.md"
RELEASE_METADATA_READINESS = ROOT / "documentation" / "release-metadata-readiness.md"
SOURCE_READINESS = ROOT / "documentation" / "source-readiness.md"
FAMILY_NAME_READINESS = ROOT / "documentation" / "family-name-readiness.md"
AUTHORSHIP_DISCLOSURE_READINESS = ROOT / "documentation" / "authorship-disclosure-readiness.md"
PACKAGER_SOURCE_STRATEGY = ROOT / "documentation" / "packager-source-strategy.md"
PROOF_REVIEW_READINESS = ROOT / "documentation" / "proof-review-readiness.md"
PROOF_REVIEW_PACKET = ROOT / "documentation" / "proof-review-packet.md"
PROOF_INDEX = ROOT / "out" / "proof" / "index.html"
RELEASE_REPORT = ROOT / "out" / "fontspector" / "fontspector-report.md"
PACKAGE_REPORT = ROOT / "out" / "fontspector" / "fontspector-package-context-report.md"
ARCHIVE_MANIFEST = ROOT / "documentation" / "release-archive-manifest.md"
PACKAGER_READINESS = ROOT / "documentation" / "package-dry-run-readiness.md"
PACKAGER_DRY_RUN_RECORD = ROOT / "documentation" / "packager-dry-run-record.md"
DOWNSTREAM_PR_READINESS = ROOT / "documentation" / "downstream-pr-readiness.md"
SUBMISSION_HANDOFF_READINESS = ROOT / "documentation" / "submission-handoff-readiness.md"
AGENT_REUSE_READINESS = ROOT / "documentation" / "google-fonts-agent-reuse-readiness.md"
PLACEHOLDER_AUDIT = ROOT / "documentation" / "open-placeholder-audit.md"
DECISION_APPLICATION = ROOT / "documentation" / "decision-application-blockers.md"
OFL = ROOT / "OFL.txt"
SOURCES = ROOT / "sources"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def report_summary(text: str) -> tuple[int, int, int]:
    match = re.search(
        r"Summary:\s+SKIP:\s+\d+\s+INFO:\s+\d+\s+PASS:\s+\d+\s+WARN:\s+(\d+)\s+FAIL:\s+(\d+)\s+FATAL:\s+(\d+)\s+ERROR:\s+(\d+)",
        text,
    )
    if not match:
        return 0, 0, 0
    warn, fail, fatal, error = (int(value) for value in match.groups())
    return warn, fail + fatal + error, error


def final_answer_cells(decision_text: str) -> list[str]:
    cells: list[str] = []
    for line in decision_text.splitlines():
        if not line.startswith("| ") or line.startswith("| ---"):
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) >= 3 and parts[0] not in {"Decision", "Review item"}:
            cells.append(parts[2])
    return cells


def decision_answers(decision_text: str) -> dict[str, str]:
    answers: dict[str, str] = {}
    for line in decision_text.splitlines():
        if not line.startswith("| ") or line.startswith("| ---"):
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) >= 3 and parts[0] not in {"Decision", "Review item"}:
            answers[parts[0]] = parts[2]
    return answers


def is_unresolved_answer(answer: str) -> bool:
    return (
        not answer
        or answer
        in {
            "TBD",
            "Confirm or replace",
            "Confirm wording",
            "Confirm",
            "Accept for first review or schedule source cleanup",
            "Accept, revise, or defer",
            "Keep proof-only unless Google Fonts asks",
            "Use only if Google Fonts rejects `source.config_yaml` path",
        }
        or answer.startswith("Confirm ")
        or answer.startswith("Maintainer review")
    )


def accepted_answer(answer: str) -> bool:
    lowered = answer.lower()
    return not is_unresolved_answer(answer) and any(
        marker in lowered
        for marker in ["accept", "accepted", "reviewed", "approved"]
    )


def archive_strategy_selected(metadata: str, decisions: str) -> bool:
    answers = decision_answers(decisions)
    strategy = answers.get("Package source strategy", "").lower()
    fallback = answers.get("Release/archive fallback", "").lower()
    metadata_source = re.search(r"^source\s+\{\n(.*?)^\}", metadata, flags=re.MULTILINE | re.DOTALL)
    source_text = metadata_source.group(1) if metadata_source else metadata
    return (
        "archive_url:" in source_text
        or "release/archive package" in strategy
        or (
            "archive" in strategy
            and "source.config_yaml" not in strategy
            and "config_yaml" not in source_text
        )
        or (
            "archive" in fallback
            and "not needed" not in fallback
            and "source.config_yaml" not in fallback
        )
    )


def scalar(text: str, key: str) -> str:
    match = re.search(rf'^\s*{re.escape(key)}:\s+"([^"]*)"', text, flags=re.MULTILINE)
    return match.group(1) if match else ""


def metadata_source_block(metadata: str) -> str:
    match = re.search(r"^source\s+\{\n(.*?)^\}", metadata, flags=re.MULTILINE | re.DOTALL)
    return match.group(1) if match else ""


def copyright_text(repository_url: str) -> str:
    return f"Copyright 2023 The Blocksyncer Project Authors ({repository_url})"


def copyright_alignment_blockers(metadata: str) -> list[str]:
    source = metadata_source_block(metadata)
    repository_url = scalar(source, "repository_url")
    if not repository_url or repository_url.startswith("PENDING"):
        return []

    expected = copyright_text(repository_url)
    blockers: list[str] = []
    if expected not in metadata:
        blockers.append("metadata copyright does not match final repository_url")
    if not read(OFL).startswith(expected):
        blockers.append("OFL.txt copyright does not match final repository_url")
    for path in sorted(SOURCES.glob("Blocksync-*.ufo/fontinfo.plist")):
        if expected not in read(path):
            blockers.append(f"{path.relative_to(ROOT)} copyright does not match final repository_url")
    return blockers


def source_strategy_alignment_blockers(metadata: str, decisions: str) -> list[str]:
    strategy = decision_answers(decisions).get("Package source strategy", "")
    if is_unresolved_answer(strategy):
        return []

    source = metadata_source_block(metadata)
    config_yaml = scalar(source, "config_yaml")
    archive_url = scalar(source, "archive_url")
    has_config_key = bool(re.search(r"^\s*config_yaml:", source, flags=re.MULTILINE))
    has_archive_key = bool(re.search(r"^\s*archive_url:", source, flags=re.MULTILINE))
    normalized = strategy.replace("`", "").lower()
    wants_config = "source.config_yaml" in normalized or "config_yaml" in normalized
    wants_archive = (
        "release/archive" in normalized
        or "archive_url" in normalized
        or "archive package" in normalized
        or ("archive" in normalized and not wants_config)
    )

    if wants_config and (config_yaml != "sources/config.yaml" or has_archive_key):
        return ["metadata source strategy does not match final decision sheet"]
    if wants_archive and (not archive_url.startswith("https://") or has_config_key):
        return ["metadata source strategy does not match final decision sheet"]
    if not wants_config and not wants_archive:
        return ["package source strategy final answer is not machine-readable"]
    return []


def blocker_lines() -> list[str]:
    blockers: list[str] = []
    metadata = read(METADATA)
    decisions = read(DECISIONS)
    answers = decision_answers(decisions)
    warning_text = read(WARNINGS)
    release_metadata_readiness = read(RELEASE_METADATA_READINESS)
    source_readiness = read(SOURCE_READINESS)
    family_name_readiness = read(FAMILY_NAME_READINESS)
    authorship_disclosure_readiness = read(AUTHORSHIP_DISCLOSURE_READINESS)
    packager_source_strategy = read(PACKAGER_SOURCE_STRATEGY)
    proof_review_readiness = read(PROOF_REVIEW_READINESS)
    release_report = read(RELEASE_REPORT)
    package_report = read(PACKAGE_REPORT)
    archive_manifest = read(ARCHIVE_MANIFEST)

    if "Release metadata local evidence ready: yes" not in release_metadata_readiness:
        blockers.append("release metadata readiness report is missing or local evidence is not ready")
    if "Source-ready for Google Fonts build path: yes" not in source_readiness:
        blockers.append("designspace/UFO source-readiness report is missing or not ready")
    if "Family name local evidence ready: yes" not in family_name_readiness:
        blockers.append("family-name readiness report is missing or local evidence is not ready")
    if "Local authorship/disclosure evidence ready: yes" not in authorship_disclosure_readiness:
        blockers.append("authorship/disclosure readiness report is missing or local evidence is not ready")
    if "Package source strategy local evidence ready: yes" not in packager_source_strategy:
        blockers.append("Packager source-strategy report is missing or local evidence is not ready")
    if "Proof review local evidence ready: yes" not in proof_review_readiness:
        blockers.append("proof-review readiness report is missing or local evidence is not ready")
    if "Proof review packet ready: yes" not in read(PROOF_REVIEW_PACKET):
        blockers.append("proof-review packet is missing or stale")
    if "PENDING-YYYY-MM-DD" in metadata:
        blockers.append("metadata `date_added` is still `PENDING-YYYY-MM-DD`")
    if "PENDING_FINAL_40_CHARACTER_COMMIT" in metadata:
        blockers.append("metadata `source.commit` is still pending")
    blockers.extend(copyright_alignment_blockers(metadata))
    designer_answer = answers.get("Designer string", "")
    metadata_designer = scalar(metadata, "designer")
    if not is_unresolved_answer(designer_answer) and metadata_designer != designer_answer:
        blockers.append("metadata designer does not match final decision sheet")
    blockers.extend(source_strategy_alignment_blockers(metadata, decisions))
    if is_unresolved_answer(answers.get("Family name uniqueness", "")):
        blockers.append("family name is not final-cleared at namecheck.fontdata.com")
    if is_unresolved_answer(answers.get("AI-use disclosure", "")):
        blockers.append("AI-use disclosure is still pending maintainer answer")

    unresolved_answers = [
        cell
        for cell in final_answer_cells(decisions)
        if is_unresolved_answer(cell)
    ]
    if unresolved_answers:
        blockers.append(
            f"final decision sheet still has unresolved answer cells: {len(unresolved_answers)}"
        )

    release_warn, release_bad, _ = report_summary(release_report)
    package_warn, package_bad, _ = report_summary(package_report)
    if release_bad:
        blockers.append("release Fontspector report has FAIL/FATAL/ERROR results")
    if package_bad:
        blockers.append("package-context Fontspector report has FAIL/FATAL/ERROR results")
    warnings_accepted = accepted_answer(answers.get("Fontspector warning floor", ""))
    if (release_warn or package_warn) and not warnings_accepted:
        blockers.append(
            f"Fontspector warning floor is not resolved or accepted: release {release_warn} WARN, package {package_warn} WARN"
        )
    if "Honest zero-warning state possible with current scope: no" in warning_text and not warnings_accepted:
        blockers.append("zero-warning worklist says true zero is not currently achieved")

    if not PROOF_INDEX.exists():
        blockers.append("proof index is missing; run `make proof`")
    if "Maintainer review required" in decisions:
        blockers.append("visual proof review is still marked maintainer-required")
    if "review glyphs" in decisions and ("Accept, revise, or defer" in decisions):
        blockers.append("generated composite review glyphs are not finally accepted/revised/deferred")

    if "Local release archive hashes match source files: yes" not in archive_manifest:
        blockers.append("fallback release archive does not match current source files")
    if (
        archive_strategy_selected(metadata, decisions)
        and "Final GitHub release archive URL recorded: pending" in archive_manifest
    ):
        blockers.append("fallback release archive URL is pending if release/archive strategy is used")

    packager_readiness = read(PACKAGER_READINESS)
    if "Ready to run final no-PR Packager dry run: yes" not in packager_readiness:
        blockers.append("no-PR Packager dry run is not ready to start")
    if "Final no-PR Packager dry run recorded: yes" not in read(PACKAGER_DRY_RUN_RECORD):
        blockers.append("final no-PR Packager dry run has not been recorded")
    downstream_pr_readiness = read(DOWNSTREAM_PR_READINESS)
    if "Ready to open downstream PR: yes" not in downstream_pr_readiness:
        blockers.append("downstream Google Fonts PR readiness is not complete")
    if "Submission handoff local evidence ready: yes" not in read(SUBMISSION_HANDOFF_READINESS):
        blockers.append("submission handoff readiness report is missing or stale")
    if "Reusable agent bundle ready: yes" not in read(AGENT_REUSE_READINESS):
        blockers.append("reusable Google Fonts agent workflow readiness is not complete")
    if "Public placeholder blocker count:" not in read(PLACEHOLDER_AUDIT):
        blockers.append("open placeholder audit is missing or stale")
    if "Decision rows tracked:" not in read(DECISION_APPLICATION):
        blockers.append("decision-application blocker report is missing or stale")

    return blockers


def markdown(blockers: list[str]) -> str:
    lines = [
        "# Final Readiness Report",
        "",
        "This report is intentionally stricter than `make release-check`. The",
        "release handoff can be locally coherent while final Google Fonts",
        "submission is still blocked by maintainer decisions, external checks, or",
        "reviewer-accepted warnings.",
        "",
        "## Verdict",
        "",
        f"- Final-ready for Google Fonts submission: {'yes' if not blockers else 'no'}",
        f"- Blocking items: {len(blockers)}",
        "",
        "## Blocking Items",
        "",
    ]
    if blockers:
        lines.extend(f"- {blocker}" for blocker in blockers)
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Required Final Gate",
            "",
            "Run this check after `make release-check`, `make proof`, final metadata",
            "replacement, namecheck confirmation, maintainer disclosures, proof",
            "review, and no-PR Packager dry run are complete.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    blockers = blocker_lines()
    OUTPUT.write_text(markdown(blockers), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    if blockers:
        print(f"Final readiness blocked: {len(blockers)} item(s)")
        for blocker in blockers:
            print(f"- {blocker}")
        return 1
    print("Final readiness passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
