#!/usr/bin/env python3
"""Regression tests for downstream PR draft generation."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile

from test_packager_dry_run_record import write_metadata_fixture


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "report_downstream_pr_draft.py"


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="blocksync-pr-draft.") as tmp:
        work = Path(tmp)
        metadata = work / "metadata.md"
        write_metadata_fixture(metadata)
        handoff = work / "handoff.md"
        output = work / "pr-draft.md"
        handoff.write_text("- Google Fonts issue exists: https://github.com/google/fonts/issues/1234\n", encoding="utf-8")

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
            "provenance": "https://github.com/example/blocksync/commit/0123456789abcdef0123456789abcdef01234567" in text,
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
