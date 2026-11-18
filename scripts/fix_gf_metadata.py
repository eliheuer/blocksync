#!/usr/bin/env python3
"""Patch generated TTF metadata that is not preserved by instance generation."""

from pathlib import Path
import sys

from fontTools.ttLib import TTFont, newTable


ROOT = Path(__file__).resolve().parents[1]
COPYRIGHT = (ROOT / "OFL.txt").read_text(encoding="utf-8").splitlines()[0]
SCRIPT_TAGS = "Latn"


def set_name(font: TTFont, name_id: int, value: str) -> None:
    # Windows Unicode BMP, en-US.
    font["name"].setName(value, name_id, 3, 1, 0x409)
    # Macintosh Roman, English.
    font["name"].setName(value, name_id, 1, 0, 0)


def add_identity_avar(font: TTFont) -> None:
    if "fvar" not in font or "avar" in font:
        return
    avar = newTable("avar")
    avar.majorVersion = 1
    avar.minorVersion = 0
    avar.segments = {
        axis.axisTag: {-1.0: -1.0, 0.0: 0.0, 1.0: 1.0}
        for axis in font["fvar"].axes
    }
    font["avar"] = avar


def patch_font(path: Path) -> None:
    font = TTFont(path)
    font["OS/2"].fsType = 0
    set_name(font, 0, COPYRIGHT)
    add_identity_avar(font)

    meta = font["meta"] if "meta" in font else newTable("meta")
    meta.data = dict(getattr(meta, "data", {}))
    meta.data["dlng"] = SCRIPT_TAGS
    meta.data["slng"] = SCRIPT_TAGS
    font["meta"] = meta

    font.save(path)


def main(paths: list[str]) -> int:
    if not paths:
        raise SystemExit("usage: fix_gf_metadata.py FONT.ttf [FONT.ttf ...]")
    for raw_path in paths:
        path = Path(raw_path)
        if path.suffix.lower() == ".ttf":
            patch_font(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
