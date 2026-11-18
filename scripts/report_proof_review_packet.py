#!/usr/bin/env python3
"""Generate a maintainer-facing proof and warning review packet."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "documentation" / "proof-review-packet.md"
PROOF_INDEX = ROOT / "out" / "proof" / "index.html"
PROOF_READINESS = ROOT / "documentation" / "proof-review-readiness.md"
WARNINGS = ROOT / "documentation" / "fontspector-zero-warning-worklist.md"
DECISIONS = ROOT / "documentation" / "google-fonts-final-decision-sheet.md"
FINAL_VALUES_PACKET = ROOT / "documentation" / "google-fonts-final-values-packet.md"


REVIEW_ROWS = [
    "Visual proof",
    "Generated Latin Extended and Vietnamese composites",
    "Fontspector warning floor",
    "Static TTFs",
]


WARNING_SECTIONS = [
    "Metadata Reachability",
    "Contour Count",
    "Outline Alignment",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def summary_value(label: str, text: str, default: str = "unknown") -> str:
    match = re.search(rf"^- {re.escape(label)}: (.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else default


def html_links(index_text: str) -> list[str]:
    return re.findall(r'<a href="([^"]+\.html)">([^<]+)</a>', index_text)


def font_links(index_text: str) -> list[str]:
    return re.findall(r'<a href="([^"]+\.ttf)">', index_text)


def decision_answer(label: str, text: str) -> str:
    for line in text.splitlines():
        if not line.startswith(f"| {label} |"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        return cells[2] if len(cells) >= 3 else "unknown"
    return "unknown"


def section_body(heading: str, text: str) -> str:
    match = re.search(
        rf"^### {re.escape(heading)}\n(?P<body>.*?)(?=^### |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    return match.group("body").strip() if match else ""


def bullet_items(text: str) -> list[str]:
    return [line[2:].strip() for line in text.splitlines() if line.startswith("- ")]


def main() -> int:
    proof_index = read(PROOF_INDEX)
    proof_readiness = read(PROOF_READINESS)
    warnings = read(WARNINGS)
    decisions = read(DECISIONS)
    final_values = read(FINAL_VALUES_PACKET)
    proof_links = html_links(proof_index)
    proof_fonts = font_links(proof_index)
    proof_ready = "Proof review local evidence ready: yes" in proof_readiness
    packet_ready = bool(proof_links and proof_fonts and proof_ready)

    by_kind: dict[str, list[tuple[str, str]]] = {}
    for href, label in proof_links:
        kind = label.rsplit(" ", 1)[-1]
        by_kind.setdefault(kind, []).append((href, label))

    lines = [
        "# Proof Review Packet",
        "",
        "This generated packet turns the proof output and remaining Fontspector",
        "warnings into a short maintainer review queue. It does not accept or",
        "reject any review item on the maintainer's behalf.",
        "",
        "## Summary",
        "",
        f"- Proof review packet ready: {yes_no(packet_ready)}",
        f"- Proof index: `{PROOF_INDEX.relative_to(ROOT)}`",
        f"- Proof HTML pages linked: {len(proof_links)}",
        f"- Proof fonts linked: {len(proof_fonts)}",
        f"- Proof review local evidence ready: {summary_value('Proof review local evidence ready', proof_readiness)}",
        f"- Proof review final-ready for submission: {summary_value('Proof review final-ready for submission', proof_readiness)}",
        f"- Final values packet ready: {summary_value('Final values packet ready', final_values)}",
        f"- Remaining warning floor: {summary_value('Package-context warning checks', warnings)}",
        "",
        "## Review Decisions To Record",
        "",
        "| Decision row | Current final answer | Final values key |",
        "| --- | --- | --- |",
        f"| Visual proof | {decision_answer('Visual proof', decisions)} | `visual_proof_decision` |",
        f"| Generated Latin Extended and Vietnamese composites | {decision_answer('Generated Latin Extended and Vietnamese composites', decisions)} | `generated_composites_decision` |",
        f"| Fontspector warning floor | {decision_answer('Fontspector warning floor', decisions)} | `fontspector_warning_decision` |",
        f"| Static TTFs | {decision_answer('Static TTFs', decisions)} | `static_ttf_decision` |",
        "",
        "## Proof Pages By Kind",
        "",
        "| Kind | Count | First pages |",
        "| --- | ---: | --- |",
    ]
    for kind in sorted(by_kind):
        pages = by_kind[kind]
        examples = ", ".join(f"`out/proof/{href}`" for href, _label in pages[:3])
        lines.append(f"| {kind} | {len(pages)} | {examples} |")

    lines.extend(["", "## Warning Review Items", ""])
    for heading in WARNING_SECTIONS:
        body = section_body(heading, warnings)
        items = bullet_items(body)
        lines.extend([f"### {heading}", ""])
        if items:
            for item in items[:20]:
                lines.append(f"- {item}")
            if len(items) > 20:
                lines.append(f"- ... {len(items) - 20} more item(s) in `documentation/fontspector-zero-warning-worklist.md`")
        else:
            paragraph = " ".join(line.strip() for line in body.splitlines() if line.strip())
            lines.append(f"- {paragraph or 'No current item found.'}")
        lines.append("")

    lines.extend(
        [
            "## Suggested Review Flow",
            "",
            "1. Open `out/proof/index.html` and scan glyphs, text, proofer, and",
            "   waterfall pages across normal, condensed, and expanded instances.",
            "2. Compare generated Latin Extended and Vietnamese composites against",
            "   base glyph rhythm and mark placement.",
            "3. Inspect `uni01F5`, G/S/Ccedilla families, and section-sign pages",
            "   while reviewing the remaining contour/alignment WARNs.",
            "4. Record final decisions in a filled copy of",
            "   `documentation/google-fonts-final-values.template.json`.",
            "5. Validate with `make final-values-check VALUES=/path/to/final-values.json`",
            "   before applying.",
            "",
        ]
    )

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    return 0 if packet_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
