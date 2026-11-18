#!/usr/bin/env python3
"""Regression tests for scripts/apply_final_values.py."""

from __future__ import annotations

import json
import importlib.util
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "apply_final_values.py"
FINAL_READINESS = ROOT / "scripts" / "check_final_readiness.py"
DOWNSTREAM_READINESS = ROOT / "scripts" / "report_downstream_pr_readiness.py"
DOWNSTREAM_PR_DRAFT = ROOT / "scripts" / "report_downstream_pr_draft.py"
AUTHORSHIP_READINESS = ROOT / "scripts" / "report_authorship_disclosure_readiness.py"
PROOF_READINESS = ROOT / "scripts" / "report_proof_review_readiness.py"


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def assert_final_readiness_uses_applied_answers(work: Path, metadata: Path, decisions: Path) -> None:
    module = load_module(FINAL_READINESS, "check_final_readiness_for_test")
    summary = "Summary: SKIP: 0 INFO: 0 PASS: 1 WARN: 3 FAIL: 0 FATAL: 0 ERROR: 0\n"

    module.METADATA = metadata
    module.DECISIONS = decisions
    module.WARNINGS = write(work / "warnings.md", "- Honest zero-warning state possible with current scope: no\n")
    module.BLOCKERS = write(work / "blockers.md", "# Blockers\n")
    module.RELEASE_METADATA_READINESS = write(work / "release-metadata.md", "- Release metadata local evidence ready: yes\n")
    module.SOURCE_READINESS = write(work / "source.md", "- Source-ready for Google Fonts build path: yes\n")
    module.FAMILY_NAME_READINESS = write(work / "family.md", "- Family name local evidence ready: yes\n")
    module.AUTHORSHIP_DISCLOSURE_READINESS = write(work / "authorship.md", "- Local authorship/disclosure evidence ready: yes\n")
    module.PACKAGER_SOURCE_STRATEGY = write(work / "strategy.md", "- Package source strategy local evidence ready: yes\n")
    module.PROOF_REVIEW_READINESS = write(work / "proof-review.md", "- Proof review local evidence ready: yes\n")
    module.RELEASE_REPORT = write(work / "release-report.md", summary)
    module.PACKAGE_REPORT = write(work / "package-report.md", summary)
    module.ARCHIVE_MANIFEST = write(
        work / "archive.md",
        "- Local release archive hashes match source files: yes\n- Final GitHub release archive URL recorded: pending\n",
    )
    module.PACKAGER_READINESS = write(work / "packager.md", "- Ready to run final no-PR Packager dry run: yes\n")
    module.PACKAGER_DRY_RUN_RECORD = write(work / "packager-record.md", "- Final no-PR Packager dry run recorded: yes\n")
    module.DOWNSTREAM_PR_READINESS = write(work / "downstream.md", "- Ready to open downstream PR: yes\n")
    module.AGENT_REUSE_READINESS = write(work / "agent.md", "- Reusable agent bundle ready: yes\n")
    module.PLACEHOLDER_AUDIT = write(work / "placeholders.md", "- Public placeholder blocker count: 0\n")
    module.DECISION_APPLICATION = write(work / "decision-application.md", "- Decision rows tracked: 14\n")
    module.PROOF_INDEX = write(work / "proof-index.html", "<!doctype html>\n")
    module.OFL = write(
        work / "OFL.txt",
        "Copyright 2023 The Blocksyncer Project Authors (https://github.com/example/blocksync-final)\n",
    )
    fontinfo_dir = work / "sources" / "Blocksync-Regular.ufo"
    fontinfo_dir.mkdir(parents=True, exist_ok=True)
    module.SOURCES = work / "sources"
    write(
        fontinfo_dir / "fontinfo.plist",
        "<plist><dict><key>copyright</key><string>Copyright 2023 The Blocksyncer Project Authors (https://github.com/example/blocksync-final)</string></dict></plist>\n",
    )

    blockers = module.blocker_lines()
    if blockers:
        raise AssertionError("Expected applied final answers to clear synthetic final readiness blockers:\n- " + "\n- ".join(blockers))

    mismatched_metadata = work / "metadata-designer-mismatch.md"
    mismatched_metadata.write_text(
        metadata.read_text(encoding="utf-8").replace('designer: "Example Designer"', 'designer: "Wrong Designer"'),
        encoding="utf-8",
    )
    module.METADATA = mismatched_metadata
    mismatch_blockers = module.blocker_lines()
    if "metadata designer does not match final decision sheet" not in mismatch_blockers:
        raise AssertionError("Expected mismatched metadata designer to block final readiness:\n- " + "\n- ".join(mismatch_blockers))
    module.METADATA = metadata

    module.OFL.write_text(
        "Copyright 2023 The Blocksyncer Project Authors (https://github.com/example/stale)\n",
        encoding="utf-8",
    )
    stale_blockers = module.blocker_lines()
    if "OFL.txt copyright does not match final repository_url" not in stale_blockers:
        raise AssertionError("Expected stale OFL copyright to block final readiness:\n- " + "\n- ".join(stale_blockers))
    module.OFL.write_text(
        "Copyright 2023 The Blocksyncer Project Authors (https://github.com/example/blocksync-final)\n",
        encoding="utf-8",
    )

    archive_metadata = work / "metadata-source-mismatch.md"
    archive_metadata.write_text(
        re.sub(
            r'^\s*config_yaml:\s+"sources/config.yaml"\n',
            '  archive_url: "https://github.com/example/blocksync/releases/download/v1.0.0/Blocksync-GF-review.zip"\n',
            metadata.read_text(encoding="utf-8"),
            flags=re.MULTILINE,
        ),
        encoding="utf-8",
    )
    module.METADATA = archive_metadata
    strategy_blockers = module.blocker_lines()
    if "metadata source strategy does not match final decision sheet" not in strategy_blockers:
        raise AssertionError("Expected mismatched metadata source strategy to block final readiness:\n- " + "\n- ".join(strategy_blockers))
    module.METADATA = metadata


def assert_dependent_reports_use_applied_answers(work: Path, decisions: Path, issue: Path) -> None:
    authorship = load_module(AUTHORSHIP_READINESS, "authorship_readiness_for_test")
    authorship.DECISIONS = decisions
    authorship.ISSUE_DRAFT = issue
    authorship.OUTPUT = work / "authorship-readiness.md"
    authorship.main()
    authorship_text = authorship.OUTPUT.read_text(encoding="utf-8")
    if "Authorship/disclosure final-ready for submission: yes" not in authorship_text:
        raise AssertionError(authorship_text)

    proof_dir = work / "proof"
    proof_dir.mkdir()
    html_links = []
    font_links = []
    for index in range(73):
        name = f"proof-{index}.html"
        html_links.append(name)
        (proof_dir / name).write_text("<!doctype html>\n", encoding="utf-8")
    for index in range(19):
        name = f"font-{index}.ttf"
        font_links.append(name)
        (proof_dir / name).write_text("fake font\n", encoding="utf-8")
    index_html = "\n".join(
        [*(f'<a href="{name}">{name}</a>' for name in html_links), *(f'<a href="{name}">{name}</a>' for name in font_links)]
    )
    (proof_dir / "index.html").write_text(index_html, encoding="utf-8")

    proof = load_module(PROOF_READINESS, "proof_readiness_for_test")
    proof.DECISIONS = decisions
    proof.PROOF_DIR = proof_dir
    proof.INDEX = proof_dir / "index.html"
    proof.GLYPHSET_COVERAGE = write(work / "glyphset.md", "review glyphs\n")
    proof.WARNINGS = write(work / "warnings.md", "Review `out/proof/index.html`\n")
    proof.OUTPUT = work / "proof-readiness.md"
    proof.main()
    proof_text = proof.OUTPUT.read_text(encoding="utf-8")
    if "Proof review final-ready for submission: yes" not in proof_text:
        raise AssertionError(proof_text)


def assert_downstream_readiness_sees_issue(work: Path, metadata: Path, handoff: Path) -> None:
    gf_repo = work / "fonts"
    subprocess.run(["git", "init", "-q", "-b", "main", str(gf_repo)], check=True)
    subprocess.run(["git", "-C", str(gf_repo), "remote", "add", "origin", "git@github.com:eliheuer/fonts.git"], check=True)
    subprocess.run(["git", "-C", str(gf_repo), "remote", "add", "upstream", "https://github.com/google/fonts.git"], check=True)
    (gf_repo / "ofl" / "blocksync").mkdir(parents=True)
    (gf_repo / "ofl" / "blocksync" / ".keep").write_text("", encoding="utf-8")
    subprocess.run(["git", "-C", str(gf_repo), "add", "ofl/blocksync/.keep"], check=True)
    subprocess.run(
        [
            "git",
            "-C",
            str(gf_repo),
            "-c",
            "user.name=Blocksync Test",
            "-c",
            "user.email=blocksync-test@example.com",
            "commit",
            "-q",
            "-m",
            "initial",
        ],
        check=True,
    )

    output = work / "downstream.md"
    pr_draft = work / "pr-draft.md"
    draft_result = run([
        "env",
        f"DOWNSTREAM_METADATA_PATH={metadata}",
        f"SUBMISSION_HANDOFF_PATH={handoff}",
        f"DOWNSTREAM_PR_DRAFT_OUTPUT={pr_draft}",
        sys.executable,
        str(DOWNSTREAM_PR_DRAFT),
    ])
    if draft_result.returncode != 0:
        raise AssertionError(draft_result.stdout)
    packager = write(work / "packager-ready.md", "- Ready to run final no-PR Packager dry run: yes\n")
    record = write(work / "packager-record.md", "- Final no-PR Packager dry run recorded: yes\n")
    result = run([
        "env",
        f"GF_REPO_PATH={gf_repo}",
        f"GF_CLEAN_REPO_PATH={gf_repo}",
        f"DOWNSTREAM_METADATA_PATH={metadata}",
        f"SUBMISSION_HANDOFF_PATH={handoff}",
        f"PACKAGER_READINESS_PATH={packager}",
        f"PACKAGER_RECORD_PATH={record}",
        f"DOWNSTREAM_PR_DRAFT_PATH={pr_draft}",
        f"DOWNSTREAM_PR_READINESS_OUTPUT={output}",
        sys.executable,
        str(DOWNSTREAM_READINESS),
    ])
    if result.returncode != 0:
        raise AssertionError(result.stdout)
    report = output.read_text(encoding="utf-8")
    if "Google Fonts issue pending: no" not in report:
        raise AssertionError(report)
    if "Google Fonts Add Font issue has not been recorded" in report:
        raise AssertionError(report)
    if "Downstream PR draft ready: yes" not in report:
        raise AssertionError(report)
    if "downstream PR draft is not final" in report:
        raise AssertionError(report)


def assert_invalid_values_are_rejected(work: Path, base_values: dict[str, str]) -> None:
    cases = [
        ("branch with spaces", {"branch": "release candidate"}),
        ("branch traversal", {"branch": "release..candidate"}),
        ("branch metacharacters", {"branch": "release@{candidate}"}),
    ]
    for label, changes in cases:
        values = {**base_values, **changes}
        values_path = work / f"invalid-{label.replace(' ', '-')}.json"
        values_path.write_text(json.dumps(values, indent=2) + "\n", encoding="utf-8")
        result = run([
            sys.executable,
            str(SCRIPT),
            "--values",
            str(values_path),
            "--metadata",
            str(work / "metadata.md"),
            "--decision-sheet",
            str(work / "decisions.md"),
            "--issue-draft",
            str(work / "issue.md"),
            "--handoff",
            str(work / "handoff.md"),
        ])
        if result.returncode == 0:
            raise AssertionError(f"Expected invalid values to fail: {label}")
        if "branch must" not in result.stdout:
            raise AssertionError(result.stdout)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="blocksync-final-values.") as tmp:
        work = Path(tmp)
        metadata = work / "metadata.md"
        decisions = work / "decisions.md"
        issue = work / "issue.md"
        handoff = work / "handoff.md"
        ofl = work / "OFL.txt"
        sources = work / "sources"
        values_path = work / "values.json"

        shutil.copyfile(ROOT / "documentation" / "google-fonts-downstream-metadata-draft.md", metadata)
        shutil.copyfile(ROOT / "documentation" / "google-fonts-final-decision-sheet.md", decisions)
        shutil.copyfile(ROOT / "documentation" / "google-fonts-add-font-issue-draft.md", issue)
        shutil.copyfile(ROOT / "documentation" / "google-fonts-submission-handoff.md", handoff)
        shutil.copyfile(ROOT / "OFL.txt", ofl)
        (sources / "Blocksync-Regular.ufo").mkdir(parents=True)
        shutil.copyfile(
            ROOT / "sources" / "Blocksync-Regular.ufo" / "fontinfo.plist",
            sources / "Blocksync-Regular.ufo" / "fontinfo.plist",
        )

        values = {
            "date_added": "2026-05-30",
            "source_commit": "0123456789abcdef0123456789abcdef01234567",
            "repository_url": "https://github.com/example/blocksync-final",
            "branch": "main",
            "designer": "Example Designer",
            "package_source_strategy": "config_yaml",
            "archive_url": "",
            "namecheck_result": "namecheck.fontdata.com cleared Blocksync on 2026-05-30",
            "ai_use_disclosure": "No generative AI was used to draw final outlines.",
            "authorship_cla_rfn_status": "Authorship, CLA identity, and no-RFN status confirmed.",
            "fontspector_warning_decision": "Accept remaining three WARNs for first Google Fonts review.",
            "visual_proof_decision": "Proof reviewed and accepted.",
            "generated_composites_decision": "Generated Latin Extended and Vietnamese composites accepted.",
            "static_ttf_decision": "Static TTFs remain proof-only outputs unless Google Fonts asks for them.",
            "release_archive_fallback_decision": "Use only if Google Fonts rejects source.config_yaml.",
            "google_fonts_issue_url": "https://github.com/google/fonts/issues/1234",
        }
        values_path.write_text(json.dumps(values, indent=2) + "\n", encoding="utf-8")
        assert_invalid_values_are_rejected(work, values)

        check = run([
            sys.executable,
            str(SCRIPT),
            "--values",
            str(values_path),
            "--metadata",
            str(metadata),
            "--decision-sheet",
            str(decisions),
            "--issue-draft",
            str(issue),
            "--handoff",
            str(handoff),
            "--ofl",
            str(ofl),
            "--sources-dir",
            str(sources),
        ])
        if check.returncode != 0:
            print(check.stdout)
            return check.returncode

        apply = run([
            sys.executable,
            str(SCRIPT),
            "--values",
            str(values_path),
            "--metadata",
            str(metadata),
            "--decision-sheet",
            str(decisions),
            "--issue-draft",
            str(issue),
            "--handoff",
            str(handoff),
            "--ofl",
            str(ofl),
            "--sources-dir",
            str(sources),
            "--apply",
        ])
        if apply.returncode != 0:
            print(apply.stdout)
            return apply.returncode

        metadata_text = metadata.read_text(encoding="utf-8")
        decision_text = decisions.read_text(encoding="utf-8")
        issue_text = issue.read_text(encoding="utf-8")
        handoff_text = handoff.read_text(encoding="utf-8")
        ofl_text = ofl.read_text(encoding="utf-8")
        fontinfo_text = (sources / "Blocksync-Regular.ufo" / "fontinfo.plist").read_text(encoding="utf-8")

        checks = {
            "date_added applied": 'date_added: "2026-05-30"' in metadata_text,
            "commit applied": 'commit: "0123456789abcdef0123456789abcdef01234567"' in metadata_text,
            "designer applied": 'designer: "Example Designer"' in metadata_text,
            "repository URL applied": 'repository_url: "https://github.com/example/blocksync-final"' in metadata_text,
            "metadata copyright URL applied": "Copyright 2023 The Blocksyncer Project Authors (https://github.com/example/blocksync-final)" in metadata_text,
            "decision sheet date answered": "| Google Fonts `date_added` | `PENDING-YYYY-MM-DD` | 2026-05-30 |" in decision_text,
            "decision sheet designer answered": "| Designer string | `Eli Heuer` | Example Designer |" in decision_text,
            "issue designer applied": "designer string `Example Designer` confirmed" in issue_text,
            "issue AI disclosure applied": "AI-use disclosure: No generative AI was used to draw final outlines." in issue_text,
            "handoff applied values section": "## Applied Final Values" in handoff_text,
            "handoff issue URL applied": "Google Fonts issue exists: https://github.com/google/fonts/issues/1234" in handoff_text,
            "OFL copyright URL applied": ofl_text.startswith("Copyright 2023 The Blocksyncer Project Authors (https://github.com/example/blocksync-final)"),
            "UFO copyright URL applied": "Copyright 2023 The Blocksyncer Project Authors (https://github.com/example/blocksync-final)" in fontinfo_text,
        }
        failed = [label for label, ok in checks.items() if not ok]
        if failed:
            print("Failed checks:")
            for label in failed:
                print(f"- {label}")
            return 1

        try:
            assert_final_readiness_uses_applied_answers(work, metadata, decisions)
            assert_dependent_reports_use_applied_answers(work, decisions, issue)
            assert_downstream_readiness_sees_issue(work, metadata, handoff)
        except AssertionError as error:
            print(error)
            return 1

    print("Final values helper tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
