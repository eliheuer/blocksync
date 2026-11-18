#!/usr/bin/env python3
"""Generate a non-final Google Fonts values proposal JSON."""

from __future__ import annotations

import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "documentation" / "google-fonts-final-values.proposal.json"
METADATA = ROOT / "documentation" / "google-fonts-downstream-metadata-draft.md"
FAMILY_NAME = ROOT / "documentation" / "family-name-readiness.md"
AUTHORSHIP = ROOT / "documentation" / "authorship-disclosure-readiness.md"
WARNINGS = ROOT / "documentation" / "fontspector-zero-warning-worklist.md"
PROOF_PACKET = ROOT / "documentation" / "proof-review-packet.md"
ARCHIVE = ROOT / "documentation" / "release-archive-manifest.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def metadata_proto(text: str) -> str:
    match = re.search(r"```textproto\n(?P<body>.*?)\n```", text, flags=re.DOTALL)
    return match.group("body") if match else text


def scalar(proto: str, key: str) -> str:
    match = re.search(rf'^\s*{re.escape(key)}:\s+"([^"]*)"', proto, flags=re.MULTILINE)
    return match.group(1) if match else ""


def summary_value(label: str, text: str, default: str = "") -> str:
    match = re.search(rf"^- {re.escape(label)}: (.+)$", text, flags=re.MULTILINE)
    value = match.group(1).strip() if match else default
    if value.startswith("`") and value.endswith("`"):
        return value.strip("`")
    return value


def main() -> int:
    metadata = metadata_proto(read(METADATA))
    family = read(FAMILY_NAME)
    authorship = read(AUTHORSHIP)
    warnings = read(WARNINGS)
    proof = read(PROOF_PACKET)
    archive = read(ARCHIVE)

    namecheck_date = summary_value("namecheck.fontdata.com checked at", family)
    namecheck_clear = "namecheck.fontdata.com API result clear: yes" in family
    namecheck_result = ""
    if namecheck_clear and namecheck_date:
        namecheck_result = (
            f"namecheck.fontdata.com API clear on {namecheck_date}: zero matches "
            "at confidence 0.3-1.0 and trademark=false"
        )

    authors = summary_value("AUTHORS.txt entries", authorship)
    contributors = summary_value("CONTRIBUTORS.txt entries", authorship)
    warning_floor = summary_value("Package-context warning checks", warnings)
    proof_pages = summary_value("Proof HTML pages linked", proof)
    proof_fonts = summary_value("Proof fonts linked", proof)
    archive_ready = summary_value("Local release archive hashes match source files", archive)

    values = {
        "_note": (
            "Non-final proposal generated from local evidence. Empty strings still "
            "need maintainer values before make final-values-check can pass."
        ),
        "date_added": "",
        "source_commit": "",
        "repository_url": scalar(metadata, "repository_url"),
        "branch": scalar(metadata, "branch"),
        "designer": scalar(metadata, "designer"),
        "package_source_strategy": "config_yaml",
        "archive_url": "",
        "namecheck_result": namecheck_result,
        "ai_use_disclosure": "",
        "authorship_cla_rfn_status": (
            f"AUTHORS.txt: {authors}; CONTRIBUTORS.txt: {contributors}; "
            "OFL declares no project-specific Reserved Font Names. "
            "CLA identity remains a maintainer-only final check before submission."
        ),
        "fontspector_warning_decision": "",
        "visual_proof_decision": "",
        "generated_composites_decision": "",
        "static_ttf_decision": (
            "Keep static TTFs as local proof outputs only unless Google Fonts asks for downstream static files."
        ),
        "release_archive_fallback_decision": (
            "Use source.config_yaml with sources/config.yaml for first submission; "
            f"release/archive fallback remains available with local archive hashes match: {archive_ready}."
        ),
        "google_fonts_issue_url": "",
        "_review_context": (
            f"Fontspector warning floor: {warning_floor}; proof pages: {proof_pages}; "
            f"proof fonts: {proof_fonts}; see documentation/proof-review-packet.md "
            "and documentation/google-fonts-final-values-packet.md."
        ),
    }

    OUTPUT.write_text(json.dumps(values, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
