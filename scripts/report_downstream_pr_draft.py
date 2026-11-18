#!/usr/bin/env python3
"""Generate the expected downstream google/fonts PR draft."""

from __future__ import annotations

import os
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
METADATA = Path(os.environ.get("DOWNSTREAM_METADATA_PATH", ROOT / "documentation" / "google-fonts-downstream-metadata-draft.md"))
HANDOFF = Path(os.environ.get("SUBMISSION_HANDOFF_PATH", ROOT / "documentation" / "google-fonts-submission-handoff.md"))
OUTPUT = Path(os.environ.get("DOWNSTREAM_PR_DRAFT_OUTPUT", ROOT / "documentation" / "google-fonts-downstream-pr-draft.md"))

EXPECTED_BRANCH = "gftools_packager_ofl_blocksync"
EXPECTED_TITLE = "Blocksync : 1.000 added"
PACKAGE_DIR = "ofl/blocksync"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def extract_textproto(metadata: str) -> str:
    match = re.search(r"```textproto\n(.*?)\n```", metadata, flags=re.DOTALL)
    return match.group(1) if match else ""


def scalar(text: str, key: str) -> str:
    match = re.search(rf'^\s*{re.escape(key)}:\s+"([^"]*)"', text, flags=re.MULTILINE)
    return match.group(1) if match else ""


def source_block(proto: str) -> str:
    match = re.search(r"^source\s+\{\n(.*?)^\}", proto, flags=re.MULTILINE | re.DOTALL)
    return match.group(1) if match else ""


def issue_url(handoff: str) -> str:
    match = re.search(r"^- Google Fonts issue exists:\s+(https://github\.com/google/fonts/issues/\d+)\s*$", handoff, flags=re.MULTILINE)
    return match.group(1) if match else ""


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def main() -> int:
    metadata = read(METADATA)
    handoff = read(HANDOFF)
    proto = extract_textproto(metadata)
    source = source_block(proto)
    repo_url = scalar(source, "repository_url")
    commit = scalar(source, "commit")
    branch = scalar(source, "branch")
    issue = issue_url(handoff)

    final_commit = bool(re.fullmatch(r"[0-9a-f]{40}", commit))
    final_repo = repo_url.startswith("https://github.com/")
    commit_url = f"{repo_url}/commit/{commit}" if final_repo and final_commit else ""
    provenance = (
        f"Taken from the upstream repo {repo_url} at commit {commit_url}."
        if commit_url
        else "Taken from the upstream repo <repo-url> at commit <commit-url>."
    )

    blockers: list[str] = []
    if not final_repo:
        blockers.append("source.repository_url is not a final GitHub URL")
    if not final_commit:
        blockers.append("source.commit is not a final 40-character hash")
    if not issue:
        blockers.append("Google Fonts Add Font issue URL is not recorded")
    if branch != "main":
        blockers.append(f"source.branch is not main: {branch or 'missing'}")

    ready = not blockers
    lines = [
        "# Google Fonts Downstream PR Draft",
        "",
        "This generated draft records the expected one-family downstream PR",
        "metadata after the no-PR Packager run has been reviewed.",
        "",
        "## Summary",
        "",
        f"- Downstream PR draft ready: {yes_no(ready)}",
        f"- Expected branch: `{EXPECTED_BRANCH}`",
        f"- Expected package directory: `{PACKAGE_DIR}`",
        f"- Expected PR title: `{EXPECTED_TITLE}`",
        f"- Google Fonts issue URL: `{issue or 'pending'}`",
        f"- Upstream repository URL: `{repo_url or 'missing'}`",
        f"- Upstream source commit: `{commit or 'missing'}`",
        f"- Upstream commit URL final: {yes_no(bool(commit_url))}",
        f"- First blocker: {blockers[0] if blockers else 'none'}",
        "",
        "## Blocking Items",
        "",
    ]
    lines.extend(f"- {blocker}" for blocker in blockers) if blockers else lines.append("- none")
    lines.extend(
        [
            "",
            "## PR Title",
            "",
            "```text",
            EXPECTED_TITLE,
            "```",
            "",
            "## PR Body",
            "",
            "```text",
            provenance,
            "",
            f"Related issue: {issue or '<google-fonts-issue-url>'}",
            "```",
            "",
            "## Local Branch",
            "",
            "```bash",
            f"git checkout -b {EXPECTED_BRANCH}",
            "```",
            "",
        ]
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {display_path(OUTPUT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
