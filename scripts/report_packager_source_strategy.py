#!/usr/bin/env python3
"""Generate a Google Fonts package source-strategy readiness report."""

from __future__ import annotations

from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "documentation" / "packager-source-strategy.md"
METADATA = ROOT / "documentation" / "google-fonts-downstream-metadata-draft.md"
PACKAGE_PREVIEW = ROOT / "documentation" / "google-fonts-downstream-package-preview.md"
SOURCE_READINESS = ROOT / "documentation" / "source-readiness.md"
ARCHIVE_MANIFEST = ROOT / "documentation" / "release-archive-manifest.md"
DECISIONS = ROOT / "documentation" / "google-fonts-final-decision-sheet.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def metadata_proto(text: str) -> str:
    match = re.search(r"```textproto\n(?P<body>.*?)\n```", text, flags=re.DOTALL)
    return match.group("body") if match else text


def scalar(proto: str, name: str) -> str:
    match = re.search(rf'^\s*{re.escape(name)}:\s*"([^"]*)"', proto, flags=re.MULTILINE)
    return match.group(1) if match else ""


def source_files(proto: str) -> list[tuple[str, str]]:
    return re.findall(
        r'files\s*\{\s*source_file:\s*"([^"]+)"\s*dest_file:\s*"([^"]+)"\s*\}',
        proto,
        flags=re.DOTALL,
    )


def row_final_answer(decision_name: str, decisions: str) -> str:
    for line in decisions.splitlines():
        if not line.startswith(f"| {decision_name} |"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        return cells[2] if len(cells) >= 3 else "unknown"
    return "unknown"


def git_status(path: Path) -> tuple[bool, bool]:
    rel = str(path.relative_to(ROOT))
    tracked = subprocess.run(
        ["git", "ls-files", "--error-unmatch", "--", rel],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    ).returncode == 0
    ignored = subprocess.run(
        ["git", "check-ignore", "-q", "--", rel],
        cwd=ROOT,
        check=False,
    ).returncode == 0
    return tracked, ignored


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def main() -> int:
    metadata_text = read(METADATA)
    proto = metadata_proto(metadata_text)
    preview = read(PACKAGE_PREVIEW)
    source_readiness = read(SOURCE_READINESS)
    archive = read(ARCHIVE_MANIFEST)
    decisions = read(DECISIONS)
    config_yaml = scalar(proto, "config_yaml")
    repository_url = scalar(proto, "repository_url")
    commit = scalar(proto, "commit")
    branch = scalar(proto, "branch")
    archive_url = scalar(proto, "archive_url")
    files = source_files(proto)
    strategy_answer = row_final_answer("Package source strategy", decisions)
    config_yaml_ready = (
        config_yaml == "sources/config.yaml"
        and "Source-ready for Google Fonts build path: yes" in source_readiness
        and "Preferred first-submission strategy" in preview
    )
    archive_ready = all(
        phrase in archive
        for phrase in [
            "Local release archive exists: yes",
            "Local release archive contains expected files: yes",
            "Local release archive hashes match source files: yes",
            "Local release archive metadata deterministic: yes",
        ]
    )
    final_strategy_recorded = strategy_answer not in {
        "Confirm or switch to release/archive",
        "unknown",
    }
    local_ready = config_yaml_ready and archive_ready and bool(files)
    final_commit = bool(re.fullmatch(r"[0-9a-f]{40}", commit))
    final_ready = local_ready and final_strategy_recorded and final_commit

    lines = [
        "# Packager Source Strategy",
        "",
        "This generated report checks the preferred build-from-source path and",
        "the release/archive fallback so agents do not mix the two packaging",
        "strategies during Google Fonts handoff.",
        "",
        "## Summary",
        "",
        f"- Preferred build-from-source path ready locally: {yes_no(config_yaml_ready)}",
        f"- Release/archive fallback ready locally: {yes_no(archive_ready)}",
        f"- Package source strategy local evidence ready: {yes_no(local_ready)}",
        f"- Package source strategy final-ready for submission: {yes_no(final_ready)}",
        f"- Final strategy decision recorded: {yes_no(final_strategy_recorded)}",
        f"- Metadata repository_url: `{repository_url or 'missing'}`",
        f"- Metadata branch: `{branch or 'missing'}`",
        f"- Metadata commit final-looking: {yes_no(final_commit)}",
        f"- Metadata config_yaml: `{config_yaml or 'missing'}`",
        f"- Metadata archive_url: `{archive_url or 'not set'}`",
        f"- Source files mapped: {len(files)}",
        "",
        "## Source Files",
        "",
        "| Source file | Destination | Exists | Tracked | Ignored |",
        "| --- | --- | --- | --- | --- |",
    ]
    for source, dest in files:
        path = ROOT / source
        tracked, ignored = git_status(path) if path.exists() else (False, False)
        lines.append(
            f"| `{source}` | `{dest}` | {yes_no(path.exists())} | {yes_no(tracked)} | {yes_no(ignored)} |"
        )

    lines.extend(
        [
            "",
            "## Preferred Strategy",
            "",
            "- Keep `source.config_yaml: \"sources/config.yaml\"` for the first",
            "  submission while Google Fonts accepts the reproducible",
            "  designspace/UFO build path.",
            "- Historical `.glyphs` files stay archived in `sources/archive/` and",
            "  are not package inputs.",
            "",
            "## Fallback Strategy",
            "",
            "- Use release/archive packaging only if Google Fonts rejects the",
            "  `source.config_yaml` path or explicitly asks for prebuilt files.",
            "- If fallback is selected, publish an archive equivalent to",
            "  `dist/Blocksync-GF-review.zip`, add final `source.archive_url`,",
            "  and rerun `make release-check`.",
            "",
            "## Finalization",
            "",
            f"- Current final decision sheet answer: {strategy_answer}",
            "- Replace final `source.commit` before any Packager dry run.",
            "- Confirm package strategy before opening the Add Font issue.",
            "",
        ]
    )

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
