#!/usr/bin/env python3
"""Regression tests for final-values packet generation."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "report_final_values_packet.py"
SCRIPTS = ROOT / "scripts"


def load_module():
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location("report_final_values_packet_for_test", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {SCRIPT.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def render(module, work: Path, template: Path, decisions: Path, next_actions: Path) -> str:
    module.TEMPLATE = template
    module.DECISIONS = decisions
    module.NEXT_ACTIONS = next_actions
    module.OUTPUT = work / "packet.md"
    module.main()
    return module.OUTPUT.read_text(encoding="utf-8")


def main() -> int:
    module = load_module()
    with tempfile.TemporaryDirectory(prefix="blocksync-final-values-packet.") as tmp:
        work = Path(tmp)
        template = work / "values.json"
        decisions = work / "decisions.md"
        next_actions = write(
            work / "next-actions.md",
            "## Maintainer Decisions\n\n| Blocker | Next action |\n| --- | --- |\n| metadata `date_added` is still `PENDING-YYYY-MM-DD` | Choose final date. |\n",
        )
        shutil.copyfile(ROOT / "documentation" / "google-fonts-final-values.template.json", template)
        shutil.copyfile(ROOT / "documentation" / "google-fonts-final-decision-sheet.md", decisions)

        text = render(module, work, template, decisions, next_actions)
        checks = {
            "ready": "- Final values packet ready: yes" in text,
            "mapped rows": "- Decision rows mapped to JSON keys: 14 / 14" in text,
            "required keys": "- Required JSON keys present in template: 14 / 14" in text,
            "no issues": "## Template Coverage Issues\n\n- none" in text,
            "blocker included": "metadata `date_added` is still `PENDING-YYYY-MM-DD`" in text,
        }
        failed = [name for name, ok in checks.items() if not ok]
        if failed:
            print("Failed checks:")
            for name in failed:
                print(f"- {name}")
            print(text)
            return 1

        drift_decisions = work / "decisions-drift.md"
        drift_decisions.write_text(
            decisions.read_text(encoding="utf-8").replace(
                "| Release/archive fallback |",
                "| Reviewer-only extra decision | current | pending |\n| Release/archive fallback |",
                1,
            ),
            encoding="utf-8",
        )
        drift_text = render(module, work, template, drift_decisions, next_actions)
        if "- Final values packet ready: no" not in drift_text or "unmapped decision row: Reviewer-only extra decision" not in drift_text:
            print("Expected unmapped decision row to block packet readiness")
            print(drift_text)
            return 1

        extra_template = work / "values-extra.json"
        values = json.loads(template.read_text(encoding="utf-8"))
        values["unexpected_key"] = "value"
        extra_template.write_text(json.dumps(values, indent=2) + "\n", encoding="utf-8")
        extra_text = render(module, work, extra_template, decisions, next_actions)
        if "- Final values packet ready: no" not in extra_text or "unknown template key: `unexpected_key`" not in extra_text:
            print("Expected unknown template key to block packet readiness")
            print(extra_text)
            return 1

    print("Final values packet tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
