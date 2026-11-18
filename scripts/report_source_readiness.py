#!/usr/bin/env python3
"""Generate a designspace/UFO source readiness report for Blocksync."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import plistlib
import sys
import xml.etree.ElementTree as ET

from fontTools.ufoLib import UFOReader


ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources"
CONFIG = SOURCES / "config.yaml"
DESIGNSPACE = SOURCES / "Blocksync.designspace"
OUTPUT = ROOT / "documentation" / "source-readiness.md"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def designspace_sources() -> tuple[list[dict[str, str]], list[str]]:
    issues: list[str] = []
    try:
        root = ET.parse(DESIGNSPACE).getroot()
    except ET.ParseError as error:
        return [], [f"designspace XML is invalid: {error}"]
    sources = [
        dict(source.attrib)
        for source in root.findall(".//source")
        if "filename" in source.attrib
    ]
    source_files = [source["filename"] for source in sources]
    if not sources:
        issues.append("designspace has no source filename entries")
    duplicates = sorted(name for name, count in Counter(source_files).items() if count > 1)
    if duplicates:
        issues.append(f"designspace has duplicate source entries: {', '.join(duplicates)}")
    return sources, issues


def plist(path: Path) -> object:
    with path.open("rb") as file:
        return plistlib.load(file)


def inspect_ufo(ufo: Path) -> tuple[dict[str, object], list[str], list[str]]:
    issues: list[str] = []
    notes: list[str] = []
    info: dict[str, object] = {
        "glyph_count": 0,
        "family": "unknown",
        "style": "unknown",
        "format": "unknown",
        "features": "missing",
        "glyphs": set(),
        "component_refs": 0,
        "missing_components": [],
        "extra_layers": [],
    }

    try:
        reader = UFOReader(str(ufo), validate=True)
        info["format"] = ".".join(str(part) for part in reader.formatVersionTuple)
        layer_names = reader.getLayerNames()
        if "public.default" not in layer_names:
            issues.append(f"{rel(ufo)} does not have a public.default layer")
        elif layer_names != ["public.default"]:
            extra_layers = [name for name in layer_names if name != "public.default"]
            info["extra_layers"] = extra_layers
            notes.append(
                f"{rel(ufo)} has {len(extra_layers)} historical non-default layers "
                "ignored by the designspace build"
            )
        font_info = type("Info", (), {})()
        reader.readInfo(font_info)
        info["family"] = getattr(font_info, "familyName", "unknown")
        info["style"] = getattr(font_info, "styleName", "unknown")
    except Exception as error:  # noqa: BLE001 - report validation exception text.
        issues.append(f"{rel(ufo)} failed UFOReader validation: {error}")
        return info, issues, notes

    contents_path = ufo / "glyphs" / "contents.plist"
    if not contents_path.is_file():
        issues.append(f"{rel(contents_path)} is missing")
        return info, issues, notes

    try:
        contents = plist(contents_path)
    except Exception as error:  # noqa: BLE001
        issues.append(f"{rel(contents_path)} is not readable: {error}")
        return info, issues, notes
    if not isinstance(contents, dict):
        issues.append(f"{rel(contents_path)} is not a plist dictionary")
        return info, issues, notes

    glyph_names = set(contents)
    info["glyphs"] = glyph_names
    info["glyph_count"] = len(glyph_names)

    missing_glifs: list[str] = []
    malformed_glifs: list[str] = []
    mismatched_names: list[str] = []
    missing_components: list[str] = []
    component_refs = 0

    for glyph_name, filename in sorted(contents.items()):
        glif_path = ufo / "glyphs" / filename
        if not glif_path.is_file():
            missing_glifs.append(glyph_name)
            continue
        try:
            glyph_root = ET.parse(glif_path).getroot()
        except ET.ParseError as error:
            malformed_glifs.append(f"{glyph_name}: {error}")
            continue
        if glyph_root.attrib.get("name") != glyph_name:
            mismatched_names.append(f"{glyph_name} -> {glyph_root.attrib.get('name', 'missing')}")
        for component in glyph_root.findall(".//component"):
            base = component.attrib.get("base")
            if base:
                component_refs += 1
                if base not in glyph_names:
                    missing_components.append(f"{glyph_name} -> {base}")

    if missing_glifs:
        issues.append(f"{rel(ufo)} has missing GLIF files: {', '.join(missing_glifs[:20])}")
    if malformed_glifs:
        issues.append(f"{rel(ufo)} has malformed GLIF XML: {', '.join(malformed_glifs[:10])}")
    if mismatched_names:
        issues.append(f"{rel(ufo)} has glyph name mismatches: {', '.join(mismatched_names[:20])}")
    if missing_components:
        issues.append(f"{rel(ufo)} has missing component bases: {', '.join(missing_components[:20])}")

    features = read(ufo / "features.fea")
    if "languagesystem latn dflt;" in features:
        info["features"] = "latn"
    elif features:
        info["features"] = "present-no-latn"
        issues.append(f"{rel(ufo / 'features.fea')} does not declare `languagesystem latn dflt;`")
    else:
        issues.append(f"{rel(ufo / 'features.fea')} is missing or empty")

    info["component_refs"] = component_refs
    info["missing_components"] = missing_components
    return info, issues, notes


def main() -> int:
    issues: list[str] = []
    config_text = read(CONFIG)
    config_uses_designspace = "Blocksync.designspace" in config_text and ".glyphs" not in config_text
    if not config_uses_designspace:
        issues.append("sources/config.yaml must point to Blocksync.designspace and not .glyphs")

    top_level_glyphs = sorted(path.name for path in SOURCES.glob("*.glyphs"))
    archived_glyphs = sorted(path.name for path in (SOURCES / "archive").glob("*.glyphs"))
    if top_level_glyphs:
        issues.append(f"top-level .glyphs files must stay archived: {', '.join(top_level_glyphs)}")
    if not archived_glyphs:
        issues.append("sources/archive has no archived .glyphs snapshots")

    source_entries, designspace_issues = designspace_sources()
    source_files = [source["filename"] for source in source_entries]
    layer_overrides = [
        source for source in source_entries if source.get("layer") or source.get("layername")
    ]
    issues.extend(designspace_issues)
    review_notes: list[str] = []

    ufo_reports: dict[str, dict[str, object]] = {}
    glyph_sets: dict[str, set[str]] = {}
    for source_file in source_files:
        ufo = SOURCES / source_file
        if not ufo.is_dir():
            issues.append(f"designspace source is missing: sources/{source_file}")
            continue
        report, ufo_issues, ufo_notes = inspect_ufo(ufo)
        ufo_reports[source_file] = report
        glyph_sets[source_file] = report["glyphs"] if isinstance(report["glyphs"], set) else set()
        issues.extend(ufo_issues)
        review_notes.extend(ufo_notes)

    inventory_match = False
    inventory_reference = set(next(iter(glyph_sets.values()))) if glyph_sets else set()
    if glyph_sets:
        inventory_match = all(glyphs == inventory_reference for glyphs in glyph_sets.values())
        if not inventory_match:
            for source_file, glyphs in glyph_sets.items():
                missing = sorted(inventory_reference - glyphs)
                extra = sorted(glyphs - inventory_reference)
                if missing or extra:
                    issues.append(
                        f"{source_file} inventory differs from first source: "
                        f"missing {len(missing)}, extra {len(extra)}"
                    )

    historical_layer_count = sum(
        len(report["extra_layers"]) for report in ufo_reports.values() if isinstance(report["extra_layers"], list)
    )
    default_build_layers_only = not layer_overrides
    ready = not issues
    lines = [
        "# Source Readiness",
        "",
        "This generated report validates the active Google Fonts source path.",
        "It checks that the build is designspace/UFO based, historical `.glyphs`",
        "files are archived, and each active UFO can be loaded and inspected.",
        "",
        "## Summary",
        "",
        f"- Source-ready for Google Fonts build path: {yes_no(ready)}",
        f"- sources/config.yaml uses designspace/UFO: {yes_no(config_uses_designspace)}",
        f"- Top-level `.glyphs` files in sources/: {len(top_level_glyphs)}",
        f"- Archived `.glyphs` snapshots: {len(archived_glyphs)}",
        f"- Designspace source UFOs: {len(source_files)}",
        f"- Designspace source layer overrides: {len(layer_overrides)}",
        f"- Active build uses default UFO layers only: {yes_no(default_build_layers_only)}",
        f"- Historical non-default UFO layers: {historical_layer_count}",
        f"- Existing inspected UFOs: {len(ufo_reports)} / {len(source_files)}",
        f"- Active UFO glyph inventories match: {yes_no(inventory_match)}",
        f"- Validation issues: {len(issues)}",
        f"- Review notes: {len(review_notes)}",
        "",
        "## Active UFOs",
        "",
        "| UFO | Family | Style | UFO format | Glyphs | Component refs | Historical layers | Features |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for source_file, report in ufo_reports.items():
        lines.append(
            "| `{}` | {} | {} | {} | {} | {} | {} | {} |".format(
                source_file,
                report["family"],
                report["style"],
                report["format"],
                report["glyph_count"],
                report["component_refs"],
                len(report["extra_layers"]) if isinstance(report["extra_layers"], list) else 0,
                report["features"],
            )
        )

    lines.extend(["", "## Archived Glyphs Sources", ""])
    if archived_glyphs:
        lines.extend(f"- `sources/archive/{name}`" for name in archived_glyphs)
    else:
        lines.append("- none")

    lines.extend(["", "## Validation Issues", ""])
    if issues:
        lines.extend(f"- {issue}" for issue in issues)
    else:
        lines.append("- none")

    lines.extend(["", "## Review Notes", ""])
    if review_notes:
        lines.extend(f"- {note}" for note in review_notes)
    else:
        lines.append("- none")

    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {rel(OUTPUT)}")
    if issues:
        for issue in issues:
            print(f"FAIL: {issue}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
