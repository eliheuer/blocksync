#!/usr/bin/env python3
"""Check Add Font issue and handoff text against current release reports."""

from __future__ import annotations

from pathlib import Path
import re

from check_final_readiness import fontspector_counts


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "documentation" / "submission-handoff-readiness.md"

HANDOFF = ROOT / "documentation" / "google-fonts-submission-handoff.md"
ISSUE = ROOT / "documentation" / "google-fonts-add-font-issue-draft.md"
METADATA = ROOT / "documentation" / "google-fonts-downstream-metadata-draft.md"
FINAL_READINESS = ROOT / "documentation" / "final-readiness-report.md"
FAMILY_NAME = ROOT / "documentation" / "family-name-readiness.md"
SOURCE_READINESS = ROOT / "documentation" / "source-readiness.md"
RELEASE_METADATA = ROOT / "documentation" / "release-metadata-readiness.md"
RELEASE_REPORT = ROOT / "out" / "fontspector" / "fontspector-report.md"
PACKAGE_REPORT = ROOT / "out" / "fontspector" / "fontspector-package-context-report.md"


REQUIRED_HANDOFF_REFERENCES = [
    "documentation/namecheck-fontdata-result.json",
    "documentation/google-fonts-final-decision-sheet.md",
    "documentation/google-fonts-final-values-packet.md",
    "documentation/google-fonts-downstream-package-preview.md",
    "documentation/package-dry-run-readiness.md",
    "documentation/packager-dry-run-record.md",
    "documentation/downstream-pr-readiness.md",
    "documentation/release-archive-manifest.md",
    "documentation/next-actions.md",
    "documentation/final-submission-blockers.md",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def summary_value(label: str, text: str, default: str = "unknown") -> str:
    match = re.search(rf"^- {re.escape(label)}: (.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else default


def metadata_proto(text: str) -> str:
    match = re.search(r"```textproto\n(?P<body>.*?)\n```", text, flags=re.DOTALL)
    return match.group("body") if match else text


def scalar(proto: str, key: str) -> str:
    match = re.search(rf'^\s*{re.escape(key)}:\s+"([^"]*)"', proto, flags=re.MULTILINE)
    return match.group(1) if match else ""


def report_summary(text: str) -> tuple[int, int, int, int]:
    counts = fontspector_counts(text)
    return tuple(counts[name] for name in ("WARN", "FAIL", "FATAL", "ERROR"))


def status_row(label: str, ready: bool) -> str:
    return f"| {label} | {yes_no(ready)} |"


def main() -> int:
    handoff = read(HANDOFF)
    issue = read(ISSUE)
    metadata = metadata_proto(read(METADATA))
    final_text = read(FINAL_READINESS)
    family_text = read(FAMILY_NAME)
    source_text = read(SOURCE_READINESS)
    release_metadata = read(RELEASE_METADATA)
    release_warn, release_fail, release_fatal, release_error = report_summary(read(RELEASE_REPORT))
    package_warn, package_fail, package_fatal, package_error = report_summary(read(PACKAGE_REPORT))

    repository_url = scalar(metadata, "repository_url")
    branch = scalar(metadata, "branch")
    date_added = scalar(metadata, "date_added")
    commit = scalar(metadata, "commit")
    blocker_count = summary_value("Blocking items", final_text)
    namecheck_clear = "namecheck.fontdata.com API result clear: yes" in family_text
    namecheck_date = summary_value("namecheck.fontdata.com checked at", family_text).strip("`")
    source_ready = "Source-ready for Google Fonts build path: yes" in source_text
    version = summary_value("Source UFO version", release_metadata).strip("`")

    handoff_refs = {ref: ref in handoff for ref in REQUIRED_HANDOFF_REFERENCES}
    checks = {
        "Handoff file exists": HANDOFF.exists(),
        "Issue draft exists": ISSUE.exists(),
        "Issue title is current": "Add Blocksync" in issue,
        "Issue labels are current": "I New Font, II Submission" in issue,
        "Issue includes current repository URL": bool(repository_url and repository_url in issue),
        "Issue includes current namecheck evidence": (
            namecheck_clear
            and "namecheck.fontdata.com" in issue
            and namecheck_date in issue
            and "needs final browser check" not in issue
        ),
        "Issue includes current package-context QA outcome": (
            f"{package_fail} FAIL, {package_fatal} FATAL, {package_error} ERROR" in issue
        ),
        "Handoff includes current repository URL": bool(repository_url and repository_url in handoff),
        "Handoff includes current branch": bool(branch and branch in handoff),
        "Handoff includes current source strategy": (
            source_ready
            and "sources/Blocksync.designspace" in handoff
            and "sources/archive/" in handoff
        ),
        "Handoff includes current metadata placeholders": (
            date_added in handoff and commit in handoff
        ),
        "Handoff includes current Fontspector status": all(
            summary in handoff for summary in (
                f"{release_warn} WARN, {release_fail} FAIL, {release_fatal} FATAL, {release_error} ERROR",
                f"{package_warn} WARN, {package_fail} FAIL, {package_fatal} FATAL, {package_error} ERROR",
            )
        ),
        "Handoff links the generated final readiness report": "documentation/final-readiness-report.md" in handoff,
        "Handoff includes expected downstream branch": "gftools_packager_ofl_blocksync" in handoff,
        "Handoff includes expected downstream PR title": "Blocksync : 1.000 added" in handoff,
        "Handoff includes provenance line template": "Taken from the upstream repo <repo-url> at commit <commit-url>." in handoff,
        "All required handoff references are present": all(handoff_refs.values()),
    }
    local_ready = all(checks.values())

    lines = [
        "# Submission Handoff Readiness",
        "",
        "This generated report checks the Add Font issue draft and handoff",
        "against the current Blocksync Google Fonts release reports. It is a",
        "staleness gate for issue-opening text, not a claim that final",
        "maintainer decisions are complete.",
        "",
        "## Summary",
        "",
        f"- Submission handoff local evidence ready: {yes_no(local_ready)}",
        f"- Handoff file: `{HANDOFF.relative_to(ROOT)}`",
        f"- Issue draft file: `{ISSUE.relative_to(ROOT)}`",
        f"- Current repository URL: `{repository_url or 'missing'}`",
        f"- Current branch: `{branch or 'missing'}`",
        f"- Current `date_added`: `{date_added or 'missing'}`",
        f"- Current source commit: `{commit or 'missing'}`",
        f"- Source UFO version: `{version or 'unknown'}`",
        f"- Final readiness blockers: {blocker_count}",
        f"- Namecheck clear: {yes_no(namecheck_clear)}",
        f"- Namecheck checked at: `{namecheck_date or 'unknown'}`",
        f"- Release Fontspector WARN/FAIL/FATAL/ERROR: {release_warn}/{release_fail}/{release_fatal}/{release_error}",
        f"- Package-context Fontspector WARN/FAIL/FATAL/ERROR: {package_warn}/{package_fail}/{package_fatal}/{package_error}",
        "",
        "## Checks",
        "",
        "| Check | Ready |",
        "| --- | --- |",
    ]
    lines.extend(status_row(label, ready) for label, ready in checks.items())

    lines.extend(["", "## Required Handoff References", "", "| Reference | Present |", "| --- | --- |"])
    lines.extend(status_row(f"`{ref}`", present) for ref, present in handoff_refs.items())

    lines.extend(
        [
            "",
            "## Apply Before Opening The Issue",
            "",
            "- Regenerate this report with `make submission-handoff-readiness` after",
            "  any issue draft, handoff, metadata, namecheck, or QA report change.",
            "- Keep the Add Font issue draft in sync with the latest namecheck and",
            "  Fontspector reports before pasting it into `google/fonts`.",
            "- Do not treat this report as a substitute for `make final-readiness-check`.",
            "",
        ]
    )

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    return 0 if local_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
