#!/usr/bin/env python3
"""Report unresolved Google Fonts release placeholders for Blocksync."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/open-placeholder-audit.md")

INCLUDE_FILES = [
    Path("AGENTS.md"),
    Path("GF_READINESS.md"),
    Path("OFL.txt"),
    Path("AUTHORS.txt"),
    Path("CONTRIBUTORS.txt"),
    Path("Makefile"),
    Path("sources/config.yaml"),
    Path("sources/Blocksync.designspace"),
    Path("scripts/package_gf_dry_run.sh"),
]
INCLUDE_GLOBS = [
    "documentation/*.md",
    "documentation/*.html",
]
EXCLUDE_FILES = {
    OUTPUT_DEFAULT,
}
GENERATED_EVIDENCE_FILES = {
    Path("documentation/authorship-disclosure-readiness.md"),
    Path("documentation/decision-application-blockers.md"),
    Path("documentation/downstream-pr-readiness.md"),
    Path("documentation/family-name-readiness.md"),
    Path("documentation/final-readiness-report.md"),
    Path("documentation/final-submission-blockers.md"),
    Path("documentation/fontspector-zero-warning-worklist.md"),
    Path("documentation/google-fonts-agent-reuse-readiness.md"),
    Path("documentation/google-fonts-final-values-packet.md"),
    Path("documentation/google-fonts-maintainer-decision-request.md"),
    Path("documentation/next-actions.md"),
    Path("documentation/package-dry-run-readiness.md"),
    Path("documentation/packager-source-strategy.md"),
    Path("documentation/proof-review-packet.md"),
    Path("documentation/proof-review-readiness.md"),
    Path("documentation/release-archive-manifest.md"),
    Path("documentation/release-metadata-readiness.md"),
    Path("documentation/source-readiness.md"),
    Path("documentation/submission-handoff-readiness.md"),
}
INTERNAL_GUARD_FILES = {
    Path("scripts/package_gf_dry_run.sh"),
}


@dataclass(frozen=True)
class Finding:
    kind: str
    path: Path
    line_number: int
    text: str


def is_generated_evidence(path: Path) -> bool:
    return path in GENERATED_EVIDENCE_FILES


def is_internal_guard(path: Path, line: str) -> bool:
    if path not in INTERNAL_GUARD_FILES:
        return False
    return any(
        marker in line
        for marker in [
            "PENDING-YYYY-MM-DD",
            "PENDING_FINAL_40_CHARACTER_COMMIT",
            "unresolved_metadata_markers",
        ]
    )


def iter_input_files() -> list[Path]:
    files = set()
    for path in INCLUDE_FILES:
        if (ROOT / path).exists():
            files.add(path)
    for pattern in INCLUDE_GLOBS:
        for path in ROOT.glob(pattern):
            rel_path = path.relative_to(ROOT)
            if rel_path not in EXCLUDE_FILES:
                files.add(rel_path)
    return sorted(files)


def classify_line(path: Path, line: str) -> str | None:
    stripped = line.strip()
    if not stripped:
        return None
    if is_internal_guard(path, line):
        return "internal metadata guard"
    if "PENDING-YYYY-MM-DD" in line:
        return "pending date_added"
    if "PENDING_FINAL_40_CHARACTER_COMMIT" in line:
        return "pending source commit"
    if re.search(r"\bTBD\b", line):
        return "TBD marker"
    if "<repo-url>" in line or "<commit-url>" in line:
        return "PR template placeholder"
    if "pending maintainer answer" in line:
        return "pending maintainer answer"
    if "not final-cleared" in line:
        return "pending namecheck clearance"
    if "Maintainer review required" in line:
        return "pending proof review"
    if "Confirm or replace" in line or "Confirm wording" in line:
        return "pending confirmation"
    if "Accept, revise, or defer" in line:
        return "pending review decision"
    if "Use only if Google Fonts rejects" in line:
        return "pending packaging fallback decision"
    if re.search(r"\b(TODO|FIXME)\b", line):
        return "TODO/FIXME marker"
    return None


def find_placeholders() -> list[Finding]:
    findings: list[Finding] = []
    for rel_path in iter_input_files():
        path = ROOT / rel_path
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(lines, start=1):
            kind = classify_line(rel_path, line)
            if kind:
                findings.append(
                    Finding(
                        kind=kind,
                        path=rel_path,
                        line_number=line_number,
                        text=line.strip(),
                    )
                )
    return findings


def markdown_report(findings: list[Finding]) -> str:
    public_findings = [
        finding
        for finding in findings
        if not is_generated_evidence(finding.path)
        and finding.kind != "internal metadata guard"
    ]
    guard_findings = [
        finding for finding in findings if finding.kind == "internal metadata guard"
    ]
    evidence_echoes = [finding for finding in findings if is_generated_evidence(finding.path)]

    by_kind: dict[str, list[Finding]] = {}
    public_by_kind: dict[str, list[Finding]] = {}
    for finding in findings:
        by_kind.setdefault(finding.kind, []).append(finding)
    for finding in public_findings:
        public_by_kind.setdefault(finding.kind, []).append(finding)

    lines = [
        "# Open Placeholder Audit",
        "",
        "This generated report tracks unresolved Google Fonts handoff strings",
        "that still need a maintainer answer, final metadata value, or external",
        "confirmation. Generated reports are separated from public application",
        "surfaces so echoed blockers do not look like new work.",
        "",
        "## Summary",
        "",
        f"- Public placeholder blocker count: {len(public_findings)}",
        f"- Pending date_added occurrences: {len(by_kind.get('pending date_added', []))}",
        f"- Pending source commit occurrences: {len(by_kind.get('pending source commit', []))}",
        f"- TBD markers: {len(by_kind.get('TBD marker', []))}",
        f"- PR template placeholders: {len(by_kind.get('PR template placeholder', []))}",
        f"- Pending maintainer-answer markers: {len(by_kind.get('pending maintainer answer', []))}",
        f"- Pending confirmation markers: {len(by_kind.get('pending confirmation', []))}",
        f"- Pending proof-review markers: {len(by_kind.get('pending proof review', []))}",
        f"- Pending review-decision markers: {len(by_kind.get('pending review decision', []))}",
        f"- Internal metadata guard markers: {len(guard_findings)}",
        f"- Generated evidence echoes: {len(evidence_echoes)}",
        "",
        "## Public Blockers",
        "",
    ]
    if public_findings:
        lines.extend(
            [
                "| Kind | File | Line | Text |",
                "| --- | --- | ---: | --- |",
            ]
        )
        for finding in public_findings:
            escaped_text = finding.text.replace("|", "\\|")
            lines.append(
                f"| {finding.kind} | `{finding.path}` | {finding.line_number} | `{escaped_text}` |"
            )
    else:
        lines.append("No unresolved public placeholder strings were found.")

    lines.extend(["", "## Public Blockers By Kind", ""])
    if public_by_kind:
        for kind in sorted(public_by_kind):
            lines.append(f"- {kind}: {len(public_by_kind[kind])}")
    else:
        lines.append("- none")

    lines.extend(["", "## Internal Guards", ""])
    if guard_findings:
        lines.append(
            "These strings intentionally remain in guard scripts so stale or",
        )
        lines.append("incomplete metadata cannot reach Packager.")
        lines.append("")
        lines.extend(["| Kind | File | Line | Text |", "| --- | --- | ---: | --- |"])
        for finding in guard_findings:
            escaped_text = finding.text.replace("|", "\\|")
            lines.append(
                f"| {finding.kind} | `{finding.path}` | {finding.line_number} | `{escaped_text}` |"
            )
    else:
        lines.append("No internal guard markers were found.")

    lines.extend(["", "## Generated Evidence Echoes", ""])
    if evidence_echoes:
        lines.extend(["| Kind | File | Line | Text |", "| --- | --- | ---: | --- |"])
        for finding in evidence_echoes:
            escaped_text = finding.text.replace("|", "\\|")
            lines.append(
                f"| {finding.kind} | `{finding.path}` | {finding.line_number} | `{escaped_text}` |"
            )
    else:
        lines.append("No generated report echoes were found.")

    lines.extend(
        [
            "",
            "## Apply Before Final Packaging",
            "",
            "- Replace `date_added` and `source.commit` placeholders after the final",
            "  source state is reviewed.",
            "- Replace PR provenance placeholders after the Google Fonts issue and",
            "  final upstream commit URL are known.",
            "- Resolve maintainer answer markers in the final decision sheet, issue",
            "  draft, metadata draft, and handoff document.",
            "- Regenerate this report with `make placeholder-audit` after applying",
            "  decisions.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    output = ROOT / (Path(sys.argv[1]) if len(sys.argv) > 1 else OUTPUT_DEFAULT)
    output.write_text(markdown_report(find_placeholders()), encoding="utf-8")
    print(f"Wrote {output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
