#!/usr/bin/env python3
"""Apply maintainer-provided Google Fonts final values.

The checked-in template is intentionally invalid. Copy it, replace every final
value, run this script without --apply to validate, then rerun with --apply.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_VALUES = ROOT / "documentation" / "google-fonts-final-values.template.json"
DEFAULT_METADATA = ROOT / "documentation" / "google-fonts-downstream-metadata-draft.md"
DEFAULT_DECISIONS = ROOT / "documentation" / "google-fonts-final-decision-sheet.md"
DEFAULT_ISSUE = ROOT / "documentation" / "google-fonts-add-font-issue-draft.md"
DEFAULT_HANDOFF = ROOT / "documentation" / "google-fonts-submission-handoff.md"
DEFAULT_OFL = ROOT / "OFL.txt"
DEFAULT_SOURCES = ROOT / "sources"

REQUIRED_KEYS = [
    "date_added",
    "source_commit",
    "repository_url",
    "branch",
    "designer",
    "package_source_strategy",
    "namecheck_result",
    "ai_use_disclosure",
    "authorship_cla_rfn_status",
    "fontspector_warning_decision",
    "visual_proof_decision",
    "generated_composites_decision",
    "static_ttf_decision",
    "release_archive_fallback_decision",
]

PLACEHOLDER_MARKERS = [
    "PENDING",
    "TBD",
    "YYYY",
    "40_CHARACTER",
    "FINAL_",
    "Confirm",
    "Maintainer review",
]

DECISION_LABELS = {
    "Google Fonts `date_added`": "date_added",
    "Final source commit": "source_commit",
    "Public upstream URL": "repository_url",
    "Public default branch": "branch",
    "Family name uniqueness": "namecheck_result",
    "Designer string": "designer",
    "AI-use disclosure": "ai_use_disclosure",
    "Authorship/CLA/RFN status": "authorship_cla_rfn_status",
    "Fontspector warning floor": "fontspector_warning_decision",
    "Visual proof": "visual_proof_decision",
    "Generated Latin Extended and Vietnamese composites": "generated_composites_decision",
    "Static TTFs": "static_ttf_decision",
    "Release/archive fallback": "release_archive_fallback_decision",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--values", type=Path, default=DEFAULT_VALUES)
    parser.add_argument("--metadata", type=Path, default=DEFAULT_METADATA)
    parser.add_argument("--decision-sheet", type=Path, default=DEFAULT_DECISIONS)
    parser.add_argument("--issue-draft", type=Path, default=DEFAULT_ISSUE)
    parser.add_argument("--handoff", type=Path, default=DEFAULT_HANDOFF)
    parser.add_argument("--ofl", type=Path, default=DEFAULT_OFL)
    parser.add_argument("--sources-dir", type=Path, default=DEFAULT_SOURCES)
    parser.add_argument("--apply", action="store_true")
    return parser.parse_args()


def read_values(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("final values file must be a JSON object")
    values: dict[str, str] = {}
    for key, value in data.items():
        if value is None:
            values[key] = ""
        elif isinstance(value, str):
            values[key] = value.strip()
        else:
            raise ValueError(f"{key} must be a string")
    return values


def unresolved(value: str) -> bool:
    return not value or any(marker in value for marker in PLACEHOLDER_MARKERS)


def validate(values: dict[str, str]) -> list[str]:
    problems: list[str] = []
    missing = [key for key in REQUIRED_KEYS if key not in values]
    problems.extend(f"missing required key: {key}" for key in missing)
    extra = sorted(key for key in values if key.startswith("_"))
    problems.extend(f"remove proposal-only key before applying: {key}" for key in extra)
    for key in REQUIRED_KEYS:
        if key in values and unresolved(values[key]):
            problems.append(f"{key} is not final: {values[key]!r}")

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", values.get("date_added", "")):
        problems.append("date_added must be YYYY-MM-DD")
    if not re.fullmatch(r"[0-9a-f]{40}", values.get("source_commit", "")):
        problems.append("source_commit must be a lowercase 40-character git hash")
    if not values.get("repository_url", "").startswith("https://github.com/"):
        problems.append("repository_url must be a public GitHub HTTPS URL")
    branch = values.get("branch", "")
    if (
        not re.fullmatch(r"[A-Za-z0-9._/-]+", branch)
        or branch.startswith(("-", "/", "."))
        or branch.endswith(("/", "."))
    ):
        problems.append("branch must be a simple git branch name")
    if any(part in branch for part in ["..", "//", "@{", "\\"]):
        problems.append("branch must not contain git ref metacharacters")
    if values.get("package_source_strategy") not in {"config_yaml", "archive"}:
        problems.append("package_source_strategy must be config_yaml or archive")
    if values.get("package_source_strategy") == "archive" and not values.get("archive_url", "").startswith("https://"):
        problems.append("archive_url is required for archive source strategy")
    issue_url = values.get("google_fonts_issue_url", "")
    if issue_url and not issue_url.startswith("https://github.com/google/fonts/issues/"):
        problems.append("google_fonts_issue_url must be a google/fonts issue URL when provided")
    if "|" in "\n".join(values.values()):
        problems.append("final values must not contain table pipe characters")
    return problems


def replace_scalar(text: str, key: str, value: str) -> str:
    pattern = rf'(^\s*{re.escape(key)}:\s+)"[^"]*"'
    return re.sub(pattern, rf'\1"{value}"', text, count=1, flags=re.MULTILINE)


def copyright_text(values: dict[str, str]) -> str:
    return f"Copyright 2023 The Blocksyncer Project Authors ({values['repository_url']})"


def source_block(text: str) -> str:
    match = re.search(r"(^source\s+\{\n)(.*?)(^\})", text, flags=re.MULTILINE | re.DOTALL)
    if not match:
        raise ValueError("metadata textproto must contain a source block")
    return match.group(0)


def replace_source_block(text: str, new_block: str) -> str:
    return re.sub(r"(^source\s+\{\n)(.*?)(^\})", new_block, text, count=1, flags=re.MULTILINE | re.DOTALL)


def update_source_strategy(proto: str, values: dict[str, str]) -> str:
    block = source_block(proto)
    block = replace_scalar(block, "repository_url", values["repository_url"])
    block = replace_scalar(block, "commit", values["source_commit"])
    block = replace_scalar(block, "branch", values["branch"])
    block = re.sub(r'^\s*archive_url:\s+"[^"]*"\n', "", block, flags=re.MULTILINE)

    if values["package_source_strategy"] == "config_yaml":
        if "config_yaml:" not in block:
            block = re.sub(
                rf'(^\s*commit:\s+"{re.escape(values["source_commit"])}"\n)',
                rf'\1  config_yaml: "sources/config.yaml"\n',
                block,
                count=1,
                flags=re.MULTILINE,
            )
        else:
            block = replace_scalar(block, "config_yaml", "sources/config.yaml")
    else:
        block = re.sub(r'^\s*config_yaml:\s+"[^"]*"\n', "", block, flags=re.MULTILINE)
        block = re.sub(
            rf'(^\s*commit:\s+"{re.escape(values["source_commit"])}"\n)',
            rf'\1  archive_url: "{values["archive_url"]}"\n',
            block,
            count=1,
            flags=re.MULTILINE,
        )
    return replace_source_block(proto, block)


def update_metadata(text: str, values: dict[str, str]) -> str:
    match = re.search(r"```textproto\n(.*?)\n```", text, flags=re.DOTALL)
    if not match:
        raise ValueError("metadata draft must contain a textproto fenced block")
    proto = match.group(1)
    proto = replace_scalar(proto, "designer", values["designer"])
    proto = replace_scalar(proto, "date_added", values["date_added"])
    proto = replace_scalar(proto, "copyright", copyright_text(values))
    proto = update_source_strategy(proto, values)
    return text[: match.start(1)] + proto + text[match.end(1) :]


def update_ofl(text: str, values: dict[str, str]) -> str:
    lines = text.splitlines()
    if not lines:
        raise ValueError("OFL.txt is empty")
    lines[0] = copyright_text(values)
    return "\n".join(lines) + "\n"


def update_fontinfo(text: str, values: dict[str, str]) -> str:
    updated, count = re.subn(
        r"(<key>copyright</key>\s*<string>)[^<]*(</string>)",
        rf"\1{copyright_text(values)}\2",
        text,
        count=1,
    )
    if count != 1:
        raise ValueError("fontinfo.plist does not contain a copyright string")
    return updated


def ufo_fontinfo_updates(sources_dir: Path, values: dict[str, str]) -> dict[Path, str]:
    updates: dict[Path, str] = {}
    for path in sorted(sources_dir.glob("Blocksync-*.ufo/fontinfo.plist")):
        updates[path] = update_fontinfo(path.read_text(encoding="utf-8"), values)
    if not updates:
        raise ValueError(f"no active Blocksync UFO fontinfo.plist files found in {sources_dir}")
    return updates


def table_answer(values: dict[str, str], label: str) -> str:
    if label == "Package source strategy":
        if values["package_source_strategy"] == "config_yaml":
            return 'Use `source.config_yaml: "sources/config.yaml"`'
        return f'Use release/archive package: {values["archive_url"]}'
    return values[DECISION_LABELS[label]]


def update_decisions(text: str, values: dict[str, str]) -> str:
    labels = set(DECISION_LABELS) | {"Package source strategy"}
    lines: list[str] = []
    for line in text.splitlines():
        replaced = False
        if line.startswith("| "):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if cells and cells[0] in labels and len(cells) >= 3:
                cells[2] = table_answer(values, cells[0])
                line = "| " + " | ".join(cells) + " |"
                replaced = True
        lines.append(line if replaced else line)
    return "\n".join(lines) + "\n"


def update_issue(text: str, values: dict[str, str]) -> str:
    text = re.sub(r"https://github\.com/eliheuer/blocksync(?:er)?(?=[/)\s`]|$)", lambda _: values["repository_url"], text)
    text = text.replace(
        "This draft is not ready to paste until the final source commit, metadata date,\nand remaining QA warnings are reviewed.",
        "This draft has final maintainer values applied. Rerun `make final-readiness-check` before pasting.",
    )
    replacements = {
        "Draft status: local OFL and source path are in place; public upstream URL\n    still needs final confirmation.": f"Final status: public upstream URL confirmed: {values['repository_url']}.",
        "Draft status: `AUTHORS.txt` and `CONTRIBUTORS.txt` list Eli Heuer; final\n    AI-use disclosure still needs maintainer confirmation.": f"Final status: designer string `{values['designer']}` confirmed. {values['authorship_cla_rfn_status']}; AI-use disclosure: {values['ai_use_disclosure']}.",
        "Draft status: needs final browser check.": f"Final status: {values['namecheck_result']}.",
        "Draft status: `namecheck.fontdata.com` API clear on 2026-05-30; refresh\n    if this issue is opened later.": f"Final status: {values['namecheck_result']}.",
        "Draft status: remaining WARNs and package metadata placeholders must be\n    reviewed before opening.": f"Final status: {values['fontspector_warning_decision']}.",
        "Draft status: maintainer confirmation required.": f"Final status: {values['authorship_cla_rfn_status']}.",
        "Replace pending values in\n  `documentation/google-fonts-downstream-metadata-draft.md`.": "Confirm final values applied in\n  `documentation/google-fonts-downstream-metadata-draft.md`.",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    disclosure = (
        f"**AI-use disclosure**\n\nThe designer string `{values['designer']}` is confirmed. "
        f"{values['authorship_cla_rfn_status']}\n\nAI-use disclosure: {values['ai_use_disclosure']}\n\n"
    )
    text = re.sub(r"^\*\*AI-use disclosure(?: proposed for maintainer review)?\*\*\n.*?(?=^\*\*)",
                  lambda _: disclosure, text, count=1, flags=re.MULTILINE | re.DOTALL)
    return text


def update_handoff(text: str, values: dict[str, str]) -> str:
    text = re.sub(r"https://github\.com/eliheuer/blocksync(?:er)?(?=[/)\s`]|$)", lambda _: values["repository_url"], text)
    issue_url = values.get("google_fonts_issue_url", "")
    if issue_url:
        text = re.sub(
            r"^- Google Fonts issue: .+$",
            f"- Google Fonts issue exists: {issue_url}",
            text,
            count=1,
            flags=re.MULTILINE,
        )
    marker = "## Draft Add Font Issue"
    record = "\n".join(
        [
            "## Applied Final Values",
            "",
            f"- Final source commit: `{values['source_commit']}`",
            f"- Final `date_added`: `{values['date_added']}`",
            f"- Public upstream URL: `{values['repository_url']}`",
            f"- Public branch: `{values['branch']}`",
            f"- Namecheck: {values['namecheck_result']}",
            f"- AI-use disclosure: {values['ai_use_disclosure']}",
            f"- Proof decision: {values['visual_proof_decision']}",
            f"- Fontspector warning decision: {values['fontspector_warning_decision']}",
            f"- Google Fonts issue: {issue_url if issue_url else 'pending'}",
            "",
        ]
    )
    if "## Applied Final Values" in text:
        text = re.sub(r"## Applied Final Values\n.*?(?=^## )", record, text, count=1, flags=re.MULTILINE | re.DOTALL)
    elif marker in text:
        text = text.replace(marker, record + marker, 1)
    return text


def write_if_apply(path: Path, text: str, apply: bool) -> None:
    if apply:
        path.write_text(text, encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}")


def main() -> int:
    args = parse_args()
    try:
        values = read_values(args.values)
        problems = validate(values)
    except Exception as error:
        print(f"Final values validation failed: {error}", file=sys.stderr)
        return 2

    if problems:
        print("Final values are not ready to apply:", file=sys.stderr)
        for problem in problems:
            print(f"- {problem}", file=sys.stderr)
        return 2

    updates = {
        args.metadata: update_metadata(args.metadata.read_text(encoding="utf-8"), values),
        args.decision_sheet: update_decisions(args.decision_sheet.read_text(encoding="utf-8"), values),
        args.issue_draft: update_issue(args.issue_draft.read_text(encoding="utf-8"), values),
        args.handoff: update_handoff(args.handoff.read_text(encoding="utf-8"), values),
        args.ofl: update_ofl(args.ofl.read_text(encoding="utf-8"), values),
    }
    updates.update(ufo_fontinfo_updates(args.sources_dir, values))

    if args.apply:
        for path, text in updates.items():
            write_if_apply(path, text, True)
        print("Final values applied.")
    else:
        for path in updates:
            print(f"Would update {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}")
        print("Final values validated. Rerun with --apply to write changes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
