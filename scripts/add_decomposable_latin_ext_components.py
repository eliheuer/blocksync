#!/usr/bin/env python3
"""Add decomposable Latin Extended review glyphs to the active UFO masters."""

from __future__ import annotations

import plistlib
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

from fontTools.ttLib import TTFont
from gfsubsets import CodepointsInSubset


ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources"
FONT = ROOT / "fonts" / "variable" / "Blocksync[wdth,wght].ttf"
MARK_COLOR = "0.67,0.95,0.38,1"
IGNORED = {0x0000, 0x000D, 0x0020, 0x00A0}
SUPPORTED_MARKS = {
    0x0300: ("gravecomb", "gravecomb.case", "top"),
    0x0301: ("acutecomb", "acutecomb.case", "top"),
    0x0302: ("circumflexcomb", "circumflexcomb.case", "top"),
    0x0303: ("tildecomb", "tildecomb.case", "top"),
    0x0304: ("macroncomb", "macroncomb.case", "top"),
    0x0306: ("brevecomb", "brevecomb.case", "top"),
    0x0307: ("dotaccentcomb", "dotaccentcomb.case", "top"),
    0x0308: ("dieresiscomb", "dieresiscomb.case", "top"),
    0x030A: ("ringcomb", "ringcomb.case", "top"),
    0x030B: ("hungarumlautcomb", "hungarumlautcomb.case", "top"),
    0x030C: ("caroncomb", "caroncomb.case", "top"),
    0x0312: ("commaturnedabovecomb", "commaturnedabovecomb", "top"),
    0x031B: ("horncomb", "horncomb", "top"),
    0x0323: ("dotbelowcomb", "dotbelowcomb", "bottom"),
    0x0326: ("commaaccentcomb", "commaaccentcomb.case", "bottom"),
    0x0327: ("cedillacomb", "cedillacomb", "bottom"),
    0x0328: ("ogonekcomb", "ogonekcomb", "bottom"),
}
SKIP_FOR_GLYPHSET_BOUNDARIES = {
    # These decomposable composites would push GF_TransLatin_Pinyin and/or
    # GF_Latin_PriAfrican above 80% coverage. That makes Fontspector enforce
    # broader language shaping expectations than this first submission supports.
    # Gcircumflex/gcircumflex also make package-context tofu checks treat Aleut
    # as supported even though U+0302 is not served by the declared GF subsets.
    0x011C,
    0x011D,
    0x01CF,
    0x01D0,
    0x01D1,
    0x01D2,
    0x01D5,
    0x01D6,
    0x01D7,
    0x01D8,
    0x01D9,
    0x01DA,
    0x01DB,
    0x01DC,
    0x01F8,
    0x01F9,
    0x1E3E,
    0x1E3F,
    0x1E44,
    0x1E45,
    0x1E62,
    0x1E63,
}


def fmt(value: float | str) -> str:
    if isinstance(value, str):
        return value
    if abs(value - round(value)) < 0.001:
        return str(int(round(value)))
    return f"{value:.3f}".rstrip("0").rstrip(".")


def glyph_path(ufo: Path, filename: str) -> Path:
    return ufo / "glyphs" / filename


def read_contents(ufo: Path) -> dict[str, str]:
    with (ufo / "glyphs" / "contents.plist").open("rb") as file:
        return plistlib.load(file)


def write_contents(ufo: Path, contents: dict[str, str]) -> None:
    with (ufo / "glyphs" / "contents.plist").open("wb") as file:
        plistlib.dump(contents, file, sort_keys=True)


def parse_glyph(ufo: Path, glyph_name: str, contents: dict[str, str]) -> ET.Element:
    return ET.parse(glyph_path(ufo, contents[glyph_name])).getroot()


def glyph_unicode(root: ET.Element) -> int | None:
    unicode_el = root.find("unicode")
    if unicode_el is None:
        return None
    return int(unicode_el.attrib["hex"], 16)


def unicode_map(ufo: Path, contents: dict[str, str]) -> dict[int, str]:
    result: dict[int, str] = {}
    for glyph_name in contents:
        try:
            root = parse_glyph(ufo, glyph_name, contents)
        except ET.ParseError:
            continue
        codepoint = glyph_unicode(root)
        if codepoint is not None:
            result[codepoint] = glyph_name
    return result


def anchor(root: ET.Element, name: str) -> tuple[float, float] | None:
    for anchor_el in root.findall("anchor"):
        if anchor_el.attrib.get("name") == name:
            return float(anchor_el.attrib["x"]), float(anchor_el.attrib["y"])
    return None


def mark_component_name(ufo: Path, mark_cp: int, uppercase: bool, contents: dict[str, str]) -> str:
    lower, upper, _ = SUPPORTED_MARKS[mark_cp]
    preferred = upper if uppercase else lower
    if preferred in contents:
        return preferred
    return lower


def is_uppercase_codepoint(codepoint: int) -> bool:
    return "CAPITAL" in unicodedata.name(chr(codepoint), "")


def component_attrs_for_mark(
    ufo: Path,
    base_root: ET.Element,
    base_codepoint: int,
    mark_cp: int,
    contents: dict[str, str],
) -> tuple[str, dict[str, str]]:
    mark_name = mark_component_name(ufo, mark_cp, is_uppercase_codepoint(base_codepoint), contents)
    mark_root = parse_glyph(ufo, mark_name, contents)
    _, _, side = SUPPORTED_MARKS[mark_cp]
    if side == "bottom":
        base_anchor = anchor(base_root, "bottom") or (0.0, 0.0)
        mark_anchor = anchor(mark_root, "_bottom") or (0.0, 0.0)
    else:
        base_anchor = anchor(base_root, "top") or (0.0, 800.0)
        mark_anchor = anchor(mark_root, "_top") or (0.0, 800.0)
    x_offset = base_anchor[0] - mark_anchor[0]
    y_offset = base_anchor[1] - mark_anchor[1]

    # Stacked accents can exceed current vertical metrics. Keep them inside the
    # current ascent until drawings are reviewed.
    if side == "top" and y_offset > 160:
        y_offset = 160

    attrs: dict[str, str] = {}
    if abs(x_offset) > 0.001:
        attrs["xOffset"] = fmt(x_offset)
    if abs(y_offset) > 0.001:
        attrs["yOffset"] = fmt(y_offset)
    return mark_name, attrs


def make_lib() -> ET.Element:
    lib = ET.Element("lib")
    dict_el = ET.SubElement(lib, "dict")
    ET.SubElement(dict_el, "key").text = "public.markColor"
    ET.SubElement(dict_el, "string").text = MARK_COLOR
    return lib


def write_component_glyph(
    ufo: Path,
    name: str,
    filename: str,
    codepoint: int,
    base_name: str,
    base_root: ET.Element,
    mark_components: list[tuple[str, dict[str, str]]],
) -> None:
    glyph = ET.Element("glyph", {"name": name, "format": "2"})
    advance = base_root.find("advance")
    if advance is not None:
        ET.SubElement(glyph, "advance", {"width": advance.attrib["width"]})
    ET.SubElement(glyph, "unicode", {"hex": f"{codepoint:04X}"})
    for anchor_el in base_root.findall("anchor"):
        if not anchor_el.attrib.get("name", "").startswith("_"):
            glyph.append(ET.Element("anchor", dict(anchor_el.attrib)))
    outline = ET.SubElement(glyph, "outline")
    ET.SubElement(outline, "component", {"base": base_name})
    for mark_name, attrs in mark_components:
        comp_attrs = {"base": mark_name}
        comp_attrs.update(attrs)
        ET.SubElement(outline, "component", comp_attrs)
    glyph.append(make_lib())
    ET.indent(glyph, space="  ")
    ET.ElementTree(glyph).write(glyph_path(ufo, filename), encoding="UTF-8", xml_declaration=True, short_empty_elements=True)


def built_font_codepoints() -> set[int]:
    font = TTFont(FONT)
    codepoints = set(font.getBestCmap() or {}) - IGNORED
    font.close()
    return codepoints


def target_codepoints() -> list[tuple[int, list[int]]]:
    present = built_font_codepoints()
    latin_ext = set(CodepointsInSubset("latin-ext", unique_glyphs=True))
    result: list[tuple[int, list[int]]] = []
    for codepoint in sorted((latin_ext - present) - IGNORED):
        decomp = unicodedata.decomposition(chr(codepoint))
        if not decomp or decomp.startswith("<"):
            continue
        parts = [int(part, 16) for part in decomp.split()]
        if not parts or parts[0] not in present:
            continue
        if all(part in SUPPORTED_MARKS and part in present for part in parts[1:]):
            result.append((codepoint, parts))
    return result


def add_for_ufo(ufo: Path, targets: list[tuple[int, list[int]]]) -> int:
    contents = read_contents(ufo)
    cmap = unicode_map(ufo, contents)
    removed = 0
    for glyph_name, filename in list(contents.items()):
        root = parse_glyph(ufo, glyph_name, contents)
        codepoint = glyph_unicode(root)
        if codepoint not in SKIP_FOR_GLYPHSET_BOUNDARIES:
            continue
        if not glyph_name.startswith("uni"):
            continue
        if not any(el.text == MARK_COLOR for el in root.findall("./lib/dict/string")):
            continue
        glyph_path(ufo, filename).unlink(missing_ok=True)
        del contents[glyph_name]
        cmap.pop(codepoint, None)
        removed += 1

    added = 0
    for codepoint, parts in targets:
        if codepoint in SKIP_FOR_GLYPHSET_BOUNDARIES:
            continue
        if codepoint in cmap:
            continue
        base_codepoint = parts[0]
        base_name = cmap.get(base_codepoint)
        if base_name is None:
            continue
        base_root = parse_glyph(ufo, base_name, contents)
        mark_components = [
            component_attrs_for_mark(ufo, base_root, base_codepoint, mark_cp, contents)
            for mark_cp in parts[1:]
        ]
        glyph_name = f"uni{codepoint:04X}"
        filename = f"uni{codepoint:04X}.glif"
        write_component_glyph(ufo, glyph_name, filename, codepoint, base_name, base_root, mark_components)
        contents[glyph_name] = filename
        cmap[codepoint] = glyph_name
        added += 1
    write_contents(ufo, contents)
    return added, removed


def main() -> int:
    targets = target_codepoints()
    print(f"Latin-ext decomposable targets: {len(targets)}")
    for ufo in sorted(SOURCES.glob("Blocksync-*.ufo")):
        added, removed = add_for_ufo(ufo, targets)
        print(f"Updated {ufo.relative_to(ROOT)}: {added} glyphs added, {removed} glyphs removed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
