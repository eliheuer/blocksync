#!/usr/bin/env python3
"""Generate visual proof review readiness for Blocksync."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "documentation" / "proof-review-readiness.md"
PROOF_DIR = ROOT / "out" / "proof"
INDEX = PROOF_DIR / "index.html"
DECISIONS = ROOT / "documentation" / "google-fonts-final-decision-sheet.md"
GLYPHSET_COVERAGE = ROOT / "documentation" / "google-fonts-glyphset-coverage.md"
WARNINGS = ROOT / "documentation" / "fontspector-zero-warning-worklist.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def row_final_answer(row_name: str, decisions: str) -> str:
    for line in decisions.splitlines():
        if not line.startswith(f"| {row_name} |"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        return cells[2] if len(cells) >= 3 else "unknown"
    return "unknown"


def html_links(index_text: str) -> list[str]:
    return re.findall(r'<a href="([^"]+\.html)">', index_text)


def font_links(index_text: str) -> list[str]:
    return re.findall(r'<a href="([^"]+\.ttf)">', index_text)


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def main() -> int:
    index_text = read(INDEX)
    decisions = read(DECISIONS)
    glyphset = read(GLYPHSET_COVERAGE)
    warnings = read(WARNINGS)
    links = [link for link in html_links(index_text) if link != "index.html"]
    fonts = font_links(index_text)
    missing_links = [link for link in links if not (PROOF_DIR / link).exists()]
    missing_fonts = [link for link in fonts if not (PROOF_DIR / link).exists()]
    proof_answer = row_final_answer("Visual proof", decisions)
    composite_answer = row_final_answer("Generated Latin Extended and Vietnamese composites", decisions)
    warning_answer = row_final_answer("Fontspector warning floor", decisions)
    static_answer = row_final_answer("Static TTFs", decisions)
    local_ready = (
        INDEX.exists()
        and len(links) >= 73
        and len(fonts) >= 19
        and not missing_links
        and not missing_fonts
    )
    final_review_ready = all(
        answer not in {
            "Maintainer review required",
            "Accept, revise, or defer",
            "Accept for first review or schedule source cleanup",
            "Keep proof-only unless Google Fonts asks",
            "unknown",
        }
        and not answer.lower().startswith("pending")
        for answer in [proof_answer, composite_answer, warning_answer, static_answer]
    )

    lines = [
        "# Proof Review Readiness",
        "",
        "This generated report checks the local visual proof bundle and keeps the",
        "remaining human review decisions visible for Google Fonts submission.",
        "",
        "## Summary",
        "",
        f"- Proof index exists: {yes_no(INDEX.exists())}",
        f"- Proof review local evidence ready: {yes_no(local_ready)}",
        f"- Proof review final-ready for submission: {yes_no(final_review_ready)}",
        f"- Proof HTML pages linked: {len(links)}",
        f"- Proof fonts linked: {len(fonts)}",
        f"- Missing linked proof pages: {len(missing_links)}",
        f"- Missing linked proof fonts: {len(missing_fonts)}",
        f"- Visual proof final decision recorded: {yes_no(proof_answer != 'Maintainer review required')}",
        f"- Generated composite final decision recorded: {yes_no(composite_answer != 'Accept, revise, or defer' and not composite_answer.lower().startswith('pending'))}",
        f"- Fontspector warning-floor final decision recorded: {yes_no(warning_answer != 'Accept for first review or schedule source cleanup')}",
        f"- Static TTF final decision recorded: {yes_no(static_answer != 'Keep proof-only unless Google Fonts asks')}",
        "",
        "## Review Targets",
        "",
        "- `out/proof/index.html`",
        "- generated Latin Extended review composites",
        "- generated Vietnamese review composites",
        "- `uni01F5` contour-count warning",
        "- G/S/Ccedilla-derived outline alignment warnings",
        "- static TTF proof-only package decision",
        "",
        "## Coverage Evidence",
        "",
        f"- Glyphset report documents generated review glyphs: {yes_no('review glyphs' in glyphset)}",
        f"- Warning worklist points proof review at remaining warning floor: {yes_no('Review `out/proof/index.html`' in warnings)}",
        "",
        "## Open Final Decisions",
        "",
        f"- Visual proof: {proof_answer}",
        f"- Generated Latin Extended and Vietnamese composites: {composite_answer}",
        f"- Fontspector warning floor: {warning_answer}",
        f"- Static TTFs: {static_answer}",
        "",
        "## Finalization",
        "",
        "- Rerun `make proof-legacy` after any source, spacing, glyph, or build-output",
        "  change that affects visual review.",
        "- Record maintainer decisions in",
        "  `documentation/google-fonts-final-decision-sheet.md`, then rerun",
        "  `make release-check` and `make final-readiness-check`.",
        "",
    ]
    if missing_links or missing_fonts:
        lines.extend(["## Missing Links", ""])
        lines.extend(f"- proof page missing: `{link}`" for link in missing_links)
        lines.extend(f"- proof font missing: `{font}`" for font in missing_fonts)
        lines.append("")

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {display_path(OUTPUT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
