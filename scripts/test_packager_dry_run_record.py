#!/usr/bin/env python3
"""Regression tests for Packager dry-run record reporting."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "report_packager_dry_run_record.py"


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def write_metadata_fixture(path: Path) -> None:
    path.write_text("""```textproto
name: "Blocksync"
designer: "Fixture Designer"
date_added: "2026-05-30"
copyright: "Copyright 2023 The Blocksyncer Project Authors (https://github.com/example/blocksync)"
source {
  repository_url: "https://github.com/example/blocksync"
  branch: "main"
  commit: "0123456789abcdef0123456789abcdef01234567"
  config_yaml: "sources/config.yaml"
  files {
    source_file: "fonts/variable/Blocksync[wdth,wght].ttf"
    dest_file: "Blocksync[wdth,wght].ttf"
  }
}
```
""", encoding="utf-8")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="blocksync-packager-record.") as tmp:
        work = Path(tmp)
        metadata = work / "metadata.md"
        write_metadata_fixture(metadata)
        record = work / "record.json"
        report = work / "record.md"

        gf_repo = work / "fonts"
        subprocess.run(["git", "init", "-q", "-b", "main", str(gf_repo)], check=True)
        subprocess.run(["git", "-C", str(gf_repo), "remote", "add", "origin", "git@github.com:eliheuer/fonts.git"], check=True)
        package_dir = gf_repo / "ofl" / "blocksync"
        package_dir.mkdir(parents=True)
        (package_dir / "METADATA.pb").write_text("name: \"Blocksync\"\n", encoding="utf-8")
        (package_dir / "Blocksync[wdth,wght].ttf").write_text("fake font\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(gf_repo), "add", "ofl/blocksync/METADATA.pb"], check=True)
        subprocess.run(
            [
                "git",
                "-C",
                str(gf_repo),
                "-c",
                "user.name=Blocksync Test",
                "-c",
                "user.email=blocksync-test@example.com",
                "commit",
                "-q",
                "-m",
                "initial",
            ],
            check=True,
        )

        created = run([
            sys.executable,
            str(SCRIPT),
            "--record-success",
            "--gf-repo-path",
            str(gf_repo),
            "--metadata",
            str(metadata),
            "--record-path",
            str(record),
            "--output",
            str(report),
        ])
        if created.returncode != 0:
            print(created.stdout)
            return created.returncode

        report_text = report.read_text(encoding="utf-8")
        if "Final no-PR Packager dry run recorded: yes" not in report_text:
            print(report_text)
            return 1

        changed_metadata = work / "metadata-changed.md"
        changed_metadata.write_text(
            metadata.read_text(encoding="utf-8").replace(
                "0123456789abcdef0123456789abcdef01234567",
                "1111111111111111111111111111111111111111",
            ),
            encoding="utf-8",
        )
        stale_report = work / "record-stale.md"
        stale = run([
            sys.executable,
            str(SCRIPT),
            "--metadata",
            str(changed_metadata),
            "--record-path",
            str(record),
            "--output",
            str(stale_report),
        ])
        if stale.returncode != 0:
            print(stale.stdout)
            return stale.returncode
        stale_text = stale_report.read_text(encoding="utf-8")
        if "Final no-PR Packager dry run recorded: no" not in stale_text:
            print(stale_text)
            return 1
        strict_stale = run([
            sys.executable,
            str(SCRIPT),
            "--strict",
            "--metadata",
            str(changed_metadata),
            "--record-path",
            str(record),
            "--output",
            str(work / "record-stale-strict.md"),
        ])
        if strict_stale.returncode == 0:
            print("Expected --strict stale report to fail")
            print(strict_stale.stdout)
            return 1

    print("Packager dry-run record tests passed.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--write-fixture":
        write_metadata_fixture(Path(sys.argv[2]))
    else:
        raise SystemExit(main())
