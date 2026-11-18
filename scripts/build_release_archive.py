#!/usr/bin/env python3
"""Build a deterministic local release archive for Google Fonts review."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import sys
import zipfile


ROOT = Path(__file__).resolve().parents[1]
METADATA_DRAFT = ROOT / "documentation" / "google-fonts-downstream-metadata-draft.md"
MANIFEST = ROOT / "documentation" / "release-archive-manifest.md"
OUTPUT_DEFAULT = ROOT / "dist" / "Blocksync-GF-review.zip"
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
ZIP_FILE_MODE = 0o644 << 16


def source_file_pairs(metadata: Path) -> list[tuple[str, str]]:
    text = metadata.read_text(encoding="utf-8")
    return re.findall(
        r'files\s*\{\s*source_file:\s*"([^"]+)"\s*dest_file:\s*"([^"]+)"\s*\}',
        text,
        flags=re.DOTALL,
    )


def unsafe_path(path: str) -> bool:
    parts = Path(path).parts
    return Path(path).is_absolute() or ".." in parts


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def display_path(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def validate(pairs: list[tuple[str, str]]) -> list[str]:
    issues: list[str] = []
    if not pairs:
        issues.append("no source.files entries found in metadata draft")

    source_files = [source for source, _ in pairs]
    dest_files = [dest for _, dest in pairs]

    for label, paths in (("source_file", source_files), ("dest_file", dest_files)):
        unsafe = [path for path in paths if unsafe_path(path)]
        if unsafe:
            issues.append(f"unsafe {label} paths: {', '.join(unsafe)}")
        duplicates = sorted({path for path in paths if paths.count(path) > 1})
        if duplicates:
            issues.append(f"duplicate {label} paths: {', '.join(duplicates)}")

    missing = [path for path in source_files if not (ROOT / path).is_file()]
    if missing:
        issues.append(f"missing source files: {', '.join(missing)}")
    return issues


def build_archive(output: Path, pairs: list[tuple[str, str]]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for source, _dest in sorted(pairs):
            info = zipfile.ZipInfo(source, date_time=ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = ZIP_FILE_MODE
            archive.writestr(info, (ROOT / source).read_bytes())


def archive_entries(output: Path) -> dict[str, tuple[int, str, bool]]:
    if not output.exists():
        return {}
    entries: dict[str, tuple[int, str, bool]] = {}
    with zipfile.ZipFile(output) as archive:
        for info in archive.infolist():
            digest = hashlib.sha256(archive.read(info.filename)).hexdigest()
            deterministic = (
                info.date_time == ZIP_TIMESTAMP
                and info.external_attr == ZIP_FILE_MODE
            )
            entries[info.filename] = (info.file_size, digest, deterministic)
    return entries


def manifest_markdown(
    output: Path,
    metadata: Path,
    pairs: list[tuple[str, str]],
    issues: list[str],
) -> str:
    source_files = [source for source, _ in pairs]
    entries = archive_entries(output)
    missing = [source for source in source_files if not (ROOT / source).is_file()]
    archive_missing = [source for source in source_files if source not in entries]
    archive_extra = [entry for entry in entries if entry not in source_files]
    hashes_match = all(
        source in entries and sha256(ROOT / source) == entries[source][1]
        for source in source_files
        if (ROOT / source).is_file()
    )
    deterministic = all(value[2] for value in entries.values()) if entries else False
    archive_hash = sha256(output) if output.exists() else "missing"

    lines = [
        "# Release Archive Manifest",
        "",
        "This is a local review archive for fallback Google Fonts release/archive",
        "packaging. The preferred package path remains `sources/config.yaml` ->",
        "`sources/Blocksync.designspace` unless Google Fonts asks for prebuilt",
        "release files.",
        "",
        "## Summary",
        "",
        f"- Mapping source: `{display_path(metadata)}`",
        f"- Local release archive: `{display_path(output)}`",
        f"- Archive inputs expected: {len(source_files)}",
        f"- Archive inputs present locally: {len(source_files) - len(missing)} / {len(source_files)}",
        f"- Missing archive inputs: {len(missing)}",
        f"- Validation issues: {len(issues)}",
        f"- Local release archive exists: {'yes' if output.exists() else 'no'}",
        f"- Local release archive contains expected files: {'yes' if not archive_missing and output.exists() else 'no'}",
        f"- Local release archive has extra files: {'yes' if archive_extra else 'no'}",
        f"- Local release archive hashes match source files: {'yes' if hashes_match and output.exists() else 'no'}",
        f"- Local release archive metadata deterministic: {'yes' if deterministic else 'no'}",
        f"- Local release archive SHA-256: `{archive_hash}`",
        "- Final GitHub release archive URL recorded: pending",
        "",
        "## Archive Inputs",
        "",
        "| Source file | Destination in package | Exists | Size bytes | SHA-256 |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for source, dest in pairs:
        path = ROOT / source
        exists = path.is_file()
        size = path.stat().st_size if exists else 0
        digest = sha256(path) if exists else "missing"
        lines.append(
            f"| `{source}` | `{dest}` | {'yes' if exists else 'no'} | {size} | `{digest}` |"
        )

    lines.extend(
        [
            "",
            "## Archive Entries",
            "",
            "| Archive entry | Present | Size matches source | SHA-256 matches source | Deterministic metadata |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for source in source_files:
        path = ROOT / source
        present = source in entries
        size_match = present and path.is_file() and path.stat().st_size == entries[source][0]
        hash_match = present and path.is_file() and sha256(path) == entries[source][1]
        deterministic_entry = present and entries[source][2]
        lines.append(
            "| `{}` | {} | {} | {} | {} |".format(
                source,
                "yes" if present else "no",
                "yes" if size_match else "no",
                "yes" if hash_match else "no",
                "yes" if deterministic_entry else "no",
            )
        )

    if issues:
        lines.extend(["", "## Validation Issues", ""])
        lines.extend(f"- {issue}" for issue in issues)

    lines.extend(
        [
            "",
            "## Final Release Gate",
            "",
            "1. Finish source and proof review.",
            "2. Replace final `date_added` and `source.commit` values.",
            "3. If using release/archive packaging, publish this archive or an",
            "   equivalent GitHub release asset and add the final `source.archive_url`.",
            "4. Rerun `make release-check` after any source, metadata, or archive",
            "   mapping change.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata", type=Path, default=METADATA_DRAFT)
    parser.add_argument("--output", type=Path, default=OUTPUT_DEFAULT)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--check-only", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    metadata = args.metadata if args.metadata.is_absolute() else ROOT / args.metadata
    output = args.output if args.output.is_absolute() else ROOT / args.output
    manifest = args.manifest if args.manifest.is_absolute() else ROOT / args.manifest
    pairs = source_file_pairs(metadata)
    issues = validate(pairs)
    if issues:
        manifest.write_text(manifest_markdown(output, metadata, pairs, issues), encoding="utf-8")
        for issue in issues:
            print(f"FAIL: {issue}")
        return 1
    if not args.check_only:
        build_archive(output, pairs)
    manifest.write_text(manifest_markdown(output, metadata, pairs, issues), encoding="utf-8")
    print(f"Wrote {display_path(manifest)}")
    if not args.check_only:
        print(f"Wrote {display_path(output)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
