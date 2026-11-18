#!/usr/bin/env python3
"""Check the Blocksync downstream METADATA.pb draft.

The default mode validates that the draft is structurally coherent and records
release blockers without failing on final-date/final-commit placeholders. Use
`--final` when preparing the actual downstream package.
"""

from __future__ import annotations

import argparse
import math
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "documentation" / "google-fonts-downstream-metadata-draft.md"
DESCRIPTION = ROOT / "documentation" / "DESCRIPTION.en_us.html"
DESIGNSPACE = ROOT / "sources" / "Blocksync.designspace"
CONFIG = ROOT / "sources" / "config.yaml"
FONT = ROOT / "fonts" / "variable" / "Blocksync[wdth,wght].ttf"

EXPECTED = {
    "name": "Blocksync",
    "designer": "Eli Heuer",
    "license": "OFL",
    "category": "DISPLAY",
    "repository_url": "https://github.com/eliheuer/blocksyncer",
    "branch": "main",
    "config_yaml": "sources/config.yaml",
    "primary_script": "Latn",
    "stroke": "SANS_SERIF",
}

EXPECTED_SUBSETS = ["latin", "latin-ext", "menu", "vietnamese"]
EXPECTED_SOURCE_FILES = {
    "OFL.txt": "OFL.txt",
    "fonts/variable/Blocksync[wdth,wght].ttf": "Blocksync[wdth,wght].ttf",
    "documentation/DESCRIPTION.en_us.html": "DESCRIPTION.en_us.html",
}
EXPECTED_FVAR = {
    "wdth": (75.0, 100.0, 125.0),
    "wght": (400.0, 400.0, 900.0),
}


def extract_textproto() -> str:
    text = DRAFT.read_text(encoding="utf-8")
    match = re.search(r"```textproto\n(.*?)\n```", text, flags=re.S)
    if not match:
        raise ValueError("metadata draft must contain a textproto fenced block")
    return match.group(1)


def scalar(proto: str, key: str) -> str | None:
    match = re.search(rf'^\s*{re.escape(key)}:\s+"([^"]*)"', proto, flags=re.M)
    return match.group(1) if match else None


def all_scalars(proto: str, key: str) -> list[str]:
    return re.findall(rf'^\s*{re.escape(key)}:\s+"([^"]*)"', proto, flags=re.M)


def block(proto: str, key: str) -> str:
    match = re.search(rf"^\s*{re.escape(key)}\s+\{{\n(.*?)\n\}}", proto, flags=re.M | re.S)
    return match.group(1) if match else ""


def source_files(proto: str) -> dict[str, str]:
    files: dict[str, str] = {}
    for source_file, dest_file in re.findall(
        r'files\s+\{\s*source_file:\s+"([^"]+)"\s*dest_file:\s+"([^"]+)"\s*\}',
        proto,
        flags=re.S,
    ):
        files[source_file] = dest_file
    return files


def axes(proto: str) -> dict[str, tuple[float, float]]:
    result: dict[str, tuple[float, float]] = {}
    for axis_block in re.findall(r"axes\s+\{\n(.*?)\n\}", proto, flags=re.S):
        tag = scalar(axis_block, "tag")
        min_value = re.search(r"min_value:\s+([0-9.]+)", axis_block)
        max_value = re.search(r"max_value:\s+([0-9.]+)", axis_block)
        if tag and min_value and max_value:
            result[tag] = (float(min_value.group(1)), float(max_value.group(1)))
    return result


def designspace_axes() -> dict[str, tuple[float, float, float]]:
    root = ET.parse(DESIGNSPACE).getroot()
    values: dict[str, tuple[float, float, float]] = {}
    for axis in root.findall(".//axis"):
        tag = axis.attrib["tag"]
        values[tag] = (
            float(axis.attrib["minimum"]),
            float(axis.attrib["default"]),
            float(axis.attrib["maximum"]),
        )
    return values


def git_ignored(path: Path) -> bool:
    relpath = str(path.relative_to(ROOT))
    result = subprocess.run(
        ["git", "check-ignore", "-q", relpath],
        cwd=ROOT,
        check=False,
    )
    return result.returncode == 0


def read_font_metadata() -> dict[str, object] | None:
    if not FONT.exists():
        return None
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        return None

    font = TTFont(FONT)

    def name(name_id: int) -> str:
        record = font["name"].getName(name_id, 3, 1, 0x409)
        return record.toUnicode() if record else ""

    fvar = {
        axis.axisTag: (float(axis.minValue), float(axis.defaultValue), float(axis.maxValue))
        for axis in font["fvar"].axes
    }
    meta = {}
    if "meta" in font:
        meta = {key: value.decode("utf-8") if isinstance(value, bytes) else value for key, value in font["meta"].data.items()}
    return {
        "name1": name(1),
        "name2": name(2),
        "name4": name(4),
        "name6": name(6),
        "name0": name(0),
        "fsType": int(font["OS/2"].fsType),
        "vendor": font["OS/2"].achVendID,
        "fvar": fvar,
        "meta": meta,
        "has_avar": "avar" in font,
    }


def subset_thresholds() -> dict[str, tuple[int, int, int, float]] | None:
    if not FONT.exists():
        return None
    try:
        from fontTools.ttLib import TTFont
        from gfsubsets import CodepointsInSubset
    except ImportError:
        return None

    thresholds = {"latin-ext": 20, "vietnamese": 50}
    ignored = {0x0000, 0x000D, 0x0020, 0x00A0}
    font = TTFont(FONT)
    present = set(font.getBestCmap() or {}) - ignored
    font.close()

    result: dict[str, tuple[int, int, int, float]] = {}
    for subset, threshold in thresholds.items():
        codepoints = set(CodepointsInSubset(subset, unique_glyphs=True))
        required = math.floor(len(codepoints) * threshold / 100) + 1
        covered = len(codepoints & present)
        result[subset] = (covered, required, len(codepoints), covered / len(codepoints) * 100)
    return result


def record(kind: str, message: str, failures: list[str], blockers: list[str], warnings: list[str]) -> None:
    print(f"{kind}: {message}")
    if kind == "FAIL":
        failures.append(message)
    elif kind == "BLOCKER":
        blockers.append(message)
    elif kind == "WARN":
        warnings.append(message)


def check(args: argparse.Namespace) -> int:
    failures: list[str] = []
    blockers: list[str] = []
    warnings: list[str] = []

    proto = extract_textproto()
    source = block(proto, "source")
    font_block = block(proto, "fonts")

    for key, expected in EXPECTED.items():
        haystack = source if key in {"repository_url", "branch", "config_yaml"} else proto
        actual = scalar(haystack, key)
        if actual == expected:
            record("OK", f"{key} is {expected}", failures, blockers, warnings)
        else:
            record("FAIL", f"{key} is {actual!r}, expected {expected!r}", failures, blockers, warnings)

    date_added = scalar(proto, "date_added")
    commit = scalar(source, "commit")
    if date_added and re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_added):
        record("OK", f"date_added is final-looking: {date_added}", failures, blockers, warnings)
    else:
        record("BLOCKER", f"date_added is not final: {date_added}", failures, blockers, warnings)
    if commit and re.fullmatch(r"[0-9a-f]{40}", commit):
        record("OK", "source.commit is a final-looking 40-character hash", failures, blockers, warnings)
    else:
        record("BLOCKER", f"source.commit is not final: {commit}", failures, blockers, warnings)

    subsets = all_scalars(proto, "subsets")
    if subsets == EXPECTED_SUBSETS:
        record("OK", f"subsets match expected first-submission scope: {', '.join(subsets)}", failures, blockers, warnings)
        coverage = subset_thresholds()
        if coverage is None:
            record("WARN", "subset thresholds were not checked; run under venv after make build", failures, blockers, warnings)
        else:
            for subset, (covered, required, total, percent) in coverage.items():
                message = f"{subset} subset threshold: {covered}/{total} ({percent:.2f}%), requires {required}"
                if covered >= required:
                    record("OK", message, failures, blockers, warnings)
                else:
                    record("BLOCKER", message, failures, blockers, warnings)
    else:
        record("FAIL", f"subsets are {subsets}, expected {EXPECTED_SUBSETS}", failures, blockers, warnings)

    draft_axes = axes(proto)
    ds_axes = designspace_axes()
    for tag, expected in EXPECTED_FVAR.items():
        ds_axis = ds_axes.get(tag)
        draft_axis = draft_axes.get(tag)
        if ds_axis == expected and draft_axis == (expected[0], expected[2]):
            record("OK", f"{tag} axis matches designspace and metadata draft", failures, blockers, warnings)
        else:
            record("FAIL", f"{tag} axis mismatch: designspace={ds_axis}, draft={draft_axis}, expected={expected}", failures, blockers, warnings)

    config_text = CONFIG.read_text(encoding="utf-8")
    if "Blocksync.designspace" in config_text and ".glyphs" not in config_text:
        record("OK", "sources/config.yaml uses designspace/UFO source path", failures, blockers, warnings)
    else:
        record("FAIL", "sources/config.yaml must point to Blocksync.designspace and not .glyphs", failures, blockers, warnings)

    description_text = DESCRIPTION.read_text(encoding="utf-8")
    expected_repo_url = EXPECTED["repository_url"]
    if f'href="{expected_repo_url}"' in description_text and "github.com/eliheuer/blocksyncer" in description_text:
        record("OK", "DESCRIPTION links the canonical upstream repository", failures, blockers, warnings)
    else:
        record("FAIL", "DESCRIPTION must link the canonical upstream repository URL", failures, blockers, warnings)

    files = source_files(proto)
    if files == EXPECTED_SOURCE_FILES:
        record("OK", "source.files mapping matches current package preview", failures, blockers, warnings)
    else:
        record("FAIL", f"source.files mapping is {files}, expected {EXPECTED_SOURCE_FILES}", failures, blockers, warnings)

    for source_file in EXPECTED_SOURCE_FILES:
        path = ROOT / source_file
        if path.exists():
            suffix = " (gitignored generated output)" if git_ignored(path) else ""
            record("OK", f"{source_file} exists locally{suffix}", failures, blockers, warnings)
        else:
            record("FAIL", f"{source_file} is missing locally", failures, blockers, warnings)

    expected_font_fields = {
        "name": "Blocksync",
        "style": "normal",
        "filename": "Blocksync[wdth,wght].ttf",
        "post_script_name": "Blocksync-Regular",
        "full_name": "Blocksync Regular",
        "copyright": (ROOT / "OFL.txt").read_text(encoding="utf-8").splitlines()[0],
    }
    for key, expected in expected_font_fields.items():
        actual = scalar(font_block, key)
        if actual == expected:
            record("OK", f"font block {key} is {expected}", failures, blockers, warnings)
        else:
            record("FAIL", f"font block {key} is {actual!r}, expected {expected!r}", failures, blockers, warnings)

    font_meta = read_font_metadata()
    if font_meta is None:
        message = "built variable font metadata was not checked; run under venv after make build"
        if args.require_font:
            record("FAIL", message, failures, blockers, warnings)
        else:
            record("WARN", message, failures, blockers, warnings)
    else:
        expected_names = {
            "name1": "Blocksync",
            "name2": "Regular",
            "name4": "Blocksync Regular",
            "name6": "Blocksync-Regular",
            "name0": expected_font_fields["copyright"],
        }
        for key, expected in expected_names.items():
            actual = font_meta[key]
            if actual == expected:
                record("OK", f"built font {key} is {expected}", failures, blockers, warnings)
            else:
                record("FAIL", f"built font {key} is {actual!r}, expected {expected!r}", failures, blockers, warnings)
        if font_meta["fsType"] == 0:
            record("OK", "built font fsType is installable", failures, blockers, warnings)
        else:
            record("FAIL", f"built font fsType is {font_meta['fsType']}", failures, blockers, warnings)
        if font_meta["vendor"] == "FTGD":
            record("OK", "built font vendor ID is FTGD", failures, blockers, warnings)
        else:
            record("FAIL", f"built font vendor ID is {font_meta['vendor']!r}", failures, blockers, warnings)
        if font_meta["fvar"] == EXPECTED_FVAR:
            record("OK", "built font fvar axes match metadata", failures, blockers, warnings)
        else:
            record("FAIL", f"built font fvar axes are {font_meta['fvar']}", failures, blockers, warnings)
        if font_meta["has_avar"]:
            record("OK", "built font has avar table", failures, blockers, warnings)
        else:
            record("FAIL", "built font is missing avar table", failures, blockers, warnings)
        meta = font_meta["meta"]
        if meta.get("dlng") == "Latn" and meta.get("slng") == "Latn":
            record("OK", "built font meta dlng/slng are Latn", failures, blockers, warnings)
        else:
            record("FAIL", f"built font meta table is {meta}", failures, blockers, warnings)

    print("")
    print(f"Summary: {len(failures)} FAIL, {len(blockers)} BLOCKER, {len(warnings)} WARN")

    if failures:
        return 1
    if args.final and blockers:
        return 1
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--final", action="store_true", help="fail on final-release blockers")
    parser.add_argument("--require-font", action="store_true", help="fail if built-font metadata cannot be checked")
    return check(parser.parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
