#!/usr/bin/env python3
"""Regression tests for agent porting manifest generation."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "report_agent_porting_manifest.py"
SCRIPTS = ROOT / "scripts"


def load_module():
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location(
        "report_agent_porting_manifest_for_test",
        SCRIPT,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {SCRIPT.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def create_path(root: Path, relpath: str) -> None:
    path = root / relpath.rstrip("/")
    if relpath.endswith("/"):
        path.mkdir(parents=True, exist_ok=True)
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("placeholder\n", encoding="utf-8")


def main() -> int:
    module = load_module()
    with tempfile.TemporaryDirectory(prefix="blocksync-porting-manifest.") as tmp:
        work = Path(tmp)
        module.ROOT = work
        module.OUTPUT = work / "documentation" / "manifest.md"
        all_paths = module.COPY_FIRST + module.REUSABLE_HELPERS + module.TEST_HELPERS
        for relpath in all_paths:
            create_path(work, relpath)

        module.main()
        text = module.OUTPUT.read_text(encoding="utf-8")
        total = len(all_paths)
        checks = {
            "ready": "- Porting manifest ready: yes" in text,
            "count": f"- Portable files present: {total} / {total}" in text,
            "source policy": "designspace/UFO active sources, archived `.glyphs` snapshots" in text,
            "copy entry": "- `.agents/`: yes" in text,
            "self test entry": "- `scripts/test_agent_porting_manifest.py`: yes" in text,
            "replace guidance": "Family name, package directory" in text,
            "regenerate command": "make agent-porting-manifest" in text,
            "no stale evidence": "Do not carry over Blocksync-generated release reports" in text,
        }
        failed = [name for name, ok in checks.items() if not ok]
        if failed:
            print("Failed ready checks:")
            for name in failed:
                print(f"- {name}")
            print(text)
            return 1

        missing = work / "scripts" / "report_source_readiness.py"
        missing.unlink()
        module.main()
        missing_text = module.OUTPUT.read_text(encoding="utf-8")
        missing_checks = {
            "not ready": "- Porting manifest ready: no" in missing_text,
            "missing count": f"- Portable files present: {total - 1} / {total}" in missing_text,
            "missing row": "- `scripts/report_source_readiness.py`: no" in missing_text,
        }
        failed = [name for name, ok in missing_checks.items() if not ok]
        if failed:
            print("Failed missing-file checks:")
            for name in failed:
                print(f"- {name}")
            print(missing_text)
            return 1

    print("Agent porting manifest tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
