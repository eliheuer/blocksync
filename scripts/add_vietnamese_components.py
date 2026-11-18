#!/usr/bin/env python3
"""Add component-based Vietnamese review glyphs to the active UFO masters."""

from __future__ import annotations

import plistlib
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources"
MARK_COLOR = "0.67,0.95,0.38,1"


def fmt(value: float | str) -> str:
    if isinstance(value, str):
        return value
    if abs(value - round(value)) < 0.001:
        return str(int(round(value)))
    return f"{value:.3f}".rstrip("0").rstrip(".")


def glyph_path(ufo: Path, filename: str) -> Path:
    return ufo / "glyphs" / filename


def parse_glyph(ufo: Path, filename: str) -> ET.Element:
    return ET.parse(glyph_path(ufo, filename)).getroot()


def advance_width(ufo: Path, glyph_file: str) -> str:
    root = parse_glyph(ufo, glyph_file)
    advance = root.find("advance")
    return advance.attrib["width"] if advance is not None else "0"


def component_offsets(ufo: Path, glyph_file: str) -> dict[str, dict[str, str]]:
    root = parse_glyph(ufo, glyph_file)
    return {
        component.attrib["base"]: {
            key: value
            for key, value in component.attrib.items()
            if key not in {"base"}
        }
        for component in root.findall(".//component")
    }


def copy_base_anchors(ufo: Path, glyph_file: str, above: bool = False, below: bool = False) -> list[ET.Element]:
    root = parse_glyph(ufo, glyph_file)
    anchors = []
    for anchor in root.findall("anchor"):
        name = anchor.attrib.get("name", "")
        if name.startswith("_"):
            continue
        attrs = dict(anchor.attrib)
        if above and name == "top":
            attrs["y"] = fmt(max(float(attrs.get("y", "800")), 1017))
        if below and name == "bottom":
            attrs["y"] = fmt(min(float(attrs.get("y", "0")), -260))
        anchors.append(ET.Element("anchor", attrs))
    return anchors


def make_lib() -> ET.Element:
    lib = ET.Element("lib")
    dict_el = ET.SubElement(lib, "dict")
    ET.SubElement(dict_el, "key").text = "public.markColor"
    ET.SubElement(dict_el, "string").text = MARK_COLOR
    return lib


def write_glyph(
    ufo: Path,
    name: str,
    filename: str,
    unicode_hex: str | None,
    advance: str | None,
    components: list[tuple[str, dict[str, str]]],
    anchors: list[ET.Element] | None = None,
) -> None:
    glyph = ET.Element("glyph", {"name": name, "format": "2"})
    if advance is not None:
        ET.SubElement(glyph, "advance", {"width": advance})
    if unicode_hex is not None:
        ET.SubElement(glyph, "unicode", {"hex": unicode_hex})
    if anchors:
        for anchor in anchors:
            glyph.append(anchor)
    outline = ET.SubElement(glyph, "outline")
    for base, attrs in components:
        comp_attrs = {"base": base}
        comp_attrs.update({key: fmt(value) for key, value in attrs.items() if value not in {None, "", "0", "0.0"}})
        ET.SubElement(outline, "component", comp_attrs)
    glyph.append(make_lib())

    ET.indent(glyph, space="  ")
    tree = ET.ElementTree(glyph)
    path = glyph_path(ufo, filename)
    tree.write(path, encoding="UTF-8", xml_declaration=True, short_empty_elements=True)


def update_contents(ufo: Path, entries: dict[str, str]) -> None:
    path = ufo / "glyphs" / "contents.plist"
    with path.open("rb") as file:
        contents = plistlib.load(file)
    for obsolete in ("hookabovecomb.case", "horncomb.case", "dotbelowcomb.case"):
        contents.pop(obsolete, None)
        obsolete_path = ufo / "glyphs" / f"{obsolete}.glif"
        if obsolete_path.exists():
            obsolete_path.unlink()
    contents.update(entries)
    with path.open("wb") as file:
        plistlib.dump(contents, file, sort_keys=True)


def add_mark_glyphs(ufo: Path) -> dict[str, str]:
    entries = {
        "hookabovecomb": "hookabovecomb.glif",
        "horncomb": "horncomb.glif",
        "dotbelowcomb": "dotbelowcomb.glif",
    }
    write_glyph(
        ufo,
        "hookabovecomb",
        entries["hookabovecomb"],
        "0309",
        None,
        [("quoteright", {"xOffset": "7", "yOffset": "220"})],
        [ET.Element("anchor", {"x": "114", "y": "800", "name": "_top"})],
    )
    write_glyph(
        ufo,
        "horncomb",
        entries["horncomb"],
        "031B",
        None,
        [("quoteright", {"xOffset": "0", "yOffset": "-15"})],
        [ET.Element("anchor", {"x": "109", "y": "620", "name": "_top"})],
    )
    write_glyph(
        ufo,
        "dotbelowcomb",
        entries["dotbelowcomb"],
        "0323",
        None,
        [("period", {"yOffset": "-260"})],
        [ET.Element("anchor", {"x": "109", "y": "0", "name": "_bottom"})],
    )
    return entries


SINGLE_OFFSETS = {
    "acute": ("acutecomb", "acutecomb.case"),
    "grave": ("gravecomb", "gravecomb.case"),
    "circumflex": ("circumflexcomb", "circumflexcomb.case"),
    "breve": ("brevecomb", "brevecomb.case"),
    "tilde": ("tildecomb", "tildecomb.case"),
}


def mark_offset(ufo: Path, base: str, mark: str, uppercase: bool) -> str:
    glyph_file = f"{base}_{mark}.glif" if uppercase else f"{base}{mark}.glif"
    if not glyph_path(ufo, glyph_file).exists():
        glyph_file = f"{base}_acute.glif" if uppercase else f"{base}acute.glif"
        mark_name = "acutecomb.case" if uppercase else "acutecomb"
        return component_offsets(ufo, glyph_file)[mark_name].get("xOffset", "0")
    mark_name = SINGLE_OFFSETS[mark][1 if uppercase else 0]
    offsets = component_offsets(ufo, glyph_file)
    return offsets[mark_name].get("xOffset", "0")


def dot_offset(ufo: Path, base: str, uppercase: bool) -> str:
    dot_file = f"{base}_dotaccent.glif" if uppercase else f"{base}dotaccent.glif"
    if glyph_path(ufo, dot_file).exists():
        dot_name = "dotaccentcomb.case" if uppercase else "dotaccentcomb"
        return component_offsets(ufo, dot_file)[dot_name].get("xOffset", "0")
    return mark_offset(ufo, base, "acute", uppercase)


def hook_offset(ufo: Path, base: str, uppercase: bool) -> str:
    return mark_offset(ufo, base, "acute", uppercase)


def horn_offset(ufo: Path, base_file: str) -> str:
    return fmt(float(advance_width(ufo, base_file)) - 178)


def add_composite(
    ufo: Path,
    entries: dict[str, str],
    codepoint: int,
    base_name: str,
    base_file: str,
    marks: list[tuple[str, dict[str, str]]],
    above: bool,
    below: bool,
) -> None:
    filename = f"uni{codepoint:04X}.glif"
    name = f"uni{codepoint:04X}"
    entries[name] = filename
    components = [(base_name, {})] + marks
    write_glyph(
        ufo,
        name,
        filename,
        f"{codepoint:04X}",
        advance_width(ufo, base_file),
        components,
        copy_base_anchors(ufo, base_file, above=above, below=below),
    )


def add_vietnamese_for_ufo(ufo: Path) -> None:
    entries = add_mark_glyphs(ufo)

    cases = {
        "A": ("A", "A_.glif", True),
        "a": ("a", "a.glif", False),
        "E": ("E", "E_.glif", True),
        "e": ("e", "e.glif", False),
        "I": ("I", "I_.glif", True),
        "i": ("i", "i.glif", False),
        "O": ("O", "O_.glif", True),
        "o": ("o", "o.glif", False),
        "U": ("U", "U_.glif", True),
        "u": ("u", "u.glif", False),
        "Y": ("Y", "Y_.glif", True),
        "y": ("y", "y.glif", False),
    }

    def mark(base_key: str, mark_key: str, stack: int = 0) -> tuple[str, dict[str, str]]:
        _, _, uppercase = cases[base_key]
        mark_name = SINGLE_OFFSETS[mark_key][1 if uppercase else 0]
        attrs = {"xOffset": mark_offset(ufo, base_key, mark_key, uppercase)}
        if stack:
            attrs["yOffset"] = fmt(stack)
        return (mark_name, attrs)

    def hook(base_key: str, stack: int = 0) -> tuple[str, dict[str, str]]:
        _, _, uppercase = cases[base_key]
        mark_name = "hookabovecomb"
        attrs = {"xOffset": hook_offset(ufo, base_key, uppercase)}
        if stack:
            attrs["yOffset"] = fmt(stack)
        return (mark_name, attrs)

    def dotbelow(base_key: str) -> tuple[str, dict[str, str]]:
        _, _, uppercase = cases[base_key]
        mark_name = "dotbelowcomb"
        return (mark_name, {"xOffset": dot_offset(ufo, base_key, uppercase)})

    def horn(base_key: str) -> tuple[str, dict[str, str]]:
        _, base_file, uppercase = cases[base_key]
        mark_name = "horncomb"
        return (mark_name, {"xOffset": horn_offset(ufo, base_file)})

    def comp(code: int, base_key: str, marks: list[tuple[str, dict[str, str]]], above=False, below=False) -> None:
        base_name, base_file, _ = cases[base_key]
        add_composite(ufo, entries, code, base_name, base_file, marks, above=above, below=below)

    # Horn bases.
    comp(0x01A0, "O", [horn("O")], above=True)
    comp(0x01A1, "o", [horn("o")], above=True)
    comp(0x01AF, "U", [horn("U")], above=True)
    comp(0x01B0, "u", [horn("u")], above=True)

    # A and a.
    comp(0x1EA0, "A", [dotbelow("A")], below=True)
    comp(0x1EA1, "a", [dotbelow("a")], below=True)
    comp(0x1EA2, "A", [hook("A")], above=True)
    comp(0x1EA3, "a", [hook("a")], above=True)
    for code, base_key, accent, stack, below in [
        (0x1EA4, "A", "acute", 160, False), (0x1EA5, "a", "acute", 160, False),
        (0x1EA6, "A", "grave", 160, False), (0x1EA7, "a", "grave", 160, False),
        (0x1EA8, "A", "hook", 160, False), (0x1EA9, "a", "hook", 160, False),
        (0x1EAA, "A", "tilde", 160, False), (0x1EAB, "a", "tilde", 160, False),
        (0x1EAC, "A", "dot", 0, True), (0x1EAD, "a", "dot", 0, True),
    ]:
        first = mark(base_key, "circumflex")
        second = dotbelow(base_key) if accent == "dot" else hook(base_key, stack) if accent == "hook" else mark(base_key, accent, stack)
        comp(code, base_key, [first, second], above=not below, below=below)
    for code, base_key, accent, stack, below in [
        (0x1EAE, "A", "acute", 150, False), (0x1EAF, "a", "acute", 150, False),
        (0x1EB0, "A", "grave", 150, False), (0x1EB1, "a", "grave", 150, False),
        (0x1EB2, "A", "hook", 150, False), (0x1EB3, "a", "hook", 150, False),
        (0x1EB4, "A", "tilde", 150, False), (0x1EB5, "a", "tilde", 150, False),
        (0x1EB6, "A", "dot", 0, True), (0x1EB7, "a", "dot", 0, True),
    ]:
        first = mark(base_key, "breve")
        second = dotbelow(base_key) if accent == "dot" else hook(base_key, stack) if accent == "hook" else mark(base_key, accent, stack)
        comp(code, base_key, [first, second], above=not below, below=below)

    # E and e.
    comp(0x1EB8, "E", [dotbelow("E")], below=True)
    comp(0x1EB9, "e", [dotbelow("e")], below=True)
    comp(0x1EBA, "E", [hook("E")], above=True)
    comp(0x1EBB, "e", [hook("e")], above=True)
    for code, base_key, accent, stack, below in [
        (0x1EBE, "E", "acute", 160, False), (0x1EBF, "e", "acute", 160, False),
        (0x1EC0, "E", "grave", 160, False), (0x1EC1, "e", "grave", 160, False),
        (0x1EC2, "E", "hook", 160, False), (0x1EC3, "e", "hook", 160, False),
        (0x1EC4, "E", "tilde", 160, False), (0x1EC5, "e", "tilde", 160, False),
        (0x1EC6, "E", "dot", 0, True), (0x1EC7, "e", "dot", 0, True),
    ]:
        first = mark(base_key, "circumflex")
        second = dotbelow(base_key) if accent == "dot" else hook(base_key, stack) if accent == "hook" else mark(base_key, accent, stack)
        comp(code, base_key, [first, second], above=not below, below=below)

    # I/i, O/o, U/u, Y/y.
    for code, base_key, kind in [
        (0x1EC8, "I", "hook"), (0x1EC9, "i", "hook"), (0x1ECA, "I", "dot"), (0x1ECB, "i", "dot"),
        (0x1ECC, "O", "dot"), (0x1ECD, "o", "dot"), (0x1ECE, "O", "hook"), (0x1ECF, "o", "hook"),
        (0x1EE4, "U", "dot"), (0x1EE5, "u", "dot"), (0x1EE6, "U", "hook"), (0x1EE7, "u", "hook"),
        (0x1EF4, "Y", "dot"), (0x1EF5, "y", "dot"), (0x1EF6, "Y", "hook"), (0x1EF7, "y", "hook"),
        (0x1EF8, "Y", "tilde"), (0x1EF9, "y", "tilde"),
    ]:
        if kind == "dot":
            comp(code, base_key, [dotbelow(base_key)], below=True)
        elif kind == "hook":
            comp(code, base_key, [hook(base_key)], above=True)
        else:
            comp(code, base_key, [mark(base_key, kind)], above=True)

    for code, base_key, accent, stack, below in [
        (0x1ED0, "O", "acute", 160, False), (0x1ED1, "o", "acute", 160, False),
        (0x1ED2, "O", "grave", 160, False), (0x1ED3, "o", "grave", 160, False),
        (0x1ED4, "O", "hook", 160, False), (0x1ED5, "o", "hook", 160, False),
        (0x1ED6, "O", "tilde", 160, False), (0x1ED7, "o", "tilde", 160, False),
        (0x1ED8, "O", "dot", 0, True), (0x1ED9, "o", "dot", 0, True),
    ]:
        first = mark(base_key, "circumflex")
        second = dotbelow(base_key) if accent == "dot" else hook(base_key, stack) if accent == "hook" else mark(base_key, accent, stack)
        comp(code, base_key, [first, second], above=not below, below=below)

    for code, base_key, accent, below in [
        (0x1EDA, "O", "acute", False), (0x1EDB, "o", "acute", False),
        (0x1EDC, "O", "grave", False), (0x1EDD, "o", "grave", False),
        (0x1EDE, "O", "hook", False), (0x1EDF, "o", "hook", False),
        (0x1EE0, "O", "tilde", False), (0x1EE1, "o", "tilde", False),
        (0x1EE2, "O", "dot", True), (0x1EE3, "o", "dot", True),
        (0x1EE8, "U", "acute", False), (0x1EE9, "u", "acute", False),
        (0x1EEA, "U", "grave", False), (0x1EEB, "u", "grave", False),
        (0x1EEC, "U", "hook", False), (0x1EED, "u", "hook", False),
        (0x1EEE, "U", "tilde", False), (0x1EEF, "u", "tilde", False),
        (0x1EF0, "U", "dot", True), (0x1EF1, "u", "dot", True),
    ]:
        second = dotbelow(base_key) if accent == "dot" else hook(base_key) if accent == "hook" else mark(base_key, accent)
        comp(code, base_key, [horn(base_key), second], above=not below, below=below)

    update_contents(ufo, entries)


def main() -> int:
    ufos = sorted(SOURCES.glob("Blocksync-*.ufo"))
    for ufo in ufos:
        add_vietnamese_for_ufo(ufo)
        print(f"Updated {ufo.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
