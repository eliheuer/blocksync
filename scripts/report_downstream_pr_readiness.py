#!/usr/bin/env python3
"""Generate a downstream Google Fonts PR readiness report for Blocksync."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path(
    os.environ.get(
        "DOWNSTREAM_PR_READINESS_OUTPUT",
        ROOT / "documentation" / "downstream-pr-readiness.md",
    )
)
GF_REPO_PATH = Path(os.environ.get("GF_REPO_PATH", "/Users/eli/GH/forks/fonts"))
GF_CLEAN_REPO_PATH = Path(os.environ.get("GF_CLEAN_REPO_PATH", "/private/tmp/blocksync-google-fonts"))
FAMILY_PATH = Path("ofl/blocksync")
EXPECTED_BRANCH = "gftools_packager_ofl_blocksync"
EXPECTED_PR_TITLE = "Blocksync : 1.000 added"
EXPECTED_PR_BODY = "Taken from the upstream repo <repo-url> at commit <commit-url>."
METADATA = Path(os.environ.get("DOWNSTREAM_METADATA_PATH", ROOT / "documentation" / "google-fonts-downstream-metadata-draft.md"))
HANDOFF = Path(os.environ.get("SUBMISSION_HANDOFF_PATH", ROOT / "documentation" / "google-fonts-submission-handoff.md"))
PACKAGER_READINESS = Path(os.environ.get("PACKAGER_READINESS_PATH", ROOT / "documentation" / "package-dry-run-readiness.md"))
PACKAGER_RECORD = Path(os.environ.get("PACKAGER_RECORD_PATH", ROOT / "documentation" / "packager-dry-run-record.md"))
PR_DRAFT = Path(os.environ.get("DOWNSTREAM_PR_DRAFT_PATH", ROOT / "documentation" / "google-fonts-downstream-pr-draft.md"))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def run(command: list[str], cwd: Path = ROOT) -> tuple[int, str]:
    result = subprocess.run(
        command,
        cwd=cwd,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    return result.returncode, result.stdout.strip()


def git(args: list[str], repo: Path = GF_REPO_PATH) -> str:
    if not (repo / ".git").exists():
        return "missing"
    _code, output = run(["git", "-C", str(repo), *args])
    return output or "missing"


def git_ahead_behind(left: str, right: str, repo: Path = GF_REPO_PATH) -> tuple[str, str]:
    if not (repo / ".git").exists():
        return "missing", "missing"
    code, output = run(["git", "-C", str(repo), "rev-list", "--left-right", "--count", f"{left}...{right}"])
    parts = output.split()
    if code or len(parts) != 2:
        return "unknown", "unknown"
    return parts[0], parts[1]


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def path_from_status(line: str) -> str:
    return line[3:] if len(line) > 3 else line


def dirty_paths(repo: Path = GF_REPO_PATH) -> list[str]:
    status = git(["status", "--porcelain"], repo)
    return [] if status == "missing" or not status else status.splitlines()


def family_files() -> list[str]:
    family_dir = GF_REPO_PATH / FAMILY_PATH
    if not family_dir.exists():
        return []
    return sorted(path.relative_to(GF_REPO_PATH).as_posix() for path in family_dir.rglob("*") if path.is_file())


def first_blocker(blockers: list[str]) -> str:
    return blockers[0] if blockers else "none"


def display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def main() -> int:
    metadata = read(METADATA)
    handoff = read(HANDOFF)
    packager = read(PACKAGER_READINESS)
    packager_record = read(PACKAGER_RECORD)
    pr_draft = read(PR_DRAFT)
    gf_exists = (GF_REPO_PATH / ".git").exists()
    branch = git(["rev-parse", "--abbrev-ref", "HEAD"])
    tracking = git(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"])
    origin = git(["remote", "get-url", "origin"])
    upstream = git(["remote", "get-url", "upstream"])
    origin_ahead, origin_behind = git_ahead_behind("main", "origin/main")
    upstream_ahead, upstream_behind = git_ahead_behind("main", "upstream/main")
    dirty = dirty_paths()
    family_prefix = FAMILY_PATH.as_posix() + "/"
    dirty_inside = [line for line in dirty if path_from_status(line).startswith(family_prefix)]
    dirty_outside = [line for line in dirty if not path_from_status(line).startswith(family_prefix)]
    files = family_files()
    clean_exists = (GF_CLEAN_REPO_PATH / ".git").exists()
    clean_branch = git(["rev-parse", "--abbrev-ref", "HEAD"], GF_CLEAN_REPO_PATH)
    clean_dirty = dirty_paths(GF_CLEAN_REPO_PATH)
    clean_dirty_outside = [
        line for line in clean_dirty if not path_from_status(line).startswith(family_prefix)
    ]
    clean_origin_ahead, clean_origin_behind = git_ahead_behind("main", "origin/main", GF_CLEAN_REPO_PATH)
    clean_upstream_ahead, clean_upstream_behind = git_ahead_behind("main", "upstream/main", GF_CLEAN_REPO_PATH)
    clean_base_ready = (
        clean_exists
        and clean_branch == "main"
        and clean_origin_ahead == "0"
        and clean_origin_behind == "0"
        and clean_upstream_ahead == "0"
        and clean_upstream_behind == "0"
        and not clean_dirty_outside
    )

    issue_pending = "Google Fonts issue: pending" in handoff
    metadata_placeholders = "PENDING-YYYY-MM-DD" in metadata or "PENDING_FINAL_40_CHARACTER_COMMIT" in metadata
    packager_ready = "Ready to run final no-PR Packager dry run: yes" in packager
    packager_recorded = "Final no-PR Packager dry run recorded: yes" in packager_record
    fork_base_ready = (
        gf_exists
        and branch == "main"
        and tracking in {"origin/main", "missing"}
        and origin_ahead == "0"
        and origin_behind == "0"
        and upstream_ahead == "0"
        and upstream_behind == "0"
        and not dirty_outside
    )
    effective_base_ready = fork_base_ready or clean_base_ready
    effective_repo_path = GF_CLEAN_REPO_PATH if clean_base_ready else GF_REPO_PATH
    handoff_has_branch = EXPECTED_BRANCH in handoff
    handoff_has_title = EXPECTED_PR_TITLE in handoff
    pr_draft_ready = "Downstream PR draft ready: yes" in pr_draft
    pr_draft_has_title = EXPECTED_PR_TITLE in pr_draft
    pr_draft_has_body = "Taken from the upstream repo https://github.com/" in pr_draft and "<commit-url>" not in pr_draft
    handoff_has_body = EXPECTED_PR_BODY in handoff or pr_draft_has_body
    handoff_has_issue_first = "Google Fonts issue exists" in handoff or "Add Font issue" in handoff
    handoff_has_one_dir_rule = "one family directory" in handoff or "one-family-directory" in handoff

    blockers: list[str] = []
    if not gf_exists:
        blockers.append(f"local google/fonts checkout is missing: {GF_REPO_PATH}")
    if branch != "main":
        blockers.append(f"google/fonts checkout should be on main before final Packager branch: {branch}")
    if dirty_outside and not clean_base_ready:
        blockers.append("google/fonts checkout has dirty paths outside ofl/blocksync")
    if metadata_placeholders:
        blockers.append("downstream metadata still has final-value placeholders")
    if issue_pending:
        blockers.append("Google Fonts Add Font issue has not been recorded")
    if not packager_ready:
        blockers.append("guarded no-PR Packager dry run is not ready")
    if not packager_recorded:
        blockers.append("final no-PR Packager dry run has not been recorded")
    if not handoff_has_branch or not handoff_has_title or not handoff_has_body:
        blockers.append("submission handoff is missing expected downstream PR branch/title/body details")
    if not pr_draft_ready:
        blockers.append("downstream PR draft is not final")

    ready = not blockers
    lines = [
        "# Downstream PR Readiness",
        "",
        "This generated report records local evidence for the eventual downstream",
        "`google/fonts` pull request. It does not open an issue, create a branch,",
        "push commits, or write to the local `google/fonts` checkout.",
        "",
        "## Summary",
        "",
        f"- Ready to open downstream PR: {yes_no(ready)}",
        f"- First blocker: {first_blocker(blockers)}",
        f"- Expected downstream family path: `{FAMILY_PATH}`",
        f"- Expected Packager branch: `{EXPECTED_BRANCH}`",
        f"- Expected PR title: `{EXPECTED_PR_TITLE}`",
        f"- Expected PR body provenance line: `{EXPECTED_PR_BODY}`",
        f"- Downstream PR draft ready: {yes_no(pr_draft_ready)}",
        f"- Google Fonts issue pending: {yes_no(issue_pending)}",
        f"- Metadata has final-value placeholders: {yes_no(metadata_placeholders)}",
        f"- Guarded no-PR Packager dry run ready: {yes_no(packager_ready)}",
        f"- Final no-PR Packager dry run recorded: {yes_no(packager_recorded)}",
        f"- Local google/fonts checkout exists: {yes_no(gf_exists)}",
        f"- Current google/fonts branch: `{branch}`",
        f"- google/fonts tracking branch: `{tracking}`",
        f"- google/fonts origin: `{origin}`",
        f"- google/fonts upstream: `{upstream}`",
        f"- google/fonts main vs origin/main: {origin_ahead} ahead, {origin_behind} behind",
        f"- google/fonts main vs upstream/main: {upstream_ahead} ahead, {upstream_behind} behind",
        f"- google/fonts fork base ready for branch: {yes_no(fork_base_ready)}",
        f"- Effective clean fork base ready for branch: {yes_no(effective_base_ready)}",
        f"- Dirty google/fonts paths inside family dir: {len(dirty_inside)}",
        f"- Dirty google/fonts paths outside family dir: {len(dirty_outside)}",
        f"- Suggested clean GF_REPO_PATH: `{GF_CLEAN_REPO_PATH}`",
        f"- Suggested clean checkout exists: {yes_no(clean_exists)}",
        f"- Suggested clean checkout branch: `{clean_branch}`",
        f"- Suggested clean checkout base ready: {yes_no(clean_base_ready)}",
        f"- Suggested clean checkout dirty paths outside family dir: {len(clean_dirty_outside)}",
        f"- Current downstream family file count: {len(files)}",
        "",
        "## Blocking Items",
        "",
    ]
    lines.extend(f"- {blocker}" for blocker in blockers) if blockers else lines.append("- none")
    lines.extend(
        [
            "",
            "## Handoff Coverage",
            "",
            f"- Handoff names expected Packager branch: {yes_no(handoff_has_branch)}",
            f"- Handoff includes expected PR title: {yes_no(handoff_has_title)}",
            f"- Handoff includes expected PR provenance body line: {yes_no(handoff_has_body)}",
            f"- Downstream PR draft includes final title: {yes_no(pr_draft_has_title)}",
            f"- Downstream PR draft includes final provenance: {yes_no(pr_draft_has_body)}",
            f"- Handoff records issue-first rule: {yes_no(handoff_has_issue_first)}",
            f"- Handoff records one-family-directory rule: {yes_no(handoff_has_one_dir_rule)}",
            "",
            "## google/fonts Fork Evidence",
            "",
            "Dirty paths inside family dir:",
            "",
        ]
    )
    lines.extend(f"- `{line}`" for line in dirty_inside) if dirty_inside else lines.append("- None")
    lines.extend(["", "Dirty paths outside family dir:", ""])
    lines.extend(f"- `{line}`" for line in dirty_outside) if dirty_outside else lines.append("- None")
    lines.extend(["", "Clean checkout escape hatch:", ""])
    lines.append(
        "Use `make prepare-gf-clean-checkout` and rerun readiness with "
        f"`GF_REPO_PATH={GF_CLEAN_REPO_PATH}` when the shared checkout has unrelated dirty work."
    )
    if clean_dirty_outside:
        lines.extend(["", "Suggested clean checkout dirty paths outside family dir:", ""])
        lines.extend(f"- `{line}`" for line in clean_dirty_outside)
    lines.extend(["", "Current files inside downstream family dir:", ""])
    lines.extend(f"- `{path}`" for path in files) if files else lines.append("- None")
    lines.extend(
        [
            "",
            "## Safe Local Sequence",
            "",
            "Use this only after final metadata, final proof review, issue creation,",
            "and no-PR Packager review are complete:",
            "",
            "```bash",
            "make release-check",
            f"GF_REPO_PATH={effective_repo_path} make package-dry-run-readiness",
            f"GF_REPO_PATH={effective_repo_path} make package-dry-run",
            f"git -C {effective_repo_path} checkout -b {EXPECTED_BRANCH}",
            "```",
            "",
            "Only after reviewing the no-PR package and recording the Google Fonts",
            "issue number should any final Packager run use PR-opening flags.",
            "",
        ]
    )

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {display_path(OUTPUT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
