#!/usr/bin/env python3
"""Regression tests for maintainer decision request generation."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "report_maintainer_decision_request.py"
SCRIPTS = ROOT / "scripts"


def load_module():
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location(
        "report_maintainer_decision_request_for_test",
        SCRIPT,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {SCRIPT.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def extract_json(text: str) -> dict[str, str]:
    match = re.search(r"```json\n(?P<body>.*?)\n```", text, flags=re.DOTALL)
    if not match:
        raise AssertionError("request did not contain a JSON code block")
    return json.loads(match.group("body"))


def main() -> int:
    module = load_module()
    with tempfile.TemporaryDirectory(prefix="blocksync-maintainer-request.") as tmp:
        work = Path(tmp)
        proposal = work / "proposal.json"
        values = {
            "_note": "proposal only",
            "date_added": "",
            "source_commit": "",
            "repository_url": "https://github.com/eliheuer/blocksyncer",
            "branch": "main",
            "designer": "Eli Heuer",
            "package_source_strategy": "config_yaml",
            "archive_url": "",
            "namecheck_result": "namecheck clear",
            "ai_use_disclosure": "",
            "authorship_cla_rfn_status": "local authorship evidence ready",
            "fontspector_warning_decision": "",
            "visual_proof_decision": "",
            "generated_composites_decision": "",
            "static_ttf_decision": "proof-only",
            "release_archive_fallback_decision": "config_yaml first",
            "google_fonts_issue_url": "",
            "_review_context": "proposal only",
        }
        proposal.write_text(json.dumps(values, indent=2) + "\n", encoding="utf-8")

        module.PROPOSAL = proposal
        module.PACKET = write(work / "packet.md", "- Final values packet ready: yes\n")
        module.PLACEHOLDERS = write(work / "placeholders.md", "- Public placeholder blocker count: 17\n")
        module.WARNINGS = write(work / "warnings.md", "- Package-context warning checks: `contour_count`: 1\n")
        module.FINAL_READINESS = write(
            work / "final-readiness.md",
            "## Blocking Items\n\n- fallback blocker\n",
        )
        module.OUTPUT = work / "request.md"
        module.blocker_lines = lambda: [
            "metadata `date_added` is still `PENDING-YYYY-MM-DD`",
            "AI-use disclosure is still pending maintainer answer",
        ]

        module.main()
        text = module.OUTPUT.read_text(encoding="utf-8")
        json_block = extract_json(text)
        checks = {
            "ready": "- Maintainer decision request ready: yes" in text,
            "placeholder count": "- Public placeholder blocker count: 17" in text,
            "warning floor": "- Remaining Fontspector warning floor: `contour_count`: 1" in text,
            "required blank needs answer": "| `date_added` |  | yes |" in text,
            "optional blank conditional": "| `archive_url` |  | conditional |" in text,
            "live blockers": "AI-use disclosure is still pending maintainer answer" in text,
            "proposal key omitted": "_note" not in json_block and "_review_context" not in json_block,
            "required key kept": json_block.get("repository_url") == "https://github.com/eliheuer/blocksyncer",
            "optional key kept": "google_fonts_issue_url" in json_block,
        }
        failed = [name for name, ok in checks.items() if not ok]
        if failed:
            print("Failed checks:")
            for name in failed:
                print(f"- {name}")
            print(text)
            return 1

    print("Maintainer decision request tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
