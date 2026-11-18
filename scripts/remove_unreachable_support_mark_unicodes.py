#!/usr/bin/env python3
"""Inspect GF-unreachable standalone support-mark Unicode assignments.

The glyphs stay in the UFOs for component construction and mark features.
This script is diagnostic by default because removing these assignments was
verified to cause Google Fonts glyph coverage and dotted-circle failures.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources"

UNREACHABLE_SUPPORT_MARKS = {
    "breve": "02D8",
    "dotaccent": "02D9",
    "ogonek": "02DB",
    "circumflexcomb": "0302",
    "brevecomb": "0306",
    "dotaccentcomb": "0307",
    "ringcomb": "030A",
    "hungarumlautcomb": "030B",
    "caroncomb": "030C",
    "commaturnedabovecomb": "0312",
    "caroncomb.alt": "0315",
    "commaaccentcomb": "0326",
    "cedillacomb": "0327",
    "uni25CC": "25CC",
}


@dataclass(frozen=True)
class Change:
    path: Path
    glyph_name: str
    codepoint: str


def contents_map(ufo: Path) -> dict[str, str]:
    contents = ufo / "glyphs" / "contents.plist"
    root = ET.parse(contents).getroot()
    dict_element = root.find("dict")
    children = list(dict_element) if dict_element is not None else []
    return {
        key.text or "": value.text or ""
        for key, value in zip(children[0::2], children[1::2])
        if key.tag == "key" and value.tag == "string"
    }


def remove_unicode_line(text: str, codepoint: str) -> tuple[str, bool]:
    lines = text.splitlines()
    needle_a = f'<unicode hex="{codepoint}"/>'
    needle_b = f'<unicode hex="{codepoint}" />'
    changed = False
    kept: list[str] = []
    for line in lines:
        if needle_a in line or needle_b in line:
            changed = True
            continue
        kept.append(line)
    if not changed:
        return text, False
    suffix = "\n" if text.endswith("\n") else ""
    return "\n".join(kept) + suffix, True


def planned_removals() -> list[Change]:
    changes: list[Change] = []
    for ufo in sorted(SOURCES.glob("Blocksync-*.ufo")):
        glyph_files = contents_map(ufo)
        for glyph_name, codepoint in UNREACHABLE_SUPPORT_MARKS.items():
            glif_name = glyph_files.get(glyph_name)
            if not glif_name:
                continue
            path = ufo / "glyphs" / glif_name
            text = path.read_text(encoding="utf-8")
            if f'hex="{codepoint}"' in text:
                changes.append(Change(path, glyph_name, codepoint))
    return changes


def planned_restores() -> list[Change]:
    changes: list[Change] = []
    for ufo in sorted(SOURCES.glob("Blocksync-*.ufo")):
        glyph_files = contents_map(ufo)
        for glyph_name, codepoint in UNREACHABLE_SUPPORT_MARKS.items():
            glif_name = glyph_files.get(glyph_name)
            if not glif_name:
                continue
            path = ufo / "glyphs" / glif_name
            text = path.read_text(encoding="utf-8")
            if f'hex="{codepoint}"' not in text:
                changes.append(Change(path, glyph_name, codepoint))
    return changes


def apply_changes(changes: list[Change]) -> None:
    for change in changes:
        text = change.path.read_text(encoding="utf-8")
        updated, changed = remove_unicode_line(text, change.codepoint)
        if changed:
            change.path.write_text(updated, encoding="utf-8")


def restore_changes(changes: list[Change]) -> None:
    for change in changes:
        text = change.path.read_text(encoding="utf-8")
        if f'hex="{change.codepoint}"' in text:
            continue
        lines = text.splitlines()
        insert_at = 2 if len(lines) >= 2 and lines[0].startswith("<?xml ") else 0
        for index, line in enumerate(lines):
            if "<advance " in line:
                insert_at = index + 1
                break
            if index > 0 and line.startswith("<glyph "):
                insert_at = index + 1
        lines.insert(insert_at, f'  <unicode hex="{change.codepoint}"/>')
        suffix = "\n" if text.endswith("\n") else ""
        change.path.write_text("\n".join(lines) + suffix, encoding="utf-8")


def main() -> int:
    apply = "--apply" in sys.argv
    restore = "--restore" in sys.argv
    force_unsafe = "--force-unsafe" in sys.argv
    changes = planned_restores() if restore else planned_removals()
    if changes:
        for change in changes:
            print(
                f"{'RESTORE' if restore else ('REMOVE' if apply else 'WOULD REMOVE')} "
                f"U+{change.codepoint} from {change.path.relative_to(ROOT)} "
                f"({change.glyph_name})"
            )
    else:
        print("No matching support-mark Unicode assignment changes found.")

    if restore:
        restore_changes(changes)
        print(f"Restored {len(changes)} Unicode assignment(s).")
    elif apply:
        if not force_unsafe:
            print(
                "Refusing to remove Unicode assignments without --force-unsafe; "
                "this path caused GF glyph_coverage and dotted_circle failures."
            )
            return 2
        apply_changes(changes)
        print(f"Applied {len(changes)} Unicode assignment removal(s).")
    else:
        print(
            "Dry run only. Do not use --force-unsafe for release unless Google Fonts "
            "explicitly asks to drop these codepoints."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
