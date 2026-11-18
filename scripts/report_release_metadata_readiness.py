#!/usr/bin/env python3
"""Generate release metadata readiness for Blocksync Google Fonts handoff."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import plistlib
import re
import subprocess

from fontTools.ttLib import TTFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "documentation" / "release-metadata-readiness.md"
METADATA = ROOT / "documentation" / "google-fonts-downstream-metadata-draft.md"
VARIABLE_FONT = ROOT / "fonts" / "variable" / "Blocksync[wdth,wght].ttf"


@dataclass(frozen=True)
class SourceVersion:
    path: Path
    major: int | None
    minor: int | None


@dataclass(frozen=True)
class BuiltVersion:
    path: Path
    name_id_5: str


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def metadata_proto(text: str) -> str:
    match = re.search(r"```textproto\n(?P<body>.*?)\n```", text, flags=re.DOTALL)
    return match.group("body") if match else text


def scalar(proto: str, name: str) -> str:
    match = re.search(rf'^\s*{re.escape(name)}:\s*"([^"]*)"', proto, flags=re.MULTILINE)
    return match.group(1) if match else ""


def source_version(path: Path) -> SourceVersion:
    with path.open("rb") as file:
        info = plistlib.load(file)
    return SourceVersion(path=path.relative_to(ROOT), major=info.get("versionMajor"), minor=info.get("versionMinor"))


def version_string(version: SourceVersion) -> str:
    if version.major is None or version.minor is None:
        return "missing"
    return f"{version.major}.{version.minor:03d}"


def built_version(path: Path) -> BuiltVersion:
    font = TTFont(path)
    try:
        name = font["name"].getName(5, 3, 1, 0x409)
        value = name.toUnicode() if name else ""
    finally:
        font.close()
    return BuiltVersion(path=path.relative_to(ROOT), name_id_5=value)


def git_output(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.stdout.strip()


def git_dirty_summary() -> tuple[int, int, int]:
    lines = [line for line in git_output(["status", "--short"]).splitlines() if line]
    modified = sum(1 for line in lines if not line.startswith("??"))
    untracked = sum(1 for line in lines if line.startswith("??"))
    return len(lines), modified, untracked


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def main() -> int:
    proto = metadata_proto(read(METADATA))
    date_added = scalar(proto, "date_added")
    commit = scalar(proto, "commit")
    branch = scalar(proto, "branch")
    repository_url = scalar(proto, "repository_url")
    head = git_output(["rev-parse", "HEAD"])
    dirty_total, dirty_modified, dirty_untracked = git_dirty_summary()
    source_versions = sorted(
        (source_version(path) for path in (ROOT / "sources").glob("Blocksync*.ufo/fontinfo.plist")),
        key=lambda item: str(item.path),
    )
    source_version_values = {version_string(version) for version in source_versions}
    source_version_value = source_version_values.pop() if len(source_version_values) == 1 else "mixed"
    built_versions = [built_version(VARIABLE_FONT)] if VARIABLE_FONT.exists() else []
    expected_name_id_5 = f"Version {source_version_value}" if source_version_value not in {"missing", "mixed"} else ""
    built_versions_match = all(
        version.name_id_5.startswith(expected_name_id_5) for version in built_versions
    ) if expected_name_id_5 and built_versions else False
    date_final = bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_added))
    commit_final = bool(re.fullmatch(r"[0-9a-f]{40}", commit))
    local_ready = (
        METADATA.exists()
        and bool(head)
        and bool(source_versions)
        and source_version_value not in {"missing", "mixed"}
        and built_versions_match
        and bool(repository_url)
        and bool(branch)
    )
    inputs = ["sources/*.ufo/**", "sources/*.designspace", "sources/config.yaml", "sources/build_interpolation.py", "requirements.txt", "requirements.in", "build.sh", "Makefile",
              "scripts/fix_gf_metadata.py", "OFL.txt", "documentation/DESCRIPTION.en_us.html"]
    matches_package_inputs = commit_final and all(
        subprocess.run(["git", *args], cwd=ROOT, capture_output=True).returncode == 0
        for args in (["merge-base", "--is-ancestor", commit, "HEAD"],
                     ["diff", "--quiet", commit, "--", *inputs])
    ) and not git_output(["ls-files", "--others", "--exclude-standard", "--", *inputs])
    final_ready = local_ready and date_final and matches_package_inputs

    lines = [
        "# Release Metadata Readiness",
        "",
        "The candidate revision identifies the reviewed font and package inputs. Later handoff documentation can refer to that revision.",
        "",
        "## Summary",
        "",
        f"- Release metadata local evidence ready: {yes_no(local_ready)}",
        f"- Release metadata final-ready for submission: {yes_no(final_ready)}",
        f"- Current git HEAD: `{head or 'unknown'}`",
        f"- Working tree clean: {yes_no(dirty_total == 0)}",
        f"- Dirty paths total: {dirty_total}",
        f"- Dirty modified paths: {dirty_modified}",
        f"- Dirty untracked paths: {dirty_untracked}",
        f"- Metadata repository_url: `{repository_url or 'missing'}`",
        f"- Metadata branch: `{branch or 'missing'}`",
        f"- Metadata date_added final-looking: {yes_no(date_final)}",
        f"- Metadata source.commit final-looking: {yes_no(commit_final)}",
        f"- Packaged revision matches current build and package inputs: {yes_no(matches_package_inputs)}",
        f"- Metadata source.commit equals current HEAD: {yes_no(commit == head and bool(head))}",
        f"- Source UFO version: `{source_version_value}`",
        f"- Built variable font matches source version: {yes_no(built_versions_match)}",
        "",
        "## Source UFO Versions",
        "",
        "| Source | versionMajor | versionMinor | Version string |",
        "| --- | ---: | ---: | --- |",
    ]
    for version in source_versions:
        lines.append(
            f"| `{version.path}` | {version.major} | {version.minor} | `{version_string(version)}` |"
        )

    lines.extend(["", "## Built Font Versions", "", "| Font | name ID 5 | Matches source version |", "| --- | --- | --- |"])
    for version in built_versions:
        matches = bool(expected_name_id_5 and version.name_id_5.startswith(expected_name_id_5))
        lines.append(f"| `{version.path}` | `{version.name_id_5}` | {yes_no(matches)} |")
    if not built_versions:
        lines.append("| `fonts/variable/Blocksync[wdth,wght].ttf` | `missing` | no |")

    lines.extend(
        [
            "",
            "## Finalization",
            "",
            "- Do not replace `source.commit` until the reviewed release tree has",
            "  been committed and `make release-check` passes on that commit.",
            "- Do not replace `date_added` until the downstream Google Fonts package",
            "  date is known.",
            "- After replacing either value, run `make metadata-final-check`,",
            "  `make release-check`, and `make final-readiness-check`.",
            "",
        ]
    )

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
