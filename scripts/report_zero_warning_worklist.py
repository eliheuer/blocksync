#!/usr/bin/env python3
"""Write the Blocksync Fontspector zero-warning worklist."""

from __future__ import annotations

import math
import re
import unicodedata
from pathlib import Path

from fontTools.ttLib import TTFont
from gfsubsets import CodepointsInSubset

from check_final_readiness import fontspector_counts


ROOT = Path(__file__).resolve().parents[1]
FONT = ROOT / "fonts" / "variable" / "Blocksync[wdth,wght].ttf"
OUTPUT = ROOT / "documentation" / "fontspector-zero-warning-worklist.md"
PACKAGE_REPORT = ROOT / "out" / "fontspector" / "fontspector-package-context-report.md"
VARIABLE_REPORT = ROOT / "out" / "fontspector" / "fontspector-report.md"
IGNORED = {0x0000, 0x000D, 0x0020, 0x00A0}
SUBSET_THRESHOLDS = {
    "latin-ext": 20,
    "vietnamese": 50,
}


def report_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def summary_counts(text: str) -> tuple[int, int, int, int, int]:
    counts = fontspector_counts(text)
    return tuple(counts[key] for key in ("FAIL", "WARN", "INFO", "PASS", "SKIP"))


def check_ids(text: str) -> dict[str, int]:
    ids = re.findall(r"<summary>[^<]*<b>WARN</b>[^<]*?\(([^()]+)\)</summary>", text)
    result: dict[str, int] = {}
    for check_id in ids:
        result[check_id] = result.get(check_id, 0) + 1
    return result


def font_codepoints() -> set[int]:
    font = TTFont(FONT)
    codepoints = set(font.getBestCmap() or {}) - IGNORED
    font.close()
    return codepoints


def threshold_row(subset: str, present: set[int]) -> str:
    codepoints = set(CodepointsInSubset(subset, unique_glyphs=True))
    covered = len(codepoints & present)
    required = math.floor(len(codepoints) * SUBSET_THRESHOLDS[subset] / 100) + 1
    coverage = 100 * covered / len(codepoints)
    return "| `{}` | {}% | {} | {} | {} | {:.2f}% | {} |".format(
        subset,
        SUBSET_THRESHOLDS[subset],
        len(codepoints),
        covered,
        required,
        coverage,
        "yes" if covered >= required else "no",
    )


def codepoint_label(codepoint: int) -> str:
    try:
        name = unicodedata.name(chr(codepoint))
    except ValueError:
        name = "UNNAMED"
    return f"`U+{codepoint:04X} {name}`"


def unreachable_codepoints(text: str) -> list[int]:
    return sorted({int(value, 16) for value in re.findall(r"\* U\+([0-9A-F]{4,6}) ", text)})


def outline_alignment_items(text: str) -> list[str]:
    return [
        item.replace(" [code: found-misalignments]", "")
        for item in re.findall(r"^\* - (.+)$", text, flags=re.MULTILINE)
    ]


def markdown() -> str:
    variable = report_text(VARIABLE_REPORT)
    package = report_text(PACKAGE_REPORT)
    present = font_codepoints() if FONT.exists() else set()
    variable_summary = summary_counts(variable)
    package_summary = summary_counts(package)
    package_checks = check_ids(package)
    unreachable = unreachable_codepoints(package)
    outline_items = outline_alignment_items(package)
    package_warning_line = (
        ", ".join(f"`{check}`: {count}" for check, count in package_checks.items())
        if package_checks
        else "none"
    )
    sidebearing_warning_present = "suspicious_sidebearings" in package_checks

    return "\n".join(
        [
            "# Fontspector Zero-Warning Worklist",
            "",
            f"Font: `{FONT.relative_to(ROOT)}`",
            "",
            "This report records the remaining warning floor in both checked profiles.",
            "It is a worklist for real cleanup and reviewer decisions, not",
            "a recommendation to hide supported codepoints or narrow the package",
            "scope just to reduce warning count.",
            "",
            "## Current Warning Floor",
            "",
            "- Honest zero-warning state possible with current scope: no",
            "- Release variable Fontspector summary: "
            f"{variable_summary[0]} FAIL, {variable_summary[1]} WARN, {variable_summary[2]} INFO, "
            f"{variable_summary[3]} PASS, {variable_summary[4]} SKIP",
            "- Package-context Fontspector summary: "
            f"{package_summary[0]} FAIL, {package_summary[1]} WARN, {package_summary[2]} INFO, "
            f"{package_summary[3]} PASS, {package_summary[4]} SKIP",
            "- Package-context warning checks: " + package_warning_line,
            "",
            "## Zero-Warning Verdict",
            "",
            "True zero is not a final-polish toggle. It requires either source",
            "drawing cleanup or Google Fonts reviewer acceptance for the remaining",
            "metadata reachability, contour-count, and outline warnings. The",
            "current package scope is honest: `latin`, `latin-ext`, `menu`, and",
            "`vietnamese` all pass the local release gate, and the broad",
            "`latin-ext`/`vietnamese` subset",
            "thresholds clear locally.",
            "",
            "## Subset Threshold Math",
            "",
            "| Subset | Threshold | Subset codepoints | Present | Present needed | Coverage | Threshold met |",
            "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
            *(threshold_row(subset, present) for subset in SUBSET_THRESHOLDS),
            "",
            "## Remaining Warning Buckets",
            "",
            "### Metadata Reachability",
            "",
            "The font intentionally keeps support marks and compatibility codepoints",
            "that are useful for composition and proofing, but Google Fonts serving",
            "subsets do not cover all of them. Do not delete these codepoints only",
            "to silence `unreachable_subsetting`; review the final metadata strategy",
            "with Google Fonts if needed.",
            "",
            "A source-unencoding probe of these support marks was rejected: it",
            "caused Google Fonts `glyph_coverage`, `dotted_circle`,",
            "`shape_languages`, and `unreachable_glyphs` regressions. Keep the",
            "codepoints unless Google Fonts explicitly asks for a different",
            "package strategy.",
            "",
            "Current package-context list:",
            "",
            *(f"- {codepoint_label(codepoint)}" for codepoint in unreachable),
            "",
            "### Contour Count",
            "",
            "- `uni01F5` (U+01F5 LATIN SMALL LETTER G WITH ACUTE) is component-based",
            "  and currently has 2 contours where Fontspector expects 3-5. Review",
            "  whether this should be accepted for Blocksync's construction or redrawn.",
            "",
            *(
                [
                    "### Suspicious Sidebearings",
                    "",
                    "- Spacing marks still need sidebearing review before changing metrics",
                    "  mechanically.",
                    "",
                ]
                if sidebearing_warning_present
                else []
            ),
            "### Outline Alignment",
            "",
            "- Remaining alignment warnings are G/S/Ccedilla-derived implied curve",
            "  points and scaled `section` components. Treat them as visual-review",
            "  items before snapping overshoots to the grid.",
            "",
            "Current package-context list:",
            "",
            *(f"- {item}" for item in outline_items),
            "",
            *(
                []
                if sidebearing_warning_present
                else [
                    "## Cleared Warning Buckets",
                    "",
                    "- `suspicious_sidebearings` is no longer present in the package-context",
                    "  Fontspector report after spacing mark and trademark metric cleanup.",
                    "",
                ]
            ),
            "## Fastest Honest Next Step",
            "",
            "Review `out/proof/index.html`, then either accept the current warning",
            "floor for first Google Fonts review or make deliberate source edits for",
            "`uni01F5`, metadata reachability, and the remaining implied-curve",
            "alignment warnings. Rerun `make release-check` and this report after",
            "any source or metadata change.",
            "",
        ]
    )


def main() -> int:
    OUTPUT.write_text(markdown(), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
