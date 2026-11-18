#!/usr/bin/env python3
"""Regression tests for downstream PR draft generation."""

from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "report_downstream_pr_draft.py"


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def final_metadata(path: Path) -> None:
    text = (ROOT / "documentation" / "google-fonts-downstream-metadata-draft.md").read_text(encoding="utf-8")
    text = text.replace('date_added: "PENDING-YYYY-MM-DD"', 'date_added: "2026-05-30"')
    text = text.replace(
        'commit: "PENDING_FINAL_40_CHARACTER_COMMIT"',
        'commit: "0123456789abcdef0123456789abcdef01234567"',
    )
    path.write_text(text, encoding="utf-8")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="blocksync-pr-draft.") as tmp:
        work = Path(tmp)
        metadata = work / "metadata.md"
        handoff = work / "handoff.md"
        output = work / "pr-draft.md"
        final_metadata(metadata)
        shutil.copyfile(ROOT / "documentation" / "google-fonts-submission-handoff.md", handoff)
        handoff.write_text(
            handoff.read_text(encoding="utf-8").replace(
                "- Google Fonts issue: pending",
                "- Google Fonts issue exists: https://github.com/google/fonts/issues/1234",
            ),
            encoding="utf-8",
        )

        result = run([
            "env",
            f"DOWNSTREAM_METADATA_PATH={metadata}",
            f"SUBMISSION_HANDOFF_PATH={handoff}",
            f"DOWNSTREAM_PR_DRAFT_OUTPUT={output}",
            sys.executable,
            str(SCRIPT),
        ])
        if result.returncode != 0:
            print(result.stdout)
            return result.returncode
        text = output.read_text(encoding="utf-8")
        checks = {
            "ready": "Downstream PR draft ready: yes" in text,
            "title": "Blocksync : 1.000 added" in text,
            "provenance": "https://github.com/eliheuer/blocksyncer/commit/0123456789abcdef0123456789abcdef01234567" in text,
            "issue": "https://github.com/google/fonts/issues/1234" in text,
        }
        failed = [name for name, ok in checks.items() if not ok]
        if failed:
            print("Failed checks:")
            for name in failed:
                print(f"- {name}")
            print(text)
            return 1

    print("Downstream PR draft tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
