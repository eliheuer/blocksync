#!/usr/bin/env python3
"""Build a navigable index for generated diffenator2 proof files."""

from __future__ import annotations

from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROOF_DIR = ROOT / "out" / "proof"
INDEX = PROOF_DIR / "index.html"


def title_for(path: Path) -> str:
    name = path.name
    if name.endswith("-diffbrowsers_glyphs.html"):
        return name.replace("-diffbrowsers_glyphs.html", " glyphs")
    if name.endswith("-diffbrowsers_proofer.html"):
        return name.replace("-diffbrowsers_proofer.html", " proofer")
    if name.endswith("-diffbrowsers_text.html"):
        return name.replace("-diffbrowsers_text.html", " text")
    if name.endswith("-diffbrowsers_waterfall.html"):
        return name.replace("-diffbrowsers_waterfall.html", " waterfall")
    return name


def main() -> int:
    PROOF_DIR.mkdir(parents=True, exist_ok=True)
    html_files = sorted(path for path in PROOF_DIR.glob("*.html") if path.name != "index.html")
    font_files = sorted(PROOF_DIR.glob("*.ttf"))

    lines = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '  <meta charset="utf-8"/>',
        '  <meta name="viewport" content="width=device-width, initial-scale=1"/>',
        "  <title>Blocksync proof index</title>",
        "</head>",
        "<body>",
        "  <h1>Blocksync proof index</h1>",
        "  <h2>Diffenator2 HTML proofs</h2>",
        "  <ul>",
    ]
    for path in html_files:
        label = escape(title_for(path))
        href = escape(path.name)
        lines.append(f'    <li><a href="{href}">{label}</a></li>')
    lines += [
        "  </ul>",
        "  <h2>Proof font files</h2>",
        "  <ul>",
    ]
    for path in font_files:
        label = escape(path.name)
        lines.append(f'    <li><a href="{label}">{label}</a></li>')
    lines += [
        "  </ul>",
        "</body>",
        "</html>",
        "",
    ]
    INDEX.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {INDEX.relative_to(ROOT)} with {len(html_files)} proof pages and {len(font_files)} fonts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
