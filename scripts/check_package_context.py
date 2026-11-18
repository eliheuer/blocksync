#!/usr/bin/env python3
"""Run a local Fontspector probe in a downstream-like package context."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "documentation" / "google-fonts-downstream-metadata-draft.md"
FONT = ROOT / "fonts" / "variable" / "Blocksync[wdth,wght].ttf"
PACKAGE_FILES = {
    ROOT / "OFL.txt": "OFL.txt",
    ROOT / "documentation" / "DESCRIPTION.en_us.html": "DESCRIPTION.en_us.html",
    FONT: "Blocksync[wdth,wght].ttf",
}


def metadata_text() -> str:
    text = DRAFT.read_text(encoding="utf-8")
    match = re.search(r"```textproto\n(.*?)\n```", text, flags=re.S)
    if not match:
        raise ValueError("metadata draft must contain a textproto fenced block")
    return (
        match.group(1)
        .replace("PENDING-YYYY-MM-DD", "2026-05-30")
        .replace("PENDING_FINAL_40_CHARACTER_COMMIT", "0000000000000000000000000000000000000000")
    )


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--keep-temp", action="store_true")
    args = parser.parse_args(argv)

    missing = [str(path.relative_to(ROOT)) for path in PACKAGE_FILES if not path.exists()]
    if missing:
        print(f"FAIL: missing package files: {', '.join(missing)}")
        return 1

    tempdir = Path(tempfile.mkdtemp(prefix="blocksync-package-context-"))
    package_dir = tempdir / "ofl" / "blocksync"
    package_dir.mkdir(parents=True)
    for source, dest_name in PACKAGE_FILES.items():
        shutil.copy2(source, package_dir / dest_name)
    (package_dir / "METADATA.pb").write_text(metadata_text() + "\n", encoding="utf-8")

    report_dir = ROOT / "out" / "fontspector"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_md = report_dir / "fontspector-package-context-report.md"
    report_html = report_dir / "fontspector-package-context-report.html"

    command = [
        "fontspector",
        "-p",
        "googlefonts",
        str(package_dir / "METADATA.pb"),
        str(package_dir / "Blocksync[wdth,wght].ttf"),
        str(package_dir / "OFL.txt"),
        str(package_dir / "DESCRIPTION.en_us.html"),
        "--exclude-checkid",
        "googlefonts/repo/dirname_matches_nameid_1",
        "--exclude-checkid",
        "googlefonts/axes_match",
        "--exclude-checkid",
        "googlefonts/metadata/consistent_repo_urls",
        "--succinct",
        "--loglevel",
        "warn",
        "--skip-network",
        "--full-lists",
        "--ghmarkdown",
        str(report_md),
        "--html",
        str(report_html),
    ]
    result = subprocess.run(command, cwd=ROOT, check=False)
    if args.keep_temp:
        print(f"Package-context temp dir: {package_dir}")
    else:
        shutil.rmtree(tempdir)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
