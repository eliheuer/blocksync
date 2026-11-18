#!/usr/bin/env python3
"""Record and report final no-PR Google Fonts Packager dry-run evidence."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
METADATA = Path(os.environ.get("METADATA_DRAFT_PATH", ROOT / "documentation" / "google-fonts-downstream-metadata-draft.md"))
RECORD = Path(os.environ.get("PACKAGER_DRY_RUN_RECORD_PATH", ROOT / "documentation" / "google-fonts-packager-dry-run-record.json"))
OUTPUT = Path(os.environ.get("PACKAGER_DRY_RUN_RECORD_OUTPUT", ROOT / "documentation" / "packager-dry-run-record.md"))
GF_REPO_PATH = Path(os.environ.get("GF_REPO_PATH", "/Users/eli/GH/forks/fonts"))
PACKAGE_DIR = Path("ofl/blocksync")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record-success", action="store_true")
    parser.add_argument("--strict", action="store_true", help="exit nonzero when the report is not final-ready")
    parser.add_argument("--gf-repo-path", type=Path, default=GF_REPO_PATH)
    parser.add_argument("--metadata", type=Path, default=METADATA)
    parser.add_argument("--record-path", type=Path, default=RECORD)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    return parser.parse_args()


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


def git(args: list[str], repo: Path) -> str:
    if not (repo / ".git").exists():
        return "missing"
    _code, output = run(["git", "-C", str(repo), *args])
    return output or "missing"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def extract_textproto(metadata_path: Path) -> str:
    text = read(metadata_path)
    match = re.search(r"```textproto\n(.*?)\n```", text, flags=re.DOTALL)
    if not match:
        raise ValueError("metadata draft must contain a textproto fenced block")
    return match.group(1).strip() + "\n"


def scalar(proto: str, key: str) -> str:
    match = re.search(rf'^\s*{re.escape(key)}:\s+"([^"]*)"', proto, flags=re.MULTILINE)
    return match.group(1) if match else ""


def source_block(proto: str) -> str:
    match = re.search(r"^source\s+\{\n(.*?)^\}", proto, flags=re.MULTILINE | re.DOTALL)
    return match.group(1) if match else ""


def metadata_facts(metadata_path: Path) -> dict[str, str]:
    proto = extract_textproto(metadata_path)
    source = source_block(proto)
    return {
        "sha256": hashlib.sha256(proto.encode("utf-8")).hexdigest(),
        "date_added": scalar(proto, "date_added"),
        "source_commit": scalar(source, "commit"),
        "repository_url": scalar(source, "repository_url"),
        "branch": scalar(source, "branch"),
    }


def path_from_status(line: str) -> str:
    return line[3:] if len(line) > 3 else line


def dirty_paths(repo: Path) -> list[str]:
    status = git(["status", "--porcelain"], repo)
    return [] if status == "missing" or not status else status.splitlines()


def package_files(repo: Path) -> list[str]:
    family_dir = repo / PACKAGE_DIR
    if not family_dir.exists():
        return []
    return sorted(path.relative_to(repo).as_posix() for path in family_dir.rglob("*") if path.is_file())


def record_success(gf_repo_path: Path, metadata_path: Path, record_path: Path) -> None:
    facts = metadata_facts(metadata_path)
    dirty = dirty_paths(gf_repo_path)
    family_prefix = PACKAGE_DIR.as_posix() + "/"
    payload = {
        "schema_version": 1,
        "family": "Blocksync",
        "mode": "no-pr",
        "status": "success",
        "recorded_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "gf_repo_path": str(gf_repo_path),
        "gf_repo_branch": git(["rev-parse", "--abbrev-ref", "HEAD"], gf_repo_path),
        "gf_repo_head": git(["rev-parse", "HEAD"], gf_repo_path),
        "package_dir": PACKAGE_DIR.as_posix(),
        "metadata_sha256": facts["sha256"],
        "metadata_date_added": facts["date_added"],
        "metadata_source_commit": facts["source_commit"],
        "metadata_repository_url": facts["repository_url"],
        "metadata_branch": facts["branch"],
        "package_files": package_files(gf_repo_path),
        "dirty_paths_inside_package": [
            line for line in dirty if path_from_status(line).startswith(family_prefix)
        ],
        "dirty_paths_outside_package": [
            line for line in dirty if not path_from_status(line).startswith(family_prefix)
        ],
    }
    record_path.parent.mkdir(parents=True, exist_ok=True)
    record_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_record(record_path: Path) -> dict[str, Any]:
    if not record_path.exists():
        return {}
    data = json.loads(record_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Packager dry-run record must be a JSON object")
    return data


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def report(record_path: Path, output_path: Path, metadata_path: Path) -> bool:
    record = load_record(record_path)
    facts = metadata_facts(metadata_path)
    blockers: list[str] = []

    if not record:
        blockers.append(f"no Packager dry-run record exists: {record_path}")
    if record.get("family") != "Blocksync":
        blockers.append("record family is not Blocksync")
    if record.get("mode") != "no-pr":
        blockers.append("record is not for a no-PR Packager run")
    if record.get("status") != "success":
        blockers.append("record status is not success")
    if record.get("package_dir") != PACKAGE_DIR.as_posix():
        blockers.append(f"record package_dir is not {PACKAGE_DIR}")
    if record.get("metadata_sha256") != facts["sha256"]:
        blockers.append("record metadata hash does not match current metadata draft")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(record.get("metadata_date_added", ""))):
        blockers.append("record metadata date_added is not final-looking")
    if not re.fullmatch(r"[0-9a-f]{40}", str(record.get("metadata_source_commit", ""))):
        blockers.append("record metadata source commit is not a 40-character hash")
    if record.get("dirty_paths_outside_package"):
        blockers.append("record includes dirty paths outside ofl/blocksync")
    if not record.get("package_files"):
        blockers.append("record has no package files")

    ready = not blockers
    lines = [
        "# Packager Dry-Run Record",
        "",
        "This generated report verifies the recorded final no-PR Google Fonts",
        "Packager dry run against the current downstream metadata draft.",
        "",
        "## Summary",
        "",
        f"- Final no-PR Packager dry run recorded: {yes_no(ready)}",
        f"- Record path: `{display_path(record_path)}`",
        f"- Recorded at UTC: `{record.get('recorded_at_utc', 'missing')}`",
        f"- Recorded GF_REPO_PATH: `{record.get('gf_repo_path', 'missing')}`",
        f"- Recorded google/fonts branch: `{record.get('gf_repo_branch', 'missing')}`",
        f"- Recorded google/fonts HEAD: `{record.get('gf_repo_head', 'missing')}`",
        f"- Recorded package dir: `{record.get('package_dir', 'missing')}`",
        f"- Current metadata hash matches record: {yes_no(record.get('metadata_sha256') == facts['sha256'])}",
        f"- Recorded package file count: {len(record.get('package_files', [])) if isinstance(record.get('package_files'), list) else 0}",
        f"- Dirty paths outside package in record: {len(record.get('dirty_paths_outside_package', [])) if isinstance(record.get('dirty_paths_outside_package'), list) else 'unknown'}",
        f"- First blocker: {blockers[0] if blockers else 'none'}",
        "",
        "## Blocking Items",
        "",
    ]
    lines.extend(f"- {blocker}" for blocker in blockers) if blockers else lines.append("- none")
    lines.extend(["", "## Recorded Package Files", ""])
    package_file_rows = record.get("package_files", [])
    if isinstance(package_file_rows, list) and package_file_rows:
        lines.extend(f"- `{path}`" for path in package_file_rows)
    else:
        lines.append("- none")
    lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {display_path(output_path)}")
    return ready


def main() -> int:
    args = parse_args()
    try:
        if args.record_success:
            record_success(args.gf_repo_path, args.metadata, args.record_path)
            print(f"Wrote {display_path(args.record_path)}")
        ready = report(args.record_path, args.output, args.metadata)
    except Exception as error:
        print(f"Packager dry-run record failed: {error}", file=sys.stderr)
        return 2
    if args.strict and not ready:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
