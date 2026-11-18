#!/usr/bin/env python3
"""Regression tests for Packager dry-run record reporting."""

from __future__ import annotations

from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "report_packager_dry_run_record.py"


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def final_metadata_copy(path: Path) -> None:
    text = (ROOT / "documentation" / "google-fonts-downstream-metadata-draft.md").read_text(encoding="utf-8")
    text = text.replace('date_added: "PENDING-YYYY-MM-DD"', 'date_added: "2026-05-30"')
    text = text.replace(
        'commit: "PENDING_FINAL_40_CHARACTER_COMMIT"',
        'commit: "0123456789abcdef0123456789abcdef01234567"',
    )
    path.write_text(text, encoding="utf-8")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="blocksync-packager-record.") as tmp:
        work = Path(tmp)
        metadata = work / "metadata.md"
        record = work / "record.json"
        report = work / "record.md"
        final_metadata_copy(metadata)

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
        shutil.copyfile(metadata, changed_metadata)
        changed_metadata.write_text(
            re.sub(
                r'commit: "[0-9a-f]{40}"',
                'commit: "1111111111111111111111111111111111111111"',
                changed_metadata.read_text(encoding="utf-8"),
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
    raise SystemExit(main())
