#!/usr/bin/env python3
"""Report readiness for a guarded no-PR Google Fonts Packager dry run."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path(
    os.environ.get(
        "PACKAGE_DRY_RUN_READINESS_OUTPUT",
        ROOT / "documentation" / "package-dry-run-readiness.md",
    )
)
GF_REPO_PATH = Path(os.environ.get("GF_REPO_PATH", "/Users/eli/GH/forks/fonts"))
GF_CLEAN_REPO_PATH = Path(os.environ.get("GF_CLEAN_REPO_PATH", "/private/tmp/blocksync-google-fonts"))
PACKAGE_DIR = Path("ofl/blocksync")
METADATA = Path(
    os.environ.get(
        "PACKAGE_METADATA_PATH",
        ROOT / "documentation" / "google-fonts-downstream-metadata-draft.md",
    )
)
ARCHIVE = Path(
    os.environ.get(
        "RELEASE_ARCHIVE_MANIFEST_PATH",
        ROOT / "documentation" / "release-archive-manifest.md",
    )
)
BUILT_VARIABLE_FONT = Path(
    os.environ.get(
        "BUILT_VARIABLE_FONT_PATH",
        ROOT / "fonts" / "variable" / "Blocksync[wdth,wght].ttf",
    )
)


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


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def metadata_text() -> str:
    return METADATA.read_text(encoding="utf-8") if METADATA.exists() else ""


def first_blocker(blockers: list[str]) -> str:
    return blockers[0] if blockers else "none"


def display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def dirty_paths(repo: Path = GF_REPO_PATH) -> list[str]:
    status = git(["status", "--porcelain"], repo)
    return [] if status == "missing" or not status else status.splitlines()


def path_from_status(line: str) -> str:
    return line[3:] if len(line) > 3 else line


def main() -> int:
    text = metadata_text()
    blockers: list[str] = []

    gf_exists = (GF_REPO_PATH / ".git").exists()
    branch = git(["rev-parse", "--abbrev-ref", "HEAD"])
    origin = git(["remote", "get-url", "origin"])
    upstream = git(["remote", "get-url", "upstream"])
    dirty = dirty_paths()
    dirty_outside = [
        line for line in dirty if not path_from_status(line).startswith(PACKAGE_DIR.as_posix() + "/")
    ]
    family_dir = GF_REPO_PATH / PACKAGE_DIR
    clean_exists = (GF_CLEAN_REPO_PATH / ".git").exists()
    clean_branch = git(["rev-parse", "--abbrev-ref", "HEAD"], GF_CLEAN_REPO_PATH)
    clean_dirty = dirty_paths(GF_CLEAN_REPO_PATH)
    clean_dirty_outside = [
        line
        for line in clean_dirty
        if not path_from_status(line).startswith(PACKAGE_DIR.as_posix() + "/")
    ]
    clean_can_avoid_shared_dirty = clean_exists and clean_branch == "main" and not clean_dirty_outside

    if not gf_exists:
        blockers.append(f"local google/fonts checkout is missing: {GF_REPO_PATH}")
    if branch != "main":
        blockers.append(f"google/fonts checkout is not on main: {branch}")
    if "google/fonts" not in f"{origin} {upstream}":
        blockers.append("google/fonts checkout does not have a google/fonts origin/upstream remote")
    if dirty_outside and not clean_can_avoid_shared_dirty:
        blockers.append("google/fonts checkout has dirty paths outside ofl/blocksync")
    if "PENDING-YYYY-MM-DD" in text:
        blockers.append("metadata date_added is still a placeholder")
    if "PENDING_FINAL_40_CHARACTER_COMMIT" in text:
        blockers.append("metadata source.commit is still a placeholder")
    if (
        'source_file: "fonts/variable/Blocksync[wdth,wght].ttf"' in text
        and not BUILT_VARIABLE_FONT.is_file()
    ):
        blockers.append("built variable font is missing; run make build")
    if "Local release archive hashes match source files: yes" not in (
        ARCHIVE.read_text(encoding="utf-8") if ARCHIVE.exists() else ""
    ):
        blockers.append("fallback release archive manifest does not match current sources")

    ready = not blockers
    lines = [
        "# Package Dry-Run Readiness",
        "",
        "This report checks whether a no-PR Google Fonts Packager dry run can be",
        "started safely. It does not write to the local `google/fonts` checkout.",
        "",
        "## Summary",
        "",
        f"- GF_REPO_PATH: `{GF_REPO_PATH}`",
        f"- Local google/fonts checkout exists: {yes_no(gf_exists)}",
        f"- Current google/fonts branch: `{branch}`",
        f"- google/fonts origin: `{origin}`",
        f"- google/fonts upstream: `{upstream}`",
        f"- Expected package path: `{PACKAGE_DIR}`",
        f"- Downstream family directory exists locally: {yes_no(family_dir.exists())}",
        f"- Dirty google/fonts paths outside package: {len(dirty_outside)}",
        f"- Suggested clean GF_REPO_PATH: `{GF_CLEAN_REPO_PATH}`",
        f"- Suggested clean checkout exists: {yes_no(clean_exists)}",
        f"- Suggested clean checkout branch: `{clean_branch}`",
        f"- Suggested clean checkout dirty paths outside package: {len(clean_dirty_outside)}",
        f"- Clean checkout avoids shared dirty paths: {yes_no(clean_can_avoid_shared_dirty)}",
        f"- Effective checkout path for final dry run: `{GF_CLEAN_REPO_PATH if clean_can_avoid_shared_dirty else GF_REPO_PATH}`",
        f"- Ready to run final no-PR Packager dry run: {yes_no(ready)}",
        f"- First blocker: {first_blocker(blockers)}",
        "",
        "## Blocking Items",
        "",
    ]
    lines.extend(f"- {blocker}" for blocker in blockers) if blockers else lines.append("- none")
    if dirty_outside:
        lines.extend(
            [
                "",
                "## Dirty google/fonts Paths Outside Package",
                "",
            ]
        )
        lines.extend(f"- `{line}`" for line in dirty_outside)
    lines.extend(
        [
            "",
            "## Clean Checkout Escape Hatch",
            "",
        ]
    )
    if clean_can_avoid_shared_dirty:
        lines.append(
            "The suggested clean checkout is ready for Blocksync-only package dry-run checks."
        )
    else:
        lines.append(
            "Use this when the shared `google/fonts` checkout has unrelated dirty work."
        )
    lines.extend(
        [
            "",
            "```bash",
            "make prepare-gf-clean-checkout",
            f"GF_REPO_PATH=\"{GF_CLEAN_REPO_PATH}\" make package-dry-run-readiness",
            f"GF_REPO_PATH=\"{GF_CLEAN_REPO_PATH}\" make package-dry-run",
            "```",
            "",
        ]
    )
    if clean_dirty_outside:
        lines.extend(["Suggested clean checkout dirty paths outside package:", ""])
        lines.extend(f"- `{line}`" for line in clean_dirty_outside)
        lines.append("")
    lines.extend(
        [
            "",
            "## Command",
            "",
            "After final metadata values and maintainer decisions are applied, run:",
            "",
            "```bash",
            "make package-dry-run",
            "```",
            "",
            "The wrapper is intentionally guarded and refuses to run while metadata",
            "placeholders remain.",
            "",
        ]
    )

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {display_path(OUTPUT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
